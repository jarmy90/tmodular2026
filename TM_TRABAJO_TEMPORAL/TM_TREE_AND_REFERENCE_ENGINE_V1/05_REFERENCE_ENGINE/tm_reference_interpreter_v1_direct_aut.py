"""TM REFERENCE INTERPRETER V1 — baseline Iteracion 16.

ESTADO DECLARADO (Iteracion 16; no es motor oficial):

IMPLEMENTADO_CANONICO
  * lectura con propietario, 1, apertura plano/gap, 2 candidata/confirmada/
    imposible, modulo por descarte, 3 pendiente/confirmada/imposible,
    modulo 1+2+3, extremo vivo de 3.
  * A Grande, B candidata, B Grande (100 % .. 127 % + 0,25), AUT por B.
  * AUT directo por A con precondicion A_CONFIRMED.
  * C Grande, CUT, C usada como tendencia.
  * gap implicito con nuevo 1 desde la apertura.
  * TT (posible/pendiente/confirmado/extendido/fallido) y reset tras TT.
  * FT estructural (origen en extremo real del TT, capa de patrones).
  * lectura local por AUT directo (aislamiento de referencias).

IMPLEMENTADO_PROVISIONAL
  * autonomia del retorno por extension de extremo propio.
  * proporcion interna del 35 % (PROVISIONAL_INTERNAL_RATIO): orientativa,
    no frontera canonica; aislada como constante configurable.

OPEN_RULE_BLOCK
  * descubrimiento automatico general de lecturas concurrentes (solo existe
    el disparador canonico AUT directo -> nuevo 1 local).
  * arbitraje formal FT vs nuevas funciones cuando no hay regla escrita.

NO_IMPLEMENTADO
  * variables operativas, ejecucion de ordenes, motor oficial.

The interpreter is deterministic and has no future information: every
transition is evaluated from the current tick and the state built so far.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
# TM_FEED permite verificar el paquete extraido sin copiar el tickfeed dentro
# del ZIP. No cambia ninguna regla: solo la ubicacion del archivo de ticks.
FEED = Path(os.environ.get("TM_FEED")
            or (ROOT / "TM_CANON_ACTIVO" / "02_TICKS" / "TM_TICKFEED_1615_1730.csv"))

PLANO = 25       # 0.25 in cents
NOISE = 200      # 2.00 points: physical noise filter
CORE_VERSION = "TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT"
RETURN_MIN = NOISE  # filtro fisico de ruido; nunca autonomia por si solo
# PROVISIONAL_POLICY: referencia orientativa v2.16, NO frontera canonica.
# Aislada para que ninguna prueba que dependa de ella sea CANONICAL_PASS.
PROVISIONAL_INTERNAL_RATIO = 35  # %

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

    aut_mod_origin: int = 0
    aut_mod_origin_st: int = 0
    aut_mod_extreme: int = 0
    aut_mod_dir: int = 0
    aut_mod_size: int = 0
    a_dominant: int = 0

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

    # TT (v2.6/v2.7): objetivo = final_A +/- tamano_modulo; arbitro cronologico
    tt_status: str = ""
    tt_dir: int = 0
    tt_objective: int = 0
    tt_final_a: int = 0
    tt_a_size: int = 0
    tt_aut_price: int = 0
    tt_aut_kt: int = 0
    tt_kt: int = 0
    tt_extreme: int = 0
    tt_overshoot: int = 0
    tt_ambiguous: bool = False

    # CUT: condicion cerrada (C supera el final real de A); reset pendiente
    cut_status: str = ""
    cut_kt: int = 0
    cut_price: int = 0

    # Iteracion 12: reinicio real del ciclo tras TT y capa de patrones FT
    cycle_id: int = 0
    a_absorbed_from: int = 0
    tt_cycle_closed: bool = False
    # cierre causal (tick TT) vs rotacion administrativa (apertura siguiente)
    cycle_closed_at_tt: int = 0
    cycle_rotation_committed_at: int = 0
    cycle_rotation_via: str = ""
    prev_cycle: dict = field(default_factory=dict)
    ft_status: str = ""
    ft_dir: int = 0
    ft_origin: int = 0
    ft_st: int = 0
    ft_kt: int = 0
    ft_extreme: int = 0
    ft_size: int = 0
    ft_tt_extreme: int = 0

    new_one_status: str = ""
    n_origin: int = 0
    n_origin_st: int = 0
    n_bar: int = -1
    a_origin_reason: str = ""
    tt_archived: bool = False
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
    def __init__(self, ticks: list[Tick], reading_id: str = "L1",
                 local_mode: bool = False, local_probe: bool = False,
                 tt_keep_first_pending: bool = False,
                 tt_no_invalidate: bool = False):
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
        self.prev_price = 0
        self._finished = False
        # Lectura local secundaria (Iteracion 14). No modifica la principal:
        # solo cambia el umbral de AUT por B al 100 % del origen de A, que es
        # la jerarquia local 1-2-3/AUT documentada en el motor canonico.
        self.local_mode = local_mode
        # Lectura local secundaria: se activa explicitamente por el llamador.
        self.local_probe = local_probe
        # Iteracion 17: politica de propiedad del TT en una lectura local.
        # Un TT pendiente pertenece a su lectura y no se sustituye por un AUT
        # posterior de la misma lectura; la invalidacion por final_A puede
        # desactivarse cuando la lectura local conserva su TT vivo (v005 16:24).
        self.tt_keep_first_pending = tt_keep_first_pending
        self.tt_no_invalidate = tt_no_invalidate
        self.shadow: "Reader | None" = None
        self.l2: "Reader | None" = None
        self.l2_declared_at = 0

    # ------------------------------------------------------------- bar helpers
    def _confirm_one_at_close(self, bar: int, price: int, time_ms: int) -> None:
        """Q-ONE-AT-CLOSE: el 1 queda delimitado, medido y confirmado al
        cerrar su propia vela. El primer tick de la vela siguiente NO confirma.

        structural_time_1 = inicio del movimiento (one_st)
        extreme_time_1    = tick del extremo (one_extreme_st)
        knowledge_time_1  = ultimo tick/cierre efectivo de su vela
        """
        r = self.reading
        if r.one_status != "CANDIDATE" or r.one_bar != bar:
            return
        b = self.bars[bar]
        d = 1 if b["c"] > b["o"] else (-1 if b["c"] < b["o"] else 0)
        if d == 0:
            d = 1 if b["c"] >= b["o"] else -1
        r.one_dir = d
        r.one_origin = b["h"] if d < 0 else b["l"]
        r.one_extreme = b["l"] if d < 0 else b["h"]
        r.one_size = abs(r.one_extreme - r.one_origin)
        r.one_extreme_st = (b.get("l_t") if d < 0 else b.get("h_t")) or time_ms
        r.one_status = "CONFIRMED"
        r.one_kt = time_ms
        r.phase = "WAIT_OPENING"
        r.ev(Tick(-1, time_ms, bar, price), "ONE_CONFIRMED_AT_CLOSE",
             f"dir={d} origin={r.one_origin} extreme={r.one_extreme} "
             f"size={r.one_size} knowledge_time=cierre de vela")

    def _confirm_initial_one(self, t: Tick) -> None:
        r = self.reading
        if r.one_status == "CONFIRMED":
            return
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
            # v2.19: el gap NO se mide como una unica A desde el extremo previo.
            # En el tramo implicito se consideran A Grande, B Grande y A usada
            # como tendencia; la apertura fija el origen del nuevo 1. No se
            # inventan precios internos ni ticks intermedios.
            d = 1 if gap > 0 else -1
            r.ev(t, "GAP_IMPLICIT_SEQUENCE",
                 "A Grande implicita -> B Grande implicita -> A usada como "
                 "tendencia implicita; sin precios internos inventados")
            for name, status in (("three", r.three_status),
                                 ("a", r.a_status), ("b", r.b_status),
                                 ("c", r.c_status)):
                if status:
                    if name == "three":
                        r.three_authority = "ARCHIVED"
                    elif name == "a":
                        r.a_authority = "ARCHIVED"
                    elif name == "b":
                        r.b_authority = "ARCHIVED"
                    else:
                        r.c_authority = "ARCHIVED"
            if r.mod_origin:
                r.module_authority = "FROZEN_REFERENCE"
            r.new_one_status = "NEW_ONE_ACTIVE"
            r.n_origin = t.price
            r.n_origin_st = t.time_ms
            r.n_bar = t.bar
            r.n_dir = d
            r.n_st = t.time_ms
            r.n_kt = t.time_ms
            r.n_extreme = t.price
            r.n_extreme_st = t.time_ms
            r.n_size = 0
            r.active_function = "NEW_ONE"
            r.phase = "NEW_ONE_ACTIVE"
            r.transition_reason = "GAP_IMPLICIT_A_B_TREND"
            r.ev(t, "GAP_IMPLICIT_NEW_ONE",
                 f"origen operativo = OPEN {t.price} dir={d} "
                 f"structural_time=knowledge_time={_hhmm(t.time_ms)}")
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
    def _on_a_absorbed_tick(self, t: Tick) -> None:
        """Tras absorber A, la funcion dominante manda.

        El modulo sigue vivo y actualiza su extremo. La pregunta por un nuevo
        recorrido contrario se reabre solo cuando el precio retrocede desde un
        extremo distinto del que absorbio a la candidata anterior (evita
        reabrir en bucle sobre el mismo extremo).
        """
        r = self.reading
        d = r.mod_dir or r.one_dir
        if (t.price - r.mod_extreme) * d > 0:
            r.mod_extreme = t.price
            r.mod_extreme_st = t.time_ms
            r.mod_size = abs(r.mod_extreme - r.mod_origin)
            r.ev(t, "MODULE_EXTENDED_AFTER_ABSORPTION",
                 f"module_extreme={r.mod_extreme} size={r.mod_size}")
            return
        disp = (r.mod_extreme - t.price) * d
        if disp >= NOISE and r.mod_extreme != r.a_absorbed_from:
            self._open_contrary(t, r.mod_extreme, r.mod_extreme_st,
                                "A_ABSORBED_REOPEN")

    def _open_contrary(self, t: Tick, extreme: int, extreme_st: int,
                       previous: str, mod_dir: int | None = None) -> None:
        r = self.reading
        r.mod_dir = mod_dir if mod_dir else r.one_dir
        r.a_status = "CONTRARY_MOVE_PENDING"
        r.a_origin_reason = previous
        # Cada A nace con su propio retorno: no se hereda el retorno, la
        # direccion ni el extremo de la A anterior (fuga de estado).
        r.return_status = ""
        r.return_dir = 0
        r.return_origin = 0
        r.return_extreme = 0
        r.return_extreme_st = 0
        r.return_size = 0
        r.return_ticks = 0
        r.return_extended = False
        r.return_jump = False
        r.return_absorbed = 0
        # El AUT directo es por estructura: cada A puede abrir su propio
        # cruce de la base del modulo del AUT.
        r.aut_direct_status = ""
        r.aut_direct_kt = 0
        r.a_dir = -r.mod_dir
        # v2.16: la proporcion de A se mide contra el movimiento dominante que
        # la origina (nuevo 1 tras AUT, o modulo 1-2-3).
        if previous.startswith("NEW_ONE") and r.n_size:
            r.a_dominant = r.n_size
        else:
            r.a_dominant = r.mod_size or r.n_size
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
        # Base funcional de la A pendiente: el modulo del ciclo o, si A nacio
        # de un AUT, el modulo integrado por ese AUT.
        base_extreme = r.aut_mod_extreme if r.aut_mod_origin else r.mod_extreme
        base_dir = r.aut_mod_dir if r.aut_mod_origin else r.mod_dir
        # Iteracion 17: una A nacida del extremo de un nuevo 1 no pertenece al
        # modulo anterior; la reanudacion de ese modulo no la absorbe ni
        # congela su extremo. Solo se evalua su propia extension y su retorno.
        if r.a_origin_reason.startswith(("MAIN_NEW_ONE", "NEW_ONE")):
            base_extreme = 0
            base_dir = 0
        # Extension del modulo/3 en su direccion: absorbe A pendiente.
        # Solo cuando A ya tiene un recorrido propio; si A aun no se ha
        # movido, el tick pertenece al cierre del modulo y no lo reescribe.
        if (r.a_size > 0 and base_dir
                and (t.price - base_extreme) * base_dir > 0):
            # A ya estructural: la reanudacion del modulo no la absorbe, la
            # completa como B (B alcanza el 100 % de A). La absorcion queda
            # reservada a oscilaciones internas que no adquieren dimension.
            if (r.a_size >= RETURN_MIN
                    and r.a_size * 100 >= r.a_dominant * PROVISIONAL_INTERNAL_RATIO):
                disp = (t.price - r.a_extreme) * (-r.a_dir)
                if disp > 0:
                    if r.return_status in ("", "ABSORBED_IN_A"):
                        r.return_status = "RETURN_MOVE_PENDING"
                        r.return_dir = -r.a_dir
                        r.return_origin = r.a_extreme
                        r.return_first_st = t.time_ms
                        r.return_first_extreme = t.price
                        r.return_extended = False
                        r.return_jump = False
                        r.return_ticks = 1
                    else:
                        r.return_ticks += 1
                        if (t.price - r.return_extreme) * r.return_dir > 0:
                            r.return_extreme = t.price
                            r.return_extreme_st = t.time_ms
                            if ((r.return_extreme - r.return_first_extreme)
                                    * r.return_dir > 0):
                                r.return_extended = True
                    r.return_extreme = t.price
                    r.return_extreme_st = t.time_ms
                    r.return_size = abs(r.return_extreme - r.a_extreme)
                    r.ev(t, "RESUMPTION_OVER_STRUCTURAL_A",
                         f"A={r.a_size} estructural; la reanudacion completa B "
                         f"(return {r.return_size})")
                    if r.a_status == "A_CONFIRMED":
                        self._open_b_from_return(t)
                    else:
                        self._confirm_a_and_open_b(t)
                    if r.phase == "B_LIVE":
                        self._on_b_candidate_tick(t)
                return
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
            r.a_absorbed_from = r.mod_extreme
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
            direct_base = r.aut_mod_origin if r.aut_mod_origin else r.mod_origin
            if (r.a_extreme - direct_base) * r.a_dir > 0:
                if r.a_confirmations == 0 and not self.local_mode:
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
                if (r.a_status == "A_CONFIRMED"
                        and r.b_status in ("", "ABSORBED_IN_A")):
                    # La A confirmada sigue viva: un nuevo retorno estructural
                    # reabre B candidata para la misma A.
                    self._open_b_from_return(t)
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
        # a_confirmations es acumulado de la lectura: el guard real es el
        # estado (una misma A no se confirma dos veces).
        if r.a_status != "CONTRARY_MOVE_PENDING":
            return
        # Lectura local (v2.16): una A que no alcanza la proporcion orientativa
        # del 35 % del movimiento dominante es desarrollo interno y no se
        # confirma; se resolvera por absorcion si el dominante se extiende.
        if (self.local_mode and r.a_dominant
                and r.a_size * 100 < r.a_dominant * PROVISIONAL_INTERNAL_RATIO):
            return
        # Iteracion 17: para una A nacida del extremo de un nuevo 1, el
        # retorno debe ser funcionalmente claro respecto de la propia A
        # (proporcion orientativa 35 %, politica provisional). Un rebote de
        # 2-3 puntos no confirma una A grande.
        if (r.a_origin_reason.startswith(("MAIN_NEW_ONE", "NEW_ONE"))
                and r.a_size
                and r.return_size * 100 < r.a_size * PROVISIONAL_INTERNAL_RATIO):
            return
        # Iteracion 16: RC-3 (exigir 35 % del retorno para confirmar A de un
        # nuevo 1) se REVIRTIO: rompia las anclas 16:23/16:24 ya validadas.
        # Se conserva la politica provisional vigente, documentada como tal.
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
        self._open_b_from_return(t)
        if r.three_status == "CONFIRMED":
            r.three_authority = "ARCHIVED"
        r.module_authority = "FROZEN_REFERENCE"
        r.ev(t, "A_CONFIRMED",
             f"origin={r.a_origin} extreme={r.a_extreme} size={r.a_size} "
             f"structural_time={_hhmm(r.a_origin_st)} knowledge_time={_hhmm(t.time_ms)}")
        r.ev(t, "B_CANDIDATE",
             f"origin={r.b_origin} dir={r.b_dir} extreme={r.b_extreme} "
             f"structural_time={_hhmm(r.b_st)} knowledge_time={_hhmm(t.time_ms)}")

    def _open_b_from_return(self, t: Tick) -> None:
        """Abre B candidata desde el retorno ya validado."""
        r = self.reading
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

        # Lectura local 1-2-3/AUT: la jerarquia local confirma AUT cuando B
        # supera estrictamente el origen de A (100 %). El umbral 127 % + 0,25
        # pertenece a la via principal y no se aplica aqui.
        if self.local_mode:
            if r.b_size > r.a_size:
                self._confirm_aut(t, local=True)
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

    def _confirm_aut(self, t: Tick, local: bool = False) -> None:
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
        r.n_bar = t.bar
        r.n_dir = r.b_dir
        r.n_st = r.b_st
        r.n_kt = t.time_ms
        r.n_extreme = t.price
        r.n_extreme_st = t.time_ms
        r.n_size = abs(r.n_extreme - r.n_origin)
        r.active_function = "NEW_ONE"
        r.phase = "NEW_ONE_ACTIVE"
        if local:
            r.ev(t, "AUT_CONFIRMED_LOCAL",
                 f"B={r.b_size} supera el origen de A={r.a_size} (100 % local); "
                 f"knowledge_time={_hhmm(t.time_ms)}")
        else:
            r.ev(t, "AUT_CONFIRMED",
                 f"B={r.b_size} > 127%+0,25 de A ({r.a_size * 127 // 100 + 25}); "
                 f"knowledge_time={_hhmm(t.time_ms)}")
        r.ev(t, "NEW_ONE_ACTIVE",
             f"origin={r.n_origin} dir={r.n_dir} structural_time={_hhmm(r.n_st)} "
             f"knowledge_time={_hhmm(r.n_kt)} extreme={r.n_extreme}")
        self._arm_tt(t, r.a_extreme)
        # El AUT queda integrado como modulo propio de la estructura siguiente
        # (base = origen del nuevo 1). El modulo del ciclo se conserva intacto
        # como referencia: el TT ya quedo armado con el y no se reescribe.
        r.aut_mod_origin = r.n_origin
        r.aut_mod_origin_st = r.n_origin_st
        r.aut_mod_extreme = r.n_extreme
        r.aut_mod_dir = r.n_dir
        r.aut_mod_size = abs(r.aut_mod_extreme - r.aut_mod_origin)

    # --------------------------------------------------------------------- TT
    def _arm_tt(self, t: Tick, final_a: int) -> None:
        """Abre TT POSIBLE en el mismo tick del AUT (v2.6 B.5).

        OBJETIVO_TT_100 = final_A +/- tamano_modulo, con el signo de la
        direccion del nuevo 1. No se inventa ningun umbral adicional.
        """
        r = self.reading
        if r.mod_size <= 0 or final_a == 0 or r.n_dir == 0:
            return
        if (self.tt_keep_first_pending and r.tt_status == "TT_PENDING"
                and not r.tt_archived):
            # El TT pendiente ya tiene propietario: no se reescribe su
            # objetivo con un AUT posterior de la misma lectura.
            return
        r.tt_status = "TT_PENDING"
        r.tt_archived = False
        r.tt_dir = r.n_dir
        r.tt_final_a = final_a
        r.tt_a_size = r.a_size
        r.tt_objective = final_a + r.n_dir * r.mod_size
        r.tt_aut_price = r.aut_price if r.aut_price else t.price
        r.tt_aut_kt = t.time_ms
        r.tt_extreme = t.price
        signo = "+" if r.n_dir > 0 else "-"
        r.ev(t, "TT_PENDING",
             f"objetivo={r.tt_objective} = final_A {final_a} {signo} "
             f"modulo {r.mod_size}; arbitro cronologico objetivo vs final_A")

    def _on_tt_tick(self, t: Tick) -> None:
        """Arbitro cronologico v2.7: primera frontera tocada tick a tick."""
        r = self.reading
        if not r.tt_status or r.tt_archived:
            return
        # extremo REAL del TT (no el precio de activacion del AUT)
        moved = False
        if (t.price - r.tt_extreme) * r.tt_dir > 0:
            r.tt_extreme = t.price
            moved = True
        reached_obj = (t.price - r.tt_objective) * r.tt_dir >= 0
        # "vuelve a final_A" exige cruce real desde el lado del TT: el tick de
        # activacion puede estar exactamente en final_A (AUT directo) y eso no
        # es un retorno.
        back_to_a = ((self.prev_price - r.tt_final_a) * r.tt_dir > 0
                     and (t.price - r.tt_final_a) * r.tt_dir <= 0)
        if r.tt_status == "TT_PENDING":
            if reached_obj and back_to_a and not self.tt_no_invalidate:
                # v2.7 E: reconstruir la direccion del salto y aplicar la
                # PRIMERA frontera geometrica cruzada desde el precio previo.
                # El objetivo TT esta siempre mas alla de final_A en la
                # direccion del TT, asi que un tick que cruza ambas cruzo
                # final_A primero.
                if self.prev_price == 0:
                    r.tt_ambiguous = True
                    r.ev(t, "TT_PENDIENTE_POR_ORDEN_INTRATICK",
                         "fuente sin precio previo: orden geometrico no "
                         "determinable; no se inventa reset")
                    return
                r.tt_status = "TT_FAILED"
                r.ev(t, "TT_FAILED_FINAL_A_FIRST",
                     f"salto unico {self.prev_price}->{t.price} cruza final_A "
                     f"{r.tt_final_a} antes que el objetivo {r.tt_objective} "
                     f"(v2.7 E, primera frontera geometrica)")
                r.ev(t, "OPEN_RULE_BLOCK",
                     "v2.7 D: recorrido anterior = modulo por descarte y retorno "
                     "= A Grande nueva; reapertura del ciclo pendiente de "
                     "Q-CYCLE-1, no se implementa por invencion")
                return
            if reached_obj:
                r.tt_status = "TT_CONFIRMED"
                r.tt_kt = t.time_ms
                r.tt_overshoot = abs(t.price - r.tt_objective)
                r.tt_cycle_closed = True
                r.cycle_closed_at_tt = t.time_ms
                r.ev(t, "TT_100_REACHED",
                     f"objetivo={r.tt_objective} alcanzado en "
                     f"{_hhmm(t.time_ms)} overshoot={r.tt_overshoot}")
                r.ev(t, "CYCLE_CLOSED_BY_TT",
                     "ciclo anterior cerrado; el movimiento que confirma y "
                     "extiende TT ES el nuevo 1 y se mantiene activo durante "
                     "el resto de su vela; la pregunta por 2 se abre al "
                     "comenzar la vela siguiente")
                return
            if back_to_a and not self.tt_no_invalidate:
                r.tt_status = "TT_FAILED"
                r.ev(t, "TT_FAILED_FINAL_A_FIRST",
                     f"final_A {r.tt_final_a} tocado antes del objetivo "
                     f"{r.tt_objective}; TT fallido (v2.7 D)")
                r.ev(t, "OPEN_RULE_BLOCK",
                     "v2.7 D: recorrido anterior = modulo por descarte y retorno "
                     "= A Grande nueva; la reapertura del ciclo depende de "
                     "Q-CYCLE-1 y no se implementa por invencion")
                return
            return
        if r.tt_status in ("TT_CONFIRMED", "TT_EXTENDED"):
            if moved:
                r.tt_status = "TT_EXTENDED"
                r.ev(t, "TT_EXTENDED",
                     f"extremo real={r.tt_extreme} "
                     f"extension={abs(r.tt_extreme - r.tt_objective)}")

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
        # CUT (v2.13 §6 / cuerpo v2.19): C Grande supera el FINAL REAL de A.
        # La condicion esta cerrada; la secuencia de reset posterior no.
        if r.cut_status != "CUT_CONFIRMED" and r.a_extreme:
            if (r.c_extreme - r.a_extreme) * r.c_dir > 0:
                r.cut_status = "CUT_CONFIRMED"
                r.cut_kt = t.time_ms
                r.cut_price = t.price
                r.ev(t, "CUT_CONFIRMED",
                     f"C={r.c_extreme} supera estrictamente el final real de A "
                     f"{r.a_extreme}; knowledge_time={_hhmm(t.time_ms)}")
                r.ev(t, "OPEN_RULE_BLOCK",
                     "reset posterior a CUT = PENDIENTE_JAVIER (v2.13 §6); "
                     "no se inventa la secuencia de reset ni el nuevo 1")
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
        r.n_bar = t.bar
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
        r.n_bar = t.bar
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
        self._arm_tt(t, r.a_extreme)
        # El AUT queda integrado como modulo propio de la estructura siguiente
        # (base = origen del nuevo 1). El modulo del ciclo se conserva intacto
        # como referencia: el TT ya quedo armado con el y no se reescribe.
        r.aut_mod_origin = r.n_origin
        r.aut_mod_origin_st = r.n_origin_st
        r.aut_mod_extreme = r.n_extreme
        r.aut_mod_dir = r.n_dir
        r.aut_mod_size = abs(r.aut_mod_extreme - r.aut_mod_origin)

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
        self._on_tt_tick(t)
        # Ciclo universal en la lectura local: el nuevo 1 dominante de la
        # lectura secundaria admite un recorrido contrario que abre A Grande
        # de su estructura siguiente al superar el ruido fisico (2 puntos).
        # En la lectura principal el mismo recorrido puede ser una estructura
        # anidada (lectura local) y no fragmenta el nuevo 1 dominante.
        if r.new_one_status == "NEW_ONE_ACTIVE" and r.n_dir:
            disp = (r.n_extreme - t.price) * r.n_dir
            # v2.16: el retroceso posterior al nuevo 1 no es A por distancia
            # fija; exige el minimo fisico y la proporcion orientativa del
            # 35 % del propio nuevo 1.
            umbral = max(RETURN_MIN, r.n_size * PROVISIONAL_INTERNAL_RATIO // 100)
            # Iteracion 16: en la lectura principal, el nuevo 1 nacido de un
            # gap desarrolla A Grande en la vela siguiente (v005 16:26). Un
            # nuevo 1 por AUT conserva la lectura local para ese desarrollo.
            if self.local_mode:
                if disp >= umbral:
                    self._open_contrary(t, r.n_extreme, r.n_extreme_st,
                                        "NEW_ONE_RETRACE", mod_dir=r.n_dir)
            elif (r.transition_reason == "GAP_IMPLICIT_A_B_TREND"
                  and t.bar > r.n_bar and disp >= umbral):
                self._open_contrary(t, r.n_extreme, r.n_extreme_st,
                                    "MAIN_NEW_ONE_RETRACE", mod_dir=r.n_dir)

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
        for t in self.ticks:
            self.feed(t)
        self._finish_stream()
        return self

    def feed(self, t: Tick) -> None:
        r = self.reading
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
                if (self.local_probe and self.cur_bar != -1
                        and not self.local_mode
                        and r.phase == "NEW_ONE_ACTIVE"
                        and self.shadow is None):
                    self.shadow = Reader([], reading_id=f"{r.reading_id}.L2",
                                         local_mode=True)
                    r.ev(t, "L2_SHADOW_CANDIDATE",
                         f"primera vela del nuevo 1 dominante "
                         f"({r.n_origin}->{r.n_extreme}); lectura local "
                         f"secundaria candidata")
            self.cur_bar = t.bar
            b = self.bars.setdefault(t.bar, {"o": t.price, "h": t.price,
                                             "l": t.price, "c": t.price})
            self._on_bar_open(t)
        else:
            b = self.bars[t.bar]
            if t.price > b["h"]:
                b["h"] = t.price
                b["h_t"] = t.time_ms
            if t.price < b["l"]:
                b["l"] = t.price
                b["l_t"] = t.time_ms
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
        elif r.phase == "A_ABSORBED":
            self._on_a_absorbed_tick(t)
        elif r.phase == "B_LIVE":
            self._on_b_candidate_tick(t)
        elif r.phase == "C_LIVE":
            self._on_c_tick(t)
        elif r.phase == "NEW_ONE_ACTIVE":
            self._on_new_one_tick(t)

        # El TT pendiente pertenece a la estructura anterior y sigue su
        # propio arbitro aunque la lectura haya abierto A del ciclo siguiente.
        if r.phase not in ("INITIAL_BAR", "NEW_ONE_ACTIVE"):
            self._on_tt_tick(t)
        if r.phase != "INITIAL_BAR":
            self._on_ft_tick(t)

        if self.shadow is not None and not self.shadow._finished:
            self.shadow.feed(t)
            if (self.l2 is None
                    and self.shadow.reading.aut_direct_status
                    == "AUT_DIRECT_BY_A"):
                self.l2 = self.shadow
                self.l2_declared_at = t.time_ms
                r.ev(t, "L2_DECLARED_BY_DIRECT_AUT",
                     f"lectura local declarada por AUT directo: nuevo 1 "
                     f"{self.l2.reading.n_origin} -> "
                     f"{self.l2.reading.n_extreme}")

        self.events.extend(r.events[n_events:])
        self.trace.append(self._snapshot(t))
        self.prev_price = t.price

    def _finish_stream(self) -> None:
        r = self.reading
        n_events = len(r.events)
        self._finalize()
        self.events.extend(r.events[n_events:])
        self._finished = True
        if self.shadow is not None and not self.shadow._finished:
            self.shadow._finish_stream()

    # ------------------------------------------------- iteracion 12: ciclo/FT
    def _archive_cycle(self, t: Tick, via: str) -> None:
        """Archiva el ciclo cerrado sin borrar la trazabilidad del TT."""
        r = self.reading
        r.prev_cycle = {
            "cycle_id": r.cycle_id,
            "module_origin": r.mod_origin, "module_extreme": r.mod_extreme,
            "module_size": r.mod_size, "module_status": r.mod_status,
            "module_dir": r.mod_dir,
            "a_origin": r.a_origin, "a_extreme": r.a_extreme,
            "a_dir": r.a_dir, "a_size": r.a_size,
            "b_origin": r.b_origin, "b_extreme": r.b_extreme,
            "b_size": r.b_size, "b_grande_status": r.b_grande_status,
            "c_origin": r.c_origin, "c_extreme": r.c_extreme,
            "c_size": r.c_size, "cut_status": r.cut_status,
            "tt_objective": r.tt_objective, "tt_extreme": r.tt_extreme,
            "tt_final_a": r.tt_final_a, "tt_a_size": r.tt_a_size,
            "tt_kt": r.tt_kt, "new_one_origin": r.n_origin,
            "new_one_extreme": r.n_extreme, "new_one_dir": r.n_dir,
        }
        r.cycle_id += 1
        # Iteracion 16 (RC-2): el TT del ciclo archivado queda CONGELADO para
        # la capa de patrones (FT) pero no sigue extendiendose ni arbitrando
        # dentro de la estructura nueva. Se conserva su objetivo/extremo para
        # trazabilidad y para FT; no se borra (rompia FT del ciclo anterior).
        r.tt_archived = True
        r.tt_cycle_closed = False
        r.cycle_rotation_committed_at = t.time_ms
        r.cycle_rotation_via = via
        r.ev(t, "CYCLE_ARCHIVED",
             f"cycle_id={r.cycle_id} via={via}; modulo "
             f"{r.prev_cycle['module_size']}, A {r.prev_cycle['a_size']}, "
             f"TT obj {r.prev_cycle['tt_objective']}, "
             f"extremo TT {r.prev_cycle['tt_extreme']}")

    def _clear_current_cycle(self) -> None:
        r = self.reading
        r.one_status = ""; r.one_dir = 0; r.one_size = 0
        r.one_origin = 0; r.one_extreme = 0
        r.two_status = ""; r.two_size = 0; r.two_extreme = 0
        r.three_status = ""; r.three_extreme = 0; r.three_size = 0
        r.mod_origin = 0; r.mod_extreme = 0; r.mod_size = 0
        r.mod_status = ""; r.mod_owner = ""; r.module_authority = ""
        r.a_status = ""; r.a_origin = 0; r.a_extreme = 0; r.a_size = 0
        r.a_confirmations = 0; r.a_authority = ""
        r.b_status = ""; r.b_grande_status = ""; r.b_size = 0
        r.b_origin = 0; r.b_extreme = 0; r.b_authority = ""
        # Iteracion 17: el B Grande del ciclo archivado no puede abrir C en la
        # estructura nueva (fuga de referencia entre ciclos).
        r.b_grande_kt = 0; r.b_flags = ""
        r.c_status = ""; r.c_size = 0; r.c_origin = 0; r.c_extreme = 0
        r.c_authority = ""; r.cut_status = ""
        r.aut_status = ""; r.aut_direct_status = ""; r.trend_status = ""
        r.transition_reason = ""
        r.gap_branch = False

    def _new_one_from_gap_open(self, t: Tick, gap: int) -> None:
        """Gap de apertura: A/B/A-tendencia implicitas y nuevo 1 desde OPEN.

        No inventa precios internos. Conserva intacto el TT heredado, de modo
        que el mismo tick puede confirmar el TT anterior y abrir el nuevo 1.
        """
        r = self.reading
        d = 1 if gap > 0 else -1
        r.ev(t, "GAP_IMPLICIT_SEQUENCE",
             "A Grande implicita -> B Grande implicita -> A usada como "
             "tendencia implicita; sin precios internos inventados")
        r.new_one_status = "NEW_ONE_ACTIVE"
        r.n_origin = t.price
        r.n_origin_st = t.time_ms
        r.n_bar = t.bar
        r.n_dir = d
        r.n_st = t.time_ms
        r.n_kt = t.time_ms
        r.n_extreme = t.price
        r.n_extreme_st = t.time_ms
        r.n_size = 0
        r.active_function = "NEW_ONE"
        r.phase = "NEW_ONE_ACTIVE"
        r.transition_reason = "GAP_IMPLICIT_A_B_TREND"
        r.ev(t, "GAP_IMPLICIT_NEW_ONE",
             f"origen operativo = OPEN {t.price} dir={d} "
             f"structural_time=knowledge_time={_hhmm(t.time_ms)}")

    def _resolve_tt_at_open(self, t: Tick) -> bool:
        """Arbitro del TT pendiente con el precio de apertura (v2.7 B).

        Devuelve True si consumio la apertura. Si el TT se confirma, el ciclo
        se archiva y la apertura con gap abre ademas un nuevo 1 (doble
        pertenencia): TT heredado confirmado + nuevo 1 desde el OPEN.
        """
        r = self.reading
        if r.phase != "NEW_ONE_ACTIVE" or r.tt_status != "TT_PENDING":
            return False
        self._on_tt_tick(t)
        if r.tt_status not in ("TT_CONFIRMED", "TT_EXTENDED"):
            return True
        r.tt_cycle_closed = True
        gap = t.price - self.prev_close
        self._archive_cycle(t, "TT")
        r.ev(t, "TT_PENDING_RESOLVED_AT_OPEN",
             f"TT heredado confirmado en la apertura {t.price}; "
             f"el TT conserva objetivo {r.tt_objective} y extremo {r.tt_extreme}")
        self._clear_current_cycle()
        if abs(gap) >= PLANO:
            r.ev(t, "DOUBLE_BELONGING_TT_AND_GAP",
                 f"mismo tick: TT heredado confirmado + nuevo 1 desde OPEN "
                 f"(gap {gap})")
            self._new_one_from_gap_open(t, gap)
        else:
            r.one_origin = r.n_origin
            r.one_origin_st = r.n_origin_st
            r.one_extreme = r.n_extreme
            r.one_extreme_st = r.n_extreme_st
            r.one_dir = r.n_dir
            r.one_size = r.n_size
            r.one_st = r.n_st
            r.one_kt = self.last_time
            r.one_status = "CONFIRMED"
            r.new_one_status = "NEW_ONE_ARCHIVED_AS_ONE"
            r.active_function = "1"
            r.phase = "WAIT_OPENING"
            self._eval_opening(t)
        return True

    def _rotate_cycle_after_tt(self, t: Tick) -> None:
        """Reinicio real del ciclo al abrir la vela siguiente al TT.

        El movimiento que confirmo y extendio TT se convierte en el 1 del ciclo
        nuevo. El ciclo cerrado se archiva COMPLETO en `prev_cycle` (modulo,
        final de A, A, B, C, TT) para que FT y la trazabilidad no pierdan nada.
        """
        r = self.reading
        if r.phase != "NEW_ONE_ACTIVE":
            return
        # v2.7 B: con TT pendiente NO se abre una estructura nueva (2/A/B/
        # modulo) hasta resolver que frontera se alcanza primero.
        if r.tt_status == "TT_PENDING":
            return
        # Iteracion 16 (RC-1): la rotacion administrativa SOLO existe cuando el
        # ciclo anterior se cerro causalmente por TT (v2.7). Un nuevo 1 que no
        # cerro TT no rota al cambiar de vela: la vela siguiente desarrolla
        # FT / A / B dentro de la misma estructura. Rotar por NEW_ONE producia
        # un nuevo 1 por vela (cascada de gaps) y borraba la lectura viva.
        # La rotacion tambien es canonica para el nuevo 1 nacido de
        # C_USED_AS_TREND (iteracion 12, decision 2). No se generaliza a
        # cualquier NEW_ONE: un nuevo 1 por AUT o por gap desarrolla FT/A en
        # la vela siguiente y solo rota cuando cierra TT.
        c_trend_rotation = r.transition_reason == "C_USED_AS_TREND"
        if not (r.tt_cycle_closed or c_trend_rotation):
            return
        via = "TT" if r.tt_cycle_closed else "C_TREND"
        if r.n_size <= 0:
            r.ev(t, "ONE_ZERO_SIZE_DEFERRAL",
                 "nuevo 1 sin medida; se difiere la pregunta por 2")
            return
        self._archive_cycle(t, via)
        r.ev(t, "CYCLE_RESET_AFTER_NEW_ONE",
             f"cycle_id={r.cycle_id} via={via}; ciclo {r.cycle_id - 1} "
             f"archivado (modulo {r.prev_cycle['module_size']}, "
             f"A {r.prev_cycle['a_size']}, C {r.prev_cycle['c_size']}, "
             f"TT obj {r.prev_cycle['tt_objective']}, "
             f"extremo TT {r.prev_cycle['tt_extreme']})")

        # limpiar el ciclo actual conservando prev_cycle y tt_*
        self._clear_current_cycle()

        # el nuevo 1 pasa a ser el 1 del ciclo nuevo
        r.one_origin = r.n_origin
        r.one_origin_st = r.n_origin_st
        r.one_extreme = r.n_extreme
        r.one_extreme_st = r.n_extreme_st
        r.one_dir = r.n_dir
        r.one_size = r.n_size
        r.one_st = r.n_st
        r.one_kt = self.last_time          # conocimiento al cierre de su vela
        r.one_status = "CONFIRMED"
        r.new_one_status = "NEW_ONE_ARCHIVED_AS_ONE"
        r.active_function = "1"
        r.ev(t, "NEW_ONE_BECOMES_ONE",
             f"1 nuevo: origin={r.one_origin} extreme={r.one_extreme} "
             f"dir={r.one_dir} size={r.one_size}")
        r.phase = "WAIT_OPENING"
        self._eval_opening(t)

    def _on_ft_tick(self, t: Tick) -> None:
        """Capa de patrones FT (estructural, independiente de variables).

        FT nace del EXTREMO REAL del TT ya confirmado, nunca del nivel del
        100 %. El filtro de 2 puntos solo separa ruido fisico de movimiento
        estructural minimo; no sustituye la evaluacion funcional, por eso la
        confirmacion se clasifica PROVISIONAL_POLICY_PASS.
        """
        r = self.reading
        if r.tt_status not in ("TT_CONFIRMED", "TT_EXTENDED") or not r.tt_extreme:
            return
        if (t.price - r.tt_extreme) * (-r.tt_dir) <= 0:
            return
        if not r.ft_status:
            r.ft_status = "FT_POSSIBLE"
            r.ft_origin = r.tt_extreme
            r.ft_dir = -r.tt_dir
            r.ft_st = t.time_ms
            r.ft_extreme = t.price
            r.ft_size = abs(r.ft_extreme - r.ft_origin)
            r.ft_tt_extreme = r.tt_extreme
            r.ev(t, "FT_POSSIBLE",
                 f"origen = extremo real del TT {r.tt_extreme} "
                 f"(no nivel 100 % {r.tt_objective}); dir={r.ft_dir} "
                 f"st={_hhmm(t.time_ms)}")
            return
        if (t.price - r.ft_extreme) * r.ft_dir > 0:
            r.ft_extreme = t.price
            r.ft_size = abs(r.ft_extreme - r.ft_origin)
            if r.ft_status == "FT_POSSIBLE" and r.ft_size >= NOISE:
                r.ft_status = "FT_CONFIRMED"
                r.ft_kt = t.time_ms
                r.ev(t, "FT_STRUCTURAL_CONFIRMED",
                     f"recorrido contrario claro desde el extremo real del TT: "
                     f"origen={r.ft_origin} extreme={r.ft_extreme} "
                     f"size={r.ft_size}; extremo TT origen={r.ft_tt_extreme}; "
                     f"kt={_hhmm(t.time_ms)} (PROVISIONAL_POLICY_PASS)")
            elif r.ft_status in ("FT_CONFIRMED", "FT_EXTENDED"):
                r.ft_status = "FT_EXTENDED"
                r.ev(t, "FT_EXTENDED",
                     f"extremo FT={r.ft_extreme} size={r.ft_size}")

    def _on_bar_open(self, t: Tick) -> None:
        r = self.reading
        if r.phase == "NEW_ONE_ACTIVE":
            if self._resolve_tt_at_open(t):
                return
            self._rotate_cycle_after_tt(t)
            return
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
            if r.phase == "WAIT_OPENING":
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
            r.ev(Tick(-1, time_ms, bar, price), "INITIAL_BAR_CLOSED", f"close={price}")
            self._confirm_one_at_close(bar, price, time_ms)
            return
        if r.phase == "ONE_LIVE":
            # el 1 se confirma al cierre de su propia vela (Q-ONE-AT-CLOSE)
            self._confirm_one_at_close(bar, price, time_ms)
            return
        if r.phase == "TWO_LIVE" and r.two_status == "CONFIRMED":
            # v2.13/v2.14: la 2 confirmada pertenece a su vela. Al cerrar se
            # congela su extremo final; la vela siguiente desarrolla 3 desde
            # ese extremo. No se extiende 2 con ticks de la vela siguiente.
            r.phase = "WAIT_THREE"
            r.two_kt = time_ms
            r.ev(Tick(-1, time_ms, bar, price), "TWO_FROZEN_AT_CLOSE",
                 f"extremo final de 2={r.two_extreme} size={r.two_size}; "
                 f"la vela siguiente desarrolla 3")
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
            "tt_status": r.tt_status, "tt_objective": r.tt_objective,
            "ft_status": r.ft_status, "ft_origin": r.ft_origin,
            "ft_dir": r.ft_dir, "ft_extreme": r.ft_extreme,
            "cut_status": r.cut_status,
            "c_status": r.c_status, "c_extreme": r.c_extreme,
            "trend_status": r.trend_status,
            "transition_reason": r.transition_reason,
            "n_origin": r.n_origin, "n_extreme": r.n_extreme,
            "n_size": r.n_size, "active_function": r.active_function,
            "cycle_id": r.cycle_id,
            "a_kt": _hhmm(r.a_kt) if r.a_kt else "",
            "a_origin_st": _hhmm(r.a_origin_st) if r.a_origin_st else "",
            "n_kt": _hhmm(r.n_kt) if r.n_kt else "",
            "aut_direct_kt": _hhmm(r.aut_direct_kt) if r.aut_direct_kt else "",
            "tt_kt": _hhmm(r.tt_kt) if r.tt_kt else "",
            "tt_final_a": r.tt_final_a,
            "one_kt": _hhmm(r.one_kt) if r.one_kt else "",
            "l2_status": ("L2_DECLARED" if self.l2 else
                          ("L2_SHADOW" if self.shadow else "")),
            "l2_phase": (self.l2.reading.phase if self.l2 else
                         (self.shadow.reading.phase if self.shadow else "")),
            "l2_module": (self.l2.reading.mod_size if self.l2 else
                          (self.shadow.reading.mod_size if self.shadow else 0)),
            "l2_a": ((f"{self.l2.reading.a_status}/{self.l2.reading.a_size}"
                      f"@{self.l2.reading.a_origin}") if self.l2 else
                     ((f"{self.shadow.reading.a_status}/{self.shadow.reading.a_size}"
                       f"@{self.shadow.reading.a_origin}") if self.shadow else "")),
            "l2_b": ((f"{self.l2.reading.b_status}/{self.l2.reading.b_size}")
                     if self.l2 else ""),
            "l2_aut": ((f"{self.l2.reading.aut_status}"
                        f"/{self.l2.reading.aut_direct_status}") if self.l2 else ""),
            "l2_new_one": ((f"{self.l2.reading.new_one_status}"
                            f"@{self.l2.reading.n_origin}->"
                            f"{self.l2.reading.n_extreme}"
                            f"/dir={self.l2.reading.n_dir}") if self.l2 else ""),
            "l2_events": [e for e in (self.l2.reading.events if self.l2 else [])
                          if e["seq"] == t.seq],
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
            "tt": {"status": r.tt_status, "dir": r.tt_dir,
                   "objective": r.tt_objective, "final_a": r.tt_final_a,
                   "extreme": r.tt_extreme,
                   "knowledge_time": _hhmm(r.tt_kt) if r.tt_kt else "",
                   "cycle_closed": r.tt_cycle_closed},
            "cycle_id": r.cycle_id,
            "cycle_closure": {
                "closed_at_tt": _hhmm(r.cycle_closed_at_tt) if r.cycle_closed_at_tt else "",
                "rotation_committed_at":
                    _hhmm(r.cycle_rotation_committed_at) if r.cycle_rotation_committed_at else "",
                "rotation_via": r.cycle_rotation_via,
            },
            "ft": {"status": r.ft_status, "dir": r.ft_dir,
                   "origin": r.ft_origin, "extreme": r.ft_extreme,
                   "size": r.ft_size,
                   "tt_extreme_origen": r.ft_tt_extreme,
                   "structural_time": _hhmm(r.ft_st) if r.ft_st else "",
                   "knowledge_time": _hhmm(r.ft_kt) if r.ft_kt else ""},
            "prev_cycle": r.prev_cycle,
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
