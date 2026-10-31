#!/usr/bin/env python3
"""Empaqueta la ITERACION 11 en un ZIP verificable.

Incluye: árbol normativo, intérprete, pruebas, resultados, matriz árbol-Python,
informe de auditoría, checkpoint, reglas abiertas, changelog, manifiesto y
SHA256SUMS. No incluye tickfeed, R3/R5, cachés ni credenciales.
"""
from __future__ import annotations

import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # TM_TRABAJO_TEMPORAL
PROJ = Path(__file__).resolve().parents[3]          # Teoria Modular
V1 = Path(__file__).resolve().parents[1]            # TM_TREE_AND_REFERENCE_ENGINE_V1

MEMBERS = [
    # normativa
    (PROJ / "TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md",
     "01_NORMATIVA/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md"),
    # implementación
    (V1 / "05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py",
     "02_ENGINE/tm_reference_interpreter_v1_direct_aut.py"),
    (V1 / "05_REFERENCE_ENGINE/tm_concurrent_readings.py",
     "02_ENGINE/tm_concurrent_readings.py"),
    # pruebas
    (V1 / "04_CONCEPT_TESTS/run_core_tests.py", "03_TESTS/run_core_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_ab_candidate_tests.py", "03_TESTS/run_ab_candidate_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_direct_aut_tests.py", "03_TESTS/run_direct_aut_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_iteration_09_tests.py", "03_TESTS/run_iteration_09_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_iteration_10_tests.py", "03_TESTS/run_iteration_10_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_iteration_11_tests.py", "03_TESTS/run_iteration_11_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_full_feed.py", "03_TESTS/run_full_feed.py"),
    # resultados
    (V1 / "04_CONCEPT_TESTS/CORE_TEST_RESULTS.csv", "04_RESULTS/CORE_TEST_RESULTS.csv"),
    (V1 / "04_CONCEPT_TESTS/AB_CANDIDATE_TEST_RESULTS.csv", "04_RESULTS/AB_CANDIDATE_TEST_RESULTS.csv"),
    (V1 / "04_CONCEPT_TESTS/DIRECT_AUT_TEST_RESULTS.csv", "04_RESULTS/DIRECT_AUT_TEST_RESULTS.csv"),
    (V1 / "04_CONCEPT_TESTS/C_TEST_RESULTS.csv", "04_RESULTS/C_TEST_RESULTS.csv"),
    (V1 / "04_CONCEPT_TESTS/GAP_CONCURRENCY_TEST_RESULTS.csv", "04_RESULTS/GAP_CONCURRENCY_TEST_RESULTS.csv"),
    (V1 / "04_CONCEPT_TESTS/TT_TEST_RESULTS.csv", "04_RESULTS/TT_TEST_RESULTS.csv"),
    (V1 / "07_REAL_REPLAYS/full_feed_metrics.json", "04_RESULTS/FULL_FEED_METRICS.json"),
    # documentación
    (V1 / "10_REPORTS/AUDITORIA_ITERACION_11.md", "05_DOCS/AUDITORIA_ITERACION_11.md"),
    (V1 / "10_REPORTS/CHECKPOINT_11.md", "05_DOCS/CHECKPOINT_11.md"),
    (V1 / "09_OPEN_RULES/OPEN_RULES_ITERACION_11.md", "05_DOCS/OPEN_RULES_ITERACION_11.md"),
    (V1 / "14_CHANGELOG/CHANGELOG_ITERACION_11.md", "05_DOCS/CHANGELOG_ITERACION_11.md"),
    (V1 / "08_TREE_PYTHON_COMPARISON/TREE_PYTHON_MATRIX_ITER11.csv",
     "06_MATRIX/TREE_PYTHON_MATRIX_ITER11.csv"),
]

OUT = V1 / "15_PACKAGE" / "TM_ITERATION_11_REVIEW.zip"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main() -> int:
    missing = [str(src) for src, _ in MEMBERS if not src.exists()]
    if missing:
        print("MISSING:", missing)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    entries = []
    for src, arc in MEMBERS:
        entries.append({
            "archive_path": arc,
            "source_path": str(src.relative_to(PROJ)).replace("\\", "/"),
            "size_bytes": src.stat().st_size,
            "sha256": sha(src),
        })

    manifest = {
        "package": "TM_ITERATION_11_REVIEW",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "baseline": "TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT",
        "normative_source": "TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md",
        "tree_frozen": False,
        "official_engine_created": False,
        "tree_status": "NOT_READY_TO_FREEZE_TREE",
        "reference_engine_status": "REFERENCE_ENGINE_INCOMPLETE",
        "pattern_engine_status": "PATTERN_ENGINE_BLOCKED",
        "test_totals": {"total": 114, "passed": 114, "failed": 0},
        "members": entries,
    }

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("MANIFEST.json", json.dumps(manifest, indent=2, ensure_ascii=False))
        sums = []
        for e in entries:
            with (PROJ / e["source_path"]).open("rb") as fh:
                zf.writestr(e["archive_path"], fh.read())
            sums.append(f"{e['sha256']}  {e['archive_path']}")
        zf.writestr("SHA256SUMS.txt", "\n".join(sums) + "\n")

    print(f"ZIP  {OUT}")
    print(f"size {OUT.stat().st_size} bytes")
    print(f"sha  {sha(OUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
