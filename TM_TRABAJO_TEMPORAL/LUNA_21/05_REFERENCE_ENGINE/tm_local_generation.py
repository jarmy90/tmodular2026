"""Iteracion 22 — LOCAL-G2: rama local limpia, con propietario y preguntas.

Reglas de la iteracion:

* LOCAL-G2 NO hereda nada de LOCAL-G1 ni de PRIMARY-G1. Se crea con estado
  confirmado vacio, tracker vacio y su propio QuestionBook.
* `parent_context_id` es solo descriptivo: no concede autoridad sobre las
  referencias de la rama principal.
* Toda transicion funcional (A confirmada, B confirmada, B Grande, AUT, TT)
  pasa por `TreeQuestion` + `FunctionalCommit`. Ningun candidato escribe el
  estado confirmado.
* El conocimiento es posterior al origen: `structural_time` es el tick del
  extremo, `knowledge_time` el tick que confirma. Antes de `knowledge_time`
  la estructura existe como CANDIDATE y no como funcion.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from tm_candidates import (
    ABSORBED, CONFIRM, ArchitectureViolation, BranchRuntime, ViolationLedger,
)

MAIN = "MAIN"
LOCAL = "LOCAL"

LOCAL_CANDIDATE = "LOCAL_CANDIDATE"
LOCAL_CONFIRMED = "LOCAL_CONFIRMED"
LOCAL_DOMINANT = "LOCAL_DOMINANT"
LOCAL_ABSORBED = "LOCAL_ABSORBED"
LOCAL_INTEGRATED = "LOCAL_INTEGRATED"
LOCAL_ARCHIVED = "LOCAL_ARCHIVED"

B_PHYSICAL = "B_PHYSICAL"
B_CANDIDATE_CONFIRMED = "B_CANDIDATE_CONFIRMED"
B_GRANDE = "B_GRANDE"
AUT = "AUT"

#: minimo fisico (1 punto = 100). Se inyecta; nunca se asume.
DEFAULT_MINIMUM = 200


@dataclass
class LocalBranch:
    """Rama local con referencias propias.

    `generation_id` es unico por rama: cualquier lectura cruzada entre LOCAL-G1,
    LOCAL-G2 y PRIMARY-G1 produce CROSS_OWNER_REFERENCE_VIOLATION en el
    QuestionBook.
    """

    generation_id: str = "LOCAL-G2"
    parent_context_id: str = "PRIMARY-G1"
    status: str = LOCAL_CANDIDATE
    minimum: int = DEFAULT_MINIMUM
    slot: str = LOCAL
    seed_seq: int = 0
    seed_price: int = 0
    seed_reason: str = "MAIN_EXHAUSTED_AT_CLOSE"
    violations: ViolationLedger = field(default_factory=ViolationLedger)

    # -- estructura descubierta (todo con propietario LOCAL-G2)
    module_origin: int = 0
    module_origin_seq: int = 0
    module_extreme: int = 0
    module_extreme_seq: int = 0
    module_size: int = 0
    module_dir: int = 0
    module_status: str = ""
    module_structural_time: int = 0
    module_knowledge_time: int = 0

    a_origin: int = 0
    a_origin_seq: int = 0
    a_extreme: int = 0
    a_extreme_seq: int = 0
    a_size: int = 0
    a_dir: int = 0
    a_status: str = ""
    a_structural_time: int = 0
    a_knowledge_time: int = 0

    b_origin: int = 0
    b_origin_seq: int = 0
    b_extreme: int = 0
    b_extreme_seq: int = 0
    b_size: int = 0
    b_dir: int = 0
    b_status: str = ""
    b_ratio: float = 0.0
    b_100_level: int = 0
    b_limit_level: int = 0

    tt_id: str = ""
    tt_status: str = ""
    tt_dir: int = 0
    tt_final_a: int = 0
    tt_objective: int = 0
    tt_invalidation: int = 0
    tt_structural_time: int = 0
    tt_knowledge_time: int = 0
    tt_first_boundary: str = ""

    aut_level: int = 0
    events: list[dict] = field(default_factory=list)
    commits: list[dict] = field(default_factory=list)
    authority: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Estado completamente vacio: ninguna referencia heredada.
        self.rt = BranchRuntime(self.generation_id, self.generation_id,
                                self.violations)
        self._dir_lock = 0
        self._contrary_seen = 0
        self._a_extended = False
        self._b_extended = False
        self._last_seq = 0
        self.integrated_at_seq = 0
        self.integration_reason = ""

    # -- utilidades
    def ev(self, t, name: str, detail: str = "") -> None:
        self.events.append({"seq": getattr(t, "seq", -1),
                            "time_ms": getattr(t, "time_ms", 0),
                            "event": name, "detail": detail})

    def _q(self, node: str, roles: Iterable[str], seq: int) -> str:
        key = (node, tuple(roles))
        if key in self.authority:
            return self.authority[key]
        q = self.rt.open_question(node, roles,
                                  (f"{self.generation_id}:{node}",), seq,
                                  anchor=f"{self.generation_id}:MODULE")
        self.authority[key] = q.question_id
        return q.question_id

    def _commit(self, kind: str, node: str, roles: Iterable[str], seq: int,
                writes: dict, reads: Iterable[tuple] = ()) -> bool:
        qid = self._q(node, roles, seq)
        try:
            c = self.rt.commit(kind, qid, "", seq, writes, reads)
        except ArchitectureViolation as exc:  # pragma: no cover - defensivo
            self.ev(type("T", (), {"seq": seq, "time_ms": 0})(),
                    "LOCAL_COMMIT_REJECTED", str(exc))
            return False
        self.commits.append({"seq": seq, "node": node, "kind": kind,
                            "fields": sorted(writes)})
        return True

    # -- consumo de ticks
    def seed(self, t) -> None:
        if self.seed_seq:
            return
        self.seed_seq = t.seq
        self.seed_price = t.price
        self.ev(t, "LOCAL_SEEDED",
                f"origin={t.price} reason={self.seed_reason} "
                f"slot={self.slot} parent={self.parent_context_id}")

    def feed(self, t) -> None:
        if not self.seed_seq:
            self.seed(t)
        self._last_seq = t.seq
        # 1) el modulo dominante se actualiza siempre: una retraccion interna
        #    no lo divide, y su reanudacion absorbe al candidato A.
        self._module_tick(t)
        # 2) TT pendiente: arbitraje cronologico objetivo vs invalidacion.
        if self.tt_status == "TT_PENDING":
            self._tt_tick(t)
        if not self._dir_lock:
            return
        # 3) A local
        if not self.a_status:
            self._maybe_open_a(t)
            return
        if self.a_status == "CANDIDATE":
            self._a_develop(t)
            return
        # 4) B local
        if not self.b_status:
            self._b_open(t)
            return
        if self.b_status in (B_PHYSICAL, B_CANDIDATE_CONFIRMED):
            self._b_develop(t)
        elif self.b_status in (B_GRANDE, AUT):
            self._after_b_grande(t)

    # -- modulo local
    def _module_tick(self, t) -> None:
        """Modulo = excursion DOMINANTE desde la semilla.

        El umbral fisico no crea el modulo: solo separa desplazamiento de
        ruido. Cuando existen dos excursiones validas, la dominante define la
        direccion y su origen es el extremo previo (no la semilla), porque el
        movimiento dominante empieza donde empieza su recorrido.
        """
        if not self.module_origin:
            self.module_origin = t.price
            self.module_origin_seq = t.seq
            self.module_structural_time = t.time_ms
            self.up_extreme = self.down_extreme = t.price
            self.up_seq = self.down_seq = t.seq
            return
        if t.price > self.up_extreme:
            self.up_extreme, self.up_seq = t.price, t.seq
        if t.price < self.down_extreme:
            self.down_extreme, self.down_seq = t.price, t.seq
        up = self.up_extreme - self.module_origin
        down = self.module_origin - self.down_extreme
        # La direccion se decide UNA vez, cuando existen dos excursiones
        # fisicas validas, y se elige la mayor. No se recalcula tick a tick:
        # recalcular permitia que el rebote reescribiera el propietario del
        # movimiento dominante.
        retr_up = self.up_extreme - t.price
        retr_dn = t.price - self.down_extreme
        if not self._dir_lock and (retr_up >= self.minimum
                                   or retr_dn >= self.minimum) \
                and max(up, down) >= self.minimum:
            if down >= up:
                self._dir_lock = -1
                self.module_origin, self.module_origin_seq = (self.up_extreme,
                                                              self.up_seq)
                self.module_extreme, self.module_extreme_seq = (
                    self.down_extreme, self.down_seq)
            else:
                self._dir_lock = 1
                self.module_origin, self.module_origin_seq = (
                    self.down_extreme, self.down_seq)
                self.module_extreme, self.module_extreme_seq = (
                    self.up_extreme, self.up_seq)
            self.module_dir = self._dir_lock
            self.module_size = abs(self.module_extreme - self.module_origin)
            self.ev(t, "LOCAL_DOMINANT_DIRECTION",
                    f"dir={self.module_dir} origin={self.module_origin} "
                    f"extreme={self.module_extreme} size={self.module_size}")
        if not self._dir_lock:
            return
        self.module_dir = self._dir_lock
        self.module_size = abs(self.module_extreme - self.module_origin)
        d = self.module_dir
        if (t.price - self.module_extreme) * d > 0:
            self.module_extreme = t.price
            self.module_extreme_seq = t.seq
            self.module_size = abs(self.module_extreme - self.module_origin)
            return
        # la reanudacion del modulo absorbe el candidato A si lo hay
        if (self.a_status == "CANDIDATE" and self.a_origin
                and (t.price - self.a_origin) * d > 0):
            self.a_status = ""
            self.a_origin = 0
            self.a_extreme = 0
            self.a_size = 0
            self.ev(t, "LOCAL_A_ABSORBED_IN_MODULE",
                    f"modulo={self.module_size} en {self.module_extreme}")

    # -- A local
    def _maybe_open_a(self, t) -> None:
        """A local solo nace de un retroceso autónomo desde el extremo del
        movimiento dominante, no de cada oscilación."""
        if not self._dir_lock or not self.module_extreme:
            return
        retr = (self.module_extreme - t.price) * self.module_dir
        if retr < self.minimum:
            return
        self.a_origin = self.module_extreme
        self.a_origin_seq = self.module_extreme_seq
        self.a_structural_time = self.module_structural_time
        self.a_status = "CANDIDATE"
        self.a_dir = -self.module_dir
        self.a_extreme = t.price
        self.a_extreme_seq = t.seq
        self.a_size = abs(self.a_extreme - self.a_origin)
        self.ev(t, "LOCAL_A_CANDIDATE",
                f"origin={self.a_origin} extreme={self.a_extreme} "
                f"size={self.a_size} dir={self.a_dir}")
        self._a_develop(t)

    def _a_develop(self, t) -> None:
        d = self.a_dir
        # la funcion dominante se reanuda mas alla del origen de A: A absorbida
        if self.module_dir and (t.price - self.a_origin) * self.module_dir > 0:
            self.a_status = ""
            self.a_origin = self.a_extreme = self.a_size = 0
            self.ev(t, "LOCAL_A_ABSORBED_IN_MODULE",
                    f"reanudacion del dominante en {self.module_extreme}")
            return
        if not self.a_extreme:
            self.a_extreme, self.a_extreme_seq = t.price, t.seq
            self.a_size = abs(self.a_extreme - self.a_origin)
            return
        if (t.price - self.a_extreme) * d > 0:
            self.a_extreme = t.price
            self.a_extreme_seq = t.seq
            self.a_size = abs(self.a_extreme - self.a_origin)
            return
        # retroceso contrario a A: candidato B (mismo propietario, misma A)
        if not self.a_extreme or self.a_size < self.minimum:
            return
        move = abs(t.price - self.a_extreme)
        if move < self.minimum:
            return
        if self.a_status != "A_CONFIRMED":
            if not self._commit(CONFIRM, "LOCAL_A_DEVELOPMENT", ("A",),
                                t.seq, {"a_status": "A_CONFIRMED"}):
                return
            self.a_status = "A_CONFIRMED"
            self.a_knowledge_time = t.time_ms
            self.a_size = abs(self.a_extreme - self.a_origin)
            self.status = LOCAL_CONFIRMED
            # A confirmada => el movimiento dominante queda declarado como
            # modulo por descarte (fin de la fase provisional)
            if not self.module_status:
                self.module_status = "LOCAL_MODULE_BY_DISCARD"
                self.module_knowledge_time = t.time_ms
                self.ev(t, "LOCAL_MODULE_DECLARED",
                        f"origin={self.module_origin} "
                        f"extreme={self.module_extreme} "
                        f"size={self.module_size} dir={self.module_dir} "
                        f"st={self.module_structural_time} kt={t.time_ms}")
            # Regla canonica (identica a MAIN): una A mayor que el modulo por
            # descarte deviene el modulo del ciclo, no un retroceso interno.
            if self.a_size > self.module_size:
                self.module_origin = self.a_origin
                self.module_origin_seq = self.a_origin_seq
                self.module_extreme = self.a_extreme
                self.module_extreme_seq = self.a_extreme_seq
                self.module_size = self.a_size
                self.module_dir = self.a_dir
                self.module_status = "LOCAL_MODULE_BY_DISCARD_A"
                self.module_knowledge_time = t.time_ms
                self.ev(t, "LOCAL_MODULE_BY_DISCARD_A",
                        f"A={self.a_size} > modulo previo: A deviene modulo "
                        f"origin={self.module_origin} "
                        f"extreme={self.module_extreme}")
            self.ev(t, "LOCAL_A_CONFIRMED",
                    f"A local={self.a_origin}->{self.a_extreme} size={self.a_size} "
                    f"b_ratio pendiente de B")
        self._b_open(t)

    def _b_open(self, t) -> None:
        self.b_status = B_PHYSICAL
        self.b_dir = -self.a_dir
        self.b_origin = self.a_extreme
        self.b_origin_seq = self.a_extreme_seq
        self.b_extreme = t.price
        self.b_extreme_seq = t.seq
        self.b_size = abs(self.b_extreme - self.b_origin)
        self.b_100_level = self.a_size
        self.b_limit_level = self.a_size * 127 // 100 + 25
        self.ev(t, "LOCAL_B_OPENED",
                f"origin={self.b_origin} extreme={self.b_extreme} "
                f"A={self.a_size} 100%={self.b_100_level} "
                f"127%+0,25={self.b_limit_level}")

    def _b_develop(self, t) -> None:
        d = self.b_dir
        if (t.price - self.b_extreme) * d > 0:
            self.b_extreme = t.price
            self.b_extreme_seq = t.seq
            self.b_size = abs(self.b_extreme - self.b_origin)
            self._b_extended = True
        elif (t.price - self.b_origin) * -d >= 0 and self.b_status == B_PHYSICAL:
            # el propietario recupera el origen de B: B absorbida (sin sombra
            # funcional, se conserva como candidato cerrado)
            self.b_status = ""
            self.b_extreme = 0
            self.b_size = 0
            return
        if self.a_size:
            self.b_ratio = round(self.b_size / self.a_size, 4)
        if self.b_status == B_PHYSICAL and self._b_extended \
                and self.b_size >= self.minimum:
            if not self._commit(CONFIRM, "LOCAL_B_DEVELOPMENT", ("B",), t.seq,
                                {"b_status": B_CANDIDATE_CONFIRMED}):
                return
            self.b_status = B_CANDIDATE_CONFIRMED
            # B funcional delimita A: su extremo se congela
            self.a_size = abs(self.a_extreme - self.a_origin)
            self.ev(t, "LOCAL_B_CONFIRMED",
                    f"B={self.b_size} A congelada={self.a_size} "
                    f"ratio={self.b_ratio}")
            return
        if self.b_status != B_CANDIDATE_CONFIRMED:
            return
        if self.b_size > self.b_limit_level:
            if self._commit(CONFIRM, "LOCAL_B_LIMIT", ("B",), t.seq,
                            {"b_status": AUT}):
                self.b_status = AUT
                self.ev(t, "LOCAL_AUT",
                        f"B={self.b_size} supera 127%+0,25={self.b_limit_level} "
                        f"de A={self.a_size} -> AUT")
                self._arm_local_tt(t)
            return
        if self.b_size >= self.b_100_level:
            if self._commit(CONFIRM, "LOCAL_B_GRANDE_CONFIRMATION", ("B",),
                            t.seq, {"b_status": B_GRANDE}):
                self.b_status = B_GRANDE
                self.ev(t, "LOCAL_B_GRANDE",
                        f"B={self.b_size} alcanza 100% de A={self.a_size}")

    def _arm_local_tt(self, t) -> None:
        """TT local: propietario LOCAL-G2, modulo y final_A propios."""
        if self.tt_status:
            return
        self.tt_id = f"{self.generation_id}-TT-001"
        self.tt_dir = self.b_dir
        self.tt_final_a = self.b_origin
        self.tt_objective = self.b_origin + self.b_dir * self.module_size
        self.tt_invalidation = self.a_origin
        self.tt_structural_time = self.b_origin_seq and self.a_structural_time or 0
        self.tt_knowledge_time = t.time_ms
        self.tt_status = "TT_PENDING"
        self.ev(t, "LOCAL_TT_ARMED",
                f"id={self.tt_id} dir={self.tt_dir} final_A={self.tt_final_a} "
                f"objetivo={self.tt_objective} modulo={self.module_size} "
                f"invalidacion={self.tt_invalidation}")

    def _tt_tick(self, t) -> None:
        d = self.tt_dir
        if not d:
            return
        # orden cronologico estricto dentro del tick: primero invalidacion
        inval = (t.price - self.tt_invalidation) * d < 0
        if inval:
            self.tt_status = "TT_FAILED"
            self.tt_first_boundary = f"INVALIDATION@{t.seq}"
            self.ev(t, "LOCAL_TT_FAILED",
                    f"invalidacion {self.tt_invalidation} tocada en {t.price} "
                    f"antes del objetivo {self.tt_objective}")
            return
        reached = (t.price - self.tt_objective) * d >= 0
        if reached:
            self.tt_status = "TT_CONFIRMED"
            self.tt_first_boundary = f"OBJECTIVE@{t.seq}"
            self.ev(t, "LOCAL_TT_CONFIRMED",
                    f"objetivo {self.tt_objective} alcanzado en {t.price}")

    def _after_b_grande(self, t) -> None:
        if self.b_status == B_GRANDE:
            contr = (t.price - self.b_extreme) * (-self.b_dir)
            if contr >= self.minimum:
                self.ev(t, "LOCAL_C_OPENED", f"C desde {self.b_extreme}")

    # -- ciclo de vida de la rama
    def integrate(self, seq: int, reason: str = "ABSORBED_BY_MAIN") -> None:
        """La rama local se integra en MAIN: deja de ser escala activa."""
        if self.status in (LOCAL_ARCHIVED, LOCAL_INTEGRATED):
            return
        self.status = LOCAL_INTEGRATED
        self.integrated_at_seq = seq
        self.integration_reason = reason
        self.ev(type("T", (), {"seq": seq, "time_ms": 0})(),
                "LOCAL_INTEGRATED", reason)

    def archive(self, seq: int) -> dict:
        self.status = LOCAL_ARCHIVED
        return {"generation_id": self.generation_id,
                "archived_at_seq": seq,
                "commits": len(self.commits)}

    # -- informes
    def snapshot(self) -> dict:
        return {
            "generation_id": self.generation_id,
            "parent_context_id": self.parent_context_id,
            "slot": self.slot,
            "status": self.status,
            "seed_seq": self.seed_seq,
            "seed_price": self.seed_price,
            "module": {"origin": self.module_origin,
                       "extreme": self.module_extreme,
                       "size": self.module_size,
                       "dir": self.module_dir,
                       "status": self.module_status,
                       "st": self.module_structural_time,
                       "kt": self.module_knowledge_time},
            "a": {"origin": self.a_origin, "extreme": self.a_extreme,
                  "size": self.a_size, "dir": self.a_dir,
                  "status": self.a_status,
                  "st": self.a_structural_time,
                  "kt": self.a_knowledge_time},
            "b": {"origin": self.b_origin, "extreme": self.b_extreme,
                  "size": self.b_size, "dir": self.b_dir,
                  "status": self.b_status, "ratio": self.b_ratio,
                  "level_100": self.b_100_level,
                  "level_127": self.b_limit_level},
            "tt": {"id": self.tt_id, "status": self.tt_status,
                   "dir": self.tt_dir, "final_a": self.tt_final_a,
                   "objective": self.tt_objective,
                   "invalidation": self.tt_invalidation,
                   "st": self.tt_structural_time,
                   "kt": self.tt_knowledge_time,
                   "first_boundary": self.tt_first_boundary},
            "commits": list(self.commits),
            "events": list(self.events),
            "metrics": self.rt.metrics(),
        }


def run_local(ticks, generation_id: str = "LOCAL-G2",
              minimum: int = DEFAULT_MINIMUM) -> LocalBranch:
    branch = LocalBranch(generation_id=generation_id, minimum=minimum)
    for t in ticks:
        branch.feed(t)
    return branch
