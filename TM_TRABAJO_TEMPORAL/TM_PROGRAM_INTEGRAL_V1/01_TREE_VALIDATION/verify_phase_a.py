# -*- coding: utf-8 -*-
"""Verificacion Fase A: doble ejecucion, prefijos y ausencia de futuro."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import blind_reader as br  # noqa: E402

FEED = br.FEED
BLOCK_START = "16:49"
BLOCK_END = "17:29"


def bar_of(h: str) -> int:
    hh, mm = h.split(":")
    return int(hh) * 60 + int(mm)


def load_all() -> list[br.Tick]:
    return br.load_ticks(FEED)


def run(ticks: list[br.Tick]):
    return br.Reader(ticks).run()


def trace_hash(trace) -> str:
    blob = json.dumps(trace, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(blob).hexdigest()


def main():
    ticks = [t for t in load_all()
             if bar_of("16:15") <= t.bar % 1440 <= bar_of(BLOCK_END)]

    r1 = run(ticks)
    h1 = trace_hash(r1.trace)
    r2 = run(ticks)
    h2 = trace_hash(r2.trace)

    full = {row["sequence_id"]: row for row in r1.trace}
    last_by_bar = {}
    for t in ticks:
        last_by_bar[t.bar % 1440] = t.seq

    results = []
    for b in range(bar_of(BLOCK_START), bar_of(BLOCK_END) + 1):
        if b not in last_by_bar:
            continue
        cut = last_by_bar[b]
        sub = [t for t in ticks if t.seq <= cut]
        rp = run(sub)
        row = rp.trace[-1]
        same = row == full[cut]
        results.append({"bar": f"{b // 60:02d}:{b % 60:02d}", "sequence_id": cut, "match": same})
        if not same:
            print("MISMATCH", results[-1])
            keys = set(row) | set(full[cut])
            for k in sorted(keys):
                if row.get(k) != full[cut].get(k):
                    print("  field", k, row.get(k), "!=", full[cut].get(k))

    out = {
        "determinism": {"run1": h1, "run2": h2, "equal": h1 == h2},
        "prefixes_checked": len(results),
        "prefixes_ok": sum(1 for x in results if x["match"]),
        "prefix_failures": [x for x in results if not x["match"]],
        "ticks": len(ticks),
        "readings": len(r1.readings),
        "generations": r1.active.generation + 1 if r1.active else 0,
    }
    print(json.dumps(out, indent=1, ensure_ascii=False))
    (HERE / "verify_phase_a.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    return 0 if out["determinism"]["equal"] and out["prefixes_ok"] == out["prefixes_checked"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
