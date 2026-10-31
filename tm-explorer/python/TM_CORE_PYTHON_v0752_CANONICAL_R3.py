"""TM Core v0.7.5.2-R3 - universal B Grande and dual AUT genealogy."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import pickle
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Optional

VERSION = "0.7.5.2-R3"
PRICE_SCALE = 100
MOVE = 600
STRUCTURAL_MOVE = 200
PLANO_TICK = 25
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

AUT_CAUSE_B = "B_EXCEEDS_127_PLUS_0_25"
AUT_CAUSE_A = "A_CROSSES_STRUCTURE_BASE"

FUNCTION_LABELS = {
    "1",
    "2",
    "3",
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
        raise ValueError(f"hora invÃ¡lida: {value!r}")
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
    a_knowledge_time: int = 0
    b_origin: int = 0
    b_extreme: int = 0
    b_origin_time: int = 0
    b_extreme_time: int = 0
    b_origin_seq: int = 0
    b_extreme_seq: int = 0
    b_knowledge_time: int = 0
    c_origin: int = 0
    c_extreme: int = 0
    c_origin_time: int = 0
    c_extreme_time: int = 0
    c_knowledge_time: int = 0
    aut_time: int = 0
    aut_price: int = 0
    aut_source: str = ""
    b_tick_active: bool = False
    b_candidate_emitted: bool = False
    c_tick_started: bool = False
    active_function: str = ""
    tt_target: int = 0
    tt_hit: bool = False
    tt_time: int = 0
    tt_price: int = 0
    tt_seq: int = 0
    tt_confirmation_time: int = 0
    tt_knowledge_time: int = 0
    tt_extreme: int = 0
    tt_extreme_time: int = 0
    tt_extreme_seq: int = 0
    b_grande_time: int = 0
    aut_reclassified: bool = False
    ft: bool = False
    ft_time: int = 0
    ft_price: int = 0
    ft_structural_time: int = 0
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


class MovementBuilder:
    def __init__(
        self,
        first: Pt,
        min_move: int = MOVE,
        retrace_num: int = RETRACE_NUM,
        retrace_den: int = RETRACE_DEN,
    ) -> None:
        self.min_move = min_move
        self.retrace_num = retrace_num
        self.retrace_den = retrace_den
        self.origin = first.price
        self.ext = first.price
        self.direction = 0
        self.origin_index = 0
        self.extreme_index = 0
        self.index = 0

    def feed(self, p: Pt, index: int) -> Movement | None:
        self.index = index
        if self.direction == 0:
            if p.price - self.origin >= self.min_move:
                self.direction = 1
                self.ext = p.price
                self.extreme_index = index
            elif self.origin - p.price >= self.min_move:
                self.direction = -1
                self.ext = p.price
                self.extreme_index = index
            return None
        threshold = max(self.min_move, (abs(self.ext - self.origin) * self.retrace_num) // self.retrace_den)
        if self.direction > 0:
            if p.price > self.ext:
                self.ext = p.price
                self.extreme_index = index
                return None
            if self.ext - p.price >= threshold:
                movement = Movement(self.origin, self.ext, 1, self.origin_index, self.extreme_index, index)
                self._reanchor(p, index, -1)
                return movement
        else:
            if p.price < self.ext:
                self.ext = p.price
                self.extreme_index = index
                return None
            if p.price - self.ext >= threshold:
                movement = Movement(self.origin, self.ext, -1, self.origin_index, self.extreme_index, index)
                self._reanchor(p, index, 1)
                return movement
        return None

    def _reanchor(self, p: Pt, index: int, direction: int) -> None:
        self.origin = self.ext
        self.origin_index = self.extreme_index
        self.ext = p.price
        self.extreme_index = index
        self.direction = direction


def build_movements(
    points: list[Pt],
    min_move: int = MOVE,
    retrace_num: int = RETRACE_NUM,
    retrace_den: int = RETRACE_DEN,
) -> list[Movement]:
    if not points:
        return []
    builder = MovementBuilder(points[0], min_move, retrace_num, retrace_den)
    movements: list[Movement] = []
    for i, p in enumerate(points[1:], 1):
        movement = builder.feed(p, i)
        if movement is not None:
            movements.append(movement)
    return movements


@dataclass
class LocalLeg:
    function: str
    direction: int
    origin: int
    extreme: int
    origin_time: int
    extreme_time: int
    confirmation_time: int
    bar_time: str
    note: str = ""

    @property
    def size(self) -> int:
        return abs(self.extreme - self.origin)


@dataclass
class LocalSequence:
    sequence_id: str
    direction: int
    bars: str
    module_origin: int
    module_extreme: int
    module_origin_time: int
    module_extreme_time: int
    module_origin_seq: int
    module_extreme_seq: int
    legs: list[LocalLeg] = field(default_factory=list)

    @property
    def module_size(self) -> int:
        return abs(self.module_extreme - self.module_origin)


@dataclass
class BigBTracker:
    """Tick-causal B range. Prices are integer hundredths; AUT extra is one quarter point."""
    direction: int
    anchor: int
    a_size: int
    extreme: int
    confirmed: bool = False
    aut: bool = False
    c_started: bool = False
    c_extreme: int = 0

    @property
    def limit(self) -> int:
        return (AUT_NUM * self.a_size) // AUT_DEN + AUT_EXTRA

    @property
    def b_size(self) -> int:
        return abs(self.extreme - self.anchor)

    def feed(self, price: int) -> list[str]:
        """Return transitions caused by this tick; equality confirms B100, AUT is strict >."""
        transitions: list[str] = []
        extends_b = (self.direction > 0 and price > self.extreme) or (self.direction < 0 and price < self.extreme)
        if extends_b:
            self.extreme = price
        if self.c_started:
            contrary = (self.direction > 0 and price < self.extreme) or (self.direction < 0 and price > self.extreme)
            if contrary:
                self.c_extreme = price
            return transitions
        if not self.confirmed and self.b_size >= self.a_size:
            self.confirmed = True
            transitions.append("B_GRANDE")
        if self.confirmed and not self.aut and self.b_size > self.limit:
            self.aut = True
            transitions.append("AUT_B")
        return transitions

    def begin_c(self, price: int) -> bool:
        """A post-confirmation contrary tick starts C Grande directly, never C candidata."""
        if not self.confirmed:
            return False
        contrary = (self.direction > 0 and price < self.extreme) or (self.direction < 0 and price > self.extreme)
        if contrary and not self.c_started:
            self.c_started = True
            self.c_extreme = price
            return True
        return False


def strict_crosses(direction: int, price: int, base: int) -> bool:
    """Strictly crosses a structural base; touching equality is not a crossing."""
    return price > base if direction > 0 else price < base


def local_two_gate(*, gap: int, tail: int, direction_ok: bool, size_ok: bool) -> bool:
    """Ordered 2 gate: no gap (strictly below 0.25), permitted initial tail, direction, size."""
    return abs(gap) < PLANO_TICK and tail <= PLANO_TICK and direction_ok and size_ok


def _bar_time(ms: int) -> str:
    return ms_to_hms(ms)[:5]


def _first_cross(
    points: list[Pt], start: int, end: int, level: int, direction: int
) -> Pt | None:
    for point in points[start : end + 1]:
        if (direction > 0 and point.price > level) or (
            direction < 0 and point.price < level
        ):
            return point
    return None


def _local_123(b1: Bar, b2: Bar, b3: Bar) -> dict | None:
    span = b1.high.price - b1.low.price
    if span < MOVE:
        return None
    if b1.last.price < b1.open.price:
        direction = -1
        if b2.high.price - b2.open.price > PLANO_TICK:
            return None
        if abs(b2.open.price - b1.last.price) >= PLANO_TICK:
            return None
        if b2.open.price - b2.low.price < span:
            return None
        if b3.low.price >= b2.low.price:
            return None
        leg1 = (b1.high, b1.low)
        leg2 = (b2.open, b2.low)
        leg3 = (b3.open, b3.low)
    elif b1.last.price > b1.open.price:
        direction = 1
        if b2.open.price - b2.low.price > PLANO_TICK:
            return None
        if abs(b2.open.price - b1.last.price) >= PLANO_TICK:
            return None
        if b2.high.price - b2.open.price < span:
            return None
        if b3.high.price <= b2.high.price:
            return None
        leg1 = (b1.low, b1.high)
        leg2 = (b2.open, b2.high)
        leg3 = (b3.open, b3.high)
    else:
        return None
    return {
        "direction": direction,
        "legs": [(leg1[0], leg1[1]), (leg2[0], leg2[1]), (leg3[0], leg3[1])],
        "bars": [b1.name, b2.name, b3.name],
        "module_origin": leg1[0].price,
        "module_extreme": leg3[1].price,
    }


def _add_local_leg(
    seq: LocalSequence,
    function: str,
    direction: int,
    origin: int,
    extreme: int,
    origin_time: int,
    extreme_time: int,
    confirmation_time: int,
    note: str = "",
) -> None:
    seq.legs.append(
        LocalLeg(
            function=function,
            direction=direction,
            origin=origin,
            extreme=extreme,
            origin_time=origin_time,
            extreme_time=extreme_time,
            confirmation_time=confirmation_time,
            bar_time=_bar_time(extreme_time),
            note=note,
        )
    )


class TickScheduler:
    """Ordena tareas por tiempo/seq de conocimiento; no altera la verdad estructural."""

    def __init__(self) -> None:
        self.tasks: list[dict[str, Any]] = []
        self._task_seq = 0

    def schedule(
        self,
        name: str,
        due_pt: Pt,
        callback: Callable[[], None],
        priority: int = 50,
        *,
        scheduled_at: Pt | None = None,
    ) -> None:
        now = scheduled_at or due_pt
        if due_pt.time_ms < now.time_ms or due_pt.seq < now.seq:
            raise ValueError("scheduler task cannot be scheduled in the past")
        self._task_seq += 1
        self.tasks.append(
            {
                "task_id": self._task_seq,
                "name": name,
                "due_time": due_pt.time_ms,
                "due_seq": due_pt.seq,
                "scheduled_time": now.time_ms,
                "scheduled_seq": now.seq,
                "priority": priority,
                "callback": callback,
            }
        )

    def run_due(self, pt: Pt) -> list[dict[str, Any]]:
        due = [
            task
            for task in self.tasks
            if task["due_time"] <= pt.time_ms and task["due_seq"] <= pt.seq
        ]
        due.sort(key=lambda task: (task["due_time"], task["due_seq"], task["priority"], task["task_id"]))
        done: list[dict[str, Any]] = []
        for task in due:
            self.tasks.remove(task)
            task["callback"]()
            done.append(task)
        return done

    def pending(self) -> list[dict[str, Any]]:
        return list(self.tasks)


class Engine:
    def __init__(self, points: list[Pt], bars: dict[int, Bar]):
        self.points = points
        self.bars = bars
        self.movements: list[Movement] = []
        self.readings: list[Reading] = []
        self.events: list[dict] = []
        self.patterns: list[dict] = []
        self.local_sequences: list[LocalSequence] = []
        self.local_events: list[dict] = []
        self.audit: list[dict] = []
        self.knowledge_audit: list[dict] = []
        self.narrative: list[dict] = []
        self.pending: list[str] = []
        self.coverage: dict = {}
        self.active: list[Reading] = []
        self.by_id: dict[str, Reading] = {}
        self.scheduler = TickScheduler()
        self.builder = MovementBuilder(points[0]) if points else None
        self.afs2: dict = {}
        self._reading_seq = 0
        self._event_seq = 0
        self._pattern_seq = 0
        self._last_bar: int | None = None
        self._prev_price: int | None = None
        self._tick_before: dict[str, str] = {}
        self._current_pt: Pt | None = None
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
        knowledge_pt: Pt,
        reading: Reading | None,
        function: str,
        new_state: str,
        reason: str = "",
        detail: str = "",
        *,
        structural_pt: Pt | None = None,
        confirmation_pt: Pt | None = None,
    ) -> dict:
        self._event_seq += 1
        sp = structural_pt or knowledge_pt
        cp = confirmation_pt or knowledge_pt
        event = {
            "event_id": f"E{self._event_seq:06d}",
            "sequence_id": knowledge_pt.seq,
            "knowledge_sequence_id": knowledge_pt.seq,
            "structural_sequence_id": sp.seq,
            "confirmation_sequence_id": cp.seq,
            "time_ms": knowledge_pt.time_ms,
            "time": ms_to_text(knowledge_pt.time_ms),
            "knowledge_time_ms": knowledge_pt.time_ms,
            "knowledge_time": ms_to_text(knowledge_pt.time_ms),
            "structural_time_ms": sp.time_ms,
            "structural_time": ms_to_text(sp.time_ms),
            "confirmation_time_ms": cp.time_ms,
            "confirmation_time": ms_to_text(cp.time_ms),
            "bar": knowledge_pt.bar,
            "bar_time": ms_to_hms(knowledge_pt.bar * 60000)[:5],
            "structural_bar": sp.bar,
            "price": sp.price,
            "knowledge_price": knowledge_pt.price,
            "gap": self.bars.get(knowledge_pt.bar).gap if knowledge_pt.bar in self.bars else 0,
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
            "aut_source": reading.aut_source if reading else "",
            "active_function": reading.active_function if reading else "",
            "structural_valid": int(reading.structural_valid) if reading else 1,
            "operational_valid": int(reading.operational_valid) if reading else 0,
            "operational_rejection_reason": reading.operational_rejection_reason if reading else "",
            "reason": reason,
            "detail": detail,
        }
        if event["knowledge_time_ms"] < event["confirmation_time_ms"]:
            raise AssertionError(f"event {event['event_id']} known before confirmation")
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

    def _aut_limit(self, r: Reading) -> int:
        return (AUT_NUM * r.a_size) // AUT_DEN + AUT_EXTRA

    def _maybe_aut(self, r: Reading, pt: Pt, ep: Pt, movement: Movement) -> None:
        if r.aut_reclassified or r.b_size <= self._aut_limit(r):
            return
        r.aut_source = AUT_CAUSE_B
        r.aut_time = pt.time_ms
        r.aut_price = ep.price
        r.aut_reclassified = True
        r.active_function = "AUT"
        r.labels.append((movement.confirm_index, "AUT"))
        self._emit(
            "AUT",
            pt,
            r,
            "AUT",
            "AUT",
            f"SUPERA_127_MAS_025; AUT_CAUSE={AUT_CAUSE_B}",
            detail=f"AUT_SOURCE={r.aut_source}",
            structural_pt=ep,
            confirmation_pt=pt,
        )
        self._pattern("AUT", "CONFIRMADO", r, r.b_origin, r.b_extreme, "B_SUPERA_AUT", pt.time_ms)

    def _b_grande(self, r: Reading, pt: Pt, ep: Pt, movement: Movement) -> None:
        already_confirmed = bool(r.b_grande_time)
        r.b_extreme = movement.extreme
        r.b_extreme_time = ep.time_ms
        r.b_extreme_seq = ep.seq
        if not already_confirmed:
            r.b_grande_time = pt.time_ms
        r.b_knowledge_time = pt.time_ms
        r.tt_target = r.a_end + r.direction * r.module_size
        r.state = "TT_PENDING"
        r.active_function = "AUT" if r.aut_reclassified else "B_GRANDE"
        if not already_confirmed:
            r.labels.append((movement.confirm_index, "B_GRANDE"))
            self._emit(
                "B_GRANDE",
                pt,
                r,
                "B_GRANDE",
                "TT_PENDING",
                "B_100_A",
                structural_pt=ep,
                confirmation_pt=pt,
            )
            self._pattern("B_GRANDE", "CONFIRMADO", r, r.b_origin, r.b_extreme, "B>=A", pt.time_ms)
        self._maybe_aut(r, pt, ep, movement)
        self._check_tt(r, movement, pt)

    def _check_tt(self, r: Reading, movement: Movement, knowledge_pt: Pt) -> None:
        if not r.tt_target or r.tt_hit or not r.b_grande_time:
            return
        for i in range(movement.origin_index, movement.extreme_index + 1):
            p = self.points[i]
            if (r.direction > 0 and p.price >= r.tt_target) or (r.direction < 0 and p.price <= r.tt_target):
                r.tt_hit = True
                r.tt_time = p.time_ms
                r.tt_price = p.price
                r.tt_seq = p.seq
                r.tt_confirmation_time = knowledge_pt.time_ms
                r.tt_knowledge_time = knowledge_pt.time_ms
                r.tt_extreme = movement.extreme
                r.tt_extreme_time = self.points[movement.extreme_index].time_ms
                r.tt_extreme_seq = self.points[movement.extreme_index].seq
                r.state = "TT_EXT"
                r.labels.append((movement.confirm_index, "TT"))
                r.operational_valid = True
                r.operational_rejection_reason = ""
                self._emit(
                    "TT_100",
                    knowledge_pt,
                    r,
                    "TT",
                    "TT_EXT",
                    "TT_100",
                    f"target={price_s(r.tt_target)}",
                    structural_pt=p,
                    confirmation_pt=knowledge_pt,
                )
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
                self._emit(
                    "MODULO_EXT",
                    cp,
                    r,
                    "1",
                    "MODULE",
                    "NUEVO_EXTREMO",
                    structural_pt=ep,
                    confirmation_pt=cp,
                )
            else:
                r.a_origin = r.module_extreme
                r.a_origin_time = r.module_extreme_time
                r.a_origin_seq = r.module_extreme_seq
                r.a_end = movement.extreme
                r.a_end_time = ep.time_ms
                r.a_end_seq = ep.seq
                r.a_knowledge_time = cp.time_ms
                r.state = "A"
                r.labels.append((movement.confirm_index, "A"))
                self._emit(
                    "A_INICIO",
                    cp,
                    r,
                    "A",
                    "A",
                    "MOVIMIENTO_CONTRARIO",
                    structural_pt=ep,
                    confirmation_pt=cp,
                )
            return
        if r.state == "A":
            if movement.direction == r.direction:
                r.b_origin = r.a_end
                r.b_origin_time = r.a_end_time
                r.b_origin_seq = r.a_end_seq
                r.b_extreme = movement.extreme
                r.b_extreme_time = ep.time_ms
                r.b_extreme_seq = ep.seq
                r.b_knowledge_time = cp.time_ms
                r.labels.append((movement.confirm_index, "B"))
                self._emit(
                    "B_INICIO",
                    cp,
                    r,
                    "B",
                    "B",
                    "CONTRARIO_A_A",
                    structural_pt=ep,
                    confirmation_pt=cp,
                )
                if r.b_size >= r.a_size:
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
                r.a_knowledge_time = cp.time_ms
                r.labels.append((movement.confirm_index, "A"))
                self._emit(
                    "A_EXT",
                    cp,
                    r,
                    "A",
                    "A",
                    "A_CONTINUA",
                    structural_pt=ep,
                    confirmation_pt=cp,
                )
            return
        if r.state == "B_CAND":
            if movement.direction == r.direction:
                r.b_extreme = movement.extreme
                r.b_extreme_time = ep.time_ms
                r.b_extreme_seq = ep.seq
                r.b_knowledge_time = cp.time_ms
                r.labels.append((movement.confirm_index, "B"))
                self._emit(
                    "B_EXT",
                    cp,
                    r,
                    "B",
                    "B_CAND",
                    "B_CONTINUA",
                    structural_pt=ep,
                    confirmation_pt=cp,
                )
                if r.b_size >= r.a_size:
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
                    r.a_knowledge_time = cp.time_ms
                    r.state = "A"
                    r.labels.append((movement.confirm_index, "B_FALLIDA"))
                    r.labels.append((movement.confirm_index, "A"))
                    self._emit(
                        "B_FALLIDA",
                        cp,
                        r,
                        "B_FALLIDA",
                        "A",
                        "B_NO_LLEGO_A_100",
                        structural_pt=ep,
                        confirmation_pt=cp,
                    )
                else:
                    r.labels.append((movement.confirm_index, "B_OSCILACION"))
                    self._emit(
                        "B_OSCILACION",
                        cp,
                        r,
                        "B_OSCILACION",
                        "B_CAND",
                        "OSCILACION_INTERNA",
                        structural_pt=ep,
                        confirmation_pt=cp,
                    )
            return
        if r.state == "TT_PENDING":
            if movement.direction == r.direction:
                old_b = r.b_extreme
                r.b_extreme = movement.extreme
                r.b_extreme_time = ep.time_ms
                r.b_extreme_seq = ep.seq
                if r.c_origin:
                    self._emit(
                        "C_CANCELADA",
                        cp,
                        r,
                        "C_CANCELADA",
                        "TT_PENDING",
                        "B_NUEVO_EXTREMO",
                        structural_pt=ep,
                        confirmation_pt=cp,
                    )
                    r.c_origin = 0
                    r.c_extreme = 0
                if old_b != r.b_extreme and not r.aut_reclassified:
                    r.labels.append((movement.confirm_index, "B"))
                    self._emit(
                        "B_EXT",
                        cp,
                        r,
                        "B",
                        "TT_PENDING",
                        "B_CONTINUA",
                        structural_pt=ep,
                        confirmation_pt=cp,
                    )
                self._maybe_aut(r, cp, ep, movement)
                self._check_tt(r, movement, cp)
            else:
                if r.c_tick_started:
                    r.c_extreme = movement.extreme
                    r.c_extreme_time = ep.time_ms
                    r.c_knowledge_time = cp.time_ms
                else:
                    r.c_origin = r.b_extreme
                    r.c_origin_time = r.b_extreme_time
                    r.c_extreme = movement.extreme
                    r.c_extreme_time = ep.time_ms
                    r.c_knowledge_time = cp.time_ms
                    r.labels.append((movement.confirm_index, "C"))
                    self._emit(
                        "C",
                        cp,
                        r,
                        "C",
                        "TT_PENDING",
                        "CONTRARIO_A_B",
                        structural_pt=ep,
                        confirmation_pt=cp,
                    )
                if (r.direction > 0 and movement.extreme <= r.a_end - CUT_BUFFER) or (
                    r.direction < 0 and movement.extreme >= r.a_end + CUT_BUFFER
                ):
                    r.state = "DONE"
                    r.closed_time = cp.time_ms
                    r.closed_bar = cp.bar
                    r.fail_reason = "CUT_CRUZA_A_END_MAS_2"
                    r.labels.append((movement.confirm_index, "TT_FALLIDO"))
                    r.labels.append((movement.confirm_index, "CUT"))
                    self._emit(
                        "CUT",
                        cp,
                        r,
                        "CUT",
                        "DONE",
                        "CUT_CRUZA_A_END_MAS_2",
                        structural_pt=ep,
                        confirmation_pt=cp,
                    )
                    self._pattern("CUT", "CONFIRMADO", r, r.c_origin, r.c_extreme, r.fail_reason, cp.time_ms)
            return
        if r.state == "TT_EXT":
            if movement.direction == r.direction:
                r.tt_extreme = movement.extreme
                r.tt_extreme_time = ep.time_ms
                r.tt_extreme_seq = ep.seq
                self._emit(
                    "TT_EXT",
                    cp,
                    r,
                    "TT",
                    "TT_EXT",
                    "TT_EXTIENDE",
                    structural_pt=ep,
                    confirmation_pt=cp,
                )
            else:
                r.ft = True
                r.ft_time = cp.time_ms
                r.ft_price = movement.extreme
                r.ft_structural_time = ep.time_ms
                r.state = "DONE"
                r.closed_time = cp.time_ms
                r.closed_bar = cp.bar
                r.labels.append((movement.confirm_index, "FT"))
                self._emit(
                    "FT",
                    cp,
                    r,
                    "FT",
                    "DONE",
                    "CONTRARIO_DESPUES_DE_TT",
                    structural_pt=ep,
                    confirmation_pt=cp,
                )
                self._pattern("FT", "CONFIRMADO", r, r.tt_extreme, movement.extreme, "FT", cp.time_ms)

    def _open_candidate(
        self,
        movement: Movement,
        snapshots: list[tuple[Reading, str, int, int, int, int, bool]],
    ) -> tuple[str, Reading | None, int, int, int, int, int, int] | None:
        # A primary reading may have been closed by the just-processed movement.
        # Decide whether FIRST is needed from the live primary set after updates;
        # pre-update snapshots are only for transition rules. Local readings do
        # not suppress a new primary reading.
        if not any(
            r.state != "DONE" and not getattr(r, "local_sequence_id", "")
            for r in self.active
        ):
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
        primary_active = [r for r in self.active if r.state != "DONE" and not getattr(r, "local_sequence_id", "")]
        snapshots = [
            (r, r.state, r.a_size, r.x_size, r.direction, r.a_end, r.a_sig_opened)
            for r in primary_active
        ]
        for r in primary_active:
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
            primary_live = [r for r in self.active if r.state != "DONE" and not getattr(r, "local_sequence_id", "")]
            if len(primary_live) > MAX_ACTIVE:
                keep = {r.reading_id for r in sorted(primary_live, key=lambda item: (-item.x_size, -item.created_time))[:MAX_ACTIVE]}
                for old in list(primary_live):
                    if old.reading_id not in keep:
                        self._done(old, cp, "DONE", "ARCHIVADA_POR_CAPACIDAD")
                        old.labels.append((movement.confirm_index, "ARCHIVADA"))
                        self._emit("ARCHIVADA", cp, old, "ARCHIVADA", "DONE", "MAX_3_LECTURAS_ACTIVAS")
                        if old in self.active:
                            self.active.remove(old)
        for r in list(self.active):
            if not getattr(r, "local_sequence_id", "") and r.a_sig_opened and r.a_size > A_MAX_MODULE_MULTIPLE * r.x_size:
                self._done(r, cp, "DONE", "A_DESPROPORCIONADA_MODULO")
                r.labels.append((movement.confirm_index, "A_DESPROPORCIONADA_MODULO"))
                self._emit("A_DESPROPORCIONADA_MODULO", cp, r, "A_DESPROPORCIONADA_MODULO", "DONE", "A_MAYOR_2X_MODULO")
                if r in self.active:
                    self.active.remove(r)

    def _schedule_gap(self, p: Pt) -> None:
        bar = self.bars.get(p.bar)
        if bar is None or abs(bar.gap) < PLANO_TICK:
            return

        def emit_gap() -> None:
            self._emit(
                "GAP",
                p,
                None,
                "GAP",
                "GAP",
                f"gap={price_s(bar.gap)}",
                f"gap={price_s(bar.gap)}",
                structural_pt=p,
                confirmation_pt=p,
            )

        self.scheduler.schedule("GAP", p, emit_gap, priority=0, scheduled_at=p)

    def _owner(self, p: Pt) -> tuple[Reading | None, str, int]:
        candidates: list[tuple[int, int, str, Reading, str]] = []
        for r in self.active:
            if r.state == "DONE":
                continue
            source = ""
            if r.c_origin and r.c_extreme and min(r.c_origin, r.c_extreme) <= p.price <= max(r.c_origin, r.c_extreme):
                source = "C"
            elif r.b_origin and r.b_extreme and min(r.b_origin, r.b_extreme) <= p.price <= max(r.b_origin, r.b_extreme):
                source = "B"
            elif r.a_origin and r.a_end and min(r.a_origin, r.a_end) <= p.price <= max(r.a_origin, r.a_end):
                source = "A"
            elif min(r.module_origin, r.module_extreme) <= p.price <= max(r.module_origin, r.module_extreme):
                source = "MODULE"
            if source:
                candidates.append((r.module_size, r.created_time, r.reading_id, r, source))
        if not candidates:
            if self._prev_price is not None and abs(p.price - self._prev_price) < STRUCTURAL_MOVE:
                return None, "NOISE", 0
            return None, "NONE", 0
        candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
        _, _, _, owner, source = candidates[0]
        return owner, source, len(candidates)

    def _record_knowledge(self, p: Pt) -> None:
        events_here = [event for event in self.events if event["knowledge_sequence_id"] == p.seq]
        owner, source, ownership = self._owner(p)
        active_ids = [r.reading_id for r in self.active if r.state != "DONE"]
        inherited = [rid for rid in active_ids if self.by_id[rid].created_bar < p.bar]
        local = [rid for rid in active_ids if self.by_id[rid].created_bar == p.bar]
        after = {r.reading_id: r.state for r in self.active if r.state != "DONE"}
        self.knowledge_audit.append(
            {
                "sequence_id": p.seq,
                "time": ms_to_text(p.time_ms),
                "time_ms": p.time_ms,
                "price": p.price,
                "bar_time": ms_to_hms(p.bar * 60000)[:5],
                "gap": self.bars[p.bar].gap if p.bar in self.bars else 0,
                "local_direction": ("UP" if owner.direction > 0 else "DOWN") if owner else "",
                "structural_origin": owner.module_origin if owner else 0,
                "structural_extreme": owner.module_extreme if owner else 0,
                "excursion": abs(p.price - owner.module_origin) if owner else 0,
                "owner_reading_id": owner.reading_id if owner else "",
                "owner_source": source,
                "owner_created_time": ms_to_text(owner.created_time) if owner else "",
                "owner_known_at_seq": owner.created_seq if owner else 0,
                "ownership_count": ownership,
                "functional_coverage": "OK" if owner or source == "NOISE" else "UNCOVERED",
                "active_readings": ";".join(active_ids),
                "inherited_readings": ";".join(inherited),
                "local_readings": ";".join(local),
                "functions_before": ";".join(f"{rid}:{st}" for rid, st in sorted(self._tick_before.items())),
                "functions_after": ";".join(f"{rid}:{st}" for rid, st in sorted(after.items())),
                "events_emitted": ";".join(event["event_id"] for event in events_here),
                "readings_created": ";".join(
                    event["reading_id"] for event in events_here if event["kind"] == "LECTURA_CREADA"
                ),
                "patterns_updated": ";".join(event["function"] for event in events_here if event["function"]),
                "decision_reason": ";".join(event["reason"] for event in events_here if event["reason"]) or "NO_ACTION",
            }
        )

    def run(self) -> "Engine":
        for index, p in enumerate(self.points):
            self._current_pt = p
            self._tick_before = {r.reading_id: r.state for r in self.active if r.state != "DONE"}
            if self._last_bar is None or p.bar != self._last_bar:
                self._schedule_gap(p)
            self.scheduler.run_due(p)
            if index:
                movement = self.builder.feed(p, index) if self.builder is not None else None
                if movement is not None:
                    self.movements.append(movement)
                    self._process_movement(movement)
            self._record_knowledge(p)
            self._prev_price = p.price
            self._last_bar = p.bar
        last = self.points[-1] if self.points else Pt(0, 0, 0, 0)
        self._emit("FIN_FEED", last, None, "", "END", "END_OF_FEED", "fin del feed")
        self._finalize()
        return self

    def _finalize(self) -> None:
        self.coverage = evaluate_coverage(self)
        self.audit = build_audit(self)
        self.narrative = build_narrative(self)
        self.pending = [
            "post_tt_fallido_no_definido",
            "ft_expiracion_no_definida",
            "entrada_tardia_ft_no_definida",
            "a_mayor_que_modulo_guardia_provisional",
            "aut_extra_tick_unidad_cerrada_0_25",
            "cobertura_estructural_definicion_por_confirmar",
        ]
        if not self.coverage.get("causal_functional_ok", False):
            self.pending.append("functional_coverage_causal_parcial")
        if not self.coverage.get("causal_geometric_ok", False):
            self.pending.append("geometric_coverage_causal_parcial")
        for r in self.readings:
            if r.state != "DONE":
                self.pending.append(f"lectura_abierta_al_final:{r.reading_id}")
                break
        self.local_sequences = []  # Retrospective local detector removed in v0.7.5.2.
        known_time = self.points[-1].time_ms if self.points else 0
        for sequence in self.local_sequences:
            for leg in sequence.legs:
                if leg.confirmation_time > known_time:
                    continue
                self.local_events.append(
                    {
                        "local_event_id": f"L{len(self.local_events) + 1:05d}",
                        "sequence_id": sequence.sequence_id,
                        "function": leg.function,
                        "direction": "UP" if leg.direction > 0 else "DOWN",
                        "origin": leg.origin,
                        "extreme": leg.extreme,
                        "size": leg.size,
                        "bar_time": leg.bar_time,
                        "origin_time": ms_to_text(leg.origin_time),
                        "extreme_time": ms_to_text(leg.extreme_time),
                        "confirmation_time": ms_to_text(leg.confirmation_time),
                        "knowledge_time": ms_to_text(leg.confirmation_time),
                        "origin_time_ms": leg.origin_time,
                        "extreme_time_ms": leg.extreme_time,
                        "confirmation_time_ms": leg.confirmation_time,
                        "knowledge_time_ms": leg.confirmation_time,
                        "module_origin": sequence.module_origin,
                        "module_extreme": sequence.module_extreme,
                        "module_size": sequence.module_size,
                        "note": leg.note,
                    }
                )
        self.afs2 = evaluate_afs2(self, prefix_failures=None)


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
                        "origin_seq": origin.seq,
                        "extreme_seq": ext.seq,
                        "confirm_time": p.time_ms,
                        "confirm_seq": p.seq,
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
                        "origin_seq": origin.seq,
                        "extreme_seq": ext.seq,
                        "confirm_time": p.time_ms,
                        "confirm_seq": p.seq,
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


def _known_by(r: Reading, time_ms: int, seq: int) -> bool:
    return r.created_time <= time_ms and r.created_seq <= seq


def evaluate_coverage(engine: Engine) -> dict:
    swings = structural_swings(engine.points, STRUCTURAL_MOVE)
    geometric_uncovered: list[dict] = []
    functional_uncovered: list[dict] = []
    causal_geometric_uncovered: list[dict] = []
    causal_functional_uncovered: list[dict] = []
    for swing in swings:
        geometric = any(_range_contains(r, swing["origin"], swing["extreme"]) for r in engine.readings)
        functional = any(
            _range_contains(r, swing["origin"], swing["extreme"]) and r.a_origin
            for r in engine.readings
        )
        causal_geometric = any(
            _known_by(r, swing["confirm_time"], swing["confirm_seq"])
            and _range_contains(r, swing["origin"], swing["extreme"])
            for r in engine.readings
        )
        causal_functional = any(
            _known_by(r, swing["confirm_time"], swing["confirm_seq"])
            and r.a_knowledge_time
            and r.a_knowledge_time <= swing["confirm_time"]
            and _range_contains(r, swing["origin"], swing["extreme"])
            for r in engine.readings
        )
        if not geometric:
            geometric_uncovered.append(swing)
        if not functional:
            functional_uncovered.append(swing)
        if not causal_geometric:
            causal_geometric_uncovered.append(swing)
        if not causal_functional:
            causal_functional_uncovered.append(swing)
    movements = engine.movements
    functional_movements = 0
    causal_functional_movements = 0
    for m in movements:
        confirm = engine.points[m.confirm_index]
        if any(_range_contains(r, m.origin, m.extreme) and r.a_origin for r in engine.readings):
            functional_movements += 1
        if any(
            _known_by(r, confirm.time_ms, confirm.seq)
            and r.a_knowledge_time
            and r.a_knowledge_time <= confirm.time_ms
            and _range_contains(r, m.origin, m.extreme)
            for r in engine.readings
        ):
            causal_functional_movements += 1
    owner_rows = [row for row in engine.knowledge_audit if row["functional_coverage"] == "OK"]
    uncovered_rows = [row for row in engine.knowledge_audit if row["functional_coverage"] == "UNCOVERED"]
    return {
        "structural_swing_count": len(swings),
        "geometric_count": len(swings) - len(geometric_uncovered),
        "functional_count": len(swings) - len(functional_uncovered),
        "causal_geometric_count": len(swings) - len(causal_geometric_uncovered),
        "causal_functional_count": len(swings) - len(causal_functional_uncovered),
        "geometric_uncovered": geometric_uncovered,
        "functional_uncovered": functional_uncovered,
        "causal_geometric_uncovered": causal_geometric_uncovered,
        "causal_functional_uncovered": causal_functional_uncovered,
        "geometric_ok": not geometric_uncovered,
        "functional_ok": not functional_uncovered,
        "causal_geometric_ok": not causal_geometric_uncovered,
        "causal_functional_ok": not causal_functional_uncovered,
        "movement_count": len(movements),
        "functional_movement_count": functional_movements,
        "causal_functional_movement_count": causal_functional_movements,
        "movement_coverage_ok": functional_movements == len(movements),
        "causal_movement_coverage_ok": causal_functional_movements == len(movements),
        "tick_count": len(engine.knowledge_audit),
        "owner_tick_count": len(owner_rows),
        "noise_tick_count": sum(1 for row in engine.knowledge_audit if row["owner_source"] == "NOISE"),
        "uncovered_tick_count": len(uncovered_rows),
        "owner_coverage_ok": not uncovered_rows,
    }


def build_audit(engine: Engine) -> list[dict]:
    return list(engine.knowledge_audit)


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
        audit_rows = [row for row in engine.knowledge_audit if row["bar_time"] == bar.name]
        close_row = audit_rows[-1] if audit_rows else {}
        active = close_row.get("active_readings", "").split(";") if close_row.get("active_readings") else []
        pending = [
            item.split(":", 1)[1]
            for item in close_row.get("functions_after", "").split(";")
            if ":" in item
        ]
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
                "pending": ";".join(pending),
            }
        )
    return rows


EVENT_FIELDS = [
    "event_id",
    "sequence_id",
    "knowledge_sequence_id",
    "structural_sequence_id",
    "confirmation_sequence_id",
    "time",
    "time_ms",
    "knowledge_time",
    "knowledge_time_ms",
    "structural_time",
    "structural_time_ms",
    "confirmation_time",
    "confirmation_time_ms",
    "bar",
    "bar_time",
    "structural_bar",
    "price",
    "knowledge_price",
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
    "created_seq",
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
    "tt_confirmation_time",
    "tt_knowledge_time",
    "tt_real_extreme",
    "ft",
    "ft_time",
    "ft_price",
    "ft_structural_time",
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
    "owner_reading_id",
    "owner_source",
    "owner_created_time",
    "owner_known_at_seq",
    "ownership_count",
    "functional_coverage",
    "active_readings",
    "inherited_readings",
    "local_readings",
    "functions_before",
    "functions_after",
    "events_emitted",
    "readings_created",
    "patterns_updated",
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
            "knowledge_price",
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


def write_outputs(engine: Engine, out_dir: Path | str, stem: str = "v075") -> list[Path]:
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
        "local_sequences": out_dir / f"{stem}_LocalSecuencias.csv",
        "local_events": out_dir / f"{stem}_LocalEventos.csv",
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
                "created_seq": r.created_seq,
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
                "tt_confirmation_time": ms_to_text(r.tt_confirmation_time) if r.tt_confirmation_time else "",
                "tt_knowledge_time": ms_to_text(r.tt_knowledge_time) if r.tt_knowledge_time else "",
                "tt_real_extreme": r.tt_extreme,
                "ft": int(r.ft),
                "ft_time": ms_to_text(r.ft_time) if r.ft_time else "",
                "ft_price": r.ft_price,
                "ft_structural_time": ms_to_text(r.ft_structural_time) if r.ft_structural_time else "",
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
    with paths["local_sequences"].open("w", newline="", encoding="utf-8-sig") as fh:
        fields = [
            "sequence_id",
            "direction",
            "bars",
            "module_origin",
            "module_extreme",
            "module_size",
            "module_origin_time",
            "module_extreme_time",
            "module_origin_seq",
            "module_extreme_seq",
            "legs",
        ]
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for sequence in engine.local_sequences:
            writer.writerow(
                _price_fields(
                    {
                        "sequence_id": sequence.sequence_id,
                        "direction": "UP" if sequence.direction > 0 else "DOWN",
                        "bars": sequence.bars,
                        "module_origin": sequence.module_origin,
                        "module_extreme": sequence.module_extreme,
                        "module_size": sequence.module_size,
                        "module_origin_time": ms_to_text(sequence.module_origin_time),
                        "module_extreme_time": ms_to_text(sequence.module_extreme_time),
                        "module_origin_seq": sequence.module_origin_seq,
                        "module_extreme_seq": sequence.module_extreme_seq,
                        "legs": ";".join(
                            f"{leg.function}:{price_s(leg.origin)}->{price_s(leg.extreme)}@{leg.bar_time}"
                            for leg in sequence.legs
                        ),
                    },
                    fields,
                )
            )
    with paths["local_events"].open("w", newline="", encoding="utf-8-sig") as fh:
        fields = [
            "local_event_id",
            "sequence_id",
            "function",
            "direction",
            "origin",
            "extreme",
            "size",
            "bar_time",
            "origin_time",
            "extreme_time",
            "confirmation_time",
            "knowledge_time",
            "origin_time_ms",
            "extreme_time_ms",
            "confirmation_time_ms",
            "knowledge_time_ms",
            "module_origin",
            "module_extreme",
            "module_size",
            "note",
        ]
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in engine.local_events:
            writer.writerow(_price_fields(row, fields))
    info = {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "feed_points": len(engine.points),
        "bars": len(engine.bars),
        "movements": len(engine.movements),
        "readings": len(engine.readings),
        "events": len(engine.events),
        "patterns": len(engine.patterns),
        "local_sequences": len(engine.local_sequences),
        "local_events": len(engine.local_events),
        "active_readings": len(engine.active),
        "AFS2_READY": bool(engine.afs2.get("AFS2_READY", False)),
        "causality": {
            "event_count": len(engine.events),
            "all_knowledge_after_structural": all(
                event["knowledge_time_ms"] >= event["structural_time_ms"] for event in engine.events
            ),
            "all_knowledge_after_confirmation": all(
                event["knowledge_time_ms"] >= event["confirmation_time_ms"] for event in engine.events
            ),
            "event_ids_append_only": [e["event_id"] for e in engine.events]
            == [f"E{index:06d}" for index in range(1, len(engine.events) + 1)],
            "sequence_ids_real_feed": all(
                event["sequence_id"] == event["knowledge_sequence_id"]
                for event in engine.events
            ),
            "tt_requires_b_grande": all(
                (not r.tt_hit) or (r.b_grande_time and r.tt_knowledge_time >= r.b_grande_time)
                for r in engine.readings
            ),
        },
        "AFS2": engine.afs2,
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
            "owner_coverage_partial_is_informative",
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


PREFIX_EVENT_FIELDS = [
    "event_id",
    "sequence_id",
    "knowledge_sequence_id",
    "structural_sequence_id",
    "confirmation_sequence_id",
    "time_ms",
    "structural_time_ms",
    "confirmation_time_ms",
    "kind",
    "function",
    "new_state",
    "reading_id",
    "parent_reading_id",
    "price",
    "module_origin",
    "module_extreme",
    "a_origin",
    "a_end",
    "b_origin",
    "b_extreme",
    "c_origin",
    "c_extreme",
    "tt_target",
    "tt_100",
    "ft",
    "reason",
]


def _prefix_events(engine: Engine, cutoff: int) -> list[dict]:
    return [
        event
        for event in engine.events
        if event["knowledge_time_ms"] <= cutoff and event["kind"] != "FIN_FEED"
    ]


def compare_prefix(full: Engine, prefix: Engine, cutoff: int) -> dict:
    full_events = _prefix_events(full, cutoff)
    prefix_events = _prefix_events(prefix, cutoff)
    mismatch = None
    limit = min(len(full_events), len(prefix_events))
    for index in range(limit):
        left = tuple(full_events[index][field] for field in PREFIX_EVENT_FIELDS)
        right = tuple(prefix_events[index][field] for field in PREFIX_EVENT_FIELDS)
        if left != right:
            mismatch = {
                "index": index,
                "full": full_events[index],
                "prefix": prefix_events[index],
                "fields": [
                    field
                    for field in PREFIX_EVENT_FIELDS
                    if full_events[index][field] != prefix_events[index][field]
                ],
            }
            break
    if mismatch is None and len(full_events) != len(prefix_events):
        index = limit
        mismatch = {
            "index": index,
            "full": full_events[index] if index < len(full_events) else None,
            "prefix": prefix_events[index] if index < len(prefix_events) else None,
            "fields": ["event_count"],
        }
    return {
        "cutoff_time": ms_to_text(cutoff),
        "cutoff_ms": cutoff,
        "full_events": len(full_events),
        "prefix_events": len(prefix_events),
        "full_readings": len(full.readings),
        "prefix_readings": len(prefix.readings),
        "pass": mismatch is None,
        "mismatch": mismatch,
    }


def run_prefix_matrix(
    points: list[Pt],
    bars: dict[int, Bar],
    cutoffs: list[int],
    full: Engine | None = None,
) -> tuple[Engine, list[dict]]:
    full = full or run_engine(points, bars)
    rows: list[dict] = []
    for cutoff in sorted(set(cutoffs)):
        prefix_points = [p for p in points if p.time_ms <= cutoff]
        if not prefix_points:
            continue
        prefix = run_engine(prefix_points, bars)
        row = compare_prefix(full, prefix, cutoff)
        rows.append(row)
    failures = sum(1 for row in rows if not row["pass"])
    full.afs2 = evaluate_afs2(full, prefix_failures=failures)
    return full, rows


def evaluate_afs2(engine: Engine, prefix_failures: int | None = None) -> dict:
    expected_ids = [f"E{index:06d}" for index in range(1, len(engine.events) + 1)]
    event_ids = [event["event_id"] for event in engine.events]
    event_append_only = event_ids == expected_ids
    feed_sequences = [p.seq for p in engine.points]
    sequence_ids = [event["sequence_id"] for event in engine.events]
    sequence_real = (
        all(event["sequence_id"] == event["knowledge_sequence_id"] for event in engine.events)
        and all(event["sequence_id"] in set(feed_sequences) for event in engine.events)
        and sequence_ids == sorted(sequence_ids)
    )
    knowledge_valid = all(
        event["knowledge_time_ms"] >= event["confirmation_time_ms"]
        and event["knowledge_time_ms"] >= event["structural_time_ms"]
        for event in engine.events
    )
    tt_after_b = all(
        (not r.tt_hit)
        or (
            r.b_grande_time
            and r.tt_knowledge_time
            and r.tt_knowledge_time >= r.b_grande_time
            and r.b_size >= r.a_size
        )
        for r in engine.readings
    )
    tt_targets_valid = all(
        (not r.tt_hit) or r.tt_target == r.a_end + r.direction * r.module_size
        for r in engine.readings
    )
    gap_first = True
    event_by_seq: dict[int, list[dict]] = defaultdict(list)
    for event in engine.events:
        event_by_seq[event["sequence_id"]].append(event)
    for bar_idx in sorted({p.bar for p in engine.points}):
        bar = engine.bars.get(bar_idx)
        if bar is None or not bar.gap:
            continue
        first = next((p for p in engine.points if p.bar == bar_idx), None)
        if first is None:
            continue
        events = event_by_seq.get(first.seq, [])
        if not events or events[0]["kind"] != "GAP":
            gap_first = False
            break
    geometry_generic = any(r.tt_hit and r.ft for r in engine.readings) and tt_targets_valid
    coverage = engine.coverage
    owner_sources = {"C", "B", "A", "MODULE", "NOISE", "NONE"}
    owner_audit_complete = (
        len(engine.knowledge_audit) == len(engine.points)
        and all(
            row["owner_source"] in owner_sources
            and row["functional_coverage"] in {"OK", "UNCOVERED"}
            and (not row["owner_reading_id"] or row["owner_known_at_seq"] <= row["sequence_id"])
            for row in engine.knowledge_audit
        )
    )
    causal_counts_valid = (
        coverage.get("causal_geometric_count", 0) <= coverage.get("geometric_count", 0)
        and coverage.get("causal_functional_count", 0) <= coverage.get("functional_count", 0)
        and coverage.get("causal_functional_movement_count", 0) <= coverage.get("movement_count", 0)
    )
    forbidden = FORBIDDEN_FUNCTIONS & {event["function"] for event in engine.events}
    prefix_ok = None if prefix_failures is None else prefix_failures == 0
    checks = {
        "prefix_failures": prefix_failures,
        "prefix_ok": prefix_ok,
        "event_id_append_only": event_append_only,
        "sequence_id_real_feed": sequence_real,
        "knowledge_time_valid": knowledge_valid,
        "tt_after_b_grande": tt_after_b,
        "tt_target_formula": tt_targets_valid,
        "gap_before_other_branches": gap_first,
        "geometry_invariants": geometry_generic,
        "owner_audit_complete": owner_audit_complete,
        "causal_counts_valid": causal_counts_valid,
        "vocabulary_clean": not forbidden,
    }
    ready = all(
        value is True
        for key, value in checks.items()
        if key not in {"prefix_failures"}
    ) and prefix_ok is True
    return {
        "AFS2_READY": ready,
        "AFS2_SCOPE": "integridad causal y prefijos; no implica cobertura funcional total",
        "checks": checks,
        "coverage": {
            "owner_coverage_ok": bool(coverage.get("owner_coverage_ok", False)),
            "owner_tick_count": coverage.get("owner_tick_count", 0),
            "uncovered_tick_count": coverage.get("uncovered_tick_count", 0),
            "causal_geometric_ok": bool(coverage.get("causal_geometric_ok", False)),
            "causal_functional_ok": bool(coverage.get("causal_functional_ok", False)),
            "causal_geometric_count": coverage.get("causal_geometric_count", 0),
            "causal_functional_count": coverage.get("causal_functional_count", 0),
            "geometric_count": coverage.get("geometric_count", 0),
            "functional_count": coverage.get("functional_count", 0),
        },
        "unresolved_rules": list(engine.pending),
        "unresolved_blocking": [],
    }




class CanonicalEngine(Engine):
    """Sequential adapter. Only consumed ticks are stored in the engine state."""
    def __init__(self, points: list[Pt] | None = None, bars: dict[int, Bar] | None = None):
        source=list(points or [])
        super().__init__(source, {})
        self._pending_points=source
        self.points=[]
        self.bars={}
        self.builder=None
        self.start_time=0
        self.end_time=0
        self._last_bar=None
        self._prev_price=None
        self._local={"cursor":0,"armed":False,"aut_bar":None,"candidate_bar":None,
                     "candidate_direction":0,"state":None,"last_bar":None,
                     "last_price":None,"two_bar":None,"two_extreme":None,
                     "a_origin":None,"a_extreme":None,"b_origin":None,
                     "phase":"IDLE","rejected":False}
        self._finalized=False

    def _emit(self, *args, **kwargs):
        event=super()._emit(*args, **kwargs)
        reading=args[2] if len(args)>2 else kwargs.get("reading")
        local_id=getattr(reading,"local_sequence_id","") if reading else ""
        event["local_sequence_id"]=local_id
        event["dominant"]=int(bool(getattr(reading,"dominant",False))) if reading else 0
        if local_id:
            event["local_event_id"]=f"L{len(self.local_events)+1:05d}"
        return event

    def _bar_for_tick(self,p:Pt)->tuple[Bar,bool]:
        old=self.bars.get(p.bar)
        if old is None:
            prior=self.bars[max(self.bars)].last.price if self.bars else None
            gap=p.price-prior if prior is not None else 0
            bar=Bar(p.bar,ms_to_hms(p.bar*60000)[:5],p,p,p,p,prior,gap)
            self.bars[p.bar]=bar
            return bar,True
        if p.price>old.high.price:old.high=p
        if p.price<old.low.price:old.low=p
        old.last=p
        return old,False

    def _dominant_parent(self)->Reading|None:
        chosen=[r for r in self.active if r.state!="DONE" and getattr(r,"dominant",False)]
        return chosen[-1] if chosen else (self.active[-1] if self.active else None)

    def _make_local_reading(self,p:Pt,direction:int,origin:Pt,extreme:Pt,parent:Reading|None,seq_id:str,reason:str)->Reading:
        live=[r for r in self.active if r.state!="DONE"]
        for old in live:setattr(old,"dominant",False)
        while len(live)>=MAX_ACTIVE:
            archive=min(live,key=lambda item:(item.module_size,item.created_time,item.reading_id))
            self._done(archive,p,"DONE","INTEGRADA_POR_LIMITE_GLOBAL_3")
            archive.labels.append((len(self.points)-1,"INTEGRADA"))
            self._emit("INTEGRADA",p,archive,"INTEGRADA","DONE","MAX_3_LECTURAS_ACTIVAS")
            if archive in self.active:self.active.remove(archive)
            live.remove(archive)
        self._local_reading_seq=getattr(self,"_local_reading_seq",0)+1
        r=Reading(reading_id=f"LR{self._local_reading_seq:04d}",direction=direction,state="LOCAL_MODULE",
            created_time=p.time_ms,created_seq=p.seq,created_bar=p.bar,origin_reason=reason,
            module_origin=origin.price,module_extreme=extreme.price,module_origin_time=origin.time_ms,
            module_extreme_time=extreme.time_ms,module_origin_seq=origin.seq,module_extreme_seq=extreme.seq,
            parent_reading_id=parent.reading_id if parent else "")
        r.local_sequence_id=seq_id;r.dominant=True
        r.labels.append((len(self.points)-1,"1"));r.leg_indices.append(len(self.points)-1)
        self.readings.append(r);self.by_id[r.reading_id]=r;self.active.append(r)
        self._pattern("LECTURA_FUNCIONAL","ACTIVA",r,origin.price,extreme.price,reason,p.time_ms)
        self._emit("LECTURA_CREADA",p,r,"1","LOCAL_MODULE",reason,
                   structural_pt=origin,confirmation_pt=extreme)
        return r

    def _local_leg(self,p:Pt,function:str,reading:Reading,origin:Pt,extreme:Pt,reason:str,state:str,
                   function_direction:int|None=None)->dict|None:
        local=self._local["state"]
        if local is None:return None
        reading.active_function="B_GRANDE" if state=="LOCAL_B_GRANDE" else ("C" if function=="C" else function)
        size=abs(extreme.price-origin.price)
        # A-source AUT confirms by crossing the contradicted module base; the
        # excess beyond that base can be sub-2 points and is not a module size.
        if function in {"A","B","C"} and size<MOVE:return None
        if function_direction is None:
            function_direction = -reading.direction if function=="A" or (function=="AUT" and reason.startswith("A_")) else reading.direction
        _add_local_leg(local["sequence"],function,function_direction,origin.price,extreme.price,
                       origin.time_ms,extreme.time_ms,p.time_ms,reason)
        reading.labels.append((len(self.points)-1,function));reading.leg_indices.append(len(self.points)-1)
        event=self._emit("LOCAL_FUNCTION",p,reading,function,state,reason,
                         structural_pt=origin,confirmation_pt=p)
        # The enclosing reading can still have its prior direction at the AUT
        # instant. Report the emitted function's causal direction explicitly.
        event["direction"]=function_direction
        event["aut_source"]=reading.aut_source if function=="AUT" else ""
        self.local_events.append({"local_event_id":event["local_event_id"],
            "sequence_id":local["sequence"].sequence_id,"function":function,
            "direction":"UP" if function_direction>0 else "DOWN","origin":origin.price,
            "extreme":extreme.price,"size":abs(extreme.price-origin.price),
            "bar_time":_bar_time(extreme.time_ms),"origin_time":ms_to_text(origin.time_ms),
            "extreme_time":ms_to_text(extreme.time_ms),"confirmation_time":ms_to_text(p.time_ms),
            "knowledge_time":ms_to_text(p.time_ms),"origin_time_ms":origin.time_ms,
            "extreme_time_ms":extreme.time_ms,"confirmation_time_ms":p.time_ms,
            "knowledge_time_ms":p.time_ms,"module_origin":reading.module_origin,
            "module_extreme":reading.module_extreme,"module_size":reading.module_size,"note":reason})
        self.local_events[-1]["aut_source"]=reading.aut_source if function=="AUT" else ""
        return event

    def _local_gate_event(self,p:Pt,reading:Reading,reason:str)->None:
        self._emit("LOCAL_2_GATE",p,reading,"","MODULE",reason,detail=reason)

    def _observe_core_aut(self,p:Pt)->None:
        local=self._local
        for event in self.events[local["cursor"]:]:
            if event.get("kind")=="AUT" and not event.get("local_sequence_id") and local["state"] is None:
                local["armed"]=True;local["aut_bar"]=p.bar
                local["candidate_direction"]=int(event.get("direction") or 0)
        local["cursor"]=len(self.events)

    def _close_candidate_bar(self,bar:Bar,knowledge:Pt)->None:
        local=self._local
        if local["candidate_bar"]!=bar.idx or local["state"] is not None:return
        direction=1 if bar.last.price>bar.open.price else -1 if bar.last.price<bar.open.price else 0
        span=bar.high.price-bar.low.price
        if direction==0 or direction!=local["candidate_direction"] or span<MOVE:
            local["candidate_bar"]=None
            return
        origin,extreme=(bar.high,bar.low) if direction<0 else (bar.low,bar.high)
        seq=LocalSequence(sequence_id=f"LS{len(self.local_sequences)+1:04d}",direction=direction,
            bars=bar.name,module_origin=origin.price,module_extreme=extreme.price,
            module_origin_time=origin.time_ms,module_extreme_time=extreme.time_ms,
            module_origin_seq=origin.seq,module_extreme_seq=extreme.seq)
        self.local_sequences.append(seq)
        parent=self._dominant_parent()
        reading=self._make_local_reading(knowledge,direction,origin,extreme,parent,seq.sequence_id,
                                         "LOCAL_1_CAUSAL_POR_AUT_PREVIO")
        _add_local_leg(seq,"1",direction,origin.price,extreme.price,origin.time_ms,extreme.time_ms,
                       knowledge.time_ms,"1 local confirmado al cerrar el tramo observable")
        event=self.events[-1]
        self.local_events.append({"local_event_id":event["local_event_id"],"sequence_id":seq.sequence_id,
            "function":"1","direction":"UP" if direction>0 else "DOWN","origin":origin.price,
            "extreme":extreme.price,"size":span,"bar_time":bar.name,
            "origin_time":ms_to_text(origin.time_ms),"extreme_time":ms_to_text(extreme.time_ms),
            "confirmation_time":ms_to_text(bar.last.time_ms),"knowledge_time":ms_to_text(knowledge.time_ms),
            "origin_time_ms":origin.time_ms,"extreme_time_ms":extreme.time_ms,
            "confirmation_time_ms":bar.last.time_ms,"knowledge_time_ms":knowledge.time_ms,
            "module_origin":origin.price,"module_extreme":extreme.price,"module_size":span,
            "note":"1 local confirmado causalmente desde ticks de la vela cerrada"})
        local["state"]={"sequence":seq,"reading":reading,"direction":direction,
            "module_origin":origin,"module_extreme":extreme,"one_size":span,
            # Keep the contradicted module's functional base distinct from the
            # geometry of a new dominant 1 created by AUT.
            "aut_base":origin,
            "aut_count":0,
            "bar1":bar.idx,"bar2":None,"two_open":None,"two_confirmed":False,
            "requires_base":True}
        local["phase"]="WAIT_TWO";local["candidate_bar"]=None

    def _new_local_reading_after_aut(self,p:Pt,old:Reading,direction:int,origin:Pt,extreme:Pt,reason:str,aut_source:str,
                                     new1_origin:Pt|None=None)->None:
        local=self._local;state=local["state"]
        if state is None:return
        new1_origin=new1_origin or origin
        old.aut_reclassified=True;old.aut_time=p.time_ms;old.aut_price=p.price
        old.aut_source=aut_source
        event_reason=f"{aut_source}:{reason}"
        self._local_leg(p,"AUT",old,origin,extreme,event_reason,"AUT_LOCAL_CONFIRMADO",
                        function_direction=direction)
        self._emit("LECTURA_INTEGRADA",p,old,"","LOCAL_INTEGRADA","AUT_NUEVO_1_DOMINANTE",
                   detail=f"AUT_SOURCE={aut_source}; genealogia conservada en la lectura vigente")
        old.dominant=False
        self._done(old,p,"DONE","INTEGRADA_POR_AUT_NUEVO_1")
        old.labels.append((len(self.points)-1,"INTEGRADA"))
        self._emit("LECTURA_CERRADA",p,old,"INTEGRADA","DONE","INTEGRADA_POR_AUT_NUEVO_1")
        if old in self.active:self.active.remove(old)
        new=self._make_local_reading(p,direction,new1_origin,extreme,old,state["sequence"].sequence_id,
                                     "AUT_NUEVO_1_DOMINANTE")
        new.aut_source=aut_source
        state["reading"]=new;state["direction"]=direction
        state["module_origin"]=new1_origin;state["module_extreme"]=extreme
        state["sequence"].direction=direction
        state["sequence"].module_origin=new1_origin.price;state["sequence"].module_extreme=extreme.price
        state["sequence"].module_origin_time=new1_origin.time_ms;state["sequence"].module_extreme_time=extreme.time_ms
        state["sequence"].module_origin_seq=new1_origin.seq;state["sequence"].module_extreme_seq=extreme.seq
        prior_aut_count=state.get("aut_count",0)
        # Once AUT transfers dominance, the next A-source test belongs to
        # the new 1's own functional base, never to the contradicted base again.
        state["aut_base"]=new1_origin
        state["aut_count"]=prior_aut_count+1
        pending_module=abs(extreme.price-new1_origin.price)<STRUCTURAL_MOVE
        if not pending_module:
            state["sequence"].module_origin=new1_origin.price;state["sequence"].module_extreme=extreme.price
            state["sequence"].module_origin_time=new1_origin.time_ms;state["sequence"].module_extreme_time=extreme.time_ms
            state["sequence"].module_origin_seq=new1_origin.seq;state["sequence"].module_extreme_seq=extreme.seq
        state["pending_module"]=pending_module
        state["requires_base"]=False
        state["a_emitted"]=False
        local["phase"]="AFTER_AUT";local["a_origin"]=None;local["a_extreme"]=None;local["b_origin"]=None
        self._local_leg(p,"1",new,new1_origin,extreme,"nuevo 1 dominante tras AUT","LOCAL_NUEVO_1",
                        function_direction=direction)

    def _apply_local_b_transitions(self,p:Pt,transitions:list[str],tracker:BigBTracker,
                                   reading:Reading,local:dict)->None:
        b0=local["b_origin"];a_end=local["a_extreme"];d=tracker.direction
        if "B_GRANDE" in transitions:
            reading.active_function="B_GRANDE"
            reading.b_grande_time=p.time_ms;reading.state="TT_PENDING"
            reading.b_origin=tracker.anchor;reading.b_extreme=tracker.extreme
            reading.b_origin_time=b0.time_ms;reading.b_extreme_time=local["b_extreme"].time_ms
            reading.b_origin_seq=b0.seq;reading.b_extreme_seq=local["b_extreme"].seq
            reading.tt_target=reading.a_end+d*reading.module_size
            self._local_leg(p,"B",reading,b0,local["b_extreme"],
                "B Grande confirmada en el primer tick que alcanza 100 % de A Grande","LOCAL_B_GRANDE")
        if "AUT_B" in transitions:
            reading.aut_source=AUT_CAUSE_B
            reading.active_function="AUT"
            self._new_local_reading_after_aut(p,reading,d,a_end,p,
                "B_GRANDE_SUPERA_127_MAS_025",AUT_CAUSE_B)

    def _process_local_sequence(self,p:Pt,index:int,bar:Bar,newbar:bool)->None:
        local=self._local;st=local["state"]
        if st is None:return
        d=st["direction"];r=st["reading"]
        if local["phase"]=="WAIT_TWO":
            if local["candidate_bar"] is None and newbar and bar.idx>st["bar1"]:
                st["bar2"]=bar.idx;st["two_open"]=bar.open
                prev=bar.prev_close
                gap=bar.open.price-prev if prev is not None else 0
                st["two_gap"]=gap
                if abs(gap)>=PLANO_TICK:
                    local["phase"]="NO_TWO";local["rejected"]=True
                    self._local_gate_event(p,r,"GAP_NO_HAY_2")
                else:local["phase"]="POSSIBLE_TWO"
            return
        if local["phase"]=="POSSIBLE_TWO" and bar.idx==st["bar2"]:
            op=st["two_open"]
            tail=(bar.high.price-op.price) if d<0 else (op.price-bar.low.price)
            dist=(op.price-p.price) if d<0 else (p.price-op.price)
            if tail>PLANO_TICK:
                local["phase"]="NO_TWO";local["rejected"]=True
                self._local_gate_event(p,r,"COLA_INICIAL_CONTRARIA_EXCEDE_025")
                return
            if local_two_gate(gap=st.get("two_gap",0),tail=tail,
                              direction_ok=dist>=0,size_ok=dist>=st["one_size"]):
                st["two_confirmed"]=True;st["two_extreme"]=p
                r.state="LOCAL_2_CONFIRMADO"
                r.module_extreme=p.price;r.module_extreme_time=p.time_ms;r.module_extreme_seq=p.seq
                st["module_extreme"]=p;st["sequence"].module_extreme=p.price
                self._local_leg(p,"2",r,op,p,"2 confirmado: plano, cola inicial permitida y recorrido direccional >= 1","LOCAL_2_CONFIRMADO")
                local["phase"]="TWO_CONFIRMED"
            return
        if local["phase"]=="TWO_CONFIRMED":
            if bar.idx==st["bar2"]:
                ext=st["two_extreme"]
                if (d<0 and p.price<ext.price) or (d>0 and p.price>ext.price):
                    st["two_extreme"]=p;st["module_extreme"]=p;st["sequence"].module_extreme=p.price
                    r.module_extreme=p.price;r.module_extreme_time=p.time_ms;r.module_extreme_seq=p.seq
                    self._emit("MODULO_EXT",p,r,"1","LOCAL_MODULE","2_EXTIENDE_MODULO",structural_pt=p,confirmation_pt=p)
            return
        if local["phase"]=="WAIT_THREE":
            ext=st["two_extreme"]
            new_extreme=(d<0 and p.price<ext.price) or (d>0 and p.price>ext.price)
            if new_extreme and abs(p.price-ext.price)>=STRUCTURAL_MOVE:
                st["module_extreme"]=p;st["sequence"].module_extreme=p.price
                r.module_extreme=p.price;r.module_extreme_time=p.time_ms;r.module_extreme_seq=p.seq
                r.state="LOCAL_3_CONFIRMADO"
                self._local_leg(p,"3",r,ext,p,"3 confirmado despues del 2: nuevo extremo","LOCAL_3_CONFIRMADO")
                local["phase"]="WAIT_A_BAR";local["three_bar"]=bar.idx
            return
        if local["phase"]=="WAIT_A_BAR":
            if bar.idx==local.get("three_bar"):
                ext=st["module_extreme"]
                if (d<0 and p.price<ext.price) or (d>0 and p.price>ext.price):
                    st["module_extreme"]=p;st["sequence"].module_extreme=p.price
                    r.module_extreme=p.price;r.module_extreme_time=p.time_ms;r.module_extreme_seq=p.seq
                    self._emit("MODULO_EXT",p,r,"3","LOCAL_MODULE","3_EXTIENDE_MODULO",
                               structural_pt=p,confirmation_pt=p)
                return
            if newbar and bar.idx>local.get("three_bar",bar.idx):
                local["phase"]="AFTER_3"
            else:
                return
        if local["phase"]=="AFTER_3":
            ext=st["module_extreme"]
            contrary=(d<0 and p.price>ext.price) or (d>0 and p.price<ext.price)
            if contrary:
                local["phase"]="A_ACTIVE";local["a_origin"]=ext;local["a_extreme"]=p
                st["a_emitted"]=False
                r.state="LOCAL_A"
                self._local_leg(p,"A",r,ext,p,"A Grande contraria al modulo local","LOCAL_A")
            return
        if local["phase"]=="AFTER_AUT":
            ext=st["module_extreme"]
            contrary=(d<0 and p.price>ext.price) or (d>0 and p.price<ext.price)
            if not contrary:
                if (d<0 and p.price<ext.price) or (d>0 and p.price>ext.price):
                    st["module_extreme"]=p;st["sequence"].module_extreme=p.price
                    if not st.get("pending_module",False) or abs(p.price-st["module_origin"].price)>=STRUCTURAL_MOVE:
                        st["pending_module"]=False
                        st["sequence"].module_origin=st["module_origin"].price
                        st["sequence"].module_extreme=p.price
                        st["sequence"].module_origin_time=st["module_origin"].time_ms
                        st["sequence"].module_extreme_time=p.time_ms
                        st["sequence"].module_origin_seq=st["module_origin"].seq
                        st["sequence"].module_extreme_seq=p.seq
                        r.module_origin=st["module_origin"].price;r.module_extreme=p.price
                        r.module_origin_time=st["module_origin"].time_ms;r.module_extreme_time=p.time_ms
                        r.module_origin_seq=st["module_origin"].seq;r.module_extreme_seq=p.seq
                return
            local["a_origin"]=ext;local["a_extreme"]=p;local["phase"]="A_CANDIDATE"
            return
        if local["phase"]=="A_CANDIDATE":
            a0=local["a_origin"];ae=local["a_extreme"]
            contrary_ext=(d<0 and p.price>ae.price) or (d>0 and p.price<ae.price)
            if contrary_ext:
                local["a_extreme"]=p;ae=p
            if abs(ae.price-a0.price)>=MOVE:
                local["phase"]="A_ACTIVE";st["a_emitted"]=True
                r.state="LOCAL_A";r.a_origin=a0.price;r.a_end=ae.price
                r.a_origin_time=a0.time_ms;r.a_end_time=ae.time_ms
                r.a_origin_seq=a0.seq;r.a_end_seq=ae.seq
                r.a_knowledge_time=p.time_ms
                self._local_leg(p,"A",r,a0,ae,"A Grande confirmada por movimiento estructural","LOCAL_A")
            elif (d<0 and p.price<a0.price) or (d>0 and p.price>a0.price):
                # The contrary excursion did not confirm A; absorb it into the
                # dominant 1 and keep the more extreme point causally.
                if (d<0 and p.price<st["module_extreme"].price) or (d>0 and p.price>st["module_extreme"].price):
                    st["module_extreme"]=p;st["sequence"].module_extreme=p.price
                    r.module_extreme=p.price;r.module_extreme_time=p.time_ms;r.module_extreme_seq=p.seq
                local["phase"]="AFTER_AUT";local["a_origin"]=None;local["a_extreme"]=None
            return
        if local["phase"]=="A_ACTIVE":
            a0=local["a_origin"];ae=local["a_extreme"]
            if (d<0 and p.price>ae.price) or (d>0 and p.price<ae.price):
                local["a_extreme"]=p;ae=p
            if not st.get("a_emitted",False) and abs(ae.price-a0.price)>=MOVE:
                r.a_origin=a0.price;r.a_end=ae.price;r.a_origin_time=a0.time_ms;r.a_end_time=ae.time_ms
                r.a_origin_seq=a0.seq;r.a_end_seq=ae.seq
                self._local_leg(p,"A",r,a0,ae,"A Grande contraria al modulo confirmada por movimiento estructural","LOCAL_A")
                st["a_emitted"]=True
            # A crossing the module base replaces the local reading and transfers dominance.
            a_is_structural=abs(ae.price-a0.price)>=MOVE
            # The second AUT genealogy is carried by the A Grande's own
            # directional extreme. A pullback after that extreme cannot create
            # an A-source AUT merely by crossing the module base.
            aut_base=st.get("aut_base",st["module_origin"])
            a_direction=-d
            cross_base=a_is_structural and strict_crosses(a_direction,ae.price,aut_base.price)
            if cross_base:
                next_one_origin=st["module_extreme"]
                self._new_local_reading_after_aut(p,r,-d,aut_base,ae,
                    "A_LOCAL_SUPERA_BASE_MODULO",AUT_CAUSE_A,new1_origin=next_one_origin)
                return
            # A return through its own origin confirms B and a same-direction AUT.
            counter_size=abs(p.price-ae.price)
            resumed=counter_size>=MOVE and (not st.get("requires_base",False) or cross_base) and ((d<0 and p.price<ae.price) or (d>0 and p.price>ae.price))
            if resumed:
                local["phase"]="B_ACTIVE";local["b_origin"]=ae
                local["b_extreme"]=ae
                st["big_b_tracker"]=BigBTracker(direction=d,anchor=ae.price,
                    a_size=abs(ae.price-a0.price),extreme=ae.price)
                self._local_leg(p,"B",r,ae,p,"B candidata desde el final de A Grande","LOCAL_B_CANDIDATA")
                transitions=st["big_b_tracker"].feed(p.price)
                if st["big_b_tracker"].extreme!=ae.price:local["b_extreme"]=p
                self._apply_local_b_transitions(p,transitions,st["big_b_tracker"],r,local)
            return
        if local["phase"]=="B_ACTIVE":
            b0=local["b_origin"]
            tracker=st.get("big_b_tracker")
            if tracker is None:
                a0=local["a_origin"]
                tracker=BigBTracker(direction=d,anchor=b0.price,
                    a_size=abs(local["a_extreme"].price-a0.price),extreme=b0.price)
                st["big_b_tracker"]=tracker
            previous_extreme=tracker.extreme
            if tracker.begin_c(p.price):
                tracker.feed(p.price)
                self._local_leg(p,"C",r,Pt(previous_extreme,p.seq-1,p.time_ms,p.bar),p,
                    "C Grande inicia después de B Grande confirmada","LOCAL_C_GRANDE")
                local["phase"]="C_ACTIVE"
                return
            transitions=tracker.feed(p.price)
            if tracker.extreme!=previous_extreme:
                local["b_extreme"]=p
            a0=local["a_origin"];a_end=local["a_extreme"]
            r.a_origin=a0.price;r.a_end=a_end.price;r.a_origin_time=a0.time_ms;r.a_end_time=a_end.time_ms
            r.a_origin_seq=a0.seq;r.a_end_seq=a_end.seq
            r.b_origin=tracker.anchor;r.b_extreme=tracker.extreme
            r.b_origin_time=b0.time_ms;r.b_extreme_time=local["b_extreme"].time_ms
            r.b_origin_seq=b0.seq;r.b_extreme_seq=local["b_extreme"].seq
            r.b_knowledge_time=p.time_ms
            self._apply_local_b_transitions(p,transitions,tracker,r,local)
            return
        if local["phase"]=="C_ACTIVE":
            tracker=st.get("big_b_tracker")
            if tracker is not None:
                old_c=tracker.c_extreme
                tracker.feed(p.price)
                if tracker.c_extreme!=old_c:
                    self._local_leg(p,"C",r,Pt(old_c,p.seq-1,p.time_ms,p.bar),p,
                        "C Grande extiende su extremo","LOCAL_C_GRANDE")
            return

    def _track_primary_b_aut(self,p:Pt)->None:
        """Advance the primary reading's B/AUT state on this physical tick only."""
        for r in list(self.active):
            if r.state=="DONE":continue
            if r.state=="A" and not r.b_tick_active and p.time_ms>r.a_knowledge_time:
                starts_b=(r.direction>0 and p.price>r.a_end) or (r.direction<0 and p.price<r.a_end)
                if not starts_b:continue
                r.b_tick_active=True;r.b_candidate_emitted=True;r.active_function="B_CANDIDATA"
                r.b_origin=r.a_end;r.b_extreme=p.price
                r.b_origin_time=r.a_end_time;r.b_extreme_time=p.time_ms
                r.b_origin_seq=r.a_end_seq;r.b_extreme_seq=p.seq
                self._emit("B_CANDIDATA",p,r,"B","B_CAND","ANTES_100_A",structural_pt=p,confirmation_pt=p)
            if not r.b_tick_active:
                continue
            extends=(r.direction>0 and p.price>r.b_extreme) or (r.direction<0 and p.price<r.b_extreme)
            if extends:
                r.b_extreme=p.price;r.b_extreme_time=p.time_ms;r.b_extreme_seq=p.seq
                r.b_knowledge_time=p.time_ms
            if not r.b_grande_time and r.b_size>=r.a_size:
                r.b_grande_time=p.time_ms
                r.active_function="B_GRANDE"
                r.tt_target=r.a_end+r.direction*r.module_size
                r.labels.append((len(self.points)-1,"B_GRANDE"))
                self._emit("B_GRANDE",p,r,"B","TT_PENDING","B100_TICK_EXACTO",structural_pt=p,confirmation_pt=p)
                self._pattern("B_GRANDE","CONFIRMADO",r,r.b_origin,r.b_extreme,"B100_TICK_EXACTO",p.time_ms)
            if r.b_grande_time and not r.aut_reclassified and r.b_size>self._aut_limit(r):
                r.aut_time=p.time_ms;r.aut_price=p.price;r.aut_reclassified=True
                r.aut_source=AUT_CAUSE_B
                r.active_function="AUT"
                r.labels.append((len(self.points)-1,"AUT"))
                self._emit("AUT",p,r,"AUT","AUT","SUPERA_127_MAS_025; AUT_CAUSE="+AUT_CAUSE_B,
                           structural_pt=p,confirmation_pt=p)
                self._pattern("AUT","CONFIRMADO",r,r.b_origin,r.b_extreme,AUT_CAUSE_B,p.time_ms)
            if r.b_grande_time and r.c_tick_started:
                extends_c=(r.direction>0 and p.price<r.c_extreme) or (r.direction<0 and p.price>r.c_extreme)
                if extends_c:
                    r.c_extreme=p.price;r.c_extreme_time=p.time_ms;r.c_knowledge_time=p.time_ms
            elif r.b_grande_time:
                contrary=(r.direction>0 and p.price<r.b_extreme) or (r.direction<0 and p.price>r.b_extreme)
                if contrary and p.seq>r.b_extreme_seq:
                    r.c_tick_started=True;r.c_origin=r.b_extreme;r.c_extreme=p.price
                    r.active_function="C"
                    r.c_origin_time=r.b_extreme_time;r.c_extreme_time=p.time_ms;r.c_knowledge_time=p.time_ms
                    r.labels.append((len(self.points)-1,"C"))
                    self._emit("C",p,r,"C",r.state,"CONTRARIO_POST_B_GRANDE_SIN_C_CANDIDATA",
                               structural_pt=p,confirmation_pt=p)

    def feed_chunk(self,chunk:list[Pt])->None:
        if self._finalized:raise RuntimeError("cannot feed a finalized engine")
        for p in chunk:
            if self.points and (p.seq<=self.points[-1].seq or p.time_ms<self.points[-1].time_ms):
                raise ValueError("ticks must be strictly ordered by sequence and time")
            self._tick_before={r.reading_id:r.state for r in self.active if r.state!="DONE"}
            self.points.append(p)
            if self.start_time==0:self.start_time=p.time_ms
            self.end_time=p.time_ms
            bar,newbar=self._bar_for_tick(p)
            self._current_pt=p
            if newbar:self._schedule_gap(p)
            self.scheduler.run_due(p)
            index=len(self.points)-1
            if self.builder is None:self.builder=MovementBuilder(p)
            elif index:
                movement=self.builder.feed(p,index)
                if movement is not None:
                    self.movements.append(movement);self._process_movement(movement)
            self._track_primary_b_aut(p)
            if self._local["last_bar"] is not None and newbar:
                closed=self.bars[self._local["last_bar"]]
                self._close_candidate_bar(closed,p)
                if self._local["phase"]=="TWO_CONFIRMED":
                    st=self._local["state"]
                    if st is not None and closed.idx==st["bar2"]:
                        st["two_extreme"]=closed.low if st["direction"]<0 else closed.high
                        st["module_extreme"]=st["two_extreme"]
                        st["sequence"].module_extreme=st["two_extreme"].price
                        st["reading"].module_extreme=st["two_extreme"].price
                        st["reading"].module_extreme_time=st["two_extreme"].time_ms
                        st["reading"].module_extreme_seq=st["two_extreme"].seq
                        self._local["phase"]="WAIT_THREE"
            if newbar:
                if self._local["armed"] and self._local["state"] is None and p.bar!=self._local["aut_bar"]:
                    self._local["candidate_bar"]=p.bar;self._local["armed"]=False
            self._observe_core_aut(p)
            self._process_local_sequence(p,index,bar,newbar)
            self._record_knowledge(p)
            self._prev_price=p.price;self._last_bar=p.bar;self._local["last_bar"]=p.bar
            self._local["last_price"]=p.price

    def run(self)->"CanonicalEngine":
        pending=self._pending_points;self._pending_points=[]
        for p in pending:self.feed_chunk([p])
        return self.finalize_stream()

    def finalize_stream(self)->"CanonicalEngine":
        if self._finalized:return self
        last=self.points[-1] if self.points else Pt(0,0,0,0)
        self._emit("FIN_FEED",last,None,"","END","END_OF_FEED","end of feed")
        self.coverage=evaluate_coverage(self);self.audit=build_audit(self);self.narrative=build_narrative(self)
        self.pending=["post_tt_fallido_no_definido","ft_expiracion_no_definida","lectura_local_reglas_abiertas_preservadas"]
        if not self.coverage.get("causal_functional_ok",False):self.pending.append("functional_coverage_causal_parcial")
        if not self.coverage.get("causal_geometric_ok",False):self.pending.append("geometric_coverage_causal_parcial")
        for r in self.readings:
            if r.state!="DONE":self.pending.append(f"lectura_abierta_al_final:{r.reading_id}");break
        self.afs2={"AFS2_READY":False,"status":"NO DESARROLLADO EN v0.7.5.2"}
        self._finalized=True
        return self

    def serialize_state(self)->bytes:
        return pickle.dumps(self,protocol=5)

    @classmethod
    def restore_state(cls,payload:bytes)->"CanonicalEngine":
        obj=pickle.loads(payload)
        if not isinstance(obj,cls) or obj._finalized:raise ValueError("checkpoint version/state mismatch")
        return obj


Engine=CanonicalEngine

def run_engine(points: list[Pt], bars: dict[int, Bar]) -> Engine:
    return Engine(points, bars).run()



def write_core_raw_output(engine:CanonicalEngine,path:Path|str)->Path:
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    def clean(v):
        if hasattr(v,"__dict__"):return {k:clean(x) for k,x in v.__dict__.items()}
        if isinstance(v,dict):return {k:clean(x) for k,x in v.items()}
        if isinstance(v,(list,tuple)):return [clean(x) for x in v]
        return v
    data={"artifact":"CORE_RAW_OUTPUT","version":VERSION,"source":"sequential core only",
      "feed_points":len(engine.points),"events":clean(engine.events),
      "readings":[clean(r) for r in engine.readings],"patterns":clean(engine.patterns),
      "local_sequences":clean(engine.local_sequences),"local_events":clean(engine.local_events),
      "active_readings":[r.reading_id for r in engine.active if r.state!="DONE"],
      "pending":engine.pending,"coverage":engine.coverage,"afs2":{"AFS2_READY":False}}
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    return path

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
    base = 0
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
    parser.add_argument("--out", type=Path, default=Path("out_v0752"))
    parser.add_argument("--stem", default="v075")
    parser.add_argument("--start")
    parser.add_argument("--end")
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
    raw_path = write_core_raw_output(engine, args.out / "CORE_RAW_OUTPUT.json")
    paths = [raw_path]
    print(f"v{VERSION} readings={len(engine.readings)} events={len(engine.events)} movements={len(engine.movements)}")
    print(f"coverage geometric={engine.coverage['geometric_ok']} functional={engine.coverage['functional_ok']}")
    print(f"outputs={args.out}")
    for path in paths:
        print(f"  {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

