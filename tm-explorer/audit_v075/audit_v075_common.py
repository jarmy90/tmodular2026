from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable

AUDIT_DIR = Path(__file__).resolve().parent


def locate_root() -> Path:
    for base in (AUDIT_DIR, *AUDIT_DIR.parents):
        if (base / "python" / "TM_CORE_PYTHON_v075_STREAMING.py").exists():
            return base
        if (base / "motor" / "TM_CORE_PYTHON_v075_STREAMING.py").exists():
            return base
    raise RuntimeError("no se encontro TM_CORE_PYTHON_v075_STREAMING.py")


ROOT = locate_root()
MOTOR = ROOT / "python"
if not MOTOR.exists():
    MOTOR = ROOT / "motor"
if str(MOTOR) not in sys.path:
    sys.path.insert(0, str(MOTOR))

import TM_CORE_PYTHON_v075_STREAMING as core  # noqa: E402

WORKSPACE_FEED = Path(
    r"C:\Users\profesor\OpenBot\Shared\Transfers\fb8c2a5d-d62c-48d0-8120-bae2016283c4"
    r"\TM_TICKFEED_1615_1730.csv"
)
WORKSPACE_OLD_FEED = Path(
    r"C:\Users\profesor\OpenBot\Shared\Transfers\9c9276ac-5e0f-4c1a-8edb-22e5466079b0"
    r"\TM_TICKFEED_20261016_v010_USTEC_12345_USTEC_DAY16.csv"
)
WORKSPACE_OLD_OUT = ROOT / "out_v075"
WORKSPACE_LECTURAS = Path(
    r"C:\Users\profesor\OpenBot\Shared\Transfers\fb8c2a5d-d62c-48d0-8120-bae2016283c4"
    r"\TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v002.txt"
)
WORKSPACE_ARBOL = Path(
    r"C:\Users\profesor\OpenBot\Shared\Transfers\fb8c2a5d-d62c-48d0-8120-bae2016283c4"
    r"\TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_14.md"
)
PACKAGE_FEED = ROOT / "datos" / "feed_maestro_1615_1730.csv"
PACKAGE_OLD_FEED = ROOT / "datos" / "feed_anterior_1620_1700.csv"
PACKAGE_OLD_OUT = ROOT / "datos" / "out_v075_base"
PACKAGE_LECTURAS = ROOT / "datos" / "lecturas_confirmadas_v002.txt"
PACKAGE_ARBOL = ROOT / "datos" / "arbol_canonico_v2_14.md"

if PACKAGE_FEED.exists():
    FEED = PACKAGE_FEED
    OLD_FEED = PACKAGE_OLD_FEED
    OLD_OUT = PACKAGE_OLD_OUT
    LECTURAS = PACKAGE_LECTURAS
    ARBOL = PACKAGE_ARBOL
else:
    FEED = WORKSPACE_FEED
    OLD_FEED = WORKSPACE_OLD_FEED
    OLD_OUT = WORKSPACE_OLD_OUT
    LECTURAS = WORKSPACE_LECTURAS
    ARBOL = WORKSPACE_ARBOL

SEQ_FIELDS = {
    "sequence_id",
    "knowledge_sequence_id",
    "structural_sequence_id",
    "confirmation_sequence_id",
    "created_seq",
    "owner_known_at_seq",
}
EVENT_ID_FIELDS = {"event_id"}
READING_ID_FIELDS = {"reading_id", "parent_reading_id", "parent_tt_id"}
TIME_FIELDS = {
    "time",
    "knowledge_time",
    "structural_time",
    "confirmation_time",
    "created_time",
    "closed_time",
    "a_origin_time",
    "a_end_time",
    "b_origin_time",
    "b_extreme_time",
    "c_origin_time",
    "c_extreme_time",
    "aut_time",
    "tt_100_time",
    "tt_confirmation_time",
    "tt_knowledge_time",
    "ft_time",
    "ft_structural_time",
    "fail_time",
    "owner_created_time",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def read_feed_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh, delimiter=";")
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def build_bars(points: list[core.Pt]) -> dict[int, core.Bar]:
    bars: dict[int, core.Bar] = {}
    for p in points:
        bar = bars.get(p.bar)
        if bar is None:
            prev = bars[max(bars)].last.price if bars else None
            gap = p.price - prev if prev is not None else 0
            bars[p.bar] = core.Bar(
                p.bar, core.ms_to_hms(p.bar * 60000)[:5], p, p, p, p, prev, gap
            )
        else:
            if p.price > bar.high.price:
                bar.high = p
            if p.price < bar.low.price:
                bar.low = p
            bar.last = p
    return bars


def run(points: list[core.Pt], bars: dict[int, core.Bar]) -> core.Engine:
    return core.run_engine(points, bars)


def run_feed(path: Path) -> tuple[list[core.Pt], dict[int, core.Bar], core.Engine]:
    points, bars = core.load_feed(path)
    return points, bars, core.run_engine(points, bars)


def iso(ms: int | None) -> str:
    return core.ms_to_text(ms)


def hms(ms: int | None) -> str:
    return core.ms_to_hms(ms)


def event_sig(event: dict, seq_offset: int = 0, include_ids: bool = True) -> dict:
    out: dict[str, Any] = {}
    for key in core.EVENT_FIELDS:
        if key in EVENT_ID_FIELDS and not include_ids:
            continue
        value = event.get(key)
        if key in SEQ_FIELDS and value not in ("", None):
            value = int(value) - seq_offset
        out[key] = value
    return out


READING_COMPARE_FIELDS = [
    "reading_id",
    "direction",
    "state",
    "created_time",
    "created_seq",
    "created_bar",
    "closed_time",
    "parent_reading_id",
    "origin_reason",
    "module_origin",
    "module_extreme",
    "module_size",
    "a_origin",
    "a_end",
    "a_size",
    "b_origin",
    "b_extreme",
    "b_size",
    "c_origin",
    "c_extreme",
    "c_size",
    "aut_time",
    "aut_price",
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
    "fail_reason",
    "labels",
    "structural_valid",
    "operational_valid",
    "operational_rejection_reason",
    "post_tt",
    "parent_tt_id",
    "generation",
]


def reading_sig(reading: core.Reading, seq_offset: int = 0) -> dict:
    out: dict[str, Any] = {}
    for key in READING_COMPARE_FIELDS:
        if key == "labels":
            value = ";".join(f"{idx}:{label}" for idx, label in reading.labels)
        else:
            value = getattr(reading, key, None)
        if key in SEQ_FIELDS and value not in ("", None):
            value = int(value) - seq_offset
        out[key] = value
    return out


def compare_rows(
    left: Iterable[dict],
    right: Iterable[dict],
    fields: Iterable[str],
    limit: int = 20,
) -> dict:
    left_rows = list(left)
    right_rows = list(right)
    fields = list(fields)
    mismatches: list[dict] = []
    for index in range(min(len(left_rows), len(right_rows))):
        diffs = [
            field
            for field in fields
            if left_rows[index].get(field) != right_rows[index].get(field)
        ]
        if diffs:
            mismatches.append(
                {
                    "index": index,
                    "fields": diffs,
                    "left": {key: left_rows[index].get(key) for key in diffs},
                    "right": {key: right_rows[index].get(key) for key in diffs},
                }
            )
            if len(mismatches) >= limit:
                break
    count_mismatch = len(left_rows) != len(right_rows)
    return {
        "left_count": len(left_rows),
        "right_count": len(right_rows),
        "count_mismatch": count_mismatch,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "pass": not count_mismatch and not mismatches,
    }


def canonical_digest(values) -> str:
    payload = [json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) for value in values]
    return hashlib.sha256("\n".join(payload).encode("utf-8")).hexdigest()


def known_events(events: list[dict], cutoff: int) -> list[dict]:
    return [
        event
        for event in events
        if event["knowledge_time_ms"] <= cutoff and event["kind"] != "FIN_FEED"
    ]


def event_stream_digest(events: list[dict], cutoff: int) -> dict:
    selected = known_events(events, cutoff)
    return {
        "count": len(selected),
        "digest": canonical_digest(selected),
        "first_event_id": selected[0]["event_id"] if selected else "",
        "last_event_id": selected[-1]["event_id"] if selected else "",
    }


READING_IDENTITY_FIELDS = [
    "reading_id",
    "direction",
    "created_time",
    "created_seq",
    "created_bar",
    "origin_reason",
    "parent_reading_id",
    "module_origin",
    "module_extreme",
    "module_origin_time",
    "module_extreme_time",
    "module_origin_seq",
    "module_extreme_seq",
]


READING_MUTABLE_FIELDS = [
    "state",
    "closed_time",
    "closed_bar",
    "a_origin",
    "a_end",
    "a_origin_time",
    "a_end_time",
    "a_origin_seq",
    "a_end_seq",
    "a_knowledge_time",
    "b_origin",
    "b_extreme",
    "b_origin_time",
    "b_extreme_time",
    "b_origin_seq",
    "b_extreme_seq",
    "b_knowledge_time",
    "c_origin",
    "c_extreme",
    "c_origin_time",
    "c_extreme_time",
    "c_knowledge_time",
    "aut_time",
    "aut_price",
    "tt_target",
    "tt_hit",
    "tt_time",
    "tt_price",
    "tt_seq",
    "tt_confirmation_time",
    "tt_knowledge_time",
    "tt_extreme",
    "tt_extreme_time",
    "tt_extreme_seq",
    "b_grande_time",
    "aut_reclassified",
    "ft",
    "ft_time",
    "ft_price",
    "ft_structural_time",
    "fail_reason",
    "fail_time",
    "fail_price",
    "a_sig_opened",
    "post_tt",
    "parent_tt_id",
    "generation",
    "structural_valid",
    "operational_valid",
    "operational_rejection_reason",
]


def reading_identity_snapshot(reading) -> dict:
    return {field: getattr(reading, field) for field in READING_IDENTITY_FIELDS}


def reading_mutable_snapshot(reading) -> dict:
    return {field: getattr(reading, field) for field in READING_MUTABLE_FIELDS}


def reading_identity_digest(readings: list, cutoff: int) -> dict:
    selected = sorted(
        (reading for reading in readings if reading.created_time <= cutoff),
        key=lambda reading: reading.reading_id,
    )
    return {
        "count": len(selected),
        "digest": canonical_digest([reading_identity_snapshot(reading) for reading in selected]),
        "ids": [reading.reading_id for reading in selected],
    }


def reading_closed_digest(readings: list, cutoff: int) -> dict:
    selected = sorted(
        (
            reading
            for reading in readings
            if reading.created_time <= cutoff
            and reading.closed_time is not None
            and reading.closed_time <= cutoff
        ),
        key=lambda reading: reading.reading_id,
    )
    return {
        "count": len(selected),
        "digest": canonical_digest(
            [
                {
                    "identity": reading_identity_snapshot(reading),
                    "mutable": reading_mutable_snapshot(reading),
                }
                for reading in selected
            ]
        ),
        "ids": [reading.reading_id for reading in selected],
    }


def prefix_signature(engine, cutoff: int) -> dict:
    return {
        "events": event_stream_digest(engine.events, cutoff),
        "reading_identity": reading_identity_digest(engine.readings, cutoff),
        "reading_closed": reading_closed_digest(engine.readings, cutoff),
        "active_count": sum(
            1
            for reading in engine.readings
            if reading.created_time <= cutoff and reading.closed_time is None
        ),
    }


def compare_events(
    left: list[dict],
    right: list[dict],
    seq_offset: int = 0,
    include_ids: bool = True,
    limit: int = 20,
) -> dict:
    left_rows = [event_sig(event, seq_offset, include_ids) for event in left]
    right_rows = [event_sig(event, 0, include_ids) for event in right]
    fields = [key for key in core.EVENT_FIELDS if include_ids or key not in EVENT_ID_FIELDS]
    return compare_rows(left_rows, right_rows, fields, limit)


def compare_readings(
    left: list[core.Reading],
    right: list[core.Reading],
    seq_offset: int = 0,
    limit: int = 20,
) -> dict:
    left_rows = [reading_sig(reading, seq_offset) for reading in left]
    right_rows = [reading_sig(reading, 0) for reading in right]
    return compare_rows(left_rows, right_rows, READING_COMPARE_FIELDS, limit)


def write_csv(
    path: Path,
    fields: list[str],
    rows: Iterable[dict],
    root: Path | None = None,
) -> None:
    if root is not None:
        try:
            path = root / path.relative_to(ROOT)
        except ValueError:
            path = root / path.name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            try:
                prepared = core._price_fields(row, fields)
            except (TypeError, ValueError):
                prepared = {key: row.get(key, "") for key in fields}
            writer.writerow(prepared)


def write_json(path: Path, data: Any, root: Path | None = None) -> None:
    if root is not None:
        try:
            path = root / path.relative_to(ROOT)
        except ValueError:
            path = root / path.name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def bar_points(points: list[core.Pt], bar_idx: int) -> list[core.Pt]:
    return [point for point in points if point.bar == bar_idx]


def point_by_time(points: list[core.Pt], time_ms: int) -> core.Pt | None:
    for point in points:
        if point.time_ms == time_ms:
            return point
    return None


def previous_point(points: list[core.Pt], time_ms: int) -> core.Pt | None:
    found = None
    for point in points:
        if point.time_ms < time_ms:
            found = point
        else:
            break
    return found


def event_function(events: list[dict], kind: str, reading_id: str = "") -> dict | None:
    for event in events:
        if event["kind"] == kind and (not reading_id or event["reading_id"] == reading_id):
            return event
    return None


def bar_gap_events(engine: core.Engine, bar_idx: int) -> list[dict]:
    return [event for event in engine.events if event["kind"] == "GAP" and event["bar"] == bar_idx]


def bar_events(engine: core.Engine, bar_idx: int) -> list[dict]:
    return [event for event in engine.events if event["bar"] == bar_idx]


def functions_text(events: list[dict]) -> str:
    return ";".join(event["function"] for event in events if event["function"])


def reading_for_full_id(engine: core.Engine, reading_id: str) -> core.Reading | None:
    return engine.by_id.get(reading_id)


def stable_reading_key(reading: core.Reading) -> tuple:
    return (
        reading.created_time,
        reading.module_origin,
        reading.module_extreme,
        reading.direction,
        reading.a_origin,
        reading.a_end,
        reading.b_origin,
        reading.b_extreme,
        reading.tt_target,
        reading.origin_reason,
    )


def event_digest(events: list[dict], cutoff: int) -> tuple[str, int]:
    rows = [
        event_sig(event, 0, include_ids=True)
        for event in events
        if event["kind"] != "FIN_FEED" and event["knowledge_time_ms"] <= cutoff
    ]
    payload = json.dumps(rows, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest().upper(), len(rows)


def reading_created_count(engine: core.Engine, cutoff: int) -> int:
    return sum(1 for reading in engine.readings if reading.created_time <= cutoff)
