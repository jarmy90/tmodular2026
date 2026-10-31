#!/usr/bin/env python3
"""Pre-flight audit for ITERACION_08_DIRECT_AUT package build."""
from __future__ import annotations

import sys
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
ENGINE_DIR = PACKAGE_DIR.parent
ROOT_DIR = ENGINE_DIR.parents[1]

EXPECTED = [
    ENGINE_DIR / "10_REPORTS" / "CHECKPOINT_8_DIRECT_AUT.md",
    ENGINE_DIR / "02_EXECUTABLE_TREE" / "TM_TREE_EXECUTABLE_DIRECT_AUT_V1.md",
    ENGINE_DIR / "03_TRANSITION_SPECS" / "TM_TREE_TRANSITIONS_DIRECT_AUT_V1.csv",
    ENGINE_DIR / "04_CONCEPT_TESTS" / "CONCEPT_TEST_MATRIX_DIRECT_AUT_V1.csv",
    ENGINE_DIR / "05_REFERENCE_ENGINE" / "tm_reference_interpreter_v1_direct_aut.py",
    ENGINE_DIR / "05_REFERENCE_ENGINE" / "tm_reference_interpreter_v1_bg_aut.py",
    ENGINE_DIR / "04_CONCEPT_TESTS" / "CONCEPT_TEST_MATRIX_B_GRANDE_AUT_V1.csv",
    ENGINE_DIR / "04_CONCEPT_TESTS" / "AB_CANDIDATE_TEST_RESULTS.csv",
    ENGINE_DIR / "04_CONCEPT_TESTS" / "CORE_TEST_RESULTS.csv",
    ENGINE_DIR / "04_CONCEPT_TESTS" / "CORE_TEST_RESULTS.json",
    ENGINE_DIR / "04_CONCEPT_TESTS" / "CORE_REPLAY_CHECKS.json",
    ENGINE_DIR / "07_REAL_REPLAYS" / "direct_aut_state_L2_1619_1622.json",
    ENGINE_DIR / "07_REAL_REPLAYS" / "direct_aut_events_L2_1619_1622.csv",
    ENGINE_DIR / "07_REAL_REPLAYS" / "bg_events_L2_1619_1622.csv",
    ENGINE_DIR / "08_TREE_PYTHON_COMPARISON" / "DIRECT_AUT_TREE_PYTHON_MATRIX_V1.csv",
    ENGINE_DIR / "09_OPEN_RULES" / "OPEN_RULES_DIRECT_AUT_V1.md",
    ENGINE_DIR / "10_REPORTS" / "CHECKPOINT_7_B_GRANDE_AUT.md",
    ENGINE_DIR / "05_REFERENCE_ENGINE" / "tm_reference_interpreter_v1_ab_candidate.py",
    ENGINE_DIR / "05_REFERENCE_ENGINE" / "tm_reference_interpreter_v1.py",
    ENGINE_DIR / "11_MANIFEST" / "DIRECT_AUT_MANIFEST.json",
]


def main() -> None:
    print(f"ENGINE_DIR={ENGINE_DIR}")
    print(f"PACKAGE_DIR={PACKAGE_DIR}")
    print(f"ROOT_DIR={ROOT_DIR}")
    missing = []
    for p in EXPECTED:
        if not p.is_file():
            missing.append(str(p))
    if missing:
        print("MISSING:")
        for m in missing:
            print(m)
        sys.exit(1)
    print("ALL_EXPECTED_INPUTS_PRESENT")


if __name__ == "__main__":
    main()
