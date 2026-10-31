"""v3 ownership audit.

Reads the v3 generation/event CSVs and emits:
  PHASE_4_GENERATION_AUDIT.csv
  PHASE_4_L1_L2_MAP.csv
  PHASE_4_ERRORS.csv
  PHASE_4_SUMMARY.json
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
READ = BASE / "01_BLIND_READINGS"
OUT = Path(__file__).resolve().parent


def load(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def load_events(path: Path) -> dict[int, list[str]]:
    out: dict[int, list[str]] = {}
    for r in load(path):
        out.setdefault(int(r["gid"]), []).append(r["event"])
    return out


def main() -> int:
    full = load(READ / "V4_FULL_GENERATIONS.csv")
    l2 = load(READ / "V4_L2_1619_1624_GENERATIONS.csv")
    full_events = load_events(READ / "V4_FULL_EVENTS.csv")
    l2_events = load_events(READ / "V4_L2_1619_1624_EVENTS.csv")

    rows: list[dict] = []
    errors: list[dict] = []

    def add_error(reading: str, gid: int, code: str, detail: str) -> None:
        errors.append({"reading_id": reading, "gid": gid, "code": code, "detail": detail})

    def audit(reading: str, gens: list[dict], events: dict[int, list[str]]) -> None:
        by_id = {int(g["gid"]): g for g in gens}
        for g in gens:
            gid = int(g["gid"])
            parent_id = int(g["parent"] or 0)
            parent = by_id.get(parent_id)
            two = g["two_status"]
            three = g["three_status"]
            legal = g["three_legal"] == "True"
            mod_owner = g["mod_owner"] or ""
            refs = g["refs_owner"] or ""
            three_owner = g["three_owner"] or ""
            mod_reading = g["mod_owner_reading"] or ""
            mod_gen = int(g["mod_owner_generation"] or 0)
            inherited = parent["refs_owner"] if parent else "none"
            errs: list[str] = []

            if three in ("CONFIRMED", "EXTENDED") and two != "CONFIRMED":
                errs.append("INVALID_THREE_WITHOUT_CONFIRMED_TWO")
            if g["three_extreme"] not in ("", "0") and not legal:
                errs.append("STALE_FUNCTION_STATE")
            if mod_owner.startswith("3") and not legal:
                errs.append("INVALID_MODULE_EXTENSION")
            if refs and not refs.startswith(reading + ":"):
                errs.append("CROSS_READING_REFERENCE_LEAK")
            if refs and refs.split(":")[1] != str(gid):
                errs.append("CROSS_GENERATION_REFERENCE_LEAK")
            if three_owner and not three_owner.startswith(reading + ":"):
                errs.append("CROSS_READING_REFERENCE_LEAK")
            if three_owner and three_owner.split(":")[1] != str(gid):
                errs.append("CROSS_GENERATION_REFERENCE_LEAK")
            if mod_reading and mod_reading != reading:
                errs.append("CROSS_READING_REFERENCE_LEAK")
            if mod_gen and mod_gen != gid:
                errs.append("CROSS_GENERATION_REFERENCE_LEAK")
            if "THREE_EXTENDED_ABSORBS_AB" in events.get(gid, []) and not legal:
                errs.append("INVALID_ABSORPTION")

            # new-one origin: inherit the transition's structural origin
            if parent:
                expected = None
                # The inherited origin is defined by the reason that CREATED
                # this generation, not by how it later ended.
                if g["reason"] == "AUT_B":
                    expected = parent["b_origin"]
                elif g["reason"] == "A_USED_AS_TREND":
                    expected = parent["a_origin"]
                elif g["reason"] == "C_USED_AS_TREND":
                    expected = parent["c_origin"]
                if expected is not None and g["one_origin"] != expected:
                    errs.append("INVALID_NEW_ONE_ORIGIN")

            for e in errs:
                add_error(reading, gid, e, f"end={g['end_reason']} parent={parent_id}")

            if errs:
                cls = "INVALID"
            elif g["end_reason"] == "GAP":
                cls = "INTEGRATED_IN_LARGER_MODULE"
            elif g["end_reason"] == "OPEN_AT_FEED_END":
                cls = "VALID_PRIMARY_PENDING"
            elif g["end_reason"] in ("AUT_B", "A_USED_AS_TREND", "C_USED_AS_TREND"):
                cls = "VALID_PRIMARY"
            else:
                cls = "PENDING_EXPERT_DECISION"

            next_fn = {
                "AUT_B": "1_from_B",
                "A_USED_AS_TREND": "1_from_A",
                "C_USED_AS_TREND": "1_from_C",
                "GAP": "1_observable_from_open",
                "OPEN_AT_FEED_END": "pending",
            }.get(g["end_reason"], "A/B/C")

            rows.append({
                "reading_id": reading,
                "gid": gid,
                "parent": parent_id,
                "reason": g["reason"],
                "end_reason": g["end_reason"],
                "end_time": g["end_time"],
                "two_status": two,
                "two_confirmed": "SI" if two == "CONFIRMED" else "NO",
                "three_status": three,
                "three_legal": "SI" if legal else "NO",
                "three_owner": three_owner,
                "mod_status": g["mod_status"],
                "mod_owner": mod_owner,
                "mod_owner_reading": mod_reading,
                "mod_owner_generation": mod_gen,
                "invalidation_reason": g["three_invalidation"],
                "inherited_refs": inherited,
                "next_function": next_fn,
                "classification": cls,
                "errors": ";".join(errs) if errs else "NONE",
                "one_origin": g["one_origin"],
                "one_extreme": g["one_extreme"],
                "one_size": g["one_size"],
                "module_size": g["mod_size"],
                "a_size": g["a_size"],
                "b_measure": g["b_measure"],
                "c_size": g["c_size"],
            })

    audit("L1", full, full_events)
    audit("L2", l2, l2_events)

    # L2 duplicates of L1: same one origin/extreme/size
    l1_keys = {(r["one_origin"], r["one_extreme"], r["one_size"]): f"L1-G{r['gid']}"
               for r in rows if r["reading_id"] == "L1"}
    for r in rows:
        if r["reading_id"] != "L2":
            continue
        dup = l1_keys.get((r["one_origin"], r["one_extreme"], r["one_size"]))
        if dup and r["classification"] != "INVALID":
            r["classification"] = "INTEGRATED_IN_LARGER_MODULE"
            r["errors"] = (r["errors"] + ";" if r["errors"] != "NONE" else "") + f"SAME_AS_{dup}"

    fields = list(rows[0].keys())
    with (OUT / "PHASE_4_GENERATION_AUDIT.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    with (OUT / "PHASE_4_L1_L2_MAP.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    with (OUT / "PHASE_4_ERRORS.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["reading_id", "gid", "code", "detail"])
        w.writeheader()
        w.writerows(errors)

    counts: dict[str, int] = {}
    for r in rows:
        counts[f"{r['reading_id']}:{r['classification']}"] = counts.get(
            f"{r['reading_id']}:{r['classification']}", 0) + 1
    error_counts: dict[str, int] = {}
    for e in errors:
        error_counts[e["code"]] = error_counts.get(e["code"], 0) + 1

    summary = {
        "reader": "blind_reader_v4_functional_autonomy.py",
        "L1_full_generations": len(full),
        "L2_generations": len(l2),
        "audit_rows": len(rows),
        "counts": counts,
        "error_counts": error_counts,
        "errors_total": len(errors),
        "q_b3": "CLOSED",
        "q_b3_note": (
            "The 16:23 3 in v2 belonged to a generation whose 2 was IMPOSSIBLE. "
            "v3 invalidates it. The legal path is B Grande -> C, not 3 extension."
        ),
        "q_aut": "RESOLVED_STRUCTURAL_MIDPOINT",
        "q_3_50": "RESOLVED_INCLUSIVE",
        "generations_approved": False,
        "tree_frozen": False,
        "originals_modified": False,
    }
    (OUT / "PHASE_4_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
