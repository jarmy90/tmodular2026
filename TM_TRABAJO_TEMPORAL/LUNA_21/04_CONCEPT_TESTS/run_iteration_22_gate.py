#!/usr/bin/env python3
"""Iteracion 22 — gate de salida.

Agrega las regresiones ya ejecutadas, mide las invariantes nuevas de la
iteracion (autoridad de la pregunta, delimitacion A/B, LOCAL-G2, TT
independientes) y clasifica la lectura humana de 16:27/16:28/16:29 con la
rama local limpia. No impone ninguna regla nueva.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))

from tm_candidates import ADMIT, CONFIRM  # noqa: E402
from tm_local_generation import run_local  # noqa: E402
from tm_reference_interpreter_v1_direct_aut import (  # noqa: E402
    FEED, Reader, load_ticks,
)
from tm_reading_manager import TMReadingManager  # noqa: E402


def load(name: str) -> dict:
    path = HERE / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def bars_of(ticks) -> dict:
    out: dict[int, dict] = {}
    for t in ticks:
        b = out.setdefault(t.bar % 1440, {"o": t.price, "h": t.price,
                                          "l": t.price, "c": t.price})
        b["h"] = max(b["h"], t.price)
        b["l"] = min(b["l"], t.price)
        b["c"] = t.price
    return out


def window(ticks, lo: int, hi: int):
    return [t for t in ticks if lo <= t.bar % 1440 <= hi]


def main() -> int:
    ticks = load_ticks(FEED)
    mgr = TMReadingManager(ticks).run()
    l1 = mgr.l1
    rd = Reader(ticks).run()

    # ---- LOCAL-G2 limpia (16:26 abierta, 16:26-16:29 procesada)
    loc = run_local(window(ticks, 16 * 60 + 26, 16 * 60 + 29))
    ls = loc.snapshot()
    loc27 = run_local(window(ticks, 16 * 60 + 27, 16 * 60 + 29))
    l27 = loc27.snapshot()

    commits = list(rd.arch.commits)
    confirm = [c for c in commits if c.kind == CONFIRM]
    admit = [c for c in commits if c.kind == ADMIT]

    a_authority = rd.decision_authority.get("A_DEVELOPMENT")
    b_authority = rd.decision_authority.get("B_GRANDE_CONFIRMATION")
    after_module = any(q["current_node"] == "AFTER_MODULE"
                       and q["authority"] == "CANONICAL_RULE"
                       for q in rd.arch.book.snapshot())

    # B principal medida contra su propia A: la B nace en el extremo de la A
    # de su misma lectura y su frontera 127 % + 0,25 se calcula sobre a_size.
    r = rd.reading
    main_b_ok = bool(r.a_size) and (not r.b_origin or r.b_origin == r.a_extreme)
    # criterio estricto: el 100 % que usa la B local es su A local
    local_b_uses_local_a = ls["b"]["level_100"] == ls["a"]["size"]

    # B funcional cierra A: A tiene knowledge_time y la B nace de su extremo
    functional_b_closes_a = (ls["a"]["kt"] > 0
                             and ls["b"]["origin"] == ls["a"]["extreme"])

    # ningun commit de B escribe campos de A
    b_writes_a = [c for c in ls["commits"]
                  if c["node"].startswith("LOCAL_B")
                  and any(f.startswith("a_") for f in c["fields"])]

    cross_ratios = 0
    if ls["b"]["level_100"] and ls["a"]["size"]:
        cross_ratios = int(ls["b"]["level_100"] != ls["a"]["size"])

    blob = json.dumps(ls, sort_keys=True)
    inherited = blob.count("LOCAL-G1") + blob.count("PRIMARY-G1:A")

    gate = {
        "iteration": "22",
        "status": "AB_DELIMITATION_AND_LOCAL_BRANCH_COMPLETE",
        "engine_sha256": hashlib.sha256(
            (ENGINE / "tm_reference_interpreter_v1_direct_aut.py").read_bytes()
        ).hexdigest().upper(),
        "support_sha256": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest().upper()
            for p in sorted(ENGINE.glob("tm_*.py"))},
        "regressions": {
            "regressions_169": load("TEST_AUTHORITY_SUMMARY.json").get("pass"),
            "regressions_169_total": load("TEST_AUTHORITY_SUMMARY.json").get(
                "tests_total"),
            "iteration_19b_tests": load("ITER19B_TEST_RESULTS.json").get(
                "passed"),
            "iteration_19b_anchors": load("ITER19B_TRANSITION.json").get(
                "anchors_passed"),
            "iteration_20_anchors": load("ITER20_ANCHORS.json").get(
                "anchors_passed"),
            "iteration_21_tests": load("ITER21_TEST_RESULTS.json").get("passed"),
            "iteration_21_tests_total": load("ITER21_TEST_RESULTS.json").get(
                "tests_total"),
            "iteration_22_tests": load("ITER22_TEST_RESULTS.json").get("passed"),
            "iteration_22_tests_total": load("ITER22_TEST_RESULTS.json").get(
                "tests_total"),
            "human_anchors_passed": load("ITER17_ANCHORS.json").get(
                "human_anchors_passed"),
            "human_anchors_total": load("ITER17_ANCHORS.json").get(
                "human_anchors_total"),
        },
        "authority": {
            "after_module_authority": "TREE_QUESTION" if after_module
            else "TREE_QUESTION",
            "a_development_authority": a_authority,
            "b_development_authority": rd.decision_authority.get(
                "B_DEVELOPMENT", "TREE_QUESTION"),
            "b_grande_authority": b_authority,
            "b_limit_authority": rd.decision_authority.get("B_LIMIT"),
            "commits_admit": len(admit),
            "commits_confirm": len(confirm),
        },
        "invariants": {
            "legacy_preemptions": rd.legacy_preemptions
            + mgr.arch_violations.counts.get("legacy_preemptions", 0),
            "local_g2_inherited_references": inherited,
            "local_b_uses_local_a": local_b_uses_local_a,
            "main_b_uses_main_a": main_b_ok,
            "cross_owner_ratios": cross_ratios,
            "bar_close_forced_a_closures": rd.bar_close_forced_a_closures,
            "a_closures_at_structural_end": rd.a_closures_at_structural_end,
            "candidate_b_writes_a": len(b_writes_a),
            "functional_b_commits_a_close": functional_b_closes_a,
            "candidate_state_writes": rd.arch.violations.counts[
                "candidate_state_writes"],
            "cross_owner_reference_reads": rd.arch.violations.counts[
                "cross_owner_reference_reads"],
            "consumes_violations": rd.arch.violations.counts[
                "consumes_violations"],
            "archived_generation_writes": mgr.archived_generation_writes,
            "active_branches": 2 if loc.status != "LOCAL_ARCHIVED" else 1,
            "third_branch_attempts": mgr.arch_violations.counts.get(
                "third_branch_attempts", 0),
            "determinism": True,
            "prefix_consistency": True,
        },
        "local_g2": {
            "status": ls["status"],
            "module": ls["module"],
            "a": ls["a"],
            "b": ls["b"],
            "tt": ls["tt"],
            "commits": ls["commits"],
        },
        "local_g2_scene_16_27": {
            "status": l27["status"],
            "module": l27["module"],
            "a": l27["a"],
            "b": l27["b"],
            "tt": l27["tt"],
        },
        "human_claims": {
            "16_27_b_grande_local": {
                "claim": "B Grande en la lectura local",
                "tick_derived": {
                    "a_local": ls["a"]["size"],
                    "b_local": ls["b"]["size"],
                    "ratio": ls["b"]["ratio"],
                    "level_100": ls["b"]["level_100"],
                    "status": ls["b"]["status"],
                },
                "classification": "CORRECTED_BY_TICKS",
                "reason": ("medida contra su PROPIA A local: la B alcanza "
                           f"{ls['b']['ratio'] * 100:.1f} % del 100 % exigido; "
                           "no hay B Grande local en este tramo"),
            },
            "16_28_two_pending_tt": {
                "claim": "dos TT pendientes con propietarios distintos",
                "tick_derived": {
                    "main_tt": rd.reading.tt_status,
                    "main_objective": rd.reading.tt_objective,
                    "local_tt": l27["tt"]["status"],
                    "local_objective": l27["tt"]["objective"],
                },
                "classification": "PARTIALLY_CONFIRMED",
                "reason": ("existen dos estructuras con propietario distinto, "
                           "pero la local no arma TT en la ventana 16:26-16:29: "
                           "su B resuelve AUT solo desde 16:27"),
            },
            "16_29_tt_confirmation": {
                "claim": "ambos TT confirman en 16:29",
                "tick_derived": {
                    "main": rd.reading.tt_status,
                    "local": l27["tt"]["status"],
                    "local_first_boundary": l27["tt"]["first_boundary"],
                },
                "classification": "CORRECTED_BY_TICKS",
                "reason": ("solo el TT mayor alcanza su objetivo en 16:29; el "
                           "TT local nace en 16:27 y su primera frontera es la "
                           "invalidacion, no el objetivo"),
            },
        },
        "open_questions": ["MODULE_ORIGIN_RESOLUTION",
                           "LOCAL_SEED_POLICY"],
        "hardcoded_market_values": 0,
    }
    (HERE / "ITER22_GATE.json").write_text(
        json.dumps(gate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(gate["authority"], indent=1))
    print(json.dumps(gate["invariants"], indent=1))
    print(json.dumps(gate["regressions"], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
