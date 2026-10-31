#!/usr/bin/env python3
"""ITERACION 14 — comparacion humana TICK A TICK de los cuatro bloques.

Las expectativas se toman de v005 y de las decisiones expertas, ANTES de mirar
la salida. El motor se ejecuta en continuidad desde 16:15 para cada bloque
porque la lectura humana hereda el estado anterior.

Salidas:
  TICK_COMPARISON_ITER15.csv   (una fila por tick, estado completo)
  FIRST_DIVERGENCE_ITER15.csv  (primera divergencia causal por bloque)
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

from tm_reference_interpreter_v1_direct_aut import Reader, load_ticks, FEED  # noqa: E402

FEED_TICKS = None


def feed():
    global FEED_TICKS
    if FEED_TICKS is None:
        FEED_TICKS = load_ticks(FEED)
    return FEED_TICKS


def minute(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def span(a: str, b: str):
    lo, hi = minute(a), minute(b)
    return [t for t in feed() if lo <= t.bar % 1440 <= hi]


def last_of_bar(trace, hhmm):
    rows = [r for r in trace if r["time"].startswith(hhmm)]
    return rows[-1] if rows else None


def first_of_bar(trace, hhmm):
    rows = [r for r in trace if r["time"].startswith(hhmm)]
    return rows[0] if rows else None


def by_seq(trace, seq):
    rows = [r for r in trace if r["sequence_id"] == seq]
    return rows[0] if rows else None


# --- Expectativas humanas (v005 + decisiones expertas) -----------------------
# (anchor_id, block, kind, where, description, predicate)
ANCHORS = [
    ("A1", "B1", "first_tick_of", "16:16",
     "1 bajista 16,2 confirmado al cierre de 16:15, antes de consumir la apertura",
     lambda r: bool(r["one_kt"]) and r["one_size"] == 1620
     and r["one_kt"].startswith("16:15")),
    ("A2", "B1", "first_tick_of", "16:17",
     "modulo por descarte 28,5 conocido al cierre de 16:16",
     lambda r: r["mod_size"] == 2850
     and r["two_status"] == "IMPOSSIBLE_CLOSE"),
    ("A3", "B1", "first_tick_of", "16:18",
     "A Grande 9,1 desde 29848,5 confirmada al cierre de 16:17",
     lambda r: r["a_size"] == 910 and r["a_origin"] == 2984850
     and r["a_kt"].startswith("16:17")),
    ("A4", "B1", "bar_close", "16:18",
     "AUT bajista + TT 29829,1 pendiente (no alcanzado)",
     lambda r: r["aut_status"] == "AUT_CONFIRMED"
     and r["tt_objective"] == 2982910
     and r["tt_status"] in ("TT_PENDING", "TT_POSSIBLE")),
    ("A5", "B2", "first_tick_of", "16:20",
     "nuevo 1 local 7,5 confirmado al cierre de 16:19",
     lambda r: r["one_size"] == 750 and r["one_kt"].startswith("16:19")),
    ("A6", "B2", "bar_close", "16:20",
     "2 confirmado 12,3",
     lambda r: r["two_status"] == "CONFIRMED" and r["two_size"] == 1230),
    ("A7", "B2", "bar_close", "16:21",
     "3 confirmado; minimo 29830,3",
     lambda r: r["three_status"] == "CONFIRMED" and r["three_extreme"] == 2983030),
    ("A8", "B2", "bar_close", "16:22",
     "A 20,5 + AUT directo alcista + nuevo 1 desde 29830,3",
     lambda r: r["a_size"] == 2050
     and r["aut_direct_status"] == "AUT_DIRECT_BY_A"
     and r["n_origin"] == 2983030),
    ("A9", "B3", "seq", 1846,
     "A Grande bajista desde 29850,8 alcanza 29842,8",
     lambda r: r["price"] == 2984280
     and "/800@2985080" in r.get("l2_a", "")),
    ("A10", "B3", "seq", 1879,
     "B alcista hasta 29852,6 confirma AUT alcista (supera 29850,8)",
     lambda r: ("AUT_CONFIRMED" in r.get("l2_aut", "")
                and r.get("l2_new_one", "").startswith("NEW_ONE_ACTIVE@2984280"))),
    ("A11", "B3", "seq", 2062,
     "bajada a 29837,3 supera 29842,8 -> AUT bajista + nuevo 1 bajista",
     lambda r: (r["price"] == 2983730
                and "->2983730" in r.get("l2_new_one", "")
                and "dir=-1" in r.get("l2_new_one", ""))),
    ("A12", "B4", "bar_close", "16:24",
     "TT principal bajista 29829,1 alcanzado en 16:24 (golden v003)",
     lambda r: r["tt_status"] in ("TT_CONFIRMED", "TT_EXTENDED")
     and (r["tt_kt"] or "").startswith("16:24")),
    ("A13", "B4", "seq", 2298,
     "gap: nuevo 1 desde la apertura 29848,5",
     lambda r: r["price"] == 2984850 and r["n_origin"] == 2984850),
    ("A14", "B4", "bar_close", "16:25",
     "TT alcista confirmado dentro de la vela",
     lambda r: r["tt_status"] in ("TT_CONFIRMED", "TT_EXTENDED")),
]

BLOCKS = {"B1": ("16:15", "16:18"), "B2": ("16:19", "16:22"),
          "B3": ("16:22", "16:24"), "B4": ("16:24", "16:25")}


def classify(anchor):
    """Autoridad de la regla que la ancla ejercita."""
    aid = anchor[0]
    if aid in ("A12", "A13", "A14"):
        return "PROVISIONAL"      # gap con doble pertenencia (decision experta 2)
    if aid in ("A9", "A10", "A11"):
        return "PROVISIONAL"      # depende de autonomia del retorno/L2 local
    return "CANONICAL"


def main() -> int:
    rows, divergences = [], []
    summary = {}
    for block, (a, b) in BLOCKS.items():
        ticks = span("16:15", b) if block in ("B3", "B4") else span(a, b)
        run = Reader(ticks, reading_id=f"TICK_{block}",
                     local_probe=True).run()
        trace = run.trace
        for r in trace:
            rows.append({
                "block": block, "sequence_id": r["sequence_id"],
                "time": r["time"], "price": r["price"], "phase": r["phase"],
                "cycle_id": r.get("cycle_id", ""),
                "l2_phase": r.get("l2_phase", ""),
                "l2_module": r.get("l2_module", ""),
                "l2_A": r.get("l2_a", ""),
                "l2_B": r.get("l2_b", ""),
                "l2_AUT": r.get("l2_aut", ""),
                "l2_new_one": r.get("l2_new_one", ""),
                "one": f"{'CONFIRMED' if r['one_kt'] else ''}/{r['one_size']}",
                "two": f"{r['two_status']}/{r['two_size']}",
                "three": f"{r['three_status']}/{r['three_extreme']}",
                "module": f"{r['mod_status']}/{r['mod_size']}",
                "A": f"{r['a_status']}/{r['a_size']}@{r['a_origin']}",
                "B": f"{r['b_status']}/{r['b_grande_status']}/{r['b_size']}",
                "AUT": f"{r['aut_status']}/{r['aut_direct_status']}",
                "C": f"{r['c_status']}/CUT={r['cut_status']}",
                "TT": f"{r['tt_status']}/{r['tt_objective']}/A={r['tt_final_a']}",
                "FT": r["ft_status"],
                "new_one": f"{r['new_one_status']}@{r['n_origin']}->{r['n_extreme']}",
                "active": r["active_function"],
                "reason": r["transition_reason"],
                "events": ", ".join(e["event"] for e in r.get("events", [])),
            })
        first = None
        for anchor in ANCHORS:
            if anchor[1] != block:
                continue
            aid, _, kind, where, desc, pred = anchor
            if kind == "seq":
                r = by_seq(trace, where)
            elif kind == "first_tick_of":
                r = first_of_bar(trace, where)
            else:
                r = last_of_bar(trace, where)
            ok = bool(r) and bool(pred(r))
            if not ok and first is None:
                first = (aid, where, desc, r)
        if first:
            aid, where, desc, r = first
            divergences.append({
                "block": block, "anchor": aid, "where": where,
                "human_expected": desc,
                "python_sequence_id": (r or {}).get("sequence_id", ""),
                "python_time": (r or {}).get("time", ""),
                "python_price": (r or {}).get("price", ""),
                "python_state": (r or {}).get("events", ""),
                "authority": classify(next(x for x in ANCHORS if x[0] == aid)),
                "cause": "LOCAL_READING_NOT_IMPLEMENTED (Q-L2-BIRTH)",
            })
        summary[block] = {"ticks": len(ticks), "first_divergence": bool(first),
                          "cycle_id": run.reading.cycle_id,
                          "events": len(run.events)}

    with (HERE / "TICK_COMPARISON_ITER15.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with (HERE / "FIRST_DIVERGENCE_ITER15.csv").open("w", newline="", encoding="utf-8") as fh:
        fields = ["block", "anchor", "where", "human_expected", "python_sequence_id",
                  "python_time", "python_price", "python_state", "authority", "cause"]
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(divergences)
    (HERE / "TICK_COMPARISON_ITER15.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")

    for name, s in summary.items():
        print(f"{name}: ticks={s['ticks']} first_divergence={s['first_divergence']} "
              f"cycle={s['cycle_id']} events={s['events']}")
    for d in divergences:
        print(f"  DIV {d['block']} {d['anchor']}@{d['where']} -> "
              f"{d['python_time']} {d['python_price']} | {d['human_expected']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
