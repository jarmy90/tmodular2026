from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "audit_v0751"))

import TM_CORE_PYTHON_v0751_STREAMING as core
import audit_v0751_golden as golden

FEED = golden.FEED


@pytest.fixture(scope="module")
def full() -> core.Engine:
    points, bars = core.load_feed(FEED)
    return core.run_engine(points, bars)


def _local_signature(engine: core.Engine, cutoff: int) -> list[tuple]:
    return [
        (
            event["bar_time"],
            event["function"],
            event["direction"],
            event["origin"],
            event["extreme"],
            event["confirmation_time_ms"],
        )
        for event in engine.local_events
        if event["confirmation_time_ms"] <= cutoff
    ]


def test_golden_v003(full: core.Engine) -> None:
    checks = golden.evaluate(full)
    failed = [check for check in checks if not check["ok"]]
    assert not failed, failed


def test_gap_sin_espurios(full: core.Engine) -> None:
    gaps = [event for event in full.events if event["function"] == "GAP"]
    assert len(gaps) == 62
    assert all(abs(event["gap"]) >= core.PLANO_TICK for event in gaps)
    assert min(abs(event["gap"]) for event in gaps) >= 25
    assert max(abs(event["gap"]) for event in gaps) == 1400


def test_local_causalidad(full: core.Engine) -> None:
    assert full.local_events
    for event in full.local_events:
        assert event["confirmation_time_ms"] >= event["extreme_time_ms"]
        assert event["confirmation_time_ms"] >= event["origin_time_ms"]
        assert event["knowledge_time_ms"] == event["confirmation_time_ms"]
        assert event["size"] > 0


def test_local_prefijos(full: core.Engine) -> None:
    cutoffs = [
        1792167714482,
        1792167781216,
        1792167898066,
    ]
    points, bars = core.load_feed(FEED)
    for cutoff in cutoffs:
        prefix = [point for point in points if point.time_ms <= cutoff]
        assert prefix
        engine = core.run_engine(prefix, bars)
        expected = _local_signature(full, cutoff)
        observed = _local_signature(engine, cutoff)
        assert observed == expected, (core.ms_to_text(cutoff), expected, observed)


def test_r0064_correspondencia_r0062(full: core.Engine) -> None:
    reading = next((r for r in full.readings if r.reading_id == "R0064"), None)
    assert reading is not None
    assert reading.state == "DONE"
    assert reading.module_origin == 2966730
    assert reading.module_extreme == 2960210
    assert reading.a_origin == 2960210
    assert reading.a_end == 2968040
    assert reading.b_origin == 2968040
    assert reading.b_extreme == 2960020
    assert reading.tt_target == 2961520
    assert reading.tt_hit is True
    assert reading.tt_price == 2961420
    assert reading.ft is True
    assert reading.ft_price == 2962110
    assert reading.ft_structural_time == 1792169846302
    events = [event for event in full.events if event["reading_id"] == "R0064"]
    assert len(events) == 26


def test_gap_causal_prioritario(full: core.Engine) -> None:
    for index, event in enumerate(full.events):
        if event["function"] != "GAP":
            continue
        earlier_same_time = [
            other
            for other in full.events[:index]
            if other["knowledge_time_ms"] == event["knowledge_time_ms"]
        ]
        assert all(other["function"] == "GAP" for other in earlier_same_time)


def test_local_en_v003_sin_hardcode_en_motor() -> None:
    source = (ROOT / "python" / "TM_CORE_PYTHON_v0751_STREAMING.py").read_text(
        encoding="utf-8"
    )
    assert "29850.8" not in source
    assert "16:19" not in source
    assert "LS0001" not in source
