#!/usr/bin/env python3
"""ITERACION 19B — gestor de lecturas TM con generaciones y patrones.

Arquitectura
------------
  * L1: lectura principal, arranca con el primer tick del feed.
  * L2: lectura local opcional, descubierta causalmente por el propio motor.
  * Maximo dos escalas activas. Archivo historico de lecturas cerradas.

Iteracion 19B (relevo generacional)
-----------------------------------
  * El TT confirma en un tick, pero su EXTREMO FISICO puede seguir subiendo.
  * FT nace del extremo FUNCIONAL, no del primer retroceso: si el TT supera
    el extremo desde el que nacio el candidato, el retroceso era interno y el
    candidato queda ABSORBIDO (ver Reader._absorb_ft).
  * LOCAL-G1 pasa a CLOSING cuando el extremo funcional de su TT se conoce
    (FT_STRUCTURAL_CONFIRMED = filtro fisico de 2 puntos, PROVISIONAL).
  * Al abrir la vela siguiente se ARCHIVA la generacion y se libera el slot.
  * El patron FT sigue vivo despues del archivo: la lectura local pasa a
    `pattern_only` y no crea funciones nuevas.
  * LOCAL-G2 NO se abre en 16:26: la continuacion local hereda `one` de
    LOCAL-G1 y no forma modulo por descarte. Decision auditada, no forzada.

El gestor nunca copia module_size, final_A, TT, A, B, C ni extremos entre
lecturas. Cada TT tiene propietario (reading_id + generation_id).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from tm_reference_interpreter_v1_direct_aut import (  # noqa: E402
    NOISE, PLANO, Reader, Tick, load_ticks, FEED,
)

ARCHIVE_LIMIT = 8


@dataclass
class PatternRecord:
    """Patron con identidad propia (TT o FT).

    El precio nunca es la identidad: el id es causal (generacion + tipo +
    ordinal). Los precios viven en campos.
    """
    pattern_id: str
    pattern_type: str
    owner_generation_id: str
    owner_slot: str
    status: str
    objective: int = 0
    confirmed_price: int = 0
    confirmed_at_seq: int = 0
    physical_extreme: int = 0
    physical_extreme_seq: int = 0
    physical_extreme_st: int = 0
    functional_extreme: int = 0
    functional_extreme_seq: int = 0
    functional_extreme_status: str = ""
    functional_extreme_knowledge_seq: int = 0
    structural_time: int = 0
    knowledge_time: int = 0
    opened_at_seq: int = 0
    closed_at_seq: int = 0
    derived_pattern_ids: list[str] = field(default_factory=list)
    authority: str = "CANONICAL"


@dataclass
class GenerationRecord:
    generation_id: str
    slot: str
    status: str = "ACTIVE"
    opened_at_seq: int = 0
    opened_by_event: str = ""
    functional_closure_at_seq: int = 0
    pattern_window_closed_at_seq: int = 0
    closed_at_seq: int = 0
    close_reason: str = ""
    active_pattern_ids: list[str] = field(default_factory=list)
    historical_pattern_ids: list[str] = field(default_factory=list)


@dataclass
class ReadingSlotState:
    slot_id: str
    active_generation_id: str = ""


class TMReadingManager:
    def __init__(self, ticks: list[Tick], discover_l2: bool = True,
                 archive_local: bool = True, freeze_on_closure: bool = True):
        self.ticks = ticks
        self.discover_l2 = discover_l2
        self.archive_local = archive_local
        # Sonda de continuacion: permite ver que haria el lector local sin
        # congelar funciones al entrar en CLOSING. No altera el motor real.
        self.freeze_on_closure = freeze_on_closure
        self.l1 = Reader([], reading_id="L1")
        self.l2: Reader | None = None
        self.archive: list[dict] = []
        self.l2_discovered_at_seq: int = 0
        self.l2_seed_bar: int = -1
        self.l2_discovery_rule: str = ""
        self.generations: list[dict] = []
        self.tt_records: list[dict] = []
        self.gen_records: list[GenerationRecord] = [
            GenerationRecord("PRIMARY-G1", "PRIMARY", opened_at_seq=0)]
        self.pattern_records: list[PatternRecord] = []
        self.slots: dict[str, ReadingSlotState] = {
            "PRIMARY": ReadingSlotState("PRIMARY", "PRIMARY-G1"),
            "LOCAL": ReadingSlotState("LOCAL", ""),
        }
        self.l2_generation = 0
        self.l2_archived = False
        self._tt_confirmed_bar = -1
        self.archived_generation_writes = 0
        self.cur_bar = -1
        self.by_bar: dict[int, list[Tick]] = {}
        self.rows: list[dict] = []
        self.seq_of: dict[int, int] = {t.time_ms: t.seq for t in ticks}
        self.local_g2_decision: dict = {
            "decision": "NOT_OPENED",
            "scene": "FUNCTION_AND_FT_EXPLAIN_16_26",
            "reason": "pendiente de evaluar",
            "evidence": [],
            "authority": "CANONICAL",
        }

    # ------------------------------------------------------------------ L2
    def _maybe_discover_l2(self, prev_bar: int) -> None:
        if not self.discover_l2 or self.l2 is not None:
            return
        l1 = self.l1.reading
        if l1.tt_status != "TT_PENDING" or l1.tt_archived:
            return
        if not l1.n_dir:
            return
        bar = self.l1.bars.get(prev_bar)
        if not bar or not l1.n_origin:
            return
        if prev_bar == l1.n_bar:
            # La vela de nacimiento del nuevo 1 no puede ser su propio 1 local.
            return
        rng = bar["h"] - bar["l"]
        if rng < NOISE:
            return
        # Corredor del TT pendiente: la vela local queda por dentro del origen
        # del nuevo 1 y por fuera del objetivo TT (aun no lo alcanza).
        if l1.n_dir < 0:
            inside = bar["h"] < l1.n_origin and bar["l"] > l1.tt_objective
        else:
            inside = bar["l"] > l1.n_origin and bar["h"] < l1.tt_objective
        if not inside:
            return
        seed = list(self.by_bar.get(prev_bar, []))
        if not seed:
            return
        # El 1 local se mide desde el extremo direccional de la vela (maximo
        # para bajista, minimo para alcista), no desde la primera impresion.
        if l1.n_dir < 0:
            extreme = max(t.price for t in seed)
            idx = next(i for i, t in enumerate(seed) if t.price == extreme)
        else:
            extreme = min(t.price for t in seed)
            idx = next(i for i, t in enumerate(seed) if t.price == extreme)
        seed = seed[idx:]
        l2 = Reader([], reading_id="L2", local_mode=True,
                    tt_keep_first_pending=True, tt_no_invalidate=True)
        for tick in seed:
            l2.feed(tick)
        l2.reading.ev(seed[-1], "L2_DISCOVERED_BY_LOCAL_ONE",
                      f"vela {prev_bar % 1440 // 60:02d}:{prev_bar % 1440 % 60:02d} "
                      f"rango={rng} direccion={l1.n_dir} "
                      f"mientras L1 mantiene TT pendiente "
                      f"objetivo={l1.tt_objective}")
        self.l2 = l2
        self.l2_generation = 1
        gen = GenerationRecord("LOCAL-G1", "LOCAL", opened_at_seq=seed[0].seq,
                               opened_by_event="LOCAL_ONE_DISCOVERED")
        self.gen_records.append(gen)
        self.slots["LOCAL"].active_generation_id = "LOCAL-G1"
        self.l2_discovered_at_seq = seed[-1].seq
        self.l2_seed_bar = prev_bar
        self.l2_discovery_rule = (
            "TT pendiente en L1 + vela cerrada con rango >= 2,0 en la "
            "direccion del nuevo 1 de L1")

    # ------------------------------------------------------------------ feed
    def feed(self, t: Tick) -> None:
        new_bar = t.bar != self.cur_bar
        if new_bar:
            if self.cur_bar != -1:
                self._maybe_discover_l2(self.cur_bar)
            # Iteracion 19B: el archivo se decide ANTES de procesar la vela
            # nueva. Una generacion archivada no puede crear funciones en ella.
            self._maybe_archive_local_at_open(t)
            self.cur_bar = t.bar
        self.by_bar.setdefault(t.bar, []).append(t)
        self.l1.feed(t)
        if self.l2 is not None:
            before = self._function_fingerprint()
            self.l2.feed(t)
            if self.l2_archived:
                if self._function_fingerprint() != before:
                    self.archived_generation_writes += 1
            else:
                self._sync_local_lifecycle(t)
        self._record_identity(t)
        self.rows.append(self.snapshot(t))

    def run(self) -> "TMReadingManager":
        for t in self.ticks:
            self.feed(t)
        self.l2_finalized = self.l2 is not None
        self._close_local_g2_decision()
        return self

    def _tt_id(self, slot: str, gen: int, objective: int) -> str:
        return f"{slot}-G{gen}-TT-{objective}"

    def _record_identity(self, t: Tick) -> None:
        for slot, reader, gen in ((
                "PRIMARY", self.l1, 1),
                ("LOCAL", self.l2, 1 if self.l2 else 0)):
            if reader is None:
                continue
            r = reader.reading
            gid = f"{slot}-G{gen}"
            if not any(g["generation_id"] == gid for g in self.generations):
                self.generations.append({
                    "generation_id": gid, "slot": slot, "opened_at": t.time_ms,
                    "status": "ACTIVE", "functional_closure_at_seq": 0,
                    "closed_at": 0, "closed_at_seq": 0, "close_reason": "",
                    "owner_module": r.mod_size, "n_origin": r.n_origin})
            if r.tt_objective:
                key = (gid, r.tt_objective)
                if not any((x["owner_generation"], x["objective"]) == key
                           for x in self.tt_records):
                    self.tt_records.append({
                        "tt_id": self._tt_id(slot, gen, r.tt_objective),
                        "owner_slot": slot, "owner_generation": gid,
                        "module_id": f"{gid}-MOD-{r.mod_size}",
                        "module_size": r.mod_size,
                        "final_A": r.tt_final_a, "objective": r.tt_objective,
                        "direction": r.tt_dir, "status": r.tt_status,
                        "pattern_status": "ACTIVE",
                        "confirmed_price": 0, "physical_extreme": 0,
                        "functional_extreme": 0,
                        "functional_extreme_knowledge_seq": 0,
                        "confirmed_at": 0,
                        "opened_at": t.time_ms, "closed_at": 0,
                        "invalidation_rule": ("final_A_cruce"
                                               if not self.l2 else
                                               "solo_objetivo_local")})
                else:
                    rec = next(x for x in self.tt_records
                               if (x["owner_generation"], x["objective"]) == key)
                    rec["status"] = r.tt_status
                    if r.tt_status in ("TT_CONFIRMED", "TT_EXTENDED", "TT_FAILED"):
                        if not rec.get("confirmed_at"):
                            rec["confirmed_at"] = t.time_ms

    def _function_fingerprint(self) -> tuple:
        if self.l2 is None:
            return ()
        r = self.l2.reading
        # Solo funciones: la capa de patrones (FT) puede seguir viva despues
        # del archivo sin ser una escritura en la generacion archivada.
        return (r.phase, r.one_origin, r.one_extreme, r.one_size, r.mod_size,
                r.mod_origin, r.a_status, r.a_origin, r.a_extreme, r.a_size,
                r.b_status, r.b_size, r.n_origin, r.n_extreme, r.n_dir,
                r.tt_status, r.tt_objective, r.tt_extreme)

    def _local_generation(self) -> GenerationRecord | None:
        for g in self.gen_records:
            if g.slot == "LOCAL" and g.status in ("ACTIVE", "CLOSING"):
                return g
        return None

    def _sync_local_lifecycle(self, t: Tick) -> None:
        """CLOSING cuando el extremo funcional del TT queda conocido.

        Si el TT vuelve a extenderse, la ventana se reabre y la generacion
        recupera ACTIVE: nunca se archiva un extremo que aun puede cambiar.
        """
        if self.l2 is None or self.l2_archived:
            return
        gen = self._local_generation()
        if gen is None:
            return
        r = self.l2.reading
        if r.tt_status not in ("TT_CONFIRMED", "TT_EXTENDED"):
            return
        if r.tt_extreme_status == "CONFIRMED" and gen.status == "ACTIVE":
            gen.status = "CLOSING"
            gen.functional_closure_at_seq = t.seq
            gen.pattern_window_closed_at_seq = t.seq
            # CLOSING congela funciones; el patron sigue vivo.
            if self.freeze_on_closure:
                self.l2.freeze_functions = True
        elif r.tt_extreme_status in ("REOPENED", "PROVISIONAL") \
                and gen.status == "CLOSING":
            gen.status = "ACTIVE"
            gen.functional_closure_at_seq = 0
            gen.pattern_window_closed_at_seq = 0
            self.l2.freeze_functions = False

    def _maybe_archive_local_at_open(self, t: Tick) -> None:
        """Archiva LOCAL-G1 al abrir la vela siguiente a su cierre funcional.

        No usa hora ni precio: solo el evento general
        TT_FUNCTIONAL_EXTREME_CONFIRMED y el propietario.
        """
        if self.l2 is None or self.l2_archived or not self.archive_local:
            return
        gen = self._local_generation()
        if gen is None or gen.status != "CLOSING":
            return
        r = self.l2.reading
        if r.tt_extreme_status != "CONFIRMED" or not r.tt_extreme_kt:
            return
        # Guarda: si la apertura supera el extremo funcional, el TT sigue
        # vivo. No se archiva un extremo que la propia apertura desmiente.
        if (t.price - r.tt_extreme) * r.tt_dir > 0:
            r.tt_extreme = t.price
            r.tt_extreme_st = t.time_ms
            r.tt_extreme_status = "REOPENED"
            r.tt_extreme_kt = 0
            self._absorb_ft_if_any(t)
            r.ev(t, "TT_EXTENSION_WINDOW_REOPENED_AT_OPEN",
                 f"apertura {t.price} supera el extremo funcional; no se archiva")
            return
        if r.tt_extreme_kt // 60000 == t.bar:
            # El extremo se conocio en esta misma vela: el archivo espera a la
            # apertura siguiente (no se archiva con conocimiento intravela).
            return

        # TT -> patron con identidad propia (historico, conservado).
        tt_id = f"{gen.generation_id}-TT-{r.tt_objective}"
        confirmed_price = r.tt_objective + r.tt_overshoot * r.tt_dir
        tt = next((p for p in self.pattern_records if p.pattern_id == tt_id), None)
        if tt is None:
            tt = PatternRecord(
                pattern_id=tt_id, pattern_type="TT",
                owner_generation_id=gen.generation_id, owner_slot="LOCAL",
                status=r.tt_status, objective=r.tt_objective,
                confirmed_price=confirmed_price,
                confirmed_at_seq=self.seq_of.get(r.tt_kt, 0),
                physical_extreme=r.tt_extreme,
                physical_extreme_seq=self.seq_of.get(r.tt_extreme_st, 0),
                physical_extreme_st=r.tt_extreme_st,
                functional_extreme=r.tt_extreme,
                functional_extreme_seq=self.seq_of.get(r.tt_extreme_st, 0),
                functional_extreme_status=r.tt_extreme_status,
                functional_extreme_knowledge_seq=self.seq_of.get(
                    r.tt_extreme_kt, 0),
                structural_time=r.tt_extreme_st,
                knowledge_time=r.tt_extreme_kt,
                opened_at_seq=self.l2_discovered_at_seq,
                derived_pattern_ids=[])
            # El FT nace del extremo funcional, no del primer retroceso.
            ft_id = f"{gen.generation_id}-FT-{r.ft_origin}"
            ft = PatternRecord(
                pattern_id=ft_id, pattern_type="FT",
                owner_generation_id=gen.generation_id, owner_slot="LOCAL",
                status=r.ft_status or "FT_POSSIBLE", objective=0,
                confirmed_price=r.ft_confirmed_price,
                confirmed_at_seq=self.seq_of.get(r.ft_kt, 0),
                physical_extreme=r.ft_extreme,
                physical_extreme_seq=self.seq_of.get(r.ft_extreme_st, 0),
                physical_extreme_st=r.ft_extreme_st,
                functional_extreme=r.ft_origin,
                functional_extreme_seq=self.seq_of.get(r.ft_st, 0),
                functional_extreme_status="CONFIRMED",
                functional_extreme_knowledge_seq=self.seq_of.get(r.ft_kt, 0),
                structural_time=r.ft_st,
                knowledge_time=r.ft_kt,
                opened_at_seq=self.seq_of.get(r.ft_st, 0),
                authority="PROVISIONAL_POLICY")
            tt.derived_pattern_ids.append(ft_id)
            self.pattern_records.extend([tt, ft])

        gen.close_reason = "TT_FUNCTIONAL_EXTREME_CONFIRMED"
        gen.closed_at_seq = t.seq
        gen.active_pattern_ids = [p.pattern_id for p in self.pattern_records
                                  if p.owner_generation_id == gen.generation_id
                                  and p.pattern_type == "TT"]
        gen.historical_pattern_ids = [p.pattern_id for p in self.pattern_records
                                      if p.owner_generation_id == gen.generation_id
                                      and p.pattern_type == "FT"]
        gen.status = "ARCHIVED"
        self._sync_legacy_registry(t, gen, tt)
        self.slots["LOCAL"].active_generation_id = ""
        self.l2_archived = True
        # El patron sobrevive al slot: solo se congela la capa de funciones.
        self.l2.pattern_only = True
        self.l2.reading.ev(t, "LOCAL_G1_ARCHIVED",
                           f"generation={gen.generation_id} "
                           f"close_reason={gen.close_reason} "
                           f"tt={tt_id} ft={gen.historical_pattern_ids} "
                           f"extremo_funcional={r.tt_extreme} slot=LIBRE")

    def _sync_legacy_registry(self, t: Tick, gen: GenerationRecord,
                              tt: PatternRecord) -> None:
        """Unifica los registros legacy con el ciclo de vida autoritativo.

        `self.generations` y `self.tt_records` se crean una sola vez y antes
        quedaban congelados con closed_at=0; el estado real vive en
        GenerationRecord/PatternRecord. Aqui se copia para que las tablas
        exportadas no contradigan al checkpoint.
        """
        for g in self.generations:
            if g["generation_id"] == gen.generation_id:
                g["status"] = gen.status
                g["closed_at"] = t.time_ms
                g["close_reason"] = gen.close_reason
                g["functional_closure_at_seq"] = gen.functional_closure_at_seq
                g["closed_at_seq"] = gen.closed_at_seq
        for rec in self.tt_records:
            if rec["tt_id"].endswith(f"-TT-{tt.objective}") \
                    and rec["owner_generation"] == gen.generation_id:
                rec["status"] = tt.status
                rec["pattern_status"] = "HISTORICAL"
                rec["closed_at"] = t.time_ms
                rec["confirmed_price"] = tt.confirmed_price
                rec["physical_extreme"] = tt.physical_extreme
                rec["functional_extreme"] = tt.functional_extreme
                rec["functional_extreme_knowledge_seq"] = \
                    tt.functional_extreme_knowledge_seq

    def _absorb_ft_if_any(self, t: Tick) -> None:
        """Invalida el FT cuyo origen fue superado por el TT (delegado)."""
        if self.l2 is not None and self.l2.reading.ft_status:
            self.l2._absorb_ft(t, "MANAGER_OPEN_OVERFLOW")

    def _close_local_g2_decision(self) -> None:
        """Registra por que LOCAL-G2 no se abre en 16:26 (o si se abriera)."""
        if self.l2 is None or not self.l2_archived:
            return
        r = self.l2.reading
        inherited = []
        if r.one_origin:
            inherited.append({
                "reference": "one_origin", "value": r.one_origin,
                "note": "estado congelado de LOCAL-G1 (1 local); una nueva "
                        "generacion no puede usarlo como referencia propia"})
        if r.mod_size:
            inherited.append({
                "reference": "mod_size", "value": r.mod_size,
                "note": "modulo 1-2-3 de LOCAL-G1, no un modulo por descarte "
                        "de 16:26"})
        inherited.append({
            "reference": "post_rotation_probe", "value": 0,
            "note": "con archive_local=False el Reader rota en 16:26 y su "
                    "'one' pasa a ser el nuevo 1 de LOCAL-G1 (29828,1); "
                    "mod_size permanece 0 hasta 16:29: no hay modulo por "
                    "descarte local en 16:26"})
        self.local_g2_decision = {
            "decision": "NOT_OPENED",
            "scene": "FUNCTION_AND_FT_EXPLAIN_16_26",
            "reason": ("El movimiento de 16:26 queda explicado por FT "
                       "(propietario LOCAL-G1) y por A principal (PRIMARY-G1) "
                       "compartiendo origen; no se forma modulo por descarte "
                       "local en 16:26 y la continuacion del Reader local "
                       "arrastra el 'one' de LOCAL-G1. Abrir LOCAL-G2 exigiria "
                       "heredar referencias o inventar un modulo."),
            "evidence": inherited + self.local_g2_evidence,
            "authority": "CANONICAL",
        }

    def _on_local_open(self, t: Tick) -> None:
        """Gancho reservado para LOCAL-G2 (no usado en 19B)."""
        return

    # -------------------------------------------------------------- snapshot
    def snapshot(self, t: Tick) -> dict:
        l1 = self.l1.reading
        row = {
            "sequence_id": t.seq, "time_ms": t.time_ms,
            "bar": t.bar % 1440, "price": t.price,
            "l1_phase": l1.phase, "l1_active": l1.active_function,
            "l1_tt": l1.tt_status, "l1_tt_objective": l1.tt_objective,
            "l1_tt_owner": "L1" if l1.tt_objective else "",
            "l1_n_origin": l1.n_origin, "l1_n_extreme": l1.n_extreme,
            "l1_a": f"{l1.a_status}/{l1.a_size}@{l1.a_origin}",
            "l1_b": f"{l1.b_status}/{l1.b_size}",
            "l1_mod": l1.mod_size, "l1_two": l1.two_status,
            "l1_cycle": l1.cycle_id, "l1_one_size": l1.one_size,
            "l1_one_dir": l1.one_dir, "l1_a_status": l1.a_status,
            "l1_a_size": l1.a_size, "l1_a_origin": l1.a_origin,
            "l1_b_status": l1.b_status, "l1_b_size": l1.b_size,
            "l2": "", "l2_tt": "", "l2_tt_objective": 0,
            "l2_tt_owner": "", "l2_phase": "",
            "l2_gen": "", "l2_gen_status": "",
        }
        if self.l2 is not None:
            l2 = self.l2.reading
            gen = self._local_generation()
            if gen is None:
                # Generacion local archivada: se muestra su identidad porque
                # sigue siendo la propietaria de los patrones vivos.
                gen = next((g for g in reversed(self.gen_records)
                            if g.slot == "LOCAL"), None)
            row.update({
                "l2": f"{l2.phase}|a={l2.a_status}/{l2.a_size}"
                      f"|b={l2.b_status}/{l2.b_size}"
                      f"|n={l2.n_origin}->{l2.n_extreme}",
                "l2_phase": l2.phase,
                "l2_tt": l2.tt_status,
                "l2_tt_objective": l2.tt_objective,
                "l2_tt_owner": "L2" if l2.tt_objective else "",
                "l2_one_size": l2.one_size, "l2_two_size": l2.two_size,
                "l2_one_origin": l2.one_origin,
                "l2_mod": l2.mod_size, "l2_three": l2.three_extreme,
                "l2_a_origin": l2.a_origin, "l2_a_size": l2.a_size,
                "l2_n_origin": l2.n_origin, "l2_n_extreme": l2.n_extreme,
                "l2_ft_origin": l2.ft_origin, "l2_ft_dir": l2.ft_dir,
                "l2_ft_status": l2.ft_status, "l2_ft_extreme": l2.ft_extreme,
                "l2_ft_st": l2.ft_st, "l2_ft_kt": l2.ft_kt,
                "l2_tt_extreme": l2.tt_extreme,
                "l2_tt_extreme_st": l2.tt_extreme_st,
                "l2_tt_extreme_kt": l2.tt_extreme_kt,
                "l2_tt_extreme_status": l2.tt_extreme_status,
                "l2_ft_absorbed": l2.ft_absorbed,
                "l2_gen": gen.generation_id if gen else "",
                "l2_gen_status": gen.status if gen else "",
            })
        return row

    # --------------------------------------------------------------- helpers
    def bar_close_state(self, bar: int) -> dict:
        rows = [r for r in self.rows if r["bar"] == bar % 1440]
        return rows[-1] if rows else {}

    def first_rows(self) -> dict[int, dict]:
        out: dict[int, dict] = {}
        for r in self.rows:
            out.setdefault(r["bar"], r)
        return out

    def last_rows(self) -> dict[int, dict]:
        out: dict[int, dict] = {}
        for r in self.rows:
            out[r["bar"]] = r
        return out

    def summaries(self) -> dict:
        out = {"l1": self.l1.summary(), "l2_discovered": self.l2 is not None,
               "l2_created_at_seq": self.l2_discovered_at_seq,
               "l2_seed_bar": self.l2_seed_bar,
               "l2_discovery_rule": self.l2_discovery_rule}
        out["l2"] = self.l2.summary() if self.l2 else None
        out["generations"] = self.generations
        out["tt_records"] = self.tt_records
        out["generation_records"] = [asdict(g) for g in self.gen_records]
        out["pattern_records"] = [asdict(p) for p in self.pattern_records]
        out["slots"] = {k: asdict(v) for k, v in self.slots.items()}
        out["archived_generation_writes"] = self.archived_generation_writes
        out["local_g2_decision"] = self.local_g2_decision
        return out

    def tt_owners(self) -> list[dict]:
        out = []
        for name, reader in (("L1", self.l1), ("L2", self.l2)):
            if reader is None:
                continue
            r = reader.reading
            if r.tt_objective:
                out.append({"reading_id": name, "objective": r.tt_objective,
                            "status": r.tt_status, "dir": r.tt_dir,
                            "final_a": r.tt_final_a,
                            "extreme": r.tt_extreme,
                            "extreme_status": r.tt_extreme_status,
                            "owner": name})
        return out

    # Evidencia recogida por el diagnostico de LOCAL-G2.
    local_g2_evidence: list[dict] = []


def run(ticks: list[Tick] | None = None) -> TMReadingManager:
    return TMReadingManager(ticks if ticks is not None else load_ticks(FEED)).run()


if __name__ == "__main__":
    mgr = run()
    print(mgr.summaries())
