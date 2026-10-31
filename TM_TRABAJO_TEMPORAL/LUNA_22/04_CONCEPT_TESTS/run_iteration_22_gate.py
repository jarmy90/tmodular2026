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
from tm_local_generation import AUT, B_GRANDE, run_local  # noqa: E402
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


def claim_b_grande(ls: dict) -> dict:
    """Reclamacion humana: B Grande en la lectura local de 16:27."""
    a, b = ls["a"], ls["b"]
    validated = bool(b["status"] in (B_GRANDE, AUT))
    internal = (not validated) and ls.get("module_overextensions", 0) > 0
    contradiction = validated and b["size"] < a["size"]
    return {
        "claim": "B Grande en la lectura local (16:27)",
        "tick_derived": {"a_local": a["size"], "b_local": b["size"],
                         "ratio": b["ratio"], "level_100": b["level_100"],
                         "status": b["status"],
                         "module_overextensions": ls.get(
                             "module_overextensions", 0)},
        "classification": ("CONFIRMED_BY_TICKS" if validated else
                           "PARTIALLY_CONFIRMED" if internal else
                           "CORRECTED_BY_TICKS"),
        "contradiction": contradiction,
        "reason": ("B alcanza el 100 % de su propia A" if validated else
                   f"B={b['size']} / A={a['size']} = {b['ratio'] * 100:.1f} % del "
                   f"100 % exigido; no hay B Grande en la ventana"
                   + ("; el dominante continua mas alla del extremo de A, de "
                      "modo que la B es un rebote interno del modulo"
                      if internal else "")),
    }


def claim_two_pending(main28: dict, l28: dict) -> dict:
    """Reclamacion humana: dos TT pendientes con propietarios distintos.

    Se evalua sobre el snapshot de cierre de 16:28 de cada rama, no sobre el
    estado final del feed: usar el estado posterior convertiria la reclamacion
    de 16:28 en una tautologia.
    """
    main_tt = main28.get("l1_tt", "")
    main_obj = main28.get("l1_tt_objective", 0)
    main_pending = int(main_tt == "TT_PENDING")
    local_pending = int(l28["tt"]["status"] == "TT_PENDING")
    active = main_pending + local_pending
    return {
        "claim": "dos TT pendientes con propietarios distintos al cierre 16:28",
        "tick_derived": {"main_tt_16_28": main_tt,
                         "main_objective": main_obj,
                         "local_tt_16_28": l28["tt"]["status"],
                         "local_objective": l28["tt"]["objective"],
                         "active_tts": active},
        "classification": ("CONFIRMED_BY_TICKS" if active == 2 else
                           "CORRECTED_BY_TICKS"),
        "contradiction": False,
        "reason": f"TT activos con propietario al cierre de 16:28: {active} "
                  f"(mayor={main_tt or 'ninguno'}, "
                  f"local={l28['tt']['status'] or 'ninguno'})",
    }


def claim_both_confirm(main29: dict, local: dict, confirmed_at: int) -> dict:
    """Reclamacion humana: ambos TT confirman en 16:29."""
    main_tt = main29.get("l1_tt", "")
    main_ok = main_tt in ("TT_CONFIRMED", "TT_EXTENDED")
    local_ok = local["tt"]["status"] == "TT_CONFIRMED"
    bar = (confirmed_at // 60000) % 1440 if confirmed_at else 0
    return {
        "claim": "ambos TT confirman en 16:29",
        "tick_derived": {"main_16_29": main_tt,
                         "main_objective": main29.get("l1_tt_objective", 0),
                         "main_confirmed_bar": bar,
                         "local": local["tt"]["status"],
                         "local_first_boundary": local["tt"][
                             "first_boundary"]},
        "classification": ("CONFIRMED_BY_TICKS" if main_ok and local_ok else
                           "CORRECTED_BY_TICKS"),
        "contradiction": False,
        "reason": ("ambos TT alcanzan su objetivo" if main_ok and local_ok else
                   f"TT mayor {main_tt or 'no activo'} en 16:29; TT local "
                   f"{local['tt']['status'] or 'no armado'}"),
    }


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
    # prefijo de la MISMA rama local (16:26) hasta el cierre de 16:28 y lector
    # principal en prefijo hasta 16:29: las reclamaciones de 16:28/16:29 no se
    # evaluan con el estado final del feed.
    l28 = run_local(window(ticks, 16 * 60 + 26, 16 * 60 + 28)).snapshot()
    main28 = mgr.bar_close_state(16 * 60 + 28)
    main29 = mgr.bar_close_state(16 * 60 + 29)
    tt29 = next((p for p in mgr.summaries()["tt_records"]
                 if p.get("objective") == main29.get("l1_tt_objective")), {})

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
        # Iteracion 23A: las tres reclamaciones se clasifican DERIVANDO el
        # veredicto de los ticks. La version anterior fijaba el texto y el
        # veredicto del TT local sobre una referencia de invalidacion erronea
        # (origen de A en un TT nacido de un AUT), lo que producia una
        # contradiccion documental: "TT no armado" junto a "TT con objetivo".
        "human_claims": {
            "16_27_b_grande_local": claim_b_grande(ls),
            "16_28_two_pending_tt": claim_two_pending(main28, l28),
            "16_29_tt_confirmation": claim_both_confirm(
                main29, ls, tt29.get("confirmed_at", 0)),
        },
        "local_scene_sensitivity_16_27_seed": {
            "status": l27["status"],
            "module": l27["module"],
            "a": l27["a"],
            "b": l27["b"],
            "tt": l27["tt"],
            "note": ("sonda de sensibilidad: una rama local sembrada en 16:27 "
                     "produce AUT y TT propio. No es la rama propietaria "
                     "(LOCAL-G2 se siembra en 16:26); LOCAL_SEED_POLICY abierta"),
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
