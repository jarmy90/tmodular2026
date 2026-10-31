"""Build ITERACION_06 A/B candidate flat package and verified ZIP."""
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
NAME = f"ITERACION_06_AB_CANDIDATE_{STAMP}"
OUT = OUT_ROOT / NAME
ZIP = OUT_ROOT / "TM_ITERATION_06_REVIEW.zip"

COPIES = [
    ("10_REPORTS/CHECKPOINT_6_AB_CANDIDATE.md", "01_CHECKPOINT_AB_CANDIDATE.md", "checkpoint"),
    ("02_EXECUTABLE_TREE/TM_TREE_EXECUTABLE_AB_CANDIDATE_V1.md", "02_EXECUTABLE_TREE_AB.md", "A/B executable tree"),
    ("03_TRANSITION_SPECS/TM_TREE_TRANSITIONS_AB_CANDIDATE_V1.csv", "03_TRANSITIONS_AB.csv", "A/B transition specs"),
    ("04_CONCEPT_TESTS/CONCEPT_TEST_MATRIX_AB_CANDIDATE_V1.csv", "04_TEST_MATRIX_AB.csv", "A/B test matrix"),
    ("04_CONCEPT_TESTS/AB_CANDIDATE_TEST_RESULTS.csv", "05_AB_TEST_RESULTS.csv", "A/B test results"),
    ("04_CONCEPT_TESTS/AB_CANDIDATE_TEST_RESULTS.json", "06_AB_TEST_SUMMARY.json", "A/B summary"),
    ("04_CONCEPT_TESTS/CORE_TEST_RESULTS.csv", "07_CORE_TEST_RESULTS.csv", "core baseline 19/19"),
    ("04_CONCEPT_TESTS/CORE_TEST_RESULTS.json", "08_CORE_TEST_SUMMARY.json", "core summary"),
    ("04_CONCEPT_TESTS/CORE_REPLAY_CHECKS.json", "09_CORE_REPLAY_CHECKS.json", "core replay checks"),
    ("05_REFERENCE_ENGINE/tm_reference_interpreter_v1_ab_candidate.py", "10_REFERENCE_INTERPRETER_AB.py", "A/B reference interpreter"),
    ("05_REFERENCE_ENGINE/tm_reference_interpreter_v1.py", "11_REFERENCE_INTERPRETER_CORE.py", "approved core baseline"),
    ("06_SYNTHETIC_REPLAYS/ab_state_1615_1618.json", "12_STATE_L1_1615_1618.json", "L1 A/B state"),
    ("06_SYNTHETIC_REPLAYS/ab_events_1615_1618.csv", "13_EVENTS_L1_1615_1618.csv", "L1 A/B events"),
    ("07_REAL_REPLAYS/ab_state_L2_1619_1622.json", "14_STATE_L2_1619_1622.json", "L2 A/B state"),
    ("07_REAL_REPLAYS/ab_events_L2_1619_1622.csv", "15_EVENTS_L2_1619_1622.csv", "L2 A/B events"),
    ("08_TREE_PYTHON_COMPARISON/AB_TREE_PYTHON_MATRIX_V1.csv", "16_TREE_PYTHON_MATRIX_AB.csv", "tree-Python comparison"),
    ("09_OPEN_RULES/OPEN_RULES_AB_CANDIDATE_V1.md", "17_OPEN_RULES_AB.md", "open rules"),
    ("11_MANIFEST/AB_CANDIDATE_MANIFEST.json", "18_AB_CANDIDATE_MANIFEST.json", "manifest"),
]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if OUT.exists() or ZIP.exists():
        raise SystemExit(f"already exists: {OUT} or {ZIP}")
    OUT.mkdir(parents=True)
    members = []
    for src_rel, dst_name, reason in COPIES:
        src = BASE / src_rel
        dst = OUT / dst_name
        shutil.copy2(src, dst)
        members.append({"path": dst_name, "original_path": str(src.relative_to(ROOT)),
                        "size": dst.stat().st_size, "sha256": sha(dst),
                        "reason": reason})

    trace_index = []
    sample_lines = []
    for rel, label in [("06_SYNTHETIC_REPLAYS/ab_trace_1615_1618.jsonl", "L1_AB_1615_1618"),
                       ("07_REAL_REPLAYS/ab_trace_L2_1619_1622.jsonl", "L2_AB_1619_1622")]:
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
    (OUT / "19_TRACE_INDEX.json").write_text(
        json.dumps(trace_index, indent=2) + "\n", encoding="utf-8")
    (OUT / "20_TRACE_SAMPLE.jsonl").write_text(
        "\n".join(sample_lines) + "\n", encoding="utf-8")
    for name, reason in [("19_TRACE_INDEX.json", "full trace hashes and paths"),
                         ("20_TRACE_SAMPLE.jsonl", "focal trace sample")]:
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
        "iteration_id": "ITERACION_06_AB_CANDIDATE",
        "date": datetime.now().isoformat(timespec="seconds"),
        "objective": "A, return and B candidate on the approved core",
        "folder": str(OUT),
        "zip_path": str(ZIP),
        "members": members,
        "member_count": len(members),
        "metadata_not_self_hashed": ["PACKAGE_MANIFEST.json"],
        "originals_modified": False,
        "tree_modified": False,
        "engine_modified": False,
        "golden_modified": False,
        "tests": {"core": 19, "ab_candidate": 14, "total": 33, "failed": 0},
        "anchors": {
            "L1": {"module": 2850, "A": 910, "B_origin": 2985760},
            "L2": {"one": 750, "two": 1230, "three": 2983030, "module": 1970, "A": 2050},
        },
        "gate_core": "PASS",
        "gate_ab_candidate": "GATE_A_B_CANDIDATE_PASS",
        "tree_gate": "NOT_READY_TO_FREEZE_TREE",
        "engine_status": "REFERENCE_ENGINE_INCOMPLETE",
    }
    (OUT / "PACKAGE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    staged = {p.name: sha(p) for p in OUT.iterdir() if p.is_file()}
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(OUT.iterdir()):
            zf.write(p, arcname=f"{NAME}/{p.name}")

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
            if hashlib.sha256(zf.read(arc)).hexdigest() != staged[p.name]:
                failures.append(f"hash mismatch {p.name}")

    result = {"iteration_id": "ITERACION_06_AB_CANDIDATE",
              "folder": str(OUT), "zip_path": str(ZIP),
              "zip_size": ZIP.stat().st_size, "zip_sha256": sha(ZIP),
              "members": len(staged), "failures": failures,
              "integrity": "PASS" if not failures else "FAIL"}
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
