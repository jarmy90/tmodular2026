"""Build manifest for ITERACION_07 B Grande/AUT."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]

INPUTS = {
    "tree": ("TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md",
             "94a1408a6123ed66948988334e7d540c2a2692c36eea3cb736dbff0da2346b17"),
    "tickfeed": ("TM_CANON_ACTIVO/02_TICKS/TM_TICKFEED_1615_1730.csv",
                 "5f701be2307352cb559abbd7bb856a6fd2a1f91e5d269a93dcc9ae2992e2c9ff"),
    "human_readings": ("TM_CANON_ACTIVO/03_LECTURAS_HUMANAS/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v005.txt",
                       "f5d7550c42c90897d833e6c2a3faf772753a129640fd4411de4190cb2cf94226"),
}

FILES = [
    "01_CONCEPTS/READING_OWNERSHIP_MODEL.md",
    "02_EXECUTABLE_TREE/TM_TREE_EXECUTABLE_AB_CANDIDATE_V1.md",
    "02_EXECUTABLE_TREE/TM_TREE_EXECUTABLE_B_GRANDE_AUT_V1.md",
    "03_TRANSITION_SPECS/TM_TREE_TRANSITIONS_AB_CANDIDATE_V1.csv",
    "03_TRANSITION_SPECS/TM_TREE_TRANSITIONS_B_GRANDE_AUT_V1.csv",
    "04_CONCEPT_TESTS/CONCEPT_TEST_MATRIX_B_GRANDE_AUT_V1.csv",
    "04_CONCEPT_TESTS/T001_CORRECTION.md",
    "04_CONCEPT_TESTS/CORE_TEST_RESULTS.csv",
    "04_CONCEPT_TESTS/CORE_TEST_RESULTS.json",
    "04_CONCEPT_TESTS/CORE_REPLAY_CHECKS.json",
    "04_CONCEPT_TESTS/AB_CANDIDATE_TEST_RESULTS.csv",
    "04_CONCEPT_TESTS/AB_CANDIDATE_TEST_RESULTS.json",
    "04_CONCEPT_TESTS/run_core_tests.py",
    "04_CONCEPT_TESTS/run_core_replay_checks.py",
    "04_CONCEPT_TESTS/run_ab_candidate_tests.py",
    "05_REFERENCE_ENGINE/tm_reference_interpreter_v1.py",
    "05_REFERENCE_ENGINE/tm_reference_interpreter_v1_ab_candidate.py",
    "05_REFERENCE_ENGINE/tm_reference_interpreter_v1_bg_aut.py",
    "06_SYNTHETIC_REPLAYS/bg_state_1615_1618.json",
    "06_SYNTHETIC_REPLAYS/bg_events_1615_1618.csv",
    "06_SYNTHETIC_REPLAYS/bg_trace_1615_1618.jsonl",
    "07_REAL_REPLAYS/bg_state_L2_1619_1622.json",
    "07_REAL_REPLAYS/bg_events_L2_1619_1622.csv",
    "07_REAL_REPLAYS/bg_trace_L2_1619_1622.jsonl",
    "08_TREE_PYTHON_COMPARISON/BG_TREE_PYTHON_MATRIX_V1.csv",
    "09_OPEN_RULES/OPEN_RULES_B_GRANDE_AUT_V1.md",
    "10_REPORTS/CHECKPOINT_6_AB_CANDIDATE.md",
    "10_REPORTS/CHECKPOINT_7_B_GRANDE_AUT.md",
]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    inputs = {}
    ok = True
    for key, (rel, expected) in INPUTS.items():
        p = ROOT / rel
        actual = sha(p)
        match = actual == expected
        ok = ok and match
        inputs[key] = {"path": rel, "sha256": actual, "expected": expected,
                       "match": match, "size": p.stat().st_size}

    files = []
    for rel in FILES:
        p = BASE / rel
        if not p.exists():
            raise SystemExit(f"missing: {p}")
        files.append({"path": rel, "size": p.stat().st_size, "sha256": sha(p)})

    manifest = {
        "iteration": "ITERACION_07_B_GRANDE_AUT",
        "workspace": str(BASE),
        "objective": "B Grande, AUT and new one on the approved A/B reader",
        "inputs": inputs,
        "originals_modified": not ok,
        "tree_modified": False,
        "engine_modified": False,
        "golden_modified": False,
        "scope": {
            "implemented": ["core", "A", "return", "B_CANDIDATE", "B_GRANDE",
                            "AUT by B", "NEW_ONE_ACTIVE", "authority archival"],
            "not_implemented": ["C", "CUT", "TT", "FT", "new one by direct AUT",
                                "gap new one", "concurrency"],
        },
        "tests": {"core": {"count": 19, "passed": 19, "failed": 0},
                  "a_bg_aut": {"count": 32, "passed": 32, "failed": 0},
                  "total": 51},
        "anchors": {
            "L1": {"module": 2850, "A": 910, "B_grande": 910,
                   "B_grande_time": "16:18:34.125",
                   "AUT_time": "16:18:34.926",
                   "B_aut": 1230, "new_one_origin": 2985760,
                   "new_one_structural_time": "16:17:05.425",
                   "new_one_knowledge_time": "16:18:34.926",
                   "new_one_extension": 2984300},
            "L2": {"one": 750, "two": 1230, "three": 2983030,
                   "module": 1970, "A": 2050,
                   "direct_aut_flag": True},
        },
        "gate_core": "PASS",
        "gate_bg_aut": "GATE_B_GRANDE_AUT_PASS",
        "tree_gate": "NOT_READY_TO_FREEZE_TREE",
        "engine_status": "REFERENCE_ENGINE_INCOMPLETE",
        "files": files,
    }
    out = BASE / "11_MANIFEST" / "BG_AUT_MANIFEST.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    sums = BASE / "11_MANIFEST" / "SHA256SUMS_BG.txt"
    lines = [f"{f['sha256']}  {f['path']}" for f in files]
    lines += [f"{v['sha256']}  {v['path']}" for v in inputs.values()]
    sums.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "inputs_ok": ok, "files": len(files),
        "core_reader": next(f["sha256"] for f in files
                            if f["path"].endswith("tm_reference_interpreter_v1.py")),
        "ab_reader": next(f["sha256"] for f in files
                          if f["path"].endswith("ab_candidate.py")),
        "bg_reader": next(f["sha256"] for f in files
                          if f["path"].endswith("bg_aut.py")),
        "manifest": str(out)}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
