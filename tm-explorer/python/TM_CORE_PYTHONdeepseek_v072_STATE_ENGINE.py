"""TM core v0.7.2 - causal tick state engine with post-TT continuity.

Scope: replay ticks in sequence order, never use future data, derive A/B from
the observed path, preserve every historical event, and distinguish pending
from confirmed/extending TT states. A restored confirmed TT never regresses to
TT_PENDING and remains concurrently monitored for its real extreme, its FT and
a local reading.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pandas as pd

VERSION = "0.7.2"
MOVE = 200
AUT_NUM = 127
AUT_DEN = 100
AUT_EXTRA = 25
MIN_MODULE_STUDY = 600
TT_PENDING = "TT_PENDING"
TT_CONFIRMED = "TT_CONFIRMED"
TT_EXTENDING = "TT_EXTENDING"
POST_TT_FT_WINDOW = "POST_TT_FT_WINDOW"
TT_COMPLETED = "TT_COMPLETED"
FT_CANDIDATE = "FT_CANDIDATE"
FT_CONFIRMED = "FT_CONFIRMED"
FT_REJECTED = "FT_REJECTED_AS_NOISE"
FT_WINDOW_EXPIRED = "FT_WINDOW_EXPIRED"
FT_CANDIDATE_ABSORBED = "FT_CANDIDATE_ABSORBED_BY_TT_EXTENSION"
ACTIVE_STATES = {
    "MODULE",
    "A",
    "B",
    TT_PENDING,
    FT_CANDIDATE,
    TT_CONFIRMED,
    TT_EXTENDING,
    POST_TT_FT_WINDOW,
    "TT_MINOR_CONFIRMED",
}


def aut_exceeded(b: int, a: int) -> bool:
    return AUT_DEN * b > AUT_NUM * a + AUT_EXTRA * AUT_DEN


def price_i(value: float) -> int:
    return int(round(float(value) * 100))


def price_s(value: int) -> str:
    sign = "-" if value < 0 else ""
    value = abs(value)
    return f"{sign}{value // 100}.{value % 100:02d}"


def ms_to_text(ms: int) -> str:
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def ms_to_hms(ms: int) -> str:
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    return dt.strftime("%H:%M:%S.%f")[:-3]


def parse_hms(value: str, base_ms: Optional[int] = None) -> int:
    text = value.strip()
    if text.count(":") == 1:
        text += ":00"
    if "-" in text or "/" in text:
        fmt = "%Y-%m-%d %H:%M:%S.%f" if "." in text else "%Y-%m-%d %H:%M:%S"
        dt = datetime.strptime(text, fmt)
        return int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)
    if base_ms is None:
        raise ValueError("base_ms is required for HH:MM:SS times")
    base = datetime.fromtimestamp(base_ms / 1000, tz=timezone.utc)
    fmt = "%H:%M:%S.%f" if "." in text else "%H:%M:%S"
    dt = datetime.strptime(text, fmt)
    return int(
        base.replace(hour=dt.hour, minute=dt.minute, second=dt.second, microsecond=dt.microsecond).timestamp() * 1000
    )


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
    prev_close: Optional[int]


@dataclass
class Seed:
    kind: str
    direction: int
    price: int
    module_origin: Optional[int] = None
    module_extreme: Optional[int] = None
    a_origin: Optional[int] = None
    a_end: Optional[int] = None
    tt_target: Optional[int] = None
    tt_state: str = ""
    tt_100_time: Optional[int] = None
    tt_100_price: Optional[int] = None
    tt_100_seq: Optional[int] = None
    tt_real_extreme_time: Optional[int] = None
    tt_real_extreme_price: Optional[int] = None
    tt_real_extreme_seq: Optional[int] = None
    parent_tt_id: str = ""
    source_reading_id: str = ""
    source_cycle_id: str = ""
    module_size: Optional[int] = None
    final_a: Optional[int] = None
    aut_time: Optional[int] = None
    aut_price: Optional[int] = None
    ft_window_start_bar: Optional[int] = None
    ft_window_end_bar: Optional[int] = None
    ft_state: str = ""
    last_processed_sequence_id: Optional[int] = None


@dataclass
class Reading:
    reading_id: str
    cycle_id: str
    direction: int
    state: str
    scale: int
    origin_event: str
    created_time: int
    parent_reading_id: Optional[str] = None
    parent_cycle_id: Optional[str] = None
    origin: Optional[Pt] = None
    ext: Optional[Pt] = None
    mod_origin: Optional[Pt] = None
    mod_ext: Optional[Pt] = None
    a_origin: Optional[Pt] = None
    a_end: Optional[Pt] = None
    b_origin: Optional[Pt] = None
    b_ext: Optional[Pt] = None
    aut_pt: Optional[Pt] = None
    tt_target: Optional[int] = None
    tt_pt: Optional[Pt] = None
    tt_ext: Optional[Pt] = None
    new1_origin: Optional[Pt] = None
    new1_ext: Optional[Pt] = None
    ft_ext: Optional[Pt] = None
    ft_candidate: bool = False
    ft_window_start: Optional[int] = None
    ft_window_end: Optional[int] = None
    closed_time: Optional[int] = None
    fail_pt: Optional[Pt] = None
    fail_reason: str = ""
    note: str = ""
    gap_a: bool = False
    generation: int = 1
    original_scale: int = 0
    final_priority: str = ""
    original_confirmation_time: str = ""
    original_confirmation_price: str = ""
    absorbed_time: str = ""
    absorbed_by_reading_id: str = ""
    absorbed_by_cycle_id: str = ""
    tracker_only: bool = False
    derived_from_tt: bool = False
    derived_from_ft: bool = False
    tt_confirmed: bool = False
    tt_100_already_reached: bool = False
    tt_real_extreme_seq: Optional[int] = None
    parent_tt_id: str = ""
    coexisting_function: str = ""
    ft_origin: Optional[Pt] = None
    ft_pattern_id: str = ""
    ft_status: str = ""
    track_ft: bool = True
    coverage_role: str = ""

    @property
    def is_active(self) -> bool:
        return self.state in ACTIVE_STATES and not self.tracker_only

    @property
    def x_size(self) -> int:
        if self.mod_origin is None or self.mod_ext is None:
            return 0
        return abs(self.mod_ext.price - self.mod_origin.price)

    @property
    def a_size(self) -> int:
        if self.a_origin is None or self.a_end is None:
            return 0
        return abs(self.a_end.price - self.a_origin.price)

    @property
    def b_size(self) -> int:
        if self.a_end is None or self.b_ext is None:
            return 0
        return abs(self.b_ext.price - self.a_end.price)


class Engine:
    def __init__(self, seed: Optional[Seed] = None, multi_scale: bool = False) -> None:
        self.seed = seed
        self.multi_scale = multi_scale
        self.readings: list[Reading] = []
        self.events: list[dict] = []
        self.patterns: list[dict] = []
        self.pending: list[str] = []
        self.current: Optional[Reading] = None
        self.dominant: Optional[Reading] = None
        self.minor_tt: Optional[Reading] = None
        self.minor_ft: Optional[Reading] = None
        self.tracker_child: Optional[Reading] = None
        self.post_tt_anchor: Optional[Reading] = None
        self.ft_child: Optional[Reading] = None
        self.coverage_unresolved: list[dict] = []
        self.TM_COVERAGE_OK = True
        self.last_bar: Optional[int] = None
        self.prev_close: Optional[int] = None
        self.last_pt: Optional[Pt] = None
        self._rid = 0
        self._cid = 0
        self._eid = 0
        self._pid = 0
        self.mini_used = False

    def _next_ids(self) -> tuple[str, str]:
        self._rid += 1
        self._cid += 1
        return f"R{self._rid:04d}", f"C{self._cid:04d}"

    def emit(self, kind: str, p: Pt, reading: Optional[Reading], **detail) -> None:
        self._eid += 1
        self.events.append(
            {
                "event_id": f"E{self._eid:06d}",
                "time": p.hms,
                "time_ms": p.time_ms,
                "sequence_id": p.seq,
                "bar": p.bar,
                "price": price_s(p.price),
                "kind": kind,
                "reading_id": reading.reading_id if reading else "",
                "cycle_id": reading.cycle_id if reading else "",
                "detail": json.dumps(detail, ensure_ascii=False, sort_keys=True),
            }
        )

    def pending_rule(self, kind: str, p: Pt, reading: Optional[Reading], note: str, **detail) -> None:
        if note in self.pending:
            return
        self.pending.append(note)
        self.emit(kind, p, reading, note=note, **detail)

    def pattern(self, kind: str, status: str, reading: Reading, p: Pt, **detail) -> dict:
        self._pid += 1
        origin = reading.a_end or reading.origin
        size = abs(p.price - origin.price) if origin else 0
        pattern = {
            "pattern_id": f"P{self._pid:04d}",
            "type": kind,
            "status": status,
            "final_status": status,
            "direction": "UP" if reading.direction > 0 else "DOWN",
            "origin_time": origin.hms if origin else "",
            "origin_price": price_s(origin.price) if origin else "",
            "end_time": p.hms,
            "end_price": price_s(p.price),
            "size": price_s(size),
            "reading_id": reading.reading_id,
            "cycle_id": reading.cycle_id,
            "detail": json.dumps(detail, ensure_ascii=False, sort_keys=True),
        }
        self.patterns.append(pattern)
        return pattern

    def _new_reading(
        self,
        p: Pt,
        direction: int,
        state: str,
        origin_event: str,
        origin: Pt,
        ext: Pt,
        parent: Optional[Reading] = None,
        note: str = "",
        scale: Optional[int] = None,
        generation: int = 1,
    ) -> Reading:
        rid, cid = self._next_ids()
        reading = Reading(
            reading_id=rid,
            cycle_id=cid,
            direction=direction,
            state=state,
            scale=(1 if parent is None else parent.scale + 1) if scale is None else scale,
            origin_event=origin_event,
            created_time=p.time_ms,
            parent_reading_id=parent.reading_id if parent else None,
            parent_cycle_id=parent.cycle_id if parent else None,
            origin=origin,
            ext=ext,
            mod_origin=origin,
            mod_ext=ext,
            note=note,
            generation=generation,
        )
        self.readings.append(reading)
        self.current = reading
        self.mini_used = False
        return reading

    def seed_reading(self, p: Pt) -> None:
        if self.seed is None:
            self._new_reading(p, 1, "MODULE", "AUTO_SEED", p, p, note="AUTO_SEED_FIRST_TICK")
            self.dominant = self.current
            self.emit("SEED_MODULE", p, self.current, origin=price_s(p.price), note="AUTO_SEED")
            return
        s = self.seed
        if s.kind == "MODULE":
            self._new_reading(p, s.direction, "MODULE", "SEED_MODULE", p, p, note="SEED_EXPLICIT")
            assert self.current is not None
            self.current.origin = Pt(s.price, p.seq, p.time_ms, p.bar)
            self.current.ext = self.current.origin
            self.current.mod_origin = self.current.origin
            self.current.mod_ext = self.current.origin
            self.dominant = self.current
            self.emit("SEED_MODULE", p, self.current, origin=price_s(s.price), direction=s.direction)
            return
        if s.kind == "GAP_A":
            mo = s.module_origin if s.module_origin is not None else s.price
            me = s.module_extreme if s.module_extreme is not None else s.price
            mod_origin = Pt(mo, p.seq, p.time_ms, p.bar)
            mod_ext = Pt(me, p.seq, p.time_ms, p.bar)
            a_origin = Pt(s.a_origin if s.a_origin is not None else s.price, p.seq, p.time_ms, p.bar)
            a_end = Pt(s.a_end if s.a_end is not None else s.price, p.seq, p.time_ms, p.bar)
            self._new_reading(p, s.direction, "A", "SEED_GAP_A", mod_origin, mod_ext, note="SEED_EXPLICIT_GAP")
            assert self.current is not None
            self.current.a_origin = a_origin
            self.current.a_end = a_end
            self.current.gap_a = True
            self.dominant = self.current
            self.emit(
                "SEED_GAP_A",
                p,
                self.current,
                module_origin=price_s(mo),
                module_extreme=price_s(me),
                a_origin=price_s(a_origin.price),
                direction=s.direction,
            )
            return
        if s.kind.upper() in ("TT", "TT_PENDING", "TT_CONFIRMED", "TT_EXTENDING", "POST_TT"):
            state = s.tt_state or {
                "TT": TT_PENDING,
                "TT_PENDING": TT_PENDING,
                "TT_CONFIRMED": TT_CONFIRMED,
                "TT_EXTENDING": TT_EXTENDING,
                "POST_TT": POST_TT_FT_WINDOW,
            }[s.kind.upper()]
            mo = s.module_origin if s.module_origin is not None else s.price
            me = s.module_extreme if s.module_extreme is not None else s.price
            ao = s.a_origin if s.a_origin is not None else s.price
            ae = s.a_end if s.a_end is not None else s.price
            mod_origin = Pt(mo, p.seq, p.time_ms, p.bar)
            mod_ext = Pt(me, p.seq, p.time_ms, p.bar)
            a_origin = Pt(ao, p.seq, p.time_ms, p.bar)
            a_end = Pt(ae, p.seq, p.time_ms, p.bar)
            if state == TT_PENDING:
                self._new_reading(p, s.direction, TT_PENDING, "SEED_TT_PENDING", mod_origin, mod_ext, note="SEED_EXPLICIT_TT_PENDING")
                assert self.current is not None
                self.current.a_origin = a_origin
                self.current.a_end = a_end
                self.current.tt_target = s.tt_target
                self.current.tt_ext = a_end
                self.current.parent_tt_id = s.parent_tt_id
                self.dominant = self.current
                self.emit(
                    "SEED_TT",
                    p,
                    self.current,
                    target=price_s(s.tt_target) if s.tt_target is not None else "",
                    a_end=price_s(a_end.price),
                    direction=s.direction,
                    state=state,
                )
                return
            self._restore_confirmed_tt(p, s, state, mod_origin, mod_ext, a_origin, a_end)
            return
        raise ValueError(f"unknown seed kind {s.kind}")

    def _restore_confirmed_tt(
        self,
        p: Pt,
        s: Seed,
        state: str,
        mod_origin: Pt,
        mod_ext: Pt,
        a_origin: Pt,
        a_end: Pt,
    ) -> None:
        if s.tt_target is None:
            raise ValueError("INVALID_SEED_MISSING_TT_TARGET")
        if s.tt_100_price is None or s.tt_100_time is None:
            raise ValueError("INVALID_SEED_MISSING_TT100")
        tt100 = Pt(s.tt_100_price, s.tt_100_seq if s.tt_100_seq is not None else p.seq, s.tt_100_time, s.tt_100_time // 60000)
        extreme_price = s.tt_real_extreme_price
        extreme_time = s.tt_real_extreme_time
        extreme_seq = s.tt_real_extreme_seq
        provisional = False
        if extreme_price is None:
            extreme_price = s.price
            extreme_time = p.time_ms
            extreme_seq = p.seq
            provisional = True
        if (tt100.price - s.tt_target) * s.direction < 0:
            raise ValueError("INVALID_SEED_TT100_BEFORE_TARGET")
        if (extreme_price - tt100.price) * s.direction < 0:
            raise ValueError("INVALID_SEED_REAL_EXTREME")
        ext = Pt(extreme_price, extreme_seq if extreme_seq is not None else p.seq, extreme_time if extreme_time is not None else p.time_ms, (extreme_time if extreme_time is not None else p.time_ms) // 60000)
        self._new_reading(
            p,
            s.direction,
            state,
            "SEED_TT_CONFIRMED" if state != POST_TT_FT_WINDOW else "SEED_POST_TT",
            mod_origin,
            ext,
            note="SEED_EXPLICIT_TT_CONFIRMED",
            scale=0,
        )
        r = self.current
        assert r is not None
        r.a_origin = a_origin
        r.a_end = a_end
        r.aut_pt = Pt(s.aut_price, p.seq, s.aut_time, (s.aut_time or p.time_ms) // 60000) if s.aut_price is not None else None
        r.tt_target = s.tt_target
        r.tt_pt = tt100
        r.tt_ext = ext
        r.new1_origin = ext
        r.new1_ext = ext
        r.ft_ext = ext
        r.ft_origin = ext
        r.ft_window_start = s.ft_window_start_bar if s.ft_window_start_bar is not None else tt100.bar + 1
        r.ft_window_end = s.ft_window_end_bar if s.ft_window_end_bar is not None else r.ft_window_start + 1
        r.original_confirmation_time = ms_to_text(tt100.time_ms)
        r.original_confirmation_price = price_s(tt100.price)
        r.tt_confirmed = True
        r.tt_100_already_reached = True
        r.tt_real_extreme_seq = ext.seq
        r.parent_tt_id = s.parent_tt_id or s.source_reading_id
        r.derived_from_tt = True
        r.track_ft = True
        r.ft_status = s.ft_state or "WINDOW_OPEN"
        r.cycle_id = s.source_cycle_id or r.cycle_id
        self.post_tt_anchor = r
        self.dominant = None
        self.current = r
        self.emit(
            "TT_100_RESTORED",
            p,
            r,
            target=price_s(s.tt_target),
            tt_100_time=ms_to_text(tt100.time_ms),
            tt_100_price=price_s(tt100.price),
            tt_100_sequence_id=tt100.seq,
            state=state,
        )
        self.emit(
            "TT_REAL_EXTREME_RESTORED",
            p,
            r,
            real_extreme_time=ms_to_text(ext.time_ms),
            real_extreme_price=price_s(ext.price),
            real_extreme_sequence_id=ext.seq,
            provisional=provisional,
        )
        if provisional:
            self.emit("TT_REAL_EXTREME_PROVISIONAL", p, r, real_extreme_price=price_s(ext.price))

    def _on_new_bar(self, p: Pt, bar: Bar) -> None:
        self.prev_close = bar.prev_close
        self.last_bar = p.bar
        if bar.prev_close is None:
            return
        gap = p.price - bar.prev_close
        r = self.dominant or self.current
        self.emit("GAP" if gap != 0 else "SIN_GAP", p, r, gap=price_s(gap), prev_close=price_s(bar.prev_close))
        c = self.current
        if gap != 0 and c is not None and c is not r and c.state in ("A", "B") and c.aut_pt is None:
            c.a_origin = p
            c.a_end = p
            c.b_origin = None
            c.b_ext = None
            c.state = "A"
            c.gap_a = True
            c.note = (c.note + "|GAP_A_RESET").strip("|")
            self.emit("GAP_A_RESET", p, c, gap=price_s(gap), module_extreme=price_s(c.mod_ext.price))
            return
        if self.current is not None and self.current.state in (
            "TT_OK",
            "TT_PENDING",
            "TT_MINOR_CONFIRMED",
        ):
            return
        if r is None or r.state != "MODULE":
            return
        if gap == 0:
            return
        if (p.price - r.mod_ext.price) * r.direction > 0:
            r.mod_ext = p
            r.ext = p
            if r is self.dominant:
                self._absorb_minor_by_dominant(p, r)
            self.emit("MODULO_EXT_GAP", p, r, x=price_s(r.x_size))
            return
        if r.tracker_only and r is self.dominant:
            if self.tracker_child is not None:
                return
            child = self._new_reading(
                p,
                r.direction,
                "A",
                "GAP_A_DOMINANT",
                p,
                p,
                parent=r,
                note="GAP_A",
                scale=1,
                generation=r.generation,
            )
            child.mod_origin = r.mod_origin
            child.mod_ext = r.mod_ext
            child.a_origin = p
            child.a_end = p
            child.gap_a = True
            self.minor_ft = None
            self.tracker_child = child
            self.current = child
            self.emit("A_GAP_INICIO", p, child, module_extreme=price_s(child.mod_ext.price), gap=price_s(gap))
            return
        r.a_origin = p
        r.a_end = p
        r.gap_a = True
        r.state = "A"
        r.note = "GAP_A"
        self.emit("A_GAP_INICIO", p, r, module_extreme=price_s(r.mod_ext.price), gap=price_s(gap))

    def _start_a(self, p: Pt, r: Reading) -> None:
        r.a_origin = r.mod_ext
        r.a_end = p
        r.state = "A"
        self.emit("A_GRANDE_CONFIRMADA", p, r, a_origin=price_s(r.a_origin.price), a=price_s(r.a_size))

    def _start_b(self, p: Pt, r: Reading) -> None:
        r.b_origin = r.a_end
        r.b_ext = p
        r.state = "B"
        self.emit(
            "B_CANDIDATA",
            p,
            r,
            a_origin=price_s(r.a_origin.price) if r.a_origin else "",
            a_end=price_s(r.a_end.price),
            a=price_s(r.a_size),
            b=price_s(r.b_size),
        )

    def _absorb_a(self, p: Pt, r: Reading) -> None:
        if r.a_origin is None or r.a_end is None:
            return
        if self.mini_used:
            self.emit(
                "MOVIMIENTO_2_SIN_TERCERA_ESCALA",
                p,
                r,
                a=price_s(r.a_size),
                a_origin=price_s(r.a_origin.price),
                a_end=price_s(r.a_end.price),
                note="Máximo dos escalas activas; el movimiento se registra sin abrir otra.",
            )
            return
        rid, cid = self._next_ids()
        mini = Reading(
            reading_id=rid,
            cycle_id=cid,
            direction=-r.direction,
            state="ABSORBIDO_POR_FUNCION_DOMINANTE",
            scale=0,
            origin_event="MINI_ABSORBIDO",
            created_time=r.a_origin.time_ms,
            parent_reading_id=r.reading_id,
            parent_cycle_id=r.cycle_id,
            origin=r.a_origin,
            ext=r.a_end,
            mod_origin=r.a_origin,
            mod_ext=r.a_end,
            a_origin=r.a_origin,
            a_end=r.a_end,
            closed_time=p.time_ms,
            fail_reason="ABSORBIDO_POR_FUNCION_DOMINANTE",
            note="MINI_ABSORBIDO: se conserva en auditoría; no genera TT/FT retroactivo.",
        )
        self.readings.append(mini)
        self.mini_used = True
        self.emit(
            "MINI_ABSORBIDO",
            p,
            mini,
            parent_reading_id=r.reading_id,
            a=price_s(mini.a_size),
            a_origin=price_s(mini.a_origin.price),
            a_end=price_s(mini.a_end.price),
            scale=0,
        )

    def _set_pattern_status(self, kind: str, reading_id: str, status: str, **detail) -> None:
        for pattern in self.patterns:
            if pattern["type"] != kind or pattern["reading_id"] != reading_id:
                continue
            pattern["status"] = status
            pattern["final_status"] = status
            existing = json.loads(pattern["detail"] or "{}")
            existing.update(detail)
            pattern["detail"] = json.dumps(existing, ensure_ascii=False, sort_keys=True)

    def _set_pattern_by_id(self, pattern_id: str, status: str, **detail) -> None:
        if not pattern_id:
            return
        for pattern in self.patterns:
            if pattern["pattern_id"] != pattern_id:
                continue
            pattern["status"] = status
            pattern["final_status"] = status
            for key in ("origin_time", "origin_price", "end_time", "end_price", "size", "direction"):
                if key in detail:
                    pattern[key] = detail[key]
            existing = json.loads(pattern["detail"] or "{}")
            existing.update(detail)
            pattern["detail"] = json.dumps(existing, ensure_ascii=False, sort_keys=True)
            return

    def _split_dominant_after_tt(self, p: Pt, r: Reading) -> None:
        r.original_scale = r.scale
        r.original_confirmation_time = p.hms
        r.original_confirmation_price = price_s(p.price)
        r.closed_time = p.time_ms
        r.tt_confirmed = True
        r.tt_100_already_reached = True
        r.new1_origin = r.new1_origin or p
        r.new1_ext = p
        r.ft_ext = p
        r.ft_origin = p
        r.ft_window_start = p.bar
        r.ft_window_end = p.bar + 1
        r.ft_status = "WINDOW_OPEN"
        r.track_ft = True
        r.post_tt = True
        if r.derived_from_ft:
            r.state = TT_CONFIRMED
            r.final_priority = "LOCAL"
            r.track_ft = False
            r.ft_candidate = False
            r.ft_pattern_id = ""
            r.ft_status = ""
            return
        if not self.multi_scale:
            r.state = TT_CONFIRMED
            r.final_priority = "MAJOR"
            self.post_tt_anchor = r
            if self.dominant is r:
                self.dominant = None
            return
        if r is not self.dominant or r.generation >= 2:
            r.state = TT_CONFIRMED
            r.final_priority = "MAJOR"
            self.post_tt_anchor = r
            return
        r.state = "TT_MINOR_CONFIRMED"
        r.final_priority = "MINOR"
        self.minor_tt = r
        self.post_tt_anchor = r
        d = self._new_reading(
            p,
            r.direction,
            "MODULE",
            "DOMINANT_CONTINUATION",
            r.mod_ext,
            r.mod_ext,
            parent=r,
            note="CONTINUA_FUNCION_DOMINANTE",
            scale=1,
            generation=r.generation + 1,
        )
        d.mod_origin = r.mod_origin
        d.mod_ext = p
        d.origin = p
        d.ext = p
        d.tracker_only = True
        d.derived_from_tt = True
        self.dominant = d
        self.tracker_child = None
        self.current = r

    def _absorb_minor_by_dominant(self, p: Pt, d: Reading) -> None:
        mt = self.minor_tt
        if mt is None or mt.state != "TT_MINOR_CONFIRMED":
            return
        if (p.price - mt.mod_ext.price) * mt.direction <= 0:
            return
        mt.state = "TT_MINOR_ABSORBED_BY_DOMINANT"
        mt.final_priority = "ABSORBED"
        mt.absorbed_time = p.hms
        mt.absorbed_by_reading_id = d.reading_id
        mt.absorbed_by_cycle_id = d.cycle_id
        mt.note = "TT_MENOR_ABSORBIDO_POR_FUNCION_DOMINANTE"
        self.emit(
            "TT_MINOR_ABSORBED_BY_DOMINANT",
            p,
            mt,
            absorbed_by_reading_id=d.reading_id,
            absorbed_by_cycle_id=d.cycle_id,
            original_confirmation_time=mt.original_confirmation_time,
            original_confirmation_price=mt.original_confirmation_price,
        )
        self._set_pattern_status(
            "TT",
            mt.reading_id,
            "ABSORBIDO",
            absorbed_time=p.hms,
            absorbed_by_reading_id=d.reading_id,
        )
        ft = self.minor_ft
        if ft is not None:
            ft.state = "FT_MINOR_ABSORBED_BY_DOMINANT"
            ft.ft_status = FT_CANDIDATE_ABSORBED
            ft.final_priority = "ABSORBED"
            ft.absorbed_time = p.hms
            ft.absorbed_by_reading_id = d.reading_id
            ft.absorbed_by_cycle_id = d.cycle_id
            ft.closed_time = p.time_ms
            ft.note = "FT_MENOR_ABSORBIDO_POR_FUNCION_DOMINANTE"
            self.emit(
                "FT_MINOR_ABSORBED_BY_DOMINANT",
                p,
                ft,
                absorbed_by_reading_id=d.reading_id,
                absorbed_by_cycle_id=d.cycle_id,
            )
            self._set_pattern_by_id(mt.ft_pattern_id, FT_CANDIDATE_ABSORBED, absorbed_time=p.hms, absorbed_by_reading_id=d.reading_id)
            self._set_pattern_status(
                "FT",
                ft.reading_id,
                "ABSORBIDO",
                absorbed_time=p.hms,
                absorbed_by_reading_id=d.reading_id,
            )
            self._set_pattern_status(
                "TT",
                ft.reading_id,
                "ABSORBIDO",
                absorbed_time=p.hms,
                absorbed_by_reading_id=d.reading_id,
            )
            if self.current is ft:
                self.current = d
            if self.ft_child is ft:
                self.ft_child = None
            mt.ft_candidate = False
            mt.ft_status = "FT_MINOR_ABSORBED_BY_DOMINANT"
        self.minor_tt = None

    def _absorb_active_child(self, p: Pt, d: Reading) -> None:
        c = self.current
        if c is None or c is d or c is self.dominant or c is self.post_tt_anchor or c.tt_confirmed:
            return
        if c.state in (
            "ABSORBIDO_POR_FUNCION_DOMINANTE",
            "TT_MINOR_ABSORBED_BY_DOMINANT",
            "FT_MINOR_ABSORBED_BY_DOMINANT",
            "TT_FALLIDO",
        ):
            return
        if not (c.derived_from_ft or c.scale == 0):
            return
        c.state = "FT_MINOR_ABSORBED_BY_DOMINANT" if c.derived_from_ft else "ABSORBIDO_POR_FUNCION_DOMINANTE"
        c.final_priority = "ABSORBED"
        c.absorbed_time = p.hms
        c.absorbed_by_reading_id = d.reading_id
        c.absorbed_by_cycle_id = d.cycle_id
        c.closed_time = p.time_ms
        c.note = "FT_MENOR_ABSORBIDO_POR_FUNCION_DOMINANTE" if c.derived_from_ft else "MINI_ABSORBIDO_POR_FUNCION_DOMINANTE"
        self.emit(
            "FT_MINOR_ABSORBED_BY_DOMINANT" if c.derived_from_ft else "MINI_ABSORBIDO",
            p,
            c,
            absorbed_by_reading_id=d.reading_id,
            absorbed_by_cycle_id=d.cycle_id,
            original_state=c.state,
        )
        if self.current is c:
            self.current = d
        self.minor_ft = None

    def _module_step(self, p: Pt, r: Reading) -> bool:
        if (p.price - r.mod_ext.price) * r.direction > 0:
            r.mod_ext = p
            r.ext = p
            if r is self.dominant:
                self._absorb_minor_by_dominant(p, r)
                self._absorb_active_child(p, r)
                if self.tracker_child is not None and self.tracker_child.state in (
                    "TT_OK",
                    "TT_MINOR_ABSORBED_BY_DOMINANT",
                ):
                    self.tracker_child = None
            return True
        if (r.mod_ext.price - p.price) * r.direction >= MOVE:
            if r.tracker_only and r is self.dominant:
                anchor = self.post_tt_anchor
                if (
                    anchor is not None
                    and anchor.tt_confirmed
                    and anchor.state in (TT_CONFIRMED, TT_EXTENDING, POST_TT_FT_WINDOW)
                ):
                    # v0.7.2: a retracement inside a confirmed TT extension is
                    # handled by TRACK_FT_FROM_REAL_EXTREME, never by opening a
                    # second autonomous TT from the dominant module.
                    return False
                if self.minor_tt is not None or self.tracker_child is not None:
                    return False
                if self.current is not None and self.current.state in (
                    TT_PENDING,
                    "TT_MINOR_CONFIRMED",
                    "TT_MINOR_ABSORBED_BY_DOMINANT",
                ):
                    return False
                if self.minor_ft is not None:
                    ft = self.minor_ft
                    lo = min(ft.origin.price, ft.ft_ext.price)
                    hi = max(ft.origin.price, ft.ft_ext.price)
                    if lo <= p.price <= hi:
                        return False
                    self.minor_ft = None
                child = self._new_reading(
                    p,
                    r.direction,
                    "A",
                    "DOMINANT_A",
                    r.mod_ext,
                    p,
                    parent=r,
                    note="A_DESDE_MODULO_DOMINANTE",
                    scale=1,
                    generation=r.generation,
                )
                child.mod_origin = r.mod_origin
                child.mod_ext = r.mod_ext
                child.a_origin = r.mod_ext
                child.a_end = p
                self.tracker_child = child
                self.current = child
                self.emit(
                    "A_GRANDE_CONFIRMADA",
                    p,
                    child,
                    a_origin=price_s(child.a_origin.price),
                    a=price_s(child.a_size),
                    source="DOMINANT_MODULE",
                )
                return True
            self._start_a(p, r)
            return True
        return False

    def _a_step(self, p: Pt, r: Reading) -> bool:
        if r.a_origin is None or r.a_end is None:
            return False
        ad = -r.direction
        if (p.price - r.a_end.price) * ad > 0:
            r.a_end = p
            return True
        if (p.price - r.a_end.price) * r.direction >= MOVE:
            self._start_b(p, r)
            return True
        if (p.price - r.mod_ext.price) * r.direction > 0:
            r.mod_ext = p
            r.ext = p
            self.emit("A_INVALIDADA_MODULO", p, r, x=price_s(r.x_size))
            self._absorb_a(p, r)
            r.state = "MODULE"
            r.a_origin = None
            r.a_end = None
            return True
        return False

    def _check_b(self, p: Pt, r: Reading) -> bool:
        if r.a_end is None or r.b_ext is None:
            return False
        d = r.direction
        if (p.price - r.b_ext.price) * d > 0:
            r.b_ext = p
        elif (p.price - r.a_end.price) * d < 0:
            if r.aut_pt is None:
                b_size = r.b_size
                r.a_end = p
                r.b_origin = None
                r.b_ext = None
                r.state = "A"
                r.note = (r.note + "|B_ABSORBIDA_POR_A").strip("|")
                self.emit(
                    "B_ABSORBIDA_POR_A",
                    p,
                    r,
                    a=price_s(r.a_size),
                    b=price_s(b_size),
                    note="B candidata no alcanzó AUT; la A continúa y absorbe el recorrido.",
                )
                return True
            if r.gap_a:
                b_size = r.b_size
                a_end_before = p
                self.emit(
                    "TT_FALLIDO",
                    p,
                    r,
                    a_end=price_s(r.a_end.price),
                    b=price_s(b_size),
                    note="Evento historico; la A de gap continua y absorbe el B.",
                )
                r.a_end = p
                r.b_origin = None
                r.b_ext = None
                r.aut_pt = None
                r.tt_target = None
                r.tt_pt = None
                r.tt_ext = None
                r.state = "A"
                r.fail_pt = p
                r.fail_reason = "TT_FALLIDO_ABSORBIDO_POR_A_GAP"
                r.note = (r.note + "|TT_FALLIDO_ABSORBIDO_POR_A_GAP").strip("|")
                self.emit(
                    "TT_FALLIDO_ABSORBIDO_POR_A_GAP",
                    p,
                    r,
                    a=price_s(r.a_size),
                    b=price_s(b_size),
                    a_end_before=price_s(a_end_before.price),
                    note="La A de gap extiende su extremo; no se cierra la lectura.",
                )
                return True
            r.fail_pt = p
            r.fail_reason = "TT_FALLIDO_A_PERDIDA"
            r.state = "TT_FALLIDO"
            r.closed_time = p.time_ms
            self.emit("TT_FALLIDO", p, r, a_end=price_s(r.a_end.price), b=price_s(r.b_size))
            self.pending_rule(
                "PENDIENTE_POR_REGLA",
                p,
                r,
                "post_tt_fallido_no_definido",
                detail="No se crea nueva lectura ni reset sin regla cerrada.",
            )
            return False
        if r.aut_pt is None and aut_exceeded(r.b_size, r.a_size):
            r.aut_pt = p
            r.tt_target = r.a_end.price + d * r.x_size
            self.emit(
                "AUT",
                p,
                r,
                a=price_s(r.a_size),
                b=price_s(r.b_size),
                target=price_s(r.tt_target),
            )
            self.emit("TT_PENDIENTE", p, r, target=price_s(r.tt_target), x=price_s(r.x_size))
            r.state = "TT_PENDING"
        if r.tt_target is not None and (p.price - r.tt_target) * d >= 0:
            r.tt_pt = p
            r.tt_ext = p
            r.new1_origin = p
            r.new1_ext = p
            r.ft_ext = p
            r.ft_window_start = p.bar
            r.ft_window_end = p.bar + 1
            r.original_confirmation_time = p.hms
            r.original_confirmation_price = price_s(p.price)
            self.emit("TT_CONFIRMADO", p, r, target=price_s(r.tt_target), b=price_s(r.b_size), scale=r.scale)
            self.pattern("TT", "CONFIRMADO", r, p, target=price_s(r.tt_target), x=price_s(r.x_size), scale=r.scale)
            self.emit("NUEVO_1", p, r, origin=price_s(p.price))
            self._split_dominant_after_tt(p, r)
        return True

    def _post_tt_step(self, p: Pt, r: Reading) -> bool:
        if not r.tt_confirmed or r.new1_ext is None:
            return False
        if r.ft_ext is None:
            r.ft_ext = r.new1_ext
        if r.ft_origin is None:
            r.ft_origin = r.new1_ext
        d = r.direction

        # A. TRACK_TT_EXTENSION
        if (p.price - r.new1_ext.price) * d > 0:
            self._tt_extend(p, r)
            return True

        if not r.track_ft:
            return True

        # B. TRACK_FT_FROM_REAL_EXTREME
        if (p.price - r.ft_ext.price) * (-d) > 0:
            r.ft_ext = p
            if r.ft_candidate:
                self._set_pattern_by_id(
                    r.ft_pattern_id,
                    r.ft_status or FT_CANDIDATE,
                    end_time=p.hms,
                    end_price=price_s(p.price),
                    ext=price_s(p.price),
                    size=price_s(abs(p.price - r.ft_origin.price)) if r.ft_origin else "",
                )
                self._confirm_ft(p, r)
        if not r.ft_candidate:
            size = abs(r.new1_ext.price - r.ft_ext.price)
            if size >= MOVE:
                self._open_ft_candidate(p, r)
                return True
        elif self.ft_child is not None and self.ft_child is not r and self.ft_child.state == "MODULE":
            self.ft_child.mod_ext = r.ft_ext
            self.ft_child.ext = r.ft_ext
        return True

    def _tt_extend(self, p: Pt, r: Reading) -> None:
        old = r.new1_ext
        if old is None:
            old = p
        r.new1_ext = p
        r.tt_ext = p
        r.tt_real_extreme_seq = p.seq
        previous_state = r.state
        if r.state in (TT_CONFIRMED, POST_TT_FT_WINDOW):
            r.state = TT_EXTENDING
        self.emit(
            "TT_REAL_EXTREME_UPDATED",
            p,
            r,
            previous_extreme=price_s(old.price),
            previous_extreme_time=old.hms,
            real_extreme=price_s(p.price),
            real_extreme_sequence_id=p.seq,
            previous_state=previous_state,
        )
        if r.ft_candidate:
            self._absorb_ft_by_tt_extension(p, r)
        r.ft_ext = p
        r.ft_origin = p
        r.ft_candidate = False
        r.ft_pattern_id = ""
        r.ft_status = "WINDOW_OPEN"

    def _open_ft_candidate(self, p: Pt, r: Reading) -> Reading:
        size = abs(r.new1_ext.price - r.ft_ext.price)
        r.ft_candidate = True
        r.ft_origin = r.new1_ext
        r.ft_status = "FT_CANDIDATE"
        pattern = self.pattern(
            "FT",
            "FT_CANDIDATE",
            r,
            p,
            origin=price_s(r.ft_origin.price),
            ext=price_s(r.ft_ext.price),
            size=price_s(size),
            origin_time=r.ft_origin.hms,
            ext_time=r.ft_ext.hms,
            formal="ESTRUCTURAL_2_PUNTOS",
        )
        pattern["origin_time"] = r.ft_origin.hms
        pattern["origin_price"] = price_s(r.ft_origin.price)
        pattern["end_time"] = r.ft_ext.hms
        pattern["end_price"] = price_s(r.ft_ext.price)
        pattern["size"] = price_s(size)
        r.ft_pattern_id = pattern["pattern_id"]
        self.emit(
            "FT_CANDIDATE_OPENED",
            p,
            r,
            pattern_id=pattern["pattern_id"],
            origin=price_s(r.ft_origin.price),
            ext=price_s(r.ft_ext.price),
            size=price_s(size),
        )
        is_minor = r.state == "TT_MINOR_CONFIRMED"
        ft = self._new_reading(
            p,
            -r.direction,
            FT_CANDIDATE,
            "FT_CANDIDATE_OPENED",
            r.ft_origin,
            r.ft_ext,
            parent=r,
            note="FT_CANDIDATA_PROVISIONAL",
            scale=0 if is_minor else 1,
        )
        ft.ft_candidate = False
        ft.derived_from_ft = True
        ft.ft_ext = r.ft_ext
        ft.ft_origin = r.ft_origin
        ft.parent_tt_id = r.reading_id
        ft.coexisting_function = f"TT_EXTENSION:{r.reading_id}"
        r.coexisting_function = f"LOCAL_READING:{ft.reading_id}"
        ft.track_ft = False
        ft.ft_status = "FT_CANDIDATE"
        ft.mod_origin = r.ft_origin
        ft.mod_ext = r.ft_ext
        ft.origin = r.ft_origin
        ft.ext = r.ft_ext
        if is_minor:
            ft.final_priority = "MINOR"
            self.minor_ft = ft
        self.ft_child = ft
        self.current = ft
        self.emit("LOCAL_READING_OPENED", p, ft, parent_tt_id=r.reading_id, origin=price_s(r.ft_origin.price))
        return ft

    def _confirm_ft(self, p: Pt, r: Reading) -> None:
        if r.ft_status != "FT_CONFIRMED":
            r.ft_status = "FT_CONFIRMED"
            self._set_pattern_by_id(
                r.ft_pattern_id,
                "FT_CONFIRMED",
                confirmed_time=p.hms,
                confirmed_price=price_s(p.price),
                end_time=p.hms,
                end_price=price_s(p.price),
                ext=price_s(p.price),
            )
            self.emit("FT_CONFIRMED", p, r, pattern_id=r.ft_pattern_id, origin=price_s(r.ft_origin.price), ext=price_s(r.ft_ext.price))
        if self.ft_child is not None:
            self.ft_child.ft_status = "FT_CONFIRMED"

    def _absorb_ft_by_tt_extension(self, p: Pt, r: Reading) -> None:
        origin = r.ft_origin or r.new1_ext
        size = abs(p.price - origin.price) if origin is not None else 0
        previous = r.ft_status or "FT_CANDIDATE"
        self._set_pattern_by_id(
            r.ft_pattern_id,
            FT_CANDIDATE_ABSORBED,
            absorbed_time=p.hms,
            absorbed_by_reading_id=r.reading_id,
            previous_status=previous,
            extension_price=price_s(p.price),
        )
        self.emit(
            "FT_CANDIDATE_ABSORBED",
            p,
            r,
            pattern_id=r.ft_pattern_id,
            origin=price_s(origin.price) if origin else "",
            new_tt_extreme=price_s(p.price),
            size=price_s(size),
            previous_status=previous,
        )
        child = self.ft_child
        if child is not None:
            child.state = FT_CANDIDATE_ABSORBED
            child.final_priority = "ABSORBED"
            child.absorbed_time = p.hms
            child.absorbed_by_reading_id = r.reading_id
            child.absorbed_by_cycle_id = r.cycle_id
            child.closed_time = p.time_ms
            child.ft_status = FT_CANDIDATE_ABSORBED
            child.note = "FT_ABSORBIDA_POR_EXTENSION_TT"
            self.emit(
                "OSCILACION_POST_TT_ABSORBED_IN_DOMINANT_EXTENSION",
                p,
                child,
                reading_id=child.reading_id,
                parent_tt_id=r.reading_id,
                extension_price=price_s(p.price),
            )
            self._set_pattern_status("TT", child.reading_id, "ABSORBIDO", absorbed_by_reading_id=r.reading_id)
            self._set_pattern_status("FT", child.reading_id, FT_CANDIDATE_ABSORBED, absorbed_by_reading_id=r.reading_id)
            if self.current is child:
                self.current = r
            self.ft_child = None
        r.ft_candidate = False
        r.ft_pattern_id = ""
        r.ft_status = "FT_CANDIDATE_ABSORBED_BY_TT_EXTENSION"
        r.ft_origin = None
        r.ft_ext = p

    def _ft_candidate_step(self, p: Pt, r: Reading) -> bool:
        if r.mod_origin is None or r.mod_ext is None:
            return False
        d = r.direction
        if (p.price - r.mod_ext.price) * d > 0:
            r.mod_ext = p
            r.ext = p
            r.ft_ext = p
            if r.parent_tt_id:
                anchor = next((x for x in self.readings if x.reading_id == r.parent_tt_id), None)
                if anchor is not None and anchor.ft_candidate:
                    anchor.ft_ext = p
            return True
        if (p.price - r.mod_ext.price) * (-d) >= MOVE:
            if abs(r.mod_ext.price - r.mod_origin.price) < MIN_MODULE_STUDY:
                return False
            self._start_a(p, r)
            self.emit("LOCAL_READING_OPENED", p, r, local_state="A", parent_tt_id=r.parent_tt_id)
            return True
        return False

    def _advance(self, p: Pt, r: Reading) -> None:
        for _ in range(8):
            if r.state == "MODULE":
                changed = self._module_step(p, r)
            elif r.state == FT_CANDIDATE:
                changed = self._ft_candidate_step(p, r)
            elif r.state == "A":
                changed = self._a_step(p, r)
            elif r.state in ("B", TT_PENDING):
                changed = self._check_b(p, r)
            elif r.state in (TT_CONFIRMED, TT_EXTENDING, POST_TT_FT_WINDOW, "TT_OK", "TT_MINOR_CONFIRMED"):
                changed = self._post_tt_step(p, r)
            else:
                changed = False
            if not changed:
                break
            if self.current is not r and r is not self.dominant and r is not self.post_tt_anchor:
                break

    def step(self, p: Pt, bar: Bar) -> None:
        if self.current is None and self.dominant is None:
            self.seed_reading(p)
        if self.current is None and self.dominant is None:
            return
        if self.last_bar is None:
            self.last_bar = p.bar
            self.prev_close = bar.prev_close
        elif p.bar != self.last_bar:
            self._on_new_bar(p, bar)
        if self.dominant is not None and self.dominant is not self.current:
            self._advance(p, self.dominant)
        anchor = self.post_tt_anchor
        if anchor is not None and anchor is not self.dominant and anchor is not self.current:
            if anchor.state not in (TT_COMPLETED, "TT_MINOR_ABSORBED_BY_DOMINANT", FT_CANDIDATE_ABSORBED, "TT_FALLIDO"):
                self._advance(p, anchor)
        if self.current is not None:
            self._advance(p, self.current)
        self.last_pt = p

    def close(self, reason: str) -> None:
        seen: set[str] = set()
        for r in (self.dominant, self.current):
            if r is None or r.reading_id in seen:
                continue
            seen.add(r.reading_id)
            if r.closed_time is None:
                r.closed_time = self.last_pt.time_ms if self.last_pt else r.created_time
            r.note = (r.note + "|" + reason).strip("|")


def load_feed(path: Path) -> tuple[list[Pt], dict[int, Bar]]:
    df = pd.read_csv(path, sep=";", decimal=".")
    required = {"sequence_id", "time_msc", "bid"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"feed missing columns: {sorted(missing)}")
    df["time_msc"] = df["time_msc"].astype("int64")
    df["sequence_id"] = df["sequence_id"].astype("int64")
    df["bid"] = df["bid"].map(price_i)
    df = df.sort_values(["sequence_id"], kind="mergesort").reset_index(drop=True)
    points: list[Pt] = []
    bars: dict[int, Bar] = {}
    current_bar = None
    for row in df.itertuples(index=False):
        ts = int(row.time_msc)
        bar_idx = ts // 60000
        p = Pt(int(row.bid), int(row.sequence_id), ts, bar_idx)
        points.append(p)
        if current_bar is None or current_bar.idx != bar_idx:
            current_bar = Bar(
                idx=bar_idx,
                name=ms_to_hms(bar_idx * 60000)[:5],
                open=p,
                high=p,
                low=p,
                last=p,
                prev_close=None,
            )
            if bars:
                prev = bars[max(bars)]
                current_bar.prev_close = prev.last.price
            bars[bar_idx] = current_bar
        else:
            if p.price > current_bar.high.price:
                current_bar.high = p
            if p.price < current_bar.low.price:
                current_bar.low = p
            current_bar.last = p
    return points, bars


def filter_points(points: list[Pt], start: Optional[int], end: Optional[int]) -> list[Pt]:
    result = points
    if start is not None:
        result = [p for p in result if p.time_ms >= start]
    if end is not None:
        result = [p for p in result if p.time_ms <= end]
    return result


def run_engine(points: list[Pt], bars: dict[int, Bar], seed: Optional[Seed], multi_scale: bool = False) -> Engine:
    engine = Engine(seed, multi_scale=multi_scale)
    if not points:
        return engine
    first = points[0]
    if seed is not None:
        engine.seed_reading(first)
    for p in points:
        bar = bars[p.bar]
        engine.step(p, bar)
    engine.close("END_OF_FEED")
    evaluate_coverage(engine, points)
    return engine


def validate_engine(engine: Engine) -> list[str]:
    errors: list[str] = []
    active = [r for r in engine.readings if r.is_active]
    if len(active) > 2:
        errors.append(f"active_readings={len(active)} > 2: {[r.reading_id for r in active]}")
    ids = {r.reading_id for r in engine.readings}
    for r in engine.readings:
        if r.parent_reading_id and r.parent_reading_id not in ids:
            errors.append(f"{r.reading_id}: parent {r.parent_reading_id} missing")
        if r.state in (TT_CONFIRMED, TT_EXTENDING, POST_TT_FT_WINDOW, TT_COMPLETED, "TT_MINOR_CONFIRMED", "TT_MINOR_ABSORBED_BY_DOMINANT", "TT_FALLIDO") and r.aut_pt is None:
            if not (r.derived_from_ft and r.tt_pt is not None):
                errors.append(f"{r.reading_id}: TT state without AUT")
        if r.tt_confirmed and r.state == TT_PENDING:
            errors.append(f"{r.reading_id}: confirmed TT regressed to TT_PENDING")
        if r.state in (TT_CONFIRMED, TT_EXTENDING, POST_TT_FT_WINDOW, TT_COMPLETED) and (r.tt_pt is None or not r.tt_confirmed):
            errors.append(f"{r.reading_id}: TT state without historical TT_100")
        if r.scale not in (0, 1):
            errors.append(f"{r.reading_id}: scale {r.scale} outside 0..1")
    return errors


def structural_swings(points: list[Pt], threshold: int = MOVE) -> list[dict]:
    if len(points) < 2:
        return []
    swings: list[dict] = []
    start = points[0]
    direction = 0
    ext = points[0]
    for p in points[1:]:
        if direction == 0:
            if p.price >= start.price + threshold:
                direction = 1
                ext = p
            elif p.price <= start.price - threshold:
                direction = -1
                ext = p
        elif direction > 0:
            if p.price > ext.price:
                ext = p
            elif ext.price - p.price >= threshold:
                swings.append({"origin": start, "ext": ext, "direction": 1, "size": ext.price - start.price})
                start = ext
                direction = -1
                ext = p
        else:
            if p.price < ext.price:
                ext = p
            elif p.price - ext.price >= threshold:
                swings.append({"origin": start, "ext": ext, "direction": -1, "size": start.price - ext.price})
                start = ext
                direction = 1
                ext = p
    if direction > 0 and ext.price - start.price >= threshold:
        swings.append({"origin": start, "ext": ext, "direction": 1, "size": ext.price - start.price})
    elif direction < 0 and start.price - ext.price >= threshold:
        swings.append({"origin": start, "ext": ext, "direction": -1, "size": start.price - ext.price})
    return swings


def _reading_ranges(r: Reading) -> list[tuple[int, int]]:
    pairs = [
        (r.origin, r.ext),
        (r.mod_origin, r.mod_ext),
        (r.a_origin, r.a_end),
        (r.b_origin, r.b_ext),
        (r.tt_pt, r.tt_ext),
        (r.ft_origin, r.ft_ext),
    ]
    return [(min(a.price, b.price), max(a.price, b.price)) for a, b in pairs if a is not None and b is not None]


def _covered(engine: Engine, swing: dict) -> bool:
    lo = min(swing["origin"].price, swing["ext"].price)
    hi = max(swing["origin"].price, swing["ext"].price)
    for r in engine.readings:
        for rlo, rhi in _reading_ranges(r):
            if rlo <= lo and hi <= rhi:
                return True
    return False


def evaluate_coverage(engine: Engine, points: list[Pt]) -> None:
    engine.coverage_unresolved = []
    engine.TM_COVERAGE_OK = True
    for swing in structural_swings(points):
        if _covered(engine, swing):
            continue
        engine.coverage_unresolved.append(
            {
                "reason": "UNEXPLAINED_STRUCTURAL_MOVE",
                "origin_time": swing["origin"].hms,
                "origin_price": price_s(swing["origin"].price),
                "extreme_time": swing["ext"].hms,
                "extreme_price": price_s(swing["ext"].price),
                "direction": "UP" if swing["direction"] > 0 else "DOWN",
                "size": price_s(swing["size"]),
            }
        )
    if engine.coverage_unresolved:
        engine.TM_COVERAGE_OK = False
        p = engine.last_pt or points[-1]
        for item in engine.coverage_unresolved:
            note = "UNEXPLAINED_STRUCTURAL_MOVE"
            if note not in engine.pending:
                engine.pending.append(note)
            engine.emit("UNEXPLAINED_STRUCTURAL_MOVE", p, engine.current, **item)
            engine.emit("PENDIENTE_POR_REGLA", p, engine.current, note=note, **item)


def write_outputs(engine: Engine, out_dir: Path, stem: str) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    event_path = out_dir / f"{stem}_Eventos.csv"
    reading_path = out_dir / f"{stem}_Lecturas.csv"
    pattern_path = out_dir / f"{stem}_Patrones.csv"
    event_fields = [
        "event_id", "time", "time_ms", "sequence_id", "bar", "price", "kind",
        "reading_id", "cycle_id", "detail",
    ]
    reading_fields = [
        "reading_id", "cycle_id", "direction", "state", "scale", "origin_event",
        "parent_reading_id", "parent_cycle_id", "created_time", "closed_time",
        "module_origin", "module_extreme", "x", "a_origin", "a_end", "a",
        "b_origin", "b_extreme", "b", "aut_time", "aut_price", "tt_target",
        "tt_100_time", "tt_100_price", "tt_extreme", "new1_origin", "new1_extreme",
        "ft_extreme", "ft_candidate", "fail_time", "fail_price", "fail_reason", "note",
        "generation", "original_scale", "final_priority", "derived_from_tt", "derived_from_ft",
        "original_confirmation_time",
        "original_confirmation_price", "absorbed_time", "absorbed_by_reading_id",
        "absorbed_by_cycle_id", "parent_tt_id", "coexisting_function", "ft_status",
        "tt_confirmed", "tt_100_sequence_id", "tt_real_extreme_time",
        "tt_real_extreme_price", "tt_real_extreme_sequence_id", "coverage_role",
    ]
    pattern_fields = [
        "pattern_id", "type", "status", "final_status", "direction", "origin_time", "origin_price",
        "end_time", "end_price", "size", "reading_id", "cycle_id", "detail",
    ]
    with event_path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=event_fields)
        writer.writeheader()
        for event in engine.events:
            writer.writerow({k: event.get(k, "") for k in event_fields})
    with reading_path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=reading_fields)
        writer.writeheader()
        for r in sorted(engine.readings, key=lambda item: (item.created_time, item.reading_id)):
            writer.writerow(
                {
                    "reading_id": r.reading_id,
                    "cycle_id": r.cycle_id,
                    "direction": "UP" if r.direction > 0 else "DOWN",
                    "state": r.state,
                    "scale": r.scale,
                    "origin_event": r.origin_event,
                    "parent_reading_id": r.parent_reading_id or "",
                    "parent_cycle_id": r.parent_cycle_id or "",
                    "created_time": ms_to_text(r.created_time),
                    "closed_time": ms_to_text(r.closed_time) if r.closed_time else "",
                    "module_origin": price_s(r.mod_origin.price) if r.mod_origin else "",
                    "module_extreme": price_s(r.mod_ext.price) if r.mod_ext else "",
                    "x": price_s(r.x_size),
                    "a_origin": price_s(r.a_origin.price) if r.a_origin else "",
                    "a_end": price_s(r.a_end.price) if r.a_end else "",
                    "a": price_s(r.a_size),
                    "b_origin": price_s(r.b_origin.price) if r.b_origin else "",
                    "b_extreme": price_s(r.b_ext.price) if r.b_ext else "",
                    "b": price_s(r.b_size),
                    "aut_time": r.aut_pt.hms if r.aut_pt else "",
                    "aut_price": price_s(r.aut_pt.price) if r.aut_pt else "",
                    "tt_target": price_s(r.tt_target) if r.tt_target is not None else "",
                    "tt_100_time": r.tt_pt.hms if r.tt_pt else "",
                    "tt_100_price": price_s(r.tt_pt.price) if r.tt_pt else "",
                    "tt_extreme": price_s(r.tt_ext.price) if r.tt_ext else "",
                    "new1_origin": price_s(r.new1_origin.price) if r.new1_origin else "",
                    "new1_extreme": price_s(r.new1_ext.price) if r.new1_ext else "",
                    "ft_extreme": price_s(r.ft_ext.price) if r.ft_ext else "",
                    "ft_candidate": int(r.ft_candidate),
                    "fail_time": r.fail_pt.hms if r.fail_pt else "",
                    "fail_price": price_s(r.fail_pt.price) if r.fail_pt else "",
                    "fail_reason": r.fail_reason,
                    "note": r.note,
                    "generation": r.generation,
                    "original_scale": r.original_scale,
                    "final_priority": r.final_priority,
                    "derived_from_tt": int(r.derived_from_tt),
                    "derived_from_ft": int(r.derived_from_ft),
                    "original_confirmation_time": r.original_confirmation_time,
                    "original_confirmation_price": r.original_confirmation_price,
                    "absorbed_time": r.absorbed_time,
                    "absorbed_by_reading_id": r.absorbed_by_reading_id,
                    "absorbed_by_cycle_id": r.absorbed_by_cycle_id,
                    "parent_tt_id": r.parent_tt_id,
                    "coexisting_function": r.coexisting_function,
                    "ft_status": r.ft_status,
                    "tt_confirmed": int(r.tt_confirmed),
                    "tt_100_sequence_id": r.tt_pt.seq if r.tt_pt else "",
                    "tt_real_extreme_time": r.new1_ext.hms if r.new1_ext else "",
                    "tt_real_extreme_price": price_s(r.new1_ext.price) if r.new1_ext else "",
                    "tt_real_extreme_sequence_id": r.tt_real_extreme_seq if r.tt_real_extreme_seq is not None else "",
                    "coverage_role": r.coverage_role,
                }
            )
    with pattern_path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=pattern_fields)
        writer.writeheader()
        for pattern in engine.patterns:
            writer.writerow({k: pattern.get(k, "") for k in pattern_fields})
    return [event_path, reading_path, pattern_path]


def build_seed(args: argparse.Namespace, base_ms: Optional[int] = None) -> Optional[Seed]:
    if args.seed is None:
        return None
    direction = 1 if args.seed_direction == "up" else -1
    price = price_i(args.seed_price)
    if args.seed == "module":
        return Seed("MODULE", direction, price)
    if args.seed == "gap_a":
        return Seed(
            "GAP_A",
            direction,
            price,
            module_origin=price_i(args.module_origin) if args.module_origin is not None else price,
            module_extreme=price_i(args.module_extreme) if args.module_extreme is not None else price,
            a_origin=price_i(args.a_origin) if args.a_origin is not None else price,
            a_end=price_i(args.a_end) if args.a_end is not None else price,
        )
    if args.seed in ("tt", "tt_pending", "tt_confirmed", "tt_extending", "post_tt"):
        if args.seed == "tt" and not args.seed_state:
            raise ValueError("--seed tt is ambiguous: pass --seed-state tt_pending|tt_confirmed|tt_extending|post_tt")
        if args.a_origin is None or args.a_end is None or args.tt_target is None:
            raise ValueError("--seed tt requires --a-origin, --a-end and --tt-target")
        state = args.seed_state or {
            "tt_pending": TT_PENDING,
            "tt_confirmed": TT_CONFIRMED,
            "tt_extending": TT_EXTENDING,
            "post_tt": POST_TT_FT_WINDOW,
        }[args.seed]
        state_alias = {
            "tt_pending": TT_PENDING,
            "tt_confirmed": TT_CONFIRMED,
            "tt_extending": TT_EXTENDING,
            "post_tt": POST_TT_FT_WINDOW,
        }
        state = state_alias.get(state.lower() if isinstance(state, str) else state, state)
        kind = {
            TT_PENDING: "TT_PENDING",
            TT_CONFIRMED: "TT_CONFIRMED",
            TT_EXTENDING: "TT_EXTENDING",
            POST_TT_FT_WINDOW: "POST_TT",
        }.get(state)
        if kind is None:
            raise ValueError(f"unknown --seed-state {state}")
        if state == TT_PENDING:
            return Seed(
                kind,
                direction,
                price,
                module_origin=price_i(args.module_origin) if args.module_origin is not None else price,
                module_extreme=price_i(args.module_extreme) if args.module_extreme is not None else price,
                a_origin=price_i(args.a_origin),
                a_end=price_i(args.a_end),
                tt_target=price_i(args.tt_target),
                tt_state=state,
                parent_tt_id=args.parent_tt_id or "",
            )
        missing = [
            name
            for name, value in (
                ("--tt-100-time", args.tt_100_time),
                ("--tt-100-price", args.tt_100_price),
                ("--tt-100-seq", args.tt_100_seq),
                ("--module-origin", args.module_origin),
                ("--module-extreme", args.module_extreme),
            )
            if value is None
        ]
        if missing:
            raise ValueError(f"INVALID_SEED_MISSING_TT100: missing {', '.join(missing)}")
        return Seed(
            kind,
            direction,
            price,
            module_origin=price_i(args.module_origin),
            module_extreme=price_i(args.module_extreme),
            a_origin=price_i(args.a_origin),
            a_end=price_i(args.a_end),
            tt_target=price_i(args.tt_target),
            tt_state=state,
            tt_100_time=parse_hms(args.tt_100_time, base_ms),
            tt_100_price=price_i(args.tt_100_price),
            tt_100_seq=args.tt_100_seq,
            tt_real_extreme_time=parse_hms(args.tt_real_extreme_time, base_ms) if args.tt_real_extreme_time else None,
            tt_real_extreme_price=price_i(args.tt_real_extreme_price) if args.tt_real_extreme_price is not None else None,
            tt_real_extreme_seq=args.tt_real_extreme_seq,
            parent_tt_id=args.parent_tt_id or "",
            module_size=price_i(args.module_size) if args.module_size is not None else None,
            final_a=price_i(args.final_a) if args.final_a is not None else None,
            aut_time=parse_hms(args.aut_time, base_ms) if args.aut_time else None,
            aut_price=price_i(args.aut_price) if args.aut_price is not None else None,
            ft_window_start_bar=args.ft_window_start_bar,
            ft_window_end_bar=args.ft_window_end_bar,
            ft_state=args.ft_state or "",
            last_processed_sequence_id=args.last_processed_sequence_id,
        )
    raise ValueError(f"unknown seed {args.seed}")


def selftest() -> None:
    assert not aut_exceeded(825, 630)
    assert aut_exceeded(826, 630)
    assert not aut_exceeded(279, 200)
    assert aut_exceeded(280, 200)

    def pt(price: int, seq: int, bar: int = 0) -> Pt:
        return Pt(price, seq, 1792167600000 + seq * 1000, bar)

    def bar_of(points: list[Pt]) -> dict[int, Bar]:
        first = points[0]
        high = max(points, key=lambda p: p.price)
        low = min(points, key=lambda p: p.price)
        last = points[-1]
        return {0: Bar(0, "TEST", first, high, low, last, None)}

    points = [pt(10000, 1), pt(11000, 2), pt(10800, 3), pt(11000, 4), pt(11080, 5), pt(11800, 6), pt(11600, 7)]
    engine = run_engine(points, bar_of(points), Seed("MODULE", 1, 10000))
    kinds = [e["kind"] for e in engine.events]
    assert "A_GRANDE_CONFIRMADA" in kinds
    assert "AUT" in kinds
    assert "TT_CONFIRMADO" in kinds
    assert "FT_CANDIDATE_OPENED" in kinds, kinds
    assert any(p["type"] == "TT" for p in engine.patterns)

    points_fail = [pt(10000, 1), pt(11000, 2), pt(10800, 3), pt(11000, 4), pt(11080, 5), pt(10799, 6)]
    engine_fail = run_engine(points_fail, bar_of(points_fail), Seed("MODULE", 1, 10000))
    assert any(e["kind"] == "TT_FALLIDO" for e in engine_fail.events)
    assert any(e["kind"] == "PENDIENTE_POR_REGLA" for e in engine_fail.events)

    points_gap = [pt(10000, 1), pt(10200, 2, 0), pt(10100, 3, 1)]
    bars_gap = {
        0: Bar(0, "T0", points_gap[0], points_gap[1], points_gap[0], points_gap[1], None),
        1: Bar(1, "T1", points_gap[2], points_gap[2], points_gap[2], points_gap[2], 10200),
    }
    engine_gap = run_engine(points_gap, bars_gap, Seed("MODULE", 1, 10000))
    assert any(e["kind"] in ("A_GAP_INICIO", "GAP") for e in engine_gap.events)

    points_gr = [
        pt(1000000, 1, 0),
        pt(1002500, 2, 0),
        pt(1002200, 3, 1),
        pt(1001600, 4, 1),
        pt(1002600, 5, 1),
        pt(1001500, 6, 1),
        pt(1003500, 7, 1),
        pt(1004000, 8, 1),
    ]
    bars_gr = {
        0: Bar(0, "T0", points_gr[0], points_gr[1], points_gr[0], points_gr[1], None),
        1: Bar(1, "T1", points_gr[2], points_gr[6], points_gr[5], points_gr[7], 1002500),
    }
    engine_gr = run_engine(points_gr, bars_gr, Seed("MODULE", 1, 1000000), multi_scale=True)
    assert any(e["kind"] == "TT_FALLIDO_ABSORBIDO_POR_A_GAP" for e in engine_gr.events), engine_gr.events
    assert any(e["kind"] == "TT_CONFIRMADO" for e in engine_gr.events), engine_gr.events
    gap_readings = [r for r in engine_gr.readings if r.gap_a and r.tt_pt is not None]
    assert gap_readings, [(r.reading_id, r.state) for r in engine_gr.readings]
    gr = gap_readings[0]
    assert gr.a_size == 700 and gr.b_size == 2500 and gr.tt_target == 1004000, (gr.a_size, gr.b_size, gr.tt_target)
    active = [r for r in engine_gr.readings if r.is_active]
    assert 1 <= len(active) <= 2, [(r.reading_id, r.state) for r in active]

    shifted = [pt(p.price + 5000, p.seq, p.bar) for p in points]
    engine_shifted = run_engine(shifted, bar_of(shifted), Seed("MODULE", 1, 15000))
    shifted_kinds = {e["kind"] for e in engine_shifted.events}
    assert {"A_GRANDE_CONFIRMADA", "AUT", "TT_CONFIRMADO", "FT_CANDIDATE_OPENED"} <= shifted_kinds, shifted_kinds

    inverted = [pt(20000 - (p.price - 10000), p.seq, p.bar) for p in points]
    engine_inverted = run_engine(inverted, bar_of(inverted), Seed("MODULE", -1, 20000))
    inverted_kinds = {e["kind"] for e in engine_inverted.events}
    assert {"A_GRANDE_CONFIRMADA", "AUT", "TT_CONFIRMADO", "FT_CANDIDATE_OPENED"} <= inverted_kinds, inverted_kinds
    assert all(r.direction == -1 for r in engine_inverted.readings if r.state in ("TT_OK", "TT_MINOR_CONFIRMED")), [
        (r.reading_id, r.direction, r.state) for r in engine_inverted.readings
    ]

    print(f"SELFTEST OK v{VERSION}: 15 comprobaciones")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=f"TM core v{VERSION}")
    parser.add_argument("--feed", type=Path)
    parser.add_argument("--out", type=Path, default=Path("out_v072"))
    parser.add_argument("--stem", default="v072")
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--seed", choices=["module", "gap_a", "tt", "tt_pending", "tt_confirmed", "tt_extending", "post_tt"])
    parser.add_argument(
        "--seed-state",
        choices=[
            TT_PENDING,
            TT_CONFIRMED,
            TT_EXTENDING,
            POST_TT_FT_WINDOW,
            "tt_pending",
            "tt_confirmed",
            "tt_extending",
            "post_tt",
        ],
    )
    parser.add_argument("--seed-direction", choices=["up", "down"], default="up")
    parser.add_argument("--seed-price", type=float)
    parser.add_argument("--parent-tt-id")
    parser.add_argument("--module-origin", type=float)
    parser.add_argument("--module-extreme", type=float)
    parser.add_argument("--module-size", type=float)
    parser.add_argument("--a-origin", type=float)
    parser.add_argument("--a-end", type=float)
    parser.add_argument("--final-a", type=float)
    parser.add_argument("--aut-time")
    parser.add_argument("--aut-price", type=float)
    parser.add_argument("--tt-target", type=float)
    parser.add_argument("--tt-100-time")
    parser.add_argument("--tt-100-price", type=float)
    parser.add_argument("--tt-100-seq", type=int)
    parser.add_argument("--tt-real-extreme-time")
    parser.add_argument("--tt-real-extreme-price", type=float)
    parser.add_argument("--tt-real-extreme-seq", type=int)
    parser.add_argument("--ft-window-start-bar", type=int)
    parser.add_argument("--ft-window-end-bar", type=int)
    parser.add_argument("--ft-state", default="")
    parser.add_argument("--last-processed-sequence-id", type=int)
    parser.add_argument("--multi-scale", action="store_true", help="Scheduler multiescala (default).")
    parser.add_argument("--single-scale", action="store_true", help="Legacy: una sola escala, sin absorcion contextual.")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)

    if args.selftest:
        selftest()
        return 0

    if args.feed is None:
        parser.error("--feed is required unless --selftest")
    if args.seed is not None and args.seed_price is None:
        parser.error("--seed-price is required with --seed")
    if args.multi_scale and args.single_scale:
        parser.error("--multi-scale and --single-scale are mutually exclusive")
    multi_scale = not args.single_scale

    points_all, bars = load_feed(args.feed)
    base_ms = points_all[0].time_ms if points_all else None
    try:
        start = parse_hms(args.start, base_ms) if args.start else None
        end = parse_hms(args.end, base_ms) if args.end else None
        seed = build_seed(args, base_ms)
    except ValueError as exc:
        parser.error(str(exc))
        return 2
    points = filter_points(points_all, start, end)
    if not points:
        raise SystemExit("no points in range")
    engine = run_engine(points, bars, seed, multi_scale=multi_scale)
    errors = validate_engine(engine)
    if errors:
        print(json.dumps({"validation_errors": errors}, ensure_ascii=False, indent=2))
        return 1
    paths = write_outputs(engine, args.out, args.stem)
    summary = {
        "version": VERSION,
        "mode": "multi_scale" if multi_scale else "single_scale",
        "ticks": len(points),
        "seed": args.seed,
        "readings": len(engine.readings),
        "events": len(engine.events),
        "patterns": len(engine.patterns),
        "a_invalidated": sum(1 for e in engine.events if e["kind"] == "A_INVALIDADA_MODULO"),
        "minor_tt_absorbed": sum(1 for e in engine.events if e["kind"] == "TT_MINOR_ABSORBED_BY_DOMINANT"),
        "active_operational": sum(1 for r in engine.readings if r.is_active),
        "max_scale": max((r.scale for r in engine.readings), default=0),
        "validation": "OK",
        "pending": engine.pending,
        "TM_COVERAGE_OK": engine.TM_COVERAGE_OK,
        "coverage_unresolved": engine.coverage_unresolved,
        "outputs": [str(p) for p in paths],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())





