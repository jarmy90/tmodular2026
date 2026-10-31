#!/usr/bin/env python3
"""Recorrido completo del feed 16:15-17:29 con el interprete de referencia."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "05_REFERENCE_ENGINE"))

from tm_reference_interpreter_v1_direct_aut import (  # noqa: E402
    Reader, load_ticks, FEED,
)

OUT = HERE.parent / "07_REAL_REPLAYS" / "full_feed_metrics.json"


def main() -> int:
    ticks = load_ticks(FEED)
    a = Reader(ticks, reading_id="FULL").run()
    b = Reader(ticks, reading_id="FULL").run()
    deterministic = a.trace == b.trace and a.events == b.events

    half = len(ticks) // 2
    pref = Reader(ticks[:half], reading_id="FULL").run()
    prefix_ok = pref.trace == a.trace[:len(pref.trace)]

    counts = Counter(e["event"] for e in a.events)
    s = a.summary()
    metrics = {
        "ticks": len(ticks),
        "deterministic": deterministic,
        "prefix_consistent": prefix_ok,
        "final_phase": s["phase"],
        "active_function": s["active_function"],
        "events_total": len(a.events),
        "event_counts": dict(sorted(counts.items())),
        "anchors": {
            "module_l1": "28,5", "a_l1": "9,1",
            "aut_by_b": "16:18:34.926", "aut_direct_l2": "16:22:52.576",
            "tt_l1_objetivo": "29829,1",
        },
        "not_implemented": ["CUT_RESET", "CONCURRENT_AUTO_DISCOVERY"],
        "cycle": {
            "cycles": a.reading.cycle_id,
            "modules": counts.get("MODULE_BY_DISCARD", 0) + counts.get("MODULE_1_2", 0),
            "aut": counts.get("AUT_CONFIRMED", 0) + counts.get("AUT_DIRECT_BY_A", 0),
            "tt": counts.get("TT_100_REACHED", 0),
            "ft": counts.get("FT_STRUCTURAL_CONFIRMED", 0),
            "gaps": counts.get("GAP_IMPLICIT_NEW_ONE", 0),
            "single_new_one_stall": a.reading.cycle_id == 0,
        },
        "state_final": {k: s[k] for k in
                        ("one", "two", "three", "module", "a", "b", "c",
                         "aut", "new_one", "active_function", "authority")},
    }
    OUT.write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(json.dumps({k: metrics[k] for k in
                      ("ticks", "deterministic", "prefix_consistent",
                       "final_phase", "events_total", "not_implemented")},
                     indent=2))
    print("top events:", dict(sorted(counts.items(), key=lambda kv: -kv[1])[:12]))
    print("last state:", metrics["state_final"]["active_function"],
          "| new_one:", metrics["state_final"]["new_one"]["status"])
    return 0 if deterministic and prefix_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
