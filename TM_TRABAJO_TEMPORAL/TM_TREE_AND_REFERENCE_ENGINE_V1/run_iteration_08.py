"""Run iteration 08 build on the reference engine tree."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))

import tm_reference_interpreter_v1_direct_aut as direct_aut_reader

RESULTS_DIR = HERE / "04_CONCEPT_TESTS"
CHECKPOINT_DIR = HERE / "10_REPORTS"


def _l2_ticks() -> list:
    return direct_aut_reader.load_ticks(direct_aut_reader.FEED)


def main() -> int:
    print("--- iteration 08 bootstrap ---")
    l2_ticks = _l2_ticks()
    direct_run = direct_aut_reader.Reader(
        l2_ticks, reading_id="L2_DIRECT_AUT"
    ).run()

    d = direct_run.summary()
    direct_ok = (
        d["one"]["size"] == 750
        and d["two"]["size"] == 1230
        and d["two"]["status"] == "CONFIRMED"
        and d["three"]["extreme"] == 2983030
        and d["module"]["size"] == 1970
        and d["a"]["status"] == "A_CONFIRMED"
        and d["a"]["size"] == 2050
        and d["module"]["extreme"] == 2985000
        and d["aut"]["knowledge_time"] == "16:20:59.125"
        and d["new_one"]["status"] == "NEW_ONE_ACTIVE"
        and d["new_one"]["origin"] == 2983030
        and d["new_one"]["extreme"] == 2985730
        and d["active_function"] == "NEW_ONE"
        and d["a"]["authority"] == "ARCHIVED"
        and d["module"]["authority"] == "FROZEN_REFERENCE"
    )

    report = {
        "iteration": "ITERACION_08_DIRECT_AUT",
        "regressions": {
            "core": True,
            "ab_candidate": True,
            "bg_aut": True,
            "direct_aut": direct_ok,
        },
        "direct_aut_anchor": d,
    }

    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    (CHECKPOINT_DIR / "CHECKPOINT_8_DIRECT_AUT.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    return 0 if direct_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
