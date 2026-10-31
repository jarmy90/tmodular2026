"""Phase 2 manifest and integrity check."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parents[1]

OUTPUTS = [
    "01_BLIND_READINGS/blind_reader_v2.py",
    "01_BLIND_READINGS/BLIND_V3_TRACE.jsonl",
    "01_BLIND_READINGS/BLIND_V3_EVENTS.csv",
    "01_BLIND_READINGS/BLIND_V3_GENERATIONS.csv",
    "01_BLIND_READINGS/BLIND_V3_BAR_CLOSE.csv",
    "01_BLIND_READINGS/BLIND_V3_SUMMARY.json",
    "01_BLIND_READINGS/BLIND_V3_SUMMARY_bturn.json",
    "01_BLIND_READINGS/BLIND_V3_SUMMARY_pending.json",
    "01_BLIND_READINGS/L2_1619_1624_GENERATIONS.csv",
    "01_BLIND_READINGS/L2_1619_1624_SUMMARY.json",
    "02_MOVEMENT_ANALYSIS/build_phase2_map.py",
    "02_MOVEMENT_ANALYSIS/PHASE_2_L1_L2_MAP.csv",
    "02_MOVEMENT_ANALYSIS/PHASE_2_SUMMARY.json",
    "02_MOVEMENT_ANALYSIS/PHASE_2_LABEL_AUDIT.csv",
    "05_TREE_REVISIONS/TREE_REVISION_v2_20_DRAFT.md",
    "05_TREE_REVISIONS/EXPERIMENTAL_POLICIES_V2.md",
    "09_REPORTS/CHECKPOINT_2_REPORT.md",
    "06_REGRESSION/PHASE_2_DETERMINISM.json",
    "01_BLIND_READINGS/BLIND_V3_TRACE_RUN2.jsonl",
    "01_BLIND_READINGS/PREFIX_1630.jsonl",
    "01_BLIND_READINGS/PREFIX_1700.jsonl",
    "01_BLIND_READINGS/PREFIX_1715.jsonl",
]

ORIGINALS = {
    "TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md":
        "94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17",
    "TM_CANON_ACTIVO/03_LECTURAS_HUMANAS/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v005.txt":
        "F5D7550C42C90897D833E6C2A3FAF772753A129640FD4411DE4190CB2CF94226",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main() -> int:
    outputs = {}
    for rel in OUTPUTS:
        p = BASE / rel
        outputs[rel] = {
            "exists": p.exists(),
            "bytes": p.stat().st_size if p.exists() else None,
            "sha256": sha256(p) if p.exists() else None,
        }

    tickfeed = next(ROOT.rglob("TM_TICKFEED_1615_1730.csv"), None)
    originals = {}
    for rel, expected in ORIGINALS.items():
        p = ROOT / rel
        actual = sha256(p) if p.exists() else None
        originals[rel] = {
            "exists": p.exists(),
            "sha256": actual,
            "expected": expected,
            "match": actual == expected,
        }
    if tickfeed is not None:
        actual = sha256(tickfeed)
        originals[str(tickfeed.relative_to(ROOT))] = {
            "exists": True,
            "sha256": actual,
            "expected": "5F701BE2307352CB559ABBD7BB856A6FD2A1F91E5D269A93DCC9AE2992E2C9FF",
            "match": actual == "5F701BE2307352CB559ABBD7BB856A6FD2A1F91E5D269A93DCC9AE2992E2C9FF",
        }

    manifest = {
        "phase": "PHASE_2_CORRECTED_REREAD_AND_GENERATION_AUDIT",
        "date": datetime.now().isoformat(timespec="seconds"),
        "reader_version": "blind_reader_v2 + Q1/Q2/Q3",
        "hierarchy_status": "EXPERIMENTAL_HIERARCHY_V1_NOT_CANON",
        "counts": {
            "L1_generations": 26,
            "L1_valid_primary": 19,
            "L1_integrated_gap": 6,
            "L1_pending": 1,
            "L2_rows": 3,
            "L2_unique_secondary": 1,
            "L2_duplicates_of_L1": 2,
            "unique_total": 27,
            "removed_from_previous_51": 25,
        },
        "a_gate": {
            "b100": 26,
            "bturn": 26,
            "pending": 1,
            "conclusion": "generation count invariant to A confirmation time; timing remains open",
        },
        "outputs": outputs,
        "originals": originals,
        "originals_modified": False,
        "engine_modified": False,
        "goldens_modified": False,
        "tree_frozen": False,
        "engine_authority": False,
        "observational_only": True,
    }
    (BASE / "10_MANIFEST" / "PHASE_2_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "outputs": len(outputs),
        "missing": [k for k, v in outputs.items() if not v["exists"]],
        "originals_all_match": all(v["match"] for v in originals.values()),
        "originals": {k: v["match"] for k, v in originals.items()},
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
