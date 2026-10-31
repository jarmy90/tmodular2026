#!/usr/bin/env python3
"""ITERACION 11 — TT como patron (v2.6 / v2.7).

El objetivo TT no se inventa: OBJETIVO_TT_100 = final_A +/- tamano_modulo,
con el signo de la direccion del nuevo 1. La confirmacion se decide por el
primer tick cronologico que toca la frontera, nunca por cierre de vela.
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


def extend(ticks, prices, bar=None, start_ms=0):
    """Anade ticks sinteticos a continuacion de la serie real."""
    last = ticks[-1]
    b = bar if bar is not None else last.bar + 1
    out = list(ticks)
    seq = last.seq
    for i, p in enumerate(prices):
        seq += 1
        out.append(Tick(seq, start_ms + i * 100, b, p))
    return out


def main() -> int:
    res = []

    def check(tid, area, kind, desc, cond, detail, cls="CANONICAL_PASS"):
        res.append({"test_id": tid, "area": area, "kind": kind,
                    "classification": cls, "description": desc,
                    "pass": bool(cond), "detail": detail})

    l1 = real("16:15", "16:18")
    base = Reader(l1, reading_id="L1").run()
    rd = base.reading
    obj = rd.tt_objective
    final_a = rd.tt_final_a

    # TT-01: el TT nace en el tick del AUT, no antes
    check("TT-01", "tt", "positive",
          "TT pendiente armado en el tick de AUT",
          rd.tt_status == "TT_PENDING" and rd.aut_status == "AUT_CONFIRMED"
          and rd.tt_aut_kt == rd.aut_kt,
          f"tt={rd.tt_status} aut={rd.aut_status}")

    ev_all = [e["event"] for e in base.events]
    aut_idx = ev_all.index("AUT_CONFIRMED")
    check("TT-02", "tt", "negative",
          "no existe TT antes de AUT",
          "TT_PENDING" not in ev_all[:aut_idx],
          f"first_tt={ev_all.index('TT_PENDING')} aut={aut_idx}")

    # TT-03: objetivo canonico del ancla 29829,1
    check("TT-03", "tt", "anchor",
          "ancla TT principal = 29829,1 = final_A - modulo",
          obj == 2982910 and final_a == 2985760 and rd.mod_size == 2850
          and obj == final_a - rd.mod_size,
          f"objetivo={obj} final_A={final_a} mod={rd.mod_size}")

    # TT-04: confirmacion en el primer tick que toca el objetivo
    hit = extend(l1, [2984500, 2983500, obj])
    r4 = Reader(hit, reading_id="L1").run()
    t4 = r4.reading
    check("TT-04", "tt", "positive",
          "TT confirmado en el primer tick que alcanza el objetivo",
          t4.tt_status in ("TT_CONFIRMED", "TT_EXTENDED")
          and t4.tt_kt == hit[-1].time_ms,
          f"status={t4.tt_status} kt={t4.tt_kt} target_tick={hit[-1].time_ms}")

    # TT-05: no se confirma al cierre, sino en el tick
    under = extend(l1, [2984000, 2983500, obj + 10])
    r5 = Reader(under, reading_id="L1").run()
    check("TT-05", "tt", "boundary",
          "un tick 0,10 antes del objetivo no confirma TT",
          r5.reading.tt_status == "TT_PENDING",
          f"status={r5.reading.tt_status} last={under[-1].price} obj={obj}")

    # TT-06: extension despues del 100 % (extremo real)
    over = extend(l1, [2984000, obj, obj - 1500, obj - 2000])
    r6 = Reader(over, reading_id="L1").run()
    t6 = r6.reading
    ev6 = [e["event"] for e in r6.events]
    check("TT-06", "tt", "positive",
          "TT extendido conserva el extremo real mas alla del 100 %",
          t6.tt_status == "TT_EXTENDED" and t6.tt_extreme == obj - 2000
          and "TT_EXTENDED" in ev6,
          f"status={t6.tt_status} extreme={t6.tt_extreme}")

    # TT-07: TT fallido si final_A se toca primero
    back = extend(l1, [2984000, final_a + 100, final_a])
    r7 = Reader(back, reading_id="L1").run()
    ev7 = [e["event"] for e in r7.events]
    check("TT-07", "tt", "negative",
          "TT fallido al tocar final_A antes del objetivo",
          r7.reading.tt_status == "TT_FAILED"
          and "TT_FAILED_FINAL_A_FIRST" in ev7,
          f"status={r7.reading.tt_status}")

    # TT-08: salto unico directo al objetivo. El cruce doble final_A/objetivo
    # es geometricamente imposible desde el lado del TT, porque el objetivo
    # esta siempre mas alla de final_A en la direccion del TT (obj = final_A
    # +/- modulo). v2.7 E solo aplica si el precio viniera del otro lado, y
    # ese lado ya habria fallado el TT en el tick de cruce.
    jump = extend(l1, [2984000, obj - 2000])
    r8 = Reader(jump, reading_id="L1").run()
    check("TT-08", "tt", "boundary",
          "salto unico directo al objetivo confirma TT (cruce doble imposible)",
          r8.reading.tt_status in ("TT_CONFIRMED", "TT_EXTENDED")
          and r8.reading.tt_kt == jump[-1].time_ms,
          f"status={r8.reading.tt_status} last={jump[-1].price}")

    # TT-09: TT no depende del tamano de B
    check("TT-09", "tt", "negative",
          "el objetivo TT usa modulo y final_A, no el tamano de B",
          obj == final_a - rd.mod_size and rd.b_size != rd.mod_size,
          f"obj={obj} final_A={final_a} mod={rd.mod_size} b={rd.b_size}")

    # TT-10: TT no retira autoridad al nuevo 1
    r10 = Reader(extend(l1, [2984000, obj]), reading_id="L1").run()
    check("TT-10", "tt", "positive",
          "tras confirmar TT el nuevo 1 sigue siendo la funcion activa",
          r10.reading.active_function == "NEW_ONE"
          and r10.reading.new_one_status == "NEW_ONE_ACTIVE",
          f"active={r10.reading.active_function} one={r10.reading.new_one_status}")

    # TT-11: determinismo y prefijo
    r11a = Reader(extend(l1, [2984000, 2983500, obj]), reading_id="L1").run()
    r11b = Reader(extend(l1, [2984000, 2983500, obj]), reading_id="L1").run()
    check("TT-11", "tt", "determinism",
          "doble ejecucion identica con TT",
          [e["event"] for e in r11a.events] == [e["event"] for e in r11b.events],
          "identical")

    full = extend(l1, [2984000, 2983500, obj])
    k = len(l1) + 1
    pre = Reader(full[:k], reading_id="L1").run()
    check("TT-12", "tt", "prefix",
          "prefijo sin spoiler: el estado del prefijo no conoce el objetivo",
          pre.reading.tt_status == "TT_PENDING"
          and pre.reading.tt_kt == 0,
          f"prefix_tt={pre.reading.tt_status}")

    # salida
    outdir = HERE.parent / "04_CONCEPT_TESTS"
    with open(outdir / "TT_TEST_RESULTS.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(res[0].keys()))
        w.writeheader()
        w.writerows(res)
    checks = [{"test_id": r["test_id"], "pass": r["pass"],
               "classification": r["classification"]} for r in res]
    (outdir / "TT_TEST_RESULTS.json").write_text(
        json.dumps({"total": len(res),
                    "passed": sum(1 for r in res if r["pass"]),
                    "checks": checks}, indent=2), encoding="utf-8")

    for r in res:
        print(("PASS " if r["pass"] else "FAIL ") + r["test_id"] + " " +
              r["description"] + " | " + r["detail"])
    print(f"TOTAL {len(res)} PASS {sum(1 for r in res if r['pass'])}")
    return 0 if all(r["pass"] for r in res) else 1


if __name__ == "__main__":
    raise SystemExit(main())
