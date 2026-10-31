from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

import TM_CORE_PYTHON_v0751_STREAMING as core

FEED = Path(
    r"C:\Users\profesor\OpenBot\Shared\Transfers\fb8c2a5d-d62c-48d0-8120-bae2016283c4\TM_TICKFEED_1615_1730.csv"
)
CUTOFFS = [
    "16:21:54.482",
    "16:22:52.576",
    "16:23:01.216",
    "16:24:58.066",
    "16:25:00.000",
    "16:30:00.000",
    "16:45:00.000",
    "17:00:00.000",
    "17:02:00.082",
    "17:15:00.000",
    "17:29:59.897",
]


def _event_signature(event: dict) -> tuple:
    return (
        event.get("function"),
        event.get("bar_time"),
        event.get("direction"),
        event.get("reading_id"),
        event.get("origin"),
        event.get("extreme"),
        event.get("size"),
        event.get("tt_target"),
        event.get("tt_100"),
        event.get("ft"),
        event.get("reason"),
    )


def _local_signature(event: dict) -> tuple:
    return (
        event["sequence_id"],
        event["function"],
        event["bar_time"],
        event["direction"],
        event["origin"],
        event["extreme"],
        event["size"],
        event["confirmation_time_ms"],
    )


def _cutoff_ms(points: list[core.Pt], target: str) -> int:
    eligible = [
        point.time_ms
        for point in points
        if core.ms_to_text(point.time_ms).split(" ")[1] <= target
    ]
    if not eligible:
        raise AssertionError(f"cutoff sin ticks: {target}")
    return max(eligible)


def main() -> int:
    points, bars = core.load_feed(FEED)
    full = core.run_engine(points, bars)
    rows = []
    failures = 0
    for target in CUTOFFS:
        cutoff = _cutoff_ms(points, target)
        prefix_points = [point for point in points if point.time_ms <= cutoff]
        prefix = core.run_engine(prefix_points, bars)
        expected_events = [
            _event_signature(event)
            for event in full.events
            if event["knowledge_time_ms"] <= cutoff
            and event["function"] not in {"FIN_FEED", "START"}
            and event.get("reason") != "END_OF_FEED"
        ]
        observed_events = [
            _event_signature(event)
            for event in prefix.events
            if event["knowledge_time_ms"] <= cutoff
            and event["function"] not in {"FIN_FEED", "START"}
            and event.get("reason") != "END_OF_FEED"
        ]
        expected_local = [
            _local_signature(event)
            for event in full.local_events
            if event["confirmation_time_ms"] <= cutoff
        ]
        observed_local = [
            _local_signature(event)
            for event in prefix.local_events
            if event["confirmation_time_ms"] <= cutoff
        ]
        event_ok = expected_events == observed_events
        local_ok = expected_local == observed_local
        rows.append(
            {
                "cutoff": target,
                "cutoff_ms": cutoff,
                "points": len(prefix_points),
                "events_expected": len(expected_events),
                "events_observed": len(observed_events),
                "local_expected": len(expected_local),
                "local_observed": len(observed_local),
                "events_ok": event_ok,
                "local_ok": local_ok,
                "pass": event_ok and local_ok,
            }
        )
        if not (event_ok and local_ok):
            failures += 1
    out = ROOT / "out_v0751" / "prefix_v0751.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps({"failures": failures, "rows": rows}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for row in rows:
        print(
            f"{'PASS' if row['pass'] else 'FAIL'} {row['cutoff']} "
            f"events={row['events_observed']}/{row['events_expected']} "
            f"local={row['local_observed']}/{row['local_expected']}"
        )
    print(f"PREFIJOS v0751: fallos={failures}/{len(rows)}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())



