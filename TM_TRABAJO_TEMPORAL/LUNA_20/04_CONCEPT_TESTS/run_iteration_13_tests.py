#!/usr/bin/env python3
"""ITERACION 13 — patch v2.20: frontera de plano, prioridad gap+TT y estados heredados.

Las expectativas se derivan del patch v2.20 y del arbol v2.19, no del codigo.
Donde el arbol no fija regla, el test se marca OPEN_RULE_BLOCK y comprueba que el
motor NO inventa una resolucion.
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
    Reader, Tick, load_ticks, FEED,
)


def real(a, b):
    f = lambda h: int(h.split(":")[0]) * 60 + int(h.split(":")[1])
    lo, hi = f(a), f(b)
    return [t for t in load_ticks(FEED) if lo <= t.bar % 1440 <= hi]


def cont(ticks, prices, bar_offset=1):
    last = ticks[-1]
    b = last.bar + bar_offset
    out, seq = list(ticks), last.seq
    for i, p in enumerate(prices):
        seq += 1
        out.append(Tick(seq, (b % 1440) * 60_000 + i * 100, b, p))
    return out


def build(bars):
    ts, s = [], 1
    for bar, ps in enumerate(bars):
        for i, p in enumerate(ps):
            ts.append(Tick(s, bar * 60_000 + i * 100, bar, p))
            s += 1
    return ts


def main() -> int:
    res = []

    def check(tid, area, kind, desc, cond, detail, cls="CANONICAL_PASS"):
        res.append({"test_id": tid, "area": area, "kind": kind,
                    "classification": cls, "description": desc,
                    "pass": bool(cond), "detail": detail})

    l1 = real("16:15", "16:18")
    base = Reader(l1, reading_id="L1").run()
    obj = base.reading.tt_objective          # 2982910
    final_a = base.reading.tt_final_a        # 2985760

    # ---------------- A. TT pendiente + gap alcanza primero el objetivo TT
    a = Reader(cont(l1, [obj - 150, obj - 160]), reading_id="GA").run()
    check("GP-01", "gap+tt", "positive",
          "TT pendiente: gap que alcanza el objetivo TT lo confirma",
          a.reading.tt_status in ("TT_CONFIRMED", "TT_EXTENDED")
          and a.reading.new_one_status == "NEW_ONE_ACTIVE"
          and a.reading.n_origin == a.ticks[-2].price,
          f"tt={a.reading.tt_status} n={a.reading.new_one_status} "
          f"origin={a.reading.n_origin}")

    # Decision 2/D: doble pertenencia en el mismo tick (TT heredado + nuevo 1)
    check("GP-12", "gap+tt", "positive",
          "doble pertenencia: TT heredado confirmado + nuevo 1 desde el OPEN",
          "DOUBLE_BELONGING_TT_AND_GAP" in [e["event"] for e in a.events]
          and a.reading.prev_cycle.get("tt_objective") == a.reading.tt_objective
          and a.reading.n_origin == a.ticks[-2].price
          and a.reading.cycle_id == 1,
          f"prev_tt={a.reading.prev_cycle.get('tt_objective')} "
          f"origin={a.reading.n_origin} cycle={a.reading.cycle_id}")

    # ---------------- B. TT pendiente + gap alcanza primero el final de A
    b = Reader(cont(l1, [final_a + 100]), reading_id="GB").run()
    check("GP-02", "gap+tt", "negative",
          "TT pendiente: gap que cruza final_A antes del objetivo -> TT fallido",
          b.reading.tt_status == "TT_FAILED"
          and "TT_FAILED_FINAL_A_FIRST" in [e["event"] for e in b.events]
          and b.reading.cycle_id == 0,
          f"tt={b.reading.tt_status} cycle={b.reading.cycle_id}")

    # ---------------- C. gap que cruza ambas fronteras en un solo tick
    c = Reader(cont(l1, [final_a + 100, obj - 100]), reading_id="GC").run()
    check("GP-03", "gap+tt", "boundary",
          "un solo tick cruza ambas fronteras: gana la primera geometrica (final_A)",
          c.reading.tt_status == "TT_FAILED" and c.reading.cycle_id == 0,
          f"tt={c.reading.tt_status} cycle={c.reading.cycle_id}")

    # ---------------- D/E/F: gap con funcion heredada viva (arbol silente)
    BASE = [[10000, 9000], [9000, 9000]]
    A_CONF = [[9000, 9500, 9200, 9150]]
    B_ABS = [[9150, 9600]]
    d = Reader(build(BASE + A_CONF + B_ABS + [[9600, 9800], [10000, 9900]]),
               reading_id="GD").run()
    check("GP-04", "gap+heredado", "boundary",
          "gap durante B candidata: no se inventa resolucion de gap",
          "GAP_IMPLICIT_NEW_ONE" not in [e["event"] for e in d.events],
          f"phase={d.reading.phase} events="
          f"{[e['event'] for e in d.events][-3:]}", "OPEN_RULE_BLOCK")

    BG = BASE + [[9000, 9500, 9250, 9200, 9000]]
    e = Reader(build(BG + [[9000, 9200], [9500, 9400]]), reading_id="GE").run()
    check("GP-05", "gap+heredado", "boundary",
          "gap durante C: no se inventa resolucion administrativa",
          "GAP_IMPLICIT_NEW_ONE" not in [e["event"] for e in e.events],
          f"c={e.reading.c_status} phase={e.reading.phase}", "OPEN_RULE_BLOCK")

    f = Reader(build(BG + [[9000, 9200, 9501], [9600, 9400]]),
               reading_id="GF").run()
    check("GP-06", "gap+heredado", "boundary",
          "gap despues de CUT y antes de la base: CUT conservado, sin reset nuevo",
          f.reading.prev_cycle.get("cut_status", f.reading.cut_status) == "CUT_CONFIRMED"
          and "CYCLE_RESET_AFTER_NEW_ONE" not in [x["event"] for x in f.events],
          f"cut={f.reading.cut_status} cycle={f.reading.cycle_id}",
          "OPEN_RULE_BLOCK")

    # ---------------- G. FT del ciclo anterior continua tras un gap
    reach = cont(l1, [2984000, obj, obj - 900])
    g = Reader(cont(reach, [2982500, 2982600]), reading_id="GG").run()
    check("GP-07", "gap+ft", "positive",
          "el FT del ciclo anterior sigue activo despues del gap",
          g.reading.ft_status in ("FT_CONFIRMED", "FT_EXTENDED")
          and g.reading.ft_origin == obj - 900,
          f"ft={g.reading.ft_status} origin={g.reading.ft_origin}")

    # ---------------- H/I/J. frontera de plano (patch v2.20 A)
    def opening(gap):
        # barra 1: 10000 -> 9000 (1 bajista); barra 2 abre con gap pedido
        return build([[10000, 9000], [9000 + gap, 9000 - 100]])

    h = Reader(opening(24), reading_id="H").run().reading
    i = Reader(opening(25), reading_id="I").run().reading
    j = Reader(opening(26), reading_id="J").run().reading
    check("GP-08", "plano", "boundary", "0,24 es plano -> 2 candidata",
          h.two_status == "CANDIDATE", f"two={h.two_status}")
    check("GP-09", "plano", "boundary", "0,25 exactos no es plano -> 2 prohibido",
          i.two_status == "IMPOSSIBLE_NO_FLAT", f"two={i.two_status}")
    check("GP-10", "plano", "boundary", "0,26 no es plano -> 2 prohibido",
          j.two_status == "IMPOSSIBLE_NO_FLAT", f"two={j.two_status}")

    # ---------------- cierre causal vs rotacion administrativa
    r_hit = Reader(cont(l1, [2984000, obj]), reading_id="CL").run()
    nxt = cont(cont(l1, [2984000, obj]), [obj, obj - 100])
    r_rot = Reader(nxt, reading_id="CL2").run()
    cl = r_rot.summary()["cycle_closure"]
    check("GP-11", "ciclo", "positive",
          "cierre causal (tick TT) distinto de la rotacion (apertura siguiente)",
          cl["closed_at_tt"] != "" and cl["rotation_committed_at"] != ""
          and cl["closed_at_tt"] != cl["rotation_committed_at"]
          and cl["rotation_via"] == "TT",
          f"closure={cl}")

    # determinismo y prefijo del bloque
    x = Reader(nxt, reading_id="DET").run().trace
    y = Reader(nxt, reading_id="DET").run().trace
    check("GP-DET", "ciclo", "determinism", "doble ejecucion identica",
          x == y, f"len={len(x)}")
    pref = Reader(nxt[:len(l1) + 1], reading_id="DET").run().trace
    check("GP-PRE", "ciclo", "prefix", "prefijo consistente",
          pref == x[:len(pref)], f"prefix={len(pref)} full={len(x)}")

    with (HERE / "ITER13_TEST_RESULTS.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(res[0].keys()))
        w.writeheader()
        w.writerows(res)
    summary = {"total": len(res), "passed": sum(1 for r in res if r["pass"]),
               "canonical": sum(1 for r in res if r["classification"] == "CANONICAL_PASS"),
               "provisional": sum(1 for r in res if r["classification"] == "PROVISIONAL_POLICY_PASS"),
               "blocked": sum(1 for r in res if r["classification"] == "OPEN_RULE_BLOCK"),
               "checks": [{"test_id": r["test_id"], "pass": r["pass"],
                           "classification": r["classification"]} for r in res]}
    (HERE / "ITER13_TEST_RESULTS.json").write_text(json.dumps(summary, indent=2),
                                                   encoding="utf-8")
    for r in res:
        print(("PASS " if r["pass"] else "FAIL ") + r["test_id"] + " " +
              r["description"] + " | " + r["detail"])
    print(f"TOTAL {len(res)} PASS {summary['passed']}")
    return 0 if summary["passed"] == len(res) else 1


if __name__ == "__main__":
    raise SystemExit(main())
