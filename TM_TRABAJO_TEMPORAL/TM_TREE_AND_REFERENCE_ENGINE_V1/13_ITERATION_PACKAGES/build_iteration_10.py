#!/usr/bin/env python3
"""ITERACION 10 — gap + concurrencia + feed completo (ZIP <=25 miembros)."""
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]

FILES = [
    ("10_REPORTS/CHECKPOINT_10_GAP_CONCURRENCY.md", "01_CHECKPOINT_10.md"),
    ("09_OPEN_RULES/OPEN_RULES_C_GRANDE_V1.md", "02_OPEN_RULES.md"),
    ("04_CONCEPT_TESTS/GAP_CONCURRENCY_TEST_RESULTS.csv", "03_TEST_RESULTS_GAP_CONC.csv"),
    ("04_CONCEPT_TESTS/ITERATION_10_TEST_RESULTS.json", "04_TEST_RESULTS.json"),
    ("04_CONCEPT_TESTS/ITERATION_09_TEST_RESULTS.json", "05_REGRESSION_09.json"),
    ("07_REAL_REPLAYS/full_feed_metrics.json", "06_FULL_FEED_METRICS.json"),
    ("05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py", "07_INTERPRETER.py"),
    ("05_REFERENCE_ENGINE/tm_concurrent_readings.py", "08_CONCURRENCY.py"),
    ("04_CONCEPT_TESTS/run_iteration_10_tests.py", "09_RUNNER_GAP_CONC.py"),
    ("04_CONCEPT_TESTS/run_full_feed.py", "10_RUNNER_FULL_FEED.py"),
    ("07_REAL_REPLAYS/direct_aut_state_L1_1615_1618.json", "11_STATE_L1.json"),
    ("07_REAL_REPLAYS/direct_aut_state_L2_1619_1622.json", "12_STATE_L2.json"),
    ("07_REAL_REPLAYS/direct_aut_events_L2_1619_1622.csv", "13_EVENTS_L2.csv"),
    ("08_TREE_PYTHON_COMPARISON/C_GRANDE_TREE_PYTHON_MATRIX_V1.csv", "14_MATRIX_C.csv"),
]


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main() -> int:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    name = f"ITERACION_10_GAP_CONCURRENCY_{ts}"
    pkg = ROOT / "TM_ENTREGAS_ITERACION" / name
    zip_path = ROOT / "TM_ITERATION_10_REVIEW.zip"
    pkg.mkdir(parents=True)
    if zip_path.exists():
        zip_path.unlink()

    files = []
    for rel, flat in FILES:
        src = BASE / rel
        if not src.exists():
            raise SystemExit(f"falta: {src}")
        dst = pkg / flat
        shutil.copy2(src, dst)
        files.append({"original": rel, "package_name": flat,
                      "size": dst.stat().st_size, "sha256": sha(dst)})

    manifest = {
        "iteration_id": "ITERACION_10_GAP_CONCURRENCY",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "engine": "TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT (revision 10)",
        "objective": "gap explicito con propiedad funcional y concurrencia L1/L2",
        "files": files,
        "gates": ["GATE_GAP_PASS", "GATE_CONCURRENCY_PASS"],
        "tests": {"gap_concurrency": {"total": 11, "passed": 11},
                  "regression_09": {"total": 82, "passed": 82}},
        "full_feed": {"ticks": 20335, "deterministic": True,
                      "prefix_consistent": True, "events": 335,
                      "finding": "un solo ciclo; ciclo de 1 en OPEN_RULE_BLOCK"},
        "open_rule_blocks": ["CYCLE_1", "CUT", "TT", "FT"],
        "originals_modified": False,
        "tree_modified": False,
        "official_engine_modified": False,
        "TREE_STATUS": "NOT_READY_TO_FREEZE_TREE",
        "REFERENCE_ENGINE_STATUS": "REFERENCE_ENGINE_INCOMPLETE",
        "PATTERN_ENGINE_STATUS": "PATTERN_ENGINE_BLOCKED",
    }
    (pkg / "PACKAGE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (pkg / "SHA256SUMS.txt").write_text(
        "\n".join(f"{sha(f)}  {f.name}"
                  for f in sorted(pkg.iterdir(), key=lambda p: p.name)) + "\n",
        encoding="utf-8")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(pkg.iterdir(), key=lambda p: p.name):
            zf.write(f, f"{name}/{f.name}")

    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        assert zf.testzip() is None
        if len(names) > 25:
            raise SystemExit("demasiados miembros")

    print(json.dumps({
        "package_dir": str(pkg), "zip_path": str(zip_path),
        "zip_size_bytes": zip_path.stat().st_size,
        "zip_sha256": sha(zip_path), "members": len(names),
        "integrity": "PASS",
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
