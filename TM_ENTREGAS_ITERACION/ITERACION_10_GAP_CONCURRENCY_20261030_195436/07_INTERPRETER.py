"""TM REFERENCE INTERPRETER V1 — AUT directo por A (iteración 08).

Core baseline (approved, unchanged semantics):
  * reading ownership
  * function 1
  * opening evaluation
  * 2 candidate / confirmed / impossible
  * module by discard (1+2)
  * 3 pending / confirmed / impossible
  * module 1+2+3
  * 3 live extreme

A/B candidate and B Grande/AUT by B (unchanged from iteration 07):
  * CONTRARY_MOVE_PENDING / RETURN_MOVE_PENDING / A_CONFIRMED / B_CANDIDATE
  * B_GRANDE (100% .. 127%+0,25 inclusive) / AUT_CONFIRMED / NEW_ONE_ACTIVE

Added in this version (iteration 08):
  * P-AB-04_RETURN_JUMP_4 retirada: el salto fijo de 4,0 puntos ya no es
    autoridad. El retorno se confirma por extension de su PROPIO extremo.
  * AUT_DIRECT_BY_A: si A supera ESTRICTAMENTE la base del modulo, el nuevo 1
    es el propio movimiento A. No existe B y no se aplica 127%+0,25.
  * archivado de A (CONFIRMED_ARCHIVED), 3 y modulo (FROZEN_REFERENCE).

NOT implemented:
  C, CUT, TT, FT, gap new-1, concurrency.
Those are blocked by scope, not assumed.

The interpreter is deterministic and has no future information: every
transition is evaluated from the current tick and the state built so far.
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FEED = ROOT / "TM_CANON_ACTIVO" / "02_TICKS" / "TM_TICKFEED_1615_1730.csv"

PLANO = 25       # 0.25 in cents
NOISE = 200      # 2.00 points: physical noise filter
CORE_VERSION = "TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT"
RETURN_MIN = NOISE  # filtro fisico de ruido; nunca autonomia por si solo
# P-AB-04_RETURN_JUMP_4 = REJECTED_EXPERIMENTAL_ASSUMPTION
# El salto fijo de 4,0 puntos en un tick no es regla TM canonica y no se
# sustituye por otro numero fijo. La autonomia del retorno se decide de forma
# causal: extension de su propio extremo con direccion contraria a A, o
# absorcion por extension de A.


@dataclass
class Tick:
    seq: int
    time_ms: int
    bar: int
    price: int


@dataclass
class Reading:
    reading_id: str
    gid: int = 1
    parent: int = 0
    phase: str = "INITIAL_BAR"

    one_dir: int = 0
    one_origin: int = 0
    one_extreme: int = 0
    one_extreme_st: int = 0
    one_size: int = 0
    one_st: int = 0
    one_kt: int = 0
    one_bar: int = -1
    one_status: str = ""

    two_origin: int = 0
    two_extreme: int = 0
    two_extreme_st: int = 0
    two_dir: int = 0
    two_size: int = 0
    two_st: int = 0
    two_bar: int = -1
    two_kt: int = 0
    two_status: str = ""
    two_tail: int = 0
    two_seen_dir: bool = False

    three_extreme: int = 0
    three_extreme_st: int = 0
    three_st: int = 0
    three_kt: int = 0
    three_bar: int = -1
    three_status: str = ""
    retr_active: bool = False
    retr_extreme: int = 0
    retr_base_size: int = 0
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
    mod_dir: int = 0

    a_status: str = ""
    a_dir: int = 0
    a_origin: int = 0
    a_origin_st: int = 0
    a_extreme: int = 0
    a_extreme_st: int = 0
    a_structural_end_st: int = 0
    a_kt: int = 0
    a_size: int = 0
    a_confirmations: int = 0
    aut_direct_status: str = ""
    aut_direct_kt: int = 0
    aut_direct_price: int = 0
    b_authority: str = ""

    # C Grande — funcion formal (iteracion 09)
    c_status: str = ""
    c_dir: int = 0
    c_origin: int = 0
    c_origin_st: int = 0
    c_extreme: int = 0
    c_extreme_st: int = 0
    c_kt: int = 0
    c_size: int = 0
    c_authority: str = ""
    trend_status: str = ""
    trend_kt: int = 0
    transition_reason: str = ""
    gap_branch: bool = False
    gap_kind: str = ""

    return_status: str = ""
    return_dir: int = 0
    return_origin: int = 0
    return_first_st: int = 0
    return_extreme: int = 0
    return_extreme_st: int = 0
    return_size: int = 0
    return_first_extreme: int = 0
    return_extended: bool = False
    return_jump: bool = False
    return_ticks: int = 0
    return_absorbed: int = 0

    b_status: str = ""
    b_dir: int = 0
    b_origin: int = 0
    b_origin_st: int = 0
    b_extreme: int = 0
    b_extreme_st: int = 0
    b_size: int = 0
    b_st: int = 0
    b_kt: int = 0
    b_grande_kt: int = 0
    b_grande_status: str = ""
    b_flags: str = ""

    aut_kt: int = 0
    aut_price: int = 0
    aut_status: str = ""

    new_one_status: str = ""
    n_origin: int = 0
    n_origin_st: int = 0
    n_dir: int = 0
    n_st: int = 0
    n_kt: int = 0
    n_extreme: int = 0
    n_extreme_st: int = 0
    n_size: int = 0

    active_function: str = ""
    three_authority: str = ""
    module_authority: str = ""
    a_authority: str = ""
    events: list = field(default_factory=list)

    def ev(self, t: Tick, event: str, detail: str = "") -> None:
        self.events.append({
            "seq": t.seq, "time_ms": t.time_ms, "bar": t.bar,
            "gid": self.gid, "event": event, "detail": detail,
        })


class Reader:
    def __init__(self, ticks: list[Tick], reading_id: str = "L1"):
        self.ticks = ticks
        self.reading_id = reading_id
        self.reading = Reading(reading_id=reading_id)
        self.prev_close = 0
        self.cur_bar = -1
        self.last_price = 0
        self.last_time = 0
        self.bars: dict[int, dict] = {}
        self.trace: list[dict] = []
        self.events: list[dict] = []
        self._finished = False

    # ------------------------------------------------------------- bar helpers
    def _confirm_initial_one(self, t: Tick) -> None:
        r = self.reading
        b = self.bars[r.one_bar]
        d = 1 if b["c"] > b["o"] else (-1 if b["c"] < b["o"] else 0)
        if d == 0:
            d = 1 if b["c"] >= b["o"] else -1
        r.one_dir = d
        r.one_origin = b["h"] if d < 0 else b["l"]
        r.one_extreme = b["l"] if d < 0 else b["h"]
        r.one_size = abs(r.one_extreme - r.one_origin)
        r.one_extreme_st = t.time_ms
        r.one_status = "CONFIRMED"
        r.one_kt = t.time_ms
        r.phase = "WAIT_OPENING"
        r.ev(t, "ONE_CONFIRMED_INITIAL",
             f"dir={d} origin={r.one_origin} extreme={r.one_extreme} size={r.one_size}")

    def _freeze_one(self, t: Tick) -> None:
        r = self.reading
        if r.phase != "ONE_LIVE":
            return
        if r.one_size <= 0:
            r.one_bar = t.bar
            r.ev(t, "ONE_ZERO_SIZE_DEFERRAL", "1 sin medida; se difiere la pregunta por 2")
            return
        r.one_kt = self.last_time
        r.phase = "WAIT_OPENING"
        r.ev(t, "ONE_FROZEN",
             f"origin={r.one_origin} extreme={r.one_extreme} size={r.one_size}")

    # --------------------------------------------------------------- opening/2
    def _eval_opening(self, t: Tick) -> None:
        r = self.reading
        gap = t.price - self.prev_close
        r.two_origin = t.price
        r.two_extreme = t.price
        r.two_extreme_st = t.time_ms
        r.two_dir = r.one_dir
        r.two_st = t.time_ms
        r.two_bar = t.bar
        r.two_tail = 0
        r.two_seen_dir = False

        if abs(gap) >= PLANO:
            r.two_status = "IMPOSSIBLE_NO_FLAT"
            r.two_kt = t.time_ms
            r.gap_branch = True
            r.gap_kind = "NON_FLAT_OPEN"
            r.ev(t, "NON_FLAT_OPEN_OBSERVED",
                 f"|Open - Close_previo|={abs(gap)} >= {PLANO}")
            r.ev(t, "NO_TWO_BY_NON_FLAT_OPEN",
                 f"la lectura esperaba 2; gap {abs(gap)} lo prohibe")
            r.ev(t, "TWO_IMPOSSIBLE_NO_FLAT",
                 f"|gap|={abs(gap)} >= {PLANO}; 2 prohibido")
            self._module_by_discard(t, include_two=False)
            return

        r.two_status = "CANDIDATE"
        r.phase = "TWO_LIVE"
        r.ev(t, "TWO_CANDIDATE",
             f"flat |gap|={abs(gap)} origin={t.price} dir={r.two_dir}")

    def _on_two_tick(self, t: Tick) -> None:
        r = self.reading
        d = r.two_dir
        if not r.two_seen_dir:
            if (t.price - r.two_origin) * d > 0:
                r.two_seen_dir = True
            else:
                r.two_tail = max(r.two_tail, (r.two_origin - t.price) * d)
        if (t.price - r.two_extreme) * d > 0:
            r.two_extreme = t.price
            r.two_extreme_st = t.time_ms
        r.two_size = abs(r.two_extreme - r.two_origin)

        if r.two_tail > PLANO:
            r.two_status = "IMPOSSIBLE_TAIL"
            r.two_kt = t.time_ms
            r.ev(t, "TWO_IMPOSSIBLE_TAIL", f"cola inicial={r.two_tail}")
            self._module_by_discard(t, include_two=False)
            return

        if r.two_size >= r.one_size:
            r.two_status = "CONFIRMED"
            r.two_kt = t.time_ms
            r.phase = "WAIT_THREE"
            r.retr_active = False
            r.retr_valid = False
            r.retr_50 = False
            r.ev(t, "TWO_CONFIRMED",
                 f"measure={r.two_size} >= 100% de 1 ({r.one_size})")

    # ------------------------------------------------------------------- three
    def _on_three_tick(self, t: Tick) -> None:
        r = self.reading
        d = r.two_dir

        # La candidatura de 2 pertenece a su vela: las vibraciones internas de
        # esa vela no fragmentan 2 ni abren 3. La pregunta por 3 comienza en la
        # vela siguiente, donde el retroceso ya es funcional.
        if t.bar <= r.two_bar:
            if (t.price - r.two_extreme) * d > 0:
                r.two_extreme = t.price
                r.two_extreme_st = t.time_ms
                r.two_size = abs(r.two_extreme - r.two_origin)
                r.ev(t, "TWO_EXTENDED",
                     f"extremo final de 2={t.price} size={r.two_size} (misma vela)")
            return

        # 2 confirmada sigue viva: mientras el precio haga nuevos extremos en
        # su direccion, 2 conserva la finalidad y actualiza su extremo final.
        if not r.retr_active:
            if (t.price - r.two_extreme) * d > 0:
                r.two_extreme = t.price
                r.two_extreme_st = t.time_ms
                r.two_size = abs(r.two_extreme - r.two_origin)
                r.ev(t, "TWO_EXTENDED",
                     f"extremo final de 2={t.price} size={r.two_size}")
                return
            r.retr_active = True
            r.retr_base_size = r.two_size
            r.retr_extreme = t.price
            r.retr_size = abs(t.price - r.two_extreme)
            r.retr_valid = False
            r.retr_50 = False
            r.ev(t, "RETRACE_START",
                 f"desde extremo final de 2 {r.two_extreme}; base={r.retr_base_size}")
        else:
            if (t.price - r.retr_extreme) * (-d) > 0:
                r.retr_extreme = t.price
            r.retr_size = abs(r.retr_extreme - r.two_extreme)

        if r.retr_base_size and r.retr_size * 2 > r.retr_base_size:
            r.three_status = "IMPOSSIBLE"
            r.retr_active = False
            r.ev(t, "THREE_IMPOSSIBLE_50",
                 f"retroceso={r.retr_size} > 50% de 2 ({r.retr_base_size / 2:.1f})")
            self._module_1_2(t)
            return

        if (r.retr_base_size and r.retr_size * 2 == r.retr_base_size
                and not r.retr_50):
            r.retr_50 = True
            r.ev(t, "FIFTY_PERCENT_EXACT",
                 f"retroceso={r.retr_size} = 50% de 2; frontera inclusiva")

        if r.retr_size >= NOISE:
            r.retr_valid = True

        # Recuperacion de la direccion de 2 y superacion estricta del extremo
        # final de 2: solo aqui nace 3, y solo tras un retroceso funcional.
        if (t.price - r.two_extreme) * d > 0:
            if r.retr_valid:
                r.three_status = "CONFIRMED"
                r.three_extreme = t.price
                r.three_extreme_st = t.time_ms
                r.three_st = r.two_extreme_st
                r.three_bar = t.bar
                r.three_kt = t.time_ms
                r.ev(t, "THREE_CONFIRMED",
                     f"extremo={t.price} supera 2={r.two_extreme} "
                     f"retroceso={r.retr_size}")
                self._module_1_2_3(t)
                return
            # Retroceso absorbido por ruido: 2 conserva la finalidad.
            r.two_extreme = t.price
            r.two_extreme_st = t.time_ms
            r.two_size = abs(r.two_extreme - r.two_origin)
            r.retr_active = False
            r.ev(t, "TWO_ABSORBS_NOISE_RETRACE",
                 f"retroceso={r.retr_size} < {NOISE}; 2 continua")
            return

    def _on_three_live_tick(self, t: Tick) -> None:
        r = self.reading
        d = r.two_dir
        if (t.price - r.three_extreme) * d > 0:
            r.three_extreme = t.price
            r.three_extreme_st = t.time_ms
            r.mod_extreme = t.price
            r.mod_extreme_st = t.time_ms
            r.mod_size = abs(r.mod_extreme - r.mod_origin)
            r.ev(t, "THREE_EXTENDED",
                 f"extremo final de 3={t.price} modulo={r.mod_size}")
            return
        # A puede nacer dentro de la misma vela de 3. Si 3 vuelve a
        # extenderse, la A pendiente se absorbe y 3 conserva la autoridad.
        if (t.price - r.three_extreme) * (-d) >= RETURN_MIN:
            self._open_contrary(t, r.three_extreme, r.three_extreme_st, "3")

    # ------------------------------------------------------------------- A / B
    def _open_contrary(self, t: Tick, extreme: int, extreme_st: int,
                       previous: str) -> None:
        r = self.reading
        r.mod_dir = r.one_dir
        r.a_status = "CONTRARY_MOVE_PENDING"
        r.a_dir = -r.mod_dir
        r.a_origin = extreme
        r.a_origin_st = extreme_st
        r.a_extreme = extreme
        r.a_extreme_st = extreme_st
        r.a_structural_end_st = extreme_st
        r.a_kt = 0
        r.a_size = 0
        r.a_authority = "PENDING"
        r.active_function = "A"
        r.phase = "A_PENDING"
        r.ev(t, "CONTRARY_MOVE_PENDING",
             f"previous={previous} origin={extreme} dir={r.a_dir} "
             f"module={r.mod_origin}->{r.mod_extreme} size={r.mod_size}")

    def _on_a_pending_tick(self, t: Tick) -> None:
        r = self.reading
        # Extension del modulo/3 en su direccion: absorbe A pendiente.
        # Solo cuando A ya tiene un recorrido propio; si A aun no se ha
        # movido, el tick pertenece al cierre del modulo y no lo reescribe.
        if (r.a_size > 0 and r.mod_dir
                and (t.price - r.mod_extreme) * r.mod_dir > 0):
            r.mod_extreme = t.price
            r.mod_extreme_st = t.time_ms
            r.mod_size = abs(r.mod_extreme - r.mod_origin)
            if r.three_status == "CONFIRMED":
                r.three_extreme = t.price
                r.three_extreme_st = t.time_ms
            r.a_status = "ABSORBED_IN_ACTIVE_FUNCTION"
            r.a_authority = "NONE"
            r.return_status = "ABSORBED_IN_MODULE" if r.return_status else ""
            r.return_absorbed += 1
            # Si 3 sigue vivo, la absorcion devuelve el control a 3 para que
            # continue hasta su extremo final; no se cierra la lectura.
            r.phase = "THREE_LIVE" if r.mod_status == "REGULAR_1_2_3" else "A_ABSORBED"
            r.ev(t, "A_ABSORBED_IN_ACTIVE_FUNCTION",
                 f"module_extreme={r.mod_extreme} size={r.mod_size}")
            return

        # A sigue su direccion: actualiza su extremo vivo.
        if (t.price - r.a_extreme) * r.a_dir > 0:
            r.a_extreme = t.price
            r.a_extreme_st = t.time_ms
            r.a_size = abs(r.a_extreme - r.a_origin)
            if r.return_status == "RETURN_MOVE_PENDING":
                r.return_status = "ABSORBED_IN_A"
                r.return_absorbed += 1
                r.return_extended = False
                r.return_jump = False
                r.ev(t, "RETURN_ABSORBED_IN_A",
                     f"nuevo extremo A={r.a_extreme}; retorno absorbido")
            # VIA 2 — AUT directo por A. La precondicion ejecutable es
            # A_CONFIRMED, nunca CONTRARY_MOVE_PENDING. Si un movimiento
            # pendiente cruza la base, no se inventa la causalidad: queda
            # OPEN_RULE_BLOCK y no nace nuevo 1.
            if (r.a_extreme - r.mod_origin) * r.a_dir > 0:
                if r.a_confirmations == 0:
                    r.aut_direct_status = "OPEN_RULE_BLOCK"
                    r.ev(t, "AUT_DIRECT_REQUIRES_A_CONFIRMED",
                         f"A pendiente cruza la base {r.mod_origin}; "
                         f"AUT directo exige A_CONFIRMED previa")
                else:
                    self._confirm_aut_direct(t)
            return

        # Movimiento contra A. El retorno no depende del numero de ticks:
        # se confirma por extension de su propio extremo o por un salto
        # estructural unico; el 2,0 inicial solo separa ruido.
        disp = (t.price - r.a_extreme) * (-r.a_dir)
        if disp <= 0:
            return
        if r.return_status in ("", "ABSORBED_IN_A"):
            if disp >= RETURN_MIN:
                r.return_status = "RETURN_MOVE_PENDING"
                r.return_dir = -r.a_dir
                r.return_origin = r.a_extreme
                r.return_first_st = t.time_ms
                r.return_first_extreme = t.price
                r.return_extended = False
                r.return_jump = False
                r.return_extreme = t.price
                r.return_extreme_st = t.time_ms
                r.return_size = disp
                r.return_ticks = 1
                # Politica de cuatro puntos retirada: el tamano del primer
                # tick NO confirma autonomia. Solo abre el retorno pendiente.
                r.return_extended = False
                r.return_jump = False
                r.ev(t, "RETURN_MOVE_PENDING",
                     f"origin={r.return_origin} extreme={t.price} disp={disp}")
            return

        r.return_ticks += 1
        if (t.price - r.return_extreme) * r.return_dir > 0:
            r.return_extreme = t.price
            r.return_extreme_st = t.time_ms
            if (r.return_extreme - r.return_first_extreme) * r.return_dir > 0:
                r.return_extended = True
        r.return_size = abs(r.return_extreme - r.a_extreme)

        # Autonomia causal del retorno: conserva direccion contraria a A y
        # extiende su PROPIO extremo. Sin umbral fijo de puntos ni de ticks.
        if r.return_size >= RETURN_MIN and r.return_extended:
            self._confirm_a_and_open_b(t)

    def _confirm_a_and_open_b(self, t: Tick) -> None:
        r = self.reading
        if r.a_confirmations > 0 or r.a_status != "CONTRARY_MOVE_PENDING":
            return
        # 3 conserva autoridad hasta el cierre de su vela de confirmacion;
        # A puede nacer dentro de ella, pero no archivarla antes de que 3
        # agote su extremo estructural en esa vela.
        if r.three_status == "CONFIRMED" and t.bar <= r.three_bar:
            return
        r.a_status = "A_CONFIRMED"
        r.a_authority = "ARCHIVED"
        r.a_kt = t.time_ms
        r.a_confirmations += 1
        r.a_structural_end_st = r.a_extreme_st
        r.a_size = abs(r.a_extreme - r.a_origin)
        r.return_status = "CONFIRMED_RETURN"
        r.b_status = "CANDIDATE"
        r.b_dir = r.return_dir
        r.b_origin = r.a_extreme
        r.b_origin_st = r.a_extreme_st
        r.b_extreme = r.return_extreme
        r.b_extreme_st = r.return_extreme_st
        r.b_size = abs(r.b_extreme - r.b_origin)
        r.b_st = r.return_first_st
        r.b_kt = t.time_ms
        r.phase = "B_LIVE"
        r.active_function = "B_CANDIDATE"
        if r.three_status == "CONFIRMED":
            r.three_authority = "ARCHIVED"
        r.module_authority = "FROZEN_REFERENCE"
        r.ev(t, "A_CONFIRMED",
             f"origin={r.a_origin} extreme={r.a_extreme} size={r.a_size} "
             f"structural_time={_hhmm(r.a_origin_st)} knowledge_time={_hhmm(t.time_ms)}")
        r.ev(t, "B_CANDIDATE",
             f"origin={r.b_origin} dir={r.b_dir} extreme={r.b_extreme} "
             f"structural_time={_hhmm(r.b_st)} knowledge_time={_hhmm(t.time_ms)}")

    def _on_b_candidate_tick(self, t: Tick) -> None:
        r = self.reading
        # Solo B candidata puede ser absorbida por A; B Grande/AUT ya no
        # pertenecen a A y no aceptan una extension de A como reemplazo.
        if r.b_status == "CANDIDATE" and (t.price - r.a_extreme) * r.a_dir > 0:
            r.a_extreme = t.price
            r.a_extreme_st = t.time_ms
            r.a_size = abs(r.a_extreme - r.a_origin)
            r.a_authority = "REOPENED"
            r.b_status = "ABSORBED_IN_A"
            r.phase = "A_PENDING"
            r.active_function = "A"
            r.ev(t, "B_ABSORBED_IN_A",
                 f"A={r.a_extreme}; B candidata absorbida")
            return

        prev_size = r.b_size
        if (t.price - r.b_extreme) * r.b_dir > 0:
            r.b_extreme = t.price
            r.b_extreme_st = t.time_ms
        r.b_size = abs(r.b_extreme - r.b_origin)
        if r.a_size <= 0:
            return

        limit = r.a_size * 127 // 100 + 25
        if r.b_size > limit:
            # Salto directo desde <100% a >127%+0,25: se registra el cruce
            # causal de B Grande, pero el estado vigente final es AUT.
            if prev_size < r.a_size or not r.b_grande_kt:
                r.b_grande_kt = t.time_ms
                r.b_grande_status = "CAUSAL_CROSS_IN_AUT_TICK"
                r.ev(t, "B_GRANDE_CAUSAL_CROSS",
                     f"B={r.b_size} cruza 100% y AUT en el mismo tick")
            self._confirm_aut(t)
            return

        if r.b_size >= r.a_size and not r.b_grande_kt:
            r.b_grande_kt = t.time_ms
            r.b_grande_status = "B_GRANDE"
            r.b_flags = "B_GRANDE"
            r.active_function = "B_GRANDE"
            r.ev(t, "B_GRANDE",
                 f"B={r.b_size} alcanza 100% de A={r.a_size}")

        if r.b_size == limit:
            r.b_grande_status = "B_GRANDE"
            r.active_function = "B_GRANDE"

        # C Grande (funcion formal): movimiento estructural contrario desde
        # el extremo final de B Grande. No usa el 100% de A para confirmarse.
        if r.b_grande_kt:
            contr = (t.price - r.b_extreme) * (-r.b_dir)
            if contr >= RETURN_MIN:
                self._open_c(t)

    def _confirm_aut(self, t: Tick) -> None:
        r = self.reading
        if r.aut_status == "AUT_CONFIRMED":
            return
        r.b_status = "AUT"
        r.b_grande_status = "AUT"
        r.aut_status = "AUT_CONFIRMED"
        r.aut_kt = t.time_ms
        r.aut_price = t.price
        r.a_authority = "ARCHIVED"
        if r.three_status == "CONFIRMED":
            r.three_authority = "ARCHIVED"
        r.module_authority = "FROZEN_REFERENCE"
        r.new_one_status = "NEW_ONE_ACTIVE"
        r.n_origin = r.b_origin
        r.n_origin_st = r.b_origin_st
        r.n_dir = r.b_dir
        r.n_st = r.b_st
        r.n_kt = t.time_ms
        r.n_extreme = t.price
        r.n_extreme_st = t.time_ms
        r.n_size = abs(r.n_extreme - r.n_origin)
        r.active_function = "NEW_ONE"
        r.phase = "NEW_ONE_ACTIVE"
        r.ev(t, "AUT_CONFIRMED",
             f"B={r.b_size} > 127%+0,25 de A ({r.a_size * 127 // 100 + 25}); "
             f"knowledge_time={_hhmm(t.time_ms)}")
        r.ev(t, "NEW_ONE_ACTIVE",
             f"origin={r.n_origin} dir={r.n_dir} structural_time={_hhmm(r.n_st)} "
             f"knowledge_time={_hhmm(r.n_kt)} extreme={r.n_extreme}")

    def _open_c(self, t: Tick) -> None:
        """C Grande: nacimiento del movimiento contrario desde B Grande."""
        r = self.reading
        r.c_status = "C_GRANDE"
        r.c_dir = -r.b_dir
        r.c_origin = r.b_extreme
        r.c_origin_st = t.time_ms          # nacimiento fisico del contrario
        r.c_extreme = t.price
        r.c_extreme_st = t.time_ms
        r.c_kt = t.time_ms
        r.c_size = abs(r.c_extreme - r.c_origin)
        r.c_authority = "LIVE"
        r.b_authority = "ARCHIVED"
        r.b_status = "C_OPENED"
        r.module_authority = "FROZEN_REFERENCE"
        r.active_function = "C"
        r.phase = "C_LIVE"
        r.ev(t, "C_GRANDE",
             f"origin={r.c_origin} dir={r.c_dir} extreme={r.c_extreme} "
             f"b_extreme={r.b_extreme} b_authority=ARCHIVED "
             f"structural_time={_hhmm(r.c_origin_st)} "
             f"knowledge_time={_hhmm(r.c_kt)}")
        # Si el nacimiento ya cruza la base, la tendencia se resuelve aqui.
        if (r.c_extreme - r.mod_origin) * r.c_dir > 0:
            self._confirm_c_as_trend(t)

    def _on_c_tick(self, t: Tick) -> None:
        r = self.reading
        if (t.price - r.c_extreme) * r.c_dir > 0:
            r.c_extreme = t.price
            r.c_extreme_st = t.time_ms
            r.c_size = abs(r.c_extreme - r.c_origin)
            r.ev(t, "C_EXTENDED", f"extreme={r.c_extreme} size={r.c_size}")
        # C usada como tendencia: superacion ESTRICTA de la base del modulo.
        if (r.c_extreme - r.mod_origin) * r.c_dir > 0:
            self._confirm_c_as_trend(t)

    def _confirm_c_as_trend(self, t: Tick) -> None:
        r = self.reading
        if r.trend_status == "C_USED_AS_TREND":
            return
        r.trend_status = "C_USED_AS_TREND"
        r.trend_kt = t.time_ms
        r.transition_reason = "C_USED_AS_TREND"
        r.c_authority = "ARCHIVED"
        r.new_one_status = "NEW_ONE_ACTIVE"
        r.n_origin = r.c_origin
        r.n_origin_st = r.c_origin_st
        r.n_dir = r.c_dir
        r.n_st = r.c_origin_st
        r.n_kt = t.time_ms
        r.n_extreme = t.price
        r.n_extreme_st = t.time_ms
        r.n_size = abs(r.n_extreme - r.n_origin)
        r.module_authority = "FROZEN_REFERENCE"
        r.active_function = "NEW_ONE"
        r.phase = "NEW_ONE_ACTIVE"
        r.ev(t, "C_USED_AS_TREND",
             f"C={r.c_size} supera estrictamente la base {r.mod_origin}; "
             f"transition_reason=C_USED_AS_TREND")
        r.ev(t, "NEW_ONE_ACTIVE",
             f"origin={r.n_origin} dir={r.n_dir} "
             f"structural_time={_hhmm(r.n_st)} "
             f"knowledge_time={_hhmm(r.n_kt)} extreme={r.n_extreme}")

    def _confirm_aut_direct(self, t: Tick) -> None:
        """VIA 2 — AUT directo por A.

        A ya existe y supera ESTRICTAMENTE la base del modulo. En esta via:
          * no hay B;
          * no se aplica 127%+0,25;
          * el nuevo 1 ES el propio movimiento A transformado;
          * knowledge_time es el primer tick de cruce, no el origen de A.
        """
        r = self.reading
        if r.aut_direct_status == "AUT_DIRECT_BY_A":
            return
        # Precondicion canonica: A ya confirmada. No se confirma aqui.
        if r.a_confirmations == 0:
            r.aut_direct_status = "OPEN_RULE_BLOCK"
            r.ev(t, "AUT_DIRECT_REQUIRES_A_CONFIRMED",
                 "AUT directo sin A_CONFIRMED previa: bloqueado")
            return
        r.transition_reason = "AUT_DIRECT_BY_A"
        r.a_status = "A_CONFIRMED_ARCHIVED"
        r.a_authority = "ARCHIVED"
        r.aut_direct_status = "AUT_DIRECT_BY_A"
        r.aut_direct_kt = t.time_ms
        r.aut_direct_price = t.price
        if r.three_status == "CONFIRMED":
            r.three_authority = "ARCHIVED"
        r.module_authority = "FROZEN_REFERENCE"
        # En la via directa B no existe formalmente (la candidata previa, si
        # existio, fue absorbida por la extension de A antes del cruce).
        r.b_status = ""
        r.b_grande_status = ""
        r.aut_status = ""
        r.new_one_status = "NEW_ONE_ACTIVE"
        r.n_origin = r.a_origin
        r.n_origin_st = r.a_origin_st
        r.n_dir = r.a_dir
        r.n_st = r.a_origin_st
        r.n_kt = t.time_ms
        r.n_extreme = t.price
        r.n_extreme_st = t.time_ms
        r.n_size = abs(r.n_extreme - r.n_origin)
        r.active_function = "NEW_ONE"
        r.phase = "NEW_ONE_ACTIVE"
        r.ev(t, "AUT_DIRECT_BY_A",
             f"A={r.a_size} supera estrictamente la base del modulo "
             f"{r.mod_origin}; knowledge_time={_hhmm(t.time_ms)}")
        r.ev(t, "NEW_ONE_ACTIVE",
             f"origin={r.n_origin} dir={r.n_dir} "
             f"structural_time={_hhmm(r.n_st)} "
             f"knowledge_time={_hhmm(r.n_kt)} extreme={r.n_extreme}")

    def _on_new_one_tick(self, t: Tick) -> None:
        r = self.reading
        if (t.price - r.n_extreme) * r.n_dir > 0:
            r.n_extreme = t.price
            r.n_extreme_st = t.time_ms
            r.n_size = abs(r.n_extreme - r.n_origin)
            r.ev(t, "NEW_ONE_EXTENDED",
                 f"extreme={r.n_extreme} size={r.n_size}")
        # B no se extiende despues de AUT por B: su ultimo valor es el del
        # cruce. En la via AUT directo por A, B no existe y no se escribe.
        if r.aut_status == "AUT_CONFIRMED":
            r.b_status = "AUT"

    # ------------------------------------------------------------------ modules
    def _module_by_discard(self, t: Tick, include_two: bool) -> None:
        r = self.reading
        r.mod_origin = r.one_origin
        r.mod_origin_st = r.one_st
        candidates = [(r.one_extreme, r.one_extreme_st, "1")]
        if include_two and r.two_extreme:
            candidates.append((r.two_extreme, r.two_extreme_st, "2"))
        if r.one_dir > 0:
            r.mod_extreme, r.mod_extreme_st, r.mod_owner = max(candidates)
        else:
            r.mod_extreme, r.mod_extreme_st, r.mod_owner = min(candidates)
        r.mod_size = abs(r.mod_extreme - r.mod_origin)
        r.mod_status = "BY_DISCARD_1_2" if include_two else "BY_DISCARD_1"
        r.mod_dir = r.one_dir
        r.three_status = "IMPOSSIBLE"
        r.ev(t, "MODULE_BY_DISCARD",
             f"origin={r.mod_origin} extreme={r.mod_extreme} size={r.mod_size} "
             f"owner={r.mod_owner} status={r.mod_status}")
        if r.gap_branch and not include_two:
            r.ev(t, "GAP_IMPLICIT_TRANSITION",
                 "2 prohibido por apertura no plana: modulo por descarte y A "
                 "implicita desde el extremo observable; sin precios inventados")
        self._open_contrary(t, r.mod_extreme, r.mod_extreme_st, r.mod_status)

    def _module_1_2(self, t: Tick) -> None:
        r = self.reading
        r.mod_origin = r.one_origin
        r.mod_origin_st = r.one_st
        candidates = [(r.one_extreme, r.one_extreme_st, "1"),
                      (r.two_extreme, r.two_extreme_st, "2")]
        if r.one_dir > 0:
            r.mod_extreme, r.mod_extreme_st, r.mod_owner = max(candidates)
        else:
            r.mod_extreme, r.mod_extreme_st, r.mod_owner = min(candidates)
        r.mod_size = abs(r.mod_extreme - r.mod_origin)
        r.mod_status = "MODULE_1_2"
        r.mod_dir = r.one_dir
        r.three_status = "IMPOSSIBLE"
        r.ev(t, "MODULE_1_2",
             f"origin={r.mod_origin} extreme={r.mod_extreme} size={r.mod_size} "
             f"owner={r.mod_owner}")
        self._open_contrary(t, r.mod_extreme, r.mod_extreme_st, "MODULE_1_2")

    def _module_1_2_3(self, t: Tick) -> None:
        r = self.reading
        r.mod_origin = r.one_origin
        r.mod_origin_st = r.one_st
        r.mod_extreme = r.three_extreme
        r.mod_extreme_st = r.three_extreme_st
        r.mod_owner = "3"
        r.mod_size = abs(r.mod_extreme - r.mod_origin)
        r.mod_status = "REGULAR_1_2_3"
        r.mod_dir = r.two_dir
        r.three_authority = "LIVE"
        r.module_authority = "ACTIVE"
        r.active_function = "3"
        r.phase = "THREE_LIVE"
        r.ev(t, "MODULE_1_2_3_CONFIRMED",
             f"origin={r.mod_origin} extreme={r.mod_extreme} size={r.mod_size}; "
             f"extremo de 3 vivo")

    # -------------------------------------------------------------------- loop
    def run(self) -> "Reader":
        r = self.reading
        for t in self.ticks:
            n_events = len(r.events)
            new_bar = t.bar != self.cur_bar
            if new_bar and self.cur_bar != -1 and r.phase in (
                    "A_PENDING", "B_LIVE", "C_LIVE", "NEW_ONE_ACTIVE",
                    "TWO_LIVE", "WAIT_THREE", "THREE_LIVE"):
                r.ev(t, "CONTINUATION_ACROSS_BAR",
                     f"phase={r.phase} continua sin reiniciarse al cambiar de vela")
            if new_bar:
                if self.cur_bar != -1:
                    self._on_bar_close(self.cur_bar, self.last_price, self.last_time)
                self.cur_bar = t.bar
                b = self.bars.setdefault(t.bar, {"o": t.price, "h": t.price,
                                                 "l": t.price, "c": t.price})
                self._on_bar_open(t)
            else:
                b = self.bars[t.bar]
                b["h"] = max(b["h"], t.price)
                b["l"] = min(b["l"], t.price)
                b["c"] = t.price

            self.last_price = t.price
            self.last_time = t.time_ms
            r = self.reading

            if r.phase == "INITIAL_BAR":
                pass
            elif r.phase == "ONE_LIVE":
                if (t.price - r.one_extreme) * r.one_dir > 0:
                    r.one_extreme = t.price
                    r.one_extreme_st = t.time_ms
                    r.one_size = abs(r.one_extreme - r.one_origin)
            elif r.phase == "TWO_LIVE":
                self._on_two_tick(t)
            elif r.phase == "WAIT_THREE":
                self._on_three_tick(t)
            elif r.phase == "THREE_LIVE":
                self._on_three_live_tick(t)
            elif r.phase == "A_PENDING":
                self._on_a_pending_tick(t)
            elif r.phase == "B_LIVE":
                self._on_b_candidate_tick(t)
            elif r.phase == "C_LIVE":
                self._on_c_tick(t)
            elif r.phase == "NEW_ONE_ACTIVE":
                self._on_new_one_tick(t)

            self.events.extend(r.events[n_events:])
            self.trace.append(self._snapshot(t))

        n_events = len(r.events)
        self._finalize()
        self.events.extend(r.events[n_events:])
        return self

    def _on_bar_open(self, t: Tick) -> None:
        r = self.reading
        if r.phase == "INITIAL_BAR":
            if r.one_bar == -1:
                r.one_bar = t.bar
                r.one_origin = t.price
                r.one_extreme = t.price
                r.one_st = t.time_ms
                r.one_status = "CANDIDATE"
                r.one_dir = 0
                r.ev(t, "ONE_CANDIDATE_INITIAL", f"open={t.price}")
                return
            if t.bar == r.one_bar:
                return
            self._confirm_initial_one(t)
            self._eval_opening(t)
            return
        if r.phase == "ONE_LIVE":
            self._freeze_one(t)
            if r.phase == "WAIT_OPENING":
                self._eval_opening(t)
            return
        if r.phase == "WAIT_OPENING":
            self._eval_opening(t)
            return
        # TWO_LIVE / WAIT_THREE / THREE_LIVE / CORE_A... continue across bars

    def _on_bar_close(self, bar: int, price: int, time_ms: int) -> None:
        self.prev_close = price
        r = self.reading
        if r.phase == "INITIAL_BAR":
            r.one_kt = time_ms
            r.ev(Tick(-1, time_ms, bar, price), "INITIAL_BAR_CLOSED", f"close={price}")
            return
        if r.phase == "TWO_LIVE":
            r.two_status = "IMPOSSIBLE_CLOSE"
            r.two_kt = time_ms
            r.ev(Tick(-1, time_ms, bar, price), "TWO_IMPOSSIBLE_CLOSE",
                 f"cierre sin 100% de 1: measure={r.two_size} one={r.one_size}")
            self._module_by_discard(Tick(-1, time_ms, bar, price), include_two=True)

    def _snapshot(self, t: Tick) -> dict:
        r = self.reading
        return {
            "sequence_id": t.seq, "time": _hhmm(t.time_ms), "price": t.price,
            "reading_id": r.reading_id, "gid": r.gid, "phase": r.phase,
            "one_dir": r.one_dir, "one_origin": r.one_origin,
            "one_extreme": r.one_extreme, "one_size": r.one_size,
            "two_status": r.two_status, "two_size": r.two_size,
            "two_extreme": r.two_extreme,
            "three_status": r.three_status, "three_extreme": r.three_extreme,
            "mod_status": r.mod_status, "mod_size": r.mod_size,
            "mod_origin": r.mod_origin, "mod_extreme": r.mod_extreme,
            "mod_owner": r.mod_owner, "a_status": r.a_status,
            "a_origin": r.a_origin, "a_extreme": r.a_extreme,
            "a_size": r.a_size, "a_kt": r.a_kt,
            "aut_direct_status": r.aut_direct_status,
            "aut_direct_kt": r.aut_direct_kt,
            "n_kt": r.n_kt,
            "return_status": r.return_status,
            "b_status": r.b_status, "b_origin": r.b_origin,
            "b_extreme": r.b_extreme, "b_size": r.b_size,
            "b_grande_status": r.b_grande_status,
            "aut_status": r.aut_status,
            "new_one_status": r.new_one_status,
            "c_status": r.c_status, "c_extreme": r.c_extreme,
            "trend_status": r.trend_status,
            "transition_reason": r.transition_reason,
            "n_origin": r.n_origin, "n_extreme": r.n_extreme,
            "n_size": r.n_size, "active_function": r.active_function,
            "events": [e for e in r.events if e["seq"] == t.seq],
        }

    def _finalize(self) -> None:
        r = self.reading
        if r.phase == "WAIT_THREE":
            r.phase = "CORE_WAIT_THREE_A_NOT_IMPLEMENTED"
        r.ev(Tick(-1, self.last_time, self.cur_bar, self.last_price), "CORE_END",
             f"phase={r.phase}; C/CUT/TT/FT no implementados")

    def summary(self) -> dict:
        r = self.reading
        return {
            "reader": CORE_VERSION,
            "reading_id": r.reading_id,
            "ticks": len(self.ticks),
            "phase": r.phase,
            "one": {"dir": r.one_dir, "origin": r.one_origin,
                    "extreme": r.one_extreme, "size": r.one_size,
                    "status": r.one_status},
            "two": {"origin": r.two_origin, "extreme": r.two_extreme,
                    "size": r.two_size, "status": r.two_status},
            "three": {"extreme": r.three_extreme, "status": r.three_status,
                      "kt": _hhmm(r.three_kt) if r.three_kt else ""},
            "module": {"origin": r.mod_origin, "extreme": r.mod_extreme,
                       "size": r.mod_size, "status": r.mod_status,
                       "owner": r.mod_owner},
            "a": {"status": r.a_status, "dir": r.a_dir,
                  "origin": r.a_origin, "extreme": r.a_extreme,
                  "size": r.a_size,
                  "structural_time": _hhmm(r.a_origin_st) if r.a_origin_st else "",
                  "knowledge_time": _hhmm(r.a_kt) if r.a_kt else "",                    "confirmations": r.a_confirmations,
                  "aut_direct": r.aut_direct_status,
                  "aut_direct_knowledge_time":
                      _hhmm(r.aut_direct_kt) if r.aut_direct_kt else "",
                  "aut_direct_price": r.aut_direct_price},
            "return_move": {"status": r.return_status,
                            "origin": r.return_origin,
                            "extreme": r.return_extreme,
                            "size": r.return_size,
                            "structural_time": _hhmm(r.return_first_st) if r.return_first_st else "",
                            "absorbed": r.return_absorbed},
            "b": {"status": r.b_status, "origin": r.b_origin,
                  "extreme": r.b_extreme, "size": r.b_size,
                  "structural_time": _hhmm(r.b_st) if r.b_st else "",
                  "knowledge_time": _hhmm(r.b_kt) if r.b_kt else "",
                  "grande_status": r.b_grande_status,
                  "grande_knowledge": _hhmm(r.b_grande_kt) if r.b_grande_kt else "",
                  "flags": r.b_flags},
            "aut": {"status": r.aut_status,
                    "knowledge_time": _hhmm(r.aut_kt) if r.aut_kt else "",
                    "price": r.aut_price},
            "new_one": {"status": r.new_one_status,
                        "origin": r.n_origin, "dir": r.n_dir,
                        "extreme": r.n_extreme, "size": r.n_size,
                        "structural_time": _hhmm(r.n_st) if r.n_st else "",
                        "knowledge_time": _hhmm(r.n_kt) if r.n_kt else ""},
            "c": {"status": r.c_status, "dir": r.c_dir,
                  "origin": r.c_origin, "extreme": r.c_extreme,
                  "size": r.c_size,
                  "structural_time": _hhmm(r.c_origin_st) if r.c_origin_st else "",
                  "knowledge_time": _hhmm(r.c_kt) if r.c_kt else "",
                  "authority": r.c_authority},
            "trend": {"status": r.trend_status,
                      "knowledge_time": _hhmm(r.trend_kt) if r.trend_kt else ""},
            "transition_reason": r.transition_reason,
            "active_function": r.active_function,
            "authority": {"a": r.a_authority, "b": r.b_authority,
                          "three": r.three_authority,
                          "module": r.module_authority,
                          "c": r.c_authority},
            "first_tick": self.ticks[0].seq if self.ticks else None,
            "last_tick": self.ticks[-1].seq if self.ticks else None,
        }


def _hhmm(ms: int) -> str:
    if not ms:
        return ""
    total = ms // 1000
    hh = (total // 3600) % 24
    mm = (total // 60) % 60
    ss = total % 60
    return f"{hh:02d}:{mm:02d}:{ss:02d}.{ms % 1000:03d}"


def _price(s: str) -> int:
    return int(round(float(s) * 100))


def load_ticks(path: Path) -> list[Tick]:
    out = []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=";"):
            out.append(Tick(int(row["sequence_id"]), int(row["time_msc"]),
                            int(row["time_msc"]) // 60000, _price(row["bid"])))
    return out


def _bar_of(h: str) -> int:
    hh, mm = h.split(":")
    return int(hh) * 60 + int(mm)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="t_from", default="16:15")
    ap.add_argument("--to", dest="t_to", default="17:29")
    ap.add_argument("--reading-id", default="L1")
    ap.add_argument("--trace")
    ap.add_argument("--events")
    ap.add_argument("--summary")
    args = ap.parse_args(argv)

    ticks = load_ticks(FEED)
    b0, b1 = _bar_of(args.t_from), _bar_of(args.t_to)
    ticks = [t for t in ticks if b0 <= t.bar % 1440 <= b1]
    rd = Reader(ticks, reading_id=args.reading_id).run()

    if args.trace:
        with open(args.trace, "w", encoding="utf-8") as fh:
            for row in rd.trace:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    if args.events:
        with open(args.events, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["sequence_id", "time", "bar", "gid", "event", "detail"])
            for e in rd.events:
                w.writerow([e["seq"], _hhmm(e["time_ms"]), e["bar"],
                            e["gid"], e["event"], e["detail"]])
    if args.summary:
        with open(args.summary, "w", encoding="utf-8") as fh:
            json.dump(rd.summary(), fh, indent=2, ensure_ascii=False)
    if not any([args.trace, args.events, args.summary]):
        print(json.dumps(rd.summary(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
