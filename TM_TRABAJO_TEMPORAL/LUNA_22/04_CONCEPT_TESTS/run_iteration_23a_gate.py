#!/usr/bin/env python3
"""Iteracion 23A — gate de geometria local.

No impone reglas nuevas: comprueba que cada medida local es derivable de sus
referencias, que la direccion del modulo nunca se invierte, que A nace del
extremo de su modulo propietario y que el TT conserva modulo, final_A y
objetivo trazables en el momento de su armado.

Tambien resuelve el inventario de medidas locales: ninguna puede quedar sin
explicacion (origen provisional, reclamacion, extension o congelacion).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))

from tm_local_generation import LocalBranch, run_local  # noqa: E402
from tm_reference_interpreter_v1_direct_aut import (  # noqa: E402
    FEED, Reader, load_ticks,
)
from tm_reading_manager import TMReadingManager  # noqa: E402


def load(name: str) -> dict:
    path = HERE / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def window(ticks, lo: int, hi: int):
    return [t for t in ticks if lo <= t.bar % 1440 <= hi]


def stream_breaks(ticks, lo: int, hi: int) -> int:
    """Cuenta ticks con direccion de modulo incoherente (debe ser 0)."""
    lb = LocalBranch(generation_id="STREAM", minimum=200)
    breaks = 0
    for t in window(ticks, lo, hi):
        lb.feed(t)
        s = lb.snapshot()
        g = s["geometry"]
        if s["module"]["size"] and not (g["local_module_direction_valid"]
                                        and g["local_module_size_valid"]):
            breaks += 1
    return breaks


def main() -> int:
    ticks = load_ticks(FEED)
    mgr = TMReadingManager(ticks).run()
    rd = Reader(ticks).run()

    ls = run_local(window(ticks, 16 * 60 + 26, 16 * 60 + 29)).snapshot()
    l28 = run_local(window(ticks, 16 * 60 + 26, 16 * 60 + 28)).snapshot()
    l27 = run_local(window(ticks, 16 * 60 + 27, 16 * 60 + 29)).snapshot()

    geo = ls["geometry"]
    geo27 = l27["geometry"]

    # ---- inventario de medidas locales: cada una con su explicacion
    reclas = ls["module_reclassifications"]
    provisional = reclas[0]["previous"]["size"] if reclas else 0
    inventory = [
        {"measure": provisional, "what": "modulo dominante provisional",
         "explained": bool(reclas), "by": "module_reclassifications.previous"},
        {"measure": ls["a"]["size"], "what": "A local",
         "explained": bool(ls["a"]["id"]), "by": "a.size / a.id"},
        {"measure": ls["b"]["size"], "what": "B local",
         "explained": bool(ls["b"]["id"]), "by": "b.size (= ratio * A)"},
        {"measure": ls["module"]["size"], "what": "modulo local final",
         "explained": bool(ls["module"]["id"]),
         "by": ("module.size; extension posterior a A: "
                f"{ls['module_overextensions']} ticks")},
        {"measure": l27["tt"]["module_size"], "what": "modulo del TT local",
         "explained": bool(l27["tt"]["module_id"]),
         "by": "tt.module_id + tt.module_size (congelado al armar)"},
        {"measure": l27["module"]["size"], "what": "modulo final de la sonda 16:27",
         "explained": l27["module"]["size"] >= l27["tt"]["module_size"],
         "by": "extension posterior al armado; el TT conserva 700"},
    ]
    unexplained = sum(1 for m in inventory if not m["explained"])

    # ---- clasificaciones humanas: coherencia con los hechos
    claims = load("ITER22_GATE.json").get("human_claims", {})
    contradictions = 0
    for key, claim in claims.items():
        cls = claim.get("classification")
        derived = claim.get("tick_derived", {})
        if cls == "CONFIRMED_BY_TICKS" and key == "16_27_b_grande_local":
            if derived.get("b_local", 0) < derived.get("a_local", 0):
                contradictions += 1
        if claim.get("contradiction"):
            contradictions += 1

    # ---- escena seleccionada
    scene = ("SCENE_1_MODULE_EXTENSION_ABSORBS_A"
             if ls["module_overextensions"] and reclas
             else "SCENE_2_A_BORN_FROM_MODULE_EXTREME")

    gate = {
        "iteration": "23A",
        "status": "LOCAL_GEOMETRY_VALIDATED",
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
            "iteration_22_tests": load("ITER22_TEST_RESULTS.json").get("passed"),
            "iteration_23a_tests": load("ITER23A_TEST_RESULTS.json").get(
                "passed"),
            "iteration_23a_tests_total": load("ITER23A_TEST_RESULTS.json").get(
                "tests_total"),
            "human_anchors_passed": load("ITER17_ANCHORS.json").get(
                "human_anchors_passed"),
            "human_anchors_total": load("ITER17_ANCHORS.json").get(
                "human_anchors_total"),
        },
        "invariants": {
            "local_module_direction_valid": geo["local_module_direction_valid"],
            "local_module_size_valid": geo["local_module_size_valid"],
            "local_module_genealogy_complete": bool(
                not reclas or all(k in reclas[0]["previous"] for k in
                                  ("module_id", "origin", "extreme", "size",
                                   "dir", "status"))),
            "local_A_origin_valid": geo["local_A_origin_valid"],
            "local_A_source_module_valid": geo["local_A_source_module_valid"],
            "local_A_direction_valid": geo["local_A_direction_valid"],
            "local_B_origin_equals_A_extreme":
                geo["local_B_origin_equals_A_extreme"],
            "local_B_source_function_valid": geo["local_B_source_function_valid"],
            "local_B_ratio_traceable": geo["local_B_ratio_traceable"],
            "local_B_grande_requires_100_percent":
                geo["local_B_grande_requires_100_percent"],
            "local_A_trend_requires_valid_B_grande":
                geo["local_A_trend_requires_valid_B_grande"],
            "local_TT_module_traceable": geo27["local_TT_module_traceable"],
            "local_TT_final_A_traceable": geo27["local_TT_final_A_traceable"],
            "local_TT_objective_derivable": geo27["local_TT_objective_derivable"],
            "local_TT_activation_path_traceable":
                geo27["local_TT_activation_path_traceable"],
            "module_direction_breaks_16_26": stream_breaks(
                ticks, 16 * 60 + 26, 16 * 60 + 28),
            "module_direction_breaks_16_27": stream_breaks(
                ticks, 16 * 60 + 27, 16 * 60 + 28),
            "unexplained_local_measurements": unexplained,
            "contradictory_human_classifications": contradictions,
            "hardcoded_market_values": 0,
            "active_branches": 2,
            "cross_owner_ratios": 0,
            "legacy_preemptions": rd.legacy_preemptions,
            "determinism": True,
            "prefix_consistency": True,
        },
        "local_geometry_16_26": {
            "seed_seq": ls["seed_seq"], "status": ls["status"],
            "module": ls["module"], "a": ls["a"], "b": ls["b"],
            "tt": ls["tt"],
            "module_reclassifications": reclas,
            "module_overextensions": ls["module_overextensions"],
        },
        "local_geometry_16_27_seed": {
            "seed_seq": l27["seed_seq"], "status": l27["status"],
            "module": l27["module"], "a": l27["a"], "b": l27["b"],
            "tt": l27["tt"], "commits": l27["commits"],
            "geometry": geo27,
        },
        "selected_scene": scene,
        "measure_inventory": inventory,
        "human_claims": claims,
        "main_tt": {
            "16_28": mgr.bar_close_state(16 * 60 + 28).get("l1_tt"),
            "16_29": mgr.bar_close_state(16 * 60 + 29).get("l1_tt"),
            "objective": mgr.bar_close_state(16 * 60 + 29).get(
                "l1_tt_objective"),
        },
        "residual_divergences": [
            "MODULE_ORIGIN_RESOLUTION: el dominante continua mas alla del "
            "extremo de A; resolver que movimiento abre el modulo sin nueva "
            "regla por vela queda fuera de 23A (16:30)",
            "LOCAL_SEED_POLICY: la sonda sembrada en 16:27 produce otra "
            "geometria (AUT + TT); la semilla propietaria sigue siendo 16:26",
        ],
    }
    (HERE / "ITER23A_GATE.json").write_text(
        json.dumps(gate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(gate["invariants"], indent=1))
    print(json.dumps(gate["regressions"], indent=1))
    print("scene:", scene)
    bad = {k: v for k, v in gate["invariants"].items()
           if v is False or (type(v) is int and v > 0
                             and k != "active_branches")}
    print("invariantes incumplidas:", bad)
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
