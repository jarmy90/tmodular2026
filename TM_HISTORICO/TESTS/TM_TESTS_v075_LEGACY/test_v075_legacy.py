"""Tests de aceptacion v0.7.5: streaming causal y prefijos fisicos."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "python"))

from TM_CORE_PYTHON_v075_STREAMING import (  # noqa: E402
    A_MAX_MODULE_MULTIPLE,
    AUT_DEN,
    AUT_EXTRA,
    AUT_NUM,
    MAX_ACTIVE,
    MOVE,
    RETRACE_NUM,
    STRUCTURAL_MOVE,
    Engine,
    Pt,
    build_movements,
    compare_prefix,
    evaluate_afs2,
    filter_points,
    load_feed,
    ms_to_hms,
    parse_hms,
    price_i,
    run_engine,
    run_prefix_matrix,
    selftest,
    write_outputs,
)

FEED = ROOT / "data" / "TM_TICKFEED_v010_LEGACY.csv"
POINTS, BARS = load_feed(FEED)
BASE_MS = POINTS[0].time_ms
FULL = run_engine(POINTS, BARS)


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
    assert target, "no se construyo el movimiento 29667.30 -> 29602.10"
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


def test_tt_100_se_conoce_con_b_grande_no_con_el_cruce():
    key = [r for r in FULL.readings if r.reading_id == "R0062"]
    assert len(key) == 1
    r = key[0]
    assert r.tt_time == parse_hms("16:56:32.145", BASE_MS)
    assert r.b_grande_time == parse_hms("16:57:16.859", BASE_MS)
    assert r.tt_confirmation_time == r.b_grande_time
    assert r.tt_knowledge_time == r.b_grande_time
    assert r.tt_time < r.tt_knowledge_time

    cutoff_before = parse_hms("16:56:59.999", BASE_MS)
    prefix = run_engine([p for p in POINTS if p.time_ms <= cutoff_before], BARS)
    assert not any(
        e["function"] == "TT" and e["reading_id"] == "R0062" for e in prefix.events
    )
    assert compare_prefix(FULL, prefix, cutoff_before)["pass"]

    cutoff_after = parse_hms("16:57:16.859", BASE_MS)
    prefix_after = run_engine([p for p in POINTS if p.time_ms <= cutoff_after], BARS)
    tt = [e for e in prefix_after.events if e["function"] == "TT" and e["reading_id"] == "R0062"]
    assert len(tt) == 1
    assert tt[0]["structural_time"] == "2026-10-16 16:56:32.145"
    assert tt[0]["knowledge_time"] == "2026-10-16 16:57:16.859"
    assert compare_prefix(FULL, prefix_after, cutoff_after)["pass"]


def test_eventos_append_only_secuencia_real_y_conocimiento():
    ids = [e["event_id"] for e in FULL.events]
    assert ids == [f"E{index:06d}" for index in range(1, len(ids) + 1)]
    seqs = [e["sequence_id"] for e in FULL.events]
    assert seqs == sorted(seqs)
    feed_seqs = {p.seq for p in POINTS}
    for e in FULL.events:
        assert e["sequence_id"] == e["knowledge_sequence_id"]
        assert e["sequence_id"] in feed_seqs
        assert e["knowledge_time_ms"] >= e["structural_time_ms"]
        assert e["knowledge_time_ms"] >= e["confirmation_time_ms"]


def test_gap_se_emite_antes_de_cualquier_rama():
    by_seq = {}
    for e in FULL.events:
        by_seq.setdefault(e["sequence_id"], []).append(e)
    gap_bars = 0
    for bar_idx in sorted({p.bar for p in POINTS}):
        bar = BARS[bar_idx]
        if not bar.gap:
            continue
        first = next(p for p in POINTS if p.bar == bar_idx)
        events = by_seq.get(first.seq, [])
        assert events, f"sin eventos en apertura {bar.name}"
        assert events[0]["kind"] == "GAP", (bar.name, [e["kind"] for e in events])
        gap_bars += 1
    assert gap_bars == 40


def test_auditoria_un_tick_por_punto_y_owner_explicito():
    assert len(FULL.audit) == len(POINTS)
    assert [row["sequence_id"] for row in FULL.audit] == [p.seq for p in POINTS]
    allowed = {"C", "B", "A", "MODULE", "NOISE", "NONE"}
    for row in FULL.audit:
        assert row["owner_source"] in allowed
        assert row["functional_coverage"] in {"OK", "UNCOVERED"}
        if row["owner_reading_id"]:
            assert row["owner_known_at_seq"] <= row["sequence_id"]
            assert row["owner_created_time"]


def test_cobertura_causal_no_usa_lecturas_futuras():
    coverage = FULL.coverage
    assert coverage["causal_geometric_count"] <= coverage["geometric_count"]
    assert coverage["causal_functional_count"] <= coverage["functional_count"]
    assert coverage["causal_functional_movement_count"] <= coverage["movement_count"]
    for r in FULL.readings:
        assert r.created_time >= r.module_origin_time
        assert r.created_time >= r.module_extreme_time
        if r.tt_hit:
            assert r.b_grande_time
            assert r.tt_knowledge_time >= r.b_grande_time


def test_aut_solo_despues_de_b_grande_y_sobre_limite():
    b_grande_at = {}
    aut_at = {}
    for index, e in enumerate(FULL.events):
        if e["function"] == "B_GRANDE":
            b_grande_at.setdefault(e["reading_id"], index)
        if e["function"] == "AUT":
            aut_at.setdefault(e["reading_id"], index)
    assert aut_at
    for rid, index in aut_at.items():
        assert rid in b_grande_at, rid
        assert b_grande_at[rid] < index, rid
        r = FULL.by_id[rid]
        event = FULL.events[index]
        assert r.aut_reclassified is True
        excursion = abs(event["b_extreme"] - event["b_origin"])
        assert excursion > (AUT_NUM * r.a_size) // AUT_DEN + AUT_EXTRA


def test_limite_de_activas_y_guardia_a_desproporcionada():
    assert len(FULL.readings) >= 50
    assert all(len(FULL.active_at(t)) <= MAX_ACTIVE for t in (BASE_MS + 20 * 60_000, BASE_MS + 35 * 60_000))
    guarded = [
        r
        for r in FULL.readings
        if any(label == "A_DESPROPORCIONADA_MODULO" for _, label in r.labels)
    ]
    assert guarded
    for r in guarded:
        assert r.a_size > A_MAX_MODULE_MULTIPLE * r.module_size
        assert r.state == "DONE"


def test_sin_tt_antes_de_b():
    for r in FULL.readings:
        if r.tt_hit:
            assert r.b_origin != 0 and r.b_extreme != 0
            assert r.b_size >= r.a_size


def test_prefix_invariance_estricta_en_velas_y_hitos():
    cutoffs = [p.time_ms for p in POINTS if p.seq and (p.time_ms % 60000) >= 59000]
    cutoffs = sorted(set(cutoffs))
    cutoffs += [
        parse_hms("16:56:59.999", BASE_MS),
        parse_hms("16:57:16.859", BASE_MS),
        parse_hms("16:57:34.937", BASE_MS),
        parse_hms("17:00:59.931", BASE_MS),
    ]
    _, rows = run_prefix_matrix(POINTS, BARS, cutoffs, FULL)
    failures = [row for row in rows if not row["pass"]]
    assert not failures, failures[:2]
    assert rows


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
    target = [r for r in FULL.readings if r.module_size == price_i(65.20)]
    assert target
    r = target[0]
    assert r.a_size > r.module_size
    assert r.a_size < 2 * r.module_size
    assert "A_INVALIDA_MODULO" not in [label for _, label in r.labels]


def test_csv_y_reporte_completo(tmp_path):
    engine = run_window("16:52:00", "17:01:00")
    paths = write_outputs(engine, tmp_path, "v075")
    names = {p.name for p in paths}
    for required in (
        "v075_Eventos.csv",
        "v075_Lecturas.csv",
        "v075_Patrones.csv",
        "v075_FunctionalAudit.csv",
        "v075_BarNarrative.csv",
        "v075_Informe.json",
        "v075_Comparacion_1652_1700.csv",
    ):
        assert required in names, required
    with (tmp_path / "v075_Eventos.csv").open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        assert {
            "event_id",
            "sequence_id",
            "knowledge_sequence_id",
            "structural_time",
            "confirmation_time",
            "knowledge_time",
            "knowledge_price",
            "function",
        } <= set(reader.fieldnames)
        rows = list(reader)
    assert rows
    with (tmp_path / "v075_Lecturas.csv").open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        assert {
            "created_seq",
            "tt_100_time",
            "tt_confirmation_time",
            "tt_knowledge_time",
            "ft_structural_time",
            "structural_valid",
            "operational_valid",
        } <= set(reader.fieldnames)
    with (tmp_path / "v075_FunctionalAudit.csv").open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        assert {
            "owner_reading_id",
            "owner_source",
            "owner_known_at_seq",
            "ownership_count",
            "functional_coverage",
            "functions_before",
            "functions_after",
        } <= set(reader.fieldnames)
    info = json.loads((tmp_path / "v075_Informe.json").read_text(encoding="utf-8"))
    assert info["version"] == "0.7.5"
    assert info["coverage"]["geometric_count"] > 0
    assert info["coverage"]["causal_geometric_count"] > 0
    assert "AFS2_READY" in info


def test_vocabulario_funcional_sin_prohibidos():
    functions = {e["function"] for e in FULL.events}
    forbidden = {"LOCAL", "SUPERIOR", "ESTRUCTURA", "GIRO", "B_EXCESIVA", "OBSERVADOR"}
    assert not (functions & forbidden)


def test_motor_sin_hardcode_de_ventana():
    source = (ROOT / "python" / "TM_CORE_PYTHON_v075_STREAMING.py").read_text(encoding="utf-8")
    for token in ("29667.30", "29680.40", "29615.20", "16:52:32.528", "16:55:12.759"):
        assert token not in source


def test_c_grande_no_se_emite_como_candidata():
    assert any(event["function"] == "C" for event in FULL.events)
    assert "C_CAND" not in {event["kind"] for event in FULL.events}


def test_afs2_no_ready_con_fallo_de_prefijo():
    result = evaluate_afs2(FULL, prefix_failures=1)
    assert result["AFS2_READY"] is False
    assert result["checks"]["prefix_ok"] is False


def test_selftest_interno():
    selftest()
