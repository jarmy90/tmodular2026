#!/usr/bin/env python3
"""ITERACION 13 — comparacion humana bloque a bloque (v005).

Expectativas copiadas de v005 ANTES de mirar la salida. No se ajusta nada.
B3 y B4 se leen tambien en continuidad desde 16:15 porque la lectura humana
hereda el estado del bloque anterior.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))

from tm_reference_interpreter_v1_direct_aut import (  # noqa: E402
    Reader, load_ticks, FEED,
)

_FEED_CACHE = None


def feed():
    global _FEED_CACHE
    if _FEED_CACHE is None:
        _FEED_CACHE = load_ticks(FEED)
    return _FEED_CACHE


def real(a, b):
    f = lambda h: int(h.split(":")[0]) * 60 + int(h.split(":")[1])
    lo, hi = f(a), f(b)
    return [t for t in feed() if lo <= t.bar % 1440 <= hi]


HUMAN = {
    "B1": [("16:15", "1 bajista 16,2"), ("16:16", "modulo por descarte; modulo conjunto 28,5"),
           ("16:17", "A Grande 9,1 desde 29848,5"), ("16:18", "AUT bajista; TT 29829,1 pendiente")],
    "B2": [("16:19", "nuevo 1 local 7,5"), ("16:20", "2 confirmado 12,3"),
           ("16:21", "3 confirmado; minimo 29830,3"),
           ("16:22", "A 20,5 + AUT directo alcista + nuevo 1")],
    "B3": [("16:23", "A bajista 29850,8->29842,8; B a 29852,6 -> AUT alcista; AUT bajista"),
           ("16:24", "A -> B -> AUT en la vela; TT alcista NO alcanzado")],
    "B4": [("16:24", "cierre 29834,5; TT alcista pendiente"),
           ("16:25", "gap +14,0 -> nuevo 1 desde 29848,5; TT alcista en la vela")],
}
BLOCKS = {"B1": ("16:15", "16:18"), "B2": ("16:19", "16:22"),
          "B3": ("16:22", "16:24"), "B4": ("16:24", "16:25")}


def rows_at_bar(trace, bar_prefix):
    rows = [r for r in trace if r["time"].startswith(bar_prefix)]
    return rows[-1] if rows else {}


def label(r):
    if not r:
        return ""
    return (f"1={r['one_size']} 2={r['two_status']}/{r['two_size']} "
            f"3={r['three_status']}/{r['three_extreme']} "
            f"mod={r['mod_status']}/{r['mod_size']} A={r['a_status']}/{r['a_size']} "
            f"B={r['b_status']}/{r['b_grande_status']} "
            f"AUT={r['aut_status']}/{r['aut_direct_status']} "
            f"C={r['c_status']}/CUT={r['cut_status']} TT={r['tt_status']} "
            f"FT={r['ft_status']} "
            f"n={r['new_one_status']}@{r['n_origin']} act={r['active_function']}")


def main() -> int:
    out_rows, summary = [], {}
    for name, (a, b) in BLOCKS.items():
        continuous = real("16:15", b) if name in ("B3", "B4") else real(a, b)
        run = Reader(continuous, reading_id="BLK").run()
        trace = run.trace
        for bar_label, expected in HUMAN[name]:
            r = rows_at_bar(trace, bar_label)
            out_rows.append({"block": name, "bar": bar_label,
                             "human_expected": expected,
                             "python_state": label(r),
                             "bar_close_phase": r.get("phase", ""),
                             "events_at_last_tick": ", ".join(
                                 e["event"] for e in r.get("events", [])),
                             "rules": "v2.13/v2.19/v2.20"})
        summary[name] = {"ticks": len(continuous), "events": len(run.events),
                         "rotation": run.reading.cycle_id}
    with (HERE / "HUMAN_BLOCK_COMPARISON.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    (HERE / "HUMAN_BLOCK_COMPARISON.json").write_text(json.dumps(summary, indent=2),
                                                     encoding="utf-8")
    for r in out_rows:
        print(f"{r['block']} {r['bar']} | {r['human_expected']} | {r['python_state']} "
              f"| ev={r['events_at_last_tick']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
