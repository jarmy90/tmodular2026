"""Reportes v0.7.5: prefijos, causalidad y AFS2."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from TM_CORE_PYTHON_v075_STREAMING import (
    Engine,
    STRUCTURAL_MOVE,
    _known_by,
    _range_contains,
    ms_to_text,
    price_s,
    structural_swings,
)


def causal_coverage_rows(engine: Engine) -> list[dict]:
    rows: list[dict] = []
    for swing in structural_swings(engine.points, STRUCTURAL_MOVE):
        geometric = [
            r
            for r in engine.readings
            if _range_contains(r, swing["origin"], swing["extreme"])
        ]
        functional = [r for r in geometric if r.a_origin]
        causal_geometric = [
            r
            for r in geometric
            if _known_by(r, swing["confirm_time"], swing["confirm_seq"])
        ]
        causal_functional = [
            r
            for r in causal_geometric
            if r.a_knowledge_time and r.a_knowledge_time <= swing["confirm_time"]
        ]
        first_geometric = min(causal_geometric, key=lambda r: (r.created_time, r.reading_id), default=None)
        first_functional = min(causal_functional, key=lambda r: (r.created_time, r.reading_id), default=None)
        if causal_functional:
            reason = "CUBIERTO"
        elif causal_geometric:
            reason = "A_NO_CONOCIDA"
        else:
            reason = "SIN_LECTURA_CONOCIDA"
        rows.append(
            {
                "swing_origin": price_s(swing["origin"]),
                "swing_extreme": price_s(swing["extreme"]),
                "direction": swing["direction"],
                "size": price_s(swing["size"]),
                "origin_time": ms_to_text(swing["origin_time"]),
                "extreme_time": ms_to_text(swing["extreme_time"]),
                "confirm_time": ms_to_text(swing["confirm_time"]),
                "confirm_seq": swing["confirm_seq"],
                "geometric": int(bool(geometric)),
                "functional": int(bool(functional)),
                "causal_geometric": int(bool(causal_geometric)),
                "causal_functional": int(bool(causal_functional)),
                "covering_reading_id": first_geometric.reading_id if first_geometric else "",
                "functional_reading_id": first_functional.reading_id if first_functional else "",
                "a_knowledge_time": ms_to_text(first_functional.a_knowledge_time)
                if first_functional and first_functional.a_knowledge_time
                else "",
                "reason": reason,
            }
        )
    return rows


def write_prefix_matrix(rows: list[dict], out_dir: Path | str, stem: str = "v075") -> list[Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"{stem}_PrefixMatrix.csv"
    json_path = out_dir / f"{stem}_PrefixMatrix.json"
    fields = [
        "cutoff_time",
        "cutoff_ms",
        "full_events",
        "prefix_events",
        "full_readings",
        "prefix_readings",
        "pass",
        "mismatch_index",
        "mismatch_fields",
    ]
    with csv_path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            mismatch = row.get("mismatch") or {}
            writer.writerow(
                {
                    "cutoff_time": row.get("cutoff_time", ""),
                    "cutoff_ms": row.get("cutoff_ms", ""),
                    "full_events": row.get("full_events", ""),
                    "prefix_events": row.get("prefix_events", ""),
                    "full_readings": row.get("full_readings", ""),
                    "prefix_readings": row.get("prefix_readings", ""),
                    "pass": int(bool(row.get("pass"))),
                    "mismatch_index": mismatch.get("index", ""),
                    "mismatch_fields": ";".join(mismatch.get("fields", [])),
                }
            )
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    return [csv_path, json_path]


def write_causal_coverage(engine: Engine, out_dir: Path | str, stem: str = "v075") -> list[Path]:
    rows = causal_coverage_rows(engine)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"{stem}_CoberturaCausal.csv"
    summary_path = out_dir / f"{stem}_CoberturaCausal.json"
    fields = [
        "swing_origin",
        "swing_extreme",
        "direction",
        "size",
        "origin_time",
        "extreme_time",
        "confirm_time",
        "confirm_seq",
        "geometric",
        "functional",
        "causal_geometric",
        "causal_functional",
        "covering_reading_id",
        "functional_reading_id",
        "a_knowledge_time",
        "reason",
    ]
    with csv_path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "rows": len(rows),
        "geometric_count": sum(int(row["geometric"]) for row in rows),
        "functional_count": sum(int(row["functional"]) for row in rows),
        "causal_geometric_count": sum(int(row["causal_geometric"]) for row in rows),
        "causal_functional_count": sum(int(row["causal_functional"]) for row in rows),
        "uncovered_causal_geometric": sum(int(not row["causal_geometric"]) for row in rows),
        "uncovered_causal_functional": sum(int(not row["causal_functional"]) for row in rows),
        "reasons": {
            reason: sum(1 for row in rows if row["reason"] == reason)
            for reason in sorted({row["reason"] for row in rows})
        },
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return [csv_path, summary_path]


def _pct(value: int, total: int) -> str:
    return f"{(100.0 * value / total):.2f}%" if total else "n/a"


def build_causal_report(engine: Engine, prefix_rows: list[dict]) -> str:
    coverage = engine.coverage
    key = next(
        (
            r
            for r in reversed(engine.readings)
            if r.tt_hit and r.tt_time and r.b_grande_time and r.tt_time < r.b_grande_time
        ),
        None,
    )
    failures = [row for row in prefix_rows if not row.get("pass")]
    lines = [
        "# Informe de causalidad v0.7.5",
        "",
        "## Resolucion del hallazgo",
        "",
    ]
    if key:
        lines += [
            f"- Lectura: `{key.reading_id}`.",
            f"- `TT` objetivo: `{price_s(key.tt_target)}`; primer cruce estructural: "
            f"`{price_s(key.tt_price)}` a `{ms_to_text(key.tt_time)}`.",
            f"- `B Grande` confirmada: `{ms_to_text(key.b_grande_time)}`.",
            f"- `TT` conocimiento: `{ms_to_text(key.tt_knowledge_time)}`.",
            "- El evento `TT` conserva el tiempo estructural del cruce, pero se emite con el "
            "`knowledge_time` de B Grande. Un prefijo fisico anterior a B Grande no puede contenerlo.",
            "",
        ]
    else:
        lines += [
            "- No se encontro una lectura con TT estructural anterior a B Grande.",
            "",
        ]
    lines += [
        "## Invariantes medidos",
        "",
        f"- Eventos: `{len(engine.events)}`; lecturas: `{len(engine.readings)}`; "
        f"movimientos: `{len(engine.movements)}`.",
        f"- `knowledge_time >= structural_time`: "
        f"`{engine.afs2['checks']['knowledge_time_valid']}`.",
        f"- `event_id` append-only: `{engine.afs2['checks']['event_id_append_only']}`.",
        f"- `sequence_id` real del feed: `{engine.afs2['checks']['sequence_id_real_feed']}`.",
        f"- TT solo despues de B Grande: `{engine.afs2['checks']['tt_after_b_grande']}`.",
        f"- Formula TT: `{engine.afs2['checks']['tt_target_formula']}`.",
        f"- GAP antes de otras ramas: `{engine.afs2['checks']['gap_before_other_branches']}`.",
        f"- Geometria generica preservada: `{engine.afs2['checks']['geometry_invariants']}`.",
        "",
        "## Matriz de prefijos",
        "",
        f"- Cortes ejecutados: `{len(prefix_rows)}`.",
        f"- Fallos: `{len(failures)}`.",
    ]
    for row in failures[:5]:
        lines.append(f"- FALLO `{row.get('cutoff_time')}`: `{row.get('mismatch')}`")
    lines += [
        "",
        "## Cobertura causal",
        "",
        f"- Geometrica causal: `{coverage['causal_geometric_count']}/"
        f"{coverage['structural_swing_count']}` "
        f"({_pct(coverage['causal_geometric_count'], coverage['structural_swing_count'])}).",
        f"- Funcional causal: `{coverage['causal_functional_count']}/"
        f"{coverage['structural_swing_count']}` "
        f"({_pct(coverage['causal_functional_count'], coverage['structural_swing_count'])}).",
        f"- Movimientos con cobertura funcional causal: "
        f"`{coverage['causal_functional_movement_count']}/{coverage['movement_count']}`.",
        f"- Ticks con owner explicito: `{coverage['owner_tick_count']}/"
        f"{coverage['tick_count']}`; sin owner: `{coverage['uncovered_tick_count']}`.",
        "",
        "La cobertura parcial no se rellena con lecturas posteriores. Se reporta como "
        "cobertura no disponible en ese tick, no como cobertura causal.",
        "",
        "## Conclusion",
        "",
        f"- `AFS2_READY={str(engine.afs2['AFS2_READY']).lower()}`.",
        f"- Alcance: {engine.afs2['AFS2_SCOPE']}.",
        "",
    ]
    return "\n".join(lines)


def build_diff_report() -> str:
    return """# Diff conceptual v0.7.4 -> v0.7.5

## Separacion de tiempos
- v0.7.4 usaba un unico tiempo de evento y podia registrar un TT con el tiempo estructural del cruce.
- v0.7.5 separa `structural_time`, `confirmation_time` y `knowledge_time`; publica en `time` el conocimiento.

## Arquitectura
- El constructor de movimientos pasa de una pasada final a `MovementBuilder` incremental.
- El scheduler de vela/gap pasa a `TickScheduler` y ejecuta GAP antes de las ramas de lectura.
- El motor ya no ordena ni reindexa eventos al final: `event_id` es append-only y `sequence_id` es el seq real del feed en conocimiento.

## Estado y auditoria
- La auditoria por tick registra owner explicito (`C/B/A/MODULE/NOISE/NONE`), lectura propietaria, seq de conocimiento y cobertura.
- La narrativa de vela usa el snapshot de cierre, no el estado final del motor.
- La cobertura causal exige que la lectura y A fueran conocidas antes de la confirmacion del swing.

## TT y AUT
- TT solo se emite despues de B Grande conocida; conserva el tiempo estructural del cruce.
- B Grande se emite antes de AUT; AUT reclasifica el recorrido y no se borra la cronologia anterior.

## Lo que no cambia
- No se anaden reglas TM nuevas.
- No se hardcodean precios, horas ni IDs.
- La geometria funcional de v0.7.4 se conserva y se valida por tests y diff de salida.
"""


def build_unresolved_report(engine: Engine) -> str:
    lines = [
        "# Asuntos no resueltos v0.7.5",
        "",
        "## Reglas o semantica abierta",
    ]
    for item in engine.pending:
        lines.append(f"- `{item}`")
    lines += [
        "- `AUT`: se evalua al confirmar un movimiento, no en cada tick intermedio; verificar si la "
        "regla exige tick exacto.",
        "",
        "## Cobertura",
        f"- Causal geometrica: `{engine.coverage['causal_geometric_count']}/"
        f"{engine.coverage['structural_swing_count']}`.",
        f"- Causal funcional: `{engine.coverage['causal_functional_count']}/"
        f"{engine.coverage['structural_swing_count']}`.",
        f"- Ticks sin owner: `{engine.coverage['uncovered_tick_count']}`.",
        "- La cobertura parcial es informativa; no se fuerza con lecturas futuras.",
        "",
        "## Proceso",
        "- La aprobacion de Javier sobre los cuatro tests v0.7.4 corregidos sigue sin registrarse.",
        "- Faltan los documentos de prioridad/dossier indicados en `AGENTS.md`.",
        "- `AFS2_READY=true` no implica cobertura funcional total ni cierre de reglas pendientes.",
        "",
    ]
    return "\n".join(lines)


def write_v075_reports(
    engine: Engine,
    prefix_rows: list[dict],
    out_dir: Path | str,
    stem: str = "v075",
) -> list[Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    paths.extend(write_prefix_matrix(prefix_rows, out_dir, stem))
    paths.extend(write_causal_coverage(engine, out_dir, stem))
    causal_path = out_dir / f"{stem}_InformeCausalidad.md"
    causal_path.write_text(build_causal_report(engine, prefix_rows), encoding="utf-8")
    paths.append(causal_path)
    diff_path = out_dir / f"{stem}_DiffConceptual_v074_v075.md"
    diff_path.write_text(build_diff_report(), encoding="utf-8")
    paths.append(diff_path)
    unresolved_path = out_dir / f"{stem}_AsuntosNoResueltos.md"
    unresolved_path.write_text(build_unresolved_report(engine), encoding="utf-8")
    paths.append(unresolved_path)
    afs2_path = out_dir / f"{stem}_AFS2.json"
    afs2_path.write_text(json.dumps(engine.afs2, ensure_ascii=False, indent=2), encoding="utf-8")
    paths.append(afs2_path)
    return paths




def _cutoffs(engine: Engine) -> list[int]:
    cutoffs = set()
    points = engine.points
    for index, point in enumerate(points):
        if index + 1 == len(points) or points[index + 1].bar != point.bar:
            cutoffs.add(point.time_ms)
    for reading in engine.readings:
        if reading.b_grande_time:
            cutoffs.add(reading.b_grande_time - 1)
            cutoffs.add(reading.b_grande_time)
        if reading.tt_hit and reading.tt_time:
            cutoffs.add(reading.tt_time - 1)
            cutoffs.add(reading.tt_time)
        if reading.tt_hit and reading.tt_knowledge_time:
            cutoffs.add(reading.tt_knowledge_time - 1)
            cutoffs.add(reading.tt_knowledge_time)
    return sorted(cutoffs)


def main(argv: list[str] | None = None) -> int:
    import argparse

    from TM_CORE_PYTHON_v075_STREAMING import (
        filter_points,
        load_feed,
        parse_hms,
        run_engine,
        run_prefix_matrix,
        write_outputs,
    )

    parser = argparse.ArgumentParser(description="Genera entregables v0.7.5")
    parser.add_argument("--feed", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("out_v075"))
    parser.add_argument("--stem", default="v075")
    parser.add_argument("--start")
    parser.add_argument("--end")
    args = parser.parse_args(argv)
    points, bars = load_feed(args.feed)
    base = points[0].time_ms
    start = parse_hms(args.start, base) if args.start else None
    end = parse_hms(args.end, base) if args.end else None
    points = filter_points(points, start, end)
    full = run_engine(points, bars)
    cutoffs = _cutoffs(full)
    full, rows = run_prefix_matrix(points, bars, cutoffs, full)
    paths = write_outputs(full, args.out, args.stem)
    paths.extend(write_v075_reports(full, rows, args.out, args.stem))
    failures = sum(1 for row in rows if not row.get("pass"))
    print(f"v0.7.5 readings={len(full.readings)} events={len(full.events)} movements={len(full.movements)}")
    print(f"prefixes={len(rows)} failures={failures} AFS2_READY={full.afs2['AFS2_READY']}")
    print(f"outputs={args.out}")
    for path in paths:
        print(f"  {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
