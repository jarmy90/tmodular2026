"""Build manifest for ITERACION_06 A/B candidate."""
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
    "02_EXECUTABLE_TREE/TM_TREE_EXECUTABLE_CORE_V1.md",
    "02_EXECUTABLE_TREE/TM_TREE_EXECUTABLE_AB_CANDIDATE_V1.md",
    "03_TRANSITION_SPECS/TM_TREE_TRANSITIONS_CORE_V1.csv",
    "03_TRANSITION_SPECS/TM_TREE_TRANSITIONS_AB_CANDIDATE_V1.csv",
    "04_CONCEPT_TESTS/CONCEPT_TEST_MATRIX_CORE_V1.csv",
    "04_CONCEPT_TESTS/CONCEPT_TEST_MATRIX_AB_CANDIDATE_V1.csv",
    "04_CONCEPT_TESTS/CORE_TEST_RESULTS.csv",
    "04_CONCEPT_TESTS/CORE_TEST_RESULTS.json",
    "04_CONCEPT_TESTS/CORE_REPLAY_CHECKS.json",
    "04_CONCEPT_TESTS/run_core_tests.py",
    "04_CONCEPT_TESTS/run_core_replay_checks.py",
    "04_CONCEPT_TESTS/run_ab_candidate_tests.py",
    "04_CONCEPT_TESTS/AB_CANDIDATE_TEST_RESULTS.csv",
    "04_CONCEPT_TESTS/AB_CANDIDATE_TEST_RESULTS.json",
    "05_REFERENCE_ENGINE/tm_reference_interpreter_v1.py",
    "05_REFERENCE_ENGINE/tm_reference_interpreter_v1_ab_candidate.py",
    "06_SYNTHETIC_REPLAYS/ab_state_1615_1618.json",
    "06_SYNTHETIC_REPLAYS/ab_events_1615_1618.csv",
    "06_SYNTHETIC_REPLAYS/ab_trace_1615_1618.jsonl",
    "07_REAL_REPLAYS/ab_state_L2_1619_1622.json",
    "07_REAL_REPLAYS/ab_events_L2_1619_1622.csv",
    "07_REAL_REPLAYS/ab_trace_L2_1619_1622.jsonl",
    "08_TREE_PYTHON_COMPARISON/CORE_TREE_PYTHON_MATRIX_V1.csv",
    "08_TREE_PYTHON_COMPARISON/AB_TREE_PYTHON_MATRIX_V1.csv",
    "09_OPEN_RULES/OPEN_RULES_CORE_V1.md",
    "09_OPEN_RULES/OPEN_RULES_AB_CANDIDATE_V1.md",
    "10_REPORTS/CHECKPOINT_5_CORE.md",
    "10_REPORTS/CHECKPOINT_6_AB_CANDIDATE.md",
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
        "iteration": "ITERACION_06_AB_CANDIDATE",
        "workspace": str(BASE),
        "objective": "A, return and B candidate on top of the approved core",
        "inputs": inputs,
        "originals_modified": not ok,
        "tree_modified": False,
        "engine_modified": False,
        "golden_modified": False,
        "scope": {
            "core": ["1", "opening", "2", "module_by_discard", "3", "module_regular"],
            "added": ["CONTRARY_MOVE_PENDING", "RETURN_MOVE_PENDING",
                      "ABSORBED_IN_A", "A_CONFIRMED", "B_CANDIDATE",
                      "B flags"],
            "not_implemented": ["B Grande", "AUT by B", "C", "CUT", "TT", "FT",
                                "new one by direct AUT", "gap new one", "concurrency"],
        },
        "tests": {"core": {"count": 19, "passed": 19, "failed": 0},
                  "ab_candidate": {"count": 14, "passed": 14, "failed": 0},
                  "total": 33},
        "anchors": {
            "L1": {"module": 2850, "A": 910, "B_origin": 2985760,
                   "A_structural_time": "16:16:17.809",
                   "A_knowledge_time": "16:17:05.621"},
            "L2": {"one": 750, "two": 1230, "three": 2983030,
                   "module": 1970, "A": 2050,
                   "direct_aut_flag": True},
        },
        "gate_core": "PASS",
        "gate_ab_candidate": "GATE_A_B_CANDIDATE_PASS",
        "tree_gate": "NOT_READY_TO_FREEZE_TREE",
        "engine_status": "REFERENCE_ENGINE_INCOMPLETE",
        "files": files,
    }
    out = BASE / "11_MANIFEST" / "AB_CANDIDATE_MANIFEST.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    sums = BASE / "11_MANIFEST" / "SHA256SUMS_AB.txt"
    lines = [f"{f['sha256']}  {f['path']}" for f in files]
    lines += [f"{v['sha256']}  {v['path']}" for v in inputs.values()]
    sums.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "inputs_ok": ok,
        "files": len(files),
        "core_reader": next(f["sha256"] for f in files
                            if f["path"].endswith("tm_reference_interpreter_v1.py")),
        "ab_reader": next(f["sha256"] for f in files
                          if f["path"].endswith("ab_candidate.py")),
        "manifest": str(out),
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
