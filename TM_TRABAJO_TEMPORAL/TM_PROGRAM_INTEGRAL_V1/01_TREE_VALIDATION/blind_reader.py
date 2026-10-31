# -*- coding: utf-8 -*-
"""
TM - Lector causal tick a tick para FASE A (lectura ciega 16:49-17:29).

No es el motor definitivo. Es un instrumento de lectura que aplica SOLO las
reglas cerradas del mandato 4.1-4.10 y hace explicitas, con etiqueta, las
politicas adoptadas donde el arbol aun no decide.

Reglas cerradas aplicadas:
  4.1 plano ................ |open - close_prev| < 0,25 (estricto)
  4.2 funcion 2 ............ misma direccion que 1, desde apertura plana
  4.3 funcion 3 ............ retroceso valido + recuperacion + extremo estricto
  4.4 A/B/C/AUT ............ 100 % y 127 % + 0,25; AUT estricto
  4.5 AUT -> nuevo 1 ....... inmediato
  4.6 gap .................. sin 2; resolucion implicita; nuevo 1 en apertura
  4.7 umbral 2 puntos ...... ruido vs movimiento potencial, no crea funcion sola
  4.8 TT ................... patron, confirma en el primer tick que alcanza
  4.9 concurrencia ......... lecturas con referencias independientes
  4.10 structural/knowledge time

Politicas explicitas (H) y dudas abiertas (Q):
  H1  la funcion 1 se mide por el rango direccional de su vela (v005: 16,2).
  H2  A se confirma con 2,00 puntos contrarios y sin recuperar el extremo.
  H3  el retroceso valido de 2 exige >= 2,00 puntos y <= 50 % de 2.
  H4  B Grande es un hito monotono; A puede seguir extendiendose.
  H5  TT se evalua en cada tick; no espera cierre de movimiento.
  H6  el TT de una lectura sobrevive al AUT y sigue como patron.
  H7  la resolucion implicita del gap se registra como lectura secundaria
      esbozada, no se desarrolla como escalera completa.
  Q_GAP  umbral de "gap significativo" no definido por el arbol.
  Q_TAIL tamano exacto de la cola inicial prohibitiva no definido.
  Q_BASE "base del modulo" = origen del modulo (lectura adoptada).
  Q_FT   confirmacion estructural del FT no definida: BLOCKED.

Uso:
  python blind_reader.py --from 16:15 --to 17:29 --trace out.jsonl ...
  python blind_reader.py --prefix-bar 16:55 --hash-only
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

PLANO = 25          # 0,25 en centimos
NOISE = 200         # 2,00 puntos
A_FLOOR = 600       # H_A: minimo teorico v2.5 para autonomia de A (configurable)
AUT_MULT = 127      # 127 %
AUT_ADD = 25        # +0,25

FUNC_BY_PHASE = {
    "ONE_LIVE": "1",
    "WAIT_ONE": "1",
    "WAIT_TWO": "1",
    "TWO_LIVE": "2",
    "WAIT_THREE": "2",
    "WAIT_A": "A",
    "A_LIVE": "A",
    "B_LIVE": "B",
    "C_LIVE": "C",
    "CLOSED": "-",
}

EXPECTED_BY_PHASE = {
    "ONE_LIVE": "cierre de 1",
    "WAIT_ONE": "nueva vela 1",
    "WAIT_TWO": "2",
    "TWO_LIVE": "confirmacion de 2",
    "WAIT_THREE": "3",
    "WAIT_A": "A Grande",
    "A_LIVE": "B candidata",
    "B_LIVE": "B Grande / AUT",
    "C_LIVE": "C Grande / CUT",
    "CLOSED": "-",
}

QUESTION_BY_PHASE = {
    "ONE_LIVE": "¿que direccion y medida tiene 1?",
    "WAIT_ONE": "¿cual es la nueva vela 1 tras la transicion?",
    "WAIT_TWO": "¿la vela siguiente abre en plano y alcanza el 100 % de 1?",
    "TWO_LIVE": "¿2 alcanza el 100 % de 1 antes del cierre?",
    "WAIT_THREE": "¿hay retroceso valido y se supera el extremo de 2?",
    "WAIT_A": "¿el recorrido contrario tiene autonomia de A Grande?",
    "A_LIVE": "¿el retorno confirma B candidata?",
    "B_LIVE": "¿B alcanza 100 % de A, 127 % + 0,25 o ninguno?",
    "C_LIVE": "¿C supera el final de A (CUT) o la base del modulo?",
    "CLOSED": "-",
}


def price_i(s: str) -> int:
    return int(round(float(s.replace(",", ".")) * 100))


@dataclass
class Tick:
    seq: int
    time_ms: int
    bar: int
    price: int


@dataclass
class Reading:
    rid: str
    direction: int
    phase: str = "ONE_LIVE"
    parent: str = ""
    origin_reason: str = "INITIAL"
    generation: int = 0
    history: list = field(default_factory=list)
    patterns: list = field(default_factory=list)

    one_bar: int = 0
    one_open: int = 0
    one_high: int = 0
    one_low: int = 0
    one_origin: int = 0
    one_extreme: int = 0
    one_size: int = 0
    one_status: str = "CANDIDATE"
    one_st: int = 0
    one_kt: int = 0

    two_origin: int = 0
    two_extreme: int = 0
    two_size: int = 0
    two_status: str = ""
    two_st: int = 0
    two_kt: int = 0
    two_tail_max: int = 0
    two_saw_direction: bool = False

    retr_active: bool = False
    retr_extreme: int = 0
    retr_size: int = 0
    retr_valid: bool = False
    retr_50_flagged: bool = False

    three_extreme: int = 0
    three_status: str = ""
    three_st: int = 0
    three_kt: int = 0

    mod_origin: int = 0
    mod_extreme: int = 0
    mod_size: int = 0
    mod_size_expansion: int = 0
    mod_bars: tuple = ()
    mod_status: str = ""

    a_origin: int = 0
    a_extreme: int = 0
    a_size: int = 0
    a_status: str = ""
    a_st: int = 0
    a_kt: int = 0

    a_last_ev: int = 0
    two_last_ev: int = 0

    b_extreme: int = 0
    b_measure: int = 0
    b_status: str = ""
    b_st: int = 0
    b_grande_kt: int = 0
    aut_kt: int = 0
    aut_price: int = 0

    c_origin: int = 0
    c_extreme: int = 0
    c_size: int = 0
    c_status: str = ""
    c_st: int = 0
    cut_kt: int = 0
    c_trend_kt: int = 0

    tt_target: int = 0
    tt_status: str = ""
    tt_extreme: int = 0
    tt_last_ev: int = 0
    tt_st: int = 0
    tt_kt: int = 0

    gap_secondary: dict = field(default_factory=dict)
    events: list = field(default_factory=list)

    def ev(self, t: Tick, event: str, detail: str = ""):
        self.events.append(
            {
                "seq": t.seq, "time_ms": t.time_ms, "bar": t.bar,
                "reading": self.rid, "generation": self.generation,
                "event": event, "detail": detail,
            }
        )


class Reader:
    def __init__(self, ticks: list[Tick]):
        self.ticks = ticks
        self.readings: list[Reading] = []
        self.active: Reading | None = None
        self.events: list[dict] = []
        self.prev_close = 0
        self.cur_bar = -1
        self.bar_last_price = 0
        self.bar_last_time = 0
        self.bar_bars: dict[int, dict] = {}
        self.rid_counter = 0
        self.trace: list[dict] = []
        self.bar_close_states: list[dict] = []

    # ------------------------------------------------------------------ utils
    def new_reading(self, t: Tick, direction: int, origin: int, extreme: int,
                    size: int, st: int, kt: int, reason: str) -> Reading:
        self.rid_counter += 1
        r = Reading(rid=f"R{self.rid_counter:03d}", direction=direction,
                    parent=self.active.rid if self.active else "",
                    origin_reason=reason)
        r.one_bar = t.bar
        r.one_open = origin
        r.one_origin = origin
        r.one_extreme = extreme
        r.one_size = size
        r.one_status = "CONFIRMED"
        r.one_st = st
        r.one_kt = kt
        r.phase = "WAIT_TWO"
        self.readings.append(r)
        self.active = r
        return r

    def start_one_candle(self, t: Tick):
        r = self.active
        if r is None or r.phase != "WAIT_ONE":
            self.rid_counter += 1
            r = Reading(rid=f"R{self.rid_counter:03d}", direction=0,
                        origin_reason="INITIAL")
            self.readings.append(r)
            self.active = r
        r.one_bar = t.bar
        r.one_open = t.price
        r.one_high = t.price
        r.one_low = t.price
        r.one_origin = 0
        r.one_extreme = 0
        r.one_size = 0
        r.one_status = "CANDIDATE"
        r.one_st = t.time_ms
        r.one_kt = 0
        r.direction = 0
        r.phase = "ONE_LIVE"
        r.ev(t, "ONE_CANDIDATE", f"open={t.price} gen={r.generation}")

    def close_active(self, t: Tick, why: str):
        if self.active:
            self.active.phase = "CLOSED"
            self.active.ev(t, "READING_CLOSED", why)

    def add_bar(self, bar: int, o: int, h: int, l: int, c: int):
        self.bar_bars[bar] = {"o": o, "h": h, "l": l, "c": c}

    # ------------------------------------------------------------------- main
    def run(self):
        for t in self.ticks:
            self.on_tick(t)
        self.finalize()
        return self

    def on_tick(self, t: Tick):
        new_bar = t.bar != self.cur_bar
        if self.cur_bar == -1:
            new_bar = True

        if new_bar:
            if self.cur_bar != -1:
                self.on_bar_close(self.cur_bar, self.bar_last_price, self.bar_last_time)
            self.cur_bar = t.bar
            self.add_bar(t.bar, t.price, t.price, t.price, t.price)
            self.on_bar_open(t)
        else:
            b = self.bar_bars[t.bar]
            b["h"] = max(b["h"], t.price)
            b["l"] = min(b["l"], t.price)
            b["c"] = t.price

        self.bar_last_price = t.price
        self.bar_last_time = t.time_ms

        r = self.active
        if r:
            if r.phase == "ONE_LIVE":
                r.one_high = max(r.one_high, t.price)
                r.one_low = min(r.one_low, t.price)
            elif r.phase == "TWO_LIVE":
                self.on_two_tick(r, t)
            elif r.phase == "WAIT_THREE":
                self.on_three_tick(r, t)
            elif r.phase == "WAIT_A":
                self.on_a_tick(r, t)
            elif r.phase == "A_LIVE":
                self.on_a_live_tick(r, t)
            elif r.phase == "B_LIVE":
                self.on_b_tick(r, t)
            elif r.phase == "C_LIVE":
                self.on_c_tick(r, t)

        for cr in self.readings:
            self.update_current_tt(cr, t)
            self.update_patterns(cr, t)

        self.snapshot(t)

    # --------------------------------------------------------------- bar open
    def on_bar_open(self, t: Tick):
        r = self.active
        if r and r.phase == "ONE_LIVE":
            self.confirm_one(r, t)
        r = self.active
        if r and r.phase == "WAIT_TWO":
            self.eval_two_open(r, t)
        elif r and r.phase == "WAIT_ONE":
            self.start_one_candle(t)
        elif r is None:
            self.start_one_candle(t)

    def confirm_one(self, r: Reading, t: Tick):
        # cierre de la vela de 1; la informacion ya existe al abrir la siguiente
        o, h, l, c = r.one_open, r.one_high, r.one_low, r.one_open
        bar = self.bar_bars.get(r.one_bar)
        if bar:
            o, h, l, c = bar["o"], bar["h"], bar["l"], bar["c"]
        d = 1 if c > o else (-1 if c < o else 0)
        if d == 0:
            d = 1 if c >= self.prev_close else -1
        r.direction = d
        r.one_origin = h if d < 0 else l
        r.one_extreme = l if d < 0 else h
        r.one_size = h - l
        r.one_status = "CONFIRMED"
        r.one_kt = self.bar_last_time
        r.phase = "WAIT_TWO"
        r.ev(t, "ONE_CONFIRMED",
             f"dir={d} origin={r.one_origin} extreme={r.one_extreme} size={r.one_size} "
             f"close_kt={r.one_kt}")

    # -------------------------------------------------------------------- two
    def eval_two_open(self, r: Reading, t: Tick):
        gap = t.price - self.prev_close
        r.two_origin = t.price
        r.two_extreme = t.price
        r.two_st = t.time_ms
        r.two_tail_max = t.price
        r.two_saw_direction = False
        r.ev(t, "TWO_OPEN", f"open={t.price} prev_close={self.prev_close} gap={gap}")
        if abs(gap) >= PLANO:
            r.two_status = "IMPOSSIBLE"
            r.two_kt = t.time_ms
            r.ev(t, "TWO_IMPOSSIBLE_NO_FLAT",
                 f"|gap|={abs(gap)} >= {PLANO}")
            if abs(gap) >= 100:
                r.ev(t, "GAP_SIGNIFICANT_UNDEFINED",
                     "Q_GAP: el arbol no fija umbral de gap significativo")
                r.gap_secondary = {
                    "open": t.price, "gap": gap, "direction": 1 if gap > 0 else -1,
                    "policy": "H7 esbozo: nuevo 1 en apertura, A/B/AUT implicitos",
                    "status": "SKETCH_ONLY",
                }
            self.module_from_discard(r, t, include_two=False)
            return
        r.phase = "TWO_LIVE"
        r.two_status = "CANDIDATE"
        r.ev(t, "TWO_CANDIDATE", f"flat |gap|={abs(gap)}")

    def on_two_tick(self, r: Reading, t: Tick):
        d = r.direction
        # cola inicial prohibitiva: recorrido contrario antes del primer tick direccional
        if not r.two_saw_direction:
            if (t.price - r.two_origin) * d > 0:
                r.two_saw_direction = True
            else:
                r.two_tail_max = (max(r.two_tail_max, t.price) if d < 0
                                  else min(r.two_tail_max, t.price))
        disp = (r.two_origin - t.price) if d < 0 else (t.price - r.two_origin)
        if d < 0 and t.price < r.two_extreme:
            r.two_extreme = t.price
        elif d > 0 and t.price > r.two_extreme:
            r.two_extreme = t.price
        if disp >= r.one_size:
            r.two_status = "CONFIRMED"
            r.two_size = disp
            r.two_kt = t.time_ms
            r.two_extreme = t.price
            r.phase = "WAIT_THREE"
            r.retr_active = False
            r.retr_valid = False
            r.ev(t, "TWO_CONFIRMED",
                 f"measure={disp} >= 100% de 1 ({r.one_size})")

    def on_bar_close(self, bar: int, price: int, time_ms: int):
        self.prev_close = price
        r = self.active
        if not r:
            return
        if r.phase == "ONE_LIVE":
            return  # se confirma al abrir la siguiente
        if r.phase == "TWO_LIVE":
            d = r.direction
            tail = ((r.two_tail_max - r.two_origin) if d < 0
                    else (r.two_origin - r.two_tail_max))
            if tail >= PLANO:
                r.two_status = "IMPOSSIBLE"
                r.two_kt = time_ms
                r.ev(Tick(-1, time_ms, bar, price), "TWO_IMPOSSIBLE_TAIL",
                     f"cola inicial={tail} >= {PLANO}")
            else:
                r.two_status = "IMPOSSIBLE"
                r.two_kt = time_ms
                r.ev(Tick(-1, time_ms, bar, price), "TWO_IMPOSSIBLE_CLOSE",
                     f"cierre sin 100% de 1: measure={self.two_measure(r)}")
            self.module_from_discard(r, Tick(-1, time_ms, bar, price), include_two=True)

    @staticmethod
    def two_measure(r: Reading) -> int:
        return (r.two_origin - r.two_extreme) if r.direction < 0 else (r.two_extreme - r.two_origin)

    # ----------------------------------------------------------------- module
    def module_from_discard(self, r: Reading, t: Tick, include_two: bool = True):
        r.mod_origin = r.one_origin
        if include_two:
            # el extremo del modulo es el mas lejano alcanzado por 1 o por 2
            if r.direction > 0:
                r.mod_extreme = max(r.one_extreme, r.two_extreme)
            else:
                r.mod_extreme = min(r.one_extreme, r.two_extreme)
            bars = (r.one_bar, t.bar)
        else:
            # no existe 2: el modulo es solo 1, con el extremo de su propia vela
            r.mod_extreme = r.one_extreme
            bars = (r.one_bar,)
        r.mod_size = abs(r.mod_extreme - r.mod_origin)
        r.mod_bars = bars
        hs = [self.bar_bars[b]["h"] for b in bars if b in self.bar_bars]
        ls = [self.bar_bars[b]["l"] for b in bars if b in self.bar_bars]
        r.mod_size_expansion = (max(hs) - min(ls)) if hs and ls else r.mod_size
        r.mod_status = "BY_DISCARD"
        r.phase = "WAIT_A"
        r.a_origin = r.mod_extreme
        r.a_status = "CANDIDATE"
        r.ev(t, "MODULE_BY_DISCARD",
             f"origin={r.mod_origin} extreme={r.mod_extreme} size={r.mod_size} "
             f"expansion={r.mod_size_expansion}")

    def complete_module(self, r: Reading, t: Tick):
        r.mod_origin = r.one_origin
        r.mod_extreme = r.three_extreme
        r.mod_size = abs(r.mod_extreme - r.mod_origin)
        r.mod_bars = (r.one_bar, r.two_st and r.two_st // 60000, t.bar)
        hs = [self.bar_bars[b]["h"] for b in r.mod_bars if b in self.bar_bars]
        ls = [self.bar_bars[b]["l"] for b in r.mod_bars if b in self.bar_bars]
        r.mod_size_expansion = (max(hs) - min(ls)) if hs and ls else r.mod_size
        r.mod_status = "REGULAR_1_2_3"
        r.phase = "WAIT_A"
        r.a_origin = r.mod_extreme
        r.a_status = "CANDIDATE"
        r.ev(t, "MODULE_COMPLETE",
             f"origin={r.mod_origin} extreme={r.mod_extreme} size={r.mod_size} "
             f"expansion={r.mod_size_expansion}")

    # ------------------------------------------------------------------ three
    def on_three_tick(self, r: Reading, t: Tick):
        d = r.direction
        beyond = (r.two_extreme - t.price) if d < 0 else (t.price - r.two_extreme)
        if beyond > 0:
            if r.retr_valid:
                # recuperacion en direccion de 2: 3 se confirma en este tick
                r.three_status = "CONFIRMED"
                r.three_extreme = t.price
                r.three_st = r.two_kt
                r.three_kt = t.time_ms
                r.ev(t, "THREE_CONFIRMED",
                     f"extremo={t.price} estricto sobre {r.two_extreme}")
                self.complete_module(r, t)
                return
            # 2 se extiende; el retroceso previo queda absorbido
            r.two_extreme = t.price
            r.two_size = (r.two_origin - r.two_extreme) if d < 0 else (r.two_extreme - r.two_origin)
            if r.two_size - r.two_last_ev >= NOISE:
                r.two_last_ev = r.two_size
                r.ev(t, "TWO_EXTENDED", f"nuevo extremo={t.price} size={r.two_size}")
            r.retr_active = False
            r.retr_valid = False
            r.retr_50_flagged = False
            return
        disp = (t.price - r.two_extreme) if d < 0 else (r.two_extreme - t.price)
        if disp > 0:
            if not r.retr_active:
                r.retr_active = True
                r.retr_extreme = t.price
                r.ev(t, "RETRACE_START", f"desde extremo de 2 {r.two_extreme}")
            if d < 0:
                if t.price > r.retr_extreme:
                    r.retr_extreme = t.price
            else:
                if t.price < r.retr_extreme:
                    r.retr_extreme = t.price
            r.retr_size = abs(r.retr_extreme - r.two_extreme)
            two_size = (r.two_origin - r.two_extreme) if d < 0 else (r.two_extreme - r.two_origin)
            if r.retr_size >= NOISE and not r.retr_valid:
                r.retr_valid = True
                r.ev(t, "RETRACE_VALID", f"retroceso={r.retr_size} size2={two_size}")
            if two_size and r.retr_size * 2 > two_size and not r.retr_50_flagged:
                r.retr_50_flagged = True
                r.ev(t, "THREE_BLOCKED_50",
                     f"retroceso={r.retr_size} > 50% de 2 ({two_size/2})")
                r.ev(t, "THREE_IMPOSSIBLE", "Q8: retroceso superior al 50 % de 2")
                self.module_from_12(r, t)
                return
            if two_size and r.retr_size * 2 == two_size and not r.retr_50_flagged:
                r.retr_50_flagged = True
                r.ev(t, "FIFTY_PERCENT_BOUNDARY",
                     "Q8: retroceso exactamente 50 % de 2; 3 queda pendiente")
        # recuperacion en direccion de 2 y superacion estricta del extremo
        if r.retr_valid:
            beyond2 = (r.two_extreme - t.price) if d < 0 else (t.price - r.two_extreme)
            if beyond2 > 0:
                r.three_status = "CONFIRMED"
                r.three_extreme = t.price
                r.three_st = r.two_kt
                r.three_kt = t.time_ms
                r.ev(t, "THREE_CONFIRMED", f"extremo={t.price} estricto sobre {r.two_extreme}")
                self.complete_module(r, t)
                return

    def module_from_12(self, r: Reading, t: Tick):
        r.three_status = "IMPOSSIBLE"
        r.mod_origin = r.mod_origin or r.one_origin
        r.mod_extreme = r.two_extreme
        r.mod_size = abs(r.mod_extreme - r.mod_origin)
        r.mod_bars = (r.one_bar, t.bar)
        hs = [self.bar_bars[b]["h"] for b in r.mod_bars if b in self.bar_bars]
        ls = [self.bar_bars[b]["l"] for b in r.mod_bars if b in self.bar_bars]
        r.mod_size_expansion = (max(hs) - min(ls)) if hs and ls else r.mod_size
        r.mod_status = "MODULE_1_2"
        r.phase = "WAIT_A"
        r.a_origin = r.mod_extreme
        r.a_status = "CANDIDATE"
        r.ev(t, "MODULE_FROM_1_2", f"origin={r.mod_origin} extreme={r.mod_extreme} size={r.mod_size}")

    # ---------------------------------------------------------------------- A
    def check_a_trend(self, r: Reading, t: Tick, d_a: int) -> bool:
        """A usada como tendencia: A supera la base del modulo."""
        if r.mod_size <= 0 or r.a_origin == 0:
            return False
        disp = (t.price - r.a_origin) * d_a
        if disp > r.mod_size:
            r.ev(t, "A_USED_AS_TREND",
                 f"A={disp} supera la base del modulo ({r.mod_size}) precio={t.price}")
            self.reset_generation(r, t, "A_USED_AS_TREND")
            return True
        return False

    def on_a_tick(self, r: Reading, t: Tick):
        d_mod = 1 if r.mod_extreme > r.mod_origin else -1
        d_a = -d_mod
        # el modulo se extiende si continua en su direccion
        if (t.price - r.mod_extreme) * d_mod > 0:
            r.mod_extreme = t.price
            r.mod_size = abs(r.mod_extreme - r.mod_origin)
            if r.mod_bars:
                b = r.mod_bars[-1]
                if b in self.bar_bars:
                    hs = [self.bar_bars[x]["h"] for x in r.mod_bars if x in self.bar_bars]
                    ls = [self.bar_bars[x]["l"] for x in r.mod_bars if x in self.bar_bars]
                    r.mod_size_expansion = max(hs) - min(ls)
            r.a_origin = r.mod_extreme
            r.a_status = "CANDIDATE"
            r.a_extreme = r.mod_extreme
            r.a_size = 0
            r.ev(t, "MODULE_EXTENDED", f"nuevo extremo={t.price} A se reinicia")
            return
        if self.check_a_trend(r, t, d_a):
            return
        disp = (t.price - r.mod_extreme) * d_a
        if r.a_status == "CANDIDATE":
            if disp > 0:
                r.a_extreme = t.price
                r.a_size = disp
                if disp - r.a_last_ev >= NOISE:
                    r.a_last_ev = disp
                    r.ev(t, "A_EXTENDED", f"extreme={t.price} size={disp}")
                if disp >= A_FLOOR:
                    r.a_status = "CONFIRMED"
                    r.a_kt = t.time_ms
                    r.a_st = r.mod_extreme == r.three_extreme and r.three_st or r.three_st
                    r.tt_target = r.a_extreme + r.mod_size * d_mod
                    r.tt_status = "POSSIBLE"
                    r.phase = "A_LIVE"
                    r.ev(t, "A_CONFIRMED",
                         f"origin={r.a_origin} extreme={r.a_extreme} size={r.a_size} "
                         f"tt_target={r.tt_target}")
            return
        if r.a_status == "CONFIRMED":
            if disp > r.a_size:
                r.a_size = disp
                r.a_extreme = t.price
                if r.tt_status == "POSSIBLE":
                    r.tt_target = r.a_extreme + r.mod_size * d_mod
                if disp - r.a_last_ev >= NOISE:
                    r.a_last_ev = disp
                    r.ev(t, "A_EXTENDED",
                         f"extreme={t.price} size={disp} tt_target={r.tt_target}")

    def absorb_module_extension(self, r: Reading, t: Tick, d_mod: int):
        r.mod_extreme = t.price
        r.mod_size = abs(r.mod_extreme - r.mod_origin)
        if r.mod_bars:
            hs = [self.bar_bars[x]["h"] for x in r.mod_bars if x in self.bar_bars]
            ls = [self.bar_bars[x]["l"] for x in r.mod_bars if x in self.bar_bars]
            if hs and ls:
                r.mod_size_expansion = max(hs) - min(ls)
        r.a_status = "CANDIDATE"
        r.a_origin = r.mod_extreme
        r.a_extreme = r.mod_extreme
        r.a_size = 0
        r.a_st = 0
        r.a_kt = 0
        r.b_status = ""
        r.b_extreme = 0
        r.b_measure = 0
        r.b_st = 0
        r.b_grande_kt = 0
        r.c_status = ""
        r.c_origin = 0
        r.c_extreme = 0
        r.c_size = 0
        r.cut_kt = 0
        if r.tt_status == "POSSIBLE":
            r.tt_status = ""
            r.tt_target = 0
        r.phase = "WAIT_A"
        r.ev(t, "MODULE_EXTENDED_ABSORBS_AB",
             f"nuevo extremo={t.price} modulo={r.mod_size} A/B absorbidos")

    def on_a_live_tick(self, r: Reading, t: Tick):
        d_a = 1 if r.a_extreme > r.a_origin else -1
        d_b = -d_a
        d_mod = -d_a
        # un nuevo extremo del modulo absorbe A/B mientras no esten cerrados
        if (t.price - r.mod_extreme) * d_mod > 0:
            self.absorb_module_extension(r, t, d_mod)
            return
        if self.check_a_trend(r, t, d_a):
            return
        # B empieza cuando el precio gira contra A
        if (t.price - r.a_extreme) * d_b > 0:
            if r.b_status == "":
                r.b_status = "CANDIDATE"
                r.b_extreme = t.price
                r.b_st = t.time_ms
                r.phase = "B_LIVE"
                r.ev(t, "B_CANDIDATE", f"desde A extreme={r.a_extreme}")
            self.on_b_tick(r, t)
            return
        # A se extiende mas alla de su extremo
        if (t.price - r.a_extreme) * d_a > 0:
            r.a_extreme = t.price
            r.a_size = abs(r.a_extreme - r.a_origin)
            if r.tt_status == "POSSIBLE":
                r.tt_target = r.a_extreme - r.mod_size * d_a
            if r.a_size - r.a_last_ev >= NOISE:
                r.a_last_ev = r.a_size
                r.ev(t, "A_EXTENDED",
                     f"extreme={t.price} size={r.a_size} tt_target={r.tt_target}")

    # ---------------------------------------------------------------------- B
    def on_b_tick(self, r: Reading, t: Tick):
        d_a = 1 if r.a_extreme > r.a_origin else -1
        d_b = -d_a
        # B se mide desde el extremo de A hasta su extremo direccional
        if (t.price - r.b_extreme) * d_b > 0:
            r.b_extreme = t.price
        r.b_measure = abs(r.a_extreme - r.b_extreme)
        # A puede extenderse si el precio vuelve mas alla del extremo de A
        if (t.price - r.a_extreme) * d_a > 0:
            r.a_extreme = t.price
            r.a_size = abs(r.a_extreme - r.a_origin)
            if self.check_a_trend(r, t, d_a):
                return
            if r.tt_status == "POSSIBLE":
                r.tt_target = r.a_extreme - r.mod_size * d_a
            if r.a_size - r.a_last_ev >= NOISE:
                r.a_last_ev = r.a_size
                r.ev(t, "A_EXTENDED",
                     f"extreme={t.price} size={r.a_size} (B reiniciada)")
            r.b_extreme = t.price
            r.b_measure = 0
            r.b_status = "CANDIDATE"
            r.b_grande_kt = 0
            return
        if r.b_status in ("CANDIDATE", "GRANDE"):
            if r.b_measure >= r.a_size and not r.b_grande_kt:
                r.b_grande_kt = t.time_ms
                r.b_status = "GRANDE"
                r.ev(t, "B_GRANDE", f"measure={r.b_measure} >= 100% de A ({r.a_size})")
            # AUT estricto
            if r.b_measure > 0 and (r.b_measure * 100 > r.a_size * AUT_MULT + AUT_ADD * 100):
                self.confirm_aut(r, t)
                return
        # C candidata tras B Grande
        if r.b_grande_kt and r.c_status == "":
            # giro contra B (direccion de A); exige superar el filtro de ruido
            if (t.price - r.b_extreme) * d_a >= NOISE:
                r.c_status = "CANDIDATE"
                r.c_origin = r.b_extreme
                r.c_extreme = t.price
                r.c_size = abs(t.price - r.c_origin)
                r.c_st = r.b_extreme_time() if hasattr(r, "b_extreme_time") else r.b_grande_kt
                r.phase = "C_LIVE"
                r.ev(t, "C_CANDIDATE", f"desde B extreme={r.b_extreme}")
                return
        if r.c_status:
            self.on_c_tick(r, t)

    def archive_generation(self, r: Reading, reason: str):
        gen = {
            "generation": r.generation, "reason": reason,
            "one": (r.one_origin, r.one_extreme, r.one_size, r.one_st, r.one_kt),
            "two": (r.two_origin, r.two_extreme, r.two_st, r.two_kt),
            "three": (r.three_extreme, r.three_st, r.three_kt),
            "module": (r.mod_origin, r.mod_extreme, r.mod_size, r.mod_status),
            "a": (r.a_origin, r.a_extreme, r.a_size, r.a_st, r.a_kt),
            "b": (r.b_extreme, r.b_measure, r.b_status, r.b_grande_kt, r.aut_kt),
            "c": (r.c_origin, r.c_extreme, r.c_status, r.cut_kt, r.c_trend_kt),
            "tt": (r.tt_target, r.tt_status, r.tt_kt),
        }
        r.history.append(gen)
        if r.tt_status:
            d_mod = 1 if r.mod_extreme > r.mod_origin else -1
            r.patterns.append({
                "generation": r.generation, "target": r.tt_target,
                "status": r.tt_status, "extreme": r.tt_extreme,
                "a_extreme": r.a_extreme, "base": r.mod_origin, "dir": d_mod,
                "st": r.tt_st, "kt": r.tt_kt, "reason": reason,
                "last_ev": r.tt_extreme,
            })

    def reset_generation(self, r: Reading, t: Tick, reason: str):
        self.archive_generation(r, reason)
        r.generation += 1
        r.origin_reason = reason
        r.one_bar = 0; r.one_open = 0; r.one_high = 0; r.one_low = 0
        r.one_origin = 0; r.one_extreme = 0; r.one_size = 0
        r.one_status = ""; r.one_st = 0; r.one_kt = 0
        r.two_origin = 0; r.two_extreme = 0; r.two_size = 0
        r.two_status = ""; r.two_st = 0; r.two_kt = 0
        r.two_tail_max = 0; r.two_saw_direction = False
        r.retr_active = False; r.retr_extreme = 0; r.retr_size = 0
        r.retr_valid = False; r.retr_50_flagged = False
        r.three_extreme = 0; r.three_status = ""; r.three_st = 0; r.three_kt = 0
        r.mod_origin = 0; r.mod_extreme = 0; r.mod_size = 0
        r.mod_size_expansion = 0; r.mod_bars = (); r.mod_status = ""
        r.a_origin = 0; r.a_extreme = 0; r.a_size = 0
        r.a_status = ""; r.a_st = 0; r.a_kt = 0; r.a_last_ev = 0
        r.two_last_ev = 0
        r.b_extreme = 0; r.b_measure = 0; r.b_status = ""; r.b_st = 0
        r.b_grande_kt = 0; r.aut_kt = 0; r.aut_price = 0
        r.c_origin = 0; r.c_extreme = 0; r.c_size = 0; r.c_status = ""
        r.c_st = 0; r.cut_kt = 0; r.c_trend_kt = 0
        r.tt_target = 0; r.tt_status = ""; r.tt_extreme = 0; r.tt_last_ev = 0
        r.tt_st = 0; r.tt_kt = 0
        r.phase = "WAIT_ONE"
        r.ev(t, "NEW_ONE_PENDING",
             f"reason={reason} gen={r.generation} siguiente vela = 1")

    def confirm_aut(self, r: Reading, t: Tick):
        r.aut_kt = t.time_ms
        r.aut_price = t.price
        r.b_status = "AUT"
        r.ev(t, "AUT",
             f"measure={r.b_measure} > 127%+0,25 de A ({r.a_size}) precio={t.price}")
        self.reset_generation(r, t, "AUT")

    # ---------------------------------------------------------------------- C
    def on_c_tick(self, r: Reading, t: Tick):
        d_c = 1 if r.a_extreme > r.a_origin else -1
        # si el precio rompe el origen de C, C se absorbe y B continua
        if (t.price - r.c_origin) * (-d_c) > 0:
            r.ev(t, "C_ABSORBED", f"precio={t.price} rompe origen de C={r.c_origin}")
            r.c_status = ""
            r.c_origin = 0
            r.c_extreme = 0
            r.c_size = 0
            r.phase = "B_LIVE"
            self.on_b_tick(r, t)
            return
        if (t.price - r.c_extreme) * d_c > 0:
            r.c_extreme = t.price
            r.c_size = abs(r.c_extreme - r.c_origin)
        # CUT: C supera estrictamente el final de A
        if not r.cut_kt:
            beyond_a = (t.price - r.a_extreme) * d_c
            if beyond_a > 0:
                r.cut_kt = t.time_ms
                r.ev(t, "CUT", f"C={t.price} supera final de A={r.a_extreme}")
        # C usada como tendencia: supera la base del modulo
        if not r.c_trend_kt:
            base = r.mod_origin
            beyond_base = (t.price - base) * d_c
            if beyond_base > 0:
                r.c_trend_kt = t.time_ms
                r.ev(t, "C_USED_AS_TREND",
                     f"C={t.price} supera base del modulo={base} (Q_BASE: origen)")
                self.reset_generation(r, t, "C_USED_AS_TREND")

    # --------------------------------------------------------------------- TT
    def update_current_tt(self, r: Reading, t: Tick):
        if not r.tt_status:
            return
        d_mod = 1 if r.mod_extreme > r.mod_origin else -1
        if r.tt_status == "POSSIBLE":
            if (t.price - r.tt_target) * d_mod >= 0:
                r.tt_status = "CONFIRMED"
                r.tt_st = r.a_st
                r.tt_kt = t.time_ms
                r.tt_extreme = t.price
                r.ev(t, "TT_CONFIRMED",
                     f"gen={r.generation} target={r.tt_target} precio={t.price}")
            elif t.time_ms > r.a_kt and (t.price - r.mod_origin) * d_mod <= 0:
                r.tt_status = "FAILED"
                r.ev(t, "TT_FAILED",
                     f"gen={r.generation} precio={t.price} retorna la base={r.mod_origin}")
        elif r.tt_status in ("CONFIRMED", "EXTENDED"):
            if (t.price - r.tt_extreme) * d_mod > 0:
                r.tt_extreme = t.price
                r.tt_status = "EXTENDED"
                if abs(r.tt_extreme - r.tt_last_ev) >= NOISE:
                    r.tt_last_ev = r.tt_extreme
                    r.ev(t, "TT_EXTENDED", f"gen={r.generation} extreme={t.price}")

    def update_patterns(self, r: Reading, t: Tick):
        for p in r.patterns:
            if p["status"] == "POSSIBLE":
                if (t.price - p["target"]) * p["dir"] >= 0:
                    p["status"] = "CONFIRMED"
                    p["kt"] = t.time_ms
                    p["extreme"] = t.price
                    r.ev(t, "TT_CONFIRMED",
                         f"gen={p['generation']} target={p['target']} precio={t.price}")
                elif (t.price - p["base"]) * p["dir"] <= 0:
                    p["status"] = "FAILED"
                    r.ev(t, "TT_FAILED",
                         f"gen={p['generation']} precio={t.price} retorna la base={p['base']}")
            elif p["status"] in ("CONFIRMED", "EXTENDED"):
                if (t.price - p["extreme"]) * p["dir"] > 0:
                    p["extreme"] = t.price
                    p["status"] = "EXTENDED"
                    if abs(p["extreme"] - p.get("last_ev", p["extreme"])) >= NOISE:
                        p["last_ev"] = p["extreme"]
                        r.ev(t, "TT_EXTENDED",
                             f"gen={p['generation']} extreme={t.price}")

    # ---------------------------------------------------------------- snapshot
    def snapshot(self, t: Tick):
        r = self.active
        row = {
            "sequence_id": t.seq, "time_ms": t.time_ms, "bar": t.bar, "price": t.price,
            "reading": r.rid if r else "", "generation": r.generation if r else 0,
            "phase": r.phase if r else "",
            "active_function": FUNC_BY_PHASE.get(r.phase, "-") if r else "-",
            "expected": EXPECTED_BY_PHASE.get(r.phase, "-") if r else "-",
            "question": QUESTION_BY_PHASE.get(r.phase, "-") if r else "-",
            "candidate": self.candidate(r),
            "status": self.status(r),
            "origin": self.origin(r),
            "extreme": self.extreme(r),
            "one": self.one_fields(r), "two": self.two_fields(r),
            "module": self.mod_fields(r), "a": self.a_fields(r),
            "b": self.b_fields(r), "c": self.c_fields(r), "tt": self.tt_fields(r),
            "structural_time": self.st_time(r), "knowledge_time": self.kt_time(r),
            "secondary": [self.secondary_row(x) for x in self.readings
                          if x is not r and x.phase == "CLOSED"],
            "events": [e for e in (r.events if r else []) if e["seq"] == t.seq],
        }
        self.trace.append(row)

    @staticmethod
    def candidate(r):
        if not r:
            return ""
        return {"ONE_LIVE": "1", "WAIT_ONE": "1", "WAIT_TWO": "2", "TWO_LIVE": "2",
                "WAIT_THREE": "3", "WAIT_A": "A", "A_LIVE": "B",
                "B_LIVE": "B", "C_LIVE": "C"}.get(r.phase, "")

    @staticmethod
    def status(r):
        if not r:
            return ""
        return {"ONE_LIVE": r.one_status, "WAIT_ONE": "PENDING", "WAIT_TWO": r.one_status,
                "TWO_LIVE": r.two_status, "WAIT_THREE": r.two_status,
                "WAIT_A": r.a_status, "A_LIVE": r.a_status,
                "B_LIVE": r.b_status, "C_LIVE": r.c_status}.get(r.phase, "")

    @staticmethod
    def origin(r):
        if not r:
            return 0
        return {"ONE_LIVE": r.one_origin, "WAIT_ONE": 0, "WAIT_TWO": r.one_origin,
                "TWO_LIVE": r.two_origin, "WAIT_THREE": r.two_origin,
                "WAIT_A": r.a_origin, "A_LIVE": r.a_origin,
                "B_LIVE": r.a_extreme, "C_LIVE": r.c_origin}.get(r.phase, 0)

    @staticmethod
    def extreme(r):
        if not r:
            return 0
        return {"ONE_LIVE": max(r.one_high, r.one_low), "WAIT_ONE": 0, "WAIT_TWO": r.one_extreme,
                "TWO_LIVE": r.two_extreme, "WAIT_THREE": r.two_extreme,
                "WAIT_A": r.a_extreme, "A_LIVE": r.a_extreme,
                "B_LIVE": r.b_extreme, "C_LIVE": r.c_extreme}.get(r.phase, 0)

    @staticmethod
    def one_fields(r):
        if not r:
            return {}
        return {"origin": r.one_origin, "extreme": r.one_extreme,
                "size": r.one_size, "status": r.one_status,
                "st": r.one_st, "kt": r.one_kt, "bar": r.one_bar}

    @staticmethod
    def two_fields(r):
        if not r:
            return {}
        return {"origin": r.two_origin, "extreme": r.two_extreme,
                "size": (r.two_origin - r.two_extreme) if r.direction < 0 else (r.two_extreme - r.two_origin),
                "status": r.two_status, "st": r.two_st, "kt": r.two_kt,
                "retr": r.retr_size, "retr_valid": r.retr_valid}

    @staticmethod
    def mod_fields(r):
        if not r:
            return {}
        return {"origin": r.mod_origin, "extreme": r.mod_extreme,
                "size": r.mod_size, "expansion": r.mod_size_expansion,
                "status": r.mod_status}

    @staticmethod
    def a_fields(r):
        if not r:
            return {}
        return {"origin": r.a_origin, "extreme": r.a_extreme,
                "size": r.a_size, "status": r.a_status,
                "st": r.a_st, "kt": r.a_kt}

    @staticmethod
    def b_fields(r):
        if not r:
            return {}
        return {"extreme": r.b_extreme, "measure": r.b_measure,
                "status": r.b_status, "b_grande_kt": r.b_grande_kt,
                "aut_kt": r.aut_kt}

    @staticmethod
    def c_fields(r):
        if not r:
            return {}
        return {"origin": r.c_origin, "extreme": r.c_extreme,
                "size": r.c_size, "status": r.c_status,
                "cut_kt": r.cut_kt, "c_trend_kt": r.c_trend_kt}

    @staticmethod
    def tt_fields(r):
        if not r:
            return {}
        if r.tt_status:
            return {"target": r.tt_target, "status": r.tt_status,
                    "extreme": r.tt_extreme, "st": r.tt_st, "kt": r.tt_kt,
                    "generation": r.generation}
        if r.patterns:
            p = r.patterns[-1]
            return {"target": p["target"], "status": p["status"],
                    "extreme": p["extreme"], "st": p["st"], "kt": p["kt"],
                    "generation": p["generation"]}
        return {}

    @staticmethod
    def st_time(r):
        if not r:
            return 0
        return r.a_st or r.three_st or r.two_st or r.one_st

    @staticmethod
    def kt_time(r):
        if not r:
            return 0
        return r.aut_kt or r.cut_kt or r.three_kt or r.two_kt or r.one_kt

    @staticmethod
    def secondary_row(x: Reading):
        return {"reading": x.rid, "reason": x.origin_reason,
                "generation": x.generation,
                "patterns": [{"gen": p["generation"], "status": p["status"],
                              "target": p["target"]} for p in x.patterns],
                "a_size": x.a_size, "b_status": x.b_status,
                "module": x.mod_size}

    def finalize(self):
        r = self.active
        if r and r.phase == "ONE_LIVE":
            r.ev(Tick(-1, self.bar_last_time, self.cur_bar, self.bar_last_price),
                 "FEED_END_ONE_CANDIDATE", "1 no confirmada antes del final")
        # estado al cierre de vela
        for bar, b in sorted(self.bar_bars.items()):
            row = None
            for s in reversed(self.trace):
                if s["bar"] == bar:
                    row = s
                    break
            if row:
                self.bar_close_states.append(row)


def load_ticks(path: Path) -> list[Tick]:
    out = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            out.append(Tick(int(row["sequence_id"]), int(row["time_msc"]),
                            int(row["time_msc"]) // 60000, price_i(row["bid"])))
    return out


def hhmm(t_ms: int) -> str:
    d = datetime.datetime.fromtimestamp(t_ms / 1000, datetime.timezone.utc)
    return d.strftime("%H:%M:%S.%f")[:-3]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="t_from", default="16:15")
    ap.add_argument("--to", dest="t_to", default="17:29")
    ap.add_argument("--trace")
    ap.add_argument("--events")
    ap.add_argument("--bar-close")
    ap.add_argument("--generations")
    ap.add_argument("--prefix-bar")
    ap.add_argument("--hash-only", action="store_true")
    ap.add_argument("--a-floor", type=int, default=600)
    args = ap.parse_args(argv)
    global A_FLOOR
    A_FLOOR = args.a_floor

    ticks = load_ticks(FEED)
    def bar_of(h):
        hh, mm = h.split(":")
        return int(hh) * 60 + int(mm)
    b0, b1 = bar_of(args.t_from), bar_of(args.t_to)
    ticks = [t for t in ticks if b0 <= t.bar % 1440 <= b1]
    if args.prefix_bar:
        pb = bar_of(args.prefix_bar)
        ticks = [t for t in ticks if t.bar % 1440 <= pb]

    rd = Reader(ticks).run()

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
            w.writerow(["sequence_id", "time", "bar", "reading", "generation",
                        "event", "detail"])
            for r in rd.readings:
                for e in r.events:
                    w.writerow([e["seq"], hhmm(e["time_ms"]),
                                datetime.datetime.fromtimestamp(e["bar"] * 60, datetime.timezone.utc).strftime("%H:%M"),
                                e["reading"], e["generation"], e["event"], e["detail"]])
    if args.generations:
        with open(args.generations, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["generation", "ended_by", "one_origin", "one_extreme", "one_size",
                        "one_kt", "two_origin", "two_extreme", "two_kt",
                        "three_extreme", "three_kt", "module_origin", "module_extreme",
                        "module_size", "module_status", "a_origin", "a_extreme", "a_size",
                        "a_kt", "b_extreme", "b_measure", "b_status", "b_grande_kt",
                        "aut_kt", "c_origin", "c_extreme", "c_status", "cut_kt",
                        "c_trend_kt", "tt_target", "tt_status", "tt_kt"])
            r = rd.active
            entries = list(r.history) if r else []
            if r and r.one_size:
                entries.append({
                    "generation": r.generation, "reason": "OPEN_AT_FEED_END",
                    "one": (r.one_origin, r.one_extreme, r.one_size, r.one_st, r.one_kt),
                    "two": (r.two_origin, r.two_extreme, r.two_st, r.two_kt),
                    "three": (r.three_extreme, r.three_st, r.three_kt),
                    "module": (r.mod_origin, r.mod_extreme, r.mod_size, r.mod_status),
                    "a": (r.a_origin, r.a_extreme, r.a_size, r.a_st, r.a_kt),
                    "b": (r.b_extreme, r.b_measure, r.b_status, r.b_grande_kt, r.aut_kt),
                    "c": (r.c_origin, r.c_extreme, r.c_status, r.cut_kt, r.c_trend_kt),
                    "tt": (r.tt_target, r.tt_status, r.tt_kt),
                })
            for g in entries:
                one, two, three, mod, a, b, c, tt = (g["one"], g["two"], g["three"],
                                                     g["module"], g["a"], g["b"],
                                                     g["c"], g["tt"])
                w.writerow([g["generation"], g["reason"], one[0], one[1], one[2],
                            hhmm(one[4]) if one[4] else "", two[0], two[1],
                            hhmm(two[3]) if two[3] else "", three[0],
                            hhmm(three[2]) if three[2] else "",
                            mod[0], mod[1], mod[2], mod[3],
                            a[0], a[1], a[2], hhmm(a[4]) if a[4] else "",
                            b[0], b[1], b[2], hhmm(b[3]) if b[3] else "",
                            hhmm(b[4]) if b[4] else "", c[0], c[1], c[2],
                            hhmm(c[3]) if c[3] else "", hhmm(c[4]) if c[4] else "",
                            tt[0], tt[1], hhmm(tt[2]) if tt[2] else ""])
    if args.bar_close:
        with open(args.bar_close, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["bar", "time", "reading", "phase", "function", "candidate",
                        "status", "origin", "extreme", "module_origin", "module_extreme",
                        "module_size", "a_size", "b_measure", "tt_status", "tt_target",
                        "events"])
            seen = set()
            for row in reversed(rd.bar_close_states):
                if row["bar"] in seen:
                    continue
                seen.add(row["bar"])
                m = row["module"] or {}
                w.writerow([
                    datetime.datetime.fromtimestamp(row["bar"] * 60, datetime.timezone.utc).strftime("%H:%M"),
                    hhmm(row["time_ms"]), row["reading"], row["phase"],
                    row["active_function"], row["candidate"], row["status"],
                    row["origin"], row["extreme"],
                    m.get("origin", ""), m.get("extreme", ""), m.get("size", ""),
                    (row["a"] or {}).get("size", ""),
                    (row["b"] or {}).get("measure", ""),
                    (row["tt"] or {}).get("status", ""),
                    (row["tt"] or {}).get("target", ""),
                    "",
                ])
    if not args.trace and not args.events:
        for r in rd.readings:
            print(f"--- {r.rid} dir={r.direction} reason={r.origin_reason} phase={r.phase}")
            for e in r.events:
                print(f"  {hhmm(e['time_ms'])} {e['event']:28s} {e['detail']}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
