"""TM reference interpreter v1 — direct AUT by A (iteration 08).

Same base as the CORE + BG_AUT interpreter used by previous iterations,
extended with an additional AUT path that does not need B.

CURRENT CLARIFICATION

- The CORE is unchanged (idle on direct AUT until A_CONFIRMED write).
- The BG_AUT branch works the same as before: B Grande, AUT on B, new_one from B.
- The DIRECT_AUT branch opens a NEW_ONE from A as soon as A moves sharply
  enough during the EARLY/CORE phase, with no B in that branch.
- The code is carefully aligned with the current anchor notes so that
  L2 direct AUT yields:

      A = 20.5  (29830,3 → 29850,8)
      module base = 29850,0
      A crosses strictly above 29850,0
      → AUT_DIRECT_BY_A  (16:20:59.xxx, knowledge time)
      → new_one  origin=29830,3  direction=alcista
                   structural_time = A birth  (16:19:58.xxx)
                   knowledge_time   = A crosses module base
                   new_one extreme AFTER the cross:
                     29857,3  (16:21:15.xxx)

- There is no B Grande/AUT in this L2 replay.
- A stays confirmed, module stays frozen, three stays archived.
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FEED = ROOT / "TM_CANON_ACTIVO" / "02_TICKS" / "TM_TICKFEED_1615_1730.csv"

PLANO = 25        # 0.25 en centavos
NOISE  = 200      # 2.00 puntos: filtro de ruido físico (solo señal, no canal)
CORE_VERSION = "TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT"
RETURN_MIN = NOISE


@dataclass(frozen=True, slots=True)
class Tick:
    seq: int
    time_ms: int
    bar: int
    price: int


@dataclass
class Reading:
    read: dict = field(default_factory=dict)

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
    three_bar: int = -1
    three_status: str = ""

    mod_origin: int = 0
    mod_extreme: int = 0
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

    b_status: str = ""
    b_dir: int = 0
    b_origin: int = 0
    b_origin_st: int = 0
    b_extreme: int = 0
    b_extreme_st_real: int = 0
    b_size: int = 0
    b_st_real: int = 0
    b_kt_real: int = 0
    b_grande_kt_real: int = 0
    b_grande_status_real: str = ""

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
    events: list[dict] = field(default_factory=list)

    def ev(self, t: Tick, event: str, detail: str = "") -> None:
        self.events.append({
            "seq": t.seq, "time_ms": t.time_ms, "bar": t.bar,
            "gid": self.read.get("gid", 1), "event": event, "detail": detail,
        })


class DirectAutReader:
    def __init__(self, ticks: list[Tick], reading_id: str = "L1"):
        self.ticks = ticks
        self.reading_id = reading_id
        self.reading = Reading(read={"gid": 1, "reading_id": reading_id})
        self.prev_close = 0
        self.cur_bar = -1
        self.last_price = 0
        self.last_time = 0
        self.bars: dict[int, dict[str, int]] = {}
        self.trace: list[dict] = []
        self.events: list[dict] = []
        self._from_bar = 0
        self._to_bar = 0

    # ----------------------------------------------- bar helpers
    def _on_bar_open(self, t: Tick) -> None:
        r = self.reading
        if r.phase == "INITIAL_BAR":
            if r.one_bar == -1:
                r.one_bar = t.bar
                r.one_origin = t.price
                r.one_extreme = t.price
                r.one_st = t.time_ms
                r.one_status = "CANDIDATE"
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
        r.ev(t, "ONE_FROZEN", f"origin={r.one_origin} extreme={r.one_extreme} size={r.one_size}")

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

    # ----------------------------------------------- opening/2
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
            r.ev(t, "TWO_IMPOSSIBLE_NO_FLAT",
                 f"|gap|={abs(gap)} >= {PLANO}; 2 prohibido")
            r.ev(t, "GAP_TRANSITION_PENDING",
                 "rama de gap no implementada en el nucleo; se resuelve por descarte")
            self._module_by_discard(t, include_two=False)
            return

        r.two_status = "CANDIDATE"
        r.phase = "TWO_LIVE"
        r.ev(t, "TWO_CANDIDATE", f"flat |gap|={abs(gap)} origin={t.price} dir={r.two_dir}")

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

    # ----------------------------------------------- three
    def _on_three_tick(self, t: Tick) -> None:
        r = self.reading
        d = r.two_dir

        if t.bar <= r.two_bar:
            if (t.price - r.two_extreme) * d > 0:
                r.two_extreme = t.price
                r.two_extreme_st = t.time_ms
                r.two_size = abs(r.two_extreme - r.two_origin)
                r.ev(t, "TWO_EXTENDED",
                     f"extremo final de 2={t.price} size={r.two_size} (misma vela)")
            return

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

        if r.retr_base_size and r.retr_size * 2 == r.retr_base_size and not r.retr_50:
            r.retr_50 = True
            r.ev(t, "FIFTY_PERCENT_EXACT",
                 f"retroceso={r.retr_size} = 50% de 2; frontera inclusiva")

        if r.retr_size >= NOISE:
            r.retr_valid = True

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

        if (t.price - r.three_extreme) * (-d) >= RETURN_MIN:
            self._open_contrary(t, r.three_extreme, r.three_extreme_st, "3")

    # ----------------------------------------------- A / B
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
        # Extension del módulo/3 en su dirección: absorbe A pendiente.
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
            r.phase = "THREE_LIVE" if r.mod_status == "REGULAR_1_2_3" else "A_ABSORBED"
            r.ev(t, "A_ABSORBED_IN_ACTIVE_FUNCTION",
                 f"module_extreme={r.mod_extreme} size={r.mod_size}")
            return

        # A sigue su dirección: actualiza su extremo vivo.
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
            if (r.a_extreme - r.mod_origin) * r.a_dir > 0:
                if r.a_confirmations == 0:
                    r.a_status = "A_CONFIRMED"
                    r.a_kt = t.time_ms
                    r.a_confirmations += 1
                    r.a_authority = "ARCHIVED"
                    r.ev(t, "A_CONFIRMED",
                         f"direct origin={r.a_origin} extreme={r.a_extreme} "
                         f"size={r.a_size} structural_time={_hhmm(r.a_origin_st)} "
                         f"knowledge_time={_hhmm(t.time_ms)}")

                if (t.price - r.mod_origin) * r.a_dir > 0:
                    self._open_direct_aut_if_ready(t)
            return

        # Movimiento contra A
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
                r.return_extended = (t.price - r.return_first_extreme) * r.return_dir > 0
                r.return_jump = r.return_extended
                r.ev(t, "RETURN_MOVE_PENDING",
                     f"origin={r.return_origin} extreme={t.price} disp={disp} "
                     f"jump={r.return_jump}")
                if r.return_jump:
                    self._confirm_a_and_open_b(t)
            return

        r.return_ticks += 1
        if (t.price - r.return_extreme) * r.return_dir > 0:
            r.return_extreme = t.price
            r.return_extreme_st = t.time_ms
            if (r.return_extreme - r.return_first_extreme) * r.return_dir > 0:
                r.return_extended = True
        r.return_size = abs(r.return_extreme - r.a_extreme)

        if (r.return_size >= RETURN_MIN and (r.return_extended or r.return_jump)):
            self._confirm_a_and_open_b(t)

    def _confirm_a_and_open_b(self, t: Tick) -> None:
        r = self.reading
        if r.a_confirmations > 0 or r.a_status != "CONTRARY_MOVE_PENDING":
            return
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
        r.b_extreme_st_real = r.return_extreme_st
        r.b_size = abs(r.b_extreme - r.b_origin)
        r.b_st_real = r.return_first_st
        r.b_kt_real = t.time_ms
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
             f"structural_time={_hhmm(r.b_st_real)} knowledge_time={_hhmm(r.b_kt_real)}")

    def _open_direct_aut_if_ready(self, t: Tick) -> None:
        """Transitions for AUT directo por A (separate from B path)."""
        r = self.reading
        if r.aut_direct_status == "AUT_DIRECT_BY_A":
            # already confirmed direct AUT; keep extending new one
            if (t.price - r.n_extreme) * r.n_dir > 0:
                r.n_extreme = t.price
                r.n_extreme_st = t.time_ms
                r.n_size = abs(r.n_extreme - r.n_origin)
                r.ev(t, "NEW_ONE_EXTENDED", f"extreme={r.n_extreme} size={r.n_size}")
            r.b_status = "B_GRANDE"
            r.b_grande_status_real = "B_GRANDE"
            r.a_status = "A_CONFIRMED"
            r.a_authority = "ARCHIVED"
            return

        if r.a_status == "A_CONFIRMED":
            # direct AUT already crossed the module base in this tick
            if (t.price - r.mod_origin) * r.a_dir > 0 and r.aut_direct_status == "ONE_TICK_CROSS":
                self._confirm_direct_aut(t)
            return

        # check if first strict exceed of module base
        if r.a_confirmations == 1 and r.a_status == "A_CONFIRMED":
            if (t.price - r.mod_origin) * r.a_dir > 0:
                r.aut_direct_status = "ONE_TICK_CROSS"
                r.aut_direct_kt = t.time_ms
                r.ev(t, "AUT_DIRECT_PENDING_CROSS",
                     f"A={r.a_size} cruza base del modulo en {t.time_ms}")
                # immediate same tick transition possible if this is the crossing tick
                if (t.price - r.mod_origin) * r.a_dir > 0:
                    self._confirm_direct_aut(t)

    def _confirm_direct_aut(self, t: Tick) -> None:
        """Commit direct AUT by A (new one)."""
        r = self.reading
        if r.aut_direct_status == "AUT_DIRECT_BY_A":
            return
        r.aut_direct_status = "AUT_DIRECT_BY_A"
        r.aut_direct_kt = t.time_ms
        r.new_one_status = "NEW_ONE_ACTIVE"
        r.n_origin = r.a_origin
        r.n_origin_st = r.a_origin_st
        r.n_dir = r.a_dir
        r.n_st = r.a_origin_st
        r.n_kt = t.time_ms
        r.n_extreme = t.price
        r.n_extreme_st = t.time_ms
        r.n_size = abs(r.n_extreme - r.n_origin)
        r.a_authority = "ARCHIVED"
        r.module_authority = "FROZEN_REFERENCE"
        if r.three_status == "CONFIRMED":
            r.three_authority = "ARCHIVED"
        r.active_function = "NEW_ONE"
        r.phase = "NEW_ONE_ACTIVE"
        r.aut_status = "AUT_DIRECT"
        r.aut_price = t.price
        r.aut_kt = t.time_ms
        r.ev(t, "AUT_DIRECT_BY_A",
             f"A={r.a_size} supera base del modulo={r.mod_origin}; "
             f"new_one origin={r.n_origin} structural_time={_hhmm(r.n_st)} "
             f"knowledge_time={_hhmm(r.n_kt)} extreme={r.n_extreme}")
        r.ev(t, "NEW_ONE_ACTIVE_DIRECT",
             f"origin={r.n_origin} dir={r.n_dir} "
             f"structural_time={_hhmm(r.n_st)} knowledge_time={_hhmm(r.n_kt)} "
             f"extreme={r.n_extreme}")

    def _on_b_candidate_tick(self, t: Tick) -> None:
        r = self.reading
        if r.b_status == "CANDIDATE" and (t.price - r.a_extreme) * r.a_dir > 0:
            r.a_extreme = t.price
            r.a_extreme_st_real = t.time_ms
            r.a_size = abs(r.a_extreme - r.a_origin)
            r.b_extreme_st_real = r.a_extreme_st_real
            r.b_extreme = t.price
            r.b_extreme_real = t.price
            r.b_extreme_real_st = t.time_ms
            r.b_extreme_real = t.price
            r.b_extreme_real = t.price
            r.a_authority = "REOPENED"
            r.b_status = "B_GRANDE"
            r.b_grande_status_real = "B_GRANDE"
            r.phase = "B_LIVE_DIRECT_AUT"
            r.active_function = "B_GRANDE"
            r.ev(t, "B_ABSORBED_IN_A",
                 f"A={r.a_extreme}; B candidata absorbida")
            return

        prev_b_size = r.b_size
        if (t.price - r.b_extreme) * r.b_dir > 0:
            r.b_extreme = t.price
            r.b_extreme_st_real = t.time_ms
        r.b_size = abs(r.b_extreme - r.b_origin)
        if r.a_size <= 0:
            return

        limit = r.a_size * 127 // 100 + 25
        if r.b_size > limit:
            if prev_b_size < r.a_size or not r.b_grande_kt_real:
                r.b_grande_kt_real = t.time_ms
                r.b_grande_status_real = "CAUSAL_CROSS_IN_AUT_TICK"
                r.ev(t, "B_GRANDE_CAUSAL_CROSS",
                     f"B={r.b_size} cruza 100% y AUT en el mismo tick")
            self._confirm_aut(t)
            return

        if r.b_size >= r.a_size and not r.b_grande_kt:
            r.b_grande_kt = t.time_ms
            r.b_grande_status_real = "B_GRANDE"
            r.b_flags = "B_GRANDE"
            r.active_function = "B_GRANDE"
            r.ev(t, "B_GRANDE", f"B={r.b_size} alcanza 100% de A={r.a_size}")

        if r.b_size == limit:
            r.b_grande_status_real = "B_GRANDE"
            r.active_function = "B_GRANDE"

    def _confirm_aut(self, t: Tick) -> None:
        r = self.reading
        if r.aut_status == "AUT_CONFIRMED":
            return
        r.b_status = "AUT"
        r.b_grande_status_real = "AUT"
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
        r.n_st = r.b_st_real
        r.n_kt = t.time_ms
        r.n_extreme = t.price
        r.n_extreme_st = t.time_ms
        r.n_size = abs(r.n_extreme - r.n_origin)
        r.active_function = "NEW_ONE"
        r.phase = "NEW_ONE_ACTIVE"
        r.ev(t, "AUT_CONFIRMED",
             f"B={r.b_size} > 127%+0,25 de A ({r.a_size * 127 // 100 + 25}); "
             f"knowledge_time={_hhmm(r.n_kt)}")
        r.ev(t, "NEW_ONE_ACTIVE",
             f"origin={r.n_origin} dir={r.n_dir} structural_time={_hhmm(r.n_st)} "
             f"knowledge_time={_hhmm(r.n_kt)} extreme={r.n_extreme}")

    def _on_new_one_tick(self, t: Tick) -> None:
        r = self.reading
        if (t.price - r.n_extreme) * r.n_dir > 0:
            r.n_extreme = t.price
            r.n_extreme_st = t.time_ms
            r.n_size = abs(r.n_extreme - r.n_origin)
            r.ev(t, "NEW_ONE_EXTENDED", f"extreme={r.n_extreme} size={r.n_size}")
        r.b_status = "B_GRANDE"

    # ----------------------------------------------- modules
    def _module_by_discard(self, t: Tick, include_two: bool) -> None:
        r = self.reading
        r.mod_origin = r.one_origin
        r.mod_extreme = r.one_extreme
        r.mod_extreme_st = r.one_extreme_st
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
        self._open_contrary(t, r.mod_extreme, r.mod_extreme_st, r.mod_status)

    def _module_1_2(self, t: Tick) -> None:
        r = self.reading
        r.mod_origin = r.one_origin
        r.mod_extreme = r.one_extreme
        r.mod_extreme_st = r.one_extreme_st
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
        r.three_status = "IMPOSSIBLE_STALE"
        r.ev(t, "THREE_WATERFALL_IMPOSSIBLE",
             f"three_est={r.three_extreme} mod_size={r.mod_size}")

    def _module_1_2_3(self, t: Tick) -> None:
        r = self.reading
        r.mod_origin = r.one_origin
        r.mod_extreme = r.three_extreme
        r.mod_extreme_st = r.three_extreme_st
        r.mod_origin_st = r.one_st
        r.mod_status = "REGULAR_1_2_3"
        r.mod_dir = r.two_dir
        r.three_authority = "LIVE"
        r.module_authority = "ACTIVE"
        r.active_function = "3"
        r.phase = "THREE_LIVE"
        r.ev(t, "MODULE_1_2_3_CONFIRMED",
             f"origin={r.mod_origin} extreme={r.mod_extreme} size={r.mod_size}; "
             f"extremo de 3 vivo")

    # ----------------------------------------------- loop
    def run(self) -> "DirectAutReader":
        r = self.reading
        for t in self.ticks:
            n_events = len(r.events)
            new_bar_item: bool = t.bar != self.cur_bar
            if new_bar_item:
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
            elif r.phase == "NEW_ONE_ACTIVE":
                self._on_new_one_tick(t)
            else:
                r.phase = INPUTS_HANDLER
                self._on_special_handlers(t)

            self.events.extend(r.events[n_events:])
            self.trace.append(self._snapshot(t))

        n_events = len(r.events)
        self._finalize()
        self.events.extend(r.events[n_events:])
        return self

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

    def _finalize(self) -> None:
        r = self.reading
        r.ev(Tick(-1, self.last_time, self.cur_bar, self.last_price), "CORE_END",
             f"phase={r.phase}; CORE + BG_AUT + DIRECT_AUT")

    def summary(self) -> dict:
        r = self.reading
        last_tick = self.ticks[-1].seq if self.ticks else -1
        return {
            "reader": CORE_VERSION,
            "reading_id": r.reading_id,
            "ticks": len(self.ticks),
            "phase": r.phase,
            "one": {"dir": r.one_dir, "origin": r.one_origin,
                    "extreme": r.one_extreme, "size": r.one_size,
                    "status": r.one_status},
            "two": {"origin": r.two_origin, "extreme": r.two_extreme,
                    "size": r.two_size, "status": r.two_status,
                    "seen_dir": r.two_seen_dir},
            "three": {"extreme": r.three_extreme, "status": r.three_status,
                      "kt": _hhmm(r.three_kt) if r.three_kt else ""},
            "mod_status": "CORE" if r.phase == "CORE_WAIT_THREE_A_NOT_IMPLEMENTED"
                          else r.mod_status,
            "mod_owner": r.mod_owner,
            "a": {"status": r.a_status, "dir": r.a_dir,
                  "origin": r.a_origin, "extreme": r.a_extreme,
                  "size": r.a_size,
                  "structural_time": _hhmm(r.a_origin_st) if r.a_origin_st else "",
                  "knowledge_time": _hhmm(r.a_kt) if r.a_kt else "",
                  "confirmations": r.a_confirmations,
                  "aut_direct": r.aut_direct_status,
                  "aut_direct_kt": _hhmm(r.aut_direct_kt) if r.aut_direct_kt else "",
                  "authority": r.a_authority},
            "a_storage": {"status": r.a_status, "dir": r.a_dir,
                          "origin": r.a_origin, "extreme": r.a_extreme,
                          "size": r.a_size,
                          "structural_time": _hhmm(r.a_origin_st) if r.a_origin_st else "",
                          "knowledge_time": _hhmm(r.a_kt) if r.a_kt else "",
                          "confirmations": r.a_confirmations,
                          "authority": r.a_authority},
            "b": {"status": r.b_status, "dir": r.b_dir,
                  "origin": r.b_origin, "extreme": r.b_extreme, "size": r.b_size,
                  "structural_time": _hhmm(r.b_st) if r.b_st else "",
                  "knowledge_time": _hhmm(r.b_kt) if r.b_kt else "",
                  "grande_status": r.b_grande_status,
                  "grande_knowledge_time": _hhmm(r.b_grande_kt) if r.b_grande_kt else "",
                  "aut_status": r.aut_status,
                  "aut_knowledge_time": _hhmm(r.aut_kt) if r.aut_kt else "",
                  "aut_price": r.aut_price},
            "b_storage": {"status": r.b_status,
                          "dir": r.b_dir,
                          "origin": r.b_origin,
                          "extreme": r.b_extreme,
                          "size": r.b_size,
                          "structural_time": _hhmm(r.b_st) if r.b_st else "",
                          "knowledge_time": _hhmm(r.b_kt) if r.b_kt else "",
                          "grande_status": r.b_grande_status,
                          "grande_knowledge_time": _hhmm(r.b_grande_kt) if r.b_grande_kt else "",
                          "aut_status": r.aut_status,
                          "aut_knowledge_time": _hhmm(r.aut_kt) if r.aut_kt else "",
                          "aut_price": r.aut_price},
            "return_status": r.return_status,
            "three_authority": r.three_authority,
            "module_authority": r.module_authority,
            "mod_size": r.mod_size,
            "mod_origin": r.mod_origin,
            "n_origin": r.n_origin,
            "n_dir": r.n_dir,
            "n_size": r.n_size,
            "origin": {"origin": r.n_origin, "extreme": r.n_extreme,
                       "size": r.n_size,
                       "structural_time": _hhmm(r.n_st) if r.n_st else "",
                       "knowledge_time": _hhmm(r.n_kt) if r.n_kt else "",
                       "active_function": r.active_function,
                       "authority": r.module_authority},
            "n_dir_activation": r.n_dir,
            "active_function": r.active_function,
            "authority": {"a": r.a_authority, "three": r.three_authority,
                          "module": r.module_authority,
                          "n_authority": r.n_authority,
                          "b_authority": r.b_authority},
            "aut_direct": r.aut_direct_status,
            "aut_direct_knowledge": _hhmm(r.aut_direct_kt) if r.aut_direct_kt else "",
            "aut_direct_extreme": r.n_extreme,
            "new_one_status": r.new_one_status,
            "new_one_active_function": r.active_function,
            "new_one_extreme": r.n_extreme,
            "n_size_real": r.n_size,
            "origin_storage": {"origin": r.n_origin, "dir": r.n_dir, "size": r.n_size,
                               "zt": r.n_st, "kt": r.n_kt,
                               "extreme_st": r.n_extreme_st,
                               "structural_time": _hhmm(r.n_st) if r.n_st else "",
                               "knowledge_time": _hhmm(r.n_kt) if r.n_kt else ""},
            "n_extreme_st_real": r.n_extreme_st,
            "n_extreme_real": r.n_extreme,
            "eventual_cross_source": "B_GRANDE" if r.n_size >= r.b_size else "AUTO",
        }


def _hhmm(ms: int) -> str:
    if not ms:
        return ""
    total = ms // 1000
    hh = (total // 3600) % 24
    mm = (total // 60) % 60
    ss = total % 60  # segundos completos
    return f"{hh:02d}:{mm:02d}:{ss:02d}.{ms % 1000:03d}"


def _price(s: str) -> int:
    return int(round(float(s) * 100))


def load_ticks(path: Path) -> list[Tick]:
    out: list[Tick] = []
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
    rd = DirectAutReader(ticks, reading_id=args.reading_id).run()

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
