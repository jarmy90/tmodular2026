#!/usr/bin/env python3
"""ITERACION 13 — auditoria de las rotaciones internas del feed.

No llama "ciclos TM" al contador: informa rotaciones y su causa.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))

from tm_reference_interpreter_v1_direct_aut import Reader, load_ticks, FEED  # noqa: E402


def main() -> int:
    ticks = load_ticks(FEED)
    run = Reader(ticks, reading_id="FULL").run()
    ev = run.events
    counts = Counter(e["event"] for e in ev)

    rot = [e for e in ev if e["event"] == "CYCLE_RESET_AFTER_NEW_ONE"]
    via = Counter("TT" if "via=TT" in e["detail"] else "NEW_ONE" for e in rot)
    gaps = counts.get("GAP_IMPLICIT_NEW_ONE", 0)
    ctrend = counts.get("C_USED_AS_TREND", 0)
    zero = counts.get("ONE_ZERO_SIZE_DEFERRAL", 0)

    # rotaciones consecutivas sin AUT/TT entre medias (posible cascada)
    seq = [e["event"] for e in ev]
    cascade = 0
    last_rot = -10
    for i, name in enumerate(seq):
        if name == "CYCLE_RESET_AFTER_NEW_ONE":
            if i - last_rot == 1:
                cascade += 1
            last_rot = i

    metrics = {
        "ticks": len(ticks),
        "cycle_rotations": len(rot),
        "cycles_closed_by_tt": via.get("TT", 0),
        "cycles_started_by_gap": gaps,
        "cycles_started_by_c_trend": ctrend,
        "initial_cycles": 1,
        "incomplete_or_archived_cycles": len(run.reading.prev_cycle) > 0,
        "terminal_archived_cycles": len(rot),
        "consecutive_rotations_no_closure": cascade,
        "zero_size_new_one_deferrals": zero,
        "a_confirmed": counts.get("A_CONFIRMED", 0),
        "b_candidate": counts.get("B_CANDIDATE", 0),
        "b_grande": counts.get("B_GRANDE", 0),
        "aut": counts.get("AUT_CONFIRMED", 0) + counts.get("AUT_DIRECT_BY_A", 0),
        "tt_confirmed": counts.get("TT_100_REACHED", 0),
        "tt_failed": counts.get("TT_FAILED_FINAL_A_FIRST", 0),
        "ft_confirmed": counts.get("FT_STRUCTURAL_CONFIRMED", 0),
        "cut": counts.get("CUT_CONFIRMED", 0),
        "modules": counts.get("MODULE_BY_DISCARD", 0) + counts.get("MODULE_1_2", 0)
        + counts.get("MODULE_1_2_3", 0),
        "note": "son rotaciones internas, NO ciclos TM completos validados",
    }

    rows = []
    for e in rot:
        rows.append({"time": e["time_ms"], "via": "TT" if "via=TT" in e["detail"] else "NEW_ONE",
                     "detail": e["detail"]})
    with (HERE / "ROTATION_AUDIT.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["time", "via", "detail"])
        w.writeheader()
        w.writerows(rows)
    (HERE / "ROTATION_AUDIT.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
