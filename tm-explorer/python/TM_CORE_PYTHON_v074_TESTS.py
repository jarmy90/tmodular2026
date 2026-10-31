"""Tests de aceptación v0.7.4: lector funcional multi-escala."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from TM_CORE_PYTHON_v074_FUNCTIONAL_READER import (  # noqa: E402
    A_MAX_MODULE_MULTIPLE,
    A_SIGNIFICANT_NUM,
    CUT_BUFFER,
    MAX_ACTIVE,
    MIN_MODULE,
    MOVE,
    RETRACE_NUM,
    STRUCTURAL_MOVE,
    Engine,
    Pt,
    build_movements,
    filter_points,
    load_feed,
    ms_to_hms,
    parse_hms,
    price_i,
    price_s,
    run_engine,
    write_outputs,
)

FEED = Path(
    r"C:\Users\profesor\OpenBot\Shared\Transfers\9c9276ac-5e0f-4c1a-8edb-22e5466079b0"
    r"\TM_TICKFEED_20261016_v010_USTEC_12345_USTEC_DAY16.csv"
)
POINTS, BARS = load_feed(FEED)
BASE_MS = POINTS[0].time_ms


def run_window(start: str, end: str) -> Engine:
    points = filter_points(POINTS, parse_hms(start, BASE_MS), parse_hms(end, BASE_MS))
    return run_engine(points, BARS)


def synthetic(prices, t0=BASE_MS):
    return [Pt(price_i(p), i + 1, t0 + i * 1000, (t0 + i * 1000) // 60000) for i, p in enumerate(prices)]


def synthetic_bars(points):
    bars = {}
    for p in points:
        b = bars.get(p.bar)
        if b is None:
            bars[p.bar] = type(
                "B",
                (),
                {
                    "idx": p.bar,
                    "name": ms_to_hms(p.bar * 60000)[:5],
                    "open": p,
                    "high": p,
                    "low": p,
                    "last": p,
                    "prev_close": None,
                    "gap": 0,
                },
            )()
        else:
            if p.price > b.high.price:
                b.high = p
            if p.price < b.low.price:
                b.low = p
            b.last = p
    return bars


def run_prices(prices):
    points = synthetic(prices)
    return run_engine(points, synthetic_bars(points))


def test_feed_completo_y_ventana():
    assert len(POINTS) == 11120
    assert ms_to_hms(POINTS[0].time_ms) == "16:20:00.145"
    assert ms_to_hms(POINTS[-1].time_ms) == "17:00:59.931"
    assert len(BARS) == 41
    assert POINTS[-1].price == price_i(29627.30)


def test_movimiento_65_20_existe_y_es_causal():
    moves = build_movements(POINTS, MOVE, RETRACE_NUM, 100)
    target = [m for m in moves if m.origin == price_i(29667.30) and m.extreme == price_i(29602.10)]
    assert target, "no se construyó el movimiento 29667.30 -> 29602.10"
    m = target[0]
    assert m.direction == -1
    assert m.size == price_i(65.20)
    assert m.confirm_index > m.extreme_index
    assert ms_to_hms(POINTS[m.origin_index].time_ms).startswith("16:51:11")


def test_lectura_clave_65_20_tt_29615_20_y_ft():
    engine = run_window("16:50:00", "17:01:00")
    target = [
        r
        for r in engine.readings
        if r.module_origin == price_i(29667.30)
        and r.module_extreme == price_i(29602.10)
        and r.module_size == price_i(65.20)
    ]
    assert len(target) == 1, [r.reading_id for r in target]
    r = target[0]
    assert r.direction == -1
    assert r.a_origin == price_i(29602.10)
    assert r.a_end == price_i(29680.40)
    assert r.a_size == price_i(78.30)
    assert r.b_origin == price_i(29680.40)
    assert r.b_extreme == price_i(29600.20)
    assert r.b_size == price_i(80.20)
    assert r.tt_target == price_i(29615.20)
    assert r.tt_hit is True
    assert r.tt_pt is not None
    assert r.tt_pt.price <= r.tt_target
    assert r.ft is True
    assert r.state == "DONE"
    assert r.created_time <= parse_hms("16:57:26.302", BASE_MS)


def test_limite_de_activas_y_guardia_a_desproporcionada():
    engine = run_window("16:20:00", "17:01:00")
    assert len(engine.readings) >= 50
    assert all(len(engine.active_at(t)) <= MAX_ACTIVE for t in (BASE_MS + 20 * 60_000, BASE_MS + 35 * 60_000))
    guarded = [
        r
        for r in engine.readings
        if any(label == "A_DESPROPORCIONADA_MODULO" for _, label in r.labels)
    ]
    assert guarded
    for r in guarded:
        assert r.a_size > A_MAX_MODULE_MULTIPLE * r.module_size
        assert r.state == "DONE"


def test_sin_tt_antes_de_b():
    engine = run_window("16:20:00", "17:01:00")
    for r in engine.readings:
        if r.tt_hit:
            assert r.b_origin != 0 and r.b_extreme != 0
            assert r.b_size >= r.a_size


def _prefix_snapshot(engine: Engine, cutoff: int):
    events = [
        (
            e["time_ms"],
            e["kind"],
            e["function"],
            e["reading_id"],
            e["new_state"],
            e["module_origin"],
            e["module_extreme"],
            e["a_origin"],
            e["a_end"],
            e["b_extreme"],
            e["tt_target"],
            e["ft"],
        )
        for e in engine.events
        if e["time_ms"] <= cutoff and e["kind"] != "FIN_FEED"
    ]
    created = [
        (r.reading_id, r.created_time, r.module_origin, r.module_extreme, r.origin_reason)
        for r in engine.readings
        if r.created_time <= cutoff
    ]
    return events, created


def test_prefix_invariance_hasta_1659():
    cutoff = parse_hms("16:59:00.000", BASE_MS)
    full = run_window("16:20:00", "17:01:00")
    prefix_points = filter_points(POINTS, None, cutoff)
    prefix = run_engine(prefix_points, BARS)
    assert _prefix_snapshot(full, cutoff) == _prefix_snapshot(prefix, cutoff)
    assert len([r for r in full.readings if r.created_time <= cutoff]) >= 50


def test_gap_no_detiene_vela_y_eventos():
    engine = run_window("16:52:00", "17:01:00")
    gaps = [e for e in engine.events if e["function"] == "GAP"]
    assert [e["bar_time"] for e in gaps] == [
        "16:52",
        "16:53",
        "16:54",
        "16:55",
        "16:56",
        "16:57",
        "16:58",
        "16:59",
        "17:00",
    ]
    assert any(e["bar_time"] == "16:52" and e["gap"] == price_i(-0.70) for e in gaps)
    assert any(e["bar_time"] == "16:55" and e["gap"] == price_i(1.80) for e in gaps)
    assert any(e["bar_time"] == "16:56" and e["gap"] == price_i(-3.50) for e in gaps)
    audit = [a for a in engine.audit if a["bar_time"] == "16:56"]
    assert len(audit) > 0
    assert any(a["functional_coverage"] in ("OK", "UNCOVERED") for a in audit)


def test_cut_buffer_no_corta_por_1_90_y_permite_tt():
    engine = run_prices(
        [
            100.00, 90.00,
            99.00,
            88.00,
            100.90,
            87.00,
            95.00,
        ]
    )
    target = [r for r in engine.readings if r.module_origin == price_i(100.00) and r.module_extreme == price_i(90.00)]
    assert target
    r = target[0]
    assert r.a_end == price_i(99.00)
    assert r.tt_target == price_i(89.00)
    assert not any(label == "CUT" for _, label in r.labels)
    assert r.tt_hit is True
    assert r.ft is True


def test_a_mayor_que_modulo_no_se_invalida_si_es_razonable():
    engine = run_window("16:50:00", "17:01:00")
    target = [r for r in engine.readings if r.module_size == price_i(65.20)]
    assert target
    r = target[0]
    assert r.a_size > r.module_size
    assert r.a_size < 2 * r.module_size
    assert "A_INVALIDA_MODULO" not in [label for _, label in r.labels]


def test_csv_y_reporte_completo(tmp_path):
    engine = run_window("16:52:00", "17:01:00")
    paths = write_outputs(engine, tmp_path, "v074")
    names = {p.name for p in paths}
    for required in (
        "v074_Eventos.csv",
        "v074_Lecturas.csv",
        "v074_Patrones.csv",
        "v074_FunctionalAudit.csv",
        "v074_BarNarrative.csv",
        "v074_Informe.json",
        "v074_Comparacion_1652_1700.csv",
    ):
        assert required in names, required
    with (tmp_path / "v074_Eventos.csv").open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        assert {"sequence_id", "time", "bar_time", "function", "new_state", "reading_id", "parent_reading_id"} <= set(reader.fieldnames)
        rows = list(reader)
    assert rows
    with (tmp_path / "v074_Lecturas.csv").open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        assert {"structural_valid", "operational_valid", "operational_rejection_reason", "a_origin", "a_end", "tt_target", "ft"} <= set(reader.fieldnames)
    with (tmp_path / "v074_FunctionalAudit.csv").open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        assert {"sequence_id", "time", "price", "bar_time", "gap", "active_readings", "inherited_readings", "local_readings", "functions_before", "functions_after", "events_emitted", "readings_created", "ownership_count", "functional_coverage", "decision_reason"} <= set(reader.fieldnames)
    with (tmp_path / "v074_BarNarrative.csv").open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        assert {"bar_time", "open", "high", "low", "close", "gap", "extreme_order", "functions", "readings_started", "readings_closed", "active_at_close"} <= set(reader.fieldnames)
    info = json.loads((tmp_path / "v074_Informe.json").read_text(encoding="utf-8"))
    assert info["version"] == "0.7.4"
    assert info["coverage"]["geometric_count"] > 0
    assert info["coverage"]["functional_count"] > 0
    assert "implementation_pending" in info


def test_vocabulario_funcional_sin_prohibidos():
    engine = run_window("16:52:00", "17:01:00")
    functions = {e["function"] for e in engine.events}
    forbidden = {"LOCAL", "SUPERIOR", "ESTRUCTURA", "GIRO", "B_EXCESIVA", "OBSERVADOR"}
    assert not (functions & forbidden)


def test_motor_sin_hardcode_de_ventana():
    source = Path(__file__).with_name("TM_CORE_PYTHON_v074_FUNCTIONAL_READER.py").read_text(encoding="utf-8")
    for token in ("29667.30", "29680.40", "29615.20", "16:52:32.528", "16:55:12.759"):
        assert token not in source


def test_selftest_interno():
    from TM_CORE_PYTHON_v074_FUNCTIONAL_READER import selftest

    selftest()
