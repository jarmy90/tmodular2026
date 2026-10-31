#!/usr/bin/env python3
"""ITERACION 10 — gap explicito y concurrencia L1/L2 (cero fugas)."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))

from tm_reference_interpreter_v1_direct_aut import (  # noqa: E402
    Reader, Tick, load_ticks, FEED,
)
from tm_concurrent_readings import (  # noqa: E402
    CompositeReader, ReadingSpec,
)


def build(bars):
    ts, s = [], 1
    for bar, ps in enumerate(bars):
        for i, p in enumerate(ps):
            ts.append(Tick(s, bar * 60_000 + i * 100, bar, p))
            s += 1
    return ts


def real(a, b):
    def bar_of(h):
        hh, mm = h.split(":")
        return int(hh) * 60 + int(mm)
    lo, hi = bar_of(a), bar_of(b)
    return [t for t in load_ticks(FEED) if lo <= t.bar % 1440 <= hi]


def main() -> int:
    res = []

    def check(tid, area, kind, desc, cond, detail, cls="CANONICAL_PASS"):
        res.append({"test_id": tid, "area": area, "kind": kind,
                    "classification": cls, "description": desc,
                    "pass": bool(cond), "detail": detail})

    # ---------------- GAP
    GAP = [[10000, 9800], [9830, 9850, 9900]]   # apertura 9830: |30| >= 25
    r = Reader(build(GAP), reading_id="GAP1").run()
    ev = [e["event"] for e in r.events]
    check("GAP-01", "gap", "positive",
          "apertura no plana registrada con sus estados",
          "NON_FLAT_OPEN_OBSERVED" in ev and "NO_TWO_BY_NON_FLAT_OPEN" in ev,
          f"ev={[e for e in ev if 'FLAT' in e or 'GAP' in e]}")
    check("GAP-02", "gap", "negative", "2 prohibido por apertura no plana",
          r.reading.two_status == "IMPOSSIBLE_NO_FLAT",
          f"two={r.reading.two_status}")
    check("GAP-03", "gap", "positive",
          "gap abre A implicita por descarte sin inventar precios",
          "GAP_IMPLICIT_TRANSITION" in ev
          and r.reading.a_status == "CONTRARY_MOVE_PENDING"
          and r.reading.a_origin == r.reading.mod_extreme,
          f"a={r.reading.a_status} a_origin={r.reading.a_origin} "
          f"mod_extreme={r.reading.mod_extreme}")
    check("GAP-04", "gap", "negative",
          "gap no inventa ticks ni precios internos",
          len(r.trace) == len(build(GAP)),
          f"trace={len(r.trace)} ticks={len(build(GAP))}")

    CONT = [[10000, 9800], [9830, 9850], [9850, 9900]]
    rc = Reader(build(CONT), reading_id="GAP_CONT").run()
    evc = [e["event"] for e in rc.events]
    check("GAP-05", "gap", "positive",
          "funcion viva no se divide al cambiar de vela",
          "CONTINUATION_ACROSS_BAR" in evc
          and rc.reading.a_origin == rc.reading.mod_extreme,
          f"cont={'CONTINUATION_ACROSS_BAR' in evc} "
          f"a_origin={rc.reading.a_origin} mod_extreme={rc.reading.mod_extreme}")

    # ---------------- CONCURRENCIA
    l1_ticks = real("16:15", "16:18")
    l2_ticks = real("16:19", "16:22")
    solo_l1 = Reader(l1_ticks, reading_id="L1").run()
    solo_l2 = Reader(l2_ticks, reading_id="L2").run()

    comp = CompositeReader([
        ReadingSpec("L1", l1_ticks, parent_reading_id=""),
        ReadingSpec("L2", l2_ticks, parent_reading_id="L1"),
    ]).run()

    check("CONC-01", "concurrency", "positive",
          "L1 aislada == L1 en composicion (sin interferencia)",
          comp.states["L1"] == solo_l1.summary(),
          f"equal={comp.states['L1'] == solo_l1.summary()}")
    check("CONC-02", "concurrency", "positive",
          "L2 aislada == L2 en composicion (sin interferencia)",
          comp.states["L2"] == solo_l2.summary(),
          f"equal={comp.states['L2'] == solo_l2.summary()}")
    ids = [x["reading_id"] for x in comp.readings]
    check("CONC-03", "concurrency", "negative",
          "ids propios y parent correcto, sin tercera escala",
          ids == ["L1", "L2"]
          and comp.readings[1]["parent_reading_id"] == "L1",
          f"ids={ids} parent={comp.readings[1]['parent_reading_id']}")
    check("CONC-04", "concurrency", "negative",
          "cero fugas entre lecturas",
          comp.ok(), f"leaks={comp.leaks}")

    comp2 = CompositeReader([
        ReadingSpec("L1", l1_ticks, ""),
        ReadingSpec("L2", l2_ticks, "L1"),
    ]).run()
    check("CONC-05", "concurrency", "determinism",
          "doble composicion identica",
          comp2.states == comp.states, "deterministic")

    third_blocked = False
    try:
        CompositeReader([ReadingSpec("L1", l1_ticks),
                         ReadingSpec("L2", l2_ticks, "L1"),
                         ReadingSpec("L3", l1_ticks, "L1")])
    except ValueError:
        third_blocked = True
    check("CONC-06", "concurrency", "negative",
          "tercera escala prohibida sin regla expresa",
          third_blocked, f"blocked={third_blocked}")

    with (HERE / "GAP_CONCURRENCY_TEST_RESULTS.csv").open(
            "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["test_id", "area", "kind",
                                           "classification", "description",
                                           "pass", "detail"])
        w.writeheader(); w.writerows(res)

    passed = sum(1 for x in res if x["pass"])
    summary = {
        "iteration": "10",
        "reader": "TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT",
        "tests": len(res), "passed": passed, "failed": len(res) - passed,
        "all_pass": passed == len(res),
        "leaks": comp.leaks,
        "scope": "gap explicito + concurrencia L1/L2",
    }
    (HERE / "ITERATION_10_TEST_RESULTS.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    for x in res:
        print(("PASS" if x["pass"] else "FAIL"), x["test_id"], x["description"],
              "|", x["detail"])
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
