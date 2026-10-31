from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "audit_v075"))

import audit_v075_common as ac

core = ac.core


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed", required=True)
    parser.add_argument("--cutoff", required=True, type=int)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    cutoff = args.cutoff
    feed = Path(args.feed)
    points, bars = core.load_feed(feed)
    if not points:
        raise SystemExit("empty prefix feed")
    if points[-1].time_ms > cutoff:
        raise SystemExit(
            f"prefix feed exceeds cutoff: last={points[-1].time_ms} cutoff={cutoff}"
        )
    engine = core.run_engine(points, bars)
    signature = ac.prefix_signature(engine, cutoff)
    signature.update(
        {
            "cutoff_ms": cutoff,
            "cutoff_time": core.ms_to_text(cutoff),
            "points": len(points),
            "bars": len(bars),
            "events_total": len(engine.events),
            "readings_total": len(engine.readings),
            "last_point_time_ms": points[-1].time_ms,
        }
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(signature, ensure_ascii=False, sort_keys=True, indent=2),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
