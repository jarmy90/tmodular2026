# -*- coding: utf-8 -*-
"""Builds the audit input manifest, external-evidence index and SHA256SUMS.

Read-only over the source files; writes only inside FREEBUFF_AUDIT_V219.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
PROJECT = AUDIT.parents[1]
DELIV = Path(r"C:\Users\profesor\OpenBot\Agents\agent-ece275c8-821a-43f3-b05f-6cdf123b7ade")
R5_DIR = DELIV / "deliverables_R5"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest().upper()


def row(path: Path, role: str, state: str = "READ_OK") -> dict:
    st = path.stat()
    return {
        "role": role,
        "absolute_path": str(path),
        "file_name": path.name,
        "size_bytes": st.st_size,
        "mtime_utc": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(),
        "sha256": sha256(path),
        "state": state,
    }


INPUTS = [
    (PROJECT / "TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md", "tree_working_canon", "WORKING_CANON_NOT_FROZEN"),
    (PROJECT / "TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_v2_19_CERTIFICADO.json", "tree_certificate", "WORKING_CANON_NOT_FROZEN"),
    (PROJECT / "TM_CANON_ACTIVO/03_LECTURAS_HUMANAS/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v005.txt", "human_readings_v005", "PARTIAL_A_TO_16_39_AND_D_PENDING_16_49_17_29"),
    (PROJECT / "TM_CANON_ACTIVO/02_TICKS/TM_TICKFEED_1615_1730.csv", "master_tickfeed", "VERIFIED_20335_TICKS"),
    (PROJECT / "TM_CANON_ACTIVO/04_MOTOR_PYTHON/CANDIDATO_v0752_R3/TM_CORE_PYTHON_v0752_CANONICAL_R3.py", "engine_R3_frozen", "FROZEN"),
    (R5_DIR / "python/TM_CORE_PYTHON_v0752_CANONICAL_R5.py", "engine_R5_audited", "BASELINE_PROVISIONAL_NOT_FROZEN"),
    (AUDIT / "00_INPUTS_REFERENCE/variants/R5_PACKAGED_19A847C0.py", "engine_R5_packaged", "PACKAGED_VARIANT_DO_NOT_SUBSTITUTE"),
    (DELIV / "TM_CORE_v0752_R5_LECTURA_1615_1629.zip", "R5_zip_lectura", "PACKAGED_ORIGINAL"),
    (DELIV / "TM_CORE_v0752_R5_POST_CUT.zip", "R5_zip_post_cut", "PACKAGED_ORIGINAL"),
    (PROJECT / "TM_ENTREGAS/TM_CORE_v0752_R3_B_AUT.zip", "R3_zip_frozen", "FROZEN"),
    (R5_DIR / "tests/test_big_b_aut.py", "test_big_b_aut", "UNMODIFIED"),
    (R5_DIR / "tests/test_anchor_gates.py", "test_anchor_gates", "UNMODIFIED"),
    (R5_DIR / "tests/test_post_cut_gates.py", "test_post_cut_gates", "UNMODIFIED"),
    (R5_DIR / "tests/test_transformations.py", "test_transformations", "UNMODIFIED"),
    (R5_DIR / "repro/compare_v005.py", "comparator_v005", "UNMODIFIED"),
    (R5_DIR / "repro/compare_golden.py", "comparator_golden", "UNMODIFIED"),
    (R5_DIR / "repro/run_all.py", "replay_run_all", "UNMODIFIED"),
    (R5_DIR / "manifest.json", "R5_package_manifest", "INCONSISTENT_WITH_DISK_ENGINE"),
]

EXTERNAL = [
    ("CE_TESTS_v219.md", "external_audit_evidence"),
    ("CE_OBSERVATION_RESULTS_v219.md", "external_audit_evidence"),
    ("CONCEPTUAL_MOVEMENT_ERRORS_v219.md", "external_audit_evidence"),
    ("NODE_MAP.csv", "external_audit_evidence"),
    ("INPUTS_MANIFEST.json", "external_audit_evidence"),
    ("RC_BOOTSTRAP_ONE_DESIGN_v219.md", "external_audit_evidence"),
]


def main():
    manifest = {
        "artifact": "FREEBUFF_INPUTS_MANIFEST_v219",
        "document_version": "1.0",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "workspace_root": str(PROJECT),
        "audit_root": str(AUDIT),
        "outside_workspace_reads": str(DELIV),
        "engine_analyzed": "R5 9BD1BEDB5DEC8C5A1C3A831338503E90CC04EE3CD776CF4E01D27CF8AA0EBEAE",
        "tree_analyzed": "94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17",
        "baseline_rule": "R5 audited variant is the provisional baseline because it is the engine cited by CE reports and INPUTS_MANIFEST; it is not declared official or frozen.",
        "tree_modified": False,
        "engine_modified": False,
        "goldens_modified": False,
        "tests_modified": False,
        "observational_only": True,
        "inputs": [row(p, r, s) for p, r, s in INPUTS],
        "third_party_evidence": [],
    }
    for name, role in EXTERNAL:
        p = AUDIT / "00_INPUTS_REFERENCE/external_audit_evidence" / name
        r = row(p, role, "EXTERNAL_AUDIT_EVIDENCE")
        r["original_path"] = str(R5_DIR / "audit_v219" / name)
        manifest["third_party_evidence"].append(r)

    (AUDIT / "FREEBUFF_INPUTS_MANIFEST_v219.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    with (HERE / "EXTERNAL_EVIDENCE_INDEX_v219.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "sha256", "size_bytes", "copied_from", "state"])
        for e in manifest["third_party_evidence"]:
            w.writerow([e["file_name"], e["sha256"], e["size_bytes"], e["original_path"], e["state"]])

    deliverables = [
        ("FREEBUFF_INPUTS_MANIFEST_v219.json", "input manifest"),
        ("01_INTEGRITY/R5_VARIANT_COMPARISON.md", "R5 variant comparison"),
        ("FREEBUFF_CE_REPRODUCTION_v219.md", "CE reproduction"),
        ("FREEBUFF_FIRST_DIVERGENCES_v219.csv", "first divergences"),
        ("FREEBUFF_CONCEPTUAL_ROOT_CAUSES_v219.md", "conceptual root causes"),
        ("FREEBUFF_RC1_MOVEMENT_ANALYSIS_v219.md", "RC-1 analysis"),
        ("FREEBUFF_RC2_GAP_ANALYSIS_v219.md", "RC-2 analysis"),
        ("FREEBUFF_ARCHITECTURE_CONCEPTS_v219.md", "architecture concepts"),
        ("FREEBUFF_COMPONENT_REUSE_MATRIX_v219.csv", "component reuse matrix"),
        ("FREEBUFF_EXPERT_QUESTIONS_v219.md", "expert questions"),
        ("FREEBUFF_TEST_GAPS_v219.md", "test gaps"),
        ("FREEBUFF_AUDIT_SUMMARY_v219.md", "audit summary"),
    ]
    meta = {
        "artifact": "FREEBUFF_DELIVERABLE_METADATA_v219",
        "document_version": "1.0",
        "source_tree": "TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md",
        "source_tree_sha256": "94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17",
        "engine_analyzed": "R5 9BD1BEDB5DEC8C5A1C3A831338503E90CC04EE3CD776CF4E01D27CF8AA0EBEAE",
        "engine_version": "0.7.5.2-R5",
        "tree_modified": False, "engine_modified": False, "goldens_modified": False,
        "observational_only": True,
        "deliverables": [],
    }
    for rel, role in deliverables:
        p = AUDIT / rel
        meta["deliverables"].append({
            "path": rel, "role": role, "size_bytes": p.stat().st_size, "sha256": sha256(p),
            "document_version": "1.0", "engine": meta["engine_analyzed"],
            "tree_modified": False, "engine_modified": False, "goldens_modified": False,
            "observational_only": True,
        })
    (HERE / "DELIVERABLE_METADATA_v219.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    # SHA256SUMS over every produced artifact, excluding itself.
    lines = []
    for p in sorted(AUDIT.rglob("*")):
        if p.is_file() and p.name != "SHA256SUMS.txt":
            lines.append(f"{sha256(p)}  {p.relative_to(AUDIT).as_posix()}")
    (AUDIT / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"manifest: {len(manifest['inputs'])} inputs, {len(manifest['third_party_evidence'])} evidence files")
    print(f"sha256sums: {len(lines)} entries")


if __name__ == "__main__":
    main()
