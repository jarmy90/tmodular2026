"""Regresion v0.7.2: seed TT, post-TT, CSV, cobertura y metamorficos."""

import csv
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from TM_CORE_PYTHONdeepseek_v072_STATE_ENGINE import (  # noqa: E402
    FT_CANDIDATE,
    FT_CONFIRMED,
    MOVE,
    Bar,
    Engine,
    Pt,
    Seed,
    TT_CONFIRMED,
    TT_EXTENDING,
    TT_PENDING,
    evaluate_coverage,
    filter_points,
    load_feed,
    parse_hms,
    run_engine,
    validate_engine,
    write_outputs,
)

FEED = Path(
    r"C:\Users\profesor\OpenBot\Shared\Transfers\0f47948a-c114-410a-b56d-bafde6fb94f1"
    r"\TM_TICKFEED_20261016_v010_USTEC_12345_USTEC_DAY16.csv"
)
T0 = 1_792_169_100_000
POINTS, BARS = load_feed(FEED)
BASE_MS = POINTS[0].time_ms


def bars_for(points):
    first = points[0]
    return {
        first.bar: Bar(
            idx=first.bar,
            name="test",
            open=first,
            high=first,
            low=first,
            last=first,
            prev_close=None,
        )
    }


def synthetic(prices, t0=T0):
    return [Pt(price, i + 1, t0 + i, 0) for i, price in enumerate(prices)]


def run_prices(prices, seed=None):
    points = synthetic(prices)
    return run_engine(points, bars_for(points), seed, multi_scale=True)


def confirmed_seed(extreme=100_000, tt100=99_000, target=98_500):
    return Seed(
        kind="TT_CONFIRMED",
        direction=1,
        price=extreme,
        module_origin=90_000,
        module_extreme=extreme,
        a_origin=95_000,
        a_end=94_000,
        tt_target=target,
        tt_state=TT_CONFIRMED,
        tt_100_time=T0,
        tt_100_price=tt100,
        tt_100_seq=10,
        tt_real_extreme_time=T0,
        tt_real_extreme_price=extreme,
        tt_real_extreme_seq=11,
        aut_time=T0 - 1_000,
        aut_price=99_000,
        parent_tt_id="R0000",
    )


def events(engine, kind):
    return [e for e in engine.events if e["kind"] == kind]


def test_seed_tt_001_pending_before_100():
    e = run_prices(
        [100_000, 100_100, 100_200],
        Seed(kind="TT_PENDING", direction=1, price=100_000, module_origin=90_000, module_extreme=105_000, tt_target=110_000),
    )
    r = e.readings[0]
    assert r.state == TT_PENDING
    assert not r.tt_confirmed
    assert not events(e, "TT_100_RESTORED")
    assert not events(e, "TT_CONFIRMADO")
    assert e.pending == []


def test_seed_tt_002_confirmed_does_not_return_pending():
    e = run_prices([100_000, 100_100, 100_500], confirmed_seed())
    r = e.readings[0]
    assert r.state == TT_EXTENDING
    assert r.tt_confirmed and r.tt_pt is not None and r.tt_pt.price == 99_000
    assert events(e, "TT_100_RESTORED")
    assert not events(e, "TT_PENDIENTE")
    assert not validate_engine(e)


def test_seed_tt_003_real_extreme_extends():
    e = run_prices([100_000, 100_500, 101_000], confirmed_seed())
    r = e.readings[0]
    assert r.new1_ext.price == 101_000
    assert r.tt_ext.price == 101_000
    assert len(events(e, "TT_REAL_EXTREME_UPDATED")) == 2
    assert r.tt_real_extreme_seq == 3


def test_post_tt_001_retreat_below_move_is_noise():
    e = run_prices([100_000, 99_850], confirmed_seed())
    assert not [p for p in e.patterns if p["type"] == "FT"]
    assert not events(e, "FT_CANDIDATE_OPENED")


def test_post_tt_002_retreat_equal_move_opens_candidate():
    e = run_prices([100_000, 99_800], confirmed_seed())
    assert len(events(e, "FT_CANDIDATE_OPENED")) == 1
    patterns = [p for p in e.patterns if p["type"] == "FT"]
    assert len(patterns) == 1
    assert patterns[0]["status"] == FT_CANDIDATE
    assert patterns[0]["origin_price"] == "1000.00"
    assert patterns[0]["end_price"] == "998.00"


def test_post_tt_003_candidate_absorbed_by_new_extreme():
    e = run_prices([100_000, 99_800, 100_100], confirmed_seed())
    patterns = [p for p in e.patterns if p["type"] == "FT"]
    assert patterns and patterns[0]["status"] == "FT_CANDIDATE_ABSORBED_BY_TT_EXTENSION"
    assert events(e, "FT_CANDIDATE_ABSORBED")
    assert e.readings[0].new1_ext.price == 100_100


def run_1645():
    points = filter_points(POINTS, parse_hms("16:45:00", BASE_MS), parse_hms("16:48:59.999", BASE_MS))
    seed = Seed(
        kind="TT_CONFIRMED",
        direction=1,
        price=29_733_30,
        module_origin=29_651_20,
        module_extreme=29_736_70,
        a_origin=29_686_90,
        a_end=29_679_80,
        tt_target=29_715_50,
        tt_state=TT_CONFIRMED,
        tt_100_time=parse_hms("16:44:45.581", BASE_MS),
        tt_100_price=29_716_30,
        tt_100_seq=6603,
        tt_real_extreme_time=parse_hms("16:44:59.014", BASE_MS),
        tt_real_extreme_price=29_736_70,
        tt_real_extreme_seq=6666,
        aut_time=parse_hms("16:43:05.904", BASE_MS),
        aut_price=29_689_30,
        parent_tt_id="R0004",
    )
    return run_engine(points, BARS, seed, multi_scale=True)


def test_post_tt_004_ft_and_local_readings_coexist():
    e = run_1645()
    r1 = next(r for r in e.readings if r.reading_id == "R0001")
    assert r1.state == TT_EXTENDING
    assert r1.new1_ext.price == 29_745_10
    r6 = next(r for r in e.readings if r.reading_id == "R0006")
    assert r6.state == TT_EXTENDING
    assert r6.parent_tt_id == "R0001"
    assert r6.new1_ext.price == 29_674_60
    assert sum(r.is_active for r in e.readings) == 2
    assert e.pending == []
    assert e.TM_COVERAGE_OK is True


def test_reg_1645_1648_ft_and_local():
    e = run_1645()
    r1 = next(r for r in e.readings if r.reading_id == "R0001")
    assert r1.new1_ext.price == 29_745_10
    assert r1.ft_ext.price == 29_674_60
    p7 = next(p for p in e.patterns if p["pattern_id"] == "P0007")
    assert p7["status"] == FT_CONFIRMED
    assert p7["origin_price"] == "29745.10"
    assert p7["end_price"] == "29674.60"
    r6 = next(r for r in e.readings if r.reading_id == "R0006")
    assert r6.a_size == 520
    assert not validate_engine(e)


def test_post_tt_005_gap_keeps_ft_and_limits_locals():
    e = run_1645()
    assert any(ev["kind"] == "GAP" for ev in e.events)
    assert sum(r.is_active for r in e.readings) <= 2
    p7 = next(p for p in e.patterns if p["pattern_id"] == "P0007")
    assert p7["status"] == FT_CONFIRMED
    local = [r for r in e.readings if r.reading_id == "R0006"]
    assert len(local) == 1 and local[0].parent_tt_id == "R0001"


def test_csv_001_statuses_are_consistent():
    points = filter_points(POINTS, parse_hms("16:42:09.361", BASE_MS), parse_hms("16:44:59.999", BASE_MS))
    e = run_engine(points, BARS, Seed(kind="MODULE", direction=1, price=29_651_20), multi_scale=True)
    with tempfile.TemporaryDirectory() as tmp:
        paths = write_outputs(e, Path(tmp), "test")
        rows = {p.name: list(csv.DictReader(p.open(encoding="utf-8", newline=""))) for p in paths}
    patterns = rows["test_Patrones.csv"]
    readings = rows["test_Lecturas.csv"]
    assert patterns and all(p["final_status"] for p in patterns)
    assert all(p["status"] == p["final_status"] for p in patterns)
    for r in readings:
        if r["final_priority"] == "ABSORBED":
            assert r["absorbed_by_reading_id"] or r["state"].endswith("ABSORBED_BY_DOMINANT")
        if r["state"] == FT_CONFIRMED:
            assert r["ft_status"] == FT_CONFIRMED


def test_coverage_001_unexplained_move_is_pending():
    e = Engine(None, multi_scale=True)
    a = Pt(10_000, 1, T0, 0)
    b = Pt(11_000, 2, T0 + 1, 0)
    e._new_reading(a, 1, "MODULE", "TEST", a, b)
    points = [Pt(20_000, 3, T0 + 2, 0), Pt(30_000, 4, T0 + 3, 0)]
    evaluate_coverage(e, points)
    assert e.TM_COVERAGE_OK is False
    assert e.coverage_unresolved[0]["reason"] == "UNEXPLAINED_STRUCTURAL_MOVE"
    assert "UNEXPLAINED_STRUCTURAL_MOVE" in e.pending


def test_reg_1642_principal_tt():
    points = filter_points(POINTS, parse_hms("16:42:09.361", BASE_MS), parse_hms("16:44:59.999", BASE_MS))
    e = run_engine(points, BARS, Seed(kind="MODULE", direction=1, price=29_651_20), multi_scale=True)
    assert e.TM_COVERAGE_OK is True
    assert e.pending == []
    r1 = next(r for r in e.readings if r.reading_id == "R0001")
    assert r1.state == "TT_MINOR_ABSORBED_BY_DOMINANT"
    assert abs(r1.a_size - 750) == 0
    r4 = next(r for r in e.readings if r.reading_id == "R0004")
    assert r4.state == TT_EXTENDING
    assert r4.tt_target == 29_715_50
    assert r4.tt_pt.price == 29_716_30
    assert r4.new1_ext.price == 29_736_70
    assert not events(e, "TT_PENDIENTE") or all(
        ev["reading_id"] != "R0006" for ev in events(e, "TT_PENDIENTE")
    )
    assert not validate_engine(e)


def test_metamorphic_price_shift():
    points = filter_points(POINTS, parse_hms("16:42:09.361", BASE_MS), parse_hms("16:44:59.999", BASE_MS))
    baseline = run_engine(points, BARS, Seed(kind="MODULE", direction=1, price=29_651_20), multi_scale=True)
    delta = 100_000
    shifted = [Pt(p.price + delta, p.seq, p.time_ms, p.bar) for p in points]
    bars = {
        k: Bar(v.idx, v.name, _shift(v.open, delta), _shift(v.high, delta), _shift(v.low, delta), _shift(v.last, delta), None if v.prev_close is None else v.prev_close + delta)
        for k, v in BARS.items()
    }
    moved = run_engine(shifted, bars, Seed(kind="MODULE", direction=1, price=29_651_20 + delta), multi_scale=True)
    b4 = next(r for r in baseline.readings if r.reading_id == "R0004")
    m4 = next(r for r in moved.readings if r.reading_id == "R0004")
    assert m4.tt_target == b4.tt_target + delta
    assert m4.tt_pt.price == b4.tt_pt.price + delta
    assert m4.new1_ext.price == b4.new1_ext.price + delta


def test_metamorphic_time_shift():
    points = filter_points(POINTS, parse_hms("16:42:09.361", BASE_MS), parse_hms("16:44:59.999", BASE_MS))
    baseline = run_engine(points, BARS, Seed(kind="MODULE", direction=1, price=29_651_20), multi_scale=True)
    delta = 1_800_000
    dbar = 30
    shifted = [Pt(p.price, p.seq, p.time_ms + delta, p.bar + dbar) for p in points]
    bars = {
        k + dbar: Bar(v.idx + dbar, v.name, _shift_t(v.open, delta), _shift_t(v.high, delta), _shift_t(v.low, delta), _shift_t(v.last, delta), v.prev_close)
        for k, v in BARS.items()
    }
    moved = run_engine(shifted, bars, Seed(kind="MODULE", direction=1, price=29_651_20), multi_scale=True)
    b4 = next(r for r in baseline.readings if r.reading_id == "R0004")
    m4 = next(r for r in moved.readings if r.reading_id == "R0004")
    assert m4.tt_target == b4.tt_target
    assert m4.new1_ext.price == b4.new1_ext.price


def test_metamorphic_symmetry():
    e_up = run_prices([100_000, 101_200, 100_900, 101_500, 99_800], Seed(kind="MODULE", direction=1, price=100_000))
    axis = 200_000
    down = [axis - p for p in [100_000, 101_200, 100_900, 101_500, 99_800]]
    e_dn = run_prices(down, Seed(kind="MODULE", direction=-1, price=axis - 100_000))
    up_targets = [r.tt_target for r in e_up.readings if r.tt_target is not None]
    dn_targets = [r.tt_target for r in e_dn.readings if r.tt_target is not None]
    assert [axis - t for t in dn_targets] == up_targets
    assert [r.state for r in e_up.readings] == [r.state for r in e_dn.readings]


def test_metamorphic_tick_count():
    prices = [100_000, 101_000, 100_200, 102_000, 99_000]
    few = run_prices(prices, Seed(kind="MODULE", direction=1, price=100_000))
    many_prices = []
    for price in prices:
        many_prices.extend([price, price])
    many = run_prices(many_prices, Seed(kind="MODULE", direction=1, price=100_000))
    a = next(r for r in few.readings if r.tt_target is not None)
    b = next(r for r in many.readings if r.tt_target is not None)
    assert a.tt_target == b.tt_target


def _shift(pt, delta):
    return Pt(pt.price + delta, pt.seq, pt.time_ms, pt.bar)


def _shift_t(pt, delta):
    return Pt(pt.price, pt.seq, pt.time_ms + delta, pt.bar)


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
        print(f"OK {test.__name__}")
    print(f"TESTS OK v0.7.2: {len(tests)} comprobaciones")


if __name__ == "__main__":
    main()

