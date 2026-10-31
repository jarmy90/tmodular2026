#!/usr/bin/env python3
"""ITERACION 17 — gestor de lecturas TM (L1 principal + L2 local).

Arquitectura
------------
  * L1: lectura principal, arranca con el primer tick del feed.
  * L2: lectura local opcional, descubierta causalmente por el propio motor.
  * Maximo dos escalas activas. Archivo historico de lecturas cerradas.

Descubrimiento causal de L2
---------------------------
Se abre una sola L2 cuando, al cerrar una vela:

  * L1 mantiene un TT pendiente (estructura anterior viva);
  * la vela cerrada tiene un recorrido >= filtro de ruido (2,0 puntos);
  * el recorrido de la vela va en la direccion del nuevo 1 de L1.

La L2 se siembra con los ticks YA CERRADOS de esa vela. No se usan ticks
futuros: en la apertura siguiente la vela anterior es informacion conocida.

Aislamiento
-----------
Cada lectura es un Reader independiente. El gestor nunca copia module_size,
final_A, TT, A, B, C ni extremos entre lecturas. Cada TT tiene propietario
(reading_id) y cada lectura mantiene su propio estado.
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
    pattern_id: str
    pattern_type: str
    owner_generation_id: str
    owner_slot: str
    status: str
    objective: int = 0
    real_extreme: int = 0
    opened_at_seq: int = 0
    confirmed_at_seq: int = 0
    closed_at_seq: int = 0
    derived_pattern_ids: list[str] = field(default_factory=list)


@dataclass
class GenerationRecord:
    generation_id: str
    slot: str
    status: str = "ACTIVE"
    opened_at_seq: int = 0
    closed_at_seq: int = 0
    close_reason: str = ""
    active_pattern_ids: list[str] = field(default_factory=list)
    historical_pattern_ids: list[str] = field(default_factory=list)


@dataclass
class ReadingSlotState:
    slot_id: str
    active_generation_id: str = ""


class TMReadingManager:
    def __init__(self, ticks: list[Tick], discover_l2: bool = True):
        self.ticks = ticks
        self.discover_l2 = discover_l2
        self.l1 = Reader([], reading_id="L1")
        self.l2: Reader | None = None
        self.archive: list[dict] = []
        self.l2_discovered_at_seq: int = 0
        self.l2_seed_bar: int = -1
        self.l2_discovery_rule: str = ""
        self.generations: list[dict] = []
        self.tt_records: list[dict] = []
        # Iteracion 19A: registros minimos con identidad.
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
        gen = GenerationRecord("LOCAL-G1", "LOCAL", opened_at_seq=seed[0].seq)
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
            self.cur_bar = t.bar
        self.by_bar.setdefault(t.bar, []).append(t)
        self.l1.feed(t)
        if self.l2 is not None and not self.l2_archived:
            self.l2.feed(t)
            self._maybe_archive_local(t)
        self._record_identity(t)
        self.rows.append(self.snapshot(t))

    def run(self) -> "TMReadingManager":
        for t in self.ticks:
            self.feed(t)
        self.l2_finalized = self.l2 is not None
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
                    "closed_at": 0, "close_reason": "",
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
                        "opened_at": t.time_ms, "closed_at": 0,
                        "invalidation_rule": ("final_A_cruce"
                                               if not self.l2 else
                                               "solo_objetivo_local")})
                else:
                    rec = next(x for x in self.tt_records
                               if (x["owner_generation"], x["objective"]) == key)
                    rec["status"] = r.tt_status
                    if r.tt_status in ("TT_CONFIRMED", "TT_EXTENDED", "TT_FAILED"):
                        if not rec["closed_at"]:
                            rec["closed_at"] = t.time_ms

    def _local_generation(self) -> GenerationRecord | None:
        for g in self.gen_records:
            if g.slot == "LOCAL" and g.status == "ACTIVE":
                return g
        return None

    def _maybe_archive_local(self, t: Tick) -> None:
        """Cierra LOCAL-G1 cuando su TT se confirma/extiende (regla general).

        No usa hora ni precio: solo el evento TT y el propietario.
        """
        if self.l2 is None or self.l2_archived:
            return
        r = self.l2.reading
        gen = self._local_generation()
        if gen is None:
            return
        if r.tt_status not in ("TT_CONFIRMED", "TT_EXTENDED"):
            return
        # El extremo real del TT se conoce al cierre de su vela. El archivo
        # espera a la vela siguiente; no usa hora ni precio.
        if self._tt_confirmed_bar == -1:
            self._tt_confirmed_bar = t.bar
        if t.bar == self._tt_confirmed_bar:
            return
        # TT -> patron con identidad propia, conservado como historico.
        tt_id = f"{gen.generation_id}-TT-{r.tt_objective}"
        if not any(p.pattern_id == tt_id for p in self.pattern_records):
            self.pattern_records.append(PatternRecord(
                pattern_id=tt_id, pattern_type="TT",
                owner_generation_id=gen.generation_id, owner_slot="LOCAL",
                status=r.tt_status, objective=r.tt_objective,
                real_extreme=r.tt_extreme, opened_at_seq=self.l2_discovered_at_seq,
                confirmed_at_seq=t.seq))
        # FT derivado del extremo real del TT.
        ft_id = f"{gen.generation_id}-FT-{r.tt_extreme}"
        if not any(p.pattern_id == ft_id for p in self.pattern_records):
            self.pattern_records.append(PatternRecord(
                pattern_id=ft_id, pattern_type="FT",
                owner_generation_id=gen.generation_id, owner_slot="LOCAL",
                status="FT_POSSIBLE", objective=0,
                real_extreme=r.tt_extreme, opened_at_seq=t.seq))
        gen.status = "CLOSING"
        gen.closed_at_seq = t.seq
        gen.close_reason = "TT_CONFIRMED"
        gen.active_pattern_ids = [p.pattern_id for p in self.pattern_records
                                  if p.owner_generation_id == gen.generation_id
                                  and p.pattern_type == "TT"]
        gen.historical_pattern_ids = [p.pattern_id for p in self.pattern_records
                                      if p.owner_generation_id == gen.generation_id
                                      and p.pattern_type == "FT"]
        gen.status = "ARCHIVED"
        self.slots["LOCAL"].active_generation_id = ""
        self.l2_archived = True
        self.l2.reading.ev(t, "LOCAL_G1_ARCHIVED",
                           f"generation={gen.generation_id} "
                           f"close_reason={gen.close_reason} "
                           f"tt={tt_id} ft={ft_id} slot=LIBRE")

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
            "l1_mod": l1.mod_size,
            "l2": "", "l2_tt": "", "l2_tt_objective": 0,
            "l2_tt_owner": "", "l2_phase": "",
        }
        if self.l2 is not None:
            l2 = self.l2.reading
            row.update({
                "l2": f"{l2.phase}|a={l2.a_status}/{l2.a_size}"
                      f"|b={l2.b_status}/{l2.b_size}"
                      f"|n={l2.n_origin}->{l2.n_extreme}",
                "l2_phase": l2.phase,
                "l2_tt": l2.tt_status,
                "l2_tt_objective": l2.tt_objective,
                "l2_tt_owner": "L2" if l2.tt_objective else "",
                "l2_one_size": l2.one_size, "l2_two_size": l2.two_size,
                "l2_mod": l2.mod_size, "l2_three": l2.three_extreme,
                "l2_a_origin": l2.a_origin, "l2_a_size": l2.a_size,
                "l2_n_origin": l2.n_origin, "l2_n_extreme": l2.n_extreme,
                "l2_ft_origin": l2.ft_origin, "l2_ft_dir": l2.ft_dir,
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
                            "owner": name})
        return out


def run(ticks: list[Tick] | None = None) -> TMReadingManager:
    return TMReadingManager(ticks if ticks is not None else load_ticks(FEED)).run()


if __name__ == "__main__":
    mgr = run()
    print(mgr.summaries())
