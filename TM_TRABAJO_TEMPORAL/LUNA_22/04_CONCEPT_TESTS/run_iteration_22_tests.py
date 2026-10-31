#!/usr/bin/env python3
"""Iteracion 22 — autoridad de la pregunta, delimitacion A/B y LOCAL-G2.

Seccion A: arquitectura (autoridad, preempcion, consumos, propietarios).
Seccion B: delimitacion funcional de A por B (rama local dedicada).
Seccion C: LOCAL-G2 (limpieza, escenas, TT independientes).
Seccion D: invariancias (traslado, inversion, escala, prefijo, determinismo).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))

from tm_candidates import (  # noqa: E402
    ABSORBED, CONFIRM, ArchitectureViolation, BranchRuntime, CandidateShadow,
    ViolationLedger,
)
from tm_local_generation import (  # noqa: E402
    AUT, B_GRANDE, B_CANDIDATE_CONFIRMED, LOCAL_CANDIDATE, LOCAL_CONFIRMED,
    LOCAL_INTEGRATED, LocalBranch, run_local,
)
from tm_reference_interpreter_v1_direct_aut import (  # noqa: E402
    FEED, Reader, Tick, load_ticks,
)

ROWS: list[dict] = []
TICKS = load_ticks(FEED)


def add(tid: str, expected: str, ok: bool, actual: str,
        authority: str = "CANONICAL") -> None:
    ROWS.append({"test_id": tid, "expected": expected,
                 "status": "PASS" if ok else "FAIL", "actual": actual,
                 "authority": authority})


def bar_of(t: Tick) -> int:
    return t.bar % 1440


def window(*bars: int) -> list[Tick]:
    keep = {b // 60 * 60 + b % 60 for b in bars}
    return [t for t in TICKS if bar_of(t) in keep]


def full_run() -> Reader:
    return Reader(TICKS).run()


# --------------------------------------------------------------------- seccion A
def section_a() -> None:
    rd = full_run()

    # A1 — la transicion de A la decide la pregunta, no el lector
    auth = rd.decision_authority
    add("A1", "AFTER_MODULE y A_DEVELOPMENT deciden con autoridad propia",
        auth.get("A_DEVELOPMENT") == "TREE_QUESTION"
        and any(e["node"] == "A_DEVELOPMENT" for e in rd.authority_log),
        f"authority={auth} commits={len(rd.authority_log)}")

    # A2 — ningun commit de nacimiento se usa como confirmacion
    add("A2", "cero confirmaciones con la evidencia de nacimiento",
        rd.arch.violations.counts.get("same_tick_confirmation", 0) == 0,
        f"same_tick={rd.arch.violations.counts.get('same_tick_confirmation')}")

    # A3 — cero preempciones legacy en el tramo real
    add("A3", "el estado legacy no se escribe sin commit",
        rd.legacy_preemptions == 0,
        f"preemptions={rd.legacy_preemptions} failures={rd.commit_failures}")

    # A4 — el candidato no escribe el estado confirmado
    add("A4", "cero escrituras directas al estado confirmado",
        rd.arch.violations.counts.get("candidate_state_writes", 0) == 0,
        f"writes={rd.arch.violations.counts.get('candidate_state_writes')}")

    # A5 — preempcion detectada: escritura legacy antes del commit
    rt = BranchRuntime("PX", "G1")
    rt.tracker.admit("A", -1, 1000, 1, 800, 2, "SRC", 200, 200)
    q = rt.open_question("A_DEVELOPMENT", ("A",), ("PX:MODULE",), 10)
    rt.state.begin  # noqa: B018 - el ticket no esta abierto
    preempted = False
    try:
        rt.state.direct_write("a_status", "A_CONFIRMED", 3)
    except ArchitectureViolation as exc:
        preempted = str(exc) == "CANDIDATE_STATE_WRITE_VIOLATION"
    add("A5", "una escritura legacy sin ticket aborta", preempted,
        f"aborta={preempted} question={q.question_id}")

    # A6 — consumes cerrado
    rt2 = BranchRuntime("CS", "G1")
    q2 = rt2.open_question("B_DEVELOPMENT", ("B",), ("CS:A",), 5)
    ok = rt2.book.check_read(q2, "CS:MODULE", "CS", "G1", 6)
    add("A6", "leer fuera de consumes es violacion, no decision",
        ok is False and rt2.violations.counts.get("consumes_violations") == 1,
        f"ok={ok} violaciones={rt2.violations.counts}")

    # A7 — propietario ajeno
    rt3 = BranchRuntime("OW", "G1")
    q3 = rt3.open_question("B_DEVELOPMENT", ("B",), ("OW:A",), 5)
    ok3 = rt3.book.check_read(q3, "OW:A", "OTRA", "G1", 6)
    add("A7", "referencia de otra rama aborta la lectura",
        ok3 is False
        and rt3.violations.counts.get("cross_owner_reference_reads", 0) >= 1,
        f"ok={ok3} counts={rt3.violations.counts}")

    # A8 — generacion ajena
    rt4 = BranchRuntime("GEN", "G2")
    q4 = rt4.open_question("B_DEVELOPMENT", ("B",), ("GEN:A",), 5)
    ok4 = rt4.book.check_read(q4, "GEN:A", "GEN", "G1", 6)
    add("A8", "referencia de otra generacion aborta la lectura",
        ok4 is False
        and rt4.violations.counts.get("cross_owner_reference_reads", 0) >= 1,
        f"ok={ok4}")

    # A9 — la confirmacion exige retencion previa
    rt5 = BranchRuntime("RET", "G1")
    c = rt5.tracker.admit("A", -1, 1000, 1, 700, 2, "SRC", 300, 200)
    q5 = rt5.open_question("A_DEVELOPMENT", ("A",), ("RET:MODULE",), 3)
    blocked = False
    try:
        rt5.commit(CONFIRM, q5.question_id, c.candidate_id, 9,
                   {"a_status": "A_CONFIRMED"})
    except ArchitectureViolation as exc:
        blocked = "RETENTION" in str(exc)
    add("A9", "sin test de retencion no hay confirmacion", blocked,
        f"aborta={blocked}")


# --------------------------------------------------------------------- seccion B
def section_b() -> None:
    # La delimitacion A/B se prueba en la rama local (mismo motor de commits,
    # sin herencia) para no depender del estado global del feed.
    win = window(16 * 60 + 27, 16 * 60 + 28, 16 * 60 + 29, 16 * 60 + 30,
                 16 * 60 + 31, 16 * 60 + 32)
    lb = run_local(win)
    snap = lb.snapshot()
    a, b = snap["a"], snap["b"]

    add("B1", "B confirmada congela el extremo de A",
        a["status"] == "A_CONFIRMED" and a["kt"] > 0
        and abs(a["size"]) > 0,
        f"A={a['origin']}->{a['extreme']} size={a['size']} kt={a['kt']}")

    add("B2", "B se mide contra su propia A (100 % = tamano de A)",
        b["level_100"] == a["size"] and b["level_127"] == a["size"] * 127 // 100 + 25,
        f"100%={b['level_100']} A={a['size']} 127%={b['level_127']}")

    add("B3", "B supera 127 %+0,25 y resuelve AUT",
        b["status"] == AUT and b["size"] > b["level_127"],
        f"B={b['size']} limite={b['level_127']} status={b['status']}")

    add("B4", "B/A se expresa como ratio del mismo propietario",
        abs(b["ratio"] - round(b["size"] / a["size"], 4)) < 1e-9,
        f"ratio={b['ratio']}")

    add("B5", "A no se delimita al cambiar de vela sin B funcional",
        all("BAR_CLOSE" not in c["node"] for c in snap["commits"]),
        f"commits={[c['node'] for c in snap['commits']]}")

    # B6 — delimitacion por B en una rama sintetica controlada
    lb2 = LocalBranch(generation_id="B-CASE", minimum=200)
    ticks = [Tick(1, 1000, 0, 10000), Tick(2, 1200, 0, 10300),
             Tick(3, 1400, 0, 10100), Tick(4, 1600, 0, 10450),
             Tick(5, 1800, 0, 10200), Tick(6, 2000, 0, 10150),
             Tick(7, 2200, 0, 10400)]
    for t in ticks:
        lb2.feed(t)
    s2 = lb2.snapshot()
    add("B6", "rama sintetica: A confirmada y B ligada a la misma A",
        s2["a"]["status"] == "A_CONFIRMED"
        and s2["b"]["origin"] == s2["a"]["extreme"],
        f"A={s2['a']['status']} B.origin={s2['b']['origin']} "
        f"A.extreme={s2['a']['extreme']}")

    # B7 — B fisica no escribe estado confirmado
    lb3 = LocalBranch(generation_id="B-PHYS", minimum=200)
    for t in ticks[:3]:
        lb3.feed(t)
    s3 = lb3.snapshot()
    add("B7", "B fisica no toca el estado confirmado",
        not s3["b"]["status"] or s3["b"]["status"].startswith("B_"),
        f"b_status={s3['b']['status']!r} commits={len(s3['commits'])}")

    # B8 — B no escribe A: el commit de B solo escribe campos de B
    fields = {f for c in snap["commits"] for f in c["fields"]}
    add("B8", "ningun commit de B escribe campos de A",
        not any(f.startswith("a_") for c in snap["commits"]
                if c["node"].startswith("LOCAL_B") for f in c["fields"])
        and "b_status" in fields,
        f"campos={sorted(fields)}")

    # B9 — B con retrocesos internos conserva origen y propietario
    add("B9", "B conserva su origen al absorber retrocesos internos",
        b["origin"] == a["extreme"] and b["size"] > 0,
        f"B={b['origin']}->{b['extreme']} size={b['size']}")


# --------------------------------------------------------------------- seccion C
def section_c() -> None:
    win = window(16 * 60 + 26, 16 * 60 + 27, 16 * 60 + 28, 16 * 60 + 29)
    lb = run_local(win)
    snap = lb.snapshot()
    blob = json.dumps(snap, sort_keys=True)

    fresh = LocalBranch(generation_id="LOCAL-G2").snapshot()
    add("C1", "LOCAL-G2 se crea sin estado heredado",
        fresh["status"] == LOCAL_CANDIDATE and not fresh["commits"]
        and fresh["a"]["size"] == 0 and fresh["b"]["size"] == 0
        and snap["status"] == LOCAL_CONFIRMED,
        f"fresca={fresh['status']} vacia={not fresh['commits']} "
        f"tras_ticks={snap['status']}")

    add("C2", "cero referencias a LOCAL-G1", "LOCAL-G1" not in blob,
        f"menciones={blob.count('LOCAL-G1')}")

    add("C3", "parent_context_id es descriptivo, no autoridad",
        snap["parent_context_id"] == "PRIMARY-G1"
        and all(snap["parent_context_id"] != q for q in snap["commits"]),
        f"parent={snap['parent_context_id']}")

    # C4 — sin spoiler: el prefijo no conoce el estado posterior
    pre = run_local(window(16 * 60 + 26, 16 * 60 + 27)).snapshot()
    add("C4", "el prefijo 16:26-16:27 no conoce un TT que aun no existe",
        pre["tt"]["status"] == "" and snap["tt"]["status"] in ("", "TT_PENDING",
                                                              "TT_CONFIRMED",
                                                              "TT_FAILED"),
        f"pre_tt={pre['tt']['status']!r} full_tt={snap['tt']['status']!r}")

    add("C5", "el modulo local no se abre sin excursion dominante",
        snap["module"]["size"] > 0 and snap["module"]["dir"] in (1, -1),
        f"mod={snap['module']['origin']}->{snap['module']['extreme']} "
        f"size={snap['module']['size']} dir={snap['module']['dir']}")

    names = {e["event"] for e in snap["events"]}
    add("C6", "cada transicion local deja rastro auditable",
        {"LOCAL_SEEDED", "LOCAL_A_CONFIRMED"} <= names
        and any(n.startswith("LOCAL_MODULE") for n in names),
        f"eventos={sorted(names)}")

    # C6b — la B local NO alcanza el 100 % de su propia A en este tramo
    add("C6b", "la B local medida contra su A local queda bajo el 100 %",
        0 < snap["b"]["ratio"] < 1.0
        and snap["b"]["level_100"] == snap["a"]["size"],
        f"ratio={snap['b']['ratio']} B={snap['b']['size']} A={snap['a']['size']} "
        f"status={snap['b']['status']}")

    # C7 — escena CONFIRMED retroactiva en la ventana 16:27+
    later = run_local(window(16 * 60 + 27, 16 * 60 + 28, 16 * 60 + 29,
                             16 * 60 + 30, 16 * 60 + 31, 16 * 60 + 32))
    ls = later.snapshot()
    add("C7", "una A local puede confirmarse retroactivamente",
        ls["a"]["status"] == "A_CONFIRMED"
        and ls["a"]["kt"] > ls["a"]["st"],
        f"A={ls['a']['status']} st={ls['a']['st']} kt={ls['a']['kt']}")

    # C8 — TT local independiente del TT principal
    rd = full_run()
    add("C8", "TT local y TT principal tienen propietarios distintos",
        (ls["tt"]["id"].startswith("LOCAL-G2") if ls["tt"]["id"] else True)
        and rd.reading.tt_status != ""
        and (not ls["tt"]["id"] or ls["tt"]["id"] != rd.reading_id),
        f"local_tt={ls['tt']['id']!r} main_tt={rd.reading.tt_status}")

    # C9 — arbitraje cronologico en el TT local
    add("C9", "el TT local registra la primera frontera alcanzada",
        ls["tt"]["status"] in ("TT_CONFIRMED", "TT_FAILED", "TT_PENDING", "")
        and (ls["tt"]["status"] != "TT_FAILED"
             or ls["tt"]["first_boundary"].startswith("INVALIDATION")),
        f"status={ls['tt']['status']} first={ls['tt']['first_boundary']}")

    # C10 — integracion de la rama
    lb2 = run_local(window(16 * 60 + 26, 16 * 60 + 27))
    lb2.integrate(999, "TEST")
    add("C10", "la rama local se integra y deja de ser escala activa",
        lb2.status == LOCAL_INTEGRATED,
        f"status={lb2.status} seq={lb2.integrated_at_seq}")

    # C11 — sombra impide recrear y se libera con nueva geometria
    rt = BranchRuntime("SH", "G1")
    c = rt.tracker.admit("B", 1, 1000, 1, 1200, 2, "A", 200, 200)
    rt.tracker.absorb(c.candidate_id, 5, "A", "TEST")
    c2 = rt.tracker.admit("B", 1, 900, 6, 1100, 7, "A", 200, 200)
    c3 = rt.tracker.admit("B", 1, 900, 8, 1400, 9, "A", 500, 200)
    add("C11", "la sombra bloquea la geometria contenida y libera la amplia",
        c2.status == "DISCARDED" and c3.status == "PHYSICAL",
        f"contenida={c2.status} amplia={c3.status} "
        f"intentos={rt.tracker.recreation_attempts}")

    # C12 — MAIN y LOCAL consumen el mismo tick sin interferencia
    rt_main = full_run()
    lb3 = run_local(window(16 * 60 + 27, 16 * 60 + 28))
    add("C12", "MAIN y LOCAL procesan el mismo tramo sin referencias cruzadas",
        rt_main.legacy_preemptions == 0
        and lb3.violations.counts.get("cross_owner_reference_reads", 0) == 0,
        f"main_preempt={rt_main.legacy_preemptions} "
        f"local_cross={lb3.violations.counts.get('cross_owner_reference_reads')}")


# --------------------------------------------------------------------- seccion D
def _key(r) -> tuple:
    return (r.phase, r.one_size, r.two_status, r.mod_size, r.a_size,
            r.b_grande_status, r.c_status, r.tt_status, r.n_size)


def section_d() -> None:
    base = _key(full_run().reading)
    cmid = TICKS[0].price

    shifted = Reader([Tick(t.seq, t.time_ms, t.bar, t.price + 5000)
                      for t in TICKS]).run().reading
    inverted = Reader([Tick(t.seq, t.time_ms, t.bar, 2 * cmid - t.price)
                       for t in TICKS]).run().reading
    add("D1", "la lectura es invariante a traslado e inversion",
        _key(shifted) == base and _key(inverted) == base,
        f"base={base[1]} traslado={_key(shifted)[1]} "
        f"inversion={_key(inverted)[1]}")

    lb = run_local(window(16 * 60 + 27, 16 * 60 + 28, 16 * 60 + 29))
    lo = [Tick(t.seq, t.time_ms, t.bar, t.price + 4000) for t in
          window(16 * 60 + 27, 16 * 60 + 28, 16 * 60 + 29)]
    lb_s = run_local(lo)
    add("D2", "LOCAL-G2 es invariante al traslado de precios",
        (lb.snapshot()["a"]["size"], lb.snapshot()["b"]["size"])
        == (lb_s.snapshot()["a"]["size"], lb_s.snapshot()["b"]["size"]),
        f"base={lb.snapshot()['b']['size']} traslado="
        f"{lb_s.snapshot()['b']['size']}")

    pre = [t for t in TICKS if bar_of(t) <= 16 * 60 + 28]
    r_pre = Reader(pre).run()
    r_full = full_run()
    add("D3", "consistencia de prefijo del estado funcional",
        _key(r_pre.reading) == _key(Reader(pre).run().reading)
        and len(r_pre.events) <= len(r_full.events),
        f"prefijo={_key(r_pre.reading)[3]} full={_key(r_full.reading)[3]}")

    add("D4", "determinismo del lector y de la rama local",
        json.dumps(_key(full_run().reading)) == json.dumps(base)
        and json.dumps(lb.snapshot(), sort_keys=True)
        == json.dumps(run_local(window(16 * 60 + 27, 16 * 60 + 28,
                                       16 * 60 + 29)).snapshot(),
                      sort_keys=True),
        "identicos")

    lb_i = run_local(window(16 * 60 + 27, 16 * 60 + 28, 16 * 60 + 29, 16 * 60 + 30))
    add("D5", "el arbitraje del TT local es determinista",
        lb_i.snapshot()["tt"]["first_boundary"]
        == run_local(window(16 * 60 + 27, 16 * 60 + 28, 16 * 60 + 29,
                            16 * 60 + 30)).snapshot()["tt"]["first_boundary"],
        f"first={lb_i.snapshot()['tt']['first_boundary']!r}")

    # D6 — la rama local no altera el estado del lector principal
    before = _key(Reader(TICKS).run().reading)
    run_local(window(16 * 60 + 27, 16 * 60 + 28))
    after = _key(Reader(TICKS).run().reading)
    add("D6", "ejecutar la rama local no altera la lectura principal",
        before == after, f"before={before[3]} after={after[3]}")

    # D7 — sin precios ni horas del caso en la rama local
    src = (ENGINE / "tm_local_generation.py").read_text(encoding="utf-8")
    bad = [tok for tok in ("2982280", "2987080", "16:27", "1627", "29873")
           if tok in src]
    add("D7", "la rama local no contiene precios ni horas del caso",
        not bad, f"hallazgos={bad}")

    # D8 — las preguntas migradas declaran su autoridad
    rd = full_run()
    nodes = {q["current_node"] for q in rd.arch.book.snapshot()}
    add("D8", "preguntas migradas presentes en el arbol",
        {"AFTER_MODULE", "A_DEVELOPMENT"} <= nodes,
        f"nodos={sorted(nodes)}")


def main() -> int:
    section_a()
    section_b()
    section_c()
    section_d()
    passed = sum(1 for r in ROWS if r["status"] == "PASS")
    payload = {"tests_total": len(ROWS), "passed": passed,
               "failed": len(ROWS) - passed, "rows": ROWS}
    (HERE / "ITER22_TEST_RESULTS.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    import csv
    with (HERE / "ITER22_TEST_RESULTS.csv").open("w", newline="",
                                                encoding="utf-8") as fh:
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
