"""Concept tests for A/B candidate, B Grande, AUT and new 1."""
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

# Iteracion 08: el harness canonico usa el interprete con AUT directo por A.
# El motor bg_aut queda como evidencia historica (EV I DENCE_ONLY).
_MODULE = importlib.import_module(
    os.environ.get("TM_READER_MODULE", "tm_reference_interpreter_v1_direct_aut"))
FEED = _MODULE.FEED
Reader = _MODULE.Reader
Tick = _MODULE.Tick
load_ticks = _MODULE.load_ticks


def make(bars: list[list[int]]) -> list[Tick]:
    ticks = []
    seq = 1
    for bar, prices in enumerate(bars):
        for i, price in enumerate(prices):
            ticks.append(Tick(seq, bar * 60_000 + i * 100, bar, price))
            seq += 1
    return ticks


def run(bars: list[list[int]], rid: str = "TEST") -> Reader:
    return Reader(make(bars), reading_id=rid).run()


def main() -> int:
    results = []

    def check(tid, area, kind, desc, cond, detail,
              cls="CANONICAL_PASS"):
        results.append({"test_id": tid, "area": area, "kind": kind,
                        "description": desc, "pass": bool(cond), "detail": detail,
                        "classification": cls if cond else "FAIL"})

    # Module down 1000: 1=10000->9000; 2 impossible at 9000.
    base = [[10000, 9000], [9000, 9000]]
    ab = base + [[9000, 9500, 9250, 9200]]  # A=500, B candidate=300
    bg100 = base + [[9000, 9500, 9250, 9200, 9000]]
    bg_between = base + [[9000, 9500, 9250, 9200, 8950]]
    bg_limit = base + [[9000, 9500, 9250, 9200, 8840]]
    bg_aut = base + [[9000, 9500, 9250, 9200, 8839]]
    bg_jump = base + [[9000, 9500, 9250, 9200, 9100, 8700]]

    # A-01: module extension absorbs A pending. v2.16: la absorcion queda
    # reservada a la oscilacion interna que no alcanza la proporcion
    # orientativa (2,0 puntos = 20 % de un modulo de 1000).
    r = run(base + [[9000, 9200, 8900]])
    check("A-01", "absorption", "negative",
          "extension del modulo absorbe A interna (<35 %) [politica 35 %]",
          r.reading.a_status == "ABSORBED_IN_ACTIVE_FUNCTION"
          and r.reading.b_status == "" and r.reading.mod_size == 1100,
          f"a={r.reading.a_status} b={r.reading.b_status} mod={r.reading.mod_size}",
          cls="PROVISIONAL_POLICY_PASS")

    # A-02: autonomous return confirms A and opens B.
    r = run(ab)
    check("A-02", "A/B", "positive", "retorno estructural confirma A y abre B",
          r.reading.a_status == "A_CONFIRMED" and r.reading.a_size == 500
          and r.reading.b_status == "CANDIDATE"
          and r.reading.b_origin == 9500 and r.reading.b_size == 300,
          f"a={r.reading.a_status}/{r.reading.a_size} "
          f"b={r.reading.b_status}/{r.reading.b_origin}/{r.reading.b_size}")

    # A-03: one-tick return absorbed inside A; no B.
    r = run(base + [[9000, 9500, 9250, 9600]])
    check("A-03", "return", "negative", "retorno provisional absorbido en A",
          r.reading.a_status == "CONTRARY_MOVE_PENDING"
          and r.reading.b_status == ""
          and "ABSORBED_IN_A" in r.reading.return_status,
          f"a={r.reading.a_status} return={r.reading.return_status} b={r.reading.b_status}")

    # A-04 (iteracion 09): un movimiento PENDIENTE que cruza la base no puede
    # confirmar A y AUT a la vez. Queda OPEN_RULE_BLOCK, sin nuevo 1.
    r = run(base + [[9000, 10100]])
    check("A-04", "AUT direct/OPEN_RULE_BLOCK", "negative",
          "A pendiente cruza la base -> OPEN_RULE_BLOCK, sin inventar causalidad",
          r.reading.aut_direct_status == "OPEN_RULE_BLOCK"
          and r.reading.new_one_status == ""
          and r.reading.b_status == ""
          and r.reading.a_confirmations == 0,
          f"aut={r.reading.aut_direct_status} n={r.reading.new_one_status} "
          f"b={r.reading.b_status} conf={r.reading.a_confirmations}")

    # A-05: A lives across bars; origin unchanged.
    r = run(base + [[9000, 9200], [9000, 9500, 9250, 9200]])
    check("A-05", "continuity", "positive", "A cruza velas sin cambiar origen",
          r.reading.a_status == "A_CONFIRMED" and r.reading.a_origin == 9000
          and r.reading.a_extreme == 9500,
          f"a={r.reading.a_status}/{r.reading.a_origin}/{r.reading.a_extreme}")

    # Real anchors.
    ticks = load_ticks(FEED)
    l1 = [t for t in ticks if 16 * 60 + 15 <= t.bar % 1440 <= 16 * 60 + 18]
    r1 = Reader(l1, reading_id="L1").run()
    l2 = [t for t in ticks if 16 * 60 + 19 <= t.bar % 1440 <= 16 * 60 + 22]
    r2 = Reader(l2, reading_id="L2").run()

    a_events = [e for e in r1.events if e["event"] == "A_CONFIRMED"]
    check("A-06", "A", "positive", "ancla L1 A=9,1 y una sola confirmacion",
          r1.reading.a_size == 910 and r1.reading.a_confirmations == 1
          and len(a_events) == 1,
          f"a={r1.reading.a_size} conf={r1.reading.a_confirmations} events={len(a_events)}")

    check("A-07", "B", "positive", "B conserva origen en el extremo de A",
          run(ab).reading.b_origin == 9500 and run(ab).reading.b_size == 300,
          f"b={run(ab).reading.b_origin}/{run(ab).reading.b_size}")

    check("A-08", "times", "positive", "structural_time != knowledge_time",
          r1.reading.a_origin_st < r1.reading.a_kt
          and r1.reading.b_st <= r1.reading.b_kt,
          f"a_st={r1.reading.a_origin_st} a_kt={r1.reading.a_kt} "
          f"b_st={r1.reading.b_st} b_kt={r1.reading.b_kt}")

    r = run(base + [[9000, 9500]])
    check("A-09", "invariant", "negative", "no existe B antes de A confirmada",
          r.reading.b_status == "" and r.reading.a_status == "CONTRARY_MOVE_PENDING",
          f"a={r.reading.a_status} b={r.reading.b_status}")

    a_events2 = [e for e in r2.events if e["event"] == "A_CONFIRMED"]
    check("A-10", "A", "positive", "L2 A confirmada una vez desde 29830,3",
          r2.reading.a_confirmations == 1 and len(a_events2) == 1
          and r2.reading.a_origin == 2983030
          and r2.reading.three_extreme == 2983030 and r2.reading.mod_size == 1970,
          f"a={r2.reading.a_confirmations}/{r2.reading.a_origin} "
          f"three={r2.reading.three_extreme} mod={r2.reading.mod_size}")

    check("A-11", "B Grande", "positive", "L1 B Grande y AUT en ticks separados",
          r1.reading.b_grande_status == "AUT" and r1.reading.b_status == "AUT"
          and r1.reading.b_grande_kt == 1792167514125
          and r1.reading.aut_kt == 1792167514926
          and r1.reading.b_size == 1230,
          f"grande={r1.reading.b_grande_kt} aut={r1.reading.aut_kt} b={r1.reading.b_size}")

    check("A-12", "core", "real", "L2 mantiene 1/2/3/modulo",
          r2.reading.one_size == 750 and r2.reading.two_size == 1230
          and r2.reading.three_extreme == 2983030 and r2.reading.mod_size == 1970,
          f"1={r2.reading.one_size} 2={r2.reading.two_size} "
          f"3={r2.reading.three_extreme} mod={r2.reading.mod_size}")

    repeat = Reader(l1, reading_id="L1").run()
    prefix_ticks = [t for t in l1 if t.bar % 1440 <= 16 * 60 + 17]
    pref = Reader(prefix_ticks, reading_id="L1").run()
    check("A-13", "determinism", "global", "doble ejecucion y prefijo L1",
          r1.trace == repeat.trace and r1.events == repeat.events
          and pref.trace == r1.trace[:len(pref.trace)],
          f"trace={len(r1.trace)} prefix={len(pref.trace)}")

    # A-14 — TEST_DEPENDS_ON_REJECTED_POLICY (P-AB-04) reescrita:
    # un salto unico grande NO confirma A por tamano; queda RETURN_MOVE_PENDING.
    r = run(base + [[9000, 9500, 9000]])
    check("A-14", "return/REJECTED_POLICY_REWRITTEN", "boundary",
          "salto unico grande no confirma A sin extension propia",
          r.reading.a_status != "A_CONFIRMED"
          and r.reading.return_status == "RETURN_MOVE_PENDING"
          and r.reading.return_jump is False
          and r.reading.b_status == "",
          f"a={r.reading.a_status} return={r.reading.return_status} "
          f"jump={r.reading.return_jump} b={r.reading.b_status}")

    check("A-15", "new one", "positive", "nuevo 1 nace en AUT y conserva B",
          r1.reading.new_one_status == "NEW_ONE_ACTIVE"
          and r1.reading.n_origin == 2985760
          and r1.reading.n_st == r1.reading.b_st
          and r1.reading.n_kt == r1.reading.aut_kt
          and r1.reading.n_extreme == 2984300,
          f"n={r1.reading.n_origin}/{r1.reading.n_extreme} "
          f"st={r1.reading.n_st} kt={r1.reading.n_kt}")

    check("A-16", "authority", "positive", "3 y modulo archivados al confirmar A",
          r2.reading.three_authority == "ARCHIVED"
          and r2.reading.module_authority == "FROZEN_REFERENCE"
          and r2.reading.three_status == "CONFIRMED",
          f"3auth={r2.reading.three_authority} mod={r2.reading.module_authority}")

    # BG-01..BG-16
    r = run(bg100)
    check("BG-01", "B Grande", "boundary", "B alcanza exactamente 100%",
          r.reading.b_size == 500 and r.reading.b_grande_status == "B_GRANDE"
          and r.reading.aut_status == "",
          f"b={r.reading.b_size} status={r.reading.b_grande_status} aut={r.reading.aut_status}")

    r = run(bg_between)
    check("BG-02", "B Grande", "positive", "B entre 100% y limite",
          r.reading.b_size == 550 and r.reading.b_grande_status == "B_GRANDE",
          f"b={r.reading.b_size} status={r.reading.b_grande_status}")

    r = run(bg_limit)
    check("BG-03", "B Grande", "boundary", "B toca exactamente 127%+0,25",
          r.reading.b_size == 660 and r.reading.b_grande_status == "B_GRANDE"
          and r.reading.aut_status == "",
          f"b={r.reading.b_size} status={r.reading.b_grande_status} aut={r.reading.aut_status}")

    r = run(bg_aut)
    check("BG-04", "AUT", "boundary", "B supera el limite por un tick minimo",
          r.reading.b_size == 661 and r.reading.aut_status == "AUT_CONFIRMED"
          and r.reading.b_status == "AUT",
          f"b={r.reading.b_size} aut={r.reading.aut_status} status={r.reading.b_status}")

    r = run(bg_jump)
    events = [e["event"] for e in r.events]
    check("BG-05", "AUT", "jump", "salto de B candidata a AUT",
          "B_GRANDE_CAUSAL_CROSS" in events and r.reading.b_size == 800
          and r.reading.aut_status == "AUT_CONFIRMED" and r.reading.b_status == "AUT",
          f"events={events[-6:]} b={r.reading.b_size} aut={r.reading.aut_status}")

    r = run(base + [[9000, 9500]])
    check("BG-06", "AUT", "negative", "B no existe sin A confirmada",
          r.reading.b_status == "" and r.reading.aut_status == "",
          f"b={r.reading.b_status} aut={r.reading.aut_status}")

    r = run(bg_aut)
    check("BG-07", "AUT", "positive", "AUT abre nuevo 1 en el mismo tick",
          r.reading.aut_kt == r.reading.n_kt and r.reading.new_one_status == "NEW_ONE_ACTIVE",
          f"aut={r.reading.aut_kt} n_kt={r.reading.n_kt}")

    check("BG-08", "AUT", "positive", "nuevo 1 conserva origen de B",
          r.reading.n_origin == r.reading.b_origin,
          f"n={r.reading.n_origin} b={r.reading.b_origin}")

    # Iteracion 12: la extension posterior pertenece al nuevo 1, y al abrir la
    # vela siguiente ese nuevo 1 ES el 1 del ciclo nuevo (nunca B).
    r = run(bg_aut + [[8839, 8800]])
    # Iteracion 12: con TT pendiente NO se abre 2 (v2.7 B); la extension
    # posterior pertenece al nuevo 1 y B queda congelada en el AUT.
    check("BG-09", "new one", "positive",
          "extension posterior extiende el nuevo 1; B congelada y TT pendiente",
          r.reading.b_size == 661
          and r.reading.n_extreme == 8800 and r.reading.n_size == 700
          and r.reading.tt_status == "TT_PENDING"
          and r.reading.cycle_id == 0,
          f"b={r.reading.b_size} n={r.reading.n_size}/{r.reading.n_extreme} "
          f"tt={r.reading.tt_status} cycle={r.reading.cycle_id}")

    r = run(bg_aut)
    check("BG-10", "AUT", "invariant", "B Grande y AUT no quedan vigentes juntos",
          r.reading.b_status == "AUT" and r.reading.b_grande_status == "AUT"
          and r.reading.active_function == "NEW_ONE",
          f"b={r.reading.b_status} grande={r.reading.b_grande_status} active={r.reading.active_function}")

    check("BG-11", "times", "positive", "structural_time nuevo 1 < knowledge_time AUT",
          r1.reading.n_st < r1.reading.n_kt,
          f"st={r1.reading.n_st} kt={r1.reading.n_kt}")

    check("BG-12", "authority", "positive", "A y modulo sin autoridad activa tras AUT",
          r1.reading.a_authority == "ARCHIVED"
          and r1.reading.module_authority == "FROZEN_REFERENCE"
          and r1.reading.active_function == "NEW_ONE",
          f"a={r1.reading.a_authority} mod={r1.reading.module_authority} active={r1.reading.active_function}")

    r = run([[10000, 9800, 9600], [9600, 9400, 9200], [9200, 9401, 9300]])
    check("BG-13", "A birth", "positive", "A nace dentro de la vela de 3/modulo",
          r.reading.a_status == "CONTRARY_MOVE_PENDING"
          and r.reading.a_origin == 9200 and r.reading.a_size == 100,
          f"a={r.reading.a_status}/{r.reading.a_origin}/{r.reading.a_size}")

    r = run(base + [[9000, 9200], [9000, 9500, 9250, 9200]])
    check("BG-14", "A continuity", "positive", "A continua entre velas sin reiniciarse",
          r.reading.a_status == "A_CONFIRMED" and r.reading.a_origin == 9000,
          f"a={r.reading.a_status}/{r.reading.a_origin}")

    # BG-15 — TEST_DEPENDS_ON_REJECTED_POLICY (P-AB-04) reescrita:
    # retorno de varios ticks que extiende su propio extremo confirma A.
    r = run(base + [[9000, 9500, 9250, 9200]])
    check("BG-15", "return/REJECTED_POLICY_REWRITTEN", "positive",
          "retorno autonomo por extension propia, sin cuatro puntos",
          r.reading.a_status == "A_CONFIRMED" and r.reading.a_confirmations == 1
          and r.reading.return_extended is True
          and r.reading.return_jump is False
          and r.reading.b_status == "CANDIDATE",
          f"a={r.reading.a_status} ext={r.reading.return_extended} "
          f"jump={r.reading.return_jump} b={r.reading.b_status}",
          cls="PROVISIONAL_POLICY_PASS")

    r = run(base + [[9000, 9500, 9250, 9600]])
    check("BG-16", "return", "negative", "retorno absorbido no confirma A/B",
          r.reading.a_status == "CONTRARY_MOVE_PENDING" and r.reading.b_status == "",
          f"a={r.reading.a_status} b={r.reading.b_status}",
          cls="PROVISIONAL_POLICY_PASS")

    out = HERE / "AB_CANDIDATE_TEST_RESULTS.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["test_id", "area", "kind",
                                           "description", "pass", "detail",
                                           "classification"])
        w.writeheader()
        w.writerows(results)
    passed = sum(1 for x in results if x["pass"])
    summary = {"reader": _MODULE.CORE_VERSION,
               "tests": len(results), "passed": passed,
               "failed": len(results) - passed, "all_pass": passed == len(results),
               "rejected_policy_rewritten": ["A-14", "BG-15"]}
    (HERE / "AB_CANDIDATE_TEST_RESULTS.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    for x in results:
        print(("PASS" if x["pass"] else "FAIL"), x["test_id"], x["description"],
              x["detail"])
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
