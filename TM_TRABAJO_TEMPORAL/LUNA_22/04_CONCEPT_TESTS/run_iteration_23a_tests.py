#!/usr/bin/env python3
"""Iteracion 23A — auditoria geometrica de LOCAL-G2.

Seccion G: invariantes de geometria (direccion, origen de A, genealogia del
modulo y del TT) sobre secuencias sinteticas controladas.
Seccion H: umbrales 100 % / 127 % + 0,25 y genealogia B -> B Grande -> AUT -> C.
Seccion I: TT local (armado, confirmacion, fallo, trazabilidad, independencia).
Seccion J: invariancias (traslado, inversion, escala, tiempos, sequence_id,
prefijo, determinismo) y abortos de arquitectura.

Ninguna prueba usa precios ni horas del caso como condicion: los importes son
entradas sinteticas de la secuencia, no reglas del motor.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))

from tm_candidates import (  # noqa: E402
    CONFIRM, ArchitectureViolation, BranchRuntime,
)
from tm_local_generation import (  # noqa: E402
    AUT, B_CANDIDATE_CONFIRMED, B_GRANDE, TT_A_ORIGIN, TT_FINAL_A, LocalBranch,
    run_local,
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


def window(ticks, lo: int, hi: int):
    return [t for t in ticks if lo <= t.bar % 1440 <= hi]


def synth(prices, minimum: int = 200, bars=None, gen: str = "T23",
          t0: int = 60_000_000, step: int = 1000, seq0: int = 1000):
    lb = LocalBranch(generation_id=gen, minimum=minimum)
    bars = bars or [0] * len(prices)
    for i, p in enumerate(prices):
        lb.feed(Tick(seq0 + i, t0 + i * step, bars[i], p))
    return lb


def debug(lb: LocalBranch, name: str) -> None:
    print(f"--- {name}")
    for e in lb.events:
        print(f"  {e['seq']:>5} {e['event']:<32} {e['detail']}")


#: Ciclo sintetico: modulo dominante, A contraria, B en la direccion dominante.
CYCLE = [10400, 10100, 10000, 10400, 10200]


# --------------------------------------------------------------------- seccion G
def section_g() -> None:
    lb = synth(CYCLE)
    s = lb.snapshot()
    g = s["geometry"]
    add("G1", "direccion del modulo coherente con origen/extremo",
        g["local_module_direction_valid"] and g["local_module_size_valid"]
        and (s["module"]["extreme"] - s["module"]["origin"])
        * s["module"]["dir"] > 0,
        f"mod={s['module']['origin']}->{s['module']['extreme']} "
        f"dir={s['module']['dir']} geo={g['local_module_direction_valid']}")

    # G2 — el modulo extendido no abre A mientras no haya retroceso autonomo
    lb2 = synth([10400, 10100, 9900, 9800, 9700])
    add("G2", "un modulo que se extiende no abre A prematura",
        lb2.a_status == "" and lb2.a_origin == 0
        and lb2.module_size == 700,
        f"a_status={lb2.a_status!r} module={lb2.module_size}")

    add("G3", "A nace desde el extremo funcional del modulo",
        s["a"]["origin"] == s["a"]["birth_module_extreme"]
        and s["a"]["source_module_id"] != "",
        f"A.origin={s['a']['origin']} birth_module_extreme="
        f"{s['a']['birth_module_extreme']} "
        f"source={s['a']['source_module_id']}")

    # G4/G5 — en un ciclo donde A NO supera al modulo, A y modulo no comparten
    # origen y no hay reclasificacion.
    add("G4", "A no comparte origen con el modulo sin reclasificacion",
        s["a"]["origin"] != s["module"]["origin"]
        and s["module_reclassifications"] == []
        and s["geometry"]["local_A_origin_valid"],
        f"mod.origin={s['module']['origin']} A.origin={s['a']['origin']} "
        f"reclas={len(s['module_reclassifications'])}")

    # G5 — A mayor que el modulo: reclasificacion EXPLICITA con genealogia
    lb5 = synth([10400, 10100, 10000, 10450, 10250])
    s5 = lb5.snapshot()
    rec = s5["module_reclassifications"]
    add("G5", "A mayor que el modulo provoca reclasificacion trazada",
        len(rec) == 1 and rec[0]["previous"]["module_id"]
        and rec[0]["previous"]["size"] > 0
        and rec[0]["new"]["size"] == s5["a"]["size"]
        and s5["module"]["source_function_id"] == s5["a"]["id"]
        and s5["geometry"]["local_module_direction_valid"],
        f"reclas={json.dumps(rec)[:160]}")

    # G6 — A continua entre velas (no la cierra el cambio de vela)
    lb6 = synth([10400, 10100, 10000, 10400, 10200, 10250, 10300],
                bars=[0, 0, 1, 1, 2, 2, 3])
    snap6 = lb6.snapshot()
    add("G6", "A conserva continuidad a traves del cambio de vela",
        snap6["a"]["status"] == "A_CONFIRMED"
        and all("BAR_CLOSE" not in c["node"] for c in snap6["commits"]),
        f"A={snap6['a']['status']} commits={[c['node'] for c in snap6['commits']]}")

    # G7 — B fisica no delimita A
    lb7 = synth(CYCLE)
    add("G7", "una B fisica no delimita A",
        lb7.b_status == "B_PHYSICAL" and lb7.a_status == "A_CONFIRMED"
        and lb7.a_knowledge_time > 0,
        f"B={lb7.b_status} A={lb7.a_status}")

    # G8 — una B con solo evidencia fisica no escribe nada en A
    lb8 = synth(CYCLE[:4])
    before = (lb8.a_size, lb8.a_knowledge_time)
    lb8.feed(Tick(2000, 60_020_000, 0, 10350))
    add("G8", "una B fisica no modifica ni confirma A",
        (lb8.a_size, lb8.a_knowledge_time) == before
        and not any(c["node"].startswith("LOCAL_B") for c in lb8.commits),
        f"A={lb8.a_size}/{lb8.a_knowledge_time} antes={before} "
        f"b={lb8.b_status} commits={[c['node'] for c in lb8.commits]}")

    # G9 — B funcional delimita A (commit de B, no escritura de B en A)
    ok9 = (s["a"]["status"] == "A_CONFIRMED" and s["a"]["kt"] > 0
           and s["b"]["origin"] == s["a"]["extreme"]
           and not any(f.startswith("a_") for c in s["commits"]
                       if c["node"].startswith("LOCAL_B")
                       for f in c["fields"]))
    add("G9", "la confirmacion funcional de B delimita A", ok9,
        f"A.kt={s['a']['kt']} B.origin={s['b']['origin']} "
        f"A.extreme={s['a']['extreme']}")

    add("G10", "B nace exactamente en el extremo de su A",
        s["b"]["origin"] == s["a"]["extreme"]
        and s["b"]["source_function_id"] == s["a"]["id"],
        f"B.origin={s['b']['origin']} A.extreme={s['a']['extreme']} "
        f"source={s['b']['source_function_id']}")

    s12 = synth(CYCLE + [10100]).snapshot()
    add("G11", "el ratio B/A es exacto y del mismo propietario",
        s12["b"]["ratio"] == round(s12["b"]["size"] / s12["a"]["size"], 4)
        and s12["b"]["level_100"] == s12["a"]["size"]
        and s12["geometry"]["local_B_ratio_traceable"],
        f"ratio={s12['b']['ratio']} 100%={s12['b']['level_100']} "
        f"A={s12['a']['size']}")

    # G12/G13 — B bajo el 100 % no es B Grande y no arma TT ni A-tendencia
    add("G12", "una B bajo el 100 % no es B Grande",
        s12["b"]["status"] == B_CANDIDATE_CONFIRMED and s12["b"]["ratio"] < 1.0,
        f"status={s12['b']['status']} ratio={s12['b']['ratio']}")

    add("G13", "sin B Grande no se arma TT por la via de tendencia",
        s["tt"]["id"] == "" and s["tt"]["status"] == ""
        and s["b"]["grande_kt"] == 0,
        f"tt={s['tt']['status']!r} grande_kt={s['b']['grande_kt']}")

    # G14 — evidencia de nacimiento distinta de la de confirmacion
    cand = s["a"]["source_module_id"] and True
    commits = [c for c in s["commits"] if c["node"] == "LOCAL_A_DEVELOPMENT"]
    add("G14", "la evidencia de nacimiento difiere de la de confirmacion",
        bool(commits) and commits[0]["seq"] > 0 and lb.a_candidate_seq
        and commits[0]["seq"] >= lb.a_candidate_seq and cand,
        f"birth_seq={lb.a_candidate_seq} confirm_seq="
        f"{commits[0]['seq'] if commits else None}")

    # G15 — una direccion invertida se detecta (no se repara en silencio)
    lb15 = synth(CYCLE)
    lb15.module_dir = -lb15.module_dir
    add("G15", "una direccion de modulo invertida se detecta",
        lb15.geometry()["local_module_direction_valid"] is False,
        f"geo={lb15.geometry()['local_module_direction_valid']}")


# --------------------------------------------------------------------- seccion H
def section_h() -> None:
    # H1 — B toca EXACTAMENTE el 100 %: el igual se acepta como B Grande
    lb = synth([10400, 10100, 10000, 10400, 10200, 10000, 10000])
    s = lb.snapshot()
    add("H1", "B que alcanza exactamente el 100 % confirma B Grande",
        s["b"]["size"] == s["a"]["size"] == 400
        and s["b"]["status"] == B_GRANDE,
        f"B={s['b']['size']} A={s['a']['size']} status={s['b']['status']}")

    lb2 = synth([10400, 10100, 10000, 10400, 10200, 10000, 9950])
    s2 = lb2.snapshot()
    add("H2", "B dentro de 100 %-127 %+0,25 sigue siendo B Grande",
        s2["b"]["status"] == B_GRANDE
        and s2["a"]["size"] <= s2["b"]["size"] <= s2["b"]["level_127"],
        f"B={s2['b']['size']} A={s2['a']['size']} "
        f"limite={s2['b']['level_127']} status={s2['b']['status']}")

    lb3 = synth([10400, 10100, 10000, 10400, 10200, 10000, 9800, 9700])
    s3 = lb3.snapshot()
    add("H3", "superar el limite por un tick resuelve AUT",
        s3["b"]["status"] == AUT and s3["b"]["size"] > s3["b"]["level_127"],
        f"B={s3['b']['size']} limite={s3['b']['level_127']} "
        f"status={s3['b']['status']}")

    lb4 = synth([10400, 10100, 10000, 10400, 10200, 10000, 9950, 10150])
    names = {e["event"] for e in lb4.events}
    add("H4", "C aparece solo despues de B Grande",
        "LOCAL_C_OPENED" in names and lb4.b_grande_kt > 0,
        f"eventos={sorted(n for n in names if n.startswith('LOCAL_C'))} "
        f"B={lb4.b_status} grande_kt={lb4.b_grande_kt}")

    lb5 = synth([10400, 10100, 10000, 10400, 10200, 10000, 9800, 9700])
    s5 = lb5.snapshot()
    add("H5", "B Grande registra el cruce causal antes del AUT",
        s5["b"]["grande_status"] in (B_GRANDE, "CAUSAL_CROSS_IN_AUT_TICK")
        and s5["b"]["grande_kt"] > 0,
        f"grande_status={s5['b']['grande_status']} kt={s5['b']['grande_kt']}")


# --------------------------------------------------------------------- seccion I
def section_i() -> None:
    # TT real de la rama sembrada en 16:27 (sonda de sensibilidad)
    l27 = run_local(window(TICKS, 16 * 60 + 27, 16 * 60 + 29)).snapshot()
    tt = l27["tt"]
    add("I1", "el TT exige modulo propietario registrado",
        bool(tt["module_id"]) and tt["module_size"] > 0
        and l27["geometry"]["local_TT_module_traceable"],
        f"id={tt['module_id']} size={tt['module_size']}")

    add("I2", "el TT exige final_A propietario",
        tt["final_a"] == l27["a"]["extreme"]
        and l27["geometry"]["local_TT_final_A_traceable"],
        f"final_A={tt['final_a']} A.extreme={l27['a']['extreme']}")

    add("I3", "el objetivo del TT es derivable de su propia genealogia",
        tt["objective"] == tt["final_a"] + tt["dir"] * tt["module_size"]
        and l27["geometry"]["local_TT_objective_derivable"],
        f"objetivo={tt['objective']} final_A={tt['final_a']} "
        f"dir={tt['dir']} modulo={tt['module_size']}")

    add("I4", "la ruta de activacion del TT queda trazada",
        tt["source_function_id"] != "" and tt["opened_at_seq"] > 0
        and tt["invalidation_kind"] == TT_FINAL_A,
        f"source={tt['source_function_id']} seq={tt['opened_at_seq']} "
        f"kind={tt['invalidation_kind']}")

    add("I5", "un TT nacido de un AUT invalida en final_A, no en el origen de A",
        tt["invalidation"] == tt["final_a"],
        f"invalidacion={tt['invalidation']} final_A={tt['final_a']} "
        f"A.origin={l27['a']['origin']}")

    add("I6", "el TT local se confirma cuando alcanza su objetivo",
        tt["status"] == "TT_CONFIRMED"
        and tt["first_boundary"].startswith("OBJECTIVE"),
        f"status={tt['status']} first={tt['first_boundary']}")

    # TT sin modulo trazable: no se arma
    lb = synth([10400, 10100, 10000, 10400, 10200])
    lb.module_size = 0
    lb.b_origin = 10400
    lb.b_dir = -1
    lb._arm_local_tt(Tick(3000, 60_030_000, 0, 10100))
    add("I7", "un TT sin modulo propietario se rechaza", lb.tt_id == "",
        f"tt_id={lb.tt_id!r} status={lb.tt_status!r}")

    # TT que falla: vuelve a final_A antes del objetivo
    lb8 = synth([10400, 10100, 10000, 10400, 10200, 10000, 9800, 10450])
    s8 = lb8.snapshot()
    add("I8", "un TT falla si su invalidacion se cruza primero",
        s8["tt"]["status"] == "TT_FAILED"
        and "INVALIDATION" in s8["tt"]["first_boundary"],
        f"status={s8['tt']['status']} first={s8['tt']['first_boundary']}")

    # Mismo tramo en dos ramas: sin fugas
    main = Reader(TICKS).run()
    loc = run_local(window(TICKS, 16 * 60 + 26, 16 * 60 + 29))
    add("I9", "MAIN y LOCAL procesan el mismo tick sin referencias cruzadas",
        loc.violations.counts.get("cross_owner_reference_reads", 0) == 0
        and loc.violations.counts.get("consumes_violations", 0) == 0
        and main.arch.violations.counts.get("cross_owner_reference_reads",
                                           0) == 0,
        f"local={loc.violations.counts} ")

    add("I10", "los TT de MAIN y LOCAL tienen propietario y objetivo propios",
        (not tt["id"]) or tt["id"].startswith("LOCAL-G2")
        and (tt["objective"] != main.reading.tt_objective
             or main.reading.tt_objective == 0),
        f"local={tt['id']}@{tt['objective']} "
        f"main={main.reading.tt_status}@{main.reading.tt_objective}")

    add("I11", "una A usada como tendencia exigiria B Grande valida",
        l27["geometry"]["local_A_trend_requires_valid_B_grande"],
        f"kind={tt['invalidation_kind']} grande={l27['b']['grande_status']}")


# --------------------------------------------------------------------- seccion J
def invariants(transform) -> dict:
    ticks = window(TICKS, 16 * 60 + 26, 16 * 60 + 29)
    return run_local([transform(t) for t in ticks]).snapshot()


def base_signature(snap: dict) -> dict:
    return {"module": snap["module"]["size"],
            "module_dir": snap["module"]["dir"],
            "a_size": snap["a"]["size"], "a_dir": snap["a"]["dir"],
            "b_size": snap["b"]["size"], "b_ratio": snap["b"]["ratio"],
            "tt": snap["tt"]["status"],
            "first_boundary": snap["tt"]["first_boundary"].split("@")[0]}


def section_j() -> None:
    snap = run_local(window(TICKS, 16 * 60 + 26, 16 * 60 + 29)).snapshot()
    sig = base_signature(snap)

    shifted = base_signature(invariants(
        lambda t: Tick(t.seq, t.time_ms, t.bar, t.price + 50000)))
    add("J1", "el traslado de precios conserva la geometria",
        shifted == sig, f"{shifted} vs {sig}")

    base_price = window(TICKS, 16 * 60 + 26, 16 * 60 + 26)[0].price
    inverted = base_signature(invariants(
        lambda t: Tick(t.seq, t.time_ms, t.bar, 2 * base_price - t.price)))
    add("J2", "la inversion vertical conserva tamanos y cambia direccion",
        inverted["module"] == sig["module"]
        and inverted["module_dir"] == -sig["module_dir"],
        f"size={inverted['module']} dir={inverted['module_dir']}")

    scaled_t = base_signature(invariants(
        lambda t: Tick(t.seq, t.time_ms, t.bar, t.price * 2)))
    add("J3", "el escalado duplica los tamanos sin cambiar la direccion",
        scaled_t["module"] == 2 * sig["module"]
        and scaled_t["module_dir"] == sig["module_dir"],
        f"size={scaled_t['module']} dir={scaled_t['module_dir']}")

    retimed = base_signature(invariants(
        lambda t: Tick(t.seq, t.time_ms + 10 ** 6, t.bar, t.price)))
    add("J4", "cambiar los timestamps no altera la geometria",
        retimed == sig, f"{retimed}")

    reseq = base_signature(invariants(
        lambda t: Tick(t.seq + 100000, t.time_ms, t.bar, t.price)))
    add("J5", "cambiar los sequence_id no altera la geometria",
        reseq == sig, f"{reseq}")

    # Prefijo: el estado registrado tick a tick coincide con la ejecucion corta
    lb = LocalBranch(generation_id="LOCAL-G2", minimum=200)
    last_at_1628 = None
    for t in window(TICKS, 16 * 60 + 26, 16 * 60 + 29):
        lb.feed(t)
        if t.bar % 1440 == 16 * 60 + 28:
            last_at_1628 = lb.snapshot()
    short = run_local(window(TICKS, 16 * 60 + 26, 16 * 60 + 28)).snapshot()
    add("J6", "el prefijo 16:28 coincide con la ejecucion corta",
        last_at_1628 is not None
        and base_signature(last_at_1628) == base_signature(short)
        and last_at_1628["a"] == short["a"],
        f"{base_signature(last_at_1628) if last_at_1628 else None}")

    again = run_local(window(TICKS, 16 * 60 + 26, 16 * 60 + 29)).snapshot()
    add("J7", "la rama local es determinista",
        json.dumps(again, sort_keys=True) == json.dumps(snap, sort_keys=True),
        "snapshots identicos"
        if json.dumps(again, sort_keys=True) == json.dumps(snap, sort_keys=True)
        else "difieren")

    # Abortos de arquitectura
    rt = BranchRuntime("PX", "G1")
    rt.tracker.admit("A", -1, 1000, 1, 800, 2, "SRC", 200, 200)
    preempted = False
    try:
        rt.state.direct_write("a_status", "A_CONFIRMED", 3)
    except ArchitectureViolation as exc:
        preempted = str(exc) == "CANDIDATE_STATE_WRITE_VIOLATION"
    add("J8", "una escritura legacy sin ticket aborta", preempted,
        f"aborta={preempted}")

    rt2 = BranchRuntime("OW", "G1")
    q = rt2.open_question("B_DEVELOPMENT", ("B",), ("OW:A",), 5)
    ok = rt2.book.check_read(q, "OW:A", "OTRA", "G1", 6)
    add("J9", "una referencia de otra rama aborta la lectura",
        ok is False
        and rt2.violations.counts.get("cross_owner_reference_reads", 0) >= 1,
        f"ok={ok}")

    rt3 = BranchRuntime("CS", "G1")
    q3 = rt3.open_question("B_DEVELOPMENT", ("B",), ("CS:A",), 5)
    ok3 = rt3.book.check_read(q3, "CS:MODULE", "CS", "G1", 6)
    add("J10", "una lectura fuera de consumes es violacion",
        ok3 is False and rt3.violations.counts.get("consumes_violations") == 1,
        f"ok={ok3}")

    # Ausencia de valores del caso en el motor local
    src = (ENGINE / "tm_local_generation.py").read_text(encoding="utf-8")
    banned = [x for x in ("2987380", "2986260", "2985060", "16:26", "16:27",
                          "1626", "1627") if x in src]
    add("J11", "la rama local no contiene precios ni horas del caso",
        not banned, f"encontrados={banned}")


def main() -> int:
    if "--debug" in sys.argv:
        for name, prices in (("CYCLE", CYCLE),
                             ("CYCLE+A-big", [10400, 10100, 10300, 9500]),
                             ("H1", [10400, 10100, 10000, 10400, 10200,
                                     10000, 9900]),
                             ("H2", [10400, 10100, 10000, 10400, 10200,
                                     10000, 9850]),
                             ("H3", [10400, 10100, 10000, 10400, 10200,
                                     10000, 9800, 9700])):
            debug(synth(prices), name)
        return 0
    section_g()
    section_h()
    section_i()
    section_j()
    total = len(ROWS)
    passed = sum(1 for r in ROWS if r["status"] == "PASS")
    print(f"TOTAL {total} PASS {passed} FAIL {total - passed}")
    for r in ROWS:
        if r["status"] == "FAIL":
            print(f"  FAIL {r['test_id']}: {r['expected']} | {r['actual']}")
    out = HERE / "ITER23A_TEST_RESULTS.json"
    out.write_text(json.dumps({
        "iteration": "23A", "tests_total": total, "passed": passed,
        "failed": total - passed, "rows": ROWS,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (HERE / "ITER23A_TEST_RESULTS.csv").write_text(
        "test_id,expected,status,actual,authority\n" + "\n".join(
            f"{r['test_id']},\"{r['expected']}\",{r['status']},"
            f"\"{r['actual']}\",{r['authority']}" for r in ROWS) + "\n",
        encoding="utf-8")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
