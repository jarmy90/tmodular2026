import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from TM_CORE_PYTHON_v071_STATE_ENGINE import (  # noqa: E402
    Seed,
    filter_points,
    load_feed,
    parse_hms,
    run_engine,
    validate_engine,
)

FEED = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    r"C:\Users\profesor\OpenBot\Shared\Transfers\0f47948a-c114-410a-b56d-bafde6fb94f1\TM_TICKFEED_20261016_v010_USTEC_12345_USTEC_DAY16.csv"
)
points_all, bars = load_feed(FEED)


def run(start, end, direction, price):
    points = filter_points(points_all, parse_hms(start), parse_hms(end))
    return run_engine(
        points,
        bars,
        Seed(kind="MODULE", direction=direction, price=price),
        multi_scale=True,
    )


def active(engine):
    return [r for r in engine.readings if r.state in ("MODULE", "A", "B", "TT_PENDING")]


e = run("16:57:08.648", "17:00:59", 1, 2960020)
assert len(e.readings) == 4, len(e.readings)
assert [r.reading_id for r in e.readings] == ["R0001", "R0002", "R0003", "R0004"]
r3 = e.readings[2]
assert r3.state == "TT_OK"
assert r3.a_size == 630
assert r3.tt_target == 2964070
assert r3.tt_pt is not None and r3.tt_pt.price == 2964110
assert e.pending == []
assert len(active(e)) <= 2
assert max(r.scale for r in e.readings) == 1
assert not validate_engine(e)

e2 = run("16:30:00.673", "16:33:59", -1, 2983820)
assert len(e2.readings) == 6, len(e2.readings)
assert "post_tt_fallido_no_definido" in e2.pending
assert len(active(e2)) <= 2
assert max(r.scale for r in e2.readings) == 1
assert not validate_engine(e2)
assert e2.readings[3].state == "TT_OK"
assert e2.readings[5].state == "TT_FALLIDO"

print("REGRESSION OK v0.7.1: 16:57 + 16:30 + genealogy/active/scale")
