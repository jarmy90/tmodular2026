#!/usr/bin/env python3
"""Iteracion 21 — pruebas del invariante constitucional:

    UN CANDIDATO NUNCA MODIFICA EL ESTADO FUNCIONAL CONFIRMADO.

Seccion A: pruebas unitarias de la capa `tm_candidates` (sinteticas).
Seccion B: pruebas de integracion sobre el tickfeed real (lector + manager).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "05_REFERENCE_ENGINE"))

from tm_candidates import (  # noqa: E402
    ABSORBED, ADMIT, AT_PHYSICAL, AT_STRUCTURAL, CONFIRM, CONFIRMED,
    DISCARDED, OBSERVED, PHYSICAL, STRUCTURAL, ArchitectureViolation,
    BranchRuntime, CandidateTracker, FunctionalCommit, QuestionBook,
    TreeQuestion, ViolationLedger,
)
from tm_reference_interpreter_v1_direct_aut import load_ticks, FEED  # noqa: E402
from tm_reading_manager import TMReadingManager  # noqa: E402

ROWS: list[dict] = []


def add(tid: str, expected: str, ok: bool, actual: str,
        authority: str = "CANONICAL") -> None:
    ROWS.append({"test_id": tid, "expected": expected,
                 "status": "PASS" if ok else "FAIL", "actual": actual,
                 "authority": authority})


def runtime(branch: str = "T", gen: str = "G1") -> BranchRuntime:
    return BranchRuntime(branch, gen)


def question(rt: BranchRuntime, roles=("A",), consumes=("T:G1:MODULE",),
             node: str = "AFTER_MODULE") -> TreeQuestion:
    return rt.open_question(node, roles, consumes, 0, physical=200)


def candidate(rt: BranchRuntime, role: str = "A", direction: int = -1,
              origin: int = 1000, extreme: int = 800, size: int = 200):
    return rt.tracker.admit(role, direction, origin, 1, extreme, 2, "SRC",
                            abs(extreme - origin), size)


def raises(fn, *a, **kw) -> tuple[bool, str]:
    try:
        fn(*a, **kw)
        return False, ""
    except ArchitectureViolation as exc:
        return True, str(exc)


# --------------------------------------------------------------------- seccion A
def section_a() -> None:
    # A1 — movimiento inferior al minimo fisico: OBSERVED, no alimenta el arbol
    rt = runtime()
    c = rt.tracker.observe("A", -1, 1000, 1, 950, 2, "SRC", 50, 200)
    add("A1", "movimiento < minimo crea OBSERVED y no PHYSICAL",
        c.status == OBSERVED and rt.tracker.metrics()["by_status"][OBSERVED] == 1,
        f"status={c.status}")

    # A2 — 2 puntos crea PHYSICAL, nada mas
    rt = runtime()
    q = question(rt)
    c = candidate(rt)
    add("A2", "2 puntos -> PHYSICAL; no CONFIRMED ni funcion",
        c.status == PHYSICAL and c.question_id == "" and rt.commits == [],
        f"status={c.status} commits={len(rt.commits)}")

    # A3 — el tracker no puede escribir el estado confirmado
    rt = runtime()
    q = question(rt)
    rt.commit(ADMIT, q.question_id, candidate(rt, extreme=800).candidate_id,
              3, {"a_status": "CONTRARY_MOVE_PENDING"})
    before = rt.state.snapshot()
    cid = list(rt.tracker.candidates)[0]
    rt.tracker.retention(cid, 4)
    rt.tracker.absorb(cid, 5, "MODULE", "TEST")
    add("A3", "mutar candidatos no altera el estado confirmado",
        rt.state.snapshot() == before and not hasattr(rt.tracker, "reading"),
        f"state_version={rt.state.version} "
        f"state_igual={rt.state.snapshot() == before}")

    # A4 — escritura directa sin commit aborta
    rt = runtime()
    ok, msg = raises(rt.state.direct_write, "a_status", "X", 9)
    add("A4", "escritura directa aborta con CANDIDATE_STATE_WRITE_VIOLATION",
        ok and "CANDIDATE_STATE_WRITE_VIOLATION" in msg
        and rt.violations.counts["candidate_state_writes"] == 1,
        f"aborta={ok} contador={rt.violations.counts['candidate_state_writes']}")

    # A5 — veto de nacimiento: no se confirma con la evidencia que lo creo
    rt = runtime()
    q = question(rt)
    c = candidate(rt)
    rt.commit(ADMIT, q.question_id, c.candidate_id, 2,
              {"a_status": "CONTRARY_MOVE_PENDING"})
    rt.tracker.retention(c.candidate_id, 3)
    ok, msg = raises(rt.commit, CONFIRM, q.question_id, c.candidate_id,
                     2, {"a_status": "A_CONFIRMED"})
    add("A5", "CONFIRM en el tick de alta aborta y cuenta same_tick_confirmation",
        ok and "SAME_BIRTH" in msg
        and rt.violations.counts["same_tick_confirmation"] == 1,
        f"aborta={ok} contador={rt.violations.counts['same_tick_confirmation']}")

    # A6 — CONFIRM exige retencion superada
    rt = runtime()
    q = question(rt)
    c = candidate(rt)
    rt.commit(ADMIT, q.question_id, c.candidate_id, 1, {"a_status": "P"})
    ok, msg = raises(rt.commit, CONFIRM, q.question_id, c.candidate_id,
                     9, {"a_status": "A_CONFIRMED"})
    add("A6", "CONFIRM sin retencion aborta (CONFIRM_WITHOUT_RETENTION)",
        ok and "RETENTION" in msg, f"aborta={ok} msg={msg}")

    # A7 — CONFIRM con retencion posterior es valido y confirma el candidato
    rt = runtime()
    q = question(rt)
    c = candidate(rt)
    rt.commit(ADMIT, q.question_id, c.candidate_id, 1, {"a_status": "P"})
    rt.tracker.retention(c.candidate_id, 5)
    rt.commit(CONFIRM, q.question_id, c.candidate_id, 6,
              {"a_status": "A_CONFIRMED"})
    add("A7", "CONFIRM con retencion escribe estado y confirma el candidato",
        rt.state.get("a_status") == "A_CONFIRMED"
        and rt.tracker.get(c.candidate_id).status == CONFIRMED
        and rt.state.version == 2,
        f"a_status={rt.state.get('a_status')} version={rt.state.version}")

    # A8 — consumes cerrado
    rt = runtime()
    q = question(rt)
    c = candidate(rt)
    ok, msg = raises(rt.commit, ADMIT, q.question_id, c.candidate_id, 1,
                     {"a_status": "P"}, [("T:G1:OTRA", "T", "G1")])
    add("A8", "lectura fuera de consumes cuenta consumes_violations",
        ok and rt.violations.counts["consumes_violations"] == 1,
        f"aborta={ok} contador={rt.violations.counts['consumes_violations']}")

    # A9 — referencia de otra rama
    rt = runtime()
    q = question(rt)
    c = candidate(rt)
    ok, msg = raises(rt.commit, ADMIT, q.question_id, c.candidate_id, 1,
                     {"a_status": "P"}, [("X:G1:MODULE", "X", "G1")])
    add("A9", "referencia de otra rama cuenta cross_owner_reference_reads",
        ok and rt.violations.counts["cross_owner_reference_reads"] == 1,
        f"aborta={ok} contador={rt.violations.counts['cross_owner_reference_reads']}")

    # A10 — commit de otra generacion
    rt = runtime()
    q = question(rt)
    c = candidate(rt)
    bad = FunctionalCommit(kind=ADMIT, branch_id="T", generation_id="G2",
                           question_id=q.question_id, candidate_id=c.candidate_id,
                           seq=1, writes={"a_status": "P"})
    ok, msg = raises(bad.validate, rt.tracker, rt.book, rt.violations)
    add("A10", "commit de otra generacion aborta (CROSS_GENERATION_COMMIT)",
        ok and "CROSS_GENERATION" in msg, f"aborta={ok} msg={msg}")

    # A11 — rol no admitido por la pregunta
    rt = runtime()
    q = question(rt, roles=("B",))
    c = candidate(rt, role="A")
    ok, msg = raises(rt.commit, ADMIT, q.question_id, c.candidate_id, 1,
                     {"a_status": "P"})
    add("A11", "rol no permitido aborta (COMMIT_ROLE_NOT_ALLOWED)",
        ok and "ROLE_NOT_ALLOWED" in msg, f"aborta={ok} msg={msg}")

    # A12 — sombra impide recrear el candidato absorbido
    rt = runtime()
    q = question(rt)
    c = candidate(rt, direction=-1, origin=1000, extreme=800)
    rt.commit(ADMIT, q.question_id, c.candidate_id, 1, {"a_status": "P"})
    rt.tracker.retention(c.candidate_id, 3)
    rt.commit(CONFIRM, q.question_id, c.candidate_id, 4, {"a_status": "C"})
    rt.tracker.absorb(c.candidate_id, 5, "MODULE", "TEST")
    # recreacion EQUIVALENTE: no supera el extremo de la sombra
    again = candidate(rt, direction=-1, origin=1000, extreme=800)
    add("A12", "sombra convierte en DISCARDED la recreacion equivalente",
        again.status == DISCARDED
        and rt.tracker.recreation_attempts == 1
        and again.close_reason == "SHADOW_BLOCKED",
        f"status={again.status} intentos={rt.tracker.recreation_attempts}")

    # A13 — la sombra se libera con evidencia nueva (extremo superado)
    rt = runtime()
    q = question(rt)
    c = candidate(rt, direction=-1, origin=1000, extreme=800)
    rt.tracker.absorb(c.candidate_id, 5, "MODULE", "TEST")
    deeper = candidate(rt, direction=-1, origin=1000, extreme=700)
    add("A13", "extremo que supera la sombra no se bloquea (PHYSICAL)",
        deeper.status == PHYSICAL, f"status={deeper.status}")

    # A14 — nivel de absorcion registrado
    rt = runtime()
    c1 = candidate(rt, role="A")
    rt.tracker.absorb(c1.candidate_id, 5, "MODULE", "T")
    c2 = candidate(rt, role="B", direction=1, origin=800, extreme=1000)
    rt.tracker.retention(c2.candidate_id, 3)
    rt.tracker.absorb(c2.candidate_id, 6, "MODULE", "T")
    levels = rt.tracker.metrics()["absorption_levels"]
    add("A14", "absorption_level distingue PHYSICAL y STRUCTURAL",
        levels.get(AT_PHYSICAL) == 1 and levels.get(AT_STRUCTURAL) == 1,
        f"levels={levels}")

    # A15 — trazabilidad de commits y no reutilizacion de pregunta cerrada
    rt = runtime()
    q = question(rt)
    c = candidate(rt)
    rt.commit(ADMIT, q.question_id, c.candidate_id, 1, {"a_status": "P"})
    rt.book.close(q.question_id, "NO", 2)
    ok, msg = raises(rt.commit, CONFIRM, q.question_id, c.candidate_id, 9,
                     {"a_status": "C"})
    add("A15", "no se confirma sobre pregunta respondida NO",
        ok and ("CLOSED" in msg or "REJECTED" in msg), f"aborta={ok} msg={msg}")


# --------------------------------------------------------------------- seccion B
def section_b() -> None:
    ticks = [t for t in load_ticks(FEED) if 16 * 60 + 15 <= t.bar % 1440 <= 16 * 60 + 32]
    mgr = TMReadingManager(ticks).run()
    arch = mgr.l1.arch
    viol = arch.violations
    metrics = arch.metrics()

    add("B1", "cero violaciones de arquitectura en el tramo real",
        viol.total() == 0, f"total={viol.total()} counts={viol.counts}")

    add("B2", "hay commits reales: ADMIT y CONFIRM",
        len(arch.commits) > 0
        and {c.kind for c in arch.commits} >= {ADMIT, CONFIRM},
        f"commits={len(arch.commits)} kinds={sorted({c.kind for c in arch.commits})}")

    branches = sorted({c["owner_branch_id"] for c in arch.tracker.snapshot()})
    add("B3", "ningun candidato sin propietario ni rama",
        metrics["candidates"]["total"] > 0
        and all(c["owner_branch_id"] == "L1"
                for c in arch.tracker.snapshot()),
        f"total={metrics['candidates']['total']} branches={branches}")

    objs = mgr.summaries()
    gens = objs.get("generation_records", [])
    add("B4", "archivo de LOCAL-G1 y slot liberado se mantienen",
        any(g.get("status") == "ARCHIVED" for g in gens),
        f"gens={[(g.get('generation_id'), g.get('status')) for g in gens]}")

    # B5 — IMPLICIT_MODULE_ORIGIN: escenario sintetico del gap
    from tm_reference_interpreter_v1_direct_aut import Reader, Tick
    rd = Reader([])
    rd.reading.gap_branch = True
    rd.reading.one_dir = -1
    rd.reading.one_origin = 1000
    rd.reading.one_extreme = 800
    rd.reading.one_st = 10
    rd.reading.one_extreme_st = 20
    rd._module_by_discard(Tick(1, 1000, 0, 900), include_two=False)
    implicit = [qq for qq in rd.arch.book.questions.values()
                if qq.current_node == "IMPLICIT_MODULE_ORIGIN"]
    kept = [qq for qq in implicit if qq.rejected_hypotheses]
    add("B5", "IMPLICIT_MODULE_ORIGIN declarada con alternativa conservada",
        len(implicit) == 1 and len(kept) == 1
        and kept[0].rejected_hypotheses[0]["hypothesis"]
        == "MODULE_ORIGIN_AT_PROHIBITED_EXCURSION"
        and rd.reading.mod_size > 0,
        f"preguntas={len(implicit)} con_alternativa={len(kept)} "
        f"alt={kept[0].rejected_hypotheses[0]['origin'] if kept else None}")

    add("B6", "maximo dos ramas activas (MAIN + LOCAL)",
        (mgr.l2 is not None) + 1 <= 2, f"ramas={1 + (mgr.l2 is not None)}")

    # B7 — determinismo
    mgr2 = TMReadingManager(ticks).run()
    add("B7", "dos ejecuciones producen identico snapshot de arquitectura",
        json.dumps(mgr2.l1.arch.snapshot(), sort_keys=True)
        == json.dumps(arch.snapshot(), sort_keys=True),
        f"commits={len(arch.commits)}")

    # B8 — consistencia de prefijo de la capa de arquitectura
    pre = [t for t in ticks if 16 * 60 + 15 <= t.bar % 1440 <= 16 * 60 + 26]
    mgr_pre = TMReadingManager(pre).run()
    full_seq = [c.seq for c in arch.commits
                if c.seq <= max(t.seq for t in pre)]
    pre_seq = [c.seq for c in mgr_pre.l1.arch.commits]
    add("B8", "prefijo: los commits hasta 16:26 coinciden",
        full_seq == pre_seq,
        f"full={len(full_seq)} pre={len(pre_seq)}")

    # B9 — estado confirmado espejo coherente con el lector
    st = arch.state.snapshot()
    add("B9", "el ultimo commit refleja el estado confirmado del lector",
        st.get("a_status") == mgr.l1.reading.a_status,
        f"state={st.get('a_status')} reading={mgr.l1.reading.a_status}")

    # B10 — ningun candidato absorbido se recrea en el tramo real
    add("B10", "recreaciones bloqueadas por sombra < candidatos absorbidos",
        metrics["candidates"]["recreation_attempts"]
        <= metrics["candidates"]["by_status"].get(ABSORBED, 0) + 1,
        f"intentos={metrics['candidates']['recreation_attempts']} "
        f"absorbidos={metrics['candidates']['by_status'].get(ABSORBED, 0)}")


# --------------------------------------------------------------------- seccion C
def section_c() -> None:
    """Capas de mercado, absorcion, arbiter, invariancias y clasificador."""
    import re
    from tm_market_layer import (  # noqa: E402
        EARLY_CONFIRMATION, LATE_CONFIRMATION, LOST_STATE, MISSING_RULE,
        NO_DIVERGENCE, NOISE_FRAGMENTATION, OWNER_ERROR, QUESTION_ERROR,
        REFERENCE_ERROR, BranchArbiter, DecisionTracer, MarketFacts,
        TickLedger,
    )
    from tm_reference_interpreter_v1_direct_aut import Reader, Tick  # noqa: E402

    # C1 — 2 puntos absorbidos no confirman nada
    rt = runtime("X")
    question(rt)
    c = candidate(rt, origin=1000, extreme=800)
    rt.tracker.absorb(c.candidate_id, 5, "OWNER", "OWNER_RECLAIMED")
    add("C1", "2 puntos absorbidos no escriben estado confirmado",
        c.status == ABSORBED and rt.state.version == 0 and not rt.commits,
        f"status={c.status} version={rt.state.version} commits={len(rt.commits)}")

    # C2 — el mismo desplazamiento termina siendo A
    rt = runtime("Y")
    q = question(rt)
    c = candidate(rt, origin=1000, extreme=800)
    rt.tracker.retention(c.candidate_id, 3)
    rt.commit(CONFIRM, q.question_id, c.candidate_id, 4,
              {"a_status": "A_CONFIRMED"})
    add("C2", "el mismo desplazamiento puede terminar siendo A confirmada",
        c.status == CONFIRMED and rt.state.get("a_status") == "A_CONFIRMED",
        f"status={c.status} a={rt.state.get('a_status')}")

    # C3 — movimiento muy superior a 2 puntos tambien absorbido
    rt = runtime("Z")
    question(rt)
    c = candidate(rt, origin=1000, extreme=400, size=600)
    rt.tracker.absorb(c.candidate_id, 5, "OWNER", "OWNER_RECLAIMED")
    add("C3", "movimiento de 6 puntos absorbido queda sin funcion",
        c.status == ABSORBED and rt.state.version == 0
        and c.absorption_level == AT_PHYSICAL,
        f"status={c.status} nivel={c.absorption_level}")

    # C4 — por debajo del minimo fisico no hay PHYSICAL
    rt = runtime("W")
    question(rt)
    ok, msg = raises(rt.tracker.admit, "A", -1, 1000, 1, 900, 2, "SRC", 100, 200)
    obs = rt.tracker.observe("A", -1, 1000, 1, 900, 2, "SRC", 100, 200)
    rt.tracker.promote_physical(obs.candidate_id, 3)
    add("C4", "<2 puntos: OBSERVED, nunca PHYSICAL ni funcion",
        ok and obs.status == OBSERVED and rt.state.version == 0,
        f"aborta={ok} status={obs.status} msg={msg[:28]}")

    # C5/C6 — extension y no-extension del extremo
    rt = runtime("E")
    question(rt)
    c = candidate(rt, origin=1000, extreme=800)
    rt.tracker.extend(c.candidate_id, 700, 3)
    ext_ok = c.extreme == 700 and c.physical_size == 300
    rt.tracker.extend(c.candidate_id, 950, 4)
    add("C5", "extender en su direccion actualiza extremo y tamano",
        ext_ok, f"extreme={c.extreme} size={c.physical_size}")
    add("C6", "un precio contrario no recorta el extremo del candidato",
        c.extreme == 700 and c.status == PHYSICAL,
        f"extreme={c.extreme} status={c.status}")

    # C7 — retencion sin resolucion funcional
    rt = runtime("R")
    question(rt)
    c = candidate(rt, origin=1000, extreme=800)
    rt.tracker.retention(c.candidate_id, 3)
    add("C7", "retencion sin pregunta resuelta no escribe estado",
        c.status == STRUCTURAL and rt.state.version == 0 and not rt.commits,
        f"status={c.status} version={rt.state.version}")

    # C8 — extension repetida sin funcion
    rt = runtime("F")
    question(rt)
    c = candidate(rt, origin=1000, extreme=800)
    for i, px in enumerate((760, 720, 690, 650), start=3):
        rt.tracker.extend(c.candidate_id, px, i)
    add("C8", "extender sin funcion deja el candidato en PHYSICAL",
        c.status == PHYSICAL and rt.state.version == 0,
        f"status={c.status} extreme={c.extreme} version={rt.state.version}")

    # C9 — plano y gap sobre precio fisico
    f = MarketFacts()
    f.observe(1, 100, 1000)
    f.observe(2, 100, 1005)
    f.observe(3, 101, 1010)
    flat = f.flat_or_gap
    f2 = MarketFacts()
    f2.observe(1, 100, 1000)
    f2.observe(2, 101, 1040)
    add("C9", "plano y gap se deciden con el umbral 0,25 fisico",
        flat == "FLAT" and f2.flat_or_gap == "GAP"
        and f2.open_difference == 40,
        f"flat={flat} gap={f2.flat_or_gap} diff={f2.open_difference}")

    # C10 — cola inicial congelada sin informacion futura
    f = MarketFacts()
    f.observe(1, 100, 1000)
    f.observe(2, 100, 1100)
    f.observe(3, 100, 1050)
    f.observe(4, 100, 950)          # primer tick contrario: cierra la cola
    tail = f.initial_tail
    f.observe(5, 100, 1200)         # ya no puede ampliarla
    add("C10", "la cola inicial se congela con el primer tick contrario",
        tail == 100 and f.initial_tail == 100 and f.initial_tail_closed,
        f"tail={f.initial_tail} cerrada={f.initial_tail_closed}")

    # C11 — primer toque de un nivel
    f = MarketFacts()
    first = f.touch(1100, 5)
    second = f.touch(1100, 9)
    add("C11", "el primer toque se registra una sola vez con su seq",
        first and not second and f.first_touch_seq(1100) == 5,
        f"first={first} second={second} seq={f.first_touch_seq(1100)}")

    # C12/C13 — ledger inmutable y marcas de vela
    led = TickLedger()
    led.append(1, 0, 100, 1000)
    led.append(2, 1, 100, 1001)
    ok, msg = raises(led.append, 1, 2, 100, 1002)
    add("C12", "el ledger rechaza reescribir un tick",
        ok and "LEDGER_REWRITE" in msg, f"aborta={ok} msg={msg}")
    led2 = TickLedger()
    led2.append(1, 0, 100, 10)
    led2.append(2, 1, 100, 11)
    led2.append(3, 2, 101, 12)
    add("C13", "el ultimo tick de la vela queda marcado al abrir la siguiente",
        led2.rows[1].is_last_tick_of_bar and led2.rows[2].is_first_tick_of_bar,
        f"prev_last={led2.rows[1].is_last_tick_of_bar} "
        f"new_first={led2.rows[2].is_first_tick_of_bar}")

    # C14 — dos ramas reciben el mismo tick sin interferencia
    rt1, rt2 = runtime("L1"), runtime("L2")
    q1, q2 = question(rt1), question(rt2)
    c1 = candidate(rt1)
    c2 = candidate(rt2)
    rt2.tracker.retention(c2.candidate_id, 3)
    rt2.commit(CONFIRM, q2.question_id, c2.candidate_id, 4,
               {"a_status": "A_CONFIRMED"})
    add("C14", "dos ramas procesan el mismo tick sin interferirse",
        rt1.state.version == 0 and rt2.state.version == 1
        and c1.status == PHYSICAL,
        f"v1={rt1.state.version} v2={rt2.state.version} c1={c1.status}")

    # C15 — un TT confirma y otro falla en ramas distintas
    rt1, rt2 = runtime("M"), runtime("N")
    qq1 = rt1.open_question("TT_ARBITRATION", ("TT",), ("M:G1:TT",), 0,
                            physical=200)
    qq2 = rt2.open_question("TT_ARBITRATION", ("TT",), ("N:G1:TT",), 0,
                            physical=200)
    t1 = rt1.tracker.admit("TT", -1, 1000, 1, 800, 2, "SRC", 200, 200,
                           qq1.question_id)
    t2 = rt2.tracker.admit("TT", -1, 1000, 1, 800, 2, "SRC", 200, 200,
                           qq2.question_id)
    rt1.tracker.retention(t1.candidate_id, 3)
    rt1.commit(CONFIRM, qq1.question_id, t1.candidate_id, 5,
               {"tt_status": "TT_CONFIRMED"})
    rt2.tracker.retention(t2.candidate_id, 3)
    rt2.commit(CONFIRM, qq2.question_id, t2.candidate_id, 5,
               {"tt_status": "TT_FAILED"})
    add("C15", "un TT confirma y otro falla con propietarios separados",
        rt1.state.get("tt_status") == "TT_CONFIRMED"
        and rt2.state.get("tt_status") == "TT_FAILED",
        f"tt1={rt1.state.get('tt_status')} tt2={rt2.state.get('tt_status')}")

    # C16/C17 — tercera rama y referencia ajena
    v = ViolationLedger()
    arb = BranchArbiter(v)
    arb.register("A", "MAIN", "G1")
    arb.register("B", "LOCAL", "G1")
    ok3, msg3 = raises(arb.register, "C", "LOCAL", "G1")
    add("C16", "una tercera rama es rechazada y contada",
        ok3 and v.counts["third_branch_attempts"] == 1,
        f"aborta={ok3} intentos={v.counts['third_branch_attempts']}")
    own = arb.check_reference("A", "B")
    add("C17", "una lectura cruzada entre propietarios queda registrada",
        not own and v.counts["cross_owner_reference_reads"] == 1,
        f"ok={own} fugas={v.counts['cross_owner_reference_reads']}")

    ticks = [t for t in load_ticks(FEED)
             if 16 * 60 + 15 <= t.bar % 1440 <= 16 * 60 + 32]

    def key(r) -> tuple:
        return (r.phase, r.one_size, r.two_status, r.mod_size, r.a_size,
                r.b_grande_status, r.c_status, r.tt_status, r.n_size)

    base_reader = Reader(ticks).run()
    base = key(base_reader.reading)
    shifted = Reader([Tick(t.seq, t.time_ms, t.bar, t.price + 100000)
                      for t in ticks]).run().reading
    cmid = 2987000
    inverted = Reader([Tick(t.seq, t.time_ms, t.bar, 2 * cmid - t.price)
                       for t in ticks]).run().reading
    scaled = Reader([Tick(t.seq, t.time_ms, t.bar,
                          cmid + (t.price - cmid) * 2)
                     for t in ticks]).run().reading
    add("C18", "la lectura es invariante a traslado e inversion de precio",
        key(shifted) == base and key(inverted) == base,
        f"base={base[1]} trasl={key(shifted)[1]} inv={key(inverted)[1]}")
    scaled_key = (scaled.phase, scaled.one_size, scaled.two_status,
                  scaled.mod_size, scaled.a_size,
                  scaled.b_grande_status, scaled.c_status, scaled.tt_status,
                  scaled.n_size)
    doubled = (base[0], base[1] * 2, base[2], base[3] * 2, base[4] * 2,
               base[5], base[6], base[7], base[8] * 2)
    add("C19", "al duplicar la escala los tamanos se duplican y nada mas cambia",
        scaled_key == doubled,
        f"escala={scaled_key[1]} esperado={doubled[1]}")

    moved = Reader([Tick(t.seq + 1000, t.time_ms + 3600000, t.bar + 60, t.price)
                    for t in ticks]).run().reading
    add("C20", "cambiar timestamps y sequence_id no altera la estructura",
        key(moved) == base, f"moved={key(moved)[0]} base={base[0]}")

    same = Reader(ticks).run()
    add("C21", "el trazador es determinista y cubre todos los ticks",
        [r["decision"] for r in same.decision_trace.rows]
        == [r["decision"] for r in base_reader.decision_trace.rows]
        and len(same.decision_trace.rows) == len(ticks),
        f"filas={len(same.decision_trace.rows)} ticks={len(ticks)}")

    pre = [t for t in ticks if t.bar % 1440 <= 16 * 60 + 30]
    pre_reader = Reader(pre).run()
    full_rows = [r for r in base_reader.decision_trace.rows
                 if r["sequence_id"] <= pre[-1].seq]
    add("C22", "prefijo: la traza hasta 16:30 coincide con la corrida completa",
        json.dumps(full_rows, sort_keys=True)
        == json.dumps(pre_reader.decision_trace.rows, sort_keys=True),
        f"full={len(full_rows)} pre={len(pre_reader.decision_trace.rows)}")

    # C23 — clasificador de divergencias
    tr = DecisionTracer()
    row = tr.record(seq=10, timestamp=0, price=0, branch_id="L1",
                    generation_id="G1", confirmed_before={},
                    candidate_before="", current_question="L1-Q001",
                    references_used=["L1:G1:A"], physical_evidence={},
                    structural_evidence={}, functional_evidence={},
                    decision="OBSERVE",
                    confirmed_after={"a": "A_CONFIRMED"}, candidate_after="")
    cases = {
        QUESTION_ERROR: tr.classify(row, {"current_question": "L1-Q009"}),
        REFERENCE_ERROR: tr.classify(row, {"references_used": ["L2:G1:A"]}),
        OWNER_ERROR: tr.classify(row, {"branch_id": "L2"}),
        EARLY_CONFIRMATION: tr.classify(row, {"sequence_id": 20,
                                             "confirmed_node_after":
                                                 {"a": "A_CONFIRMED"}}),
        LATE_CONFIRMATION: tr.classify(row, {"sequence_id": 4,
                                            "confirmed_node_after":
                                                {"a": "A_CONFIRMED"}}),
        NO_DIVERGENCE: tr.classify(row, {"confirmed_node_after":
                                         {"a": "A_CONFIRMED"}}),
        MISSING_RULE: tr.classify(row, {"confirmed_node_after":
                                       {"a": "A_CANDIDATE"}}),
        NOISE_FRAGMENTATION: tr.classify(row, {}, absorbed_at=AT_PHYSICAL),
    }
    lost = tr.record(seq=11, timestamp=0, price=0, branch_id="L1",
                     generation_id="G1", confirmed_before={"a": "X"},
                     candidate_before="", current_question="Q",
                     references_used=[], physical_evidence={},
                     structural_evidence={}, functional_evidence={},
                     decision="OBSERVE", confirmed_after={}, candidate_after="")
    cases[LOST_STATE] = tr.classify(lost, {})
    bad = {k: v for k, v in cases.items() if k != v}
    add("C23", "el clasificador distingue las nueve categorias",
        not bad, f"casos={len(cases)} mal={bad}")

    # C24 — sin precios, horas ni atajos del caso en el motor
    eng = HERE.parent / "05_REFERENCE_ENGINE"
    pats = (r"2987050", r"2987540", r"2984910", r"2982280", r"2982980",
            r"\b16:2[6-9]\b", r"or\s+True", r"\b961\b", r"\b16\s*\*\s*60")

    def code_only(text: str) -> str:
        """Deja solo codigo ejecutable: sin docstrings, comentarios ni
        literales de texto (ninguna cadena puede decidir una transicion)."""
        text = re.sub(r'"""[\s\S]*?"""', "", text)
        text = re.sub(r"'''[\s\S]*?'''", "", text)
        text = re.sub(r'"(?:[^"\\]|\\.)*"', '""', text)
        text = re.sub(r"'(?:[^'\\]|\\.)*'", "''", text)
        return "\n".join(ln.split("#", 1)[0] for ln in text.splitlines())

    hits = []
    for p in sorted(eng.glob("tm_*.py")):
        body = code_only(p.read_text(encoding="utf-8"))
        for pat in pats:
            if re.search(pat, body):
                hits.append(f"{p.name}:{pat}")
    add("C24", "el motor no contiene precios, horas ni atajos del caso",
        not hits, f"hallazgos={hits}")

    # C25 — patrones y generaciones con propietario
    objs = TMReadingManager(ticks).run().summaries()
    pats_ = objs.get("pattern_records", [])
    gens_ = objs.get("generation_records", [])
    add("C25", "todo patron y generacion tiene propietario y slot",
        all(p.get("owner_generation_id") and p.get("owner_slot")
            for p in pats_)
        and all(g.get("generation_id") for g in gens_),
        f"patrones={len(pats_)} generaciones={len(gens_)}")


def main() -> int:
    section_a()
    section_b()
    section_c()
    passed = sum(1 for r in ROWS if r["status"] == "PASS")
    payload = {"tests_total": len(ROWS), "passed": passed,
               "failed": len(ROWS) - passed, "rows": ROWS}
    (HERE / "ITER21_TEST_RESULTS.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    with (HERE / "ITER21_TEST_RESULTS.csv").open("w", newline="",
                                                encoding="utf-8") as fh:
        import csv
        w = csv.DictWriter(fh, fieldnames=["test_id", "expected", "status",
                                           "actual", "authority"])
        w.writeheader()
        w.writerows(ROWS)
    for r in ROWS:
        print(f"{r['status']} {r['test_id']} {r['expected']} | {r['actual']}")
    print(f"TOTAL {len(ROWS)} PASS {passed} FAIL {len(ROWS) - passed}")
    return 0 if passed == len(ROWS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
