"""Determinism and prefix checks on the two real anchors."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))

from tm_reference_interpreter_v1 import FEED, Reader, load_ticks  # noqa: E402


def digest(rows: list[dict]) -> str:
    payload = json.dumps(rows, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def run(ticks, rid):
    return Reader(ticks, reading_id=rid).run()


def main() -> int:
    ticks = load_ticks(FEED)
    l2 = [t for t in ticks if 16 * 60 + 19 <= t.bar % 1440 <= 16 * 60 + 22]
    l2_prefix = [t for t in l2 if t.bar % 1440 <= 16 * 60 + 21]
    l1 = [t for t in ticks if 16 * 60 + 15 <= t.bar % 1440 <= 16 * 60 + 18]

    a = run(l2, "L2")
    b = run(l2, "L2")
    p = run(l2_prefix, "L2")
    c = run(l1, "L1")
    d = run(l1, "L1")

    checks = {
        "l2_double_trace": digest(a.trace) == digest(b.trace),
        "l2_double_events": digest(a.events) == digest(b.events),
        "l2_prefix": p.trace == a.trace[:len(p.trace)]
        and [e for e in p.events if e["event"] != "CORE_END"]
        == [e for e in a.events if e["event"] != "CORE_END"][:len([e for e in p.events if e["event"] != "CORE_END"])],
        "l1_double_trace": digest(c.trace) == digest(d.trace),
        "l1_double_events": digest(c.events) == digest(d.events),
    }
    summary = {
        "checks": checks,
        "all_pass": all(checks.values()),
        "l2_trace_sha256": digest(a.trace),
        "l2_trace_lines": len(a.trace),
        "l2_prefix_lines": len(p.trace),
        "l1_trace_sha256": digest(c.trace),
        "l1_trace_lines": len(c.trace),
    }
    (HERE / "CORE_REPLAY_CHECKS.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
