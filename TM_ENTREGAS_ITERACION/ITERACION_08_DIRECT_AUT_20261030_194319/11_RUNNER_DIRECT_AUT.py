#!/usr/bin/env python3
"""ITARACION 08 — tests de AUT directo por A + consolidacion CORE/BG.

El interprete de referencia es `tm_reference_interpreter_v1_direct_aut`.
RESULTADOS:
  * CORE_TEST_RESULTS.csv/json      (via run_core_tests.py)
  * AB_CANDIDATE_TEST_RESULTS.csv/json (via run_ab_candidate_tests.py)
  * DIRECT_AUT_TEST_RESULTS.csv/json (este runner)
  * ITERATION_08_TEST_RESULTS.json   (consolidado)
"""
from __future__ import annotations

import csv
import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))

_MODULE = importlib.import_module(
    os.environ.get("TM_READER_MODULE", "tm_reference_interpreter_v1_direct_aut"))
Reader = _MODULE.Reader
Tick = _MODULE.Tick


def build(bars: list[list[int]]) -> list[Tick]:
    ticks = []
    seq = 1
    for bar, prices in enumerate(bars):
        for i, price in enumerate(prices):
            ticks.append(Tick(seq, bar * 60_000 + i * 100, bar, price))
            seq += 1
    return ticks


def run(bars: list[list[int]], rid: str = "AD") -> Reader:
    return Reader(build(bars), reading_id=rid).run()


# Modulo bajista 10000 -> 9000 al cierre de la vela 1 (2 imposible).
# Base del modulo = mod_origin = 10000. A contraria (alcista) nace en 9000.
BASE = [[10000, 9000], [9000, 9000]]


def direct_aut_tests() -> tuple[list[dict], int, int]:
    results: list[dict] = []

    def check(tid, transition, kind, desc, cond, detail):
        results.append({"test_id": tid, "transition": transition, "kind": kind,
                        "description": desc, "pass": bool(cond),
                        "detail": detail})

    # AD-01: A toca exactamente la base -> sin AUT directo.
    r = run(BASE + [[9000, 9500, 10000]], "AD_T001")
    check("AD-01", "AUT_DIRECT", "boundary",
          "A toca exactamente la base -> no AUT directo todavia",
          r.reading.aut_direct_status == ""
          and r.reading.a_status in ("A_CONFIRMED", "CONTRARY_MOVE_PENDING", "")
          and r.reading.new_one_status == "",
          f"aut={r.reading.aut_direct_status} a={r.reading.a_status} "
          f"n={r.reading.new_one_status} a_extreme={r.reading.a_extreme} "
          f"base={r.reading.mod_origin}")

    # AD-02: superacion estricta por 1 cent -> AUT directo.
    r2 = run(BASE + [[9000, 9500, 10001]], "AD_T002")
    check("AD-02", "AUT_DIRECT", "positive",
          "A supera la base por un tick minimo -> AUT directo",
          r2.reading.aut_direct_status == "AUT_DIRECT_BY_A"
          and r2.reading.new_one_status == "NEW_ONE_ACTIVE"
          and r2.reading.aut_direct_kt != 0,
          f"aut={r2.reading.aut_direct_status} n={r2.reading.new_one_status} "
          f"kt={r2.reading.aut_direct_kt}")

    # AD-03: salto de debajo a encima en un solo tick.
    r3 = run(BASE + [[9000, 10500]], "AD_T003")
    check("AD-03", "AUT_DIRECT", "positive",
          "A salta desde debajo hasta encima -> AUT directo en el mismo tick",
          r3.reading.aut_direct_status == "AUT_DIRECT_BY_A"
          and r3.reading.new_one_status == "NEW_ONE_ACTIVE"
          and r3.reading.n_extreme == 10500,
          f"aut={r3.reading.aut_direct_status} n_extreme={r3.reading.n_extreme}")

    # AD-04: A continua despues del AUT -> extiende nuevo 1.
    r4 = run(BASE + [[9000, 9500, 10001], [10001, 10200]], "AD_T004")
    check("AD-04", "AUT_DIRECT", "positive",
          "A continua despues del AUT -> extiende nuevo 1",
          r4.reading.new_one_status == "NEW_ONE_ACTIVE"
          and r4.reading.n_extreme == 10200
          and r4.reading.n_size == 1200,
          f"n_extreme={r4.reading.n_extreme} n_size={r4.reading.n_size}")

    # AD-05: no existe B en la via directa, ni siquiera al extender el nuevo 1.
    check("AD-05", "AUT_DIRECT", "negative",
          "no existe B en la via directa (tampoco tras extension)",
          r2.reading.b_status == "" and r2.reading.b_grande_kt == 0
          and r2.reading.active_function == "NEW_ONE"
          and r4.reading.b_status == "" and r4.reading.aut_status == "",
          f"b={r2.reading.b_status} b_tras_ext={r4.reading.b_status} "
          f"aut_b={r4.reading.aut_status} b_grande_kt={r2.reading.b_grande_kt} "
          f"active={r2.reading.active_function}")

    # AD-06: no se aplica 127%+0,25 en la via directa.
    check("AD-06", "AUT_DIRECT", "negative",
          "no se aplica 127%+0,25 en la via directa",
          r2.reading.aut_direct_status == "AUT_DIRECT_BY_A"
          and r2.reading.b_grande_status in ("", "B_GRANDE")
          and r2.reading.aut_status == "",
          f"aut_direct={r2.reading.aut_direct_status} "
          f"b_grande={r2.reading.b_grande_status} aut_b={r2.reading.aut_status}")

    # AD-07: nuevo 1 conserva origen de A.
    check("AD-07", "AUT_DIRECT", "positive",
          "nuevo 1 conserva origen de A",
          r2.reading.n_origin == r2.reading.a_origin == 9000,
          f"n_origin={r2.reading.n_origin} a_origin={r2.reading.a_origin}")

    # AD-08: structural_time del nuevo 1 = structural_time de A.
    check("AD-08", "AUT_DIRECT", "positive",
          "structural_time del nuevo 1 = structural_time de A",
          r2.reading.n_st == r2.reading.a_origin_st and r2.reading.n_st > 0,
          f"n_st={r2.reading.n_st} a_origin_st={r2.reading.a_origin_st}")

    # AD-09: knowledge_time = primer tick de cruce.
    cross_kt = [t.time_ms for t in build(BASE + [[9000, 9500, 10001]])
                if t.bar == 2 and t.price == 10001][0]
    check("AD-09", "AUT_DIRECT", "positive",
          "knowledge_time = primer tick de cruce",
          r2.reading.aut_direct_kt == cross_kt
          and r2.reading.n_kt == r2.reading.aut_direct_kt,
          f"aut_direct_kt={r2.reading.aut_direct_kt} cross_kt={cross_kt} "
          f"n_kt={r2.reading.n_kt}")

    # AD-10: A archivada y sin autoridad activa.
    check("AD-10", "AUT_DIRECT", "negative",
          "A queda archivada y pierde autoridad activa",
          r2.reading.a_authority == "ARCHIVED"
          and r2.reading.a_status == "A_CONFIRMED_ARCHIVED"
          and r2.reading.active_function == "NEW_ONE",
          f"a_authority={r2.reading.a_authority} a_status={r2.reading.a_status} "
          f"active={r2.reading.active_function}")

    # AD-11: modulo como referencia congelada.
    check("AD-11", "AUT_DIRECT", "negative",
          "modulo queda como referencia congelada",
          r2.reading.module_authority == "FROZEN_REFERENCE",
          f"module_authority={r2.reading.module_authority}")

    # AD-12: tocar base y retroceder -> no AUT directo.
    r12 = run(BASE + [[9000, 9500, 10000], [10000, 9800, 9700]], "AD_T012")
    check("AD-12", "AUT_DIRECT", "boundary",
          "tocar base y retroceder -> no AUT directo",
          r12.reading.aut_direct_status == "",
          f"aut={r12.reading.aut_direct_status} a={r12.reading.a_status} "
          f"a_extreme={r12.reading.a_extreme}")

    # AD-13: cruce dentro de la misma vela.
    r13 = run(BASE + [[9000, 9500, 10000, 10001]], "AD_T013")
    check("AD-13", "AUT_DIRECT", "positive",
          "cruce dentro de la misma vela",
          r13.reading.aut_direct_status == "AUT_DIRECT_BY_A"
          and r13.reading.n_kt // 60_000 == 2,
          f"aut={r13.reading.aut_direct_status} aut_kt={r13.reading.aut_direct_kt}")

    # AD-14: cruce entre velas sin reiniciar A.
    r14 = run(BASE + [[9000, 9500, 10000], [10000, 10001]], "AD_T014")
    check("AD-14", "AUT_DIRECT", "positive",
          "cruce entre velas sin reiniciar A",
          r14.reading.aut_direct_status == "AUT_DIRECT_BY_A"
          and r14.reading.a_origin == 9000
          and r14.reading.n_origin == 9000,
          f"aut={r14.reading.aut_direct_status} a_origin={r14.reading.a_origin} "
          f"n_origin={r14.reading.n_origin}")

    # AD-DET: doble ejecucion identica.
    a = run(BASE + [[9000, 9500, 10001], [10001, 10200]], "AD_DET").trace
    b = run(BASE + [[9000, 9500, 10001], [10001, 10200]], "AD_DET").trace
    check("AD-DET", "global", "determinism",
          "doble ejecucion identica en la via directa",
          a == b, f"len_a={len(a)} len_b={len(b)}")

    # AD-PRE: prefijo consistente.
    full_ticks = build(BASE + [[9000, 9500, 10001], [10001, 10200]])
    full = Reader(full_ticks, reading_id="AD_PRE").run().trace
    pref = Reader(full_ticks[:6], reading_id="AD_PRE").run().trace
    check("AD-PRE", "global", "prefix",
          "prefijo consistente en la via directa",
          len(pref) > 0 and pref == full[:len(pref)],
          f"prefix={len(pref)} full={len(full)}")

    return results, sum(x["pass"] for x in results), len(results)


def _run_sub(script: str) -> dict:
    env = dict(os.environ)
    env["TM_READER_MODULE"] = "tm_reference_interpreter_v1_direct_aut"
    out = subprocess.run([sys.executable, str(HERE / script)],
                         cwd=str(HERE.parent), env=env,
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        print(out.stdout[-2000:])
        print(out.stderr[-2000:])
        raise SystemExit(f"subprocess {script} failed rc={out.returncode}")
    return {"stdout": out.stdout, "stderr": out.stderr}


def main() -> int:
    _run_sub("run_core_tests.py")
    _run_sub("run_ab_candidate_tests.py")

    core = json.loads((HERE / "CORE_TEST_RESULTS.json").read_text(encoding="utf-8"))
    ab = json.loads((HERE / "AB_CANDIDATE_TEST_RESULTS.json").read_text(encoding="utf-8"))

    ad_results, ad_pass, ad_total = direct_aut_tests()
    with (HERE / "DIRECT_AUT_TEST_RESULTS.csv").open(
            "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["test_id", "transition", "kind",
                                           "description", "pass", "detail"])
        w.writeheader()
        w.writerows(ad_results)

    ad_summary = {
        "reader": _MODULE.CORE_VERSION,
        "tests": ad_total,
        "passed": ad_pass,
        "failed": ad_total - ad_pass,
        "all_pass": ad_pass == ad_total,
        "scope": "AUT directo por A (iteracion 08)",
    }
    (HERE / "DIRECT_AUT_TEST_RESULTS.json").write_text(
        json.dumps(ad_summary, indent=2) + "\n", encoding="utf-8")

    total = core["tests"] + ab["tests"] + ad_total
    passed = core["passed"] + ab["passed"] + ad_pass
    consolidated = {
        "reader": _MODULE.CORE_VERSION,
        "reader_file": "tm_reference_interpreter_v1_direct_aut.py",
        "tests": total,
        "passed": passed,
        "failed": total - passed,
        "all_pass": passed == total,
        "blocks": {
            "core": {"tests": core["tests"], "passed": core["passed"],
                     "all_pass": core["all_pass"]},
            "b_grande_aut_by_b": {"tests": ab["tests"], "passed": ab["passed"],
                                  "all_pass": ab["all_pass"]},
            "aut_direct_by_a": {"tests": ad_total, "passed": ad_pass,
                                "all_pass": ad_pass == ad_total},
        },
        "experimental_policies_removed": ["P-AB-04_RETURN_JUMP_4"],
        "open_rule_blocks": ["C", "CUT", "TT", "FT", "gap new-1", "concurrency"],
    }
    (HERE / "ITERATION_08_TEST_RESULTS.json").write_text(
        json.dumps(consolidated, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(consolidated, indent=2))
    for x in ad_results:
        print(("PASS" if x["pass"] else "FAIL"), x["test_id"],
              x["description"], "|", x["detail"])
    return 0 if consolidated["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
