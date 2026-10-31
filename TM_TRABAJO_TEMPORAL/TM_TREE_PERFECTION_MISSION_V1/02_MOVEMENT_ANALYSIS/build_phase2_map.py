"""Phase 2 map builder — experimental L1/L2 hierarchy and generation classification.

Inputs (already blocked in Checkpoint 1, corrected by Q1/Q2/Q3):
  BLIND_V3_GENERATIONS.csv          -> L1 principal chain, 26 generations
  L2_1619_1624_GENERATIONS.csv      -> L2 local read, 3 generations

This script does NOT create rules. It only classifies the experimental output.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "01_BLIND_READINGS"
OUT = Path(__file__).resolve().parent

FIELDS = [
    "reading_id", "layer", "parent", "origin_event", "end_reason", "end_time",
    "direction", "one_origin", "one_extreme", "one_size",
    "two_status", "two_size", "three_status", "three_extreme",
    "module_origin", "module_extreme", "module_size", "module_status", "module_owner",
    "a_origin", "a_extreme", "a_size", "a_status",
    "b_measure", "b_status", "aut_reason", "c_size", "c_status",
    "tt_status", "classification", "note",
]


def load(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def classify_l1(row: dict) -> tuple[str, str]:
    end = row["end_reason"]
    if end == "GAP":
        return "INTEGRATED_IN_LARGER_MODULE", "gap implicit A-B-AUT; new 1 from open, no invented ticks"
    if end == "OPEN_AT_FEED_END":
        return "VALID_PRIMARY_PENDING", "structural transition valid; evolution open at feed end"
    if end == "AUT_B":
        return "VALID_PRIMARY", "AUT_B structural transition; new 1 inherited from B"
    if end == "A_USED_AS_TREND":
        a = int(row["a_size"] or 0)
        m = int(row["mod_size"] or 0)
        if a > m:
            return "VALID_PRIMARY", "A used as trend crossed module base; new 1 inherited from A"
        return "INTEGRATED_IN_LARGER_MODULE", "A did not cross module base; no autonomous trend"
    return "PENDING_EXPERT_DECISION", "unclassified end reason"


def main() -> int:
    l1 = load(BASE / "BLIND_V3_GENERATIONS.csv")
    l2 = load(BASE / "L2_1619_1624_GENERATIONS.csv")

    rows: list[dict] = []
    for r in l1:
        cls, note = classify_l1(r)
        rows.append({
            "reading_id": f"L1-G{r['gid']}",
            "layer": "L1_PRIMARY",
            "parent": f"L1-G{r['parent']}" if r["parent"] != "0" else "",
            "origin_event": r["reason"],
            "end_reason": r["end_reason"],
            "end_time": r["end_time"],
            "direction": r["one_dir"],
            "one_origin": r["one_origin"],
            "one_extreme": r["one_extreme"],
            "one_size": r["one_size"],
            "two_status": r["two_status"],
            "two_size": r["two_size"],
            "three_status": r["three_status"],
            "three_extreme": r["three_extreme"],
            "module_origin": r["mod_origin"],
            "module_extreme": r["mod_extreme"],
            "module_size": r["mod_size"],
            "module_status": r["mod_status"],
            "module_owner": r["mod_owner"],
            "a_origin": r["a_origin"],
            "a_extreme": r["a_extreme"],
            "a_size": r["a_size"],
            "a_status": r["a_status"],
            "b_measure": r["b_measure"],
            "b_status": r["b_status"],
            "aut_reason": r["aut_reason"],
            "c_size": r["c_size"],
            "c_status": r["c_status"],
            "tt_status": r["tt_status"],
            "classification": cls,
            "note": note,
        })

    for r in l2:
        duplicate = None
        for p in l1:
            if (p["one_origin"] == r["one_origin"] and p["one_extreme"] == r["one_extreme"]
                    and p["one_size"] == r["one_size"]):
                duplicate = f"L1-G{p['gid']}"
                break
        rows.append({
            "reading_id": f"L2-G{r['gid']}",
            "layer": "L2_SECONDARY",
            "parent": f"L2-G{r['parent']}" if r["parent"] != "0" else "",
            "origin_event": r["reason"],
            "end_reason": r["end_reason"],
            "end_time": r["end_time"],
            "direction": r["one_dir"],
            "one_origin": r["one_origin"],
            "one_extreme": r["one_extreme"],
            "one_size": r["one_size"],
            "two_status": r["two_status"],
            "two_size": r["two_size"],
            "three_status": r["three_status"],
            "three_extreme": r["three_extreme"],
            "module_origin": r["mod_origin"],
            "module_extreme": r["mod_extreme"],
            "module_size": r["mod_size"],
            "module_status": r["mod_status"],
            "module_owner": r["mod_owner"],
            "a_origin": r["a_origin"],
            "a_extreme": r["a_extreme"],
            "a_size": r["a_size"],
            "a_status": r["a_status"],
            "b_measure": r["b_measure"],
            "b_status": r["b_status"],
            "aut_reason": r["aut_reason"],
            "c_size": r["c_size"],
            "c_status": r["c_status"],
            "tt_status": r["tt_status"],
            "classification": "INTEGRATED_IN_LARGER_MODULE" if duplicate else "VALID_SECONDARY",
            "note": (
                f"same structural generation as {duplicate}; not a second reading"
                if duplicate else
                "L2 local scale authorized by Q1; independent references, max two active scales"
            ),
        })

    out_csv = OUT / "PHASE_2_L1_L2_MAP.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    counts: dict[str, int] = {}
    for r in rows:
        key = f"{r['layer']}:{r['classification']}"
        counts[key] = counts.get(key, 0) + 1

    summary = {
        "generated_from": {
            "L1": "BLIND_V3_GENERATIONS.csv",
            "L2": "L2_1619_1624_GENERATIONS.csv",
        },
        "L1_generations": len(l1),
        "L2_generations": len(l2),
        "total_rows": len(rows),
        "counts": counts,
        "L1_end_reasons": {},
        "a_gate_note": (
            "b100 and bturn produce the same 26 L1 generations; only A confirmation time differs. "
            "The hierarchy is experimental and does not freeze the tree."
        ),
        "hierarchy_status": "EXPERIMENTAL_HIERARCHY_V1_NOT_CANON",
    }
    for r in l1:
        summary["L1_end_reasons"][r["end_reason"]] = summary["L1_end_reasons"].get(r["end_reason"], 0) + 1

    (OUT / "PHASE_2_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
