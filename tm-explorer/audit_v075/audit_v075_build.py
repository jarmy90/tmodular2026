from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import audit_v075_common as c
import TM_CORE_PYTHON_v075_STREAMING as core

OUT = c.ROOT / "out_v075_audit2"
STEM = "v075a2"
WINDOW_START = "16:20:00.145"
WINDOW_END = "17:00:59.931"
SEQ_OFFSET = 1145


def field_row(name: str, expected, observed, match: bool, note: str = "") -> dict:
    return {
        "criterio": name,
        "esperado": expected,
        "observado": observed,
        "cumple": int(match),
        "nota": note,
    }


def common_feed_rows(rows: list[dict], lo: int, hi: int) -> list[dict]:
    return [row for row in rows if lo <= int(row["time_msc"]) <= hi]


def compare_common_feed(new_rows: list[dict], old_rows: list[dict]) -> dict:
    lo = int(old_rows[0]["time_msc"])
    hi = int(old_rows[-1]["time_msc"])
    new_common = common_feed_rows(new_rows, lo, hi)
    fields = ["time_msc", "bar_time_m1", "symbol", "bid", "ask", "spread"]
    mismatches = []
    for index in range(min(len(new_common), len(old_rows))):
        diffs = [field for field in fields if new_common[index].get(field) != old_rows[index].get(field)]
        if diffs:
            mismatches.append(
                {
                    "index": index,
                    "fields": diffs,
                    "nuevo": {field: new_common[index].get(field) for field in diffs},
                    "anterior": {field: old_rows[index].get(field) for field in diffs},
                }
            )
            if len(mismatches) >= 10:
                break
    offsets = {
        int(new_common[index]["sequence_id"]) - int(old_rows[index]["sequence_id"])
        for index in range(min(len(new_common), len(old_rows)))
    }
    return {
        "old_count": len(old_rows),
        "new_common_count": len(new_common),
        "old_first": old_rows[0].get("server_time_msc", ""),
        "old_last": old_rows[-1].get("server_time_msc", ""),
        "new_common_first": new_common[0].get("server_time_msc", "") if new_common else "",
        "new_common_last": new_common[-1].get("server_time_msc", "") if new_common else "",
        "sequence_offsets": sorted(offsets),
        "sequence_offset_unique": len(offsets) == 1,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "pass": len(new_common) == len(old_rows) and not mismatches and len(offsets) == 1,
    }


def feed_audit(new_path: Path, old_path: Path) -> dict:
    new_fields, new_rows = c.read_feed_rows(new_path)
    old_fields, old_rows = c.read_feed_rows(old_path)
    new_points, new_bars = core.load_feed(new_path)
    old_points, old_bars = core.load_feed(old_path)
    new_gaps = [(bar.name, bar.gap) for bar in new_bars.values()]
    old_gaps = [(bar.name, bar.gap) for bar in old_bars.values()]
    common = compare_common_feed(new_rows, old_rows)
    new_seq = [int(row["sequence_id"]) for row in new_rows]
    old_seq = [int(row["sequence_id"]) for row in old_rows]
    new_time = [int(row["time_msc"]) for row in new_rows]
    old_time = [int(row["time_msc"]) for row in old_rows]
    return {
        "nuevo": {
            "archivo": new_path.name,
            "sha256": c.sha256(new_path),
            "bytes": new_path.stat().st_size,
            "filas": len(new_rows),
            "columnas": new_fields,
            "primer_sequence_id": new_seq[0],
            "ultimo_sequence_id": new_seq[-1],
            "sequence_contiguo": new_seq == list(range(new_seq[0], new_seq[-1] + 1)),
            "primer_tick": new_rows[0].get("server_time_msc", ""),
            "ultimo_tick": new_rows[-1].get("server_time_msc", ""),
            "time_msc_primero": new_time[0],
            "time_msc_ultimo": new_time[-1],
            "timestamps_monotonos": all(a <= b for a, b in zip(new_time, new_time[1:])),
            "timestamps_duplicados": len(new_time) - len(set(new_time)),
            "symbols": sorted({row.get("symbol", "") for row in new_rows}),
            "velas": len(new_bars),
            "primer_vela": min(new_bars),
            "ultima_vela": max(new_bars),
            "gaps": new_gaps,
            "gaps_abs_menor_025": sum(1 for _, gap in new_gaps if 0 < abs(gap) < 25),
            "gaps_abs_igual_mayor_025": sum(1 for _, gap in new_gaps if abs(gap) >= 25),
            "gaps_cero": sum(1 for _, gap in new_gaps if gap == 0),
        },
        "anterior": {
            "archivo": old_path.name,
            "sha256": c.sha256(old_path),
            "bytes": old_path.stat().st_size,
            "filas": len(old_rows),
            "columnas": old_fields,
            "primer_sequence_id": old_seq[0],
            "ultimo_sequence_id": old_seq[-1],
            "sequence_contiguo": old_seq == list(range(old_seq[0], old_seq[-1] + 1)),
            "primer_tick": old_rows[0].get("server_time_msc", ""),
            "ultimo_tick": old_rows[-1].get("server_time_msc", ""),
            "time_msc_primero": old_time[0],
            "time_msc_ultimo": old_time[-1],
            "timestamps_monotonos": all(a <= b for a, b in zip(old_time, old_time[1:])),
            "velas": len(old_bars),
            "gaps": old_gaps,
            "gaps_abs_menor_025": sum(1 for _, gap in old_gaps if 0 < abs(gap) < 25),
            "gaps_abs_igual_mayor_025": sum(1 for _, gap in old_gaps if abs(gap) >= 25),
        },
        "tramo_comun": common,
        "puntos_cargados": {"nuevo": len(new_points), "anterior": len(old_points)},
        "pass": common["pass"]
        and len(new_points) == len(new_rows)
        and len(old_points) == len(old_rows),
    }


def map_readings(old_engine: core.Engine, full_engine: core.Engine) -> tuple[list[dict], dict[str, str], dict]:
    full_index: dict[tuple, list[core.Reading]] = defaultdict(list)
    for reading in full_engine.readings:
        full_index[c.stable_reading_key(reading)].append(reading)
    rows = []
    mapping: dict[str, str] = {}
    ambiguous = []
    for old in old_engine.readings:
        candidates = full_index.get(c.stable_reading_key(old), [])
        if not candidates:
            near = [
                reading
                for reading in full_engine.readings
                if reading.created_time == old.created_time
                and reading.module_origin == old.module_origin
                and reading.module_extreme == old.module_extreme
            ]
            candidates = near
        if len(candidates) > 1:
            ambiguous.append(old.reading_id)
        match = candidates[0] if candidates else None
        if match:
            mapping[old.reading_id] = match.reading_id
        rows.append(
            {
                "reading_id_base": old.reading_id,
                "reading_id_full": match.reading_id if match else "",
                "match": int(match is not None),
                "created_time": c.iso(old.created_time),
                "module_origin": old.module_origin,
                "module_extreme": old.module_extreme,
                "direction": "UP" if old.direction > 0 else "DOWN",
                "a_end": old.a_end,
                "b_extreme": old.b_extreme,
                "tt_target": old.tt_target,
                "ft_time": c.iso(old.ft_time) if old.ft_time else "",
                "origin_reason": old.origin_reason,
                "full_origin_reason": match.origin_reason if match else "",
                "parent_base": old.parent_reading_id,
                "parent_full": match.parent_reading_id if match else "",
            }
        )
    summary = {
        "base_readings": len(old_engine.readings),
        "full_readings": len(full_engine.readings),
        "mapped": sum(row["match"] for row in rows),
        "unmapped": [row["reading_id_base"] for row in rows if not row["match"]],
        "ambiguous": ambiguous,
    }
    return rows, mapping, summary


def compare_common_engines(old_engine: core.Engine, common_engine: core.Engine) -> dict:
    events = c.compare_events(common_engine.events, old_engine.events, SEQ_OFFSET, True)
    readings = c.compare_readings(common_engine.readings, old_engine.readings, SEQ_OFFSET)
    return {
        "events_base": len(old_engine.events),
        "events_common": len(common_engine.events),
        "readings_base": len(old_engine.readings),
        "readings_common": len(common_engine.readings),
        "event_compare": events,
        "reading_compare": readings,
        "pass": events["pass"] and readings["pass"],
    }


def r0062_audit(old_engine: core.Engine, full_engine: core.Engine, mapping: dict[str, str]) -> dict:
    old = old_engine.by_id.get("R0062")
    if old is None:
        return {"pass": False, "error": "R0062 no existe en la base"}
    full_id = mapping.get("R0062", "")
    full = full_engine.by_id.get(full_id)
    if full is None:
        return {"pass": False, "error": "R0062 base no mapeado al feed ampliado"}
    fields = [
        "direction",
        "state",
        "created_time",
        "closed_time",
        "module_origin",
        "module_extreme",
        "module_size",
        "a_origin",
        "a_end",
        "a_size",
        "b_origin",
        "b_extreme",
        "b_size",
        "tt_target",
        "tt_time",
        "tt_price",
        "tt_confirmation_time",
        "tt_knowledge_time",
        "tt_extreme",
        "ft",
        "ft_time",
        "ft_price",
        "ft_structural_time",
    ]
    rows = []
    for name in fields:
        left = getattr(old, name)
        right = getattr(full, name)
        rows.append(field_row(name, left, right, left == right, "secuencia/tiempo estructural"))
    event_fields = [
        "time_ms",
        "structural_time_ms",
        "confirmation_time_ms",
        "kind",
        "function",
        "new_state",
        "price",
        "module_origin",
        "module_extreme",
        "a_origin",
        "a_end",
        "b_origin",
        "b_extreme",
        "tt_target",
        "tt_100",
        "ft",
        "reason",
    ]
    old_events = [event for event in old_engine.events if event["reading_id"] == "R0062"]
    full_events = [event for event in full_engine.events if event["reading_id"] == full_id]
    event_diffs = []
    for index in range(min(len(old_events), len(full_events))):
        diffs = [field for field in event_fields if old_events[index].get(field) != full_events[index].get(field)]
        if diffs:
            event_diffs.append(
                {
                    "index": index,
                    "fields": diffs,
                    "base": {field: old_events[index].get(field) for field in diffs},
                    "full": {field: full_events[index].get(field) for field in diffs},
                }
            )
    critical = {
        "tt_100_time": c.iso(old.tt_time),
        "tt_100_price": core.price_s(old.tt_price),
        "b_grande_time": c.iso(old.b_grande_time),
        "tt_knowledge_time": c.iso(old.tt_knowledge_time),
        "ft_structural_time": c.iso(old.ft_structural_time),
        "ft_time": c.iso(old.ft_time),
        "module": f"{core.price_s(old.module_origin)}->{core.price_s(old.module_extreme)} X={core.price_s(old.module_size)}",
        "a": f"{core.price_s(old.a_origin)}->{core.price_s(old.a_end)} A={core.price_s(old.a_size)}",
        "b": f"{core.price_s(old.b_origin)}->{core.price_s(old.b_extreme)} B={core.price_s(old.b_size)}",
        "tt_target": core.price_s(old.tt_target),
        "full_reading_id": full_id,
        "full_module_time": c.iso(full.created_time),
        "full_tt_100_time": c.iso(full.tt_time),
        "full_b_grande_time": c.iso(full.b_grande_time),
        "full_ft_time": c.iso(full.ft_time),
    }
    return {
        "base": "R0062",
        "full": full_id,
        "mapeo_por_geometria_y_tiempo": True,
        "campos": rows,
        "campos_ok": all(row["cumple"] for row in rows),
        "eventos_base": len(old_events),
        "eventos_full": len(full_events),
        "eventos_diff": event_diffs,
        "eventos_ok": len(old_events) == len(full_events) and not event_diffs,
        "critico": critical,
        "pass": all(row["cumple"] for row in rows)
        and len(old_events) == len(full_events)
        and not event_diffs,
    }


def movement_rows(engine: core.Engine) -> list[dict]:
    rows = []
    for movement in engine.movements:
        origin = engine.points[movement.origin_index]
        extreme = engine.points[movement.extreme_index]
        confirm = engine.points[movement.confirm_index]
        geometric = [
            reading
            for reading in engine.readings
            if core._range_contains(reading, movement.origin, movement.extreme)
        ]
        causal = [
            reading
            for reading in geometric
            if core._known_by(reading, confirm.time_ms, confirm.seq)
        ]
        functional = [
            reading
            for reading in causal
            if reading.a_origin
            and reading.a_knowledge_time
            and reading.a_knowledge_time <= confirm.time_ms
        ]
        owner = min(functional or causal, key=lambda reading: (reading.created_time, reading.reading_id), default=None)
        rows.append(
            {
                "movement_index": len(rows) + 1,
                "origin": movement.origin,
                "extreme": movement.extreme,
                "direction": movement.direction,
                "size": movement.size,
                "origin_time": c.iso(origin.time_ms),
                "extreme_time": c.iso(extreme.time_ms),
                "confirm_time": c.iso(confirm.time_ms),
                "origin_seq": origin.seq,
                "extreme_seq": extreme.seq,
                "confirm_seq": confirm.seq,
                "geometric": int(bool(geometric)),
                "causal_geometric": int(bool(causal)),
                "causal_functional": int(bool(functional)),
                "owner_reading_id": owner.reading_id if owner else "",
                "owner_reason": owner.origin_reason if owner else "",
                "coverage": "FUNCIONAL" if functional else ("GEOMETRICA" if causal else "SIN_COBERTURA"),
            }
        )
    return rows


def coverage_rows(engine: core.Engine) -> tuple[list[dict], dict]:
    swings = core.structural_swings(engine.points, core.STRUCTURAL_MOVE)
    rows = []
    for index, swing in enumerate(swings, 1):
        geometric = [
            reading
            for reading in engine.readings
            if core._range_contains(reading, swing["origin"], swing["extreme"])
        ]
        functional = [reading for reading in geometric if reading.a_origin]
        causal_geometric = [
            reading
            for reading in geometric
            if core._known_by(reading, swing["confirm_time"], swing["confirm_seq"])
        ]
        causal_functional = [
            reading
            for reading in causal_geometric
            if reading.a_knowledge_time and reading.a_knowledge_time <= swing["confirm_time"]
        ]
        first_geometric = min(causal_geometric, key=lambda reading: (reading.created_time, reading.reading_id), default=None)
        first_functional = min(causal_functional, key=lambda reading: (reading.created_time, reading.reading_id), default=None)
        if causal_functional:
            reason = "CUBIERTO"
        elif not geometric:
            reason = "SIN_LECTURA_QUE_CONTE"
        elif not functional:
            reason = "A_NO_DEFINIDA"
        elif not causal_geometric:
            reason = "LECTURA_CONOCIDA_TARDE"
        else:
            reason = "A_CONOCIDA_TARDE"
        if swing["size"] < core.MOVE and reason != "CUBIERTO":
            reason = "SWING_MENOR_6_SIN_FUNCION"
        rows.append(
            {
                "swing_index": index,
                "origin": swing["origin"],
                "extreme": swing["extreme"],
                "direction": swing["direction"],
                "size": swing["size"],
                "origin_time": c.iso(swing["origin_time"]),
                "extreme_time": c.iso(swing["extreme_time"]),
                "confirm_time": c.iso(swing["confirm_time"]),
                "origin_seq": swing["origin_seq"],
                "extreme_seq": swing["extreme_seq"],
                "confirm_seq": swing["confirm_seq"],
                "geometric": int(bool(geometric)),
                "functional": int(bool(functional)),
                "causal_geometric": int(bool(causal_geometric)),
                "causal_functional": int(bool(causal_functional)),
                "covering_reading_id": first_geometric.reading_id if first_geometric else "",
                "functional_reading_id": first_functional.reading_id if first_functional else "",
                "a_knowledge_time": c.iso(first_functional.a_knowledge_time) if first_functional else "",
                "reason": reason,
                "functional_applicable": int(swing["size"] >= core.MOVE),
            }
        )
    summary = {
        "swings": len(rows),
        "geometric": sum(row["geometric"] for row in rows),
        "functional": sum(row["functional"] for row in rows),
        "causal_geometric": sum(row["causal_geometric"] for row in rows),
        "causal_functional": sum(row["causal_functional"] for row in rows),
        "causal_geometric_uncovered": sum(1 - row["causal_geometric"] for row in rows),
        "causal_functional_uncovered": sum(1 - row["causal_functional"] for row in rows),
        "functional_applicable": sum(row["functional_applicable"] for row in rows),
        "functional_applicable_causal": sum(
            row["causal_functional"] for row in rows if row["functional_applicable"]
        ),
        "reasons": dict(Counter(row["reason"] for row in rows)),
    }
    return rows, summary


def owner_rows(engine: core.Engine) -> tuple[list[dict], dict]:
    rows = []
    by_seq = {point.seq: point for point in engine.points}
    previous_price = None
    first_reading_time = min((reading.created_time for reading in engine.readings), default=0)
    for audit in engine.knowledge_audit:
        point = by_seq.get(audit["sequence_id"])
        uncovered = audit["functional_coverage"] == "UNCOVERED"
        if not uncovered:
            previous_price = point.price if point else previous_price
            continue
        active = [item for item in audit["active_readings"].split(";") if item]
        if not active:
            if point and point.time_ms < first_reading_time:
                reason = "PRE_LECTURA"
            else:
                reason = "SIN_LECTURA_ACTIVA"
        elif point is not None and previous_price is not None and abs(point.price - previous_price) < core.STRUCTURAL_MOVE:
            reason = "RUIDO_MENOR_2"
        else:
            reason = "MOVIMIENTO_ESTRUCTURAL_SIN_OWNER"
        if point and active:
            inside = False
            for reading_id in active:
                reading = engine.by_id.get(reading_id)
                if reading is None:
                    continue
                if min(reading.module_origin, reading.module_extreme) <= point.price <= max(
                    reading.module_origin, reading.module_extreme
                ):
                    inside = True
                    break
            if not inside:
                reason = "PRECIO_FUERA_RANGO_ACTIVO"
        rows.append(
            {
                "sequence_id": audit["sequence_id"],
                "time": audit["time"],
                "price": audit["price"],
                "bar_time": audit["bar_time"],
                "owner_source": audit["owner_source"],
                "active_readings": audit["active_readings"],
                "local_direction": audit["local_direction"],
                "excursion": audit["excursion"],
                "reason": reason,
            }
        )
        previous_price = point.price if point else previous_price
    summary = {
        "ticks": len(engine.knowledge_audit),
        "owner_ok": engine.coverage["owner_tick_count"],
        "uncovered": len(rows),
        "noise": engine.coverage["noise_tick_count"],
        "reasons": dict(Counter(row["reason"] for row in rows)),
    }
    return rows, summary


def golden_rows(engine: core.Engine) -> tuple[list[dict], dict]:
    narrative = {row["bar_time"]: row for row in engine.narrative}
    events_by_bar = defaultdict(list)
    for event in engine.events:
        events_by_bar[event["bar_time"]].append(event)
    readings_by_bar = defaultdict(list)
    for reading in engine.readings:
        readings_by_bar[c.hms(reading.created_time)[:5]].append(reading)
    expected = {
        "16:15": "CONFIRMADA; modulo 29877.00->29860.80; X=16.20; sin plano",
        "16:16": "PLANO +0.10; sin cola superior; recorrido 29861.10->29848.50=12.60 < 16.20; modulo por descarte; modulo conjunto 29877.00->29848.50 X=28.50",
        "16:17": "NO PLANO +0.70; A Grande 29848.50->29857.60 A=9.10; despues B bajista",
        "16:18": "max 29857.40 seq 740 no extiende A; min 29843.00 seq 923; AUT bajista; TT pendiente 29829.10",
        "16:19": "continuacion bajista AUT; max 29850.00 min 29842.50; lectura local en revision",
        "16:20": "PLANO -0.20; abre en maximo y baja; si 16:19=1 entonces 16:20=2 valido",
        "16:21": "NO PLANO -1.00; nuevo minimo 29830.30; posible 3; el gap no invalida el 2 previo",
        "16:22": "NO PLANO +0.50; A Grande alcista 29830.30->29850.80 A=20.50; AUT alcista NO confirmado; no supera 29877.00",
    }
    rows = []
    for bar_time in [f"16:{minute:02d}" for minute in range(15, 23)]:
        row = narrative.get(bar_time, {})
        events = events_by_bar.get(bar_time, [])
        funcs = c.functions_text(events)
        gap_events = [event for event in events if event["kind"] == "GAP"]
        gap = row.get("gap", 0)
        a_events = [event for event in events if event["function"] in ("A", "A_EXT")]
        b_grande = [event for event in events if event["function"] == "B_GRANDE"]
        aut = [event for event in events if event["function"] == "AUT"]
        tt = [event for event in events if event["function"] == "TT"]
        created = readings_by_bar.get(bar_time, [])
        observed_parts = [
            f"OHLC {core.price_s(row.get('open', 0))}/{core.price_s(row.get('high', 0))}/"
            f"{core.price_s(row.get('low', 0))}/{core.price_s(row.get('close', 0))}",
            f"gap={core.price_s(gap)}",
            f"funciones={funcs or 'NINGUNA'}",
            f"lecturas_creadas={','.join(reading.reading_id for reading in created) or 'NINGUNA'}",
        ]
        if gap_events:
            observed_parts.append(f"GAP_evento={c.hms(gap_events[0]['time_ms'])}")
        if a_events:
            event = a_events[-1]
            observed_parts.append(
                f"A={core.price_s(event['a_origin'])}->{core.price_s(event['a_end'])}"
            )
        if b_grande:
            observed_parts.append(f"B_GRANDE={c.hms(b_grande[0]['time_ms'])}")
        if aut:
            observed_parts.append(f"AUT={c.hms(aut[0]['time_ms'])}")
        if tt:
            observed_parts.append(f"TT={c.hms(tt[0]['time_ms'])} target={core.price_s(tt[0]['tt_target'])}")
        observed = "; ".join(observed_parts)
        match = False
        note = ""
        if bar_time == "16:15":
            created_15 = [
                reading
                for reading in created
                if reading.module_origin == core.price_i(29877.00)
                and reading.module_extreme == core.price_i(29860.80)
            ]
            match = bool(created_15)
            note = "No se emite lectura en 16:15; R0001 nace en 16:16 con el modulo conjunto 29877.00->29848.50."
        elif bar_time == "16:16":
            match = (
                abs(gap) < 25
                and not gap_events
                and any(
                    reading.module_origin == core.price_i(29877.00)
                    and reading.module_extreme == core.price_i(29848.50)
                    for reading in created
                )
            )
            note = "El motor emite GAP por +0.10 y no emite PLANO; la geometria conjunta si coincide."
        elif bar_time == "16:17":
            reading = next((reading for reading in created if reading.reading_id == "R0001"), None)
            a_end_at_bar = a_events[-1]["a_end"] if a_events else 0
            match = bool(reading) and a_end_at_bar == core.price_i(29857.60) and reading.a_size == core.price_i(9.10)
            note = "A se emite inicialmente hasta 29856.30; se extiende a 29857.60 solo al confirmar B_FALLIDA en 16:18."
        elif bar_time == "16:18":
            high_ok = any(
                point.price == core.price_i(29857.40) and point.seq == 740
                for point in engine.points
                if point.time_ms // 60000 == core.parse_hms("16:18", engine.start_time) // 60000
            )
            low_ok = any(
                point.price == core.price_i(29843.00) and point.seq == 923
                for point in engine.points
                if point.time_ms // 60000 == core.parse_hms("16:18", engine.start_time) // 60000
            )
            match = high_ok and low_ok and bool(aut) and bool(b_grande)
            note = "AUT y B Grande coinciden; TT queda pendiente en 29829.10."
        elif bar_time == "16:19":
            match = False
            note = "El motor emite C y A alcistas; la lectura humana pide continuacion bajista y lectura local en revision."
        elif bar_time == "16:20":
            match = False
            note = "El motor emite GAP por -0.20 y no reconoce el 2 alternativo."
        elif bar_time == "16:21":
            match = False
            note = "El motor solo emite GAP; no reconoce el posible 3."
        elif bar_time == "16:22":
            has_up_a = any(
                event["function"] in ("A", "A_EXT")
                and event["a_origin"] == core.price_i(29830.30)
                and event["a_end"] == core.price_i(29850.80)
                for event in events
            )
            match = has_up_a
            note = "El motor no forma A Grande alcista desde 29830.30 en 16:22; emite AUT/TT sobre una lectura bajista distinta."
        rows.append(
            {
                "bar_time": bar_time,
                "esperado": expected[bar_time],
                "observado": observed,
                "cumple": int(match),
                "nota": note,
            }
        )
    summary = {
        "bars": len(rows),
        "match": sum(row["cumple"] for row in rows),
        "mismatch": sum(1 - row["cumple"] for row in rows),
        "rows": rows,
    }
    return rows, summary


def gap_plano_rows(engine: core.Engine) -> tuple[list[dict], dict]:
    rows = []
    for bar in engine.bars.values():
        gap_events = c.bar_gap_events(engine, bar.idx)
        if bar.gap == 0:
            expected = "SIN_CAMBIO"
            should_emit = False
        elif abs(bar.gap) < 25:
            expected = "PLANO_NO_GAP"
            should_emit = False
        else:
            expected = "GAP"
            should_emit = True
        observed = "GAP" if gap_events else "NO_GAP"
        match = should_emit == bool(gap_events)
        rows.append(
            {
                "bar_time": bar.name,
                "gap": bar.gap,
                "abs_gap": abs(bar.gap),
                "esperado": expected,
                "observado": observed,
                "evento": c.hms(gap_events[0]["time_ms"]) if gap_events else "",
                "cumple": int(match),
                "nota": "0.25 o mas no es plano" if expected == "GAP" else "menor de 0.25 se absorbe como plano",
            }
        )
    summary = {
        "bars": len(rows),
        "expected_gap": sum(row["esperado"] == "GAP" for row in rows),
        "observed_gap": sum(row["observado"] == "GAP" for row in rows),
        "false_gap": sum(row["esperado"] != "GAP" and row["observado"] == "GAP" for row in rows),
        "missed_gap": sum(row["esperado"] == "GAP" and row["observado"] != "GAP" for row in rows),
        "match": sum(row["cumple"] for row in rows),
        "failures": [row for row in rows if not row["cumple"]],
    }
    return rows, summary


def boundary_rows(engine: core.Engine) -> tuple[list[dict], dict]:
    rows = []
    point_by_seq = {point.seq: point for point in engine.points}
    for reading in engine.readings:
        if not reading.a_origin or not reading.a_end or not reading.b_origin:
            continue
        direction = reading.direction
        b_limit = reading.b_origin + direction * reading.a_size
        aut_limit = reading.b_origin + direction * ((core.AUT_NUM * reading.a_size) // core.AUT_DEN + core.AUT_EXTRA)
        start = point_by_seq.get(reading.b_origin_seq)
        end = point_by_seq.get(reading.b_extreme_seq)
        if start is None or end is None:
            continue
        start_index = engine.points.index(start)
        end_index = engine.points.index(end)
        leg = engine.points[start_index : end_index + 1]
        b_cross = next(
            (
                point
                for point in leg
                if (direction > 0 and point.price >= b_limit)
                or (direction < 0 and point.price <= b_limit)
            ),
            None,
        )
        aut_cross = next(
            (
                point
                for point in leg
                if (direction > 0 and point.price >= aut_limit)
                or (direction < 0 and point.price <= aut_limit)
            ),
            None,
        )
        rows.append(
            {
                "reading_id": reading.reading_id,
                "direction": "UP" if direction > 0 else "DOWN",
                "x": reading.module_size,
                "a": reading.a_size,
                "b": reading.b_size,
                "b_origin": reading.b_origin,
                "b_limit_100": b_limit,
                "b_cross_time": c.iso(b_cross.time_ms) if b_cross else "",
                "b_cross_price": b_cross.price if b_cross else 0,
                "b_grande_time": c.iso(reading.b_grande_time) if reading.b_grande_time else "",
                "b_grande_ok": int(reading.b_size >= reading.a_size and bool(reading.b_grande_time)),
                "aut_limit": aut_limit,
                "aut_cross_time": c.iso(aut_cross.time_ms) if aut_cross else "",
                "aut_cross_price": aut_cross.price if aut_cross else 0,
                "aut_time": c.iso(reading.aut_time) if reading.aut_time else "",
                "aut_expected": int(reading.b_size > aut_limit),
                "aut_observed": int(bool(reading.aut_time)),
                "aut_match": int((reading.b_size > aut_limit) == bool(reading.aut_time)),
                "b_extra_over_aut": core.price_s(max(0, reading.b_size - aut_limit)),
            }
        )
    summary = {
        "rows": len(rows),
        "b_grande_ok": sum(row["b_grande_ok"] for row in rows),
        "aut_match": sum(row["aut_match"] for row in rows),
        "aut_expected": sum(row["aut_expected"] for row in rows),
        "aut_observed": sum(row["aut_observed"] for row in rows),
    }
    return rows, summary


def reclassification_rows(engine: core.Engine) -> list[dict]:
    kinds = {
        "AUT",
        "B_FALLIDA",
        "B_OSCILACION",
        "C_CANCELADA",
        "ARCHIVADA",
        "A_DESPROPORCIONADA_MODULO",
        "TT_100",
        "FT",
        "CUT",
        "C",
    }
    rows = []
    for event in engine.events:
        if event["kind"] not in kinds and event["function"] not in kinds:
            continue
        rows.append(
            {
                "event_id": event["event_id"],
                "time": event["time"],
                "sequence_id": event["sequence_id"],
                "reading_id": event["reading_id"],
                "kind": event["kind"],
                "function": event["function"],
                "new_state": event["new_state"],
                "reason": event["reason"],
                "module_range": f"{core.price_s(event['module_origin'])}->{core.price_s(event['module_extreme'])}",
                "a_range": f"{core.price_s(event['a_origin'])}->{core.price_s(event['a_end'])}",
                "b_range": f"{core.price_s(event['b_origin'])}->{core.price_s(event['b_extreme'])}",
                "tt_target": event["tt_target"],
                "tt_100": event["tt_100"],
                "ft": event["ft"],
            }
        )
    return rows


def ft_state_rows(engine: core.Engine) -> tuple[list[dict], dict]:
    allowed = {
        "FT_CANDIDATE",
        "FT_CONFIRMED",
        "FT_CANDIDATE_ABSORBED_BY_TT_EXTENSION",
        "FT_REJECTED_AS_NOISE",
        "FT_WINDOW_EXPIRED",
        "FT_MISSED_OPERATIVELY",
    }
    rows = []
    for pattern in engine.patterns:
        if pattern["type"] != "FT":
            continue
        rows.append(
            {
                "pattern_id": pattern["pattern_id"],
                "reading_id": pattern["reading_id"],
                "status": pattern["status"],
                "final_status": pattern["final_status"],
                "direction": pattern["direction"],
                "size": pattern["size"],
                "canonical": int(pattern["final_status"] in allowed),
            }
        )
    summary = {
        "ft_patterns": len(rows),
        "canonical": sum(row["canonical"] for row in rows),
        "non_canonical": [row for row in rows if not row["canonical"]][:20],
        "allowed": sorted(allowed),
        "pass": bool(rows) and all(row["canonical"] for row in rows),
    }
    return rows, summary


def invariants(engine: core.Engine, feed: dict, regression: dict, r0062: dict, golden: dict, gap: dict, ft: dict) -> dict:
    expected_ids = [f"E{index:06d}" for index in range(1, len(engine.events) + 1)]
    event_ids = [event["event_id"] for event in engine.events]
    knowledge_valid = all(
        event["knowledge_time_ms"] >= event["confirmation_time_ms"]
        and event["knowledge_time_ms"] >= event["structural_time_ms"]
        for event in engine.events
    )
    sequence_valid = all(
        event["sequence_id"] == event["knowledge_sequence_id"] for event in engine.events
    ) and all(event["sequence_id"] in {point.seq for point in engine.points} for event in engine.events)
    tt_valid = all(
        (not reading.tt_hit)
        or (
            reading.b_grande_time
            and reading.tt_knowledge_time >= reading.b_grande_time
            and reading.b_size >= reading.a_size
        )
        for reading in engine.readings
    )
    target_valid = all(
        (not reading.tt_hit) or reading.tt_target == reading.a_end + reading.direction * reading.module_size
        for reading in engine.readings
    )
    gap_order = True
    by_seq = defaultdict(list)
    for event in engine.events:
        by_seq[event["sequence_id"]].append(event)
    for bar in engine.bars.values():
        if bar.gap == 0:
            continue
        first = next((point for point in engine.points if point.bar == bar.idx), None)
        if first is None:
            continue
        events = by_seq[first.seq]
        if not events or events[0]["kind"] != "GAP":
            gap_order = False
            break
    forbidden = core.FORBIDDEN_FUNCTIONS & {event["function"] for event in engine.events}
    coverage = engine.coverage
    unexplained = coverage["structural_swing_count"] - coverage["causal_functional_count"]
    pending_rule = any(
        event["kind"] == "PENDIENTE_POR_REGLA"
        and event["reason"] == "UNEXPLAINED_STRUCTURAL_MOVE"
        for event in engine.events
    )
    final_ok = unexplained == 0 or pending_rule
    return {
        "feed_carga_ok": feed["pass"],
        "event_id_append_only": event_ids == expected_ids,
        "sequence_id_real": sequence_valid,
        "knowledge_time_valido": knowledge_valid,
        "tt_despues_b_grande": tt_valid,
        "tt_target_formula": target_valid,
        "gap_primero_en_su_tick": gap_order,
        "vocabulario_limpio": not forbidden,
        "owner_audit_completo": len(engine.knowledge_audit) == len(engine.points),
        "owner_reading_conocida": all(
            (not row["owner_reading_id"]) or row["owner_known_at_seq"] <= row["sequence_id"]
            for row in engine.knowledge_audit
        ),
        "regresion_tramo_comun_exacta": regression.get("pass", False),
        "r0062_geometria_exacta": r0062.get("pass", False),
        "golden_16_15_16_22_completo": golden.get("mismatch", 1) == 0,
        "plano_gap_regla_canonica": gap.get("false_gap", 1) == 0 and gap.get("missed_gap", 0) == 0,
        "ft_estados_finales_canonicos": ft.get("pass", False),
        "integridad_fin_feed": final_ok,
        "unexplained_structural_moves": unexplained,
        "unexplained_structural_moves_sin_pendiente": unexplained if not pending_rule else 0,
        "forbidden_functions": sorted(forbidden),
    }


def write_gap_plano_markdown(path: Path, summary: dict) -> None:
    lines = [
        "# Regla de plano y GAP",
        "",
        "La correccion confirmada por Javier exige: `|apertura - cierre anterior| < 0,25` es plano;",
        "`0,25` exacto o superior no es plano. Por tanto no debe emitirse `GAP` para 0,10 o 0,20.",
        "",
        f"- Velas: `{summary['bars']}`.",
        f"- GAP esperados: `{summary['expected_gap']}`; GAP observados: `{summary['observed_gap']}`.",
        f"- Falsos GAP: `{summary['false_gap']}`; GAP omitidos: `{summary['missed_gap']}`.",
        f"- Velas conformes: `{summary['match']}/{summary['bars']}`.",
        "",
        "## Falsos GAP",
        "",
    ]
    for row in summary["failures"]:
        lines.append(
            f"- `{row['bar_time']}` gap `{core.price_s(row['gap'])}` "
            f"esperado `{row['esperado']}` observado `{row['observado']}`"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Genera artefactos audit2 v0.7.5")
    parser.add_argument("--feed", type=Path, default=c.FEED)
    parser.add_argument("--old-feed", type=Path, default=c.OLD_FEED)
    parser.add_argument("--old-out", type=Path, default=c.OLD_OUT)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--stem", default=STEM)
    args = parser.parse_args(argv)
    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    feed = feed_audit(args.feed, args.old_feed)
    new_points, new_bars = core.load_feed(args.feed)
    old_points, old_bars = core.load_feed(args.old_feed)
    old_engine = core.run_engine(old_points, old_bars)
    full_engine = core.run_engine(new_points, new_bars)
    core.write_outputs(full_engine, out, args.stem)

    lo = core.parse_hms(WINDOW_START, new_points[0].time_ms)
    hi = core.parse_hms(WINDOW_END, new_points[0].time_ms)
    common_points = [point for point in new_points if lo <= point.time_ms <= hi]
    common_bars = c.build_bars(common_points)
    common_engine = core.run_engine(common_points, common_bars)
    cli_common_points = [point for point in new_points if lo <= point.time_ms <= hi]
    cli_common_engine = core.run_engine(cli_common_points, new_bars)

    regression = compare_common_engines(old_engine, common_engine)
    regression["common_strict"] = {
        "points": len(common_points),
        "bars": len(common_bars),
        "readings": len(common_engine.readings),
        "events": len(common_engine.events),
        "movements": len(common_engine.movements),
    }
    regression["cli_con_barras_completas"] = {
        "points": len(cli_common_points),
        "bars": len(new_bars),
        "readings": len(cli_common_engine.readings),
        "events": len(cli_common_engine.events),
        "movements": len(cli_common_engine.movements),
        "gap_16_20": [
            event
            for event in cli_common_engine.events
            if event["kind"] == "GAP" and event["bar_time"] == "16:20"
        ],
    }
    regression["pass"] = regression["event_compare"]["pass"] and regression["reading_compare"]["pass"]
    c.write_json(out / "A02_RegresionTramoComun.json", regression)

    mapping_rows, mapping, mapping_summary = map_readings(old_engine, full_engine)
    c.write_csv(
        out / "A03_CorrespondenciaIDs.csv",
        [
            "reading_id_base",
            "reading_id_full",
            "match",
            "created_time",
            "module_origin",
            "module_extreme",
            "direction",
            "a_end",
            "b_extreme",
            "tt_target",
            "ft_time",
            "origin_reason",
            "full_origin_reason",
            "parent_base",
            "parent_full",
        ],
        mapping_rows,
    )
    c.write_json(out / "A03_CorrespondenciaIDs.json", mapping_summary)

    r0062 = r0062_audit(old_engine, full_engine, mapping)
    c.write_json(out / "A09_R0062.json", r0062)

    movements = movement_rows(full_engine)
    c.write_csv(
        out / "A04_Movimientos.csv",
        [
            "movement_index",
            "origin",
            "extreme",
            "direction",
            "size",
            "origin_time",
            "extreme_time",
            "confirm_time",
            "origin_seq",
            "extreme_seq",
            "confirm_seq",
            "geometric",
            "causal_geometric",
            "causal_functional",
            "owner_reading_id",
            "owner_reason",
            "coverage",
        ],
        movements,
    )

    cover, cover_summary = coverage_rows(full_engine)
    c.write_csv(
        out / "A05_CoberturaSwings.csv",
        [
            "swing_index",
            "origin",
            "extreme",
            "direction",
            "size",
            "origin_time",
            "extreme_time",
            "confirm_time",
            "origin_seq",
            "extreme_seq",
            "confirm_seq",
            "geometric",
            "functional",
            "causal_geometric",
            "causal_functional",
            "covering_reading_id",
            "functional_reading_id",
            "a_knowledge_time",
            "reason",
            "functional_applicable",
        ],
        cover,
    )
    movement_cover_summary = {
        "movements": len(movements),
        "geometric": sum(row["geometric"] for row in movements),
        "causal_geometric": sum(row["causal_geometric"] for row in movements),
        "causal_functional": sum(row["causal_functional"] for row in movements),
        "uncovered": [row for row in movements if not row["causal_functional"]],
    }
    c.write_csv(
        out / "A06_CoberturaMovimientos.csv",
        [
            "movement_index",
            "origin",
            "extreme",
            "direction",
            "size",
            "origin_time",
            "extreme_time",
            "confirm_time",
            "origin_seq",
            "extreme_seq",
            "confirm_seq",
            "geometric",
            "causal_geometric",
            "causal_functional",
            "owner_reading_id",
            "coverage",
        ],
        movements,
    )
    c.write_json(out / "A06_CoberturaMovimientos.json", movement_cover_summary)

    uncovered, owner_summary = owner_rows(full_engine)
    c.write_csv(
        out / "A07_TicksSinOwner.csv",
        [
            "sequence_id",
            "time",
            "price",
            "bar_time",
            "owner_source",
            "active_readings",
            "local_direction",
            "excursion",
            "reason",
        ],
        uncovered,
    )
    c.write_json(out / "A07_TicksSinOwner.json", owner_summary)

    golden, golden_summary = golden_rows(full_engine)
    c.write_csv(
        out / "A08_LecturasGolden.csv",
        ["bar_time", "esperado", "observado", "cumple", "nota"],
        golden,
    )
    c.write_json(out / "A08_LecturasGolden.json", golden_summary)

    gap_rows, gap_summary = gap_plano_rows(full_engine)
    c.write_csv(
        out / "A11_PlanoGap.csv",
        ["bar_time", "gap", "abs_gap", "esperado", "observado", "evento", "cumple", "nota"],
        gap_rows,
    )
    c.write_json(out / "A11_PlanoGap.json", gap_summary)
    write_gap_plano_markdown(out / "A11_PlanoGap.md", gap_summary)

    boundaries, boundary_summary = boundary_rows(full_engine)
    c.write_csv(
        out / "A10_FronterasAUTB.csv",
        [
            "reading_id",
            "direction",
            "x",
            "a",
            "b",
            "b_origin",
            "b_limit_100",
            "b_cross_time",
            "b_cross_price",
            "b_grande_time",
            "b_grande_ok",
            "aut_limit",
            "aut_cross_time",
            "aut_cross_price",
            "aut_time",
            "aut_expected",
            "aut_observed",
            "aut_match",
            "b_extra_over_aut",
        ],
        boundaries,
    )
    c.write_json(out / "A10_FronterasAUTB.json", boundary_summary)

    reclass = reclassification_rows(full_engine)
    c.write_csv(
        out / "A12_Reclasificaciones.csv",
        [
            "event_id",
            "time",
            "sequence_id",
            "reading_id",
            "kind",
            "function",
            "new_state",
            "reason",
            "module_range",
            "a_range",
            "b_range",
            "tt_target",
            "tt_100",
            "ft",
        ],
        reclass,
    )

    ft_rows, ft_summary = ft_state_rows(full_engine)
    c.write_csv(
        out / "A22_FTEstados.csv",
        ["pattern_id", "reading_id", "status", "final_status", "direction", "size", "canonical"],
        ft_rows,
    )
    c.write_json(out / "A22_FTEstados.json", ft_summary)

    inv = invariants(full_engine, feed, regression, r0062, golden_summary, gap_summary, ft_summary)
    inv["motor"] = {
        "version": core.VERSION,
        "readings": len(full_engine.readings),
        "events": len(full_engine.events),
        "movements": len(full_engine.movements),
        "patterns": len(full_engine.patterns),
        "active_readings": len(full_engine.active),
        "pending": full_engine.pending,
        "coverage": full_engine.coverage,
    }
    c.write_json(out / "A13_Invariantes.json", inv)

    coverage_summary = {
        "motor": {
            "structural_swing_count": full_engine.coverage["structural_swing_count"],
            "geometric_count": full_engine.coverage["geometric_count"],
            "functional_count": full_engine.coverage["functional_count"],
            "causal_geometric_count": full_engine.coverage["causal_geometric_count"],
            "causal_functional_count": full_engine.coverage["causal_functional_count"],
            "movement_count": full_engine.coverage["movement_count"],
            "causal_functional_movement_count": full_engine.coverage["causal_functional_movement_count"],
            "owner_tick_count": full_engine.coverage["owner_tick_count"],
            "uncovered_tick_count": full_engine.coverage["uncovered_tick_count"],
            "tick_count": full_engine.coverage["tick_count"],
        },
        "swings": cover_summary,
        "movements": {
            key: value for key, value in movement_cover_summary.items() if key != "uncovered"
        },
        "owner": owner_summary,
        "uncovered_swing_reasons": cover_summary["reasons"],
    }
    c.write_json(out / "A15_ResumenCobertura.json", coverage_summary)
    c.write_csv(
        out / "A15_CoberturaSwingsNoCubiertos.csv",
        [
            "swing_index",
            "origin",
            "extreme",
            "direction",
            "size",
            "origin_time",
            "extreme_time",
            "confirm_time",
            "reason",
            "covering_reading_id",
            "functional_reading_id",
        ],
        [row for row in cover if not row["causal_functional"]],
    )

    feed["pass"] = bool(feed["pass"])
    c.write_json(out / "A01_FeedAuditoria.json", feed)

    summary = {
        "version": core.VERSION,
        "feed": {
            "nuevo_filas": feed["nuevo"]["filas"],
            "nuevo_velas": feed["nuevo"]["velas"],
            "anterior_filas": feed["anterior"]["filas"],
            "anterior_velas": feed["anterior"]["velas"],
            "tramo_comun": feed["tramo_comun"],
        },
        "motor": {
            "readings": len(full_engine.readings),
            "events": len(full_engine.events),
            "movements": len(full_engine.movements),
            "patterns": len(full_engine.patterns),
            "active_readings": len(full_engine.active),
        },
        "regresion": {
            "pass": regression["pass"],
            "events_base": regression["events_base"],
            "events_common": regression["events_common"],
            "event_mismatch": regression["event_compare"]["mismatch_count"],
            "reading_mismatch": regression["reading_compare"]["mismatch_count"],
            "cli_events": regression["cli_con_barras_completas"]["events"],
        },
        "mapeo": mapping_summary,
        "r0062": {
            "pass": r0062.get("pass", False),
            "base": r0062.get("base"),
            "full": r0062.get("full"),
            "eventos_base": r0062.get("eventos_base"),
            "eventos_full": r0062.get("eventos_full"),
            "eventos_diff": len(r0062.get("eventos_diff", [])),
        },
        "golden": golden_summary,
        "gap": gap_summary,
        "coverage": coverage_summary,
        "ft": ft_summary,
        "invariantes": inv,
    }
    c.write_json(out / "A00_Resumen.json", summary)

    print(f"audit2 build: readings={len(full_engine.readings)} events={len(full_engine.events)}")
    print(f"feed pass={feed['pass']} regression pass={regression['pass']} r0062 pass={r0062.get('pass')}")
    print(f"golden match={golden_summary['match']}/{golden_summary['bars']} gap false={gap_summary['false_gap']}")
    print(f"coverage causal functional={cover_summary['causal_functional']}/{cover_summary['swings']} owner uncovered={owner_summary['uncovered']}")
    print(f"outputs={out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
