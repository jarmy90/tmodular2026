from __future__ import annotations

import argparse
import bisect
import csv
import json
import random
import subprocess
import sys
import tempfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "audit_v075"))

import audit_v075_common as ac

core = ac.core

SEED = 20261016
RUNNER = Path(__file__).with_name("audit_v075_prefix_run.py")


def previous_time(points: list, index: int) -> int:
    return points[max(0, index - 1)].time_ms


def add_cut(cutoffs: dict[int, set[str]], cutoff: int, reason: str, lo: int, hi: int) -> None:
    if lo <= cutoff <= hi:
        cutoffs[cutoff].add(reason)


def find_r0062(engine) -> object:
    target_origin = core.price_i(29667.30)
    target_extreme = core.price_i(29602.10)
    matches = [
        reading
        for reading in engine.readings
        if reading.module_origin == target_origin
        and reading.module_extreme == target_extreme
        and reading.a_size == core.price_i(78.30)
        and reading.b_size == core.price_i(80.20)
    ]
    if len(matches) != 1:
        raise SystemExit(f"R0062 mapping not unique: {[r.reading_id for r in matches]}")
    return matches[0]


def threshold_cutoffs(engine, points: list, cutoffs: dict[int, set[str]]) -> None:
    seqs = [point.seq for point in points]
    for reading in engine.readings:
        if not reading.a_end or not reading.b_extreme or not reading.direction:
            continue
        start = bisect.bisect_left(seqs, reading.a_end_seq)
        end = bisect.bisect_right(seqs, reading.b_extreme_seq)
        b100 = None
        aut = None
        for index in range(start, end):
            point = points[index]
            signed = (point.price - reading.a_end) * reading.direction
            if b100 is None and signed >= reading.a_size:
                b100 = index
            if aut is None and signed > int(reading.a_size * 1.27) + 25:
                aut = index
            if b100 is not None and aut is not None:
                break
        for label, index in (("umbral_B_100", b100), ("umbral_AUT", aut)):
            if index is None:
                continue
            add_cut(cutoffs, points[index].time_ms, label, points[0].time_ms, points[-1].time_ms)
            add_cut(
                cutoffs,
                previous_time(points, index),
                f"{label}_antes",
                points[0].time_ms,
                points[-1].time_ms,
            )


def build_cutoffs(engine, points: list) -> tuple[dict[int, set[str]], dict]:
    lo = points[0].time_ms
    hi = points[-1].time_ms
    cutoffs: dict[int, set[str]] = defaultdict(set)

    last_by_bar: dict[int, int] = {}
    for index, point in enumerate(points):
        last_by_bar[point.bar] = index
    for index in last_by_bar.values():
        add_cut(cutoffs, points[index].time_ms, "cierre_vela", lo, hi)

    event_times = sorted(
        {
            event["knowledge_time_ms"]
            for event in engine.events
            if event["kind"] != "FIN_FEED"
        }
    )
    for event_time in event_times:
        index = bisect.bisect_left([point.time_ms for point in points], event_time)
        if index >= len(points):
            index = len(points) - 1
        add_cut(cutoffs, event_time, "evento", lo, hi)
        add_cut(cutoffs, previous_time(points, index), "evento_antes", lo, hi)

    threshold_cutoffs(engine, points, cutoffs)

    r0062 = find_r0062(engine)
    start = bisect.bisect_left([point.time_ms for point in points], r0062.module_origin_time)
    end = bisect.bisect_right([point.time_ms for point in points], r0062.ft_time)
    for point in points[start:end]:
        add_cut(cutoffs, point.time_ms, "r0062_todos", lo, hi)

    rng = random.Random(SEED)
    times = sorted({point.time_ms for point in points})
    for cutoff in rng.sample(times, 500):
        add_cut(cutoffs, cutoff, "aleatorio_500", lo, hi)

    metadata = {
        "seed": SEED,
        "r0062_full_reading": r0062.reading_id,
        "r0062_window": [core.ms_to_text(r0062.module_origin_time), core.ms_to_text(r0062.ft_time)],
        "r0062_points": end - start,
        "feed_points": len(points),
    }
    return cutoffs, metadata


def compare_signatures(expected: dict, actual: dict) -> tuple[bool, list[str]]:
    differences: list[str] = []
    for section in ("events", "reading_identity", "reading_closed"):
        left = expected[section]
        right = actual.get(section, {})
        for field in ("count", "digest", "first_event_id", "last_event_id", "ids"):
            if field not in left:
                continue
            if left.get(field) != right.get(field):
                differences.append(f"{section}.{field}")
    expected_active = expected["reading_identity"]["count"] - expected["reading_closed"]["count"]
    actual_active = actual.get("reading_identity", {}).get("count", 0) - actual.get(
        "reading_closed", {}
    ).get("count", 0)
    if expected_active != actual_active:
        differences.append("active_count")
    return not differences, differences


def run_cutoff(
    cutoff: int,
    reasons: list[str],
    source_header: list[str],
    source_rows: list[list[str]],
    source_times: list[int],
    expected: dict,
    temp_root: Path,
) -> dict:
    index = bisect.bisect_right(source_times, cutoff)
    safe = f"{cutoff}"
    prefix_path = temp_root / f"prefix_{safe}.csv"
    snapshot_path = temp_root / f"prefix_{safe}.json"
    with prefix_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter=";", lineterminator="\n")
        writer.writerow(source_header)
        writer.writerows(source_rows[:index])
    command = [
        sys.executable,
        str(RUNNER),
        "--feed",
        str(prefix_path),
        "--cutoff",
        str(cutoff),
        "--out",
        str(snapshot_path),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if completed.returncode != 0:
        return {
            "cutoff_ms": cutoff,
            "cutoff_time": core.ms_to_text(cutoff),
            "reasons": "|".join(sorted(reasons)),
            "pass": 0,
            "differences": "runner_error",
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip()[-3000:],
            "points": index,
        }
    try:
        actual = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "cutoff_ms": cutoff,
            "cutoff_time": core.ms_to_text(cutoff),
            "reasons": "|".join(sorted(reasons)),
            "pass": 0,
            "differences": f"snapshot_error:{exc}",
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip()[-3000:],
            "points": index,
        }
    finally:
        prefix_path.unlink(missing_ok=True)
        snapshot_path.unlink(missing_ok=True)
    ok, differences = compare_signatures(expected, actual)
    return {
        "cutoff_ms": cutoff,
        "cutoff_time": core.ms_to_text(cutoff),
        "reasons": "|".join(sorted(reasons)),
        "points": actual.get("points", index),
        "events_count": actual.get("events", {}).get("count", 0),
        "readings_created": actual.get("reading_identity", {}).get("count", 0),
        "readings_closed": actual.get("reading_closed", {}).get("count", 0),
        "pass": int(ok),
        "differences": "|".join(differences),
        "expected_events": expected["events"]["count"],
        "expected_readings_created": expected["reading_identity"]["count"],
        "expected_readings_closed": expected["reading_closed"]["count"],
        "actual_event_digest": actual.get("events", {}).get("digest", ""),
        "expected_event_digest": expected["events"]["digest"],
        "actual_reading_digest": actual.get("reading_identity", {}).get("digest", ""),
        "expected_reading_digest": expected["reading_identity"]["digest"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--feed",
        default=str(ac.FEED),
    )
    parser.add_argument("--out", default=str(ROOT / "out_v075_audit2"))
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    feed = Path(args.feed)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    points, bars = core.load_feed(feed)
    full = core.run_engine(points, bars)
    cutoffs, metadata = build_cutoffs(full, points)
    ordered = sorted(cutoffs.items())
    if args.limit:
        ordered = ordered[: args.limit]
    print(f"prefix audit: cutoffs={len(ordered)} points={len(points)} workers={args.workers}", flush=True)

    with feed.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter=";")
        source_header = next(reader)
        source_rows = list(reader)
    time_column = source_header.index("time_msc")
    source_times = [int(row[time_column]) for row in source_rows]

    temp_root = Path(tempfile.mkdtemp(prefix="tm_prefix_", dir=str(ROOT)))
    rows: list[dict] = []
    try:
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            futures = {}
            for cutoff, reasons in ordered:
                expected = ac.prefix_signature(full, cutoff)
                future = pool.submit(
                    run_cutoff,
                    cutoff,
                    sorted(reasons),
                    source_header,
                    source_rows,
                    source_times,
                    expected,
                    temp_root,
                )
                futures[future] = cutoff
            for count, future in enumerate(as_completed(futures), 1):
                row = future.result()
                rows.append(row)
                if count % 250 == 0:
                    failures = sum(1 for item in rows if not item["pass"])
                    print(f"  {count}/{len(futures)} failures={failures}", flush=True)
    finally:
        for path in temp_root.glob("*"):
            path.unlink(missing_ok=True)
        temp_root.rmdir()

    rows.sort(key=lambda item: item["cutoff_ms"])
    failures = [row for row in rows if not row["pass"]]
    r0062_rows = [
        row for row in rows if "r0062_todos" in row["reasons"].split("|")
    ]
    summary = {
        "feed": str(feed),
        "seed": metadata["seed"],
        "r0062_full_reading": metadata["r0062_full_reading"],
        "r0062_window": metadata["r0062_window"],
        "r0062_points": metadata["r0062_points"],
        "feed_points": metadata["feed_points"],
        "cutoffs": len(rows),
        "pass": len(rows) - len(failures),
        "failures": len(failures),
        "prefix_failures": len(failures),
        "r0062_cutoffs": len(r0062_rows),
        "r0062_failures": sum(1 for row in r0062_rows if not row["pass"]),
        "category_counts": {
            reason: sum(1 for row in rows if reason in row["reasons"].split("|"))
            for reason in sorted({reason for row in rows for reason in row["reasons"].split("|")})
        },
        "first_failure": failures[0] if failures else None,
    }
    ac.write_json(out / "P00_PrefijosResumen.json", summary)
    ac.write_csv(
        out / "P02_PrefijosMatriz.csv",
        [
            "cutoff_ms",
            "cutoff_time",
            "reasons",
            "points",
            "events_count",
            "readings_created",
            "readings_closed",
            "expected_events",
            "expected_readings_created",
            "expected_readings_closed",
            "pass",
            "differences",
            "actual_event_digest",
            "expected_event_digest",
            "actual_reading_digest",
            "expected_reading_digest",
        ],
        rows,
    )
    ac.write_csv(
        out / "P01_PrefijosFallos.csv",
        [
            "cutoff_ms",
            "cutoff_time",
            "reasons",
            "points",
            "pass",
            "differences",
            "expected_events",
            "expected_readings_created",
            "expected_readings_closed",
            "actual_event_digest",
            "expected_event_digest",
            "actual_reading_digest",
            "expected_reading_digest",
            "stdout",
            "stderr",
        ],
        failures,
    )
    ac.write_json(
        out / "P03_R0062Prefijos.json",
        {
            "reading": metadata["r0062_full_reading"],
            "window": metadata["r0062_window"],
            "cutoffs": len(r0062_rows),
            "failures": sum(1 for row in r0062_rows if not row["pass"]),
            "first_failure": next((row for row in r0062_rows if not row["pass"]), None),
        },
    )
    print(
        f"prefix done: pass={summary['pass']}/{summary['cutoffs']} "
        f"failures={summary['failures']} r0062={len(r0062_rows)} "
        f"r0062_failures={summary['r0062_failures']}",
        flush=True,
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
