#!/usr/bin/env python3
"""ITERACION 12 — reinicio del ciclo tras TT, cadena CUT -> tendencia y FT.

Clasificacion:
  CANONICAL_PASS            decision experta cerrada (iteracion 12, puntos 1-3)
  PROVISIONAL_POLICY_PASS   depende de la autonomia provisional (retorno / FT)
  OPEN_RULE_BLOCK           sin regla cerrada
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


def bar_of(h: str) -> int:
    hh, mm = h.split(":")
    return int(hh) * 60 + int(mm)


def real(a: str, b: str):
    lo, hi = bar_of(a), bar_of(b)
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
    obj = base.reading.tt_objective          # 2982910 = 29829,1
    n_origin = base.reading.n_origin         # 2985760
    tt_ext_at_close = base.reading.tt_extreme

    # ---------------- reinicio del ciclo tras TT
    reach = cont(l1, [2984000, obj])
    r_hit = Reader(reach, reading_id="L1").run()
    check("CR-01", "cycle", "positive", "TT confirmado en el tick del objetivo",
          r_hit.reading.tt_status in ("TT_CONFIRMED", "TT_EXTENDED")
          and r_hit.reading.tt_kt == reach[-1].time_ms
          and r_hit.reading.cycle_id == 0,
          f"tt={r_hit.reading.tt_status} kt={r_hit.reading.tt_kt} "
          f"cycle={r_hit.reading.cycle_id}")

    nxt = cont(reach, [obj, obj - 100])
    r_next = Reader(nxt, reading_id="L1").run()
    d = r_next.reading
    # TT extendido dentro de su propia vela (extremo real != nivel 100 %)
    ext = cont(l1, [2984000, obj, obj - 900])
    r_ext = Reader(ext, reading_id="TTX").run()
    up = cont(ext, [2982300, 2982500])
    r_up = Reader(up, reading_id="FT").run()
    check("CR-02", "cycle", "positive",
          "la vela siguiente reinicia el ciclo y abre 2 candidata",
          d.cycle_id == 1 and d.one_origin == n_origin
          and d.one_extreme == obj and d.two_status == "CANDIDATE",
          f"cycle={d.cycle_id} one={d.one_origin}->{d.one_extreme} "
          f"two={d.two_status}")

    check("CR-03", "cycle", "positive",
          "el reinicio conserva la trazabilidad del TT anterior",
          d.prev_cycle.get("tt_objective") == obj
          and d.prev_cycle.get("tt_extreme") == r_hit.reading.tt_extreme
          and d.tt_objective == obj
          and d.tt_status in ("TT_CONFIRMED", "TT_EXTENDED"),
          f"prev_tt={d.prev_cycle.get('tt_objective')}/"
          f"{d.prev_cycle.get('tt_extreme')} "
          f"tt={d.tt_objective}/{d.tt_extreme}/{d.tt_status}")

    ev_names = [e["event"] for e in r_next.events]
    reset_i = ev_names.index("CYCLE_RESET_AFTER_NEW_ONE")
    two_after = [i for i, e in enumerate(ev_names)
                 if e == "TWO_CANDIDATE" and i > reset_i]
    check("CR-04", "cycle", "negative",
          "el nuevo 1 no abre 2 dentro de su propia vela",
          len(two_after) == 1,
          f"reset={reset_i} two_after={two_after}")

    before = Reader(cont(l1, [2984000, obj + 100]), reading_id="L1").run()
    check("CR-05", "cycle", "negative",
          "sin TT al 100 % no hay reinicio de ciclo",
          before.reading.cycle_id == 0
          and before.reading.tt_status == "TT_PENDING"
          and "CYCLE_RESET_AFTER_NEW_ONE" not in
          [e["event"] for e in before.events],
          f"cycle={before.reading.cycle_id} tt={before.reading.tt_status}")

    gap_next = cont(reach, [obj - 500])
    r_gap = Reader(gap_next, reading_id="L1").run()
    check("CR-06", "cycle", "boundary",
          "gap en la vela siguiente: 2 prohibido y rama de gap",
          r_gap.reading.two_status == "IMPOSSIBLE_NO_FLAT"
          and "GAP_IMPLICIT_NEW_ONE" in [e["event"] for e in r_gap.events],
          f"two={r_gap.reading.two_status}")

    # reinicio generico (nuevo 1 por C-trend, sin TT)
    BASE = [[10000, 9000], [9000, 9000]]
    BG = BASE + [[9000, 9500, 9250, 9200, 9000]]
    r_tr = Reader(build(BG + [[9000, 9200, 10001], [10001, 10200]]),
                  reading_id="CR_TREND").run()
    check("CR-07", "cycle", "positive",
          "reinicio tambien tras el nuevo 1 nacido de C-tendencia",
          r_tr.reading.prev_cycle.get("tt_objective") == 0
          and r_tr.reading.prev_cycle.get("c_extreme") == 10001
          and r_tr.reading.two_status == "CANDIDATE",
          f"prev_c={r_tr.reading.prev_cycle.get('c_extreme')} "
          f"two={r_tr.reading.two_status}")

    # ---------------- cadena CUT -> C tendencia -> nuevo 1
    r_cut = Reader(build(BG + [[9000, 9200, 9501]], ), reading_id="CUT1").run()
    r_chain = Reader(build(BG + [[9000, 9200, 9501, 10001]]),
                     reading_id="CUT2").run()
    ev = [e["event"] for e in r_chain.events]
    check("CUT-CHAIN-01", "cut", "positive",
          "CUT confirmado sin crear nuevo 1",
          r_cut.reading.cut_status == "CUT_CONFIRMED"
          and r_cut.reading.new_one_status == ""
          and r_cut.reading.active_function == "C",
          f"cut={r_cut.reading.cut_status} n={r_cut.reading.new_one_status!r}")
    check("CUT-CHAIN-02", "cut", "positive",
          "CUT precede a C usada como tendencia y al nuevo 1",
          "CUT_CONFIRMED" in ev and "C_USED_AS_TREND" in ev
          and ev.index("CUT_CONFIRMED") < ev.index("C_USED_AS_TREND"),
          f"order={[e for e in ev if e in ('CUT_CONFIRMED', 'C_USED_AS_TREND')]}")
    check("CUT-CHAIN-03", "cut", "boundary",
          "final real de A y base del modulo son referencias distintas",
          r_chain.reading.prev_cycle.get("a_extreme", r_chain.reading.a_extreme) != 10000
          and r_chain.reading.a_extreme == 9500,
          f"a_extreme={r_chain.reading.a_extreme} base=10000")

    # ---------------- FT estructural
    f = r_up.reading
    check("FT-01", "ft", "negative", "antes del 100 % de TT no existe FT",
          before.reading.ft_status == "", f"ft={before.reading.ft_status!r}")
    check("FT-02", "ft", "positive",
          "FT se origina en el extremo REAL del TT, no en el nivel 100 %",
          f.ft_origin == f.ft_tt_extreme and f.ft_origin == obj - 900
          and f.ft_origin != f.tt_objective,
          f"origin={f.ft_origin} tt_ext={f.ft_tt_extreme} obj={f.tt_objective}")
    check("FT-03", "ft", "positive",
          "FT se confirma estructuralmente con extremo propio (tick exacto PROVISIONAL)",
          f.ft_status in ("FT_CONFIRMED", "FT_EXTENDED") and f.ft_kt > 0
          and f.ft_size >= 200,
          f"ft={f.ft_status} kt={f.ft_kt} size={f.ft_size}",
          "PROVISIONAL_POLICY_PASS")
    check("FT-04", "ft", "positive",
          "FT convive con el ciclo nuevo sin consumir su autoridad",
          f.cycle_id >= 1 and f.ft_status in ("FT_CONFIRMED", "FT_EXTENDED")
          and f.active_function != "FT",
          f"cycle={f.cycle_id} two={f.two_status} active={f.active_function} "
          f"ft={f.ft_status}")
    check("FT-05", "ft", "negative",
          "FT es patron: no aparece como funcion activa",
          "FT" not in (f.active_function, r_up.reading.new_one_status)
          and f.ft_status != "",
          f"active={f.active_function} n={f.new_one_status}")
    check("FT-06", "ft", "boundary",
          "un retroceso menor que el filtro de ruido no confirma FT (filtro 2 pts PROVISIONAL)",
          Reader(cont(ext, [2982200]), reading_id="FT2").run().reading.ft_status
          == "FT_POSSIBLE",
          f"ft={Reader(cont(ext, [2982200]), reading_id='FT2').run().reading.ft_status}",
          "PROVISIONAL_POLICY_PASS")

    # ---------------- determinismo / prefijo
    a = Reader(nxt, reading_id="DET").run().trace
    b = Reader(nxt, reading_id="DET").run().trace
    check("CR-DET", "cycle", "determinism", "doble ejecucion identica",
          a == b, f"len={len(a)}")
    full = Reader(nxt, reading_id="PRE").run().trace
    pref = Reader(nxt[:len(l1) + 2], reading_id="PRE").run().trace
    check("CR-PRE", "cycle", "prefix",
          "prefijo sin spoiler (estado previo no conoce el objetivo)",
          pref == full[:len(pref)] and
          Reader(nxt[:len(l1) + 2], reading_id="PRE").run().reading.cycle_id == 0,
          f"prefix={len(pref)} full={len(full)}")

    out = HERE
    with (out / "ITER12_TEST_RESULTS.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(res[0].keys()))
        w.writeheader()
        w.writerows(res)
    summary = {
        "total": len(res),
        "passed": sum(1 for r in res if r["pass"]),
        "canonical": sum(1 for r in res if r["classification"] == "CANONICAL_PASS"),
        "provisional": sum(1 for r in res if r["classification"] == "PROVISIONAL_POLICY_PASS"),
        "blocked": sum(1 for r in res if r["classification"] == "OPEN_RULE_BLOCK"),
        "checks": [{"test_id": r["test_id"], "pass": r["pass"],
                    "classification": r["classification"]} for r in res],
    }
    (out / "ITER12_TEST_RESULTS.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")

    for r in res:
        print(("PASS " if r["pass"] else "FAIL ") + r["test_id"] + " " +
              r["description"] + " | " + r["detail"])
    print(f"TOTAL {len(res)} PASS {summary['passed']}")
    return 0 if summary["passed"] == len(res) else 1


if __name__ == "__main__":
    raise SystemExit(main())
