#!/usr/bin/env python3
"""ITERACION 08 — replays reales L1/L2 con el interprete direct_aut."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ENGINE = BASE / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))

from tm_reference_interpreter_v1_direct_aut import (  # noqa: E402
    Reader, Tick, load_ticks, FEED, CORE_VERSION, _hhmm,
)


def ticks_between(real: list[Tick], a: str, b: str) -> list[Tick]:
    def bar_of(h):
        hh, mm = h.split(":")
        return int(hh) * 60 + int(mm)
    lo, hi = bar_of(a), bar_of(b)
    return [t for t in real if lo <= t.bar % 1440 <= hi]


def write_block(name: str, ticks: list[Tick]) -> dict:
    rd = Reader(ticks, reading_id=name).run()
    out_state = BASE / "07_REAL_REPLAYS" / f"direct_aut_state_{name}.json"
    out_events = BASE / "07_REAL_REPLAYS" / f"direct_aut_events_{name}.csv"
    out_state.write_text(
        json.dumps(rd.summary(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    out_trace = BASE / "07_REAL_REPLAYS" / f"direct_aut_trace_{name}.jsonl"
    with out_trace.open("w", encoding="utf-8") as fh:
        for row in rd.trace:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    with out_events.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["sequence_id", "time", "bar", "gid", "event", "detail"])
        for e in rd.events:
            w.writerow([e["seq"], _hhmm(e["time_ms"]), e["bar"],
                        e["gid"], e["event"], e["detail"]])
    print(f"[{name}] ticks={len(ticks)} phase={rd.reading.phase} "
          f"a={rd.reading.a_status}/{rd.reading.a_size} "
          f"aut_direct={rd.reading.aut_direct_status} "
          f"new_one={rd.reading.new_one_status}")
    for e in rd.events:
        if e["event"] in ("A_CONFIRMED", "AUT_DIRECT_BY_A", "NEW_ONE_ACTIVE",
                          "B_CANDIDATE", "B_GRANDE", "AUT_CONFIRMED",
                          "MODULE_BY_DISCARD", "MODULE_1_2", "MODULE_1_2_3_CONFIRMED"):
            print("   ", _hhmm(e["time_ms"]), e["event"], e["detail"])
    return rd.summary()


def main() -> int:
    real = load_ticks(FEED)
    l1 = ticks_between(real, "16:15", "16:18")
    l2 = ticks_between(real, "16:19", "16:22")
    s1 = write_block("L1_1615_1618", l1)
    print()
    s2 = write_block("L2_1619_1622", l2)
    print()
    print("L1 new_one:", s1["new_one"])
    print("L2 a:", s2["a"])
    print("L2 new_one:", s2["new_one"])
    print("L2 b:", s2["b"])
    print("reader:", CORE_VERSION)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
