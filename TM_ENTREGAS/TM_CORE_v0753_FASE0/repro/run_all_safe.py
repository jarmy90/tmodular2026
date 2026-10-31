from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "python" / "TM_CORE_PYTHON_v0752_CANONICAL.py"
FEED = ROOT / "data" / "TM_TICKFEED_1615_1730.csv"
OUT = ROOT / "out"

FROZEN_ZIP = Path(
    r"C:\Users\profesor\tm\Teoria Modular\TM_ENTREGAS\TM_CORE_v0752_R3_B_AUT.zip"
)
FROZEN_SHA = "450379bd5f1e22380614e6112e3fb52c2a653ee8358bf7e5238995af99d3b7db"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def guard_frozen() -> None:
    if not FROZEN_ZIP.exists():
        raise SystemExit(f"FROZEN GUARD: falta {FROZEN_ZIP}")
    got = sha256(FROZEN_ZIP)
    if got != FROZEN_SHA:
        raise SystemExit(
            "FROZEN GUARD: el ZIP congelado cambio.\n"
            f"esperado {FROZEN_SHA}\n"
            f"obtenido {got}\n"
            "Restaurar antes de continuar."
        )


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    print(" ".join(cmd), flush=True)
    return subprocess.run(cmd, **kw)


def main() -> int:
    os.chdir(ROOT)
    guard_frozen()
    OUT.mkdir(exist_ok=True)

    print("SELFTEST:", flush=True)
    run([sys.executable, str(CORE), "--selftest"], check=True)

    print("UNIVERSAL_B_AUT_TESTS:", flush=True)
    run([sys.executable, str(ROOT / "tests" / "test_big_b_aut.py")], check=True)

    print("LEGACY_20_TESTS:", flush=True)
    run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            str(ROOT / "tests" / "legacy_v075" / "TM_CORE_PYTHON_v075_TESTS.py"),
        ],
        check=True,
    )

    print("TRANSFORMATION_TESTS:", flush=True)
    run([sys.executable, str(ROOT / "tests" / "test_transformations.py")], check=True)

    print("CORE:", flush=True)
    run([sys.executable, str(CORE), "--feed", str(FEED), "--out", str(OUT)], check=True)

    print("PHYSICAL_TRANSITION_PREFIXES:", flush=True)
    prefixes = run([sys.executable, str(ROOT / "repro" / "run_transition_prefixes.py")])
    if prefixes.returncode:
        return prefixes.returncode

    print("COMPARISON:", flush=True)
    comparison = run([sys.executable, str(ROOT / "repro" / "compare_golden.py")])

    raw = json.loads((OUT / "CORE_RAW_OUTPUT.json").read_text(encoding="utf-8"))
    prefix_report = json.loads(
        (OUT / "TRANSITION_PREFIXES.json").read_text(encoding="utf-8")
    )
    summary = {
        "core_raw_sha256": sha256(OUT / "CORE_RAW_OUTPUT.json"),
        "feed_points": raw["feed_points"],
        "events": len(raw["events"]),
        "readings": len(raw["readings"]),
        "local_sequences": len(raw["local_sequences"]),
        "local_events": len(raw["local_events"]),
        "comparison_exit": comparison.returncode,
        "transition_prefixes": prefix_report["cuts"],
        "prefix_failures": prefix_report["prefix_failures"],
        "frozen_zip_sha256": sha256(FROZEN_ZIP),
        "frozen_zip_unchanged": sha256(FROZEN_ZIP) == FROZEN_SHA,
    }
    (OUT / "RUN_SUMMARY_SAFE.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    guard_frozen()
    return comparison.returncode


if __name__ == "__main__":
    raise SystemExit(main())
