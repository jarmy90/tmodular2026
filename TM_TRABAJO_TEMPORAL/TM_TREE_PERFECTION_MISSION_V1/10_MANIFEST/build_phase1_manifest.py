#!/usr/bin/env python3
"""Build the Phase 1 manifest for TM_TREE_PERFECTION_MISSION_V1."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "10_MANIFEST"

FILES = [
    ("reader_v2", "01_BLIND_READINGS/blind_reader_v2.py"),
    ("trace_b100", "01_BLIND_READINGS/BLIND_V2_TRACE.jsonl"),
    ("events_b100", "01_BLIND_READINGS/BLIND_V2_EVENTS.csv"),
    ("generations_b100", "01_BLIND_READINGS/BLIND_V2_GENERATIONS.csv"),
    ("bar_close_b100", "01_BLIND_READINGS/BLIND_V2_BAR_CLOSE.csv"),
    ("summary_b100", "01_BLIND_READINGS/BLIND_V2_SUMMARY.json"),
    ("trace_pending", "01_BLIND_READINGS/BLIND_V2_TRACE_pending.jsonl"),
    ("events_pending", "01_BLIND_READINGS/BLIND_V2_EVENTS_pending.csv"),
    ("generations_pending", "01_BLIND_READINGS/BLIND_V2_GENERATIONS_pending.csv"),
    ("summary_pending", "01_BLIND_READINGS/BLIND_V2_SUMMARY_pending.json"),
    ("trace_bturn", "01_BLIND_READINGS/BLIND_V2_TRACE_bturn.jsonl"),
    ("events_bturn", "01_BLIND_READINGS/BLIND_V2_EVENTS_bturn.csv"),
    ("generations_bturn", "01_BLIND_READINGS/BLIND_V2_GENERATIONS_bturn.csv"),
    ("summary_bturn", "01_BLIND_READINGS/BLIND_V2_SUMMARY_bturn.json"),
    ("first_divergences", "02_MOVEMENT_ANALYSIS/PHASE_1_FIRST_DIVERGENCES.csv"),
    ("tree_contradictions", "03_CONCEPTUAL_GAPS/TREE_CONTRADICTIONS.csv"),
    ("expert_questions", "04_EXPERT_QUESTIONS/PHASE_1_EXPERT_QUESTIONS.md"),
    ("revision_r1", "05_TREE_REVISIONS/PROPOSED_REVISION_R1_A_FUNCTIONAL.md"),
    ("prefix_check", "06_REGRESSION/PREFIX_CHECK_V2.json"),
    ("checkpoint_1", "09_REPORTS/CHECKPOINT_1_REPORT.md"),
    ("checkpoint_0", "09_REPORTS/CHECKPOINT_0_MANDATE_RECEPTION.md"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    inputs = json.loads((OUT / "INPUTS_MANIFEST.json").read_text(encoding="utf-8"))
    summary = json.loads(
        (BASE / "01_BLIND_READINGS/BLIND_V2_SUMMARY.json").read_text(encoding="utf-8")
    )
    prefix = json.loads(
        (BASE / "06_REGRESSION/PREFIX_CHECK_V2.json").read_text(encoding="utf-8")
    )
    rows = []
    for key, rel in FILES:
        p = BASE / rel
        rows.append({
            "key": key,
            "path": rel,
            "exists": p.is_file(),
            "size_bytes": p.stat().st_size if p.is_file() else None,
            "sha256": sha256(p) if p.is_file() else None,
        })
    payload = {
        "mission": "TM_TREE_PERFECTION_MISSION_V1",
        "phase": "PHASE_1_BLIND_READING",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "NOT_READY_TO_FREEZE",
        "gate": "NEEDS_EXPERT_DECISION",
        "recommendation": "NOT_READY_TO_FREEZE",
        "originals_modified": False,
        "tree_modified": False,
        "engine_modified": False,
        "goldens_modified": False,
        "observational_only": True,
        "tree_status": "WORKING_CANON_NOT_FROZEN",
        "inputs": inputs["inputs"],
        "all_expected_hashes_match": inputs["all_expected_hashes_match"],
        "reader": {
            "file": "01_BLIND_READINGS/blind_reader_v2.py",
            "a_modes": ["b100", "pending", "bturn"],
            "ticks": summary["ticks"],
            "generations_b100": summary["generations"],
            "end_reasons_b100": summary["end_reasons"],
            "trace_sha256_b100": summary["trace_sha256"],
            "double_run_identical": True,
            "all_prefixes_pass": prefix["all_prefixes_pass"],
        },
        "prefix_check": prefix,
        "expert_questions": ["Q1_concurrencia_L1_L2", "Q2_vida_2_3",
                             "Q3_B_AUT_base_modulo"],
        "outputs": rows,
    }
    (OUT / "PHASE_1_MANIFEST.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    sums = "".join(
        f"{r['sha256']} *{r['path']}\n" for r in rows if r["sha256"]
    )
    with (OUT / "SHA256SUMS_PHASE_1.txt").open(
        "w", encoding="utf-8", newline="\n"
    ) as fh:
        fh.write(sums)
    print(json.dumps({
        "status": payload["status"],
        "gate": payload["gate"],
        "generations": payload["reader"]["generations_b100"],
        "trace": payload["reader"]["trace_sha256_b100"],
        "prefixes": payload["reader"]["all_prefixes_pass"],
        "outputs": len(rows),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
