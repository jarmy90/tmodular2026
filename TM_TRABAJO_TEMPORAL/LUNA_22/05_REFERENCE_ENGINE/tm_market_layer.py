#!/usr/bin/env python3
"""Iteracion 21 — capas compartidas: ledger fisico, hechos, arbitraje, trazador.

    CAPA 1  TickLedger      hechos fisicos inmutables, append-only
    CAPA 2  MarketFacts     apertura/cierre, plano o gap, cola inicial,
                            high/low fisico y primer toque de un nivel
    CAPA 3  (por rama)      CandidateTracker + QuestionBook + ConfirmedState
                            — ya vive en tm_candidates.py
    CAPA 4  BranchArbiter   maximo MAIN + LOCAL, sin tercera rama, sin
                            referencias entre propietarios
    TRAZA   DecisionTracer  una fila por tick con evidencia y decision, mas
                            clasificacion de divergencias

Ninguna capa de este modulo escribe estado funcional confirmado: son lectura
pura sobre el flujo de ticks. El estado funcional solo cambia por
FunctionalCommit (tm_candidates).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from tm_candidates import (ArchitectureViolation, AT_BIRTH, AT_PHYSICAL,
                           AT_STRUCTURAL, ViolationLedger)

# 1 punto de precio = 100 unidades internas (29870,50 -> 2987050)
POINT = 100
FLAT_THRESHOLD = 25      # abs(Open - Close previo) < 0,25 -> plano
NOISE_MOVE = 200         # 2,00 puntos: solo ruido fisico vs desplazamiento

MAIN = "MAIN"
LOCAL = "LOCAL"

# clasificaciones de divergencia
QUESTION_ERROR = "QUESTION_ERROR"
REFERENCE_ERROR = "REFERENCE_ERROR"
OWNER_ERROR = "OWNER_ERROR"
EARLY_CONFIRMATION = "EARLY_CONFIRMATION"
LATE_CONFIRMATION = "LATE_CONFIRMATION"
NOISE_FRAGMENTATION = "NOISE_FRAGMENTATION"
WRONG_ABSORPTION = "WRONG_ABSORPTION"
LOST_STATE = "LOST_STATE"
MISSING_RULE = "MISSING_RULE"
NO_DIVERGENCE = "NO_DIVERGENCE"


# ------------------------------------------------------------------- CAPA 1
@dataclass(frozen=True)
class TickRecord:
    """Un tick fisico. Inmutable: el ledger nunca se reescribe."""
    sequence_id: int
    timestamp: int
    bar_id: int
    bid: int
    ask: int | None = None
    spread: int | None = None
    is_first_tick_of_bar: bool = False
    is_last_tick_of_bar: bool = False

    def snapshot(self) -> dict:
        return {
            "sequence_id": self.sequence_id, "timestamp": self.timestamp,
            "bar_id": self.bar_id, "bid": self.bid, "ask": self.ask,
            "spread": self.spread,
            "is_first_tick_of_bar": self.is_first_tick_of_bar,
            "is_last_tick_of_bar": self.is_last_tick_of_bar,
        }


class TickLedger:
    """CAPA 1 — append-only. Cualquier intento de reescritura aborta."""

    def __init__(self) -> None:
        self.rows: list[TickRecord] = []
        self._sealed: dict[int, TickRecord] = {}
        self._seqs: set[int] = set()
        self.violations = ViolationLedger()

    def append(self, seq: int, time_ms: int, bar: int, price: int,
               ask: int | None = None, spread: int | None = None) -> TickRecord:
        if seq in self._seqs or seq in self._sealed:
            self.violations.hit("candidate_state_writes",
                                "LEDGER_REWRITE", seq)
            raise ArchitectureViolation(f"LEDGER_REWRITE:{seq}")
        first = not self.rows or self.rows[-1].bar_id != bar
        if self.rows and first:
            prev = self.rows[-1]
            self._sealed[prev.sequence_id] = TickRecord(
                **{**prev.snapshot(), "is_last_tick_of_bar": True})
            self.rows[-1] = self._sealed[prev.sequence_id]
        rec = TickRecord(seq, time_ms, bar, price, ask, spread,
                         is_first_tick_of_bar=first)
        self.rows.append(rec)
        self._seqs.add(seq)
        return rec

    def __len__(self) -> int:
        return len(self.rows)

    def last(self) -> TickRecord | None:
        return self.rows[-1] if self.rows else None


# ------------------------------------------------------------------- CAPA 2
class MarketFacts:
    """Hechos fisicos compartidos. No asigna ninguna etiqueta TM."""

    def __init__(self) -> None:
        self.bar_id: int | None = None
        self.bar_open: int | None = None
        self.previous_close: int | None = None
        self.open_difference: int = 0
        self.flat_or_gap: str = ""
        self.initial_tail: int = 0
        self.initial_tail_dir: int = 0
        self.initial_tail_closed: bool = False
        self.physical_high: int | None = None
        self.physical_low: int | None = None
        self.high_bar: int | None = None
        self.low_bar: int | None = None
        self.touches: dict[int, int] = {}
        self.touch_log: list[tuple[int, int]] = []

    # -- ciclo de vida por tick -------------------------------------------
    def observe(self, seq: int, bar: int, price: int) -> None:
        if self.bar_id is None:
            self.bar_id = bar
            self.bar_open = price
            self.open_difference = 0
            self.flat_or_gap = "OPENING_BAR"
        elif bar != self.bar_id:
            self.previous_close = self._last_price
            self.bar_id = bar
            self.bar_open = price
            self.open_difference = price - self.previous_close
            self.flat_or_gap = ("FLAT" if abs(self.open_difference)
                                < FLAT_THRESHOLD else "GAP")
            self.initial_tail = 0
            self.initial_tail_dir = 0
            self.initial_tail_closed = False
        if self.physical_high is None or price > self.physical_high:
            self.physical_high = price
            self.high_bar = bar
        if self.physical_low is None or price < self.physical_low:
            self.physical_low = price
            self.low_bar = bar
        self._observe_tail(price)
        self._last_price = price

    _last_price: int = 0

    def _observe_tail(self, price: int) -> None:
        """Cola inicial: excursion desde la apertura hasta el primer tick que
        la contradice. Se congela una sola vez; no se recalcula con futuro."""
        if self.initial_tail_closed or self.bar_open is None:
            return
        off = price - self.bar_open
        if off == 0:
            return
        d = 1 if off > 0 else -1
        if self.initial_tail_dir == 0:
            self.initial_tail_dir = d
            self.initial_tail = abs(off)
            return
        if d != self.initial_tail_dir:
            self.initial_tail_closed = True
            return
        self.initial_tail = max(self.initial_tail, abs(off))

    # -- consultas --------------------------------------------------------
    def touch(self, level: int, seq: int) -> bool:
        """Registra el primer toque exacto de un nivel. True si es el primero."""
        if level in self.touches:
            return False
        self.touches[level] = seq
        self.touch_log.append((level, seq))
        return True

    def first_touch_seq(self, level: int) -> int | None:
        return self.touches.get(level)

    def snapshot(self) -> dict:
        return {
            "bar_id": self.bar_id, "bar_open": self.bar_open,
            "previous_close": self.previous_close,
            "open_difference": self.open_difference,
            "flat_or_gap": self.flat_or_gap,
            "initial_tail": self.initial_tail,
            "initial_tail_dir": self.initial_tail_dir,
            "initial_tail_closed": self.initial_tail_closed,
            "physical_high": self.physical_high,
            "physical_low": self.physical_low,
            "touches": len(self.touches),
        }


# ------------------------------------------------------------------- CAPA 4
@dataclass
class BranchRecord:
    branch_id: str
    branch_type: str
    generation_id: str
    status: str = "ACTIVE"
    rank: str = "PRIMARY"
    opened_at_seq: int = 0
    closed_at_seq: int = 0

    def snapshot(self) -> dict:
        return {
            "branch_id": self.branch_id, "branch_type": self.branch_type,
            "generation_id": self.generation_id, "status": self.status,
            "rank": self.rank, "opened_at_seq": self.opened_at_seq,
            "closed_at_seq": self.closed_at_seq,
        }


class BranchArbiter:
    """Maximo una MAIN y una LOCAL. Ninguna tercera rama. Sin lecturas
    cruzadas entre propietarios."""

    def __init__(self, violations: ViolationLedger) -> None:
        self.violations = violations
        self.branches: dict[str, BranchRecord] = {}

    def register(self, branch_id: str, branch_type: str, generation_id: str,
                 seq: int = 0, rank: str = "PRIMARY") -> BranchRecord:
        if branch_type not in (MAIN, LOCAL):
            self.violations.hit("third_branch_attempts",
                                f"TYPE:{branch_type}", seq)
            raise ArchitectureViolation(f"BRANCH_TYPE_NOT_ALLOWED:{branch_type}")
        if branch_id in self.branches:
            return self.branches[branch_id]
        live = [b for b in self.branches.values() if b.status == "ACTIVE"]
        if any(b.branch_type == branch_type for b in live):
            self.violations.hit("third_branch_attempts",
                                f"SECOND_{branch_type}", seq)
            raise ArchitectureViolation(f"SECOND_BRANCH_OF_TYPE:{branch_type}")
        if len(live) >= 2:
            self.violations.hit("third_branch_attempts", "THIRD_BRANCH", seq)
            raise ArchitectureViolation("THIRD_BRANCH")
        rec = BranchRecord(branch_id, branch_type, generation_id,
                           opened_at_seq=seq, rank=rank)
        self.branches[branch_id] = rec
        return rec

    def close(self, branch_id: str, seq: int) -> None:
        rec = self.branches.get(branch_id)
        if rec is None:
            return
        rec.status = "ARCHIVED"
        rec.closed_at_seq = seq

    def active(self) -> list[BranchRecord]:
        return [b for b in self.branches.values() if b.status == "ACTIVE"]

    def set_rank(self, branch_id: str, rank: str) -> None:
        if branch_id in self.branches:
            self.branches[branch_id].rank = rank

    def check_reference(self, reader_branch: str, reference_branch: str,
                        seq: int = -1) -> bool:
        ok = reader_branch == reference_branch
        if not ok:
            self.violations.hit("cross_owner_reference_reads",
                                f"{reader_branch}->{reference_branch}", seq)
        return ok

    def snapshot(self) -> list[dict]:
        return [b.snapshot() for b in self.branches.values()]


# --------------------------------------------------------------------- traza
class DecisionTracer:
    """Una fila por tick con la evidencia y la decision. Permite clasificar
    una divergencia sin adivinar."""

    def __init__(self) -> None:
        self.rows: list[dict] = []
        self.classifications: list[dict] = []

    def record(self, *, seq: int, timestamp: int, price: int, branch_id: str,
               generation_id: str, confirmed_before: dict, candidate_before: str,
               current_question: str, references_used: Iterable[str],
               physical_evidence: dict, structural_evidence: dict,
               functional_evidence: dict, decision: str,
               confirmed_after: dict, candidate_after: str,
               events: Iterable[str] = (), structural_time: int = 0,
               knowledge_time: int = 0, explanation: str = "") -> dict:
        row = {
            "sequence_id": seq, "timestamp": timestamp, "price": price,
            "branch_id": branch_id, "generation_id": generation_id,
            "confirmed_node_before": confirmed_before,
            "candidate_before": candidate_before,
            "current_question": current_question,
            "references_used": list(references_used),
            "physical_evidence": physical_evidence,
            "structural_evidence": structural_evidence,
            "functional_evidence": functional_evidence,
            "decision": decision,
            "confirmed_node_after": confirmed_after,
            "candidate_after": candidate_after,
            "events": list(events),
            "structural_time": structural_time,
            "knowledge_time": knowledge_time,
            "explanation": explanation,
        }
        self.rows.append(row)
        return row

    # -- clasificacion de una divergencia ---------------------------------
    def classify(self, row: dict, expected: dict, *, seq: int = -1,
                 absorbed_at: str = "") -> str:
        """Compara la traza real con la esperada y devuelve la clase."""
        after = row.get("confirmed_node_after", {}) or {}
        want = expected.get("confirmed_node_after", {}) or {}
        exp_seq = expected.get("sequence_id")
        row_seq = row.get("sequence_id")
        if expected.get("current_question") and (
                row.get("current_question") != expected["current_question"]):
            code = QUESTION_ERROR
        elif expected.get("references_used") and (
                list(row.get("references_used", []))
                != list(expected["references_used"])):
            code = REFERENCE_ERROR
        elif expected.get("branch_id") and (
                row.get("branch_id") != expected["branch_id"]):
            code = OWNER_ERROR
        elif want and all(after.get(k) == v for k, v in want.items()
                          if v is not None) and not exp_seq:
            code = NO_DIVERGENCE
        elif want and all(after.get(k) == v for k, v in want.items()
                          if v is not None) and exp_seq:
            # el valor llega, pero en otro tick: confirmacion temprana o tardia
            code = (EARLY_CONFIRMATION if row_seq < exp_seq else
                    LATE_CONFIRMATION if row_seq > exp_seq else NO_DIVERGENCE)
        elif absorbed_at in (AT_BIRTH, AT_PHYSICAL, AT_STRUCTURAL):
            code = NOISE_FRAGMENTATION
        elif str(row.get("decision", "")).startswith("ABSORB") and expected.get(
                "keep", False):
            code = WRONG_ABSORPTION
        elif row.get("confirmed_node_before") and not after:
            code = LOST_STATE
        else:
            code = MISSING_RULE
        self.classifications.append({"sequence_id": row.get("sequence_id", seq),
                                     "classification": code})
        return code

    def first_divergence(self, expected: list[dict]) -> dict | None:
        """Compara fila a fila contra las filas esperadas (mismo seq)."""
        by_seq = {r["sequence_id"]: r for r in self.rows}
        for exp in expected:
            got = by_seq.get(exp.get("sequence_id"))
            if got is None:
                continue
            want = exp.get("confirmed_node_after") or {}
            for k, v in want.items():
                if v is not None and got["confirmed_node_after"].get(k) != v:
                    return {"sequence_id": exp["sequence_id"], "field": k,
                            "expected": v,
                            "actual": got["confirmed_node_after"].get(k)}
        return None

    def snapshot(self, limit: int = 0) -> list[dict]:
        return self.rows[:limit] if limit else list(self.rows)

