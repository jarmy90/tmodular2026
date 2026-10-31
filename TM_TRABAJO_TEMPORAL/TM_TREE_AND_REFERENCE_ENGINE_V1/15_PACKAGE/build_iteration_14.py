#!/usr/bin/env python3
"""Empaqueta la ITERACION 14 (TM_ITERATION_14_REVIEW.zip)."""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

PROJ = Path(__file__).resolve().parents[3]
V1 = Path(__file__).resolve().parents[1]

MEMBERS = [
    (PROJ / "TM_CANON_ACTIVO/01_ARBOL/TM_PATCH_CANONICO_v2_20_PLANO_Y_CUT.md",
     "01_NORMATIVA/TM_PATCH_CANONICO_v2_20_PLANO_Y_CUT.md"),
    (PROJ / "TM_CANON_ACTIVO/03_LECTURAS_HUMANAS/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v005.txt",
     "01_NORMATIVA/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v005.txt"),
    (V1 / "05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py",
     "02_ENGINE/tm_reference_interpreter_v1_direct_aut.py"),
    (V1 / "05_REFERENCE_ENGINE/tm_concurrent_readings.py",
     "02_ENGINE/tm_concurrent_readings.py"),
    (V1 / "04_CONCEPT_TESTS/run_core_tests.py", "03_TESTS/run_core_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_ab_candidate_tests.py",
     "03_TESTS/run_ab_candidate_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_direct_aut_tests.py",
     "03_TESTS/run_direct_aut_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_iteration_09_tests.py",
     "03_TESTS/run_iteration_09_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_iteration_10_tests.py",
     "03_TESTS/run_iteration_10_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_iteration_11_tests.py",
     "03_TESTS/run_iteration_11_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_iteration_12_tests.py",
     "03_TESTS/run_iteration_12_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_iteration_13_tests.py",
     "03_TESTS/run_iteration_13_tests.py"),
    (V1 / "04_CONCEPT_TESTS/run_iteration_14_all.py",
     "03_TESTS/run_iteration_14_all.py"),
    (V1 / "04_CONCEPT_TESTS/run_tick_comparison.py",
     "03_TESTS/run_tick_comparison.py"),
    (V1 / "04_CONCEPT_TESTS/ITER14_TEST_RESULTS.csv",
     "04_RESULTS/ITER14_TEST_RESULTS.csv"),
    (V1 / "04_CONCEPT_TESTS/ITER14_TEST_RESULTS.json",
     "04_RESULTS/ITER14_TEST_RESULTS.json"),
    (V1 / "04_CONCEPT_TESTS/TICK_COMPARISON_ITER14.csv",
     "04_RESULTS/TICK_COMPARISON_ITER14.csv"),
    (V1 / "04_CONCEPT_TESTS/FIRST_DIVERGENCE_ITER14.csv",
     "04_RESULTS/FIRST_DIVERGENCE_ITER14.csv"),
    (V1 / "10_REPORTS/AUDITORIA_ITERACION_14.md", "05_DOCS/AUDITORIA_ITERACION_14.md"),
    (V1 / "10_REPORTS/CHECKPOINT_14.md", "05_DOCS/CHECKPOINT_14.md"),
    (V1 / "09_OPEN_RULES/OPEN_RULES_ITERACION_14.md",
     "05_DOCS/OPEN_RULES_ITERACION_14.md"),
    (V1 / "14_CHANGELOG/CHANGELOG_ITERACION_14.md", "05_DOCS/CHANGELOG_ITERACION_14.md"),
    (V1 / "08_TREE_PYTHON_COMPARISON/TREE_PYTHON_MATRIX_ITER14.csv",
     "06_MATRIX/TREE_PYTHON_MATRIX_ITER14.csv"),
]

OUT = V1 / "15_PACKAGE" / "TM_ITERATION_14_REVIEW.zip"
FORBIDDEN = ("tickfeed", ".env", "credential", "secret", ".git/", "__pycache__")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main() -> int:
    missing = [str(s) for s, _ in MEMBERS if not s.exists()]
    if missing:
        print("FALTAN:")
        for m in missing:
            print("  ", m)
        return 1
    if len(MEMBERS) + 2 > 25:
        print("DEMASIADOS MIEMBROS:", len(MEMBERS) + 2)
        return 1

    manifest, sums = [], []
    for src, arc in MEMBERS:
        digest = sha(src)
        manifest.append({"path": arc, "bytes": src.stat().st_size, "sha256": digest})
        sums.append(f"{digest}  {arc}")

    manifest_txt = json.dumps({"iteration": 14, "files": manifest}, indent=2,
                              ensure_ascii=False)
    sums_txt = "\n".join(sums) + "\n"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for src, arc in MEMBERS:
            zf.write(src, arc)
        zf.writestr("MANIFEST.json", manifest_txt)
        zf.writestr("SHA256SUMS.txt", sums_txt)

    # verificacion: reabrir y comprobar
    with zipfile.ZipFile(OUT) as zf:
        names = zf.namelist()
        bad = zf.testzip()
        forbidden = [n for n in names if any(f in n.lower() for f in FORBIDDEN)]
        recomputed = {n: hashlib.sha256(zf.read(n)).hexdigest().upper()
                      for n in names if n not in ("MANIFEST.json", "SHA256SUMS.txt")}
    assert bad is None, bad
    assert not forbidden, forbidden
    assert len(names) <= 25, len(names)
    mismatch = [m["path"] for m in manifest
                if recomputed[m["path"]] != m["sha256"]]
    assert not mismatch, mismatch

    print(f"ZIP        : {OUT}")
    print(f"bytes      : {OUT.stat().st_size}")
    print(f"sha256     : {sha(OUT)}")
    print(f"members    : {len(names)}")
    print(f"integrity  : PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
