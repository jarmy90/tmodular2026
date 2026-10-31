#!/usr/bin/env python3
"""ITERACION 09 — AD (AUT directo por A) con baseline endurecido.

Precondicion canonica: A_CONFIRMED antes de cruzar la base.
Si un movimiento pendiente cruza la base -> OPEN_RULE_BLOCK (AD-BLOCK).
"""
from __future__ import annotations

import csv
import importlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))
from tm_reader_guard import verify as _verify_reader  # noqa: E402
_verify_reader()

_MODULE = importlib.import_module(
    os.environ.get("TM_READER_MODULE", "tm_reference_interpreter_v1_direct_aut"))
Reader = _MODULE.Reader
Tick = _MODULE.Tick


def build(bars):
    ticks, seq = [], 1
    for bar, prices in enumerate(bars):
        for i, price in enumerate(prices):
            ticks.append(Tick(seq, bar * 60_000 + i * 100, bar, price))
            seq += 1
    return ticks


def run(bars, rid="AD"):
    return Reader(build(bars), reading_id=rid).run()


# Modulo bajista 1+2: origin 10000, extreme 9000 -> base del modulo 10000.
BASE = [[10000, 9000], [9000, 9000]]
# A nace en 9000, sube a 9500, retorno a 9150 confirma A y abre B candidata.
A_CONF = [[9000, 9500, 9200, 9150]]
# B candidata absorbida por extension de A; A reabierta en 9600 (< base).
B_ABSORBED = [[9150, 9600]]


def tests():
    res = []

    def check(tid, kind, desc, cond, detail, cls="CANONICAL_PASS"):
        res.append({"test_id": tid, "transition": "AUT_DIRECT", "kind": kind,
                    "classification": cls, "description": desc,
                    "pass": bool(cond), "detail": detail})

    # AD-BLOCK: pendiente cruza base -> bloqueado, sin nuevo 1.
    rb = run(BASE + [[9000, 10100]], "AD_BLOCK")
    check("AD-BLOCK", "negative",
          "A pendiente cruza la base -> OPEN_RULE_BLOCK sin inventar AUT",
          rb.reading.aut_direct_status == "OPEN_RULE_BLOCK"
          and rb.reading.new_one_status == ""
          and rb.reading.a_confirmations == 0,
          f"aut={rb.reading.aut_direct_status} n={rb.reading.new_one_status} "
          f"conf={rb.reading.a_confirmations}")

    # AD-01: A confirmada toca exactamente la base -> sin AUT.
    r1 = run(BASE + A_CONF + B_ABSORBED + [[9600, 10000]], "AD_T001")
    check("AD-01", "boundary", "A confirmada toca la base -> no AUT",
          r1.reading.aut_direct_status == "" and r1.reading.new_one_status == ""
          and r1.reading.a_confirmations == 1
          and r1.reading.a_extreme == 10000,
          f"aut={r1.reading.aut_direct_status} n={r1.reading.new_one_status} "
          f"a={r1.reading.a_extreme} base={r1.reading.mod_origin}",
          "PROVISIONAL_POLICY_PASS")

    # AD-02: supera por 1 cent -> AUT directo.
    r2 = run(BASE + A_CONF + B_ABSORBED + [[9600, 10001]], "AD_T002")
    check("AD-02", "positive", "A confirmada supera la base por 1 cent -> AUT",
          r2.reading.aut_direct_status == "AUT_DIRECT_BY_A"
          and r2.reading.new_one_status == "NEW_ONE_ACTIVE"
          and r2.reading.b_status == "",
          f"aut={r2.reading.aut_direct_status} n={r2.reading.new_one_status} "
          f"b={r2.reading.b_status}",
          "PROVISIONAL_POLICY_PASS")

    # AD-03: salto de debajo a encima en un tick.
    r3 = run(BASE + A_CONF + B_ABSORBED + [[9600, 10500]], "AD_T003")
    check("AD-03", "positive", "A salta de debajo a encima de la base en un tick",
          r3.reading.aut_direct_status == "AUT_DIRECT_BY_A"
          and r3.reading.n_extreme == 10500,
          f"aut={r3.reading.aut_direct_status} n_extreme={r3.reading.n_extreme}",
          "PROVISIONAL_POLICY_PASS")

    # AD-04: extension posterior del nuevo 1 (iteracion 12: al abrir la vela
    # siguiente el nuevo 1 se convierte en el 1 del ciclo nuevo).
    r4 = run(BASE + A_CONF + B_ABSORBED + [[9600, 10001], [10001, 10200]], "AD_T004")
    check("AD-04", "positive",
          "A continua tras el AUT y extiende el nuevo 1 (TT pendiente)",
          r4.reading.new_one_status == "NEW_ONE_ACTIVE"
          and r4.reading.n_extreme == 10200 and r4.reading.n_size == 1200
          and r4.reading.tt_status == "TT_PENDING"
          and r4.reading.cycle_id == 0,
          f"n={r4.reading.n_size}/{r4.reading.n_extreme} "
          f"tt={r4.reading.tt_status} cycle={r4.reading.cycle_id}",
          "PROVISIONAL_POLICY_PASS")

    # AD-05: no existe B en la via directa (ni tras extender).
    check("AD-05", "negative", "no existe B en la via directa",
          r2.reading.b_status == "" and r2.reading.b_grande_kt == 0
          and r4.reading.b_status == "" and r4.reading.aut_status == ""
          and r2.reading.active_function == "NEW_ONE",
          f"b={r2.reading.b_status} b_ext={r4.reading.b_status} "
          f"active={r2.reading.active_function}",
          "PROVISIONAL_POLICY_PASS")

    # AD-06: no se aplica 127%+0,25 en la via directa.
    check("AD-06", "negative", "no se aplica 127%+0,25 en la via directa",
          r2.reading.aut_direct_status == "AUT_DIRECT_BY_A"
          and r2.reading.aut_status == "" and r2.reading.b_grande_status == "",
          f"aut_direct={r2.reading.aut_direct_status} aut_b={r2.reading.aut_status}",
          "PROVISIONAL_POLICY_PASS")

    # AD-07/08/09: herencia de A.
    check("AD-07", "positive", "nuevo 1 conserva origen de A",
          r2.reading.n_origin == r2.reading.a_origin == 9000,
          f"n={r2.reading.n_origin} a={r2.reading.a_origin}",
          "PROVISIONAL_POLICY_PASS")
    check("AD-08", "positive", "structural_time nuevo 1 = structural de A",
          r2.reading.n_st == r2.reading.a_origin_st and r2.reading.n_st > 0,
          f"n_st={r2.reading.n_st} a_st={r2.reading.a_origin_st}",
          "PROVISIONAL_POLICY_PASS")
    cross = [t.time_ms for t in build(BASE + A_CONF + B_ABSORBED + [[9600, 10001]])
             if t.price == 10001][0]
    check("AD-09", "positive", "knowledge_time = primer tick de cruce",
          r2.reading.aut_direct_kt == cross and r2.reading.n_kt == cross,
          f"kt={r2.reading.aut_direct_kt} cross={cross}",
          "PROVISIONAL_POLICY_PASS")

    # AD-10/11: archivado.
    check("AD-10", "negative", "A archivada sin autoridad activa",
          r2.reading.a_authority == "ARCHIVED"
          and r2.reading.a_status == "A_CONFIRMED_ARCHIVED"
          and r2.reading.active_function == "NEW_ONE",
          f"a_auth={r2.reading.a_authority} a={r2.reading.a_status}",
          "PROVISIONAL_POLICY_PASS")
    check("AD-11", "negative", "modulo congelado como referencia",
          r2.reading.module_authority == "FROZEN_REFERENCE",
          f"mod_auth={r2.reading.module_authority}",
          "PROVISIONAL_POLICY_PASS")

    # AD-12: tocar base y retroceder.
    r12 = run(BASE + A_CONF + B_ABSORBED + [[9600, 10000], [10000, 9800, 9700]],
              "AD_T012")
    check("AD-12", "boundary", "tocar la base y retroceder -> no AUT",
          r12.reading.aut_direct_status == "",
          f"aut={r12.reading.aut_direct_status} a={r12.reading.a_status}",
          "PROVISIONAL_POLICY_PASS")

    # AD-13: cruce dentro de la misma vela.
    r13 = run(BASE + A_CONF + [[9150, 9600, 10000, 10001]], "AD_T013")
    check("AD-13", "positive", "cruce dentro de la misma vela",
          r13.reading.aut_direct_status == "AUT_DIRECT_BY_A",
          f"aut={r13.reading.aut_direct_status}",
          "PROVISIONAL_POLICY_PASS")

    # AD-14: cruce entre velas sin reiniciar A.
    r14 = run(BASE + A_CONF + [[9150, 9600], [9600, 10001]], "AD_T014")
    check("AD-14", "positive", "cruce entre velas sin reiniciar A",
          r14.reading.aut_direct_status == "AUT_DIRECT_BY_A"
          and r14.reading.a_origin == 9000 and r14.reading.n_origin == 9000,
          f"aut={r14.reading.aut_direct_status} a_origin={r14.reading.a_origin}",
          "PROVISIONAL_POLICY_PASS")

    # determinismo / prefijo
    bars = BASE + A_CONF + B_ABSORBED + [[9600, 10001], [10001, 10200]]
    a = run(bars, "AD_DET").trace
    b = run(bars, "AD_DET").trace
    check("AD-DET", "determinism", "doble ejecucion identica",
          a == b, f"len={len(a)}", "PROVISIONAL_POLICY_PASS")
    full = Reader(build(bars), reading_id="AD_PRE").run().trace
    pref = Reader(build(bars)[:12], reading_id="AD_PRE").run().trace
    check("AD-PRE", "prefix", "prefijo consistente",
          len(pref) > 0 and pref == full[:len(pref)],
          f"prefix={len(pref)} full={len(full)}", "PROVISIONAL_POLICY_PASS")
    return res


def main() -> int:
    res = tests()
    with (HERE / "DIRECT_AUT_TEST_RESULTS.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["test_id", "transition", "kind",
                                           "classification", "description",
                                           "pass", "detail"])
        w.writeheader()
        w.writerows(res)
    passed = sum(1 for x in res if x["pass"])
    summary = {"reader": _MODULE.CORE_VERSION, "tests": len(res),
               "passed": passed, "failed": len(res) - passed,
               "all_pass": passed == len(res),
               "canonical": sum(1 for x in res if x["classification"] == "CANONICAL_PASS"),
               "provisional": sum(1 for x in res if x["classification"] == "PROVISIONAL_POLICY_PASS"),
               "scope": "AUT directo con precondicion A_CONFIRMED"}
    (HERE / "DIRECT_AUT_TEST_RESULTS.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    for x in res:
        print(("PASS" if x["pass"] else "FAIL"), x["test_id"], x["classification"],
              x["description"], "|", x["detail"])
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
