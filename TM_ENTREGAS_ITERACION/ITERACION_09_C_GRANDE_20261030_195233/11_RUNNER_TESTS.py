#!/usr/bin/env python3
"""ITERACION 09 — baseline endurecido + C Grande + C usada como tendencia.

Clasificacion separada:
  CANONICAL_PASS            regla cerrada, no depende de politica provisional
  PROVISIONAL_POLICY_PASS   depende de la autonomia provisional del retorno
  OPEN_RULE_BLOCK           la regla esta bloqueada por decision abierta
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
ROOT_DIR = HERE.parent
ENGINE = ROOT_DIR / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))

_MODULE = importlib.import_module(
    os.environ.get("TM_READER_MODULE", "tm_reference_interpreter_v1_direct_aut"))
Reader = _MODULE.Reader
Tick = _MODULE.Tick
load_ticks = _MODULE.load_ticks
FEED = _MODULE.FEED


def build(bars):
    ts, s = [], 1
    for bar, ps in enumerate(bars):
        for i, p in enumerate(ps):
            ts.append(Tick(s, bar * 60_000 + i * 100, bar, p))
            s += 1
    return ts


def run(bars, rid="C"):
    return Reader(build(bars), reading_id=rid).run()


BASE = [[10000, 9000], [9000, 9000]]
BG = BASE + [[9000, 9500, 9250, 9200, 9000]]       # A=500, B=500 -> B Grande


def c_tests():
    res = []

    def check(tid, kind, desc, cond, detail):
        res.append({"test_id": tid, "transition": "C", "kind": kind,
                    "classification": "PROVISIONAL_POLICY_PASS",
                    "description": desc, "pass": bool(cond), "detail": detail})

    r_open = run(BG + [[9000, 9200]], "C_OPEN")
    check("C-01", "positive", "C nace despues de B Grande",
          r_open.reading.c_status == "C_GRANDE"
          and "C_GRANDE" in [e["event"] for e in r_open.events],
          f"c={r_open.reading.c_status} phase={r_open.reading.phase}")

    check("C-02", "positive", "origen de C en el extremo final de B",
          r_open.reading.c_origin == r_open.reading.b_extreme == 9000,
          f"c_origin={r_open.reading.c_origin} b_extreme={r_open.reading.b_extreme}")

    check("C-03", "positive", "direccion de C contraria a B",
          r_open.reading.c_dir == -r_open.reading.b_dir,
          f"c_dir={r_open.reading.c_dir} b_dir={r_open.reading.b_dir}")

    check("C-04", "negative", "B Grande queda historica y pierde autoridad",
          r_open.reading.b_authority == "ARCHIVED"
          and r_open.reading.c_authority == "LIVE"
          and r_open.reading.active_function == "C",
          f"b_auth={r_open.reading.b_authority} c_auth={r_open.reading.c_authority} "
          f"active={r_open.reading.active_function}")

    r_xbar = run(BG + [[9000, 9200], [9200, 9400]], "C_XBAR")
    check("C-05", "positive", "C continua entre velas sin reiniciarse",
          r_xbar.reading.c_extreme == 9400 and r_xbar.reading.c_origin == 9000,
          f"c_extreme={r_xbar.reading.c_extreme} origin={r_xbar.reading.c_origin}")

    r_touch = run(BG + [[9000, 9200, 10000]], "C_TOUCH")
    check("C-06", "boundary", "C toca exactamente la base -> no se transforma",
          r_touch.reading.trend_status == ""
          and r_touch.reading.new_one_status == ""
          and r_touch.reading.c_extreme == 10000,
          f"trend={r_touch.reading.trend_status} n={r_touch.reading.new_one_status} "
          f"c_extreme={r_touch.reading.c_extreme}")

    r_cross = run(BG + [[9000, 9200, 10001]], "C_CROSS")
    check("C-07", "positive", "C supera la base -> C usada como tendencia",
          r_cross.reading.trend_status == "C_USED_AS_TREND"
          and r_cross.reading.new_one_status == "NEW_ONE_ACTIVE"
          and r_cross.reading.transition_reason == "C_USED_AS_TREND",
          f"trend={r_cross.reading.trend_status} "
          f"reason={r_cross.reading.transition_reason}")

    r_jump = run(BG + [[9000, 9200], [9200, 10500]], "C_JUMP")
    check("C-08", "positive", "salto sobre la base -> nuevo 1 en ese tick",
          r_jump.reading.trend_status == "C_USED_AS_TREND"
          and r_jump.reading.n_extreme == 10500,
          f"trend={r_jump.reading.trend_status} n_extreme={r_jump.reading.n_extreme}")

    check("C-09", "positive", "nuevo 1 hereda C (origen, direccion, st)",
          r_cross.reading.n_origin == r_cross.reading.c_origin
          and r_cross.reading.n_dir == r_cross.reading.c_dir
          and r_cross.reading.n_st == r_cross.reading.c_origin_st,
          f"n_origin={r_cross.reading.n_origin} c_origin={r_cross.reading.c_origin} "
          f"n_dir={r_cross.reading.n_dir} n_st={r_cross.reading.n_st} "
          f"c_st={r_cross.reading.c_origin_st}")

    r_ext = run(BG + [[9000, 9200, 10001], [10001, 10200]], "C_EXT")
    check("C-10", "positive", "extension posterior pertenece al nuevo 1",
          r_ext.reading.n_extreme == 10200 and r_ext.reading.c_extreme == 10001
          and r_ext.reading.c_authority == "ARCHIVED",
          f"n_extreme={r_ext.reading.n_extreme} c_extreme={r_ext.reading.c_extreme} "
          f"c_auth={r_ext.reading.c_authority}")

    check("C-11", "negative", "C no depende del 100% de A para confirmarse",
          r_open.reading.c_status == "C_GRANDE"
          and r_open.reading.b_size == r_open.reading.a_size,
          f"b={r_open.reading.b_size} a={r_open.reading.a_size} "
          f"c={r_open.reading.c_status}")

    check("C-12", "negative", "no coexisten autoridad B y C activas",
          r_open.reading.b_authority == "ARCHIVED"
          and r_open.reading.active_function == "C"
          and r_ext.reading.active_function == "NEW_ONE"
          and r_ext.reading.c_authority == "ARCHIVED",
          f"open: b={r_open.reading.b_authority} active={r_open.reading.active_function}; "
          f"trend: c={r_ext.reading.c_authority} active={r_ext.reading.active_function}")

    # determinismo / prefijo del bloque C
    bars = BG + [[9000, 9200, 10001], [10001, 10200]]
    a = run(bars, "C_DET").trace
    b = run(bars, "C_DET").trace
    check("C-DET", "determinism", "doble ejecucion identica en C",
          a == b, f"len={len(a)}")
    full = Reader(build(bars), reading_id="C_PRE").run().trace
    pref = Reader(build(bars)[:14], reading_id="C_PRE").run().trace
    check("C-PRE", "prefix", "prefijo consistente en C",
          len(pref) > 0 and pref == full[:len(pref)],
          f"prefix={len(pref)} full={len(full)}")
    return res


def _sub(script):
    env = dict(os.environ)
    env["TM_READER_MODULE"] = "tm_reference_interpreter_v1_direct_aut"
    out = subprocess.run([sys.executable, str(HERE / script)], cwd=str(ROOT_DIR),
                         env=env, capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        print(out.stdout[-1500:]); print(out.stderr[-1500:])
        raise SystemExit(f"{script} rc={out.returncode}")


CANONICAL_IDS = {"A-01", "A-09", "A-14", "AD-BLOCK"}
BLOCKED_IDS = {"A-04"}


def classify(block, row):
    tid = row["test_id"]
    if block == "core":
        return "CANONICAL_PASS"
    if tid in CANONICAL_IDS:
        return "CANONICAL_PASS"
    if tid in BLOCKED_IDS:
        return "OPEN_RULE_BLOCK"
    return "PROVISIONAL_POLICY_PASS"


def main() -> int:
    _sub("run_core_tests.py")
    _sub("run_ab_candidate_tests.py")
    _sub("run_direct_aut_tests.py")

    core = json.loads((HERE / "CORE_TEST_RESULTS.json").read_text(encoding="utf-8"))
    ab = json.loads((HERE / "AB_CANDIDATE_TEST_RESULTS.json").read_text(encoding="utf-8"))
    ad = json.loads((HERE / "DIRECT_AUT_TEST_RESULTS.json").read_text(encoding="utf-8"))

    rows = []
    for block, path in (("core", "CORE_TEST_RESULTS.csv"),
                        ("ab", "AB_CANDIDATE_TEST_RESULTS.csv"),
                        ("ad", "DIRECT_AUT_TEST_RESULTS.csv")):
        with (HERE / path).open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                rows.append({"test_id": row["test_id"], "block": block,
                             "classification": classify(block, row),
                             "pass": row["pass"] in ("True", "true", "1"),
                             "description": row["description"]})

    c_res = c_tests()
    rows.extend({"test_id": x["test_id"], "block": "c",
                 "classification": x["classification"], "pass": x["pass"],
                 "description": x["description"]} for x in c_res)

    with (HERE / "C_TEST_RESULTS.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["test_id", "transition", "kind",
                                           "classification", "description",
                                           "pass", "detail"])
        w.writeheader(); w.writerows(c_res)

    def count(cls):
        sel = [r for r in rows if r["classification"] == cls]
        return {"tests": len(sel), "passed": sum(r["pass"] for r in sel),
                "all_pass": all(r["pass"] for r in sel) if sel else True}

    groups = {k: count(k) for k in
              ("CANONICAL_PASS", "PROVISIONAL_POLICY_PASS", "OPEN_RULE_BLOCK")}
    total = len(rows)
    passed = sum(1 for r in rows if r["pass"])
    summary = {
        "reader": _MODULE.CORE_VERSION,
        "reader_file": "tm_reference_interpreter_v1_direct_aut.py",
        "iteration": "09",
        "tests_total": total,
        "tests_passed": passed,
        "tests_failed": total - passed,
        "all_pass": passed == total,
        "classification": groups,
        "blocks": {"core": core["tests"], "b_grande_aut_by_b": ab["tests"],
                   "aut_direct_by_a": ad["tests"], "c_grande_trend": len(c_res)},
        "provisional_policies": ["return autonomy: contrary + own extension"],
        "open_rule_blocks": ["CUT", "FT", "gap new-1", "concurrency",
                             "AUT direct with A pending"],
    }
    (HERE / "ITERATION_09_TEST_RESULTS.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    for x in c_res:
        print(("PASS" if x["pass"] else "FAIL"), x["test_id"], x["description"],
              "|", x["detail"])
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
