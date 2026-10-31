"""TM Core v0.7.4 - lector funcional multicapa, causal y auditable."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

VERSION = "0.7.4"
PRICE_SCALE = 100
MOVE = 600
STRUCTURAL_MOVE = 200
RETRACE_NUM = 25
RETRACE_DEN = 100
AUT_NUM = 127
AUT_DEN = 100
AUT_EXTRA = 25
CUT_BUFFER = 200
MIN_MODULE = 1000
A_SIGNIFICANT_NUM = 75
A_SIGNIFICANT_DEN = 100
A_MAX_MODULE_MULTIPLE = 2.0
MAX_ACTIVE = 3
WINDOW_START = "16:52:00"
WINDOW_END = "17:01:00"

FUNCTION_LABELS = {
    "1",
    "A",
    "B",
    "C",
    "AUT",
    "TT",
    "FT",
    "CUT",
    "GAP",
    "B_GRANDE",
    "B_FALLIDA",
    "B_OSCILACION",
    "C_CAND",
    "C_CANCELADA",
    "A_SIGNIFICATIVA",
    "A_DESPROPORCIONADA_MODULO",
    "TT_FALLIDO",
    "ARCHIVADA",
}
FORBIDDEN_FUNCTIONS = {"LOCAL", "SUPERIOR", "ESTRUCTURA", "GIRO", "B_EXCESIVA", "OBSERVADOR"}


def price_i(value: float | int | str) -> int:
    return int(round(float(value) * PRICE_SCALE))


def price_s(value: int | float | None) -> str:
    if value is None:
        return ""
    return f"{int(value) / PRICE_SCALE:.2f}"


def ms_to_text(ms: int | None) -> str:
    if ms is None:
        return ""
    dt = datetime.fromtimestamp(ms / 1000, timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S.") + f"{dt.microsecond // 1000:03d}"


def ms_to_hms(ms: int | None) -> str:
    if ms is None:
        return ""
    dt = datetime.fromtimestamp(ms / 1000, timezone.utc)
    return dt.strftime("%H:%M:%S.") + f"{dt.microsecond // 1000:03d}"


def parse_hms(value: str | int | None, base_ms: int | None = None) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, int):
        return value
    text = str(value).strip()
    if text.isdigit():
        return int(text)
    parts = text.split(":")
    if len(parts) < 2:
        raise ValueError(f"hora inválida: {value!r}")
    hour = int(parts[0])
    minute = int(parts[1])
    second = 0
    milli = 0
    if len(parts) >= 3:
        sec_part = parts[2]
        if "." in sec_part:
            sec_text, frac = sec_part.split(".", 1)
            second = int(sec_text)
            milli = int((frac + "000")[:3])
        else:
            second = int(sec_part)
    if base_ms is None:
        now = datetime.now(timezone.utc)
        base = now.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        base = datetime.fromtimestamp(base_ms / 1000, timezone.utc)
    target = base.replace(hour=hour, minute=minute, second=second, microsecond=milli * 1000)
    return int(target.timestamp() * 1000)


@dataclass(frozen=True)
class Pt:
    price: int
    seq: int
    time_ms: int
    bar: int

    @property
    def hms(self) -> str:
        return ms_to_hms(self.time_ms)


@dataclass
class Bar:
    idx: int
    name: str
    open: Pt
    high: Pt
    low: Pt
    last: Pt
    prev_close: Optional[int] = None
    gap: int = 0


@dataclass(frozen=True)
class Movement:
    origin: int
    extreme: int
    direction: int
    origin_index: int
    extreme_index: int
    confirm_index: int

    @property
    def size(self) -> int:
        return abs(self.extreme - self.origin)


@dataclass
class Reading:
    reading_id: str
    direction: int
    state: str
    created_time: int
    created_seq: int
    created_bar: int
    origin_reason: str
    module_origin: int
    module_extreme: int
    module_origin_time: int
    module_extreme_time: int
    module_origin_seq: int
    module_extreme_seq: int
    parent_reading_id: str = ""
    closed_time: int | None = None
    closed_bar: int | None = None
    a_origin: int = 0
    a_end: int = 0
    a_origin_time: int = 0
    a_end_time: int = 0
    a_origin_seq: int = 0
    a_end_seq: int = 0
    b_origin: int = 0
    b_extreme: int = 0
    b_origin_time: int = 0
    b_extreme_time: int = 0
    b_origin_seq: int = 0
    b_extreme_seq: int = 0
    c_origin: int = 0
    c_extreme: int = 0
    c_origin_time: int = 0
    c_extreme_time: int = 0
    aut_time: int = 0
    aut_price: int = 0
    tt_target: int = 0
    tt_hit: bool = False
    tt_time: int = 0
    tt_price: int = 0
    tt_seq: int = 0
    tt_extreme: int = 0
    tt_extreme_time: int = 0
    tt_extreme_seq: int = 0
    ft: bool = False
    ft_time: int = 0
    ft_price: int = 0
    fail_reason: str = ""
    fail_time: int = 0
    fail_price: int = 0
    a_sig_opened: bool = False
    labels: list[tuple[int, str]] = field(default_factory=list)
    leg_indices: list[int] = field(default_factory=list)
    structural_valid: bool = True
    operational_valid: bool = False
    operational_rejection_reason: str = "FASE1_SOLO_LECTURA"
    post_tt: bool = False
    parent_tt_id: str = ""
    generation: int = 1

    @property
    def module_size(self) -> int:
        return abs(self.module_extreme - self.module_origin)

    @property
    def a_size(self) -> int:
        if not self.a_origin or not self.a_end:
            return 0
        return abs(self.a_end - self.a_origin)

    @property
    def b_size(self) -> int:
        if not self.b_origin or not self.b_extreme:
            return 0
        return abs(self.b_extreme - self.b_origin)

    @property
    def c_size(self) -> int:
        if not self.c_origin or not self.c_extreme:
            return 0
        return abs(self.c_extreme - self.c_origin)

    @property
    def x_size(self) -> int:
        return self.module_size

    @property
    def tt_pt(self) -> Pt | None:
        if not self.tt_hit:
            return None
        return Pt(self.tt_price, self.tt_seq, self.tt_time, self.tt_time // 60000)


def load_feed(path: Path | str) -> tuple[list[Pt], dict[int, Bar]]:
    path = Path(path)
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh, delimiter=";")
        required = {"sequence_id", "time_msc", "bid"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"feed missing columns: {sorted(missing)}")
        rows = list(reader)
    points: list[Pt] = []
    seen: set[int] = set()
    last_time = -1
    for row in sorted(rows, key=lambda item: int(item["sequence_id"])):
        seq = int(row["sequence_id"])
        if seq in seen:
            raise ValueError(f"duplicate sequence_id: {seq}")
        seen.add(seq)
        ts = int(row["time_msc"])
        if ts < last_time:
            raise ValueError("time moves backwards after sequence_id ordering")
        last_time = ts
        points.append(Pt(price_i(row["bid"]), seq, ts, ts // 60000))
    bars: dict[int, Bar] = {}
    for p in points:
        bar = bars.get(p.bar)
        if bar is None:
            prev = bars[max(bars)].last.price if bars else None
            gap = p.price - prev if prev is not None else 0
            bars[p.bar] = Bar(p.bar, ms_to_hms(p.bar * 60000)[:5], p, p, p, p, prev, gap)
        else:
            if p.price > bar.high.price:
                bar.high = p
            if p.price < bar.low.price:
                bar.low = p
            bar.last = p
    return points, bars


def filter_points(points: list[Pt], start: int | None = None, end: int | None = None) -> list[Pt]:
    result = points
    if start is not None:
        result = [p for p in result if p.time_ms >= start]
    if end is not None:
        result = [p for p in result if p.time_ms <= end]
    return result


def build_movements(
    points: list[Pt],
    min_move: int = MOVE,
    retrace_num: int = RETRACE_NUM,
    retrace_den: int = RETRACE_DEN,
) -> list[Movement]:
    if not points:
        return []
    origin = points[0].price
    ext = origin
    direction = 0
    origin_index = 0
    extreme_index = 0
    movements: list[Movement] = []
    for i, p in enumerate(points[1:], 1):
        if direction == 0:
            if p.price - origin >= min_move:
                direction = 1
                ext = p.price
                extreme_index = i
            elif origin - p.price >= min_move:
                direction = -1
                ext = p.price
                extreme_index = i
            continue
        threshold = max(min_move, (abs(ext - origin) * retrace_num) // retrace_den)
        if direction > 0:
            if p.price > ext:
                ext = p.price
                extreme_index = i
            elif ext - p.price >= threshold:
                movements.append(Movement(origin, ext, 1, origin_index, extreme_index, i))
                origin = ext
                origin_index = extreme_index
                ext = p.price
                extreme_index = i
                direction = -1
        else:
            if p.price < ext:
                ext = p.price
                extreme_index = i
            elif p.price - ext >= threshold:
                movements.append(Movement(origin, ext, -1, origin_index, extreme_index, i))
                origin = ext
                origin_index = extreme_index
                ext = p.price
                extreme_index = i
                direction = 1
    return movements


class Engine:
    def __init__(self, points: list[Pt], bars: dict[int, Bar]):
        self.points = points
        self.bars = bars
        self.movements = build_movements(points)
        self.readings: list[Reading] = []
        self.events: list[dict] = []
        self.patterns: list[dict] = []
        self.audit: list[dict] = []
        self.narrative: list[dict] = []
        self.pending: list[str] = []
        self.coverage: dict = {}
        self.active: list[Reading] = []
        self.by_id: dict[str, Reading] = {}
        self._reading_seq = 0
        self._event_seq = 0
        self._pattern_seq = 0
        self.start_time = points[0].time_ms if points else 0
        self.end_time = points[-1].time_ms if points else 0

    def active_at(self, time_ms: int) -> list[Reading]:
        return [
            r
            for r in self.readings
            if r.created_time <= time_ms and (r.closed_time is None or r.closed_time > time_ms)
        ]

    def _next_reading_id(self) -> str:
        self._reading_seq += 1
        return f"R{self._reading_seq:04d}"

    def _emit(
        self,
        kind: str,
        pt: Pt,
        reading: Reading | None,
        function: str,
        new_state: str,
        reason: str = "",
        detail: str = "",
    ) -> dict:
        self._event_seq += 1
        event = {
            "event_id": f"E{self._event_seq:06d}",
            "sequence_id": self._event_seq,
            "time_ms": pt.time_ms,
            "time": ms_to_text(pt.time_ms),
            "bar": pt.bar,
            "bar_time": ms_to_hms(pt.bar * 60000)[:5],
            "price": pt.price,
            "gap": self.bars.get(pt.bar).gap if pt.bar in self.bars else 0,
            "kind": kind,
            "function": function,
            "new_state": new_state,
            "reading_id": reading.reading_id if reading else "",
            "parent_reading_id": reading.parent_reading_id if reading else "",
            "direction": reading.direction if reading else 0,
            "module_origin": reading.module_origin if reading else 0,
            "module_extreme": reading.module_extreme if reading else 0,
            "module_size": reading.module_size if reading else 0,
            "a_origin": reading.a_origin if reading else 0,
            "a_end": reading.a_end if reading else 0,
            "a_size": reading.a_size if reading else 0,
            "b_origin": reading.b_origin if reading else 0,
            "b_extreme": reading.b_extreme if reading else 0,
            "b_size": reading.b_size if reading else 0,
            "c_origin": reading.c_origin if reading else 0,
            "c_extreme": reading.c_extreme if reading else 0,
            "c_size": reading.c_size if reading else 0,
            "tt_target": reading.tt_target if reading else 0,
            "tt_100": reading.tt_price if reading and reading.tt_hit else 0,
            "tt_real_extreme": reading.tt_extreme if reading else 0,
            "ft": int(reading.ft) if reading else 0,
            "structural_valid": int(reading.structural_valid) if reading else 1,
            "operational_valid": int(reading.operational_valid) if reading else 0,
            "operational_rejection_reason": reading.operational_rejection_reason if reading else "",
            "reason": reason,
            "detail": detail,
        }
        self.events.append(event)
        return event

    def _pattern(
        self,
        pattern_type: str,
        status: str,
        reading: Reading | None,
        origin: int,
        end: int,
        detail: str = "",
        time_ms: int | None = None,
    ) -> dict:
        self._pattern_seq += 1
        pattern = {
            "pattern_id": f"P{self._pattern_seq:04d}",
            "type": pattern_type,
            "status": status,
            "final_status": status,
            "direction": reading.direction if reading else 0,
            "origin_time": ms_to_text(reading.module_origin_time if reading else time_ms),
            "origin_price": origin,
            "end_time": ms_to_text(time_ms if time_ms is not None else (reading.closed_time if reading else None)),
            "end_price": end,
            "size": abs(end - origin),
            "reading_id": reading.reading_id if reading else "",
            "cycle_id": reading.reading_id if reading else "",
            "detail": detail,
        }
        self.patterns.append(pattern)
        return pattern

    def _create_reading(
        self,
        pt: Pt,
        reason: str,
        parent: Reading | None,
        direction: int,
        origin: int,
        ext: int,
        origin_time: int,
        ext_time: int,
        origin_seq: int,
        ext_seq: int,
        leg_index: int,
    ) -> Reading:
        reading = Reading(
            reading_id=self._next_reading_id(),
            direction=direction,
            state="MODULE",
            created_time=pt.time_ms,
            created_seq=pt.seq,
            created_bar=pt.bar,
            origin_reason=reason,
            module_origin=origin,
            module_extreme=ext,
            module_origin_time=origin_time,
            module_extreme_time=ext_time,
            module_origin_seq=origin_seq,
            module_extreme_seq=ext_seq,
            parent_reading_id=parent.reading_id if parent else "",
        )
        reading.labels.append((leg_index, "1"))
        reading.leg_indices.append(leg_index)
        self.readings.append(reading)
        self.by_id[reading.reading_id] = reading
        self.active.append(reading)
        self._pattern("LECTURA_FUNCIONAL", "ACTIVA", reading, origin, ext, reason)
        self._emit("LECTURA_CREADA", pt, reading, "1", "MODULE", reason)
        return reading

    def _done(self, r: Reading, pt: Pt, state: str = "DONE", reason: str = "") -> None:
        if r.state == "DONE":
            return
        r.state = state
        r.closed_time = pt.time_ms
        r.closed_bar = pt.bar
        if reason:
            r.fail_reason = reason

    def _b_grande(self, r: Reading, pt: Pt, ep: Pt, movement: Movement) -> None:
        r.b_extreme = movement.extreme
        r.b_extreme_time = ep.time_ms
        r.b_extreme_seq = ep.seq
        r.tt_target = r.a_end + r.direction * r.module_size
        r.state = "TT_PENDING"
        r.labels.append((movement.confirm_index, "B_GRANDE"))
        self._emit("B_GRANDE", pt, r, "B", "TT_PENDING", "B_100_A")
        self._pattern("B_GRANDE", "CONFIRMADO", r, r.b_origin, r.b_extreme, "B>=A", pt.time_ms)
        self._check_tt(r, movement)

    def _check_tt(self, r: Reading, movement: Movement) -> None:
        if not r.tt_target or r.tt_hit:
            return
        for i in range(movement.origin_index, movement.extreme_index + 1):
            p = self.points[i]
            if (r.direction > 0 and p.price >= r.tt_target) or (r.direction < 0 and p.price <= r.tt_target):
                r.tt_hit = True
                r.tt_time = p.time_ms
                r.tt_price = p.price
                r.tt_seq = p.seq
                r.tt_extreme = movement.extreme
                r.tt_extreme_time = self.points[movement.extreme_index].time_ms
                r.tt_extreme_seq = self.points[movement.extreme_index].seq
                r.state = "TT_EXT"
                r.labels.append((movement.confirm_index, "TT"))
                r.operational_valid = True
                r.operational_rejection_reason = ""
                self._emit("TT_100", p, r, "TT", "TT_EXT", "TT_100", f"target={price_s(r.tt_target)}")
                self._pattern("TT", "CONFIRMADO", r, r.a_end, p.price, "TT_100", p.time_ms)
                return

    def _update(self, r: Reading, movement: Movement) -> None:
        if r.state == "DONE":
            return
        cp = self.points[movement.confirm_index]
        ep = self.points[movement.extreme_index]
        if r.state == "MODULE":
            if movement.direction == r.direction:
                r.module_extreme = movement.extreme
                r.module_extreme_time = ep.time_ms
                r.module_extreme_seq = ep.seq
                r.labels.append((movement.confirm_index, "1"))
                self._emit("MODULO_EXT", ep, r, "1", "MODULE", "NUEVO_EXTREMO")
            else:
                r.a_origin = r.module_extreme
                r.a_origin_time = r.module_extreme_time
                r.a_origin_seq = r.module_extreme_seq
                r.a_end = movement.extreme
                r.a_end_time = ep.time_ms
                r.a_end_seq = ep.seq
                r.state = "A"
                r.labels.append((movement.confirm_index, "A"))
                self._emit("A_INICIO", ep, r, "A", "A", "MOVIMIENTO_CONTRARIO")
            return
        if r.state == "A":
            if movement.direction == r.direction:
                r.b_origin = r.a_end
                r.b_origin_time = r.a_end_time
                r.b_origin_seq = r.a_end_seq
                r.b_extreme = movement.extreme
                r.b_extreme_time = ep.time_ms
                r.b_extreme_seq = ep.seq
                r.labels.append((movement.confirm_index, "B"))
                self._emit("B_INICIO", ep, r, "B", "B", "CONTRARIO_A_A")
                if r.b_size > (AUT_NUM * r.a_size) // AUT_DEN + AUT_EXTRA:
                    r.aut_time = cp.time_ms
                    r.aut_price = movement.extreme
                    r.labels.append((movement.confirm_index, "AUT"))
                    self._emit("AUT", cp, r, "AUT", "AUT", "SUPERA_127_MAS_025")
                    self._b_grande(r, cp, ep, movement)
                elif r.b_size >= r.a_size:
                    self._b_grande(r, cp, ep, movement)
                else:
                    r.state = "B_CAND"
            else:
                if r.direction > 0:
                    r.a_end = min(r.a_end, movement.extreme)
                else:
                    r.a_end = max(r.a_end, movement.extreme)
                r.a_end_time = ep.time_ms
                r.a_end_seq = ep.seq
                r.labels.append((movement.confirm_index, "A"))
                self._emit("A_EXT", ep, r, "A", "A", "A_CONTINUA")
            return
        if r.state == "B_CAND":
            if movement.direction == r.direction:
                r.b_extreme = movement.extreme
                r.b_extreme_time = ep.time_ms
                r.b_extreme_seq = ep.seq
                r.labels.append((movement.confirm_index, "B"))
                self._emit("B_EXT", ep, r, "B", "B_CAND", "B_CONTINUA")
                if r.b_size > (AUT_NUM * r.a_size) // AUT_DEN + AUT_EXTRA:
                    r.aut_time = cp.time_ms
                    r.aut_price = movement.extreme
                    r.labels.append((movement.confirm_index, "AUT"))
                    self._emit("AUT", cp, r, "AUT", "AUT", "SUPERA_127_MAS_025")
                    self._b_grande(r, cp, ep, movement)
                elif r.b_size >= r.a_size:
                    self._b_grande(r, cp, ep, movement)
            else:
                crosses = (r.direction > 0 and movement.extreme <= r.a_end) or (
                    r.direction < 0 and movement.extreme >= r.a_end
                )
                if crosses:
                    if r.direction > 0:
                        r.a_end = min(r.a_end, movement.extreme)
                    else:
                        r.a_end = max(r.a_end, movement.extreme)
                    r.a_end_time = ep.time_ms
                    r.a_end_seq = ep.seq
                    r.state = "A"
                    r.labels.append((movement.confirm_index, "B_FALLIDA"))
                    r.labels.append((movement.confirm_index, "A"))
                    self._emit("B_FALLIDA", cp, r, "B_FALLIDA", "A", "B_NO_LLEGO_A_100")
                else:
                    r.labels.append((movement.confirm_index, "B_OSCILACION"))
                    self._emit("B_OSCILACION", ep, r, "B_OSCILACION", "B_CAND", "OSCILACION_INTERNA")
            return
        if r.state == "TT_PENDING":
            if movement.direction == r.direction:
                old_b = r.b_extreme
                r.b_extreme = movement.extreme
                r.b_extreme_time = ep.time_ms
                r.b_extreme_seq = ep.seq
                if r.c_origin:
                    self._emit("C_CANCELADA", ep, r, "C_CANCELADA", "TT_PENDING", "B_NUEVO_EXTREMO")
                    r.c_origin = 0
                    r.c_extreme = 0
                if old_b != r.b_extreme:
                    r.labels.append((movement.confirm_index, "B"))
                    self._emit("B_EXT", ep, r, "B", "TT_PENDING", "B_CONTINUA")
                self._check_tt(r, movement)
            else:
                r.c_origin = r.b_extreme
                r.c_origin_time = r.b_extreme_time
                r.c_extreme = movement.extreme
                r.c_extreme_time = ep.time_ms
                r.labels.append((movement.confirm_index, "C_CAND"))
                self._emit("C_CAND", ep, r, "C", "TT_PENDING", "CONTRARIO_A_B")
                if (r.direction > 0 and movement.extreme <= r.a_end - CUT_BUFFER) or (
                    r.direction < 0 and movement.extreme >= r.a_end + CUT_BUFFER
                ):
                    r.state = "DONE"
                    r.closed_time = cp.time_ms
                    r.closed_bar = cp.bar
                    r.fail_reason = "CUT_CRUZA_A_END_MAS_2"
                    r.labels.append((movement.confirm_index, "TT_FALLIDO"))
                    r.labels.append((movement.confirm_index, "CUT"))
                    self._emit("CUT", cp, r, "CUT", "DONE", "CUT_CRUZA_A_END_MAS_2")
                    self._pattern("CUT", "CONFIRMADO", r, r.c_origin, r.c_extreme, r.fail_reason, cp.time_ms)
            return
        if r.state == "TT_EXT":
            if movement.direction == r.direction:
                r.tt_extreme = movement.extreme
                r.tt_extreme_time = ep.time_ms
                r.tt_extreme_seq = ep.seq
                self._emit("TT_EXT", ep, r, "TT", "TT_EXT", "TT_EXTIENDE")
            else:
                r.ft = True
                r.ft_time = cp.time_ms
                r.ft_price = movement.extreme
                r.state = "DONE"
                r.closed_time = cp.time_ms
                r.closed_bar = cp.bar
                r.labels.append((movement.confirm_index, "FT"))
                self._emit("FT", cp, r, "FT", "DONE", "CONTRARIO_DESPUES_DE_TT")
                self._pattern("FT", "CONFIRMADO", r, r.tt_extreme, movement.extreme, "FT", cp.time_ms)

    def _open_candidate(
        self,
        movement: Movement,
        snapshots: list[tuple[Reading, str, int, int, int, int, bool]],
    ) -> tuple[str, Reading | None, int, int, int, int, int, int] | None:
        if not self.active:
            p = self.points[movement.origin_index]
            e = self.points[movement.extreme_index]
            return (
                "FIRST",
                None,
                movement.direction,
                movement.origin,
                movement.extreme,
                p.time_ms,
                e.time_ms,
                p.seq,
                e.seq,
            )
        for r, state, a_size, x_size, direction, a_end, a_sig in snapshots:
            if r.state == "DONE":
                continue
            if state == "TT_EXT" and movement.direction != direction:
                p = self.points[movement.origin_index]
                e = self.points[movement.extreme_index]
                return (
                    "FT_NEW1",
                    r,
                    movement.direction,
                    movement.origin,
                    movement.extreme,
                    p.time_ms,
                    e.time_ms,
                    p.seq,
                    e.seq,
                )
        for r, state, a_size, x_size, direction, a_end, a_sig in snapshots:
            if r.state == "DONE":
                continue
            if state == "A" and movement.direction == direction and movement.size >= a_size and movement.size >= MOVE:
                p = self.points[movement.origin_index]
                e = self.points[movement.extreme_index]
                return (
                    "B_CONFIRMADA_NEW1",
                    r,
                    movement.direction,
                    movement.origin,
                    movement.extreme,
                    p.time_ms,
                    e.time_ms,
                    p.seq,
                    e.seq,
                )
        for r, state, a_size, x_size, direction, a_end, a_sig in snapshots:
            if r.state == "DONE":
                continue
            if (
                state in ("MODULE", "A", "B_CAND")
                and movement.direction != direction
                and x_size >= MIN_MODULE
                and a_size * A_SIGNIFICANT_DEN >= x_size * A_SIGNIFICANT_NUM
                and not a_sig
            ):
                return (
                    "A_SIGNIFICATIVA",
                    r,
                    -direction,
                    r.a_origin,
                    r.a_end,
                    r.a_origin_time,
                    r.a_end_time,
                    r.a_origin_seq,
                    r.a_end_seq,
                )
        for r, state, a_size, x_size, direction, a_end, a_sig in snapshots:
            if r.state == "DONE":
                continue
            if state == "TT_PENDING" and movement.direction != direction:
                cut = (direction > 0 and movement.extreme <= a_end - CUT_BUFFER) or (
                    direction < 0 and movement.extreme >= a_end + CUT_BUFFER
                )
                if cut:
                    p = self.points[movement.origin_index]
                    e = self.points[movement.extreme_index]
                    return (
                        "CUT_NEW1",
                        r,
                        movement.direction,
                        movement.origin,
                        movement.extreme,
                        p.time_ms,
                        e.time_ms,
                        p.seq,
                        e.seq,
                    )
        return None

    def _process_movement(self, movement: Movement) -> None:
        cp = self.points[movement.confirm_index]
        snapshots = [
            (r, r.state, r.a_size, r.x_size, r.direction, r.a_end, r.a_sig_opened)
            for r in list(self.active)
            if r.state != "DONE"
        ]
        for r in list(self.active):
            self._update(r, movement)
        self.active = [r for r in self.active if r.state != "DONE"]
        candidate = self._open_candidate(movement, snapshots)
        if candidate is not None:
            reason, parent, direction, origin, ext, origin_time, ext_time, origin_seq, ext_seq = candidate
            reading = self._create_reading(
                cp,
                reason,
                parent,
                direction,
                origin,
                ext,
                origin_time,
                ext_time,
                origin_seq,
                ext_seq,
                movement.confirm_index,
            )
            if parent is not None and reason == "A_SIGNIFICATIVA":
                parent.a_sig_opened = True
            if len(self.active) > MAX_ACTIVE:
                keep = {r.reading_id for r in sorted(self.active, key=lambda item: (-item.x_size, -item.created_time))[:MAX_ACTIVE]}
                for old in list(self.active):
                    if old.reading_id not in keep:
                        self._done(old, cp, "DONE", "ARCHIVADA_POR_CAPACIDAD")
                        old.labels.append((movement.confirm_index, "ARCHIVADA"))
                        self._emit("ARCHIVADA", cp, old, "ARCHIVADA", "DONE", "MAX_3_ACTIVAS")
                        if old in self.active:
                            self.active.remove(old)
        for r in list(self.active):
            if r.a_sig_opened and r.a_size > A_MAX_MODULE_MULTIPLE * r.x_size:
                self._done(r, cp, "DONE", "A_DESPROPORCIONADA_MODULO")
                r.labels.append((movement.confirm_index, "A_DESPROPORCIONADA_MODULO"))
                self._emit("A_DESPROPORCIONADA_MODULO", cp, r, "A_DESPROPORCIONADA_MODULO", "DONE", "A_MAYOR_2X_MODULO")
                if r in self.active:
                    self.active.remove(r)

    def run(self) -> "Engine":
        for movement in self.movements:
            self._process_movement(movement)
        feed_bars = {p.bar for p in self.points}
        for bar_idx in sorted(feed_bars):
            bar = self.bars.get(bar_idx)
            if bar is None:
                continue
            if bar.gap:
                self._emit("GAP", bar.open, None, "GAP", "GAP", f"gap={price_s(bar.gap)}", f"gap={price_s(bar.gap)}")
        last = self.points[-1] if self.points else Pt(0, 0, 0, 0)
        self._emit("FIN_FEED", last, None, "", "END", "END_OF_FEED", "fin del feed")
        self._finalize()
        return self

    def _finalize(self) -> None:
        self.events.sort(key=lambda e: (e["time_ms"], e["event_id"]))
        for i, event in enumerate(self.events, 1):
            event["sequence_id"] = i
        self.coverage = evaluate_coverage(self)
        self.audit = build_audit(self)
        self.narrative = build_narrative(self)
        self.pending = [
            "post_tt_fallido_no_definido",
            "ft_expiracion_no_definida",
            "entrada_tardia_ft_no_definida",
            "a_mayor_que_modulo_guardia_provisional",
        ]
        if not self.coverage.get("functional_ok", False):
            self.pending.append("functional_coverage_parcial")
        if not self.coverage.get("geometric_ok", False):
            self.pending.append("geometric_coverage_parcial")
        for r in self.readings:
            if r.state != "DONE":
                self.pending.append(f"lectura_abierta_al_final:{r.reading_id}")
                break


def structural_swings(points: list[Pt], threshold: int = STRUCTURAL_MOVE) -> list[dict]:
    if not points:
        return []
    origin = points[0]
    ext = origin
    direction = 0
    origin_index = extreme_index = 0
    swings: list[dict] = []
    for i, p in enumerate(points[1:], 1):
        if direction == 0:
            if p.price - origin.price >= threshold:
                direction = 1
                ext = p
                extreme_index = i
            elif origin.price - p.price >= threshold:
                direction = -1
                ext = p
                extreme_index = i
            continue
        if direction > 0:
            if p.price > ext.price:
                ext = p
                extreme_index = i
            elif ext.price - p.price >= threshold:
                swings.append(
                    {
                        "origin": origin.price,
                        "extreme": ext.price,
                        "direction": 1,
                        "size": ext.price - origin.price,
                        "origin_time": origin.time_ms,
                        "extreme_time": ext.time_ms,
                    }
                )
                origin = ext
                origin_index = extreme_index
                ext = p
                extreme_index = i
                direction = -1
        else:
            if p.price < ext.price:
                ext = p
                extreme_index = i
            elif p.price - ext.price >= threshold:
                swings.append(
                    {
                        "origin": origin.price,
                        "extreme": ext.price,
                        "direction": -1,
                        "size": origin.price - ext.price,
                        "origin_time": origin.time_ms,
                        "extreme_time": ext.time_ms,
                    }
                )
                origin = ext
                origin_index = extreme_index
                ext = p
                extreme_index = i
                direction = 1
    return swings


def _range_contains(reading: Reading, origin: int, extreme: int) -> bool:
    lo, hi = sorted((origin, extreme))
    ranges = [(reading.module_origin, reading.module_extreme)]
    if reading.a_origin and reading.a_end:
        ranges.append((reading.a_origin, reading.a_end))
    if reading.b_origin and reading.b_extreme:
        ranges.append((reading.b_origin, reading.b_extreme))
    if reading.c_origin and reading.c_extreme:
        ranges.append((reading.c_origin, reading.c_extreme))
    return any(min(a, b) <= lo and hi <= max(a, b) for a, b in ranges)


def evaluate_coverage(engine: Engine) -> dict:
    swings = structural_swings(engine.points, STRUCTURAL_MOVE)
    geometric_uncovered: list[dict] = []
    functional_uncovered: list[dict] = []
    for swing in swings:
        geometric = any(_range_contains(r, swing["origin"], swing["extreme"]) for r in engine.readings)
        functional = any(
            _range_contains(r, swing["origin"], swing["extreme"]) and r.a_origin
            for r in engine.readings
        )
        if not geometric:
            geometric_uncovered.append(swing)
        if not functional:
            functional_uncovered.append(swing)
    movements = engine.movements
    functional_movements = 0
    for m in movements:
        if any(_range_contains(r, m.origin, m.extreme) and r.a_origin for r in engine.readings):
            functional_movements += 1
    return {
        "structural_swing_count": len(swings),
        "geometric_count": len(swings) - len(geometric_uncovered),
        "functional_count": len(swings) - len(functional_uncovered),
        "geometric_uncovered": geometric_uncovered[:50],
        "functional_uncovered": functional_uncovered[:50],
        "geometric_ok": not geometric_uncovered,
        "functional_ok": not functional_uncovered,
        "movement_count": len(movements),
        "functional_movement_count": functional_movements,
        "movement_coverage_ok": functional_movements == len(movements),
    }


def build_audit(engine: Engine) -> list[dict]:
    by_time: dict[int, list[dict]] = defaultdict(list)
    for event in engine.events:
        by_time[event["time_ms"]].append(event)
    state: dict[str, str] = {}
    created_bar: dict[str, int] = {}
    rows: list[dict] = []
    prev_price = engine.points[0].price if engine.points else 0
    for p in engine.points:
        before = dict(state)
        for event in by_time.get(p.time_ms, []):
            rid = event["reading_id"]
            if rid:
                state[rid] = event["new_state"]
                created_bar.setdefault(rid, p.bar)
        after = dict(state)
        active_ids = [rid for rid, st in after.items() if st != "DONE"]
        inherited = [rid for rid in active_ids if created_bar.get(rid, p.bar) < p.bar]
        local = [rid for rid in active_ids if created_bar.get(rid, p.bar) == p.bar]
        active_objects = [engine.by_id[rid] for rid in active_ids if rid in engine.by_id]
        primary = max(active_objects, key=lambda item: item.x_size) if active_objects else None
        ownership = 0
        for r in active_objects:
            if min(r.module_origin, r.module_extreme) <= p.price <= max(r.module_origin, r.module_extreme):
                ownership += 1
        noise = abs(p.price - prev_price) < STRUCTURAL_MOVE
        coverage = "OK" if ownership > 0 or noise else "UNCOVERED"
        events_here = by_time.get(p.time_ms, [])
        rows.append(
            {
                "sequence_id": p.seq,
                "time": ms_to_text(p.time_ms),
                "price": p.price,
                "bar_time": ms_to_hms(p.bar * 60000)[:5],
                "gap": engine.bars[p.bar].gap if p.bar in engine.bars else 0,
                "local_direction": ("UP" if primary.direction > 0 else "DOWN") if primary else "",
                "structural_origin": primary.module_origin if primary else 0,
                "structural_extreme": primary.module_extreme if primary else 0,
                "excursion": abs(p.price - primary.module_origin) if primary else 0,
                "active_readings": ";".join(active_ids),
                "inherited_readings": ";".join(inherited),
                "local_readings": ";".join(local),
                "functions_before": ";".join(f"{rid}:{st}" for rid, st in sorted(before.items()) if st != "DONE"),
                "functions_after": ";".join(f"{rid}:{st}" for rid, st in sorted(after.items()) if st != "DONE"),
                "events_emitted": ";".join(e["event_id"] for e in events_here),
                "readings_created": ";".join(e["reading_id"] for e in events_here if e["kind"] == "LECTURA_CREADA"),
                "patterns_updated": ";".join(e["function"] for e in events_here if e["function"]),
                "ownership_count": ownership,
                "functional_coverage": coverage,
                "decision_reason": ";".join(e["reason"] for e in events_here if e["reason"]) or "NO_ACTION",
            }
        )
        prev_price = p.price
    return rows


def build_narrative(engine: Engine) -> list[dict]:
    rows: list[dict] = []
    for bar_idx in sorted(engine.bars):
        bar = engine.bars[bar_idx]
        start = bar_idx * 60000
        end = start + 59999
        bar_points = [p for p in engine.points if start <= p.time_ms <= end]
        if not bar_points:
            continue
        events = [e for e in engine.events if start <= e["time_ms"] <= end]
        started = [e["reading_id"] for e in events if e["kind"] == "LECTURA_CREADA"]
        closed = [
            e["reading_id"]
            for e in events
            if e["function"] in ("FT", "CUT", "TT_FALLIDO", "A_DESPROPORCIONADA_MODULO", "ARCHIVADA")
        ]
        active = [r.reading_id for r in engine.active_at(end)]
        extreme_order = (
            f"L({ms_to_hms(bar.low.time_ms)},{price_s(bar.low.price)})"
            f";H({ms_to_hms(bar.high.time_ms)},{price_s(bar.high.price)})"
            if bar.low.time_ms <= bar.high.time_ms
            else f"H({ms_to_hms(bar.high.time_ms)},{price_s(bar.high.price)})"
            f";L({ms_to_hms(bar.low.time_ms)},{price_s(bar.low.price)})"
        )
        rows.append(
            {
                "bar_time": bar.name,
                "open": bar.open.price,
                "high": bar.high.price,
                "low": bar.low.price,
                "close": bar.last.price,
                "gap": bar.gap,
                "extreme_order": extreme_order,
                "functions": ";".join(e["function"] for e in events if e["function"]),
                "readings_started": ";".join(started),
                "readings_closed": ";".join(closed),
                "active_at_close": ";".join(active),
                "patterns": len([e for e in events if e["function"]]),
                "pending": ";".join(r.state for r in engine.active_at(end)),
            }
        )
    return rows


EVENT_FIELDS = [
    "event_id",
    "sequence_id",
    "time",
    "time_ms",
    "bar",
    "bar_time",
    "price",
    "gap",
    "kind",
    "function",
    "new_state",
    "reading_id",
    "parent_reading_id",
    "direction",
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
    "tt_target",
    "tt_100",
    "tt_real_extreme",
    "ft",
    "structural_valid",
    "operational_valid",
    "operational_rejection_reason",
    "reason",
    "detail",
]

READING_FIELDS = [
    "reading_id",
    "direction",
    "state",
    "created_time",
    "created_bar",
    "closed_time",
    "parent_reading_id",
    "origin_reason",
    "module_origin",
    "module_extreme",
    "x",
    "a_origin",
    "a_end",
    "a",
    "b_origin",
    "b_extreme",
    "b",
    "c_origin",
    "c_extreme",
    "c",
    "aut_time",
    "aut_price",
    "tt_target",
    "tt_100_time",
    "tt_100_price",
    "tt_real_extreme",
    "ft",
    "ft_time",
    "ft_price",
    "fail_reason",
    "fail_time",
    "fail_price",
    "structural_valid",
    "operational_valid",
    "operational_rejection_reason",
    "post_tt",
    "parent_tt_id",
    "generation",
    "labels",
]

PATTERN_FIELDS = [
    "pattern_id",
    "type",
    "status",
    "final_status",
    "direction",
    "origin_time",
    "origin_price",
    "end_time",
    "end_price",
    "size",
    "reading_id",
    "cycle_id",
    "detail",
]

AUDIT_FIELDS = [
    "sequence_id",
    "time",
    "price",
    "bar_time",
    "gap",
    "local_direction",
    "structural_origin",
    "structural_extreme",
    "excursion",
    "active_readings",
    "inherited_readings",
    "local_readings",
    "functions_before",
    "functions_after",
    "events_emitted",
    "readings_created",
    "patterns_updated",
    "ownership_count",
    "functional_coverage",
    "decision_reason",
]

NARRATIVE_FIELDS = [
    "bar_time",
    "open",
    "high",
    "low",
    "close",
    "gap",
    "extreme_order",
    "functions",
    "readings_started",
    "readings_closed",
    "active_at_close",
    "patterns",
    "pending",
]


def _price_fields(row: dict, fields: Iterable[str]) -> dict:
    out = {}
    for key in fields:
        value = row.get(key, "")
        if key in {
            "price",
            "module_origin",
            "module_extreme",
            "module_size",
            "structural_origin",
            "structural_extreme",
            "excursion",
            "a_origin",
            "a_end",
            "a_size",
            "b_origin",
            "b_extreme",
            "b_size",
            "c_origin",
            "c_extreme",
            "c_size",
            "tt_target",
            "tt_100",
            "tt_real_extreme",
            "x",
            "a",
            "b",
            "c",
            "aut_price",
            "tt_100_price",
            "ft_price",
            "fail_price",
            "gap",
            "origin_price",
            "end_price",
            "size",
            "open",
            "high",
            "low",
            "close",
        }:
            out[key] = price_s(int(value)) if value not in ("", None) else ""
        else:
            out[key] = value
    return out


def write_outputs(engine: Engine, out_dir: Path | str, stem: str = "v074") -> list[Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "events": out_dir / f"{stem}_Eventos.csv",
        "readings": out_dir / f"{stem}_Lecturas.csv",
        "patterns": out_dir / f"{stem}_Patrones.csv",
        "audit": out_dir / f"{stem}_FunctionalAudit.csv",
        "narrative": out_dir / f"{stem}_BarNarrative.csv",
        "info": out_dir / f"{stem}_Informe.json",
        "comparison": out_dir / f"{stem}_Comparacion_1652_1700.csv",
    }
    with paths["events"].open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=EVENT_FIELDS)
        writer.writeheader()
        for row in engine.events:
            writer.writerow(_price_fields(row, EVENT_FIELDS))
    with paths["readings"].open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=READING_FIELDS)
        writer.writeheader()
        for r in sorted(engine.readings, key=lambda item: (item.created_time, item.reading_id)):
            row = {
                "reading_id": r.reading_id,
                "direction": "UP" if r.direction > 0 else "DOWN",
                "state": r.state,
                "created_time": ms_to_text(r.created_time),
                "created_bar": ms_to_hms(r.created_bar * 60000)[:5],
                "closed_time": ms_to_text(r.closed_time) if r.closed_time else "",
                "parent_reading_id": r.parent_reading_id,
                "origin_reason": r.origin_reason,
                "module_origin": r.module_origin,
                "module_extreme": r.module_extreme,
                "x": r.module_size,
                "a_origin": r.a_origin,
                "a_end": r.a_end,
                "a": r.a_size,
                "b_origin": r.b_origin,
                "b_extreme": r.b_extreme,
                "b": r.b_size,
                "c_origin": r.c_origin,
                "c_extreme": r.c_extreme,
                "c": r.c_size,
                "aut_time": ms_to_text(r.aut_time) if r.aut_time else "",
                "aut_price": r.aut_price,
                "tt_target": r.tt_target,
                "tt_100_time": ms_to_text(r.tt_time) if r.tt_time else "",
                "tt_100_price": r.tt_price,
                "tt_real_extreme": r.tt_extreme,
                "ft": int(r.ft),
                "ft_time": ms_to_text(r.ft_time) if r.ft_time else "",
                "ft_price": r.ft_price,
                "fail_reason": r.fail_reason,
                "fail_time": ms_to_text(r.fail_time) if r.fail_time else "",
                "fail_price": r.fail_price,
                "structural_valid": int(r.structural_valid),
                "operational_valid": int(r.operational_valid),
                "operational_rejection_reason": r.operational_rejection_reason,
                "post_tt": int(r.post_tt),
                "parent_tt_id": r.parent_tt_id,
                "generation": r.generation,
                "labels": ";".join(f"{idx}:{label}" for idx, label in r.labels),
            }
            writer.writerow(_price_fields(row, READING_FIELDS))
    with paths["patterns"].open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=PATTERN_FIELDS)
        writer.writeheader()
        for row in engine.patterns:
            writer.writerow(_price_fields(row, PATTERN_FIELDS))
    with paths["audit"].open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=AUDIT_FIELDS)
        writer.writeheader()
        for row in engine.audit:
            writer.writerow(_price_fields(row, AUDIT_FIELDS))
    with paths["narrative"].open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=NARRATIVE_FIELDS)
        writer.writeheader()
        for row in engine.narrative:
            writer.writerow(_price_fields(row, NARRATIVE_FIELDS))
    info = {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "feed_points": len(engine.points),
        "bars": len(engine.bars),
        "movements": len(engine.movements),
        "readings": len(engine.readings),
        "events": len(engine.events),
        "patterns": len(engine.patterns),
        "active_readings": len(engine.active),
        "coverage": {
            k: v
            for k, v in engine.coverage.items()
            if k not in ("geometric_uncovered", "functional_uncovered")
        },
        "coverage_uncovered_samples": {
            "geometric": engine.coverage.get("geometric_uncovered", [])[:10],
            "functional": engine.coverage.get("functional_uncovered", [])[:10],
        },
        "pending": engine.pending,
        "implementation_pending": [
            "post_tt_fallido",
            "ft_expiration_semantics",
            "late_ft_entry_semantics",
            "A>module_guard_is_provisional_2x",
            "macro_stream_40_points_not_separate_scale",
        ],
        "constants": {
            "MOVE": MOVE,
            "STRUCTURAL_MOVE": STRUCTURAL_MOVE,
            "RETRACE_NUM": RETRACE_NUM,
            "RETRACE_DEN": RETRACE_DEN,
            "MIN_MODULE": MIN_MODULE,
            "A_MAX_MODULE_MULTIPLE": A_MAX_MODULE_MULTIPLE,
            "MAX_ACTIVE": MAX_ACTIVE,
            "CUT_BUFFER": CUT_BUFFER,
            "A_SIGNIFICANT_NUM": A_SIGNIFICANT_NUM,
            "A_SIGNIFICANT_DEN": A_SIGNIFICANT_DEN,
        },
    }
    paths["info"].write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    comparison_rows = []
    window_start = parse_hms(WINDOW_START, engine.start_time)
    window_end = parse_hms(WINDOW_END, engine.start_time)
    for r in engine.readings:
        if window_start <= r.created_time <= window_end:
            comparison_rows.append(
                {
                    "reading_id": r.reading_id,
                    "module_origin": r.module_origin,
                    "module_extreme": r.module_extreme,
                    "module_size": r.module_size,
                    "a_end": r.a_end,
                    "b_extreme": r.b_extreme,
                    "tt_target": r.tt_target,
                    "tt_hit": int(r.tt_hit),
                    "ft": int(r.ft),
                    "state": r.state,
                    "origin_reason": r.origin_reason,
                }
            )
    with paths["comparison"].open("w", newline="", encoding="utf-8-sig") as fh:
        fields = [
            "reading_id",
            "module_origin",
            "module_extreme",
            "module_size",
            "a_end",
            "b_extreme",
            "tt_target",
            "tt_hit",
            "ft",
            "state",
            "origin_reason",
        ]
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in comparison_rows:
            writer.writerow(_price_fields(row, fields))
    return list(paths.values())


def run_engine(points: list[Pt], bars: dict[int, Bar]) -> Engine:
    return Engine(points, bars).run()


def _synthetic_engine(prices: list[float], start_ms: int) -> Engine:
    points = [Pt(price_i(p), i + 1, start_ms + i * 1000, (start_ms + i * 1000) // 60000) for i, p in enumerate(prices)]
    bars: dict[int, Bar] = {}
    for p in points:
        bar = bars.get(p.bar)
        if bar is None:
            prev = bars[max(bars)].last.price if bars else None
            gap = p.price - prev if prev is not None else 0
            bars[p.bar] = Bar(p.bar, ms_to_hms(p.bar * 60000)[:5], p, p, p, p, prev, gap)
        else:
            if p.price > bar.high.price:
                bar.high = p
            if p.price < bar.low.price:
                bar.low = p
            bar.last = p
    return run_engine(points, bars)


def selftest() -> None:
    base = 1_792_169_100_000
    engine = _synthetic_engine([100.00, 94.00, 100.00, 94.00, 100.00, 94.00, 100.00], base)
    assert engine.readings
    assert any(r.tt_hit for r in engine.readings)
    assert any(r.ft for r in engine.readings)
    assert len(engine.audit) == 7
    assert len(engine.narrative) >= 1
    assert engine.coverage["movement_count"] > 0
    assert not (FORBIDDEN_FUNCTIONS & {e["function"] for e in engine.events})
    with tempfile.TemporaryDirectory() as tmp:
        paths = write_outputs(engine, Path(tmp), "selftest")
        assert all(p.exists() for p in paths)
    print(f"SELFTEST OK v{VERSION}: 8 comprobaciones")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=f"TM core v{VERSION} functional reader")
    parser.add_argument("--feed", type=Path)
    parser.add_argument("--out", type=Path, default=Path("out_v074"))
    parser.add_argument("--stem", default="v074")
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--window-start", default=WINDOW_START)
    parser.add_argument("--window-end", default=WINDOW_END)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    if args.feed is None:
        parser.error("--feed is required unless --selftest")
    points, bars = load_feed(args.feed)
    base = points[0].time_ms
    start = parse_hms(args.start, base) if args.start else None
    end = parse_hms(args.end, base) if args.end else None
    points = filter_points(points, start, end)
    engine = run_engine(points, bars)
    paths = write_outputs(engine, args.out, args.stem)
    print(f"v{VERSION} readings={len(engine.readings)} events={len(engine.events)} movements={len(engine.movements)}")
    print(f"coverage geometric={engine.coverage['geometric_ok']} functional={engine.coverage['functional_ok']}")
    print(f"outputs={args.out}")
    for path in paths:
        print(f"  {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
