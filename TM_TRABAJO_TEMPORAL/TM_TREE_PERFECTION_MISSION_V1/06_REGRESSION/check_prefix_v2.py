#!/usr/bin/env python3
"""Prefix consistency check for blind_reader_v2.

A prefix run must produce exactly the same trace rows as the full run up to
the last tick of the prefix. No future information may change a past tick.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "01_BLIND_READINGS"))
import blind_reader_v2 as br  # noqa: E402


def main() -> int:
    ticks = br.load_ticks(br.FEED)
    full = br.Reader(ticks, a_mode="b100").run()
    checks = []
    ok = True
    for pb in ("16:20", "16:30", "16:49", "17:00", "17:15"):
        cut = [t for t in ticks if t.bar % 1440 <= br.bar_of(pb)]
        pref = br.Reader(cut, a_mode="b100").run()
        n = len(pref.trace)
        mismatch = None
        for i in range(n):
            if pref.trace[i] != full.trace[i]:
                mismatch = i
                break
        checks.append({
            "prefix_bar": pb,
            "ticks": n,
            "rows_compared": n,
            "mismatch_index": mismatch,
            "pass": mismatch is None,
        })
        ok = ok and mismatch is None
    payload = {
        "reader": "blind_reader_v2.py",
        "a_mode": "b100",
        "full_ticks": len(ticks),
        "full_trace_sha256": full.summary()["trace_sha256"],
        "all_prefixes_pass": ok,
        "checks": checks,
    }
    out = BASE / "06_REGRESSION" / "PREFIX_CHECK_V2.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
