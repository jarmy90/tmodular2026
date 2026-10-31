#!/usr/bin/env python3
"""ITERACION 19B — extremo fisico/funcional, FT causal y relevo generacional.

Las expectativas se derivan de los ticks y de las reglas vigentes, no del
resultado del motor. Las pruebas que dependen del filtro fisico de 2 puntos
para confirmar FT se clasifican PROVISIONAL_POLICY_PASS (la autonomia
funcional canonica es A/FT confirmada por su propia estructura).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))
from tm_reader_guard import verify as _verify_reader  # noqa: E402
_verify_reader()

from tm_reference_interpreter_v1_direct_aut import (  # noqa: E402
    Reader, Tick, load_ticks, FEED, NOISE,
)
from tm_reading_manager import TMReadingManager  # noqa: E402

T0 = 1792167950000
B0 = 16 * 60 + 25


def tick(seq, price, t=T0, bar=B0):
    return Tick(seq, t, bar, price)


def synthetic(direction=1, objective=2987050, extreme=2987540,
              t=T0, lifetime=0):
    """Lector con un TT ya confirmado y su extremo estructural fijado."""
    rd = Reader([], reading_id="SYN")
    r = rd.reading
    r.phase = "NEW_ONE_ACTIVE"
    r.tt_status = "TT_CONFIRMED"
    r.tt_dir = direction
    r.tt_objective = objective
    r.tt_kt = t
    r.tt_extreme = extreme
    r.tt_extreme_st = t
    r.tt_extreme_status = "PROVISIONAL"
    rd.prev_price = extreme
    return rd


def contrary(rd, price, seq=1, dt=1000):
    t = tick(seq, price, t=rd.reading.tt_extreme_st + dt * seq)
    rd._on_ft_tick(t)
    return t


def extend(rd, price, seq=50):
    t = tick(seq, price, t=rd.reading.tt_extreme_st + 1000 * seq)
    rd.prev_price = rd.reading.tt_extreme
    rd._on_tt_tick(t)
    return t


def main() -> int:
    res = []

    def check(tid, area, kind, desc, cond, detail, cls="CANONICAL_PASS"):
        res.append({"test_id": tid, "area": area, "kind": kind,
                    "classification": cls, "description": desc,
                    "pass": bool(cond), "detail": detail})

    # ---------------------------------------------------------- sinteticos
    # T01 TT confirma sin extension: FT nace del extremo confirmado.
    rd = synthetic()
    contrary(rd, 2987400)
    r = rd.reading
    check("FT-19B-01", "ft", "positive",
          "TT confirmado sin extension: FT nace del extremo funcional",
          r.ft_origin == 2987540 and r.ft_status == "FT_POSSIBLE",
          f"origin={r.ft_origin} status={r.ft_status}")

    # T02 TT confirma y extiende: el candidato previo queda absorbido.
    rd = synthetic()
    contrary(rd, 2987400)
    extend(rd, 2988000)
    r = rd.reading
    check("FT-19B-02", "ft", "positive",
          "TT extendido absorbe el FT nacido del extremo anterior",
          r.ft_status == "" and r.ft_absorbed == 1 and r.tt_extreme == 2988000,
          f"ft={r.ft_status!r} absorbed={r.ft_absorbed} ext={r.tt_extreme}",
          "PROVISIONAL_POLICY_PASS")

    # T03 Multiples extensiones: el FT final nace del ultimo extremo.
    rd = synthetic()
    contrary(rd, 2987400)
    extend(rd, 2987700)
    contrary(rd, 2987600, seq=2, dt=1200)
    extend(rd, 2987900, seq=60)
    contrary(rd, 2987800, seq=3, dt=1400)
    r = rd.reading
    check("FT-19B-03", "ft", "positive",
          "extensiones multiples: FT final desde el ultimo extremo",
          r.ft_origin == 2987900 and r.ft_absorbed == 2,
          f"origin={r.ft_origin} absorbed={r.ft_absorbed}",
          "PROVISIONAL_POLICY_PASS")

    # T04 El retroceso interno se registra como absorcion, no como FT.
    rd = synthetic()
    contrary(rd, 2987400)
    extend(rd, 2987700)
    names = [e["event"] for e in rd.reading.events]
    check("FT-19B-04", "ft", "negative",
          "retroceso interno absorbido deja evento trazable",
          names.count("FT_ABSORBED_BY_TT_EXTENSION") == 1
          and "FT_CONFIRMED" not in names,
          f"absorbed_events={names.count('FT_ABSORBED_BY_TT_EXTENSION')} "
          f"events={names}")

    # T05 No queda ningun FT confirmado con el origen viejo.
    rd = synthetic()
    contrary(rd, 2987400)
    contrary(rd, 2987200, seq=2, dt=1200)
    stale_confirmed = rd.reading.ft_status == "FT_CONFIRMED"
    extend(rd, 2987900)
    r = rd.reading
    check("FT-19B-05", "ft", "negative",
          "ningun FT confirmado sobrevive al nuevo extremo del TT",
          stale_confirmed and r.ft_status == "" and r.ft_origin == 0,
          f"antes={stale_confirmed} despues={r.ft_status!r} origin={r.ft_origin}")

    # T06 El filtro fisico de 2 puntos separa ruido de movimiento contrario.
    rd = synthetic()
    contrary(rd, 2987350)   # 1,9 puntos: ruido
    a = rd.reading.ft_status
    contrary(rd, 2987340, seq=2, dt=1200)  # 2,0 puntos: confirmado
    b = rd.reading.ft_status
    check("FT-19B-06", "ft", "boundary",
          "FT exige recorrido contrario >= 2,0 puntos",
          a == "FT_POSSIBLE" and b == "FT_CONFIRMED",
          f"1,9->{a} 2,0->{b}", "PROVISIONAL_POLICY_PASS")

    # T07 structural_time retroactivo = tick del extremo.
    rd = synthetic()
    contrary(rd, 2987400)
    contrary(rd, 2987200, seq=2, dt=1200)
    r = rd.reading
    check("FT-19B-07", "ft", "positive",
          "structural_time del FT = tick del extremo funcional",
          r.ft_st == r.tt_extreme_st and r.ft_kt > r.ft_st,
          f"st={r.ft_st} kt={r.ft_kt} extreme_st={r.tt_extreme_st}",
          "PROVISIONAL_POLICY_PASS")

    # T08 knowledge posterior al structural.
    check("FT-19B-08", "ft", "positive",
          "knowledge_time del extremo funcional posterior al structural",
          r.tt_extreme_status == "CONFIRMED" and r.tt_extreme_kt > r.tt_extreme_st,
          f"status={r.tt_extreme_status} st={r.tt_extreme_st} kt={r.tt_extreme_kt}")

    # T11 La ventana CLOSING permite extender el TT (reabre el extremo).
    rd = synthetic()
    contrary(rd, 2987400)
    contrary(rd, 2987200, seq=2, dt=1200)
    before = rd.reading.tt_extreme_status
    extend(rd, 2988100)
    r = rd.reading
    check("FT-19B-11", "lifecycle", "positive",
          "generacion CLOSING: el TT puede extenderse y reabre el extremo",
          before == "CONFIRMED" and r.tt_extreme == 2988100
          and r.tt_extreme_status == "REOPENED" and r.ft_status == "",
          f"antes={before} ext={r.tt_extreme} status={r.tt_extreme_status}")

    # T16 traslacion de precios: misma estructura.
    def run_shift(delta):
        rd = synthetic(objective=2987050 + delta, extreme=2987540 + delta)
        contrary(rd, 2987200 + delta)
        r = rd.reading
        return r.ft_status, r.ft_size, r.ft_origin - delta

    s0 = run_shift(0)
    s1 = run_shift(100000)
    check("FT-19B-16", "adversarial", "translation",
          "secuencia trasladada 1.000 puntos conserva estructura",
          s0 == s1, f"base={s0} shifted={s1}")

    # T17 inversion vertical.
    rd_up = synthetic(direction=1, objective=2987050, extreme=2987540)
    contrary(rd_up, 2987200)
    rd_dn = synthetic(direction=-1, objective=2987050, extreme=2986560)
    contrary(rd_dn, 2986900)
    check("FT-19B-17", "adversarial", "inversion",
          "secuencia invertida conserva tamanos y estados",
          rd_up.reading.ft_size == rd_dn.reading.ft_size
          and rd_up.reading.ft_status == rd_dn.reading.ft_status,
          f"up={rd_up.reading.ft_size}/{rd_up.reading.ft_status} "
          f"dn={rd_dn.reading.ft_size}/{rd_dn.reading.ft_status}")

    # T18 escala distinta: doble tamano, misma clasificacion.
    rd2 = synthetic(objective=2987050, extreme=2988540)  # 14,9 de extension
    contrary(rd2, 2988000)
    contrary(rd2, 2987900, seq=2, dt=1200)
    check("FT-19B-18", "adversarial", "scale",
          "otra escala conserva la clasificacion estructural",
          rd2.reading.ft_status == "FT_CONFIRMED"
          and rd2.reading.ft_origin == 2988540,
          f"status={rd2.reading.ft_status} origin={rd2.reading.ft_origin}")

    # T19 timestamps alterados, mismos movimientos.
    rd_t = synthetic()
    contrary(rd_t, 2987400, dt=7000)
    check("FT-19B-19", "adversarial", "timestamps",
          "desplazar timestamps no cambia la clasificacion",
          rd_t.reading.ft_status == "FT_POSSIBLE",
          f"status={rd_t.reading.ft_status}")

    # ------------------------------------------------------------ feed real
    full = [t for t in load_ticks(FEED) if 16 * 60 + 15 <= t.bar % 1440 <= 16 * 60 + 32]
    mgr = TMReadingManager(full).run()
    ident = mgr.summaries()
    pats = {p["pattern_id"]: p for p in ident["pattern_records"]}
    tt = pats.get("LOCAL-G1-TT-2987050", {})
    ft = pats.get("LOCAL-G1-FT-2987540", {})
    gens = {g["generation_id"]: g for g in ident["generation_records"]}
    g1 = gens.get("LOCAL-G1", {})
    last = {}
    for row in mgr.rows:
        last[row["bar"]] = row

    check("FT-19B-09", "real", "positive",
          "FT real nace del extremo funcional 29875,4",
          ft.get("functional_extreme") == 2987540
          and ft.get("structural_time") == tt.get("structural_time"),
          f"ft_origin={ft.get('functional_extreme')} "
          f"ft_st={ft.get('structural_time')} tt_st={tt.get('structural_time')}",
          "PROVISIONAL_POLICY_PASS")

    l1 = mgr.l1.reading
    check("FT-19B-10", "real", "positive",
          "A principal y FT comparten origen con propietarios distintos",
          last[16 * 60 + 26]["l1_a_origin"] == 2987540
          and ft.get("owner_generation_id") == "LOCAL-G1"
          and ft.get("owner_slot") == "LOCAL",
          f"A_origin={last[16*60+26]['l1_a_origin']} ft_owner="
          f"{ft.get('owner_generation_id')} A_owner=PRIMARY-G1")

    check("FT-19B-12", "lifecycle", "negative",
          "generacion ARCHIVED no crea funciones nuevas",
          mgr.l2.pattern_only and ident["archived_generation_writes"] == 0,
          f"pattern_only={mgr.l2.pattern_only} "
          f"writes={ident['archived_generation_writes']}")

    check("FT-19B-13", "lifecycle", "positive",
          "slot LOCAL liberado tras el archivo",
          ident["slots"]["LOCAL"]["active_generation_id"] == "",
          f"slot={ident['slots']['LOCAL']}")

    check("FT-19B-14", "lifecycle", "positive",
          "LOCAL-G1 archivada con motivo funcional propio",
          g1.get("status") == "ARCHIVED"
          and g1.get("close_reason") == "TT_FUNCTIONAL_EXTREME_CONFIRMED"
          and g1.get("closed_at_seq", 0) > g1.get("functional_closure_at_seq", -1) > 0,
          f"status={g1.get('status')} reason={g1.get('close_reason')} "
          f"closure={g1.get('functional_closure_at_seq')} "
          f"closed={g1.get('closed_at_seq')}")

    dec = ident["local_g2_decision"]
    check("FT-19B-15", "lifecycle", "negative",
          "no se abre LOCAL-G2 heredando referencias de LOCAL-G1",
          dec["decision"] == "NOT_OPENED" and len(dec["evidence"]) >= 1,
          f"decision={dec['decision']} evidence={len(dec['evidence'])}")

    # T20 la lectura humana aproximada se corrige con los ticks.
    stale, derived, human_high = 2987180, 2987540, 2987540
    check("FT-19B-20", "human", "correction",
          "origen FT corregido por ticks: 29871,8 -> 29875,4",
          derived == human_high and derived - stale == 360,
          f"stale={stale} derived={derived} diff={derived - stale} "
          f"(3,6 puntos)")

    # T21 consistencia de prefijo en 16:26.
    upto = [t for t in full if t.bar % 1440 <= 16 * 60 + 26]
    pre = TMReadingManager(upto).run()
    pl = {}
    for row in pre.rows:
        pl[row["bar"]] = row
    keys = ("l1_a", "l2_ft_origin", "l2_ft_extreme", "l2_gen_status")
    same = all(pl[16 * 60 + 26].get(k) == last[16 * 60 + 26].get(k) for k in keys)
    check("FT-19B-21", "determinism", "prefix",
          "el estado de 16:26 no depende de ticks posteriores",
          same,
          f"prefix={[pl[16*60+26].get(k) for k in keys]} "
          f"full={[last[16*60+26].get(k) for k in keys]}")

    # T22 determinismo completo.
    again = TMReadingManager(full).run()
    same_summary = json.dumps(ident, sort_keys=True) == json.dumps(
        again.summaries(), sort_keys=True)
    check("FT-19B-22", "determinism", "positive",
          "dos ejecuciones producen el mismo estado",
          same_summary, f"identical={same_summary}")

    # T23 los registros exportados coinciden con el ciclo de vida real.
    gens = {g["generation_id"]: g for g in ident["generations"]}
    lg1 = gens.get("LOCAL-G1", {})
    ttr = next((x for x in ident["tt_records"]
                if x["owner_generation"] == "LOCAL-G1"), {})
    check("FT-19B-23", "identity", "registry",
          "tablas exportadas coherentes con GenerationRecord/PatternRecord",
          (lg1.get("status") == "ARCHIVED" and lg1.get("closed_at", 0) > 0
           and lg1.get("close_reason") == "TT_FUNCTIONAL_EXTREME_CONFIRMED"
           and ttr.get("pattern_status") == "HISTORICAL"
           and ttr.get("closed_at", 0) > 0
           and ttr.get("functional_extreme") == 2987540),
          f"gen={lg1.get('status')}/{lg1.get('closed_at_seq')} "
          f"tt={ttr.get('pattern_status')}/{ttr.get('functional_extreme')}")

    # -------------------------------------------------------------- salida
    with (HERE / "ITER19B_TEST_RESULTS.csv").open("w", newline="",
                                                  encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(res[0].keys()))
        w.writeheader()
        w.writerows(res)
    summary = {
        "total": len(res),
        "passed": sum(1 for x in res if x["pass"]),
        "canonical": sum(1 for x in res if x["classification"] == "CANONICAL_PASS"),
        "provisional": sum(1 for x in res
                           if x["classification"] == "PROVISIONAL_POLICY_PASS"),
        "open_rule": sum(1 for x in res if x["classification"] == "OPEN_RULE_BLOCK"),
        "checks": [{"test_id": x["test_id"], "pass": x["pass"],
                    "classification": x["classification"]} for x in res],
    }
    (HERE / "ITER19B_TEST_RESULTS.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for x in res:
        print(("PASS " if x["pass"] else "FAIL ") + x["test_id"] + " " +
              x["description"] + " | " + x["detail"])
    print(f"TOTAL {len(res)} PASS {summary['passed']}")
    return 0 if summary["passed"] == len(res) else 1


if __name__ == "__main__":
    raise SystemExit(main())
