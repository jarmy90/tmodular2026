# -*- coding: utf-8 -*-
"""TM — Lector experimental v2 para la misión de perfeccionamiento del árbol.

No es el motor definitivo. Aplica el árbol v2.19 con las correcciones expresas
del mandato 2026-10-30:

  * plano: |open - close_prev| < 0,25; 0,25 exactos NO es plano.
  * 1: direccion y origen de la transicion, no de la vela siguiente.
  * nuevo 1: nace en el AUT / A usada como tendencia / C usada como tendencia,
    con direccion y origen de la funcion transformada.
  * 2: una sola candidata en su vela; 100 % de 1; imposible al cierre.
  * 3: retroceso funcional (filtro de ruido 2 puntos, <= 50 % de 2),
    recuperacion y superacion estricta del extremo de 2.
  * modulo: extremos estructurales con propietario; nunca rango bruto de velas.
  * A: CONTRARY_MOVE_PENDING. No hay umbral fijo de autonomia. A se confirma
    funcionalmente cuando B alcanza el 100 % de A o cuando A supera la base del
    modulo (A usada como tendencia). Es una REGLA UNIVERSAL PROPUESTA, no canon.
  * B: candidata provisional; 100 %-127 % + 0,25 = B Grande; estricto = AUT.
  * C: C Grande desde el giro posterior a B Grande; CUT al superar el final de A;
    C usada como tendencia al superar la base del modulo.
  * gap: sin 2; A/B/A usada como tendencia implicitas; nuevo 1 desde la apertura.

Modos de A:
  --a-mode b100     (por defecto) A se confirma cuando B alcanza 100 % de A.
  --a-mode pending  A queda pendiente; no se evaluan B/C/AUT (lectura fiel sin
                    regla de autonomia).
  --a-mode bturn    A se confirma en el giro de B de 2 puntos (sensibilidad).

Uso:
  python blind_reader_v2.py --trace out.jsonl --events out.csv \
      --generations out.csv --bar-close out.csv --summary out.json
"""
from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FEED = ROOT / "TM_CANON_ACTIVO" / "02_TICKS" / "TM_TICKFEED_1615_1730.csv"

PLANO = 25            # 0,25 en centimos
NOISE = 200           # 2,00 puntos: filtro de ruido, no autonomia
AUT_MULT = 127
AUT_ADD = 25          # +0,25 -> 25 centimos
GAP_MIN = 200         # 2,00 puntos: umbral experimental de gap significativo


def price_i(s: str) -> int:
    return int(round(float(s.replace(",", ".")) * 100))


def hhmm(t_ms: int) -> str:
    d = datetime.datetime.fromtimestamp(t_ms / 1000, datetime.timezone.utc)
    return d.strftime("%H:%M:%S.%f")[:-3]


def bar_hhmm(bar: int) -> str:
    return datetime.datetime.fromtimestamp(bar * 60, datetime.timezone.utc).strftime("%H:%M")


@dataclass
class Tick:
    seq: int
    time_ms: int
    bar: int
    price: int


@dataclass
class Gen:
    gid: int
    parent: int
    reason: str
    phase: str = "ONE_LIVE"

    one_dir: int = 0
    one_origin: int = 0
    one_extreme: int = 0
    one_size: int = 0
    one_st: int = 0
    one_kt: int = 0
    one_bar: int = -1
    one_status: str = ""
    one_frozen: bool = False
    one_extreme_st: int = 0

    two_origin: int = 0
    two_extreme: int = 0
    two_extreme_st: int = 0
    two_dir: int = 0
    two_size: int = 0
    two_st: int = 0
    two_kt: int = 0
    two_status: str = ""
    two_tail: int = 0
    two_seen_dir: bool = False

    three_extreme: int = 0
    three_extreme_st: int = 0
    three_st: int = 0
    three_kt: int = 0
    three_status: str = ""
    retr_active: bool = False
    retr_extreme: int = 0
    retr_size: int = 0
    retr_valid: bool = False
    retr_50: bool = False

    mod_origin: int = 0
    mod_origin_st: int = 0
    mod_extreme: int = 0
    mod_extreme_st: int = 0
    mod_size: int = 0
    mod_status: str = ""
    mod_owner: str = ""

    a_origin: int = 0
    a_extreme: int = 0
    a_extreme_st: int = 0
    a_dir: int = 0
    a_size: int = 0
    a_status: str = ""
    a_st: int = 0
    a_kt: int = 0

    b_origin: int = 0
    b_dir: int = 0
    b_extreme: int = 0
    b_extreme_st: int = 0
    b_measure: int = 0
    b_status: str = ""
    b_st: int = 0
    b_grande_kt: int = 0

    c_origin: int = 0
    c_dir: int = 0
    c_extreme: int = 0
    c_extreme_st: int = 0
    c_size: int = 0
    c_status: str = ""
    c_st: int = 0
    cut_kt: int = 0
    c_trend_kt: int = 0

    aut_kt: int = 0
    aut_price: int = 0
    aut_reason: str = ""

    tt_target: int = 0
    tt_status: str = ""
    tt_st: int = 0
    tt_kt: int = 0
    tt_extreme: int = 0
    tt_last_ev: int = 0

    end_kt: int = 0
    end_reason: str = ""
    events: list = field(default_factory=list)

    def ev(self, t: Tick, event: str, detail: str = "") -> None:
        self.events.append({
            "seq": t.seq, "time_ms": t.time_ms, "bar": t.bar,
            "gid": self.gid, "parent": self.parent, "event": event,
            "detail": detail,
        })


class Reader:
    def __init__(self, ticks: list[Tick], a_mode: str = "b100"):
        self.ticks = ticks
        self.a_mode = a_mode
        self.gens: list[Gen] = []
        self.active: Gen | None = None
        self.prev_close = 0
        self.cur_bar = -1
        self.last_price = 0
        self.last_time = 0
        self.bars: dict[int, dict] = {}
        self.trace: list[dict] = []
        self.bar_close: list[dict] = []
        self._gid = 0

    # ------------------------------------------------------------------ helpers
    def new_gen(self, t: Tick, direction: int, origin: int, st: int, kt: int,
                reason: str) -> Gen:
        self._gid += 1
        g = Gen(
            gid=self._gid,
            parent=self.active.gid if self.active else 0,
            reason=reason,
            phase="ONE_LIVE",
            one_dir=direction,
            one_origin=origin,
            one_extreme=origin,
            one_size=0,
            one_st=st,
            one_kt=kt,
            one_bar=t.bar,
            one_status="CONFIRMED",
            one_extreme_st=st,
        )
        if (t.price - origin) * direction > 0:
            g.one_extreme = t.price
            g.one_size = abs(t.price - origin)
            g.one_extreme_st = t.time_ms
        self.gens.append(g)
        self.active = g
        g.ev(t, "NEW_ONE", f"reason={reason} dir={direction} origin={origin} "
                           f"st={hhmm(st) if st else ''} kt={hhmm(kt) if kt else ''}")
        return g

    def start_initial_bar(self, t: Tick) -> None:
        self._gid += 1
        g = Gen(gid=self._gid, parent=0, reason="INITIAL", phase="INITIAL_BAR",
                one_dir=0, one_origin=t.price, one_extreme=t.price,
                one_size=0, one_st=t.time_ms, one_bar=t.bar,
                one_status="CANDIDATE", one_extreme_st=t.time_ms)
        self.gens.append(g)
        self.active = g
        g.ev(t, "ONE_CANDIDATE_INITIAL", f"open={t.price}")

    def confirm_initial_one(self, t: Tick) -> None:
        g = self.active
        if not g or g.phase != "INITIAL_BAR":
            return
        b = self.bars.get(g.one_bar)
        if not b:
            return
        d = 1 if b["c"] > b["o"] else (-1 if b["c"] < b["o"] else 0)
        if d == 0:
            d = 1 if b["c"] >= g.one_origin else -1
        g.one_dir = d
        g.one_origin = b["h"] if d < 0 else b["l"]
        g.one_extreme = b["l"] if d < 0 else b["h"]
        g.one_size = b["h"] - b["l"]
        g.one_status = "CONFIRMED"
        g.one_kt = t.time_ms
        g.one_frozen = True
        g.phase = "WAIT_TWO"
        g.ev(t, "ONE_CONFIRMED_INITIAL",
             f"dir={d} origin={g.one_origin} extreme={g.one_extreme} "
             f"size={g.one_size} kt={hhmm(g.one_kt)}")

    def freeze_one(self, t: Tick) -> bool:
        g = self.active
        if not g or g.phase != "ONE_LIVE":
            return False
        if g.one_size <= 0:
            # 1 nacio sin recorrido: se le concede la vela siguiente para medirse
            g.one_bar = t.bar
            g.ev(t, "ONE_ZERO_SIZE_DEFERRAL",
                 "1 sin medida al abrir la vela siguiente; se difiere la pregunta por 2")
            return False
        g.one_frozen = True
        g.one_kt = self.last_time
        g.phase = "WAIT_TWO"
        g.ev(t, "ONE_FROZEN",
             f"origin={g.one_origin} extreme={g.one_extreme} size={g.one_size} "
             f"st={hhmm(g.one_st)} kt={hhmm(g.one_kt)}")
        return True

    # ------------------------------------------------------------------- module
    def module_by_discard(self, t: Tick, include_two: bool) -> None:
        g = self.active
        if not g:
            return
        g.mod_origin = g.one_origin
        g.mod_origin_st = g.one_st
        candidates = [(g.one_extreme, g.one_extreme_st, "1")]
        if include_two and g.two_extreme:
            candidates.append((g.two_extreme, g.two_extreme_st, "2"))
        if g.one_dir > 0:
            g.mod_extreme, g.mod_extreme_st, g.mod_owner = max(candidates)
        else:
            g.mod_extreme, g.mod_extreme_st, g.mod_owner = min(candidates)
        g.mod_size = abs(g.mod_extreme - g.mod_origin)
        g.mod_status = "BY_DISCARD_1_2" if include_two else "BY_DISCARD_1"
        g.phase = "A_PENDING"
        g.a_origin = g.mod_extreme
        g.a_extreme = g.mod_extreme
        g.a_extreme_st = g.mod_extreme_st
        g.a_dir = -g.one_dir
        g.a_size = 0
        g.a_st = g.mod_extreme_st
        g.a_kt = 0
        g.a_status = "CONTRARY_MOVE_PENDING"
        g.ev(t, "MODULE_BY_DISCARD",
             f"origin={g.mod_origin} extreme={g.mod_extreme} size={g.mod_size} "
             f"owner={g.mod_owner} status={g.mod_status}")

    def module_1_2_3(self, t: Tick) -> None:
        g = self.active
        if not g:
            return
        g.mod_origin = g.one_origin
        g.mod_origin_st = g.one_st
        g.mod_extreme = g.three_extreme
        g.mod_extreme_st = g.three_extreme_st
        g.mod_owner = "3"
        g.mod_size = abs(g.mod_extreme - g.mod_origin)
        g.mod_status = "REGULAR_1_2_3"
        # Q2: 3 conserva su tick de confirmacion, pero su extremo sigue vivo
        # hasta que comienza A. El modulo y el origen de A usan el extremo
        # final real de 3, no el tick de confirmacion.
        g.phase = "THREE_LIVE"
        g.a_origin = g.mod_extreme
        g.a_extreme = g.mod_extreme
        g.a_extreme_st = g.mod_extreme_st
        g.a_dir = -g.one_dir
        g.a_size = 0
        g.a_st = g.mod_extreme_st
        g.a_kt = 0
        g.a_status = "WAIT_A_START"
        g.ev(t, "MODULE_1_2_3_CONFIRMED",
             f"origin={g.mod_origin} extreme={g.mod_extreme} size={g.mod_size} "
             f"kt3={hhmm(g.three_kt)}; extremo de 3 vivo")

    def module_1_2(self, t: Tick) -> None:
        g = self.active
        if not g:
            return
        g.mod_origin = g.one_origin
        g.mod_origin_st = g.one_st
        candidates = [(g.one_extreme, g.one_extreme_st, "1"),
                      (g.two_extreme, g.two_extreme_st, "2")]
        if g.one_dir > 0:
            g.mod_extreme, g.mod_extreme_st, g.mod_owner = max(candidates)
        else:
            g.mod_extreme, g.mod_extreme_st, g.mod_owner = min(candidates)
        g.mod_size = abs(g.mod_extreme - g.mod_origin)
        g.mod_status = "MODULE_1_2"
        g.three_status = "IMPOSSIBLE"
        g.phase = "A_PENDING"
        g.a_origin = g.mod_extreme
        g.a_extreme = g.mod_extreme
        g.a_extreme_st = g.mod_extreme_st
        g.a_dir = -g.one_dir
        g.a_size = 0
        g.a_st = g.mod_extreme_st
        g.a_kt = 0
        g.a_status = "CONTRARY_MOVE_PENDING"
        g.ev(t, "MODULE_1_2", f"origin={g.mod_origin} extreme={g.mod_extreme} "
                               f"size={g.mod_size} owner={g.mod_owner}")

    # --------------------------------------------------------------------- two
    def eval_two(self, t: Tick) -> None:
        g = self.active
        if not g:
            return
        gap = t.price - self.prev_close
        g.two_origin = t.price
        g.two_extreme = t.price
        g.two_extreme_st = t.time_ms
        g.two_dir = g.one_dir
        g.two_st = t.time_ms
        g.two_tail = 0
        g.two_seen_dir = False
        if abs(gap) >= PLANO:
            g.two_status = "IMPOSSIBLE"
            g.two_kt = t.time_ms
            g.ev(t, "TWO_IMPOSSIBLE_NO_FLAT",
                 f"|gap|={abs(gap)} >= {PLANO} open={t.price} prev_close={self.prev_close}")
            if abs(gap) >= GAP_MIN:
                g.ev(t, "GAP_IMPLICIT_ABAUT",
                     f"gap={gap} > {GAP_MIN}: A/B/A usada como tendencia implicitas; "
                     f"nuevo 1 desde la apertura")
                g.phase = "DONE"
                g.end_kt = t.time_ms
                g.end_reason = "GAP"
                self.new_gen(t, 1 if gap > 0 else -1, t.price, t.time_ms, t.time_ms,
                             "GAP_IMPLICIT_ABAUT")
            else:
                self.module_by_discard(t, include_two=False)
            return
        g.two_status = "CANDIDATE"
        g.phase = "TWO_LIVE"
        g.ev(t, "TWO_CANDIDATE",
             f"flat |gap|={abs(gap)} origin={t.price} dir={g.two_dir} "
             f"one_size={g.one_size}")

    def on_two_tick(self, t: Tick) -> None:
        g = self.active
        if not g or g.phase != "TWO_LIVE":
            return
        d = g.two_dir
        if not g.two_seen_dir:
            if (t.price - g.two_origin) * d > 0:
                g.two_seen_dir = True
            else:
                g.two_tail = max(g.two_tail, (g.two_origin - t.price) * d)
        if (t.price - g.two_extreme) * d > 0:
            g.two_extreme = t.price
            g.two_extreme_st = t.time_ms
        g.two_size = abs(g.two_extreme - g.two_origin)
        if g.two_tail > PLANO:
            g.two_status = "IMPOSSIBLE_TAIL"
            g.two_kt = t.time_ms
            g.ev(t, "TWO_IMPOSSIBLE_TAIL",
                 f"cola inicial={g.two_tail} > {PLANO}")
            self.module_by_discard(t, include_two=False)
            return
        if g.two_size >= g.one_size:
            g.two_status = "CONFIRMED"
            g.two_kt = t.time_ms
            g.phase = "WAIT_THREE"
            g.retr_active = False
            g.retr_valid = False
            g.retr_50 = False
            g.ev(t, "TWO_CONFIRMED",
                 f"measure={g.two_size} >= 100% de 1 ({g.one_size})")

    # ------------------------------------------------------------------- three
    def on_three_tick(self, t: Tick) -> None:
        g = self.active
        if not g or g.phase != "WAIT_THREE":
            return
        d = g.two_dir
        if (t.price - g.two_extreme) * d > 0:
            if g.retr_valid:
                g.three_status = "CONFIRMED"
                g.three_extreme = t.price
                g.three_extreme_st = t.time_ms
                g.three_st = g.two_kt
                g.three_kt = t.time_ms
                g.ev(t, "THREE_CONFIRMED",
                     f"extremo={t.price} estricto sobre 2={g.two_extreme} "
                     f"retroceso={g.retr_size}")
                self.module_1_2_3(t)
                return
            g.two_extreme = t.price
            g.two_extreme_st = t.time_ms
            g.two_size = abs(g.two_extreme - g.two_origin)
            g.retr_active = False
            g.retr_valid = False
            g.retr_50 = False
            return
        # retroceso contrario a 2
        if not g.retr_active:
            g.retr_active = True
            g.retr_extreme = t.price
            g.ev(t, "RETRACE_START", f"desde extremo de 2 {g.two_extreme}")
        if (t.price - g.retr_extreme) * (-d) > 0:
            g.retr_extreme = t.price
        g.retr_size = abs(g.retr_extreme - g.two_extreme)
        if g.retr_size * 2 > g.two_size:
            g.three_status = "IMPOSSIBLE"
            g.ev(t, "THREE_IMPOSSIBLE_50",
                 f"retroceso={g.retr_size} > 50% de 2 ({g.two_size / 2})")
            self.module_1_2(t)
            return
        if g.retr_size * 2 == g.two_size and not g.retr_50:
            g.retr_50 = True
            g.ev(t, "FIFTY_PERCENT_EXACT",
                 f"retroceso={g.retr_size} = 50% de 2; arbol N-009 lo admite, "
                 f"mandato lo deja abierto")
        if g.retr_size >= NOISE:
            g.retr_valid = True

    def on_three_live_tick(self, t: Tick) -> None:
        """Q2: 3 sigue actualizando su extremo hasta que comienza A."""
        g = self.active
        if not g or g.phase != "THREE_LIVE":
            return
        d = g.two_dir
        if (t.price - g.three_extreme) * d > 0:
            g.three_extreme = t.price
            g.three_extreme_st = t.time_ms
            g.mod_extreme = t.price
            g.mod_extreme_st = t.time_ms
            g.mod_size = abs(g.mod_extreme - g.mod_origin)
            g.a_origin = g.mod_extreme
            g.a_extreme = g.mod_extreme
            g.a_extreme_st = t.time_ms
            g.a_size = 0
            g.a_st = t.time_ms
            g.ev(t, "THREE_EXTENDED",
                 f"extremo final de 3={t.price} modulo={g.mod_size}")
            return
        if (t.price - g.three_extreme) * (-d) >= NOISE:
            # giro contrario estructural (filtro de ruido 2 puntos): comienza A
            # desde el extremo final de 3. Un tick de 0,1 no abre A.
            g.a_status = "CONTRARY_MOVE_PENDING"
            g.a_origin = g.three_extreme
            g.a_extreme = g.three_extreme
            g.a_extreme_st = g.three_extreme_st
            g.a_st = g.three_extreme_st
            g.a_dir = -d
            g.a_size = 0
            g.a_kt = 0
            g.phase = "A_PENDING"
            g.ev(t, "A_START_AFTER_3",
                 f"desde extremo final de 3={g.three_extreme} "
                 f"modulo={g.mod_size}")
            self.on_a_tick(t)

    # ----------------------------------------------------------------------- A
    def reset_bc(self, g: Gen) -> None:
        g.b_origin = 0
        g.b_dir = 0
        g.b_extreme = 0
        g.b_extreme_st = 0
        g.b_measure = 0
        g.b_status = ""
        g.b_st = 0
        g.b_grande_kt = 0
        g.c_origin = 0
        g.c_dir = 0
        g.c_extreme = 0
        g.c_extreme_st = 0
        g.c_size = 0
        g.c_status = ""
        g.c_st = 0
        g.cut_kt = 0
        g.c_trend_kt = 0

    def on_a_tick(self, t: Tick) -> None:
        g = self.active
        if not g or g.phase != "A_PENDING":
            return
        d = g.a_dir
        # Q2: si el precio hace un nuevo extremo de 3 (direccion del modulo),
        # el 3 sigue vivo y absorbe A/B. No se confirma un A prematuro por una
        # oscilacion interna de la vela.
        if (t.price - g.mod_extreme) * (-d) > 0:
            g.a_status = "ABSORBED_IN_ACTIVE_FUNCTION"
            g.three_extreme = t.price
            g.three_extreme_st = t.time_ms
            g.mod_extreme = t.price
            g.mod_extreme_st = t.time_ms
            g.mod_size = abs(g.mod_extreme - g.mod_origin)
            g.mod_owner = "3_extension"
            g.a_origin = g.mod_extreme
            g.a_extreme = g.mod_extreme
            g.a_extreme_st = t.time_ms
            g.a_size = 0
            g.a_st = t.time_ms
            g.a_status = "CONTRARY_MOVE_PENDING"
            self.reset_bc(g)
            g.phase = "THREE_LIVE"
            g.ev(t, "THREE_EXTENDED_ABSORBS_AB",
                 f"nuevo extremo final de 3={g.mod_extreme} modulo={g.mod_size}")
            return
        if (t.price - g.a_extreme) * d > 0:
            g.a_extreme = t.price
            g.a_extreme_st = t.time_ms
            g.a_size = abs(g.a_extreme - g.a_origin)
            if g.a_size > g.mod_size and g.b_status == "":
                g.a_status = "TREND"
                g.aut_kt = t.time_ms
                g.aut_price = t.price
                g.aut_reason = "A_USED_AS_TREND"
                g.ev(t, "A_USED_AS_TREND",
                     f"A size={g.a_size} > modulo={g.mod_size} precio={t.price}")
                g.phase = "DONE"
                g.end_kt = t.time_ms
                g.end_reason = "A_USED_AS_TREND"
                self.new_gen(t, d, g.a_origin, g.a_st, t.time_ms, "A_USED_AS_TREND")
                return
        # B provisional: giro contrario a A de al menos el filtro de ruido.
        # En modo pending no se abre B: A queda como recorrido contrario
        # pendiente y no se inventa autonomia.
        if self.a_mode == "pending":
            return
        disp = (t.price - g.a_extreme) * (-d)
        if disp >= NOISE:
            if g.b_status == "":
                g.b_origin = g.a_extreme
                g.b_dir = -d
                g.b_extreme = t.price
                g.b_extreme_st = t.time_ms
                g.b_measure = disp
                g.b_st = t.time_ms
                g.b_status = "PROVISIONAL"
                if self.a_mode == "bturn":
                    g.a_status = "CONFIRMED"
                    g.a_kt = t.time_ms
                    g.ev(t, "A_CONFIRMED_BY_B_TURN",
                         f"A size={g.a_size} B turn={disp}")
                g.ev(t, "B_CANDIDATE_PROVISIONAL",
                     f"desde A={g.a_extreme} disp={disp} A_status={g.a_status}")
                g.phase = "B_LIVE"
            self.on_b_tick(t)

    # ----------------------------------------------------------------------- B
    def on_b_tick(self, t: Tick) -> None:
        g = self.active
        if not g or g.phase != "B_LIVE":
            return
        d = g.b_dir
        # B falla si el precio vuelve mas alla del extremo de A en direccion A
        if (t.price - g.a_extreme) * g.a_dir > 0:
            g.a_extreme = t.price
            g.a_extreme_st = t.time_ms
            g.a_size = abs(g.a_extreme - g.a_origin)
            g.b_status = ""
            g.b_origin = 0
            g.b_extreme = 0
            g.b_measure = 0
            g.b_st = 0
            g.b_grande_kt = 0
            g.ev(t, "B_FAILED_A_EXTENDS",
                 f"A={g.a_extreme} size={g.a_size}")
            if g.a_size > g.mod_size:
                g.a_status = "TREND"
                g.aut_kt = t.time_ms
                g.aut_price = t.price
                g.aut_reason = "A_USED_AS_TREND"
                g.ev(t, "A_USED_AS_TREND",
                     f"A size={g.a_size} > modulo={g.mod_size}")
                g.phase = "DONE"
                g.end_kt = t.time_ms
                g.end_reason = "A_USED_AS_TREND"
                self.new_gen(t, g.a_dir, g.a_origin, g.a_st, t.time_ms,
                             "A_USED_AS_TREND")
                return
            g.phase = "A_PENDING"
            return
        if (t.price - g.b_extreme) * d > 0:
            g.b_extreme = t.price
            g.b_extreme_st = t.time_ms
        g.b_measure = abs(g.b_extreme - g.b_origin)
        # Q2: un nuevo extremo de 3 mientras B no es AUT absorbe A/B; el 3
        # conserva la finalidad y sigue actualizando su extremo final.
        if g.a_size > 0 and (t.price - g.mod_extreme) * g.two_dir > 0:
            limit = g.a_size * AUT_MULT / 100 + AUT_ADD
            if g.b_measure <= limit:
                g.three_extreme = t.price
                g.three_extreme_st = t.time_ms
                g.mod_extreme = t.price
                g.mod_extreme_st = t.time_ms
                g.mod_size = abs(g.mod_extreme - g.mod_origin)
                g.mod_owner = "3_extension"
                g.a_status = "CONTRARY_MOVE_PENDING"
                g.a_origin = g.mod_extreme
                g.a_extreme = g.mod_extreme
                g.a_extreme_st = t.time_ms
                g.a_size = 0
                g.a_st = t.time_ms
                self.reset_bc(g)
                g.phase = "THREE_LIVE"
                g.ev(t, "THREE_EXTENDED_ABSORBS_AB",
                     f"B={g.b_measure} <= AUT; nuevo extremo 3={g.three_extreme}")
                return
        if g.a_size <= 0:
            return
        if g.b_measure >= g.a_size:
            if g.a_status != "CONFIRMED":
                g.a_status = "CONFIRMED"
                g.a_kt = t.time_ms
                g.ev(t, "A_CONFIRMED_BY_B_100",
                     f"B={g.b_measure} >= A={g.a_size}; "
                     f"structural_time={hhmm(g.a_st)} knowledge_time={hhmm(t.time_ms)}")
            if not g.b_grande_kt:
                g.b_grande_kt = t.time_ms
                g.b_status = "GRANDE"
                g.ev(t, "B_GRANDE",
                     f"measure={g.b_measure} >= 100% de A ({g.a_size})")
            limit = g.a_size * AUT_MULT / 100 + AUT_ADD
            if g.b_measure > limit:
                g.b_status = "AUT"
                g.aut_kt = t.time_ms
                g.aut_price = t.price
                g.aut_reason = "AUT_B"
                g.ev(t, "AUT_B",
                     f"measure={g.b_measure} > 127%+0,25 de A ({limit:.2f})")
                # TT del modulo anterior
                g.tt_target = g.a_extreme + g.mod_size * (-g.a_dir)
                g.tt_status = "POSSIBLE"
                g.tt_st = g.a_extreme_st
                if (t.price - g.tt_target) * (-g.a_dir) >= 0:
                    g.tt_status = "CONFIRMED"
                    g.tt_kt = t.time_ms
                    g.tt_extreme = t.price
                    g.ev(t, "TT_CONFIRMED_AT_AUT", f"target={g.tt_target}")
                g.phase = "DONE"
                g.end_kt = t.time_ms
                g.end_reason = "AUT_B"
                self.new_gen(t, g.b_dir, g.b_origin, g.a_extreme_st, t.time_ms,
                             "AUT_B")
                return
        if g.b_grande_kt:
            # C Grande: giro contrario a B de al menos el filtro de ruido
            if g.c_status == "":
                disp_c = (t.price - g.b_extreme) * g.a_dir
                if disp_c >= NOISE:
                    g.c_origin = g.b_extreme
                    g.c_dir = g.a_dir
                    g.c_extreme = t.price
                    g.c_extreme_st = t.time_ms
                    g.c_size = disp_c
                    g.c_status = "C_GRANDE"
                    g.c_st = g.b_extreme_st or g.b_grande_kt
                    g.phase = "C_LIVE"
                    g.ev(t, "C_GRANDE",
                         f"desde B={g.b_extreme} dir={g.c_dir} size={disp_c}")
                    return
            if g.c_status:
                self.on_c_tick(t)

    # ----------------------------------------------------------------------- C
    def on_c_tick(self, t: Tick) -> None:
        g = self.active
        if not g or g.phase != "C_LIVE":
            return
        d = g.c_dir
        # si B crea nuevo extremo, C se cancela
        if (t.price - g.b_extreme) * g.b_dir > 0:
            g.c_status = ""
            g.c_origin = 0
            g.c_extreme = 0
            g.c_size = 0
            g.phase = "B_LIVE"
            g.ev(t, "C_CANCELLED_B_NEW_EXTREME", f"B={t.price}")
            self.on_b_tick(t)
            return
        if (t.price - g.c_extreme) * d > 0:
            g.c_extreme = t.price
            g.c_extreme_st = t.time_ms
            g.c_size = abs(g.c_extreme - g.c_origin)
        if not g.cut_kt and (t.price - g.a_extreme) * d > 0:
            g.cut_kt = t.time_ms
            g.ev(t, "CUT", f"C={t.price} supera final de A={g.a_extreme}")
        if not g.c_trend_kt and (t.price - g.mod_origin) * d > 0:
            g.c_trend_kt = t.time_ms
            g.ev(t, "C_USED_AS_TREND",
                 f"C={t.price} supera base del modulo={g.mod_origin}")
            g.phase = "DONE"
            g.end_kt = t.time_ms
            g.end_reason = "C_USED_AS_TREND"
            self.new_gen(t, d, g.c_origin, g.c_st, t.time_ms, "C_USED_AS_TREND")

    # ---------------------------------------------------------------------- TT
    def update_tt(self, g: Gen, t: Tick) -> None:
        if not g.tt_status:
            return
        d_mod = -g.a_dir
        if g.tt_status == "POSSIBLE":
            if (t.price - g.tt_target) * d_mod >= 0:
                g.tt_status = "CONFIRMED"
                g.tt_kt = t.time_ms
                g.tt_extreme = t.price
                g.ev(t, "TT_CONFIRMED", f"target={g.tt_target} precio={t.price}")
            elif t.time_ms > g.aut_kt and (t.price - g.a_extreme) * g.a_dir >= 0:
                g.tt_status = "FAILED"
                g.ev(t, "TT_FAILED", f"precio={t.price} toca final de A={g.a_extreme}")
        elif g.tt_status in ("CONFIRMED", "EXTENDED"):
            if (t.price - g.tt_extreme) * d_mod > 0:
                g.tt_extreme = t.price
                g.tt_status = "EXTENDED"
                if abs(g.tt_extreme - g.tt_last_ev) >= NOISE:
                    g.tt_last_ev = g.tt_extreme
                    g.ev(t, "TT_EXTENDED", f"extreme={t.price}")

    # -------------------------------------------------------------------- main
    def run(self) -> "Reader":
        for t in self.ticks:
            new_bar = t.bar != self.cur_bar
            if new_bar:
                if self.cur_bar != -1:
                    self.on_bar_close(self.cur_bar, self.last_price, self.last_time)
                self.cur_bar = t.bar
                b = self.bars.setdefault(t.bar, {"o": t.price, "h": t.price,
                                                 "l": t.price, "c": t.price})
                self.on_bar_open(t)
            else:
                b = self.bars[t.bar]
                b["h"] = max(b["h"], t.price)
                b["l"] = min(b["l"], t.price)
                b["c"] = t.price
            self.last_price = t.price
            self.last_time = t.time_ms
            g = self.active
            if g:
                if g.phase == "INITIAL_BAR":
                    pass
                elif g.phase == "ONE_LIVE":
                    if (t.price - g.one_extreme) * g.one_dir > 0:
                        g.one_extreme = t.price
                        g.one_extreme_st = t.time_ms
                        g.one_size = abs(g.one_extreme - g.one_origin)
                elif g.phase == "TWO_LIVE":
                    self.on_two_tick(t)
                elif g.phase == "WAIT_THREE":
                    self.on_three_tick(t)
                elif g.phase == "THREE_LIVE":
                    self.on_three_live_tick(t)
                elif g.phase == "A_PENDING":
                    self.on_a_tick(t)
                elif g.phase == "B_LIVE":
                    self.on_b_tick(t)
                elif g.phase == "C_LIVE":
                    self.on_c_tick(t)
            for x in self.gens:
                self.update_tt(x, t)
            self.trace.append(self.snapshot(t))
        self.finalize()
        return self

    def on_bar_open(self, t: Tick) -> None:
        g = self.active
        if g is None:
            self.start_initial_bar(t)
            return
        if g.phase == "INITIAL_BAR":
            return
        if g.phase == "ONE_LIVE" and t.bar != g.one_bar:
            if self.freeze_one(t):
                self.eval_two(t)
            return
        if g.phase == "WAIT_TWO":
            self.eval_two(t)
            return
        # TWO_LIVE se resuelve al cierre; el resto continua entre velas

    def on_bar_close(self, bar: int, price: int, time_ms: int) -> None:
        self.prev_close = price
        g = self.active
        if not g:
            return
        if g.phase == "INITIAL_BAR":
            self.confirm_initial_one(Tick(-1, time_ms, bar, price))
            return
        if g.phase == "TWO_LIVE":
            g.two_status = "IMPOSSIBLE_CLOSE"
            g.two_kt = time_ms
            g.ev(Tick(-1, time_ms, bar, price), "TWO_IMPOSSIBLE_CLOSE",
                 f"cierre sin 100% de 1: measure={g.two_size} one={g.one_size}")
            self.module_by_discard(Tick(-1, time_ms, bar, price), include_two=True)
            return

    # ---------------------------------------------------------------- snapshot
    def snapshot(self, t: Tick) -> dict:
        g = self.active
        row = {
            "sequence_id": t.seq, "time_ms": t.time_ms, "bar": t.bar,
            "time": hhmm(t.time_ms), "price": t.price,
            "gid": g.gid if g else 0, "parent": g.parent if g else 0,
            "phase": g.phase if g else "",
            "one_dir": g.one_dir if g else 0,
            "one_origin": g.one_origin if g else 0,
            "one_extreme": g.one_extreme if g else 0,
            "one_size": g.one_size if g else 0,
            "one_status": g.one_status if g else "",
            "two_status": g.two_status if g else "",
            "two_size": g.two_size if g else 0,
            "three_status": g.three_status if g else "",
            "mod_origin": g.mod_origin if g else 0,
            "mod_extreme": g.mod_extreme if g else 0,
            "mod_size": g.mod_size if g else 0,
            "mod_status": g.mod_status if g else "",
            "mod_owner": g.mod_owner if g else "",
            "a_status": g.a_status if g else "",
            "a_origin": g.a_origin if g else 0,
            "a_extreme": g.a_extreme if g else 0,
            "a_size": g.a_size if g else 0,
            "b_status": g.b_status if g else "",
            "b_measure": g.b_measure if g else 0,
            "c_status": g.c_status if g else "",
            "tt_status": g.tt_status if g else "",
            "tt_target": g.tt_target if g else 0,
            "events": [e for e in (g.events if g else []) if e["seq"] == t.seq],
            "secondary": [{"gid": x.gid, "reason": x.reason, "tt": x.tt_status,
                           "tt_target": x.tt_target}
                          for x in self.gens if x is not g and x.tt_status],
        }
        return row

    def finalize(self) -> None:
        g = self.active
        if g:
            g.end_reason = g.end_reason or "OPEN_AT_FEED_END"
            g.end_kt = g.end_kt or self.last_time
        # estado al cierre de cada vela
        seen = set()
        for row in reversed(self.trace):
            if row["bar"] in seen:
                continue
            seen.add(row["bar"])
            self.bar_close.append(row)

    def summary(self) -> dict:
        counts = {}
        for g in self.gens:
            counts[g.end_reason] = counts.get(g.end_reason, 0) + 1
        return {
            "a_mode": self.a_mode,
            "ticks": len(self.ticks),
            "generations": len(self.gens),
            "end_reasons": counts,
            "trace_sha256": hashlib.sha256(
                json.dumps(self.trace, sort_keys=True, ensure_ascii=False).encode()
            ).hexdigest(),
            "first_tick": self.ticks[0].seq if self.ticks else None,
            "last_tick": self.ticks[-1].seq if self.ticks else None,
        }


def load_ticks(path: Path) -> list[Tick]:
    out = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            out.append(Tick(int(row["sequence_id"]), int(row["time_msc"]),
                            int(row["time_msc"]) // 60000, price_i(row["bid"])))
    return out


def bar_of(h: str) -> int:
    hh, mm = h.split(":")
    return int(hh) * 60 + int(mm)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="t_from", default="16:15")
    ap.add_argument("--to", dest="t_to", default="17:29")
    ap.add_argument("--prefix-bar", default=None)
    ap.add_argument("--a-mode", choices=["b100", "pending", "bturn"], default="b100")
    ap.add_argument("--trace")
    ap.add_argument("--events")
    ap.add_argument("--generations")
    ap.add_argument("--bar-close")
    ap.add_argument("--summary")
    ap.add_argument("--hash-only", action="store_true")
    args = ap.parse_args(argv)

    ticks = load_ticks(FEED)
    b0, b1 = bar_of(args.t_from), bar_of(args.t_to)
    ticks = [t for t in ticks if b0 <= t.bar % 1440 <= b1]
    if args.prefix_bar:
        pb = bar_of(args.prefix_bar)
        ticks = [t for t in ticks if t.bar % 1440 <= pb]

    rd = Reader(ticks, a_mode=args.a_mode).run()

    if args.hash_only:
        blob = json.dumps(rd.trace, sort_keys=True, ensure_ascii=False).encode()
        print(hashlib.sha256(blob).hexdigest())
        return 0

    if args.trace:
        with open(args.trace, "w", encoding="utf-8") as f:
            for row in rd.trace:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
    if args.events:
        with open(args.events, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["sequence_id", "time", "bar", "gid", "parent", "event", "detail"])
            for g in rd.gens:
                for e in g.events:
                    w.writerow([e["seq"], hhmm(e["time_ms"]), bar_hhmm(e["bar"]),
                                e["gid"], e["parent"], e["event"], e["detail"]])
    if args.generations:
        with open(args.generations, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow([
                "gid", "parent", "reason", "end_reason", "end_time",
                "one_dir", "one_origin", "one_extreme", "one_size", "one_st", "one_kt",
                "two_origin", "two_extreme", "two_size", "two_status", "two_kt",
                "three_extreme", "three_status", "three_kt",
                "mod_origin", "mod_extreme", "mod_size", "mod_status", "mod_owner",
                "a_origin", "a_extreme", "a_size", "a_status", "a_st", "a_kt",
                "b_origin", "b_extreme", "b_measure", "b_status", "b_grande_kt",
                "aut_kt", "aut_reason",
                "c_origin", "c_extreme", "c_size", "c_status", "cut_kt", "c_trend_kt",
                "tt_target", "tt_status", "tt_kt",
            ])
            for g in rd.gens:
                w.writerow([
                    g.gid, g.parent, g.reason, g.end_reason,
                    hhmm(g.end_kt) if g.end_kt else "",
                    g.one_dir, g.one_origin, g.one_extreme, g.one_size,
                    hhmm(g.one_st) if g.one_st else "",
                    hhmm(g.one_kt) if g.one_kt else "",
                    g.two_origin, g.two_extreme, g.two_size, g.two_status,
                    hhmm(g.two_kt) if g.two_kt else "",
                    g.three_extreme, g.three_status,
                    hhmm(g.three_kt) if g.three_kt else "",
                    g.mod_origin, g.mod_extreme, g.mod_size, g.mod_status, g.mod_owner,
                    g.a_origin, g.a_extreme, g.a_size, g.a_status,
                    hhmm(g.a_st) if g.a_st else "",
                    hhmm(g.a_kt) if g.a_kt else "",
                    g.b_origin, g.b_extreme, g.b_measure, g.b_status,
                    hhmm(g.b_grande_kt) if g.b_grande_kt else "",
                    hhmm(g.aut_kt) if g.aut_kt else "", g.aut_reason,
                    g.c_origin, g.c_extreme, g.c_size, g.c_status,
                    hhmm(g.cut_kt) if g.cut_kt else "",
                    hhmm(g.c_trend_kt) if g.c_trend_kt else "",
                    g.tt_target, g.tt_status,
                    hhmm(g.tt_kt) if g.tt_kt else "",
                ])
    if args.bar_close:
        with open(args.bar_close, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["bar", "time", "gid", "phase", "one_dir", "one_size",
                        "two_status", "three_status", "mod_size", "a_status",
                        "a_size", "b_status", "b_measure", "c_status",
                        "tt_status", "tt_target"])
            for row in sorted(rd.bar_close, key=lambda r: r["bar"]):
                w.writerow([bar_hhmm(row["bar"]), row["time"], row["gid"],
                            row["phase"], row["one_dir"], row["one_size"],
                            row["two_status"], row["three_status"], row["mod_size"],
                            row["a_status"], row["a_size"], row["b_status"],
                            row["b_measure"], row["c_status"], row["tt_status"],
                            row["tt_target"]])
    if args.summary:
        with open(args.summary, "w", encoding="utf-8") as f:
            json.dump(rd.summary(), f, ensure_ascii=False, indent=2)
    if not any([args.trace, args.events, args.generations, args.summary]):
        for g in rd.gens:
            print(f"--- G{g.gid} parent={g.parent} reason={g.reason} "
                  f"end={g.end_reason} phase={g.phase}")
            for e in g.events:
                print(f"  {hhmm(e['time_ms'])} {e['event']:30s} {e['detail']}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
