# -*- coding: utf-8 -*-
"""Ejecucion observacional de R5 sobre el bloque real 16:49-17:29.
No modifica el motor. Solo registra eventos y estado como evidencia."""
from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CORE = Path(r"C:\Users\profesor\OpenBot\Agents\agent-ece275c8-821a-43f3-b05f-6cdf123b7ade"
            r"\deliverables_R5\python\TM_CORE_PYTHON_v0752_CANONICAL_R5.py")
FEED = ROOT / "TM_CANON_ACTIVO" / "02_TICKS" / "TM_TICKFEED_1615_1730.csv"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
spec = importlib.util.spec_from_file_location("r5", CORE)
m = importlib.util.module_from_spec(spec)
sys.modules["r5"] = m
spec.loader.exec_module(m)


def price_i(s: str) -> int:
    return int(round(float(s.replace(",", ".")) * 100))


def main():
    pts = []
    with open(FEED, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            bar = int(row["time_msc"]) // 60000
            if 16 * 60 + 49 <= bar % 1440 <= 17 * 60 + 29:
                pts.append(m.Pt(price_i(row["bid"]), int(row["sequence_id"]),
                                int(row["time_msc"]), bar))
    eng = m.CanonicalEngine(pts, {})
    eng.trace_states = False
    before = 0
    rows = []
    for p in pts:
        eng.feed_chunk([p])
        new = eng.events[before:]
        before = len(eng.events)
        for e in new:
            rows.append({"sequence_id": p.seq, "time_ms": p.time_ms,
                         "event": e if isinstance(e, str) else json.dumps(e, ensure_ascii=False),
                         "readings": len(eng.readings)})
    eng.finalize_stream()
    out = HERE / "R5_BLOCK_EVIDENCE.json"
    out.write_text(json.dumps({
        "engine": str(CORE),
        "ticks": len(pts),
        "events_total": len(eng.events),
        "events_in_block": len(rows),
        "readings": len(eng.readings),
        "event_rows": rows,
        "final_readings": [
            {"id": r.reading_id, "state": r.state,
             "function": getattr(r, "active_function", ""),
             "module": (r.module_origin, r.module_extreme, r.module_size),
             "a": r.a_size, "b": r.b_size,
             "tt": getattr(r, "tt_hit", False)}
            for r in eng.readings
        ],
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"ticks": len(pts), "events_total": len(eng.events),
                      "events_in_block": len(rows), "readings": len(eng.readings)}, indent=1))
    for r in eng.readings[:10]:
        print(r.reading_id, r.state, getattr(r, "active_function", ""),
              r.module_origin, r.module_extreme, r.module_size, r.a_size, r.b_size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
