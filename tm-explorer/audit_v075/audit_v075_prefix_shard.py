from __future__ import annotations

import argparse
import bisect
import csv
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "audit_v075"))

import audit_v075_common as ac

core = ac.core
from audit_v075_prefix_matrix import build_cutoffs, compare_signatures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed", required=True)
    parser.add_argument("--out-jsonl", required=True)
    parser.add_argument("--shard", type=int, required=True)
    parser.add_argument("--shards", type=int, required=True)
    args = parser.parse_args()

    feed = Path(args.feed)
    out = Path(args.out_jsonl)
    out.parent.mkdir(parents=True, exist_ok=True)
    points, bars = core.load_feed(feed)
    full = core.run_engine(points, bars)
    cutoffs, metadata = build_cutoffs(full, points)
    ordered_all = sorted(cutoffs.items())[args.shard :: args.shards]
    done: set[int] = set()
    if out.exists():
        with out.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    done.add(int(json.loads(line)["cutoff_ms"]))
    ordered = [(cutoff, reasons) for cutoff, reasons in ordered_all if cutoff not in done]
    print(
        f"shard {args.shard}/{args.shards}: pending={len(ordered)} of {len(ordered_all)} "
        f"already={len(done)}",
        flush=True,
    )
    if not ordered:
        return 0

    with feed.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter=";")
        header = next(reader)
        rows = list(reader)
    time_column = header.index("time_msc")
    times = [int(row[time_column]) for row in rows]
    expected_cache = {cutoff: ac.prefix_signature(full, cutoff) for cutoff in dict(ordered)}

    temp_dir = Path(tempfile.mkdtemp(prefix=f"tmprefix_s{args.shard}_", dir=str(ROOT)))
    prefix_path = temp_dir / "prefix.csv"
    failures = 0
    try:
        with out.open("a", encoding="utf-8", newline="") as sink:
            for order, (cutoff, reasons) in enumerate(ordered, 1):
                index = bisect.bisect_right(times, cutoff)
                try:
                    with prefix_path.open("w", encoding="utf-8-sig", newline="") as handle:
                        writer = csv.writer(handle, delimiter=";", lineterminator="\n")
                        writer.writerow(header)
                        writer.writerows(rows[:index])
                    prefix_points, prefix_bars = core.load_feed(prefix_path)
                    if prefix_points and prefix_points[-1].time_ms > cutoff:
                        raise RuntimeError("physical prefix exceeds cutoff")
                    prefix_engine = core.run_engine(prefix_points, prefix_bars)
                    actual = ac.prefix_signature(prefix_engine, cutoff)
                    expected = expected_cache[cutoff]
                    ok, differences = compare_signatures(expected, actual)
                    row = {
                        "cutoff_ms": cutoff,
                        "cutoff_time": core.ms_to_text(cutoff),
                        "reasons": "|".join(sorted(reasons)),
                        "points": len(prefix_points),
                        "events_count": actual["events"]["count"],
                        "readings_created": actual["reading_identity"]["count"],
                        "readings_closed": actual["reading_closed"]["count"],
                        "expected_events": expected["events"]["count"],
                        "expected_readings_created": expected["reading_identity"]["count"],
                        "expected_readings_closed": expected["reading_closed"]["count"],
                        "pass": int(ok),
                        "differences": "|".join(differences),
                        "actual_event_digest": actual["events"]["digest"],
                        "expected_event_digest": expected["events"]["digest"],
                        "actual_reading_digest": actual["reading_identity"]["digest"],
                        "expected_reading_digest": expected["reading_identity"]["digest"],
                        "shard": args.shard,
                    }
                except Exception as exc:
                    row = {
                        "cutoff_ms": cutoff,
                        "cutoff_time": core.ms_to_text(cutoff),
                        "reasons": "|".join(sorted(reasons)),
                        "points": index,
                        "events_count": 0,
                        "readings_created": 0,
                        "readings_closed": 0,
                        "expected_events": 0,
                        "expected_readings_created": 0,
                        "expected_readings_closed": 0,
                        "pass": 0,
                        "differences": f"shard_error:{type(exc).__name__}:{exc}",
                        "actual_event_digest": "",
                        "expected_event_digest": "",
                        "actual_reading_digest": "",
                        "expected_reading_digest": "",
                        "shard": args.shard,
                    }
                if not row["pass"]:
                    failures += 1
                sink.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
                sink.flush()
                if order % 250 == 0:
                    print(
                        f"  shard {args.shard}: {order}/{len(ordered)} failures={failures}",
                        flush=True,
                    )
    finally:
        prefix_path.unlink(missing_ok=True)
        temp_dir.rmdir()
    print(f"shard {args.shard} done: {len(ordered)} failures={failures}", flush=True)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
