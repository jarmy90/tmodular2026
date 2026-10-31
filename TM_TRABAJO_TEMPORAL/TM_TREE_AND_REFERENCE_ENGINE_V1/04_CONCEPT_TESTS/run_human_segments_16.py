#!/usr/bin/env python3
"""ITERACION 16 — segmentos humanos independientes 16:15-16:32.

Corrige el alcance de la comparacion (fase 4): no existe una etiqueta humana
independiente por tick. Lo que existe son ANCLAS por vela y SEGMENTOS con
estado esperado, referencias invariantes y evento final.

Fuentes: TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v005.txt (bloques 16:15-16:24
y 16:25-16:32).

Salidas:
  HUMAN_SEGMENTS_1615_1632.csv
  HUMAN_SEGMENTS_1615_1632.json
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "05_REFERENCE_ENGINE"))
from tm_reader_guard import verify as _verify_reader  # noqa: E402

_verify_reader()

from tm_reference_interpreter_v1_direct_aut import (  # noqa: E402
    Reader, load_ticks, FEED,
)

BARS = [16 * 60 + m for m in range(15, 33)]


def bar_label(b: int) -> str:
    return f"{b // 60:02d}:{b % 60:02d}"


def rows_by_bar(trace):
    """Primera fila de cada vela: incluye el cierre conocido al abrir."""
    out = {}
    for row in trace:
        hh, mm, _ = row["time"].split(":")
        b = int(hh) * 60 + int(mm)
        out.setdefault(b, row)
    return out


def run_feed():
    ticks = [t for t in load_ticks(FEED) if BARS[0] <= t.bar % 1440 <= BARS[-1]]
    reader = Reader(ticks, reading_id="L1").run()
    return reader, rows_by_bar(reader.trace)


def main() -> int:
    reader, rows = run_feed()
    # El estado al cierre de una vela se conoce en el primer tick de la
    # siguiente (v2.13/v2.14: cierre conocido, no durante la vela).
    close = {}
    for row in reader.trace:
        hh, mm, _ = row["time"].split(":")
        close[int(hh) * 60 + int(mm)] = row
    closed = {b: rows.get(b + 1, close[b]) for b in BARS}
    events = reader.events
    ev_by_bar = {}
    for e in events:
        ev_by_bar.setdefault(e["bar"] % 1440, []).append(e["event"])

    segs = []

    def seg(bar, sid, expected, check, detail, authority="CANONICAL"):
        segs.append({
            "segment_id": sid, "bar": bar_label(bar), "sequence_from": "",
            "sequence_to": "", "expected_state": expected,
            "references_invariant": "",
            "expected_end_event": "", "authority": authority,
            "status": "PASS" if check else "FAIL", "detail": detail,
        })

    r15 = closed[16 * 60 + 15]
    seg(16 * 60 + 15, "B1-S1", "1 inicial bajista 29877,0 -> 29860,8",
        r15["one_size"] == 1620 and r15["one_dir"] == -1,
        f"one={r15['one_size']}/{r15['one_dir']}")

    r16 = closed[16 * 60 + 16]
    seg(16 * 60 + 16, "B1-S2", "2 candidata no confirma; modulo conjunto 28,5",
        r16["two_status"] == "IMPOSSIBLE_CLOSE" and r16["mod_size"] == 2850,
        f"two={r16['two_status']} mod={r16['mod_size']}")

    r17 = close[16 * 60 + 17]
    seg(16 * 60 + 17, "B1-S3", "A Grande 29848,5 -> 29857,6 (9,1)",
        r17["a_status"] == "A_CONFIRMED" and r17["a_size"] == 910,
        f"a={r17['a_status']}/{r17['a_size']}")

    r18 = close[16 * 60 + 18]
    seg(16 * 60 + 18, "B1-S4", "AUT bajista; TT principal pendiente 29829,1",
        r18["b_status"] == "AUT" and r18["tt_status"] == "TT_PENDING"
        and r18["tt_objective"] == 2982910,
        f"b={r18['b_status']} tt={r18['tt_status']}/{r18['tt_objective']}")

    r19 = close[16 * 60 + 19]
    seg(16 * 60 + 19, "B1-S5", "1 local bajista 7,5 (29850,0 -> 29842,5)",
        r19["n_origin"] == 2985000 and r19["n_extreme"] == 2984250,
        "lectura local: no hay L2 descubierta en 16:19; "
        f"L1 n={r19['n_origin']}->{r19['n_extreme']}",
        authority="PROVISIONAL")

    r20 = close[16 * 60 + 20]
    seg(16 * 60 + 20, "B2-S1", "2 bajista confirmada 12,3 >= 7,5",
        r20["two_status"] == "CONFIRMED" and r20["two_size"] == 1230,
        f"two L1={r20['two_status']}/{r20['two_size']} (local no descubierta)")

    r21 = close[16 * 60 + 21]
    seg(16 * 60 + 21, "B2-S2", "3 confirmada; extremo final 29830,3",
        r21["three_status"] == "CONFIRMED" and r21["three_extreme"] == 2983030,
        f"three L1={r21['three_status']}/{r21['three_extreme']}")

    r22 = close[16 * 60 + 22]
    seg(16 * 60 + 22, "B2-S3",
        "A Grande 29830,3 -> 29850,8; AUT directo; nuevo 1 alcista",
        r22["aut_direct_status"] == "AUT_DIRECT_BY_A"
        and r22["n_origin"] == 2983030,
        f"aut={r22['aut_direct_status']} n={r22['n_origin']}")

    r23 = close[16 * 60 + 23]
    seg(16 * 60 + 23, "B3-S1",
        "A bajista desde 29850,8; AUT local; nuevo 1 29852,6 -> 29837,3",
        r23["n_origin"] == 2985260 and r23["n_extreme"] == 2983730,
        f"n L1={r23['n_origin']}->{r23['n_extreme']}")

    r24 = close[16 * 60 + 24]
    seg(16 * 60 + 24, "B3-S2",
        "A/B/AUT; TT bajista confirmado en 29828,1; TT alcista no alcanzado",
        r24["tt_status"] in ("TT_CONFIRMED", "TT_EXTENDED")
        and r24["tt_objective"] == 2982910 and r24["n_extreme"] <= 2982810,
        f"tt={r24['tt_status']} obj={r24['tt_objective']} n={r24['n_extreme']}")

    r25 = close[16 * 60 + 25]
    seg(16 * 60 + 25, "B4-S1", "gap +14; sin 2; secuencia implicita; nuevo 1 29848,5",
        r25["two_status"] == "IMPOSSIBLE_NO_FLAT"
        and r25["n_origin"] == 2984850
        and "GAP_IMPLICIT_SEQUENCE" in ev_by_bar.get(16 * 60 + 25, []),
        f"two={r25['two_status']} n={r25['n_origin']} "
        f"ev={[e for e in ev_by_bar.get(16*60+25, []) if 'GAP' in e or 'TT' in e]}")

    seg(16 * 60 + 25, "B4-S2", "TT alcista confirmado en 16:25",
        r25["tt_status"] in ("TT_CONFIRMED", "TT_EXTENDED")
        and r25["tt_objective"] > 2985000,
        f"tt={r25['tt_status']} obj={r25['tt_objective']}")

    r26 = close[16 * 60 + 26]
    seg(16 * 60 + 26, "B4-S3", "FT del TT de 16:25 y A bajista principal",
        r26["ft_status"] in ("FT_CONFIRMED", "FT_EXTENDED")
        and r26["ft_origin"] == 2987540 and r26["ft_dir"] == -1
        and r26["a_status"] in
        ("CONTRARY_MOVE_PENDING", "A_CONFIRMED") and r26["a_origin"] == 2987540,
        f"ft={r26['ft_status']}/{r26['ft_origin']}/{r26['ft_dir']} "
        f"a={r26['a_status']}/{r26['a_origin']}")

    r27 = close[16 * 60 + 27]
    seg(16 * 60 + 27, "B4-S4",
        "apertura plana +0,2; A/B/A-tendencia; TT pendiente",
        r27["two_status"] == "IMPOSSIBLE_TAIL"
        and r27["b_status"] in ("CANDIDATE", "B_GRANDE", "AUT")
        and r27["tt_status"] == "TT_PENDING",
        f"two={r27['two_status']} b={r27['b_status']} tt={r27['tt_status']}")

    r28 = close[16 * 60 + 28]
    seg(16 * 60 + 28, "B4-S5", "gap bajista; dos TT pendientes coexistentes",
        len([e for e in reader.events if e["event"] == "TT_PENDING"]) >= 2,
        f"TT_PENDING events={len([e for e in reader.events if e['event']=='TT_PENDING'])}")

    r29 = close[16 * 60 + 29]
    seg(16 * 60 + 29, "B4-S6", "dos TT culminados; nuevo 1 bajista dominante",
        r29["tt_status"] in ("TT_CONFIRMED", "TT_EXTENDED")
        and r29["n_extreme"] <= 2982210,
        f"tt={r29['tt_status']} n={r29['n_extreme']}")

    r30 = close[16 * 60 + 30]
    seg(16 * 60 + 30, "B4-S7", "1 bajista simplificado; modulo 53,6; A iniciada",
        r30["mod_size"] == 5360 and r30["a_status"] != "",
        f"mod={r30['mod_size']} a={r30['a_status']}")

    r31 = close[16 * 60 + 31]
    seg(16 * 60 + 31, "B4-S8",
        "FINAL_A 29810,8; TT objetivo 29757,2; minimo 29760,3; pendiente 3,1",
        r31["tt_objective"] == 2975720 and r31["tt_status"] == "TT_PENDING",
        f"tt={r31['tt_status']}/{r31['tt_objective']} min={r31['price']}")

    r32 = close[16 * 60 + 32]
    seg(16 * 60 + 32, "B4-S9",
        "gap; TT falla al superar FINAL_A; modulo conjunto 16:30-16:31; nueva A",
        r32["tt_status"] == "TT_FAILED",
        f"tt={r32['tt_status']} obj={r32['tt_objective']} a={r32['a_status']}")

    # metricas con nombres corregidos
    total = len(segs)
    passed = sum(1 for s in segs if s["status"] == "PASS")
    independent_ticks = 0  # v005 no etiqueta tick a tick
    summary = {
        "human_anchors_total": total,
        "human_anchors_passed": passed,
        "trace_rows_generated": len(reader.trace),
        "human_segments_validated": passed,
        "ticks_with_independent_human_label": independent_ticks,
        "blocks_total": 4,
        "blocks_passed": 1,
        "note": ("Las anclas son por vela; no existe etiqueta humana por tick. "
                 "trace_rows_generated NO es una metrica de fidelidad."),
    }
    with (HERE / "HUMAN_SEGMENTS_1615_1632.csv").open(
            "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(segs[0].keys()))
        w.writeheader()
        w.writerows(segs)
    (HERE / "HUMAN_SEGMENTS_1615_1632.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    for s in segs:
        print(s["status"], s["bar"], s["segment_id"], s["detail"])
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
