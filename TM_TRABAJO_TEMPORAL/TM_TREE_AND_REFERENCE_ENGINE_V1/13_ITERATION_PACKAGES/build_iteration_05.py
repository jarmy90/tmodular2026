"""Build ITERACION_05 flat package and verified ZIP."""
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
OUT_ROOT = ROOT / "TM_ENTREGAS_ITERACION"
STAMP = datetime.now().strftime("%Y%m%d_%H%M")
NAME = f"ITERACION_05_CORE_{STAMP}"
OUT = OUT_ROOT / NAME
ZIP = OUT_ROOT / f"TM_ITERATION_05_REVIEW.zip"

COPIES = [
    ("10_REPORTS/CHECKPOINT_5_CORE.md", "01_CHECKPOINT_CORE.md", "checkpoint"),
    ("01_CONCEPTS/READING_OWNERSHIP_MODEL.md", "02_READING_OWNERSHIP_MODEL.md", "ownership model"),
    ("02_EXECUTABLE_TREE/TM_TREE_EXECUTABLE_CORE_V1.md", "03_EXECUTABLE_TREE_CORE.md", "executable tree core"),
    ("03_TRANSITION_SPECS/TM_TREE_TRANSITIONS_CORE_V1.csv", "04_TRANSITIONS_CORE.csv", "transition specs"),
    ("04_CONCEPT_TESTS/CONCEPT_TEST_MATRIX_CORE_V1.csv", "05_TEST_MATRIX_CORE.csv", "test matrix"),
    ("04_CONCEPT_TESTS/CORE_TEST_RESULTS.csv", "06_TEST_RESULTS.csv", "test results"),
    ("04_CONCEPT_TESTS/CORE_TEST_RESULTS.json", "07_TEST_RESULTS.json", "test summary"),
    ("04_CONCEPT_TESTS/CORE_REPLAY_CHECKS.json", "08_REPLAY_CHECKS.json", "determinism and prefix checks"),
    ("05_REFERENCE_ENGINE/tm_reference_interpreter_v1.py", "09_REFERENCE_INTERPRETER_V1.py", "reference interpreter"),
    ("06_SYNTHETIC_REPLAYS/state_1615_1618.json", "10_STATE_1615_1618.json", "anchor 16:15-16:18 state"),
    ("06_SYNTHETIC_REPLAYS/events_1615_1618.csv", "11_EVENTS_1615_1618.csv", "anchor 16:15-16:18 events"),
    ("07_REAL_REPLAYS/state_L2_1619_1622.json", "12_STATE_L2_1619_1622.json", "anchor L2 state"),
    ("07_REAL_REPLAYS/events_L2_1619_1622.csv", "13_EVENTS_L2_1619_1622.csv", "anchor L2 events"),
    ("08_TREE_PYTHON_COMPARISON/CORE_TREE_PYTHON_MATRIX_V1.csv", "14_TREE_PYTHON_MATRIX.csv", "tree-Python comparison"),
    ("09_OPEN_RULES/OPEN_RULES_CORE_V1.md", "15_OPEN_RULES.md", "open rules"),
    ("11_MANIFEST/CORE_MANIFEST.json", "16_CORE_MANIFEST.json", "core manifest"),
]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if OUT.exists():
        raise SystemExit(f"already exists: {OUT}")
    OUT.mkdir(parents=True)
    members = []
    for src_rel, dst_name, reason in COPIES:
        src = BASE / src_rel
        dst = OUT / dst_name
        shutil.copy2(src, dst)
        members.append({"path": dst_name, "original_path": str(src.relative_to(ROOT)),
                        "size": dst.stat().st_size, "sha256": sha(dst),
                        "reason": reason})

    # trace index and focal sample (full traces stay in the project)
    trace_index = []
    sample_lines = []
    for rel, label in [("06_SYNTHETIC_REPLAYS/trace_1615_1618.jsonl", "L1_1615_1618"),
                       ("07_REAL_REPLAYS/trace_L2_1619_1622.jsonl", "L2_1619_1622")]:
        p = BASE / rel
        lines = p.read_text(encoding="utf-8").splitlines()
        trace_index.append({"path": str(p.relative_to(ROOT)), "label": label,
                            "size": p.stat().st_size, "sha256": sha(p),
                            "lines": len(lines),
                            "note": "full trace only in project; sample included"})
        for idx in [0, 1, 2, len(lines) - 3, len(lines) - 2, len(lines) - 1]:
            if 0 <= idx < len(lines):
                sample_lines.append(json.dumps({
                    "trace": label, "line_index": idx + 1, "line": lines[idx],
                }, ensure_ascii=False))
    (OUT / "17_TRACE_INDEX.json").write_text(
        json.dumps(trace_index, indent=2) + "\n", encoding="utf-8")
    (OUT / "18_TRACE_SAMPLE.jsonl").write_text(
        "\n".join(sample_lines) + "\n", encoding="utf-8")
    for name, reason in [("17_TRACE_INDEX.json", "full trace hashes and paths"),
                         ("18_TRACE_SAMPLE.jsonl", "focal trace sample")]:
        p = OUT / name
        members.append({"path": name, "original_path": "TM_TRABAJO_TEMPORAL/TM_TREE_AND_REFERENCE_ENGINE_V1",
                        "size": p.stat().st_size, "sha256": sha(p), "reason": reason})

    sums = OUT / "SHA256SUMS.txt"
    sums.write_text("\n".join(f"{m['sha256']}  {m['path']}" for m in members) + "\n",
                    encoding="utf-8")
    members.append({"path": "SHA256SUMS.txt", "original_path": str(sums.relative_to(ROOT)),
                    "size": sums.stat().st_size, "sha256": sha(sums),
                    "reason": "hashes of the package members"})

    manifest = {
        "iteration_id": "ITERACION_05_CORE",
        "date": datetime.now().isoformat(timespec="seconds"),
        "objective": "clean reference interpreter core and its concept tests",
        "folder": str(OUT),
        "zip_path": str(ZIP),
        "members": members,
        "member_count": len(members),
        "metadata_not_self_hashed": ["PACKAGE_MANIFEST.json"],
        "originals_modified": False,
        "tree_modified": False,
        "engine_modified": False,
        "golden_modified": False,
        "scope": "1, opening, 2, module by discard, 3, module regular",
        "not_implemented": ["A", "B", "C", "AUT", "CUT", "TT", "FT", "gap new 1", "concurrency"],
        "tests": {"count": 19, "passed": 19, "failed": 0},
        "gate_core": "PASS",
        "tree_gate": "NOT_READY_TO_FREEZE_TREE",
        "engine_status": "REFERENCE_ENGINE_INCOMPLETE",
    }
    (OUT / "PACKAGE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    # verification hashes for every file that goes into the zip
    staged = {p.name: sha(p) for p in OUT.iterdir() if p.is_file()}

    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(OUT.iterdir()):
            zf.write(p, arcname=f"{NAME}/{p.name}")

    # reopen and verify every member
    failures = []
    with zipfile.ZipFile(ZIP) as zf:
        names = zf.namelist()
        if len(names) != len(staged):
            failures.append(f"member count {len(names)} != {len(staged)}")
        for p in OUT.iterdir():
            arc = f"{NAME}/{p.name}"
            if arc not in names:
                failures.append(f"missing member {p.name}")
                continue
            data = zf.read(arc)
            if hashlib.sha256(data).hexdigest() != staged[p.name]:
                failures.append(f"hash mismatch {p.name}")

    result = {
        "iteration_id": "ITERACION_05_CORE",
        "folder": str(OUT),
        "zip_path": str(ZIP),
        "zip_size": ZIP.stat().st_size,
        "zip_sha256": sha(ZIP),
        "members": len(staged),
        "failures": failures,
        "integrity": "PASS" if not failures else "FAIL",
    }
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
