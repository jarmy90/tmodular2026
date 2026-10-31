#!/usr/bin/env python3
"""ITERACION 17 — 19 anclas humanas 16:15-16:32 sobre TMReadingManager."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "05_REFERENCE_ENGINE"))
from tm_reader_guard import verify as _verify_reader  # noqa: E402
_verify_reader()

from tm_reference_interpreter_v1_direct_aut import load_ticks, FEED  # noqa: E402
from tm_reading_manager import TMReadingManager  # noqa: E402

BARS = list(range(16 * 60 + 15, 16 * 60 + 33))


def main() -> int:
    ticks = [t for t in load_ticks(FEED) if BARS[0] <= t.bar % 1440 <= BARS[-1]]
    mgr = TMReadingManager(ticks).run()
    last = {}
    for r in mgr.rows:
        last[r["bar"]] = r
    l1 = mgr.l1.reading
    l2 = mgr.l2.reading if mgr.l2 else None
    l2_events = [e["event"] for e in (mgr.l2.events if mgr.l2 else [])]
    rows = []

    def l2bar(bar, key):
        return last.get(bar, {}).get(key)

    def add(sid, bar, expected, ok, detail):
        rows.append({"segment_id": sid, "bar": f"{bar // 60:02d}:{bar % 60:02d}",
                     "expected_state": expected, "status": "PASS" if ok else "FAIL",
                     "detail": detail})

    add("B1-1", BARS[1], "1 inicial 29877,0->29860,8",
        l2bar(BARS[1],"l1_one_size") == 1620 and l2bar(BARS[1],"l1_one_dir") == -1,
        f"L1_one={l2bar(BARS[1],'l1_one_size')}")
    add("B1-2", BARS[2], "2 no confirma; modulo 28,5",
        l2bar(BARS[2],"l1_mod") == 2850,
        f"L1_mod={l2bar(BARS[2],'l1_mod')}")
    add("B1-3", BARS[3], "A 9,1",
        l2bar(BARS[3],"l1_a_status") == "A_CONFIRMED"
        and l2bar(BARS[3],"l1_a_size") == 910,
        f"L1_a={l2bar(BARS[3],'l1_a_status')}/{l2bar(BARS[3],'l1_a_size')}")
    add("B1-4", BARS[4], "AUT + TT 29829,1",
        l2bar(BARS[4],"l1_b_status") == "AUT"
        and l2bar(BARS[4],"l1_tt") == "TT_PENDING"
        and l2bar(BARS[4],"l1_tt_objective") == 2982910,
        f"L1_b={l2bar(BARS[4],'l1_b_status')} tt={l2bar(BARS[4],'l1_tt_objective')}")

    def at(bar):
        return last.get(bar, {})

    add("B2-1", 16 * 60 + 20, "L2 1 = 7,5",
        l2bar(16 * 60 + 20, "l2_one_size") == 750,
        f"L2_one={l2bar(16 * 60 + 20, 'l2_one_size')}")
    add("B2-2", 16 * 60 + 21, "L2 2 = 12,3",
        l2bar(16 * 60 + 21, "l2_two_size") == 1230,
        f"L2_two={l2bar(16 * 60 + 21, 'l2_two_size')}")
    add("B2-3", 16 * 60 + 22, "L2 3 = 29830,3; modulo 19,7",
        l2bar(16 * 60 + 22, "l2_mod") == 1970,
        f"L2_mod={l2bar(16 * 60 + 22, 'l2_mod')}")
    add("B2-4", 16 * 60 + 22, "L2 AUT directo; nuevo 1 hasta 29850,8",
        l2bar(16 * 60 + 22, "l2_n_extreme") == 2985080
        and l2bar(16 * 60 + 22, "l2_tt_objective") == 2987050,
        f"L2_n={l2bar(16*60+22,'l2_n_origin')}->{l2bar(16*60+22,'l2_n_extreme')}")
    add("B3-1", 16 * 60 + 23, "L2 nuevo 1 29852,6->29837,3",
        l2bar(16*60+23,"l2_n_origin") == 2985260 and l2bar(16*60+23,"l2_n_extreme") == 2983730,
        f"L2_n={l2bar(16*60+23,'l2_n_origin')}->{l2bar(16*60+23,'l2_n_extreme')}")
    add("B3-2", 16 * 60 + 24, "TT alcista L2 pendiente; nuevo 1 a 29828,1",
        l2bar(16*60+24,"l2_tt") == "TT_PENDING"
        and l2bar(16*60+24,"l2_tt_objective") == 2987050,
        f"L2_tt={l2bar(16*60+24,'l2_tt')}/{l2bar(16*60+24,'l2_tt_objective')}")
    add("B4-1", 16 * 60 + 25, "TT L2 confirmado/extendido a 29875,4",
        l2bar(16*60+25,"l2_tt") == "TT_EXTENDED",
        f"L2_tt={l2bar(16*60+25,'l2_tt')}/{l2bar(16*60+25,'l2_tt_objective')}")
    add("B4-2", 16 * 60 + 25, "nuevo 1 L1 desde la apertura 29848,5",
        l2bar(16*60+25,"l1_n_origin") == 2984850, f"L1_n={l2bar(16*60+25,'l1_n_origin')}")
    add("B4-3", 16 * 60 + 26, "A principal desde 29875,4",
        l2bar(16*60+26,"l1_a").endswith("@2987540"),
        f"L1_a={l2bar(16*60+26,'l1_a')}")
    add("B4-4", 16 * 60 + 27, "A/B/A-tendencia; TT pendiente",
        False, f"L1={l1.phase}/{l1.a_status}/{l1.b_status} tt={l1.tt_status}")
    add("B4-5", 16 * 60 + 28, "dos TT pendientes (L1 y L2)",
        False, f"L1_tt={l1.tt_status} L2_tt={l2.tt_status if l2 else ''}")
    add("B4-6", 16 * 60 + 29, "dos TT confirmados; nuevo 1 bajista",
        False, "no alcanzado")
    add("B4-7", 16 * 60 + 30, "modulo 53,6; A iniciada",
        False, f"L1_mod={l1.mod_size}")
    add("B4-8", 16 * 60 + 31, "final_A 29810,8; TT 29757,2 pendiente",
        False, f"L1_tt={l1.tt_status}/{l1.tt_objective}")
    add("B4-9", 16 * 60 + 32, "TT falla por final_A; modulo conjunto",
        False, f"L1_tt={l1.tt_status}")

    passed = sum(1 for r in rows if r["status"] == "PASS")
    summary = {
        "human_anchors_total": len(rows),
        "human_anchors_passed": passed,
        "blocks_passed": sum(
            1 for b0, b1 in ((16*60+15, 16*60+18), (16*60+19, 16*60+22),
                             (16*60+22, 16*60+24), (16*60+24, 16*60+32))
            if all(r["status"] == "PASS" for r in rows
                   if b0 <= int(r["bar"][:2]) * 60 + int(r["bar"][3:]) <= b1)),
        "l2_discovered_automatically": mgr.l2 is not None,
        "l2_created_at_seq": mgr.l2_discovered_at_seq,
        "l2_seed_bar": mgr.l2_seed_bar % 1440,
        "tt_owners": mgr.tt_owners(),
        "l2_events": l2_events[:40],
    }
    ident = mgr.summaries()
    with (HERE / "ITER18_TT_OWNERS.csv").open("w", newline="", encoding="utf-8") as fh:
        recs = ident["tt_records"]
        w = csv.DictWriter(fh, fieldnames=list(recs[0].keys()) if recs else ["tt_id"])
        w.writeheader(); w.writerows(recs)
    with (HERE / "ITER18_GENERATIONS.csv").open("w", newline="", encoding="utf-8") as fh:
        gens = ident["generations"]
        w = csv.DictWriter(fh, fieldnames=list(gens[0].keys()) if gens else ["generation_id"])
        w.writeheader(); w.writerows(gens)
    with (HERE / "ITER17_ANCHORS.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    (HERE / "ITER17_ANCHORS.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for r in rows:
        print(r["status"], r["bar"], r["segment_id"], r["detail"])
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
