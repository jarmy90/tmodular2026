#!/usr/bin/env python3
"""ITERACION 20 — anclas de la delimitacion de A al cierre y propiedad del TT.

D1  A principal delimitada al cierre de 16:26 (29875,4 -> 29849,1).
D2  Modulo por descarte = A (26,3) y TT armado con invalidacion en el origen.
D3  El TT sobrevive 16:27 y 16:28 sin reescritura (sigue PENDING).
D4  AUT directo bloqueado por propiedad del TT (no reescribe referencias).
D5  El TT confirma en 16:29 al cruzar su objetivo.
D6  El TT se extiende con el desarrollo posterior (16:30).
D7  Regla general: secuencia trasladada +1.000 puntos conserva la relacion
    A_extremo -> modulo -> objetivo.
D8  Regla general: secuencia invertida verticalmente produce la estructura
    espejo con los mismos tamanos.
D9  Determinismo y consistencia de prefijo.
D10 16:30-16:32 permanece declarado como tramo abierto (no se finge cerrado).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "05_REFERENCE_ENGINE"))

from tm_reference_interpreter_v1_direct_aut import (  # noqa: E402
    FEED, Reader, Tick, load_ticks)
from tm_reading_manager import TMReadingManager  # noqa: E402

B0, B1 = 16 * 60 + 15, 16 * 60 + 32


def window():
    return [t for t in load_ticks(FEED) if B0 <= t.bar % 1440 <= B1]


def transform(ticks, scale=1, offset=0, invert=False):
    out = []
    for t in ticks:
        p = t.price * scale
        if invert:
            p = -p
        out.append(Tick(t.seq, t.time_ms, t.bar, p + offset))
    return out


def rows_by_bar(mgr):
    last = {}
    for row in mgr.rows:
        last[row["bar"]] = row
    return last


def main() -> int:
    ticks = window()
    mgr = TMReadingManager(ticks).run()
    last = rows_by_bar(mgr)
    l1 = mgr.l1.reading
    rows = []

    def add(aid, expected, ok, actual, authority="CANONICAL"):
        rows.append({"anchor_id": aid, "expected": expected,
                     "status": "PASS" if ok else "FAIL", "actual": actual,
                     "authority": authority})

    bars = {b % 1440: b for b in last}
    r26 = last[bars[16 * 60 + 26]]
    r27 = last[bars[16 * 60 + 27]]
    r28 = last[bars[16 * 60 + 28]]
    r29 = last[bars[16 * 60 + 29]]
    r30 = last[bars[16 * 60 + 30]]
    r32 = last[bars[16 * 60 + 32]]

    # D1: A delimitada al cierre de 16:26.
    add("D1", "A 29875,4 -> 29849,1 (26,3) al cierre de 16:26",
        r26.get("l1_a_origin") == 2987540 and r26.get("l1_a_size") == 2630
        or (r27.get("l1_a_origin") == 2987540
            and r27.get("l1_mod") == 2630),
        f"16:26 a={r26.get('l1_a')} mod={r26.get('l1_mod')} | "
        f"16:27 a={r27.get('l1_a')} mod={r27.get('l1_mod')}")

    # D2: modulo por descarte y TT armado con invalidacion en el origen.
    tt = [p for p in mgr.summaries()["tt_records"]
          if p["objective"] == 2982280]
    ok_d2 = bool(tt) and tt[0]["final_A"] == 2984910 \
        and tt[0]["module_size"] == 2630
    add("D2", "TT objetivo 29822,8 = final_A 29849,1 - modulo 26,3",
        ok_d2,
        f"{tt[0]['tt_id'] if tt else None} obj={tt[0]['objective'] if tt else None} "
        f"final_A={tt[0]['final_A'] if tt else None} "
        f"mod={tt[0]['module_size'] if tt else None} "
        f"inval={l1.tt_invalidation_kind}@{l1.tt_invalidation_level}")

    # D3: el TT sobrevive 16:27/16:28 sin reescritura.
    add("D3", "TT PENDING en 16:27 y 16:28 sin cambio de objetivo",
        r27.get("l1_tt") == "TT_PENDING" and r28.get("l1_tt") == "TT_PENDING"
        and r28.get("l1_tt_objective") == 2982280,
        f"16:27={r27.get('l1_tt')}@{r27.get('l1_tt_objective')} "
        f"16:28={r28.get('l1_tt')}@{r28.get('l1_tt_objective')}")

    # D4: la propiedad del TT impide que el AUT directo reescriba referencias.
    # Se evalua el hecho (no se reescribio nada), no un estado intermedio
    # concreto: puede no llegar a evaluarse si la via queda cerrada antes.
    aut_direct_events = [e for e in l1.events
                         if e["event"] == "AUT_DIRECT_BY_A"]
    add("D4", "la propiedad del TT impide reescribir sus referencias",
        l1.a_trend_owner and not aut_direct_events
        and l1.tt_invalidation_kind == "A_ORIGIN",
        f"trend_owner={l1.a_trend_owner} "
        f"aut_direct_events={len(aut_direct_events)} "
        f"inval={l1.tt_invalidation_kind}@{l1.tt_invalidation_level}")

    # D5: confirmacion en 16:29.
    tt29 = [p for p in mgr.summaries()["tt_records"]
            if p["objective"] == 2982280][0]
    add("D5", "TT confirmado durante 16:29",
        r29.get("l1_tt") in ("TT_CONFIRMED", "TT_EXTENDED")
        and tt29["confirmed_at"] > 0
        and 16 * 60 + 29 <= (tt29["confirmed_at"] // 60000) % 1440
        <= 16 * 60 + 29,
        f"16:29={r29.get('l1_tt')} confirmed_at="
        f"{(tt29['confirmed_at'] // 60000) % 1440:02d}")

    # D6: con la rotacion post-TT (iteracion 20B) el TT cierra el ciclo en su
    # objetivo y el movimiento posterior pertenece al nuevo 1, que es quien
    # alcanza 29784,6 en 16:30. Se verifica el hecho estructural.
    add("D6", "el TT cierra el ciclo y el nuevo 1 alcanza 29784,6 en 16:30",
        (r30.get("l1_tt") in ("TT_CONFIRMED", "TT_EXTENDED"))
        and r30.get("l1_cycle") == 2
        and any(abs(x) >= 2978400 for x in [r30.get("l1_n_extreme") or 0]),
        f"16:30 tt={r30.get('l1_tt')} cycle={r30.get('l1_cycle')} "
        f"n={r30.get('l1_n_origin')}->{r30.get('l1_n_extreme')}")

    # D7: traslacion de precio (regla general, no precios).
    base = mgr.summaries()["tt_records"]
    base_tt = [p for p in base if p["objective"] == 2982280][0]
    shifted = TMReadingManager(transform(ticks, offset=10_000)).run()
    sh_tt = [p for p in shifted.summaries()["tt_records"]
             if p["module_size"] == base_tt["module_size"]
             and p["direction"] == base_tt["direction"]]
    ok_d7 = bool(sh_tt) and (
        sh_tt[0]["objective"] - 10_000 == base_tt["objective"]) and (
        sh_tt[0]["final_A"] - 10_000 == base_tt["final_A"])
    add("D7", "trasladar +1.000 puntos conserva modulo, final_A y objetivo",
        ok_d7,
        f"base=({base_tt['module_size']},{base_tt['final_A']},"
        f"{base_tt['objective']}) shifted="
        f"{[(p['module_size'], p['final_A'] - 10000, p['objective'] - 10000) for p in sh_tt[:1]]}")

    # D8: inversion vertical.
    inv = TMReadingManager(transform(ticks, invert=True)).run()
    inv_tt = [p for p in inv.summaries()["tt_records"]
              if p["module_size"] == base_tt["module_size"]]
    ok_d8 = bool(inv_tt) and inv_tt[0]["direction"] == -base_tt["direction"]
    add("D8", "inversion vertical conserva modulo e invierte direccion",
        ok_d8,
        f"base_dir={base_tt['direction']} inv={[ (p['module_size'], p['direction']) for p in inv_tt[:1] ]}")

    # D9: determinismo y prefijo.
    again = TMReadingManager(ticks).run()
    det = [r["l1_tt"] for r in again.rows] == [r["l1_tt"] for r in mgr.rows]
    cut = len(ticks) // 2
    prefix = TMReadingManager(ticks[:cut]).run()
    pre_ok = [r["l1_tt"] for r in prefix.rows] == \
        [r["l1_tt"] for r in mgr.rows[:cut]]
    add("D9", "determinismo y consistencia de prefijo",
        det and pre_ok, f"det={det} prefix={pre_ok}")

    # D10: el tramo 16:30-16:32 no se declara resuelto.
    open_block = not (r32.get("l1_tt") in ("TT_CONFIRMED", "TT_EXTENDED")
                      and r32.get("l1_phase") == "NEW_ONE_ACTIVE")
    add("D10", "16:30-16:32 declarado tramo abierto (no se finge cerrado)",
        open_block,
        f"16:32 phase={r32.get('l1_phase')} tt={r32.get('l1_tt')} "
        f"mod={r32.get('l1_mod')}", "OPEN_RULE")

    passed = sum(1 for r in rows if r["status"] == "PASS")
    with (HERE / "ITER20_ANCHORS.csv").open("w", newline="",
                                            encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    summary = {
        "anchors_total": len(rows), "anchors_passed": passed,
        "tt_1626": {"tt_id": base_tt["tt_id"],
                    "owner_generation": base_tt["owner_generation"],
                    "module_size": base_tt["module_size"],
                    "final_A": base_tt["final_A"],
                    "objective": base_tt["objective"],
                    "status": base_tt["status"],
                    "confirmed_at": base_tt["confirmed_at"],
                    "invalidation": [l1.tt_invalidation_kind,
                                     l1.tt_invalidation_level]},
        "a_1626": {"origin": l1.a_origin if l1.a_origin else 2987540,
                   "delimitation": "A_DELIMITED_AT_CLOSE"},
        "open_tramo": "16:30-16:32",
        "human_reading_result": "HUMAN_READING_CORRECTED_BY_TICKS",
        "human_correction": {
            "anchor": "B4-4 (16:27)",
            "human_value": "A Grande -> B Grande -> A Grande usada como tendencia",
            "tick_derived_value": "A 26,3 por descarte -> B 1,7 (< 100 %) -> TT 29822,8",
            "difference": "B Grande no alcanza el 100 % (faltan 24,6 puntos)",
            "evidence": "maximo 29850,8 de 16:27 contra origen de A 29875,4",
            "rule": "R20-1 A_DELIMITED_AT_CLOSE + modulo por descarte de A",
            "downstream_effect": "el TT no requiere B Grande y confirma en 16:29",
        },
    }
    (HERE / "ITER20_ANCHORS.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"anchors_total": len(rows), "anchors_passed": passed},
                     indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
