#!/usr/bin/env python3
"""ITERACION 08 — empaquetado plano + ZIP de revision verificado.

Crea:
  TM_ENTREGAS_ITERACION/ITERACION_08_DIRECT_AUT_<ts>/   (carpeta plana)
  TM_ITERATION_08_REVIEW.zip                            (raiz del proyecto)

No incluye trazas gigantes completas: incluye estado/eventos focales y el
SHA-256 de las trazas completas que quedan dentro del proyecto.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]          # .../TM_TREE_AND_REFERENCE_ENGINE_V1
ROOT = Path(__file__).resolve().parents[3]          # .../Teoria Modular

# (origen relativo a BASE, nombre plano en la entrega)
FILES: list[tuple[str, str]] = [
    ("10_REPORTS/CHECKPOINT_8_DIRECT_AUT.md", "01_CHECKPOINT_8.md"),
    ("09_OPEN_RULES/OPEN_RULES_DIRECT_AUT_V1.md", "02_OPEN_RULES.md"),
    ("02_EXECUTABLE_TREE/TM_TREE_EXECUTABLE_DIRECT_AUT_V1.md", "03_TREE_EXECUTABLE.md"),
    ("03_TRANSITION_SPECS/TM_TREE_TRANSITIONS_DIRECT_AUT_V1.csv", "04_TRANSITIONS.csv"),
    ("04_CONCEPT_TESTS/CONCEPT_TEST_MATRIX_DIRECT_AUT_V1.csv", "05_TEST_MATRIX.csv"),
    ("04_CONCEPT_TESTS/ITERATION_08_TEST_RESULTS.json", "06_TEST_RESULTS_CONSOLIDATED.json"),
    ("04_CONCEPT_TESTS/CORE_TEST_RESULTS.csv", "07_CORE_TEST_RESULTS.csv"),
    ("04_CONCEPT_TESTS/AB_CANDIDATE_TEST_RESULTS.csv", "08_AB_BG_TEST_RESULTS.csv"),
    ("04_CONCEPT_TESTS/DIRECT_AUT_TEST_RESULTS.csv", "09_DIRECT_AUT_TEST_RESULTS.csv"),
    ("05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py", "10_INTERPRETER_DIRECT_AUT.py"),
    ("04_CONCEPT_TESTS/run_direct_aut_tests.py", "11_RUNNER_DIRECT_AUT.py"),
    ("04_CONCEPT_TESTS/run_iteration_08_replays.py", "12_RUNNER_REPLAYS.py"),
    ("07_REAL_REPLAYS/direct_aut_state_L1_1615_1618.json", "13_STATE_L1.json"),
    ("07_REAL_REPLAYS/direct_aut_events_L1_1615_1618.csv", "14_EVENTS_L1.csv"),
    ("07_REAL_REPLAYS/direct_aut_state_L2_1619_1622.json", "15_STATE_L2.json"),
    ("07_REAL_REPLAYS/direct_aut_events_L2_1619_1622.csv", "16_EVENTS_L2.csv"),
    ("08_TREE_PYTHON_COMPARISON/DIRECT_AUT_TREE_PYTHON_MATRIX_V1.csv", "17_TREE_PYTHON_MATRIX.csv"),
    ("05_REFERENCE_ENGINE/tm_reference_interpreter_v1_bg_aut.py", "18_EVIDENCE_INTERPRETER_BG_AUT.py"),
]

TRACES = [
    "07_REAL_REPLAYS/direct_aut_trace_L1_1615_1618.jsonl",
    "07_REAL_REPLAYS/direct_aut_trace_L2_1619_1622.jsonl",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    pkg_name = f"ITERACION_08_DIRECT_AUT_{ts}"
    pkg = ROOT / "TM_ENTREGAS_ITERACION" / pkg_name
    zip_path = ROOT / "TM_ITERATION_08_REVIEW.zip"
    if pkg.exists():
        raise SystemExit(f"ya existe: {pkg}")
    pkg.mkdir(parents=True)
    if zip_path.exists():
        zip_path.unlink()

    manifest: list[dict] = []
    for rel, flat in FILES:
        src = BASE / rel
        if not src.exists():
            raise SystemExit(f"falta el archivo fuente: {src}")
        dst = pkg / flat
        shutil.copy2(src, dst)
        manifest.append({
            "original_relative_path": rel,
            "package_name": flat,
            "size": dst.stat().st_size,
            "sha256": sha256(dst),
            "reason": "entregable esencial de la iteracion 08",
        })

    traces = []
    for rel in TRACES:
        src = BASE / rel
        if src.exists():
            traces.append({
                "original_relative_path": rel,
                "size": src.stat().st_size,
                "sha256": sha256(src),
                "note": "traza completa conservada en el proyecto; no incluida integra",
            })

    pkg_manifest = {
        "iteration_id": "ITERACION_08_DIRECT_AUT",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "engine": "TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT",
        "engine_version": "iteration 08",
        "objective": "retirar P-AB-04 (cuatro puntos) e implementar AUT directo por A",
        "files": manifest,
        "full_traces_referenced": traces,
        "originals_modified": False,
        "tree_modified": False,
        "official_engine_modified": False,
        "goldens_modified": False,
        "open_rule_blocks": ["C", "CUT", "TT", "FT", "gap new-1", "concurrency"],
        "gate": "GATE_AUT_DIRECT_BY_A_PASS",
        "status": "NOT_READY_TO_FREEZE_TREE / REFERENCE_ENGINE_INCOMPLETE",
    }
    (pkg / "PACKAGE_MANIFEST.json").write_text(
        json.dumps(pkg_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    sums = []
    for f in sorted(pkg.iterdir(), key=lambda p: p.name):
        sums.append(f"{sha256(f)}  {f.name}")
    (pkg / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(pkg.iterdir(), key=lambda p: p.name):
            zf.write(f, f"{pkg_name}/{f.name}")

    # Verificacion: reabrir, contar miembros y recomputar hashes.
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        bad = zf.testzip()
        if bad:
            raise SystemExit(f"ZIP corrupto en {bad}")
        inner = {}
        for n in names:
            inner[n] = hashlib.sha256(zf.read(n)).hexdigest()

    print(json.dumps({
        "package_dir": str(pkg),
        "zip_path": str(zip_path),
        "zip_size_bytes": zip_path.stat().st_size,
        "zip_sha256": sha256(zip_path),
        "members": len(names),
        "integrity": "PASS",
        "member_hashes": inner,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
