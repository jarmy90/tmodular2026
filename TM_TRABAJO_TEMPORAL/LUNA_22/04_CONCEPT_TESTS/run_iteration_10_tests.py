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
from tm_reader_guard import verify as _verify_reader  # noqa: E402
_verify_reader()

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
    # v2.19: the gap is resolved as implicit A -> B Grande -> A as trend and
    # a new 1 born at the negotiated opening (not as a module by discard).
    check("GAP-03", "gap", "positive",
          "gap resuelve A/B Grande/tendencia implicitos y nuevo 1 en la apertura",
          "GAP_IMPLICIT_SEQUENCE" in ev and "GAP_IMPLICIT_NEW_ONE" in ev
          and r.reading.new_one_status == "NEW_ONE_ACTIVE"
          and r.reading.n_origin == 9830
          and r.reading.n_dir == 1
          and r.reading.n_st == r.reading.n_kt,
          f"one={r.reading.new_one_status} origin={r.reading.n_origin} "
          f"dir={r.reading.n_dir}")
    check("GAP-03b", "gap", "negative",
          "el gap no se mide como una unica A desde el extremo previo",
          r.reading.a_status == "" and r.reading.new_one_status == "NEW_ONE_ACTIVE",
          f"a={r.reading.a_status!r} one={r.reading.new_one_status}")
    check("GAP-04", "gap", "negative",
          "gap no inventa ticks ni precios internos",
          len(r.trace) == len(build(GAP)),
          f"trace={len(r.trace)} ticks={len(build(GAP))}")

    CONT = [[10000, 9800], [9830, 9850], [9850, 9900]]
    rc = Reader(build(CONT), reading_id="GAP_CONT").run()
    evc = [e["event"] for e in rc.events]
    # Iteracion 16 (RC-1, derivado de v005 16:25-16:26): el nuevo 1 nacido de
    # un gap NO rota al abrir la vela siguiente. La estructura viva se conserva
    # y la pregunta por 2 no se abre porque no hay ciclo cerrado por TT.
    check("GAP-05", "gap", "positive",
          "la funcion viva no se divide al cambiar de vela ni rota sin TT",
          "CONTINUATION_ACROSS_BAR" in evc
          and rc.reading.new_one_status == "NEW_ONE_ACTIVE"
          and rc.reading.n_origin == 9830 and rc.reading.n_extreme == 9900
          and rc.reading.two_status != "CONFIRMED",
          f"cont={'CONTINUATION_ACROSS_BAR' in evc} "
          f"n={rc.reading.n_origin}->{rc.reading.n_extreme} "
          f"two={rc.reading.two_status}")

    # Ancla canonica v2.19 D: cierre 16:24 = 29834,5 | apertura 16:25 = 29848,5
    # precios en centesimas de punto: 2984850 = 29848,50
    ANCH = [[2984000, 2983000, 2984500, 2983400],
            [2984850, 2986000, 2985500, 2985800]]
    ra = Reader(build(ANCH), reading_id="GAP_ANCHOR").run()
    eva = [e["event"] for e in ra.events]
    check("GAP-06", "gap", "positive",
          "ancla 16:24-16:25: nuevo 1 alcista desde 29848,5",
          ra.reading.new_one_status == "NEW_ONE_ACTIVE"
          and ra.reading.n_origin == 2984850
          and ra.reading.n_dir == 1,
          f"origin={ra.reading.n_origin} dir={ra.reading.n_dir} "
          f"size={ra.reading.n_size}")
    check("GAP-07", "gap", "negative",
          "el nuevo 1 no se mide desde el cierre previo ni desde 29828-ish",
          ra.reading.n_origin != 29834 and ra.reading.n_origin != 29840
          and ra.reading.n_origin == 2984850,
          f"origin={ra.reading.n_origin}")
    check("GAP-08", "gap", "positive",
          "secuencia implicita registrada sin precios internos inventados",
          "GAP_IMPLICIT_SEQUENCE" in eva
          and len(ra.trace) == len(build(ANCH)),
          f"trace={len(ra.trace)} ticks={len(build(ANCH))}")
    check("GAP-09", "gap", "negative",
          "las funciones previas pierden autoridad activa tras el gap",
          ra.reading.active_function == "NEW_ONE"
          and ra.reading.a_authority != "LIVE"
          and ra.reading.b_authority != "LIVE"
          and ra.reading.c_authority != "LIVE",
          f"active={ra.reading.active_function} a={ra.reading.a_authority} "
          f"b={ra.reading.b_authority} c={ra.reading.c_authority}")

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
