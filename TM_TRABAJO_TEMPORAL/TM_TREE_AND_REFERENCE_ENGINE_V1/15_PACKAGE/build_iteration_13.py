#!/usr/bin/env python3
"""Empaqueta la ITERACION 13 (TM_ITERATION_13_REVIEW.zip)."""
from __future__ import annotations

import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

PROJ = Path(__file__).resolve().parents[3]
V1 = Path(__file__).resolve().parents[1]

MEMBERS = [
    (PROJ / "TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md",
     "01_NORMATIVA/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md"),
    (PROJ / "TM_CANON_ACTIVO/01_ARBOL/TM_PATCH_CANONICO_v2_20_PLANO_Y_CUT.md",
     "01_NORMATIVA/TM_PATCH_CANONICO_v2_20_PLANO_Y_CUT.md"),
    (V1 / "05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py",
     "02_ENGINE/tm_reference_interpreter_v1_direct_aut.py"),
    (V1 / "05_REFERENCE_ENGINE/tm_concurrent_readings.py", "02_ENGINE/tm_concurrent_readings.py"),
    (V1 / "04_CONCEPT_TESTS/run_core_tests.py", "03_TESTS/run_core_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_ab_candidate_tests.py", "03_TESTS/run_ab_candidate_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_direct_aut_tests.py", "03_TESTS/run_direct_aut_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_iteration_09_tests.py", "03_TESTS/run_iteration_09_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_iteration_10_tests.py", "03_TESTS/run_iteration_10_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_iteration_11_tests.py", "03_TESTS/run_iteration_11_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_iteration_12_tests.py", "03_TESTS/run_iteration_12_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_iteration_13_tests.py", "03_TESTS/run_iteration_13_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_block_comparison.py", "03_TESTS/run_block_comparison.py"),
    (V1 / "04_CONCEPT_TESTS/run_rotation_audit.py", "03_TESTS/run_rotation_audit.py"),
    (V1 / "04_CONCEPT_TESTS/run_full_feed.py", "03_TESTS/run_full_feed.py"),
    (V1 / "04_CONCEPT_TESTS/ITER13_TEST_RESULTS.csv", "04_RESULTS/ITER13_TEST_RESULTS.csv"),
    (V1 / "04_CONCEPT_TESTS/ITER13_TEST_RESULTS.json", "04_RESULTS/ITER13_TEST_RESULTS.json"),
    (V1 / "04_CONCEPT_TESTS/ITER12_TEST_RESULTS.json", "04_RESULTS/ITER12_TEST_RESULTS.json"),
    (V1 / "04_CONCEPT_TESTS/HUMAN_BLOCK_COMPARISON.csv", "04_RESULTS/HUMAN_BLOCK_COMPARISON.csv"),
    (V1 / "04_CONCEPT_TESTS/ROTATION_AUDIT.json", "04_RESULTS/ROTATION_AUDIT.json"),
    (V1 / "04_CONCEPT_TESTS/ROTATION_AUDIT.csv", "04_RESULTS/ROTATION_AUDIT.csv"),
    (V1 / "07_REAL_REPLAYS/full_feed_metrics.json", "04_RESULTS/FULL_FEED_METRICS.json"),
    (V1 / "10_REPORTS/AUDITORIA_ITERACION_13.md", "05_DOCS/AUDITORIA_ITERACION_13.md"),
    (V1 / "10_REPORTS/CHECKPOINT_13.md", "05_DOCS/CHECKPOINT_13.md"),
    (V1 / "09_OPEN_RULES/OPEN_RULES_ITERACION_13.md", "05_DOCS/OPEN_RULES_ITERACION_13.md"),
    (V1 / "14_CHANGELOG/CHANGELOG_ITERACION_13.md", "05_DOCS/CHANGELOG_ITERACION_13.md"),
    (V1 / "08_TREE_PYTHON_COMPARISON/TREE_PYTHON_MATRIX_ITER13.csv",
     "06_MATRIX/TREE_PYTHON_MATRIX_ITER13.csv"),
]

OUT = V1 / "15_PACKAGE" / "TM_ITERATION_13_REVIEW.zip"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main() -> int:
    missing = [str(s) for s, _ in MEMBERS if not s.exists()]
    if missing:
        print("MISSING:", missing)
        return 1
    entries = [{"archive_path": a,
                "source_path": str(s.relative_to(PROJ)).replace("\\", "/"),
                "size_bytes": s.stat().st_size, "sha256": sha(s)}
               for s, a in MEMBERS]
    manifest = {
        "package": "TM_ITERATION_13_REVIEW",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "baseline": "TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT",
        "normative_source": "TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md",
        "normative_patch_added": "TM_PATCH_CANONICO_v2_20_PLANO_Y_CUT.md",
        "tree_modified": False,
        "tree_frozen": False,
        "official_engine_created": False,
        "q_cut": "CLOSED",
        "test_totals": {"total": 145, "passed": 145, "failed": 0,
                        "canonical": 79, "provisional": 62, "open_rule_block": 4},
        "human_comparison": {
            "B1_16_15_16_18": "MATCH",
            "B2_16_19_16_22": "MATCH except 1 knowledge time at 16:19 (PROVISIONAL)",
            "B3_16_22_16_24": "DIVERGES at 16:23 (Q-CONCURRENCY, OPEN)",
            "B4_16_24_16_25": "new 1 from 29848,5 MATCH; TT after gap OPEN (Q-GAP-TT)",
        },
        "rotation_metrics": {"cycle_rotations": 47, "closed_by_tt": 2,
                             "started_by_gap": 38, "started_by_c_trend": 3,
                             "initial": 1, "cascades": 0},
        "members": entries,
    }
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("MANIFEST.json", json.dumps(manifest, indent=2, ensure_ascii=False))
        sums = []
        for e in entries:
            zf.writestr(e["archive_path"], (PROJ / e["source_path"]).read_bytes())
            sums.append(f"{e['sha256']}  {e['archive_path']}")
        zf.writestr("SHA256SUMS.txt", "\n".join(sums) + "\n")
    print(f"ZIP  {OUT}")
    print(f"size {OUT.stat().st_size} bytes")
    print(f"sha  {sha(OUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
