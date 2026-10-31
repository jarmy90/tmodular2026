#!/usr/bin/env python3
"""Iteracion 21 — arquitectura de candidatos, preguntas y estado confirmado.

Principio constitucional:

    UN CANDIDATO NUNCA MODIFICA EL ESTADO FUNCIONAL CONFIRMADO.

El estado confirmado solo cambia por un FunctionalCommit emitido despues de que
la pregunta vigente del arbol lo autorice. Este modulo es la unica via.

Diseno:

    TickRecord            ledger fisico inmutable (vive en el lector)
    CandidateRecord       observacion con evidencia acumulada
    CandidateTracker      por rama; NO tiene referencia al Reading (no puede
                          escribir el estado funcional ni por error)
    CandidateShadow       geometria de un candidato absorbido que impide
                          recrearlo sin evidencia nueva
    TreeQuestion          contrato de pregunta con `consumes` cerrado
    QuestionBook          preguntas de una rama, prioridad y resolucion
    ConfirmedState        campos funcionales + version; solo escribe por commit
    FunctionalCommit      ticket ADMIT / CONFIRM / ABSORB / EXTEND / RECLASSIFY
    ViolationLedger       contadores y registros de violacion
    BranchRuntime         union por rama: tracker + preguntas + estado + commits
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

# --------------------------------------------------------------------- estados
OBSERVED = "OBSERVED"
PHYSICAL = "PHYSICAL"
STRUCTURAL = "STRUCTURAL"
CONFIRMED = "CONFIRMED"
ABSORBED = "ABSORBED"
DISCARDED = "DISCARDED"
RECLASSIFIED = "RECLASSIFIED"

TERMINAL = {ABSORBED, DISCARDED, RECLASSIFIED}

# Tipos de commit. ADMIT escribe un estado PENDIENTE autorizado por la pregunta;
# CONFIRM escribe una funcion confirmada y exige evidencia posterior al alta.
ADMIT = "ADMIT"
CONFIRM = "CONFIRM"
ABSORB = "ABSORB"
EXTEND = "EXTEND"
RECLASSIFY = "RECLASSIFY"

# Iteracion 22 — autoridad de la decision
LEGACY = "LEGACY"
TREE_QUESTION = "TREE_QUESTION"
PHYSICAL_FACT = "PHYSICAL_FACT"
PATTERN_ARBITRATION = "PATTERN_ARBITRATION"
AUTHORITIES = (LEGACY, TREE_QUESTION, PHYSICAL_FACT, PATTERN_ARBITRATION)

# Niveles de absorcion (donde murio el candidato)
AT_BIRTH = "AT_BIRTH"
AT_PHYSICAL = "AT_PHYSICAL"
AT_STRUCTURAL = "AT_STRUCTURAL"
AT_FUNCTIONAL = "AT_FUNCTIONAL"


class ArchitectureViolation(RuntimeError):
    """Violacion de un invariante de la arquitectura (aborta la ejecucion)."""


# --------------------------------------------------------------------- violaciones
class ViolationLedger:
    KEYS = (
        "candidate_state_writes",
        "cross_owner_reference_reads",
        "consumes_violations",
        "unowned_candidates",
        "same_tick_confirmation",
        "third_branch_attempts",
        "shadow_recreations_blocked",
        "archived_generation_writes",
        "legacy_preemptions",
    )

    def __init__(self) -> None:
        self.counts = {k: 0 for k in self.KEYS}
        self.records: list[dict] = []
        self.strict = False

    def hit(self, kind: str, detail: str, seq: int = -1) -> None:
        if kind not in self.counts:
            self.counts[kind] = 0
        self.counts[kind] += 1
        self.records.append({"seq": seq, "kind": kind, "detail": detail})
        if self.strict:
            raise ArchitectureViolation(f"{kind} @ {seq}: {detail}")

    def total(self) -> int:
        return sum(self.counts.values())

    def summary(self) -> dict:
        return {"counts": dict(self.counts), "total": self.total(),
                "records": len(self.records)}


# --------------------------------------------------------------------- candidato
@dataclass
class CandidateRecord:
    candidate_id: str
    owner_branch_id: str
    owner_generation_id: str
    source_function_id: str
    role_hypothesis: str
    direction: int
    origin: int
    origin_seq: int
    extreme: int
    extreme_seq: int
    status: str = OBSERVED
    physical_size: int = 0
    physical_requirement: int = 0
    retention_tests: int = 0
    owner_reclaimed: bool = False
    question_id: str = ""
    structural_time: int = 0
    knowledge_time: int = 0
    absorption_level: str = ""
    absorbing_id: str = ""
    shadow_id: str = ""
    close_reason: str = ""
    created_at_seq: int = 0
    closed_at_seq: int = 0
    commits: list = field(default_factory=list)

    @property
    def size(self) -> int:
        return abs(self.extreme - self.origin)

    def snapshot(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "owner_branch_id": self.owner_branch_id,
            "owner_generation_id": self.owner_generation_id,
            "source_function_id": self.source_function_id,
            "role_hypothesis": self.role_hypothesis,
            "direction": self.direction,
            "origin": self.origin,
            "origin_seq": self.origin_seq,
            "extreme": self.extreme,
            "extreme_seq": self.extreme_seq,
            "status": self.status,
            "physical_size": self.physical_size,
            "retention_tests": self.retention_tests,
            "owner_reclaimed": self.owner_reclaimed,
            "question_id": self.question_id,
            "structural_time": self.structural_time,
            "knowledge_time": self.knowledge_time,
            "absorption_level": self.absorption_level,
            "absorbing_id": self.absorbing_id,
            "shadow_id": self.shadow_id,
            "close_reason": self.close_reason,
            "created_at_seq": self.created_at_seq,
            "closed_at_seq": self.closed_at_seq,
            "commits": list(self.commits),
        }


@dataclass
class CandidateShadow:
    """Geometria de un candidato absorbido.

    Impide recrear un candidato equivalente dentro de la misma generacion
    mientras el nuevo no supere el extremo de la sombra con evidencia
    estructural. Sin sombra, el motor recrea y reabsorbe el mismo candidato.
    """
    shadow_id: str
    role: str
    direction: int
    origin: int
    extreme: int
    generation_id: str
    absorbed_at_seq: int
    released_at_seq: int = 0

    def blocks(self, role: str, direction: int, generation_id: str,
               extreme: int) -> bool:
        if self.released_at_seq:
            return False
        if role != self.role or generation_id != self.generation_id:
            return False
        if direction == self.direction:
            # mismo rol y direccion: bloquea hasta superar el extremo sombra
            return (extreme - self.extreme) * direction <= 0
        # direccion contraria: el candidato es otro objeto estructural
        return False


# --------------------------------------------------------------------- preguntas
@dataclass
class TreeQuestion:
    question_id: str
    owner_branch_id: str
    owner_generation_id: str
    current_node: str
    roles_allowed: tuple = ()
    anchor_reference_id: str = ""
    consumes: tuple = ()
    physical_requirement: int = 0
    structural_requirement: str = "RETENTION"
    confirmation_condition: str = ""
    rejection_condition: str = ""
    absorption_condition: str = ""
    expiry_condition: str = ""
    next_node_if_yes: str = ""
    next_node_if_no: str = ""
    priority: int = 100
    authority: str = "CANONICAL_RULE"
    opened_at_seq: int = 0
    closed_at_seq: int = 0
    answer: str = ""
    rejected_hypotheses: list = field(default_factory=list)

    def allows_role(self, role: str) -> bool:
        return role in self.roles_allowed

    def snapshot(self) -> dict:
        return {
            "question_id": self.question_id,
            "owner_branch_id": self.owner_branch_id,
            "owner_generation_id": self.owner_generation_id,
            "current_node": self.current_node,
            "roles_allowed": list(self.roles_allowed),
            "anchor_reference_id": self.anchor_reference_id,
            "consumes": list(self.consumes),
            "physical_requirement": self.physical_requirement,
            "structural_requirement": self.structural_requirement,
            "confirmation_condition": self.confirmation_condition,
            "priority": self.priority,
            "authority": self.authority,
            "opened_at_seq": self.opened_at_seq,
            "closed_at_seq": self.closed_at_seq,
            "answer": self.answer,
            "rejected_hypotheses": list(self.rejected_hypotheses),
        }


class QuestionBook:
    def __init__(self, branch_id: str, violations: ViolationLedger) -> None:
        self.branch_id = branch_id
        self.violations = violations
        self.questions: dict[str, TreeQuestion] = {}
        self.order: list[str] = []

    def open(self, q: TreeQuestion) -> TreeQuestion:
        self.questions[q.question_id] = q
        self.order.append(q.question_id)
        return q

    def current(self) -> TreeQuestion | None:
        live = [self.questions[qid] for qid in self.order
                if not self.questions[qid].closed_at_seq]
        if not live:
            return None
        live.sort(key=lambda q: (q.priority, -q.opened_at_seq))
        return live[0]

    def check_read(self, q: TreeQuestion, reference_id: str,
                   owner_branch: str, owner_generation: str,
                   seq: int = -1) -> bool:
        """`consumes` es una lista cerrada. Cualquier lectura fuera de ella o
        de otro propietario es violacion, no decision silenciosa."""
        if owner_branch != q.owner_branch_id:
            self.violations.hit(
                "cross_owner_reference_reads",
                f"{reference_id} de rama {owner_branch} leida por "
                f"{q.question_id} de rama {q.owner_branch_id}", seq)
            return False
        if owner_generation != q.owner_generation_id:
            self.violations.hit(
                "cross_owner_reference_reads",
                f"{reference_id} de generacion {owner_generation} leida por "
                f"{q.question_id} de generacion {q.owner_generation_id}", seq)
            return False
        if reference_id not in q.consumes:
            self.violations.hit(
                "consumes_violations",
                f"{q.question_id} intento leer {reference_id} fuera de consumes",
                seq)
            return False
        return True

    def close(self, question_id: str, answer: str, seq: int) -> None:
        q = self.questions[question_id]
        q.answer = answer
        q.closed_at_seq = seq

    def snapshot(self) -> list:
        return [self.questions[qid].snapshot() for qid in self.order]


# --------------------------------------------------------------------- estado
class ConfirmedState:
    """Estado funcional confirmado. Solo `apply` escribe, y `apply` exige un
    FunctionalCommit valido. Cualquier otra escritura es una violacion."""

    def __init__(self, violations: ViolationLedger) -> None:
        self.violations = violations
        self.fields: dict[str, Any] = {}
        self.version = 0
        self.history: list[dict] = []
        self._open_ticket: FunctionalCommit | None = None

    # -- lectura
    def get(self, name: str, default: Any = None) -> Any:
        return self.fields.get(name, default)

    def snapshot(self) -> dict:
        return dict(self.fields)

    # -- escritura
    def begin(self, commit: "FunctionalCommit") -> None:
        self._open_ticket = commit

    def apply(self, commit: "FunctionalCommit") -> None:
        if self._open_ticket is not commit:
            self.violations.hit(
                "candidate_state_writes",
                f"escritura sin ticket valido ({commit.kind})", commit.seq)
            raise ArchitectureViolation("CONFIRMED_STATE_WRITE_WITHOUT_COMMIT")
        for name, value in commit.writes.items():
            self.fields[name] = value
        self.version += 1
        self.history.append({"seq": commit.seq, "kind": commit.kind,
                             "question_id": commit.question_id,
                             "candidate_id": commit.candidate_id,
                             "fields": sorted(commit.writes)})
        self._open_ticket = None

    def direct_write(self, name: str, value: Any, seq: int = -1) -> None:
        self.violations.hit("candidate_state_writes",
                            f"escritura directa de {name} sin commit", seq)
        raise ArchitectureViolation("CANDIDATE_STATE_WRITE_VIOLATION")


# --------------------------------------------------------------------- commits
@dataclass
class FunctionalCommit:
    kind: str
    branch_id: str
    generation_id: str
    question_id: str
    candidate_id: str
    seq: int
    writes: dict
    reads: tuple = ()
    created_at_seq: int = 0
    authority: str = "CANONICAL_RULE"

    def validate(self, tracker: "CandidateTracker", book: QuestionBook,
                 violations: ViolationLedger) -> None:
        if not self.question_id:
            raise ArchitectureViolation("COMMIT_WITHOUT_QUESTION")
        q = book.questions.get(self.question_id)
        if q is None:
            raise ArchitectureViolation(f"COMMIT_UNKNOWN_QUESTION {self.question_id}")
        if q.closed_at_seq and q.answer != "YES" and self.kind in (CONFIRM, EXTEND):
            raise ArchitectureViolation("COMMIT_ON_CLOSED_QUESTION")
        if self.generation_id != q.owner_generation_id:
            violations.hit("cross_owner_reference_reads",
                           f"commit de {self.generation_id} sobre pregunta de "
                           f"{q.owner_generation_id}", self.seq)
            raise ArchitectureViolation("CROSS_GENERATION_COMMIT")

        c = tracker.get(self.candidate_id) if self.candidate_id else None
        if self.candidate_id and c is None:
            violations.hit("unowned_candidates",
                           f"commit sobre candidato inexistente {self.candidate_id}",
                           self.seq)
            raise ArchitectureViolation("COMMIT_WITHOUT_CANDIDATE")
        if c is not None:
            if c.owner_branch_id != self.branch_id:
                violations.hit("unowned_candidates",
                               f"candidato de rama {c.owner_branch_id}", self.seq)
                raise ArchitectureViolation("COMMIT_FOREIGN_BRANCH")
            if c.status in TERMINAL:
                raise ArchitectureViolation("COMMIT_ON_CLOSED_CANDIDATE")
            if self.kind == ADMIT and not q.allows_role(c.role_hypothesis):
                raise ArchitectureViolation("COMMIT_ROLE_NOT_ALLOWED")
            if self.kind == CONFIRM:
                # veto de nacimiento: no se confirma con la evidencia que creo
                # el candidato; se exige un tick posterior y retencion superada.
                if self.seq <= c.created_at_seq:
                    violations.hit(
                        "same_tick_confirmation",
                        f"{c.candidate_id} confirmado en su tick de alta "
                        f"({self.seq})", self.seq)
                    raise ArchitectureViolation(
                        "SAME_BIRTH_AND_CONFIRMATION_EVIDENCE")
                if q.structural_requirement == "RETENTION" and c.retention_tests < 1:
                    raise ArchitectureViolation("CONFIRM_WITHOUT_RETENTION")
        for ref, owner_branch, owner_gen in self.reads:
            if not book.check_read(q, ref, owner_branch, owner_gen, self.seq):
                raise ArchitectureViolation(
                    f"REFERENCE_NOT_CONSUMED {ref} por {q.question_id}")
        if self.kind == CONFIRM:
            # confirmar exige pregunta en YES
            if q.answer not in ("YES", ""):
                raise ArchitectureViolation("CONFIRM_ON_REJECTED_QUESTION")


# --------------------------------------------------------------------- tracker
class CandidateTracker:
    """Registro de candidatos de una rama.

    Deliberadamente no recibe ninguna referencia al Reading: no puede escribir
    el estado funcional ni por error. La unica salida es un FunctionalCommit.
    """

    def __init__(self, branch_id: str, generation_id: str,
                 violations: ViolationLedger) -> None:
        self.branch_id = branch_id
        self.generation_id = generation_id
        self.violations = violations
        self.candidates: dict[str, CandidateRecord] = {}
        self.shadows: list[CandidateShadow] = []
        self._n = 0
        self.counters = {s: 0 for s in (OBSERVED, PHYSICAL, STRUCTURAL,
                                        CONFIRMED, ABSORBED, DISCARDED,
                                        RECLASSIFIED)}
        self.recreation_attempts = 0

    # -- alta
    def observe(self, role: str, direction: int, origin: int, origin_seq: int,
                extreme: int, extreme_seq: int, source_function_id: str,
                size: int, minimum: int) -> CandidateRecord:
        """Movimiento inferior al minimo fisico: se conserva para auditoria,
        nunca alimenta el arbol."""
        return self._new(role, direction, origin, origin_seq, extreme,
                         extreme_seq, source_function_id, size, minimum,
                         OBSERVED)

    def admit(self, role: str, direction: int, origin: int, origin_seq: int,
              extreme: int, extreme_seq: int, source_function_id: str,
              size: int, minimum: int, question_id: str = "") -> CandidateRecord:
        """Desplazamiento fisico suficiente: crea candidato PHYSICAL.
        No crea A, B, C, modulo, FT, TT ni rama.

        Un movimiento por debajo del minimo fisico NO puede admitirse como
        PHYSICAL: solo existe como OBSERVED (auditoria)."""
        if size < minimum:
            self.violations.hit(
                "unowned_candidates",
                f"ADMIT_BELOW_PHYSICAL_MINIMUM {role} size={size} < {minimum}",
                extreme_seq)
            raise ArchitectureViolation(
                f"ADMIT_BELOW_PHYSICAL_MINIMUM:{size}<{minimum}")
        rec = self._new(role, direction, origin, origin_seq, extreme,
                        extreme_seq, source_function_id, size, minimum,
                        PHYSICAL, question_id)
        return rec

    def _new(self, role, direction, origin, origin_seq, extreme, extreme_seq,
             source_function_id, size, minimum, status,
             question_id="") -> CandidateRecord:
        for sh in self.shadows:
            if sh.blocks(role, direction, self.generation_id, extreme):
                self.recreation_attempts += 1
                self.violations.hit(
                    "shadow_recreations_blocked",
                    f"{role} {direction} en {extreme} bloqueado por {sh.shadow_id}",
                    extreme_seq)
                # el candidato se registra DEScartado: no alimenta el arbol
                status = DISCARDED
                break
        self._n += 1
        cid = f"{self.branch_id}-{self.generation_id}-C{self._n:03d}-{role}"
        rec = CandidateRecord(
            candidate_id=cid, owner_branch_id=self.branch_id,
            owner_generation_id=self.generation_id,
            source_function_id=source_function_id, role_hypothesis=role,
            direction=direction, origin=origin, origin_seq=origin_seq,
            extreme=extreme, extreme_seq=extreme_seq, status=status,
            physical_size=size, physical_requirement=minimum,
            question_id=question_id, created_at_seq=extreme_seq)
        if status == DISCARDED:
            rec.close_reason = "SHADOW_BLOCKED"
            rec.closed_at_seq = extreme_seq
            rec.absorption_level = AT_BIRTH
        self.candidates[cid] = rec
        self.counters[status] = self.counters.get(status, 0) + 1
        return rec

    def get(self, candidate_id: str) -> CandidateRecord | None:
        return self.candidates.get(candidate_id)

    # -- evolucion
    def extend(self, candidate_id: str, price: int, seq: int) -> None:
        c = self.candidates[candidate_id]
        if c.status in TERMINAL:
            return
        if (price - c.extreme) * c.direction > 0:
            c.extreme = price
            c.extreme_seq = seq
            c.physical_size = abs(c.extreme - c.origin)

    def promote_physical(self, candidate_id: str, seq: int) -> None:
        """El movimiento alcanzo el minimo fisico DESPUES del alta: el
        candidato observado pasa a PHYSICAL. No crea funcion."""
        c = self.candidates[candidate_id]
        if c.status != OBSERVED:
            return
        if c.size < c.physical_requirement:
            return
        c.status = PHYSICAL
        c.physical_size = c.size
        c.extreme_seq = seq
        self.counters[OBSERVED] = max(0, self.counters.get(OBSERVED, 1) - 1)
        self.counters[PHYSICAL] = self.counters.get(PHYSICAL, 0) + 1

    def retention(self, candidate_id: str, seq: int) -> None:
        """Test de retencion superado: el propietario no ha recuperado el
        origen del candidato. No es un contador de extensiones."""
        c = self.candidates[candidate_id]
        if c.status in (PHYSICAL, OBSERVED):
            c.status = STRUCTURAL
            c.retention_tests += 1
            c.structural_time = c.extreme_seq
            c.knowledge_time = seq
            self.counters[PHYSICAL] = max(0, self.counters.get(PHYSICAL, 1) - 1)
            self.counters[STRUCTURAL] = self.counters.get(STRUCTURAL, 0) + 1

    def reclaim(self, candidate_id: str, seq: int, absorbing_id: str) -> None:
        """El propietario re-extensiona mas alla del origen del candidato."""
        c = self.candidates[candidate_id]
        c.owner_reclaimed = True
        self.absorb(candidate_id, seq, absorbing_id, "OWNER_RECLAIMED")

    def absorb(self, candidate_id: str, seq: int, absorbing_id: str,
               reason: str) -> CandidateShadow | None:
        c = self.candidates[candidate_id]
        if c.status in TERMINAL:
            return None
        level = {OBSERVED: AT_BIRTH, PHYSICAL: AT_PHYSICAL,
                 STRUCTURAL: AT_STRUCTURAL}.get(c.status, AT_FUNCTIONAL)
        c.status = ABSORBED
        c.absorption_level = level
        c.absorbing_id = absorbing_id
        c.close_reason = reason
        c.closed_at_seq = seq
        self.counters[ABSORBED] = self.counters.get(ABSORBED, 0) + 1
        sh = CandidateShadow(
            shadow_id=f"{c.candidate_id}-SH",
            role=c.role_hypothesis, direction=c.direction,
            origin=c.origin, extreme=c.extreme,
            generation_id=self.generation_id, absorbed_at_seq=seq)
        c.shadow_id = sh.shadow_id
        self.shadows.append(sh)
        return sh

    def discard(self, candidate_id: str, seq: int, reason: str) -> None:
        c = self.candidates[candidate_id]
        c.status = DISCARDED
        c.close_reason = reason
        c.closed_at_seq = seq
        self.counters[DISCARDED] = self.counters.get(DISCARDED, 0) + 1

    def reclassify(self, candidate_id: str, seq: int, new_role: str,
                   reason: str) -> CandidateRecord:
        c = self.candidates[candidate_id]
        c.status = RECLASSIFIED
        c.close_reason = f"RECLASSIFIED_AS_{new_role}:{reason}"
        c.closed_at_seq = seq
        self.counters[RECLASSIFIED] = self.counters.get(RECLASSIFIED, 0) + 1
        return self._new(new_role, c.direction, c.origin, c.origin_seq,
                         c.extreme, c.extreme_seq, c.source_function_id,
                         c.size, c.physical_requirement, PHYSICAL)

    def release_shadow(self, shadow_id: str, seq: int) -> None:
        for sh in self.shadows:
            if sh.shadow_id == shadow_id:
                sh.released_at_seq = seq
                return
        raise ArchitectureViolation(f"SHADOW_INEXISTENTE {shadow_id}")

    def mark_confirmed(self, candidate_id: str, seq: int) -> None:
        c = self.candidates[candidate_id]
        c.status = CONFIRMED
        c.knowledge_time = c.knowledge_time or seq
        self.counters[CONFIRMED] = self.counters.get(CONFIRMED, 0) + 1

    # -- informes
    def metrics(self) -> dict:
        levels: dict[str, int] = {}
        for c in self.candidates.values():
            if c.status == ABSORBED:
                levels[c.absorption_level] = levels.get(c.absorption_level, 0) + 1
        return {"total": len(self.candidates),
                "by_status": dict(self.counters),
                "absorption_levels": levels,
                "shadows": len(self.shadows),
                "recreation_attempts": self.recreation_attempts}

    def snapshot(self) -> list:
        return [c.snapshot() for c in self.candidates.values()]


# --------------------------------------------------------------------- runtime
class BranchRuntime:
    """Union por rama: tracker + preguntas + estado confirmado + violaciones."""

    def __init__(self, branch_id: str, generation_id: str = "G1",
                 violations: ViolationLedger | None = None) -> None:
        self.branch_id = branch_id
        self.generation_id = generation_id
        self.violations = violations or ViolationLedger()
        self.tracker = CandidateTracker(branch_id, generation_id,
                                        self.violations)
        self.book = QuestionBook(branch_id, self.violations)
        self.state = ConfirmedState(self.violations)
        self.commits: list[FunctionalCommit] = []
        self._q = 0

    # -- generacion
    def new_generation(self, generation_id: str) -> None:
        self.generation_id = generation_id
        self.tracker.generation_id = generation_id

    def archive_generation(self, seq: int) -> dict:
        """Una generacion archivada no acepta escrituras funcionales."""
        live = self.tracker.metrics()["by_status"].get(STRUCTURAL, 0)
        return {"generation_id": self.generation_id, "archived_at_seq": seq,
                "open_structural": live}

    # -- preguntas
    def current_question(self) -> "TreeQuestion | None":
        return self.book.current()

    def open_question(self, node: str, roles: Iterable[str], consumes: Iterable[str],
                      seq: int, anchor: str = "", priority: int = 100,
                      physical: int = 0, structural: str = "RETENTION",
                      authority: str = "CANONICAL_RULE") -> TreeQuestion:
        self._q += 1
        q = TreeQuestion(
            question_id=f"{self.branch_id}-Q{self._q:03d}-{node}",
            owner_branch_id=self.branch_id,
            owner_generation_id=self.generation_id,
            current_node=node, roles_allowed=tuple(roles),
            anchor_reference_id=anchor, consumes=tuple(consumes),
            physical_requirement=physical, structural_requirement=structural,
            priority=priority, authority=authority, opened_at_seq=seq)
        return self.book.open(q)

    # -- commits
    def commit(self, kind: str, question_id: str, candidate_id: str, seq: int,
               writes: dict, reads: Iterable[tuple] = ()) -> FunctionalCommit:
        c = FunctionalCommit(
            kind=kind, branch_id=self.branch_id,
            generation_id=self.generation_id, question_id=question_id,
            candidate_id=candidate_id, seq=seq, writes=dict(writes),
            reads=tuple(reads), created_at_seq=seq)
        c.validate(self.tracker, self.book, self.violations)
        self.state.begin(c)
        self.state.apply(c)
        if candidate_id:
            cand = self.tracker.get(candidate_id)
            if cand is not None:
                cand.commits.append(kind)
                if kind == CONFIRM:
                    self.tracker.mark_confirmed(candidate_id, seq)
        self.commits.append(c)
        return c

    # -- informes
    def metrics(self) -> dict:
        return {"branch_id": self.branch_id,
                "generation_id": self.generation_id,
                "candidates": self.tracker.metrics(),
                "questions": len(self.book.order),
                "open_questions": len([q for q in self.book.order
                                       if not self.book.questions[q].closed_at_seq]),
                "commits": len(self.commits),
                "state_version": self.state.version,
                "violations": self.violations.summary()}

    def snapshot(self) -> dict:
        return {"branch_id": self.branch_id,
                "generation_id": self.generation_id,
                "candidates": self.tracker.snapshot(),
                "questions": self.book.snapshot(),
                "confirmed_state": self.state.snapshot(),
                "commits": [{"kind": c.kind, "seq": c.seq,
                             "question_id": c.question_id,
                             "candidate_id": c.candidate_id,
                             "fields": sorted(c.writes)} for c in self.commits]}
