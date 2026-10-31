#!/usr/bin/env python3
"""ITERACION 09 — empaquetado plano + ZIP verificado (<=25 miembros)."""
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
    ("10_REPORTS/CHECKPOINT_9_C_GRANDE.md", "01_CHECKPOINT_9.md"),
    ("09_OPEN_RULES/OPEN_RULES_C_GRANDE_V1.md", "02_OPEN_RULES.md"),
    ("02_EXECUTABLE_TREE/TM_TREE_EXECUTABLE_C_GRANDE_V1.md", "03_TREE_EXECUTABLE.md"),
    ("03_TRANSITION_SPECS/TM_TREE_TRANSITIONS_C_GRANDE_V1.csv", "04_TRANSITIONS_C.csv"),
    ("04_CONCEPT_TESTS/C_TEST_RESULTS.csv", "05_TEST_RESULTS_C.csv"),
    ("04_CONCEPT_TESTS/ITERATION_09_TEST_RESULTS.json", "06_TEST_RESULTS.json"),
    ("04_CONCEPT_TESTS/DIRECT_AUT_TEST_RESULTS.csv", "07_TEST_RESULTS_AD.csv"),
    ("04_CONCEPT_TESTS/AB_CANDIDATE_TEST_RESULTS.csv", "08_TEST_RESULTS_AB_BG.csv"),
    ("04_CONCEPT_TESTS/CORE_TEST_RESULTS.csv", "09_TEST_RESULTS_CORE.csv"),
    ("05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py", "10_INTERPRETER.py"),
    ("04_CONCEPT_TESTS/run_iteration_09_tests.py", "11_RUNNER_TESTS.py"),
    ("04_CONCEPT_TESTS/run_iteration_08_replays.py", "12_RUNNER_REPLAYS.py"),
    ("07_REAL_REPLAYS/direct_aut_state_L1_1615_1618.json", "13_STATE_L1.json"),
    ("07_REAL_REPLAYS/direct_aut_events_L1_1615_1618.csv", "14_EVENTS_L1.csv"),
    ("07_REAL_REPLAYS/direct_aut_state_L2_1619_1622.json", "15_STATE_L2.json"),
    ("07_REAL_REPLAYS/direct_aut_events_L2_1619_1622.csv", "16_EVENTS_L2.csv"),
    ("08_TREE_PYTHON_COMPARISON/C_GRANDE_TREE_PYTHON_MATRIX_V1.csv", "17_MATRIX_C.csv"),
    ("05_REFERENCE_ENGINE/tm_reference_interpreter_v1_bg_aut.py", "18_EVIDENCE_BASELINE_PREV.py"),
]

TRACES = ["07_REAL_REPLAYS/direct_aut_trace_L1_1615_1618.jsonl",
          "07_REAL_REPLAYS/direct_aut_trace_L2_1619_1622.jsonl"]


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main() -> int:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    name = f"ITERACION_09_C_GRANDE_{ts}"
    pkg = ROOT / "TM_ENTREGAS_ITERACION" / name
    zip_path = ROOT / "TM_ITERATION_09_REVIEW.zip"
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

    traces = [{"original": t, "size": (BASE / t).stat().st_size,
               "sha256": sha(BASE / t),
               "note": "traza completa en el proyecto; no incluida integra"}
              for t in TRACES if (BASE / t).exists()]

    manifest = {
        "iteration_id": "ITERACION_09_C_GRANDE",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "engine": "TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT (revision 09)",
        "objective": "endurecer baseline (AUT directo exige A_CONFIRMED) e "
                     "implementar C Grande y C usada como tendencia",
        "files": files,
        "full_traces_referenced": traces,
        "gate": "GATE_C_GRANDE_TREND_PASS",
        "tests": {"total": 82, "passed": 82,
                  "canonical": 23, "provisional": 58, "open_rule_block": 1},
        "open_rule_blocks": ["CUT", "FT", "gap new-1", "concurrency",
                             "AUT direct with A pending"],
        "originals_modified": False,
        "tree_modified": False,
        "official_engine_modified": False,
        "goldens_modified": False,
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
        members = len(names)
        inner = {n: hashlib.sha256(zf.read(n)).hexdigest() for n in names}
    if members > 25:
        raise SystemExit(f"demasiados miembros: {members}")

    print(json.dumps({
        "package_dir": str(pkg), "zip_path": str(zip_path),
        "zip_size_bytes": zip_path.stat().st_size,
        "zip_sha256": sha(zip_path), "members": members,
        "integrity": "PASS", "member_hashes": inner,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
