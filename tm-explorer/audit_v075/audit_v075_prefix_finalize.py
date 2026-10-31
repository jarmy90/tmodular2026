from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "audit_v075"))

import audit_v075_common as ac

SHARD = Path(__file__).with_name("audit_v075_prefix_shard.py")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--feed",
        default=str(ac.FEED),
    )
    parser.add_argument("--out", default=str(ROOT / "out_v075_audit2"))
    parser.add_argument("--shards", type=int, default=4)
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    processes = []
    shard_paths = []
    env = dict(os.environ)
    env["PYTHONUNBUFFERED"] = "1"
    for shard in range(args.shards):
        path = out / f"P_shard_{shard}.jsonl"
        shard_paths.append(path)
        command = [
            sys.executable,
            str(SHARD),
            "--feed",
            args.feed,
            "--out-jsonl",
            str(path),
            "--shard",
            str(shard),
            "--shards",
            str(args.shards),
        ]
        processes.append(subprocess.Popen(command, env=env))
    codes = [process.wait() for process in processes]
    if any(code != 0 for code in codes):
        print(f"shard exit codes: {codes}", flush=True)

    rows = []
    for path in shard_paths:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    rows.append(json.loads(line))
    if not rows:
        raise SystemExit("no prefix rows")
    rows.sort(key=lambda item: item["cutoff_ms"])
    failures = [row for row in rows if not row["pass"]]
    r0062_rows = [row for row in rows if "r0062_todos" in row["reasons"].split("|")]
    summary = {
        "feed": args.feed,
        "seed": 20261016,
        "process_model": "un proceso por shard; recarga fisica del CSV y motor nuevos por corte",
        "shards": args.shards,
        "shard_exit_codes": codes,
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
            "shard",
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
            "shard",
        ],
        failures,
    )
    ac.write_json(
        out / "P03_R0062Prefijos.json",
        {
            "reading": "R0064",
            "window": ["2026-10-16 16:51:11.326", "2026-10-16 16:57:34.937"],
            "cutoffs": len(r0062_rows),
            "failures": sum(1 for row in r0062_rows if not row["pass"]),
            "first_failure": next((row for row in r0062_rows if not row["pass"]), None),
        },
    )
    print(
        f"prefix finalize: pass={summary['pass']}/{summary['cutoffs']} "
        f"failures={summary['failures']} r0062={len(r0062_rows)} "
        f"r0062_failures={summary['r0062_failures']}",
        flush=True,
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
