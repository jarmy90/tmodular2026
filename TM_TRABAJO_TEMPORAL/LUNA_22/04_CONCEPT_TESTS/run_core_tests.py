"""Core concept tests for TM_REFERENCE_INTERPRETER_V1."""
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
    os.environ.get("TM_READER_MODULE",
                   "tm_reference_interpreter_v1_direct_aut"))
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


def run(ticks: list[Tick], reading_id: str = "TEST") -> Reader:
    return Reader(ticks, reading_id=reading_id).run()




def main() -> int:
    results = []

    def check(test_id, transition, kind, description, cond, detail):
        results.append({
            "test_id": test_id, "transition": transition, "kind": kind,
            "description": description, "pass": bool(cond), "detail": detail,
            "classification": "CANONICAL_PASS" if cond else "FAIL",
        })

    # T-001: 1 initial + confirmation
    r = run(make([[10000, 9900, 9800], [9800, 9700, 9600]]))
    check("T-001", "1", "positive", "1 inicial 10000->9800 confirmada",
          r.reading.one_status == "CONFIRMED" and r.reading.one_size == 200,
          f"status={r.reading.one_status} size={r.reading.one_size}")

    # T-002: 2 candidate
    r = run(make([[10000, 9900, 9800], [9800, 9700]]))
    check("T-002", "2", "positive", "2 candidata tras apertura plana",
          r.reading.two_status == "CANDIDATE",
          f"status={r.reading.two_status}")

    # T-003: 2 confirmed at 100%
    r = run(make([[10000, 9900, 9800], [9800, 9700, 9600]]))
    check("T-003", "2", "positive", "2 confirmada al 100% de 1",
          r.reading.two_status == "CONFIRMED" and r.reading.two_size == 200,
          f"status={r.reading.two_status} size={r.reading.two_size}")

    # T-004: 2 impossible at close
    r = run(make([[10000, 9900, 9800], [9800, 9750], [9750]]))
    check("T-004", "2", "negative", "2 imposible al cierre sin 100%",
          r.reading.two_status == "IMPOSSIBLE_CLOSE" and r.reading.mod_size == 250,
          f"two={r.reading.two_status} mod={r.reading.mod_size}")

    # T-005: 2 impossible by initial tail
    r = run(make([[10000, 9900, 9800], [9800, 9830]]))
    check("T-005", "2", "negative", "2 imposible por cola inicial > 0,25",
          r.reading.two_status == "IMPOSSIBLE_TAIL" and r.reading.mod_size == 200,
          f"two={r.reading.two_status} mod={r.reading.mod_size}")

    # T-015: 0,25 exact is not flat and forbids 2.
    # v2.19: the gap is not read as a single A from the previous extreme; it
    # yields implicit A -> B Grande -> A as trend and a new 1 from the open.
    r = run(make([[10000, 9900, 9800], [9825, 9820]]))
    events = [e["event"] for e in r.events]
    # Iteracion 16: sin compatibilidad silenciosa. La semantica historica
    # (modulo por descarte de 200) ya no satisface T-015.
    check("T-015", "opening", "boundary",
          "0,25 exacto no es plano, prohibe 2 y abre nuevo 1 desde la apertura",
          r.reading.two_status == "IMPOSSIBLE_NO_FLAT"
          and r.reading.new_one_status == "NEW_ONE_ACTIVE"
          and r.reading.n_origin == 9825
          and r.reading.n_dir == 1
          and "GAP_IMPLICIT_SEQUENCE" in events
          and "GAP_IMPLICIT_NEW_ONE" in events,
          f"two={r.reading.two_status} one={r.reading.new_one_status} "
          f"origin={r.reading.n_origin} dir={r.reading.n_dir} events={events}")

    # T-016: 0,10 is flat and allows 2 candidate
    r = run(make([[10000, 9900, 9800], [9810, 9815]]))
    check("T-016", "opening", "boundary", "0,10 es plano y permite 2 candidata",
          r.reading.two_status == "CANDIDATE", f"two={r.reading.two_status}")

    # T-017: non-flat 0,30 forbids 2 before any direction advance
    r = run(make([[10000, 9900, 9800], [9830, 9820]]))
    check("T-017", "opening", "negative", "apertura no plana prohibe 2",
          r.reading.two_status == "IMPOSSIBLE_NO_FLAT",
          f"two={r.reading.two_status}")

    # T-006: 3 pending after valid retrace, before recovery
    r = run(make([[10000, 9800, 9600], [9600, 9400, 9200], [9200, 9400]]))
    check("T-006", "3", "pending", "3 pendiente con retroceso valido",
          r.reading.phase in ("WAIT_THREE", "CORE_WAIT_THREE_A_NOT_IMPLEMENTED")
          and r.reading.three_status == "",
          f"phase={r.reading.phase} three={r.reading.three_status}")

    # T-007: 3 confirmed after recovery
    r = run(make([[10000, 9800, 9600], [9600, 9400, 9200], [9200, 9400, 9100]]))
    check("T-007", "3", "positive", "3 confirmada al superar el extremo de 2",
          r.reading.three_status == "CONFIRMED" and r.reading.three_extreme == 9100,
          f"three={r.reading.three_status} extreme={r.reading.three_extreme}")

    # T-008: exact 50% is valid and confirms after recovery
    r = run(make([[10000, 9800, 9600], [9600, 9400, 9200], [9200, 9400, 9100]]))
    has_fifty = any(e["event"] == "FIFTY_PERCENT_EXACT" for e in r.events)
    check("T-008", "3", "boundary", "50% exacto conserva 3",
          has_fifty and r.reading.three_status == "CONFIRMED",
          f"event={has_fifty} three={r.reading.three_status}")

    # T-009: >50% makes 3 impossible
    r = run(make([[10000, 9800, 9600], [9600, 9400, 9200], [9200, 9401, 9100]]))
    check("T-009", "3", "negative", "retroceso > 50% imposibilita 3",
          r.reading.three_status == "IMPOSSIBLE" and r.reading.mod_size == 800,
          f"three={r.reading.three_status} mod={r.reading.mod_size}")

    # T-010: regular 1+2+3 module
    r = run(make([[10000, 9800, 9600], [9600, 9400, 9200], [9200, 9400, 9100]]))
    check("T-010", "module", "positive", "modulo regular 1+2+3",
          r.reading.mod_status == "REGULAR_1_2_3" and r.reading.mod_size == 900,
          f"status={r.reading.mod_status} size={r.reading.mod_size}")

    # T-018: internal vibration of 2 does not open 3 inside 2's bar
    r = run(make([[10000, 9900, 9800], [9800, 9600, 9900, 9400]]))
    check("T-018", "2/3", "negative", "vibracion interna no abre 3 en la vela de 2",
          r.reading.three_status == "" and r.reading.two_extreme == 9400
          and r.reading.two_size == 400,
          f"three={r.reading.three_status} two={r.reading.two_extreme}/{r.reading.two_size}")

    # T-019: 3 opens in the next bar after a valid retrace
    r = run(make([[10000, 9900, 9800], [9800, 9600, 9900, 9400], [9400, 9600, 9350]]))
    check("T-019", "3", "positive", "3 se abre en la vela siguiente tras retroceso valido",
          r.reading.three_status == "CONFIRMED" and r.reading.three_extreme == 9350
          and r.reading.mod_size == 650,
          f"three={r.reading.three_status}/{r.reading.three_extreme} mod={r.reading.mod_size}")

    # T-011: determinism
    ticks = make([[10000, 9800, 9600], [9600, 9400, 9200], [9200, 9400, 9100]])
    a = run(ticks).trace
    b = run(ticks).trace
    check("T-011", "global", "determinism", "doble ejecucion identica", a == b,
          f"lines={len(a)}")

    # T-012: prefix consistency
    full = run(ticks).trace
    prefix = run([t for t in ticks if t.bar <= 1]).trace
    check("T-012", "global", "prefix", "prefijo consistente",
          prefix == full[:len(prefix)], f"prefix={len(prefix)} full={len(full)}")

    # T-013: real 16:15-16:18 anchor (core only)
    real = load_ticks(FEED)
    ticks1 = [t for t in real if 16 * 60 + 15 <= t.bar % 1440 <= 16 * 60 + 18]
    r1 = run(ticks1, reading_id="L1")
    check("T-013", "1/2/module", "real", "ancla 16:15-16:18",
          r1.reading.one_size == 1620
          and r1.reading.two_status == "IMPOSSIBLE_CLOSE"
          and r1.reading.two_size == 1260
          and r1.reading.mod_size == 2850
          and r1.reading.mod_status == "BY_DISCARD_1_2",
          f"one={r1.reading.one_size} two={r1.reading.two_status}/{r1.reading.two_size} "
          f"mod={r1.reading.mod_size}/{r1.reading.mod_status}")

    # T-014: real L2 16:19-16:22 anchor (core only)
    ticks2 = [t for t in real if 16 * 60 + 19 <= t.bar % 1440 <= 16 * 60 + 22]
    r2 = run(ticks2, reading_id="L2")
    check("T-014", "1/2/3/module", "real", "ancla L2 16:19-16:22",
          r2.reading.one_size == 750
          and r2.reading.two_status == "CONFIRMED"
          and r2.reading.two_size == 1230
          and r2.reading.two_extreme == 2983250
          and r2.reading.three_status == "CONFIRMED"
          and r2.reading.three_extreme == 2983030
          and r2.reading.mod_size == 1970
          and r2.reading.mod_status == "REGULAR_1_2_3",
          f"one={r2.reading.one_size} two={r2.reading.two_size} "
          f"three={r2.reading.three_extreme} mod={r2.reading.mod_size}")

    out_csv = HERE / "CORE_TEST_RESULTS.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["test_id", "transition", "kind",
                                           "description", "pass", "detail",
                                           "classification"])
        w.writeheader()
        w.writerows(results)
    passed = sum(1 for r in results if r["pass"])
    summary = {
        "reader": "TM_REFERENCE_INTERPRETER_V1_CORE",
        "tests": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "all_pass": passed == len(results),
        "scope": "core 1/2/3/module; A/B/C not implemented",
    }
    (HERE / "CORE_TEST_RESULTS.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    for r in results:
        print(("PASS" if r["pass"] else "FAIL"), r["test_id"], r["description"], r["detail"])
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
