#!/usr/bin/env python3
"""Iteracion 21 — diagnostico del tramo abierto 16:25-16:32.

No modifica nada: imprime la evidencia fisica (OHLC por vela), los eventos
causales de cada lectura y el primer punto donde el motor y la lectura humana
dejan de coincidir, con la clasificacion del trazador.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "05_REFERENCE_ENGINE"))

from tm_reference_interpreter_v1_direct_aut import load_ticks, FEED  # noqa: E402
from tm_reading_manager import TMReadingManager  # noqa: E402


def hhmm(bar: int) -> str:
    return f"{bar % 1440 // 60:02d}:{bar % 1440 % 60:02d}"


def main() -> int:
    ticks = [t for t in load_ticks(FEED)
             if 16 * 60 + 15 <= t.bar % 1440 <= 16 * 60 + 35]
    mgr = TMReadingManager(ticks).run()

    print("== OHLC fisico por vela (unidades x100)")
    print("vela    open     high     low      close    rango")
    bars = {}
    for t in ticks:
        b = bars.setdefault(t.bar, {"o": t.price, "h": t.price, "l": t.price,
                                    "c": t.price})
        b["h"] = max(b["h"], t.price)
        b["l"] = min(b["l"], t.price)
        b["c"] = t.price
    for bar in sorted(bars):
        if bar % 1440 < 16 * 60 + 25:
            continue
        b = bars[bar]
        print(f"{hhmm(bar)}  {b['o']:8d} {b['h']:8d} {b['l']:8d} {b['c']:8d} "
              f"{b['h'] - b['l']:6d}")

    print("\n== eventos L1 (16:26 en adelante)")
    for e in mgr.l1.events:
        bar = e.get("bar")
        if bar is None or bar % 1440 < 16 * 60 + 26:
            continue
        print(f"{hhmm(bar)} seq={e.get('seq'):5d} {e.get('event')}: "
              f"{e.get('detail', '')[:110]}")

    print("\n== eventos L2 (16:26 en adelante)")
    if mgr.l2 is not None:
        for e in mgr.l2.events:
            bar = e.get("bar")
            if bar is None or bar % 1440 < 16 * 60 + 26:
                continue
            print(f"{hhmm(bar)} seq={e.get('seq'):5d} {e.get('event')}: "
                  f"{e.get('detail', '')[:110]}")

    print("\n== estado declarado al cierre de cada vela (L1 / L2)")
    last = {}
    for row in mgr.rows:
        last[row["bar"]] = row
    for bar in sorted(last):
        if bar % 1440 < 16 * 60 + 26:
            continue
        r = last[bar]
        print(f"{hhmm(bar)} L1 {r.get('l1_phase')} mod={r.get('l1_mod')}"
              f" a={r.get('l1_a_status')}/{r.get('l1_a_size')}"
              f" b={r.get('l1_b_status')}/{r.get('l1_b_size')}"
              f" c={r.get('l1_b')}"
              f" tt={r.get('l1_tt')}/{r.get('l1_tt_objective')}"
              f" n={r.get('l1_n_origin')}->{r.get('l1_n_extreme')}"
              f" | L2 {r.get('l2')}/{r.get('l2_phase')}"
              f" mod={r.get('l2_mod')} tt={r.get('l2_tt')}")

    print("\n== trazador: primera fila con decision estructural por vela")
    seen = set()
    for row in mgr.l1.decision_trace.rows:
        text = row["decision"]
        if text == "OBSERVE":
            continue
        bar = row["timestamp"] // 60000
        key = (bar, text)
        if key in seen or bar % 1440 < 16 * 60 + 26:
            continue
        seen.add(key)
        print(f"{hhmm(bar)} seq={row['sequence_id']:5d} {text}"
              f" | q={(row['current_question'] or '').split('-')[-1]}"
              f" | tt={row['confirmed_node_after'].get('tt')}")

    s = mgr.summaries()
    print("\n== TT owners")
    for o in s.get("tt_owners", []):
        print(o)
    print("\n== resumen de metricas de arquitectura")
    print(mgr.l1.arch.metrics())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
