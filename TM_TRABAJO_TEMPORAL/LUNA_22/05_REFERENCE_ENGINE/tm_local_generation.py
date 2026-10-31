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

#: referencia de invalidacion del TT segun su genesis (espejo de MAIN).
#: Un TT nacido de un AUT invalida en final_A; solo el TT nacido de una A usada
#: como tendencia invalida en el origen de A.
TT_FINAL_A = "FINAL_A"
TT_A_ORIGIN = "A_ORIGIN"

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
    module_id: str = ""
    module_source_function_id: str = ""
    module_extreme_time: int = 0
    module_reclassifications: list[dict] = field(default_factory=list)

    a_origin: int = 0
    a_origin_seq: int = 0
    a_extreme: int = 0
    a_extreme_seq: int = 0
    a_size: int = 0
    a_dir: int = 0
    a_status: str = ""
    a_structural_time: int = 0
    a_knowledge_time: int = 0
    a_function_id: str = ""
    a_source_module_id: str = ""
    a_birth_module_extreme: int = 0
    a_candidate_seq: int = 0
    a_origin_time: int = 0
    a_extreme_time: int = 0

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
    b_function_id: str = ""
    b_source_function_id: str = ""
    b_candidate_seq: int = 0
    b_origin_time: int = 0
    b_grande_kt: int = 0
    b_grande_status: str = ""

    tt_id: str = ""
    tt_status: str = ""
    tt_dir: int = 0
    tt_final_a: int = 0
    tt_objective: int = 0
    tt_invalidation: int = 0
    tt_structural_time: int = 0
    tt_knowledge_time: int = 0
    tt_first_boundary: str = ""
    tt_module_id: str = ""
    tt_module_origin: int = 0
    tt_module_extreme: int = 0
    tt_module_size: int = 0
    tt_module_dir: int = 0
    tt_source_function_id: str = ""
    tt_opened_at_seq: int = 0
    tt_invalidation_kind: str = ""

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
        self._last_price = 0
        self._prev_price = 0
        self._id_seq: dict[str, int] = {}
        self.module_overextensions = 0
        self.integrated_at_seq = 0
        self.integration_reason = ""

    # -- utilidades
    def _new_id(self, kind: str) -> str:
        """Identificador causal: nunca contiene precios ni horas."""
        self._id_seq[kind] = self._id_seq.get(kind, 0) + 1
        return f"{self.generation_id}:{kind}:{self._id_seq[kind]:03d}"
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
        """Consume un tick conservando el precio previo (cruce de fronteras)."""
        self._prev_price = self._last_price or t.price
        try:
            self._consume(t)
        finally:
            self._last_price = t.price

    def _consume(self, t) -> None:
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
            self.up_time = self.down_time = t.time_ms
            return
        if t.price > self.up_extreme:
            self.up_extreme, self.up_seq = t.price, t.seq
            self.up_time = t.time_ms
        if t.price < self.down_extreme:
            self.down_extreme, self.down_seq = t.price, t.seq
            self.down_time = t.time_ms
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
                self.module_structural_time = self.up_time
                self.module_extreme, self.module_extreme_seq = (
                    self.down_extreme, self.down_seq)
                self.module_extreme_time = self.down_time
            else:
                self._dir_lock = 1
                self.module_origin, self.module_origin_seq = (
                    self.down_extreme, self.down_seq)
                self.module_structural_time = self.down_time
                self.module_extreme, self.module_extreme_seq = (
                    self.up_extreme, self.up_seq)
                self.module_extreme_time = self.up_time
            self.module_dir = self._dir_lock
            self.module_size = abs(self.module_extreme - self.module_origin)
            self.module_id = self.module_id or self._new_id("MODULE")
            self.ev(t, "LOCAL_DOMINANT_DIRECTION",
                    f"id={self.module_id} dir={self.module_dir} "
                    f"origin={self.module_origin} "
                    f"extreme={self.module_extreme} size={self.module_size}")
        if not self._dir_lock:
            return
        # Invariante: la direccion del modulo siempre es signo(extremo-origen).
        # Una direccion invertida haria que el modulo se extendiera por el lado
        # contrario y corromperia toda la genealogia A/B/TT.
        if self.module_dir and ((self.module_extreme - self.module_origin)
                               * self.module_dir) < 0:
            self.violations.hit("module_direction_invalid",
                                f"dir={self.module_dir} "
                                f"{self.module_origin}->{self.module_extreme}",
                                t.seq)
        self.module_size = abs(self.module_extreme - self.module_origin)
        d = self.module_dir
        if (t.price - self.module_extreme) * d > 0:
            # Diagnostico: si el modulo nacio de la A y el dominante continua
            # mas alla del extremo de esa A, el tramo confirmado como A es en
            # realidad parte del movimiento dominante. No se reescribe nada
            # (la A conserva su delimitacion y su knowledge_time): se registra
            # el hecho para que ninguna medida quede sin explicacion. Resolver
            # el origen correcto del modulo es MODULE_ORIGIN_RESOLUTION.
            if (self.a_status == "A_CONFIRMED"
                    and self.module_source_function_id == self.a_function_id
                    and (t.price - self.a_extreme) * d > 0):
                self.module_overextensions += 1
                if self.module_overextensions == 1:
                    self.ev(t, "LOCAL_MODULE_EXTENDS_BEYOND_A",
                            f"el dominante continua mas alla del extremo de A "
                            f"{self.a_extreme} hasta {t.price}; la A queda como "
                            f"tramo interno del modulo (sin reescritura)")
            self.module_extreme = t.price
            self.module_extreme_seq = t.seq
            self.module_extreme_time = t.time_ms
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
        self.a_origin_time = self.module_extreme_time
        self.a_structural_time = self.a_origin_time
        self.a_status = "CANDIDATE"
        self.a_dir = -self.module_dir
        self.a_extreme = t.price
        self.a_extreme_seq = t.seq
        self.a_extreme_time = t.time_ms
        self.a_size = abs(self.a_extreme - self.a_origin)
        self.a_function_id = self._new_id("A")
        self.a_source_module_id = self.module_id
        self.a_birth_module_extreme = self.module_extreme
        self.a_candidate_seq = t.seq
        self.ev(t, "LOCAL_A_CANDIDATE",
                f"id={self.a_function_id} origin={self.a_origin} "
                f"extreme={self.a_extreme} size={self.a_size} "
                f"dir={self.a_dir} source_module={self.a_source_module_id} "
                f"structural_time={self.a_structural_time} "
                f"knowledge_time={t.time_ms}")
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
            self.a_extreme_time = t.time_ms
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
            # Regla canonica (identica a MAIN): una A mayor que el modulo por
            # descarte deviene el modulo del ciclo, no un retroceso interno.
            # La reclasificacion se registra con genealogia completa y RE-BLOQUEA
            # la direccion dominante en la direccion de A.
            if self.a_size > self.module_size:
                self._reclassify_module_to_a(t)
            elif not self.module_status:
                # A confirmada => el movimiento dominante queda declarado como
                # modulo por descarte (fin de la fase provisional)
                self.module_status = "LOCAL_MODULE_BY_DISCARD"
                self.module_knowledge_time = t.time_ms
                self.ev(t, "LOCAL_MODULE_DECLARED",
                        f"id={self.module_id} origin={self.module_origin} "
                        f"extreme={self.module_extreme} "
                        f"size={self.module_size} dir={self.module_dir} "
                        f"st={self.module_structural_time} kt={t.time_ms}")
            self.ev(t, "LOCAL_A_CONFIRMED",
                    f"A local={self.a_origin}->{self.a_extreme} size={self.a_size} "
                    f"source_module={self.a_source_module_id} "
                    f"b_ratio pendiente de B")
        self._b_open(t)

    def _reclassify_module_to_a(self, t) -> None:
        """A mayor que el modulo provisional deviene el modulo del ciclo.

        Es una RECLASIFICACION explicita, no una escritura silenciosa:

        * el modulo anterior se conserva completo (id, origen, extremo, tamano,
          direccion, estado) en `module_reclassifications`;
        * el modulo pasa a tener la geometria de la A (`module_source_function_id`
          = funcion A), de modo que el origen compartido queda justificado;
        * la direccion dominante se RE-BLOQUEA en la direccion de A. Sin este
          re-bloqueo `_module_tick` seguiria extendiendo el modulo antiguo y la
          geometria quedaria incoherente (origen de A + extremo contrario).
        """
        previous = {"module_id": self.module_id,
                    "origin": self.module_origin,
                    "extreme": self.module_extreme,
                    "size": self.module_size,
                    "dir": self.module_dir,
                    "status": self.module_status or "PROVISIONAL"}
        self.module_reclassifications.append({
            "seq": t.seq, "reason": "A_BIGGER_THAN_PROVISIONAL_MODULE",
            "previous": previous,
            "new": {"origin": self.a_origin, "extreme": self.a_extreme,
                    "size": self.a_size, "dir": self.a_dir,
                    "source_function_id": self.a_function_id},
        })
        self.module_id = self._new_id("MODULE")
        self.module_origin = self.a_origin
        self.module_origin_seq = self.a_origin_seq
        self.module_extreme = self.a_extreme
        self.module_extreme_seq = self.a_extreme_seq
        self.module_extreme_time = self.a_extreme_time
        self.module_size = self.a_size
        self.module_dir = self.a_dir
        self.module_status = "LOCAL_MODULE_BY_DISCARD_A"
        self.module_source_function_id = self.a_function_id
        self.module_knowledge_time = t.time_ms
        self._dir_lock = self.a_dir
        self.ev(t, "LOCAL_MODULE_RECLASSIFIED",
                f"previous={previous['module_id']} "
                f"{previous['origin']}->{previous['extreme']} "
                f"size={previous['size']} dir={previous['dir']} "
                f"status={previous['status']} ; new={self.module_id} "
                f"origin={self.module_origin} extreme={self.module_extreme} "
                f"size={self.module_size} dir={self.module_dir} "
                f"source_function={self.module_source_function_id} "
                f"kt={t.time_ms}")

    def _b_open(self, t) -> None:
        self.b_status = B_PHYSICAL
        self.b_dir = -self.a_dir
        self.b_origin = self.a_extreme
        self.b_origin_seq = self.a_extreme_seq
        self.b_origin_time = self.a_extreme_time
        self.b_extreme = t.price
        self.b_extreme_seq = t.seq
        self.b_size = abs(self.b_extreme - self.b_origin)
        self.b_100_level = self.a_size
        self.b_limit_level = self.a_size * 127 // 100 + 25
        self.b_function_id = self._new_id("B")
        self.b_source_function_id = self.a_function_id
        self.b_candidate_seq = t.seq
        self.ev(t, "LOCAL_B_OPENED",
                f"id={self.b_function_id} source_function={self.a_function_id} "
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
        # Salto directo de <100 % a >127 %+0,25 en el mismo tick: se registra
        # el cruce causal del 100 % (espejo de MAIN) para que la genealogia
        # B -> B Grande -> AUT no pierda el paso intermedio.
        if (self.b_status == B_CANDIDATE_CONFIRMED and not self.b_grande_kt
                and self.b_size > self.b_limit_level):
            self.b_grande_kt = t.time_ms
            self.b_grande_status = "CAUSAL_CROSS_IN_AUT_TICK"
            self.ev(t, "LOCAL_B_GRANDE_CAUSAL_CROSS",
                    f"B={self.b_size} cruza 100% de A={self.a_size} y AUT "
                    f"en el mismo tick")
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
                self.b_grande_kt = t.time_ms
                self.b_grande_status = B_GRANDE
                self.ev(t, "LOCAL_B_GRANDE",
                        f"B={self.b_size} alcanza 100% de A={self.a_size}")

    def _arm_local_tt(self, t, invalidation_kind: str = TT_FINAL_A) -> None:
        """TT local: propietario LOCAL-G2, modulo y final_A propios.

        La genealogia se congela en el momento del armado: el objetivo SIEMPRE
        es `final_A +/- tt_module_size` con el modulo registrado en el TT. Si el
        modulo se extiende despues, el TT NO reescribe su objetivo ni su tamano
        de referencia (identico a MAIN); re-derivarlo con el modulo final hacia
        que la medida del patron no fuese reproducible.

        Referencia de invalidacion: un TT nacido de un AUT invalida en final_A;
        solo la A usada como tendencia invalida en su propio origen.
        """
        if self.tt_status:
            return
        if not self.module_size or not self.b_origin or not self.b_dir:
            return
        self.tt_id = f"{self.generation_id}:TT:001"
        self.tt_dir = self.b_dir
        self.tt_final_a = self.b_origin
        self.tt_module_id = self.module_id
        self.tt_module_origin = self.module_origin
        self.tt_module_extreme = self.module_extreme
        self.tt_module_size = self.module_size
        self.tt_module_dir = self.module_dir
        self.tt_source_function_id = self.b_function_id
        self.tt_opened_at_seq = t.seq
        self.tt_invalidation_kind = invalidation_kind
        self.tt_invalidation = (self.tt_final_a if invalidation_kind == TT_FINAL_A
                                else self.a_origin)
        self.tt_objective = self.tt_final_a + self.tt_dir * self.tt_module_size
        self.tt_structural_time = self.b_origin_time or self.a_structural_time
        self.tt_knowledge_time = t.time_ms
        self.tt_status = "TT_PENDING"
        self.ev(t, "LOCAL_TT_ARMED",
                f"id={self.tt_id} dir={self.tt_dir} final_A={self.tt_final_a} "
                f"objetivo={self.tt_objective} modulo={self.tt_module_size} "
                f"module_id={self.tt_module_id} "
                f"source_function={self.tt_source_function_id} "
                f"invalidacion={self.tt_invalidation_kind} "
                f"{self.tt_invalidation}")

    def _tt_tick(self, t) -> None:
        d = self.tt_dir
        if not d:
            return
        # Orden cronologico estricto dentro del tick: primero invalidacion.
        # Solo cuenta el CRUCE real desde el lado del TT: estar en el nivel no
        # es volver a el (identico a MAIN).
        ref = self.tt_invalidation
        back = ((self._prev_price - ref) * d > 0
                and (t.price - ref) * d <= 0)
        if back:
            self.tt_status = "TT_FAILED"
            self.tt_first_boundary = (f"INVALIDATION_{self.tt_invalidation_kind}"
                                      f"@{t.seq}")
            self.ev(t, "LOCAL_TT_FAILED",
                    f"invalidacion {self.tt_invalidation_kind} "
                    f"{self.tt_invalidation} cruzada en {t.price} antes del "
                    f"objetivo {self.tt_objective}")
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
    def geometry(self) -> dict:
        """Invariantes geometricas de la rama (Iteracion 23A).

        Cada invariante es una igualdad derivable de los campos registrados: no
        depende de precios ni de horas del caso.
        """
        geo = {
            "local_module_direction_valid": bool(
                self.module_dir and self.module_origin and self.module_extreme
                and (self.module_extreme - self.module_origin)
                * self.module_dir > 0),
            "local_module_size_valid": self.module_size == abs(
                self.module_extreme - self.module_origin),
            "local_A_origin_valid": bool(
                not self.a_origin or self.a_origin == self.a_birth_module_extreme),
            "local_A_source_module_valid": bool(
                not self.a_origin or bool(self.a_source_module_id)),
            "local_A_direction_valid": bool(
                not self.a_dir or self.a_dir == -self.module_dir
                or self.module_source_function_id == self.a_function_id),
            "local_B_origin_equals_A_extreme": bool(
                not self.b_origin or self.b_origin == self.a_extreme),
            "local_B_source_function_valid": bool(
                not self.b_origin or self.b_source_function_id == self.a_function_id),
            "local_B_ratio_traceable": bool(
                not self.b_size or not self.a_size
                or abs(self.b_ratio - round(self.b_size / self.a_size, 4))
                < 1e-9),
            "local_B_grande_requires_100_percent": bool(
                self.b_status not in (B_GRANDE,) or self.b_size >= self.a_size),
            "local_A_trend_requires_valid_B_grande": bool(
                not self.tt_id or self.tt_invalidation_kind != TT_A_ORIGIN
                or self.b_grande_status in (B_GRANDE,
                                            "CAUSAL_CROSS_IN_AUT_TICK")),
            "local_TT_module_traceable": bool(
                not self.tt_id or (bool(self.tt_module_id)
                                   and self.tt_module_size > 0
                                   and self.tt_module_size == abs(
                                       self.tt_module_extreme
                                       - self.tt_module_origin))),
            "local_TT_final_A_traceable": bool(
                not self.tt_id or self.tt_final_a == self.a_extreme),
            "local_TT_objective_derivable": bool(
                not self.tt_id or self.tt_objective
                == self.tt_final_a + self.tt_dir * self.tt_module_size),
            "local_TT_activation_path_traceable": bool(
                not self.tt_id or bool(self.tt_source_function_id)
                and self.tt_opened_at_seq > 0),
        }
        return geo

    def snapshot(self) -> dict:
        return {
            "generation_id": self.generation_id,
            "parent_context_id": self.parent_context_id,
            "slot": self.slot,
            "status": self.status,
            "seed_seq": self.seed_seq,
            "seed_price": self.seed_price,
            "module": {"id": self.module_id,
                       "origin": self.module_origin,
                       "extreme": self.module_extreme,
                       "size": self.module_size,
                       "dir": self.module_dir,
                       "status": self.module_status,
                       "source_function_id": self.module_source_function_id,
                       "st": self.module_structural_time,
                       "kt": self.module_knowledge_time},
            "a": {"id": self.a_function_id,
                  "origin": self.a_origin, "extreme": self.a_extreme,
                  "size": self.a_size, "dir": self.a_dir,
                  "status": self.a_status,
                  "source_module_id": self.a_source_module_id,
                  "birth_module_extreme": self.a_birth_module_extreme,
                  "st": self.a_structural_time,
                  "kt": self.a_knowledge_time},
            "b": {"id": self.b_function_id,
                  "source_function_id": self.b_source_function_id,
                  "origin": self.b_origin, "extreme": self.b_extreme,
                  "size": self.b_size, "dir": self.b_dir,
                  "status": self.b_status, "ratio": self.b_ratio,
                  "level_100": self.b_100_level,
                  "level_127": self.b_limit_level,
                  "grande_status": self.b_grande_status,
                  "grande_kt": self.b_grande_kt},
            "tt": {"id": self.tt_id, "status": self.tt_status,
                   "dir": self.tt_dir, "final_a": self.tt_final_a,
                   "objective": self.tt_objective,
                   "invalidation": self.tt_invalidation,
                   "invalidation_kind": self.tt_invalidation_kind,
                   "module_id": self.tt_module_id,
                   "module_origin": self.tt_module_origin,
                   "module_extreme": self.tt_module_extreme,
                   "module_size": self.tt_module_size,
                   "source_function_id": self.tt_source_function_id,
                   "opened_at_seq": self.tt_opened_at_seq,
                   "st": self.tt_structural_time,
                   "kt": self.tt_knowledge_time,
                   "first_boundary": self.tt_first_boundary},
            "module_reclassifications": list(self.module_reclassifications),
            "module_overextensions": self.module_overextensions,
            "geometry": self.geometry(),
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
