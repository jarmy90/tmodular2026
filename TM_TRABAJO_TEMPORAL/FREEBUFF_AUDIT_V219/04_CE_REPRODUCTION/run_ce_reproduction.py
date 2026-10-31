# -*- coding: utf-8 -*-
"""Independent reproduction of the 21 CE sequences against R5 9BD1BEDB.

Read-only w.r.t. the engine: it is imported from 00_INPUTS_REFERENCE/variants.
Writes observations to ./ce_out/. No expectation is fed into the engine.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
CORE = AUDIT / "00_INPUTS_REFERENCE" / "variants" / "R5_AUDITED_9BD1BEDB.py"
OUT = HERE / "ce_out"
OUT.mkdir(exist_ok=True)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

spec = importlib.util.spec_from_file_location("tm_r5_audited", CORE)
m = importlib.util.module_from_spec(spec)
sys.modules["tm_r5_audited"] = m
spec.loader.exec_module(m)

# Tick layouts exactly as published in CE_TESTS_v219.md (one list = one bar).
CASES = [
    dict(id="CE1-POS", ce="CE-1", variant="POSITIVO",
         bars=[[100.00, 101.00, 102.00, 101.75, 102.00],
               [102.00, 102.75, 103.50, 104.00, 104.25]]),
    dict(id="CE1-NEG", ce="CE-1", variant="NEGATIVO",
         bars=[[100.00, 101.00, 102.00, 101.75, 102.00],
               [102.00, 101.50, 101.00, 100.50]]),
    dict(id="CE1-FRON", ce="CE-1", variant="FRONTERA",
         bars=[[100.00, 101.00, 102.00, 101.75, 102.00],
               [102.00, 102.50, 103.00, 104.00]]),
    dict(id="CE2-POS", ce="CE-2", variant="POSITIVO",
         bars=[[0.00, 4.00, 8.00, 10.00],
               [10.00, 8.00, 6.00],
               [6.00, 8.00, 10.00, 11.00],
               [11.00, 9.00, 7.00],
               [7.00, 12.00, 16.00],
               [16.00, 10.00, 3.90]]),
    dict(id="CE2-NEG", ce="CE-2", variant="NEGATIVO",
         bars=[[0.00, 4.00, 8.00, 10.00],
               [10.00, 8.00, 6.00],
               [6.00, 8.00, 10.00, 11.00],
               [11.00, 9.00, 7.00],
               [7.00, 12.00, 16.00],
               [16.00, 10.00, 0.25]]),
    dict(id="CE2-FRON", ce="CE-2", variant="FRONTERA",
         bars=[[0.00, 4.00, 8.00, 10.00],
               [10.00, 8.00, 6.00],
               [6.00, 8.00, 10.00, 11.00],
               [11.00, 6.00, 0.00]]),
    dict(id="CE3-POS", ce="CE-3", variant="POSITIVO",
         bars=[[0.00, 3.00, 6.00],
               [6.00, 7.00, 8.00, 9.00, 10.00, 11.00, 11.75],
               [11.75, 12.25]]),
    dict(id="CE3-NEG", ce="CE-3", variant="NEGATIVO",
         bars=[[0.00, 3.00, 6.00],
               [6.25, 7.00, 8.00, 9.00, 10.00, 11.00, 11.50]]),
    dict(id="CE3-FRON", ce="CE-3", variant="FRONTERA",
         bars=[[0.00, 3.00, 6.00],
               [6.00, 7.00, 8.00, 9.00, 10.00, 11.00, 12.00]]),
    dict(id="CE4-POS", ce="CE-4", variant="POSITIVO",
         bars=[[0.00, 5.00, 10.00, 15.00, 20.00],
               [20.00, 18.00, 16.00],
               [16.00, 18.00, 20.00, 21.00],
               [21.00, 19.00, 17.00],
               [17.00, 23.00, 28.00, 30.00]]),
    dict(id="CE4-NEG", ce="CE-4", variant="NEGATIVO",
         bars=[[0.00, 5.00, 10.00, 15.00, 20.00],
               [20.00, 18.00, 16.00],
               [16.00, 15.00, 14.00, 15.00]]),
    dict(id="CE4-FRON", ce="CE-4", variant="FRONTERA",
         bars=[[0.00, 5.00, 10.00, 15.00, 20.00],
               [20.00, 18.00, 16.00],
               [16.00, 17.00, 18.00, 19.00, 20.00]]),
    dict(id="CE5-POS", ce="CE-5", variant="POSITIVO",
         bars=[[0.00, 4.00, 8.00, 10.00],
               [10.00, 8.00, 6.00],
               [6.00, 14.00, 15.75, 16.00],
               [15.75, 15.50, 15.25, 15.00, 14.00]]),
    dict(id="CE5-NEG", ce="CE-5", variant="NEGATIVO",
         bars=[[0.00, 4.00, 8.00, 10.00],
               [10.00, 8.00, 6.00],
               [6.00, 14.00, 15.75, 15.50]]),
    dict(id="CE5-FRON", ce="CE-5", variant="FRONTERA",
         bars=[[0.00, 4.00, 8.00, 10.00],
               [10.00, 8.00, 6.00],
               [6.00, 14.00, 16.00]]),
    dict(id="CE6-POS", ce="CE-6", variant="POSITIVO",
         bars=[[90.00, 96.00, 100.00],
               [100.00],
               [110.00, 110.50, 109.75, 111.00]]),
    dict(id="CE6-NEG", ce="CE-6", variant="NEGATIVO",
         bars=[[90.00, 96.00, 100.00],
               [100.00],
               [100.10, 100.50, 100.25, 100.75]]),
    dict(id="CE6-FRON", ce="CE-6", variant="FRONTERA",
         bars=[[90.00, 96.00, 100.00],
               [100.00],
               [100.25, 100.75, 100.50, 101.00]]),
    dict(id="CE7-AUT", ce="CE-7", variant="A_BASE",
         bars=[[0.00, 5.00, 10.00, 15.00, 20.00],
               [20.00, 15.00, 10.00, 5.00, -1.00, -3.00]]),
    dict(id="CE7-C-NEG", ce="CE-7", variant="C_SIN_CUT",
         bars=[[25.00, 20.00, 15.00, 10.00, 0.00],
               [0.00, 2.00, 4.00],
               [4.00, 2.00, 0.00, -0.25],
               [-0.25, 3.00, 7.00]]),
    dict(id="CE7-C-FRON", ce="CE-7", variant="C_CUT",
         bars=[[25.00, 20.00, 15.00, 10.00, 0.00],
               [0.00, 2.00, 4.00],
               [4.00, 2.00, 0.00, -0.25],
               [-0.25, 10.00, 20.00, 25.00, 26.00]]),
]


def build_points(bars):
    pts, seq = [], 0
    for bi, bar in enumerate(bars, start=1):
        for ti, price in enumerate(bar):
            seq += 1
            pts.append(m.Pt(m.price_i(price), seq, bi * 60000 + ti * 1000, bi))
    return pts


def snapshot(eng, p):
    def row(r):
        return {
            "id": r.reading_id, "state": r.state,
            "function": getattr(r, "active_function", ""),
            "dominant": bool(getattr(r, "dominant", False)),
            "direction": r.direction,
            "module_origin": r.module_origin, "module_extreme": r.module_extreme,
            "module_size": r.module_size,
            "a_origin": r.a_origin, "a_end": r.a_end, "a_size": r.a_size,
            "b_origin": r.b_origin, "b_extreme": r.b_extreme, "b_size": r.b_size,
            "b_grande": bool(getattr(r, "b_grande_time", 0)),
            "c_origin": r.c_origin, "c_extreme": r.c_extreme,
            "aut": bool(getattr(r, "aut_time", 0)),
            "aut_source": getattr(r, "aut_source", ""),
            "tt_hit": bool(getattr(r, "tt_hit", False)),
            "tt_target": getattr(r, "tt_target", 0),
            "tt_time": getattr(r, "tt_time", 0),
            "tt_knowledge_time": getattr(r, "tt_knowledge_time", 0),
            "cut": bool(getattr(r, "cut_confirmed", False)),
            "ft": bool(getattr(r, "ft", False)),
            "fail": getattr(r, "fail_reason", ""),
            "local_sequence_id": getattr(r, "local_sequence_id", ""),
            "question": {k: r.question.get(k, "") for k in m.QUESTION_KEYS},
        }
    local = eng._local
    return {
        "tick": p.seq, "bar": p.bar, "price": p.price,
        "phase": local.get("phase"),
        "armed": local.get("armed"),
        "candidate_bar": local.get("candidate_bar"),
        "readings": [row(r) for r in eng.readings],
        "active": [row(r) for r in eng.active if r.state != "DONE"],
        "events": [dict(e) for e in eng.events],
    }


def run(case):
    pts = build_points(case["bars"])
    eng = m.CanonicalEngine(pts, {})
    eng.trace_states = True
    states, event_cursor = [], 0
    for p in pts:
        before = len(eng.events)
        state_before = snapshot(eng, p)
        state_before["events"] = []
        eng.feed_chunk([p])
        snap = snapshot(eng, p)
        snap["before"] = state_before
        snap["events"] = [dict(e) for e in eng.events[before:]]
        snap["state_log_row"] = eng.state_log[-1] if eng.state_log else None
        states.append(snap)
    eng.finalize_stream()
    return eng, states, pts


def fingerprint(engine):
    blob = json.dumps({
        "events": engine.events,
        "readings": [{
            "id": r.reading_id, "state": r.state,
            "module_origin": r.module_origin, "module_extreme": r.module_extreme,
            "a_origin": r.a_origin, "a_end": r.a_end,
            "b_origin": r.b_origin, "b_extreme": r.b_extreme,
            "c_origin": r.c_origin, "c_extreme": r.c_extreme,
            "tt_hit": r.tt_hit, "tt_target": r.tt_target,
            "tt_time": r.tt_time, "tt_knowledge_time": r.tt_knowledge_time,
            "aut_time": r.aut_time, "b_grande_time": r.b_grande_time,
            "cut_confirmed": r.cut_confirmed, "ft": r.ft,
        } for r in engine.readings],
    }, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode()).hexdigest()


def main():
    report = []
    total_ticks = 0
    for case in CASES:
        eng1, states, pts = run(case)
        eng2, states2, _ = run(case)
        total_ticks += len(pts)
        fp1, fp2 = fingerprint(eng1), fingerprint(eng2)
        state_equal = json.dumps(states, sort_keys=True) == json.dumps(states2, sort_keys=True)

        # Prefix consistency: a run stopped at tick k must equal the full run at tick k.
        prefix_mismatch = 0
        for k in range(1, len(pts) + 1):
            e = m.CanonicalEngine(pts[:k], {})
            e.trace_states = True
            for p in pts[:k]:
                e.feed_chunk([p])
            a = e.state_log[-1] if e.state_log else None
            b = states[k - 1]["state_log_row"]
            if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
                prefix_mismatch += 1

        kinds = sorted({ev["kind"] for ev in eng1.events})
        funcs = sorted({ev.get("function", "") for ev in eng1.events if ev.get("function")})
        readings = [{
            "id": r.reading_id, "state": r.state,
            "function": getattr(r, "active_function", ""),
            "module_origin": r.module_origin, "module_extreme": r.module_extreme,
            "module_size": r.module_size,
            "a_size": r.a_size, "b_size": r.b_size,
            "b_grande": bool(r.b_grande_time), "aut": bool(r.aut_time),
            "tt_target": r.tt_target, "tt_hit": r.tt_hit,
            "cut": bool(r.cut_confirmed), "local": getattr(r, "local_sequence_id", ""),
        } for r in eng1.readings]
        report.append({
            "id": case["id"], "ce": case["ce"], "variant": case["variant"],
            "ticks": len(pts), "deterministic": (fp1 == fp2) and state_equal,
            "deterministic_state_log": state_equal,
            "fingerprint": fp1, "prefix_mismatch": prefix_mismatch,
            "event_kinds": kinds, "functions": funcs,
            "n_readings": len(eng1.readings),
            "readings": readings,
            "states": states,
        })
        print(f'{case["id"]:12s} ticks={len(pts):3d} det={(fp1==fp2) and state_equal} '
              f'prefix_bad={prefix_mismatch} readings={len(eng1.readings)} '
              f'events={len(eng1.events)} kinds={kinds}')

    (OUT / "CE_REPRODUCTION_RAW.json").write_text(
        json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    summary = {
        "engine": str(CORE), "engine_sha256": "9BD1BEDB5DEC8C5A1C3A831338503E90CC04EE3CD776CF4E01D27CF8AA0EBEAE",
        "cases": len(report), "ticks_total": total_ticks,
        "deterministic": sum(1 for r in report if r["deterministic"]),
        "deterministic_state_log": sum(1 for r in report if r["deterministic_state_log"]),
        "prefix_checks": total_ticks,
        "prefix_mismatches": sum(r["prefix_mismatch"] for r in report),
        "cases_with_reading": sum(1 for r in report if r["n_readings"] > 0),
        "cases_with_two_three_A_B_C_AUT_CUT_TT": sum(
            1 for r in report
            if any(f in r["functions"] for f in ("2", "3", "A", "B", "C", "AUT", "CUT", "TT"))),
    }
    (OUT / "CE_REPRODUCTION_SUMMARY.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
