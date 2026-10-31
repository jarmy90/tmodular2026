#!/usr/bin/env python3
"""Iteracion 23A — trazador tick a tick de LOCAL-G2.

Exporta, para cada tick de la ventana, el estado local completo y las
invariantes geometricas. No modifica el motor: solo lo observa para localizar
las contradicciones de direccion, origen de A y genealogia del TT.

Uso:
    python trace_local_23a.py 1626    # semilla en 16:26
    python trace_local_23a.py 1627    # semilla en 16:27
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))

from tm_local_generation import LocalBranch  # noqa: E402
from tm_reference_interpreter_v1_direct_aut import FEED, load_ticks  # noqa: E402


def window(ticks, lo: int, hi: int):
    return [t for t in ticks if lo <= t.bar % 1440 <= hi]


FIELDS = ("seq", "bar", "price", "question", "cand_role", "cand_status",
          "mod_status", "mod_origin", "mod_extreme", "mod_size", "mod_dir",
          "mod_ok", "a_status", "a_origin", "a_extreme", "a_size", "a_dir",
          "b_status", "b_origin", "b_extreme", "b_size", "b_dir", "b_ratio",
          "tt_status", "tt_module_size", "tt_final_a", "tt_objective",
          "tt_invalidation", "events")


def state(branch: LocalBranch, t) -> dict:
    # direccion esperada por geometria: signo(extremo - origen)
    mod_ok = ""
    if branch.module_origin and branch.module_extreme and branch.module_dir:
        geo = (branch.module_extreme > branch.module_origin) - (
            branch.module_extreme < branch.module_origin)
        mod_ok = "OK" if geo == branch.module_dir else "BROKEN"
    return {
        "seq": t.seq, "bar": t.bar % 1440, "price": t.price,
        "question": branch.module_status,
        "cand_role": "A" if branch.a_status == "CANDIDATE" else (
            "B" if branch.b_status == "B_PHYSICAL" else ""),
        "cand_status": branch.a_status or branch.b_status,
        "mod_status": branch.module_status,
        "mod_origin": branch.module_origin,
        "mod_extreme": branch.module_extreme,
        "mod_size": branch.module_size, "mod_dir": branch.module_dir,
        "mod_ok": mod_ok,
        "a_status": branch.a_status, "a_origin": branch.a_origin,
        "a_extreme": branch.a_extreme, "a_size": branch.a_size,
        "a_dir": branch.a_dir,
        "b_status": branch.b_status, "b_origin": branch.b_origin,
        "b_extreme": branch.b_extreme, "b_size": branch.b_size,
        "b_dir": branch.b_dir, "b_ratio": branch.b_ratio,
        "tt_status": branch.tt_status,
        "tt_module_size": getattr(branch, "tt_module_size", ""),
        "tt_final_a": branch.tt_final_a, "tt_objective": branch.tt_objective,
        "tt_invalidation": branch.tt_invalidation,
        "events": "|".join(e["event"] for e in branch.events[
            max(0, len(branch.events) - 4):]),
    }


def main() -> int:
    which = sys.argv[1] if len(sys.argv) > 1 else "1626"
    lo = {"1626": 16 * 60 + 26, "1627": 16 * 60 + 27}[which]
    ticks = load_ticks(FEED)
    ticks = window(ticks, lo, 16 * 60 + 29)
    branch = LocalBranch(generation_id=f"LOCAL-G2-{which}")
    rows = []
    prev_events = 0
    for t in ticks:
        branch.feed(t)
        rows.append(state(branch, t))
        for e in branch.events[prev_events:]:
            if e["event"] not in ("LOCAL_SEEDED",):
                print(f"[{which}] {e['seq']:>5} {e['event']:<34} {e['detail']}")
        prev_events = len(branch.events)
    out = HERE / f"ITER23A_LOCAL_TRACE_{which}.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    broken = [r for r in rows if r["mod_ok"] == "BROKEN"]
    print(f"\nfilas={len(rows)} ticks={len(ticks)} "
          f"invariantes_direccion_rotas={len(broken)}")
    if broken:
        b = broken[0]
        print("primera ruptura:", {k: b[k] for k in
                                   ("seq", "price", "mod_origin", "mod_extreme",
                                    "mod_size", "mod_dir")})
    snap = branch.snapshot()
    print("final:", {k: snap[k] for k in ("status", "module", "a", "b", "tt")})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
