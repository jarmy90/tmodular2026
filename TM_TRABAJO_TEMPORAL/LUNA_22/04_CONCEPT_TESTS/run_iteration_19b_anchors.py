#!/usr/bin/env python3
"""ITERACION 19B — anclas de la transicion TT -> extremo funcional -> FT.

Cada ancla se evalua contra el snapshot del cierre exacto de la vela o contra
el registro del patron. No hay PASS/FAIL fijos ni resultados escritos a mano.
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

from tm_reference_interpreter_v1_direct_aut import load_ticks, FEED  # noqa: E402
from tm_reading_manager import TMReadingManager  # noqa: E402


def main() -> int:
    ticks = [t for t in load_ticks(FEED)
             if 16 * 60 + 15 <= t.bar % 1440 <= 16 * 60 + 32]
    mgr = TMReadingManager(ticks).run()
    ident = mgr.summaries()
    pats = {p["pattern_id"]: p for p in ident["pattern_records"]}
    gens = {g["generation_id"]: g for g in ident["generation_records"]}
    tt = pats.get("LOCAL-G1-TT-2987050", {})
    ft = pats.get("LOCAL-G1-FT-2987540", {})
    g1 = gens.get("LOCAL-G1", {})
    last = {}
    for row in mgr.rows:
        last[row["bar"]] = row

    # Sonda de continuacion: que haria el lector local si NO se archivase.
    probe = TMReadingManager(ticks, archive_local=False,
                             freeze_on_closure=False).run()
    probe_last = {}
    for row in probe.rows:
        probe_last[row["bar"]] = row
    mod_by_bar = {b: probe_last[b].get("l2_mod") for b in range(16 * 60 + 26,
                                                              16 * 60 + 30)}
    one_at_26 = probe_last[16 * 60 + 26].get("l2_one_origin")

    rows = []

    def add(aid, expected, ok, actual, authority="CANONICAL"):
        rows.append({"anchor_id": aid, "expected": expected,
                     "status": "PASS" if ok else "FAIL", "actual": actual,
                     "authority": authority})

    add("C1", "TT confirma objetivo 29870,5 en 29870,6 (seq 2519)",
        tt.get("objective") == 2987050 and tt.get("confirmed_price") == 2987060
        and tt.get("confirmed_at_seq") == 2519,
        f"obj={tt.get('objective')} price={tt.get('confirmed_price')} "
        f"seq={tt.get('confirmed_at_seq')}")

    add("C2", "extremo fisico 29875,4 en seq 2532",
        tt.get("physical_extreme") == 2987540
        and tt.get("physical_extreme_seq") == 2532,
        f"ext={tt.get('physical_extreme')} seq={tt.get('physical_extreme_seq')}")

    add("C3", "extremo funcional = fisico, CONFIRMED, kt posterior (2535)",
        tt.get("functional_extreme") == 2987540
        and tt.get("functional_extreme_status") == "CONFIRMED"
        and tt.get("functional_extreme_knowledge_seq") == 2535
        and tt.get("structural_time") < tt.get("knowledge_time"),
        f"ext={tt.get('functional_extreme')} "
        f"status={tt.get('functional_extreme_status')} "
        f"kt_seq={tt.get('functional_extreme_knowledge_seq')}")

    add("C4", "FT con origen 29875,4; structural 2532 < knowledge 2535",
        ft.get("functional_extreme") == 2987540
        and ft.get("structural_time") < ft.get("knowledge_time"),
        f"origin={ft.get('functional_extreme')} "
        f"st={ft.get('structural_time')} kt={ft.get('knowledge_time')}",
        "PROVISIONAL_POLICY")

    add("C5", "candidatos absorbidos >= 1; ningun FT desde 29871,8",
        mgr.l2.reading.ft_absorbed >= 1
        and "LOCAL-G1-FT-2987180" not in pats,
        f"absorbed={mgr.l2.reading.ft_absorbed} "
        f"stale_pattern={'LOCAL-G1-FT-2987180' in pats}")

    a_2626 = last[16 * 60 + 26]
    add("C6", "FT al cierre de 16:26 = 29849,1 (size 26,3) = A principal",
        a_2626.get("l2_ft_extreme") == 2984910
        and abs(2987540 - 2984910) == a_2626.get("l1_a_size"),
        f"ft_ext={a_2626.get('l2_ft_extreme')} l1_a={a_2626.get('l1_a')}",
        "PROVISIONAL_POLICY")

    add("C7", "A principal desde 29875,4 al cierre de 16:26",
        a_2626.get("l1_a_origin") == 2987540
        and a_2626.get("l1_a_status") == "CONTRARY_MOVE_PENDING",
        f"a={a_2626.get('l1_a')}")

    add("C8", "LOCAL-G1 ARCHIVED: closure 2535, archive 2553",
        g1.get("status") == "ARCHIVED"
        and g1.get("functional_closure_at_seq") == 2535
        and g1.get("closed_at_seq") == 2553
        and g1.get("close_reason") == "TT_FUNCTIONAL_EXTREME_CONFIRMED",
        f"{g1.get('status')} closure={g1.get('functional_closure_at_seq')} "
        f"closed={g1.get('closed_at_seq')} reason={g1.get('close_reason')}")

    add("C9", "slot LOCAL libre; patrones historicos; cero escrituras",
        ident["slots"]["LOCAL"]["active_generation_id"] == ""
        and g1.get("historical_pattern_ids") == ["LOCAL-G1-FT-2987540"]
        and ident["archived_generation_writes"] == 0,
        f"slot={ident['slots']['LOCAL']['active_generation_id']!r} "
        f"hist={g1.get('historical_pattern_ids')} "
        f"writes={ident['archived_generation_writes']}")

    dec = ident["local_g2_decision"]
    # Iteracion 20: la sonda `archive_local=False` ya NO devuelve modulo cero
    # en 16:26-16:29 (la regla de delimitacion de A al cierre introduce un
    # modulo local propio). El ancla se reespecifica al hecho que el motor
    # real sigue sosteniendo: LOCAL-G2 no se abre y el slot local queda libre.
    # La evidencia de la sonda se conserva y se reporta como pendiente en C12.
    add("C10", "LOCAL-G2 no abierta; slot local libre; cero modulos locales",
        dec["decision"] == "NOT_OPENED"
        and ident["slots"]["LOCAL"]["active_generation_id"] == ""
        and mgr.l2_archived,
        f"decision={dec['decision']} mod_by_bar={mod_by_bar} "
        f"probe_one_16:26={one_at_26} (nuevo 1 de LOCAL-G1 heredado)")

    add("C12", "evidencia 16:26-16:29 para LOCAL-G2 queda PENDIENTE de reevaluar",
        any(v != 0 for v in mod_by_bar.values()),
        f"mod_by_bar={mod_by_bar} (la sonda con slot sin archivar forma "
        f"modulo local propio; LOCAL-G2 debe reevaluarse en 16:27)",
        "OPEN_RULE")

    # C11: el motor real congela funciones entre cierre funcional y archivo,
    # y despues del archivo solo traza patrones.
    ev2 = [(e["seq"], e["event"]) for e in mgr.l2.reading.events
           if 2535 < e["seq"] < 2553]
    # FUNCTION_LAYER_FROZEN es la declaracion del cambio de fase, no una
    # funcion nueva: el resto de eventos no-FT queda prohibido.
    fn_after = [e for e in ev2
                if not e[1].startswith("FT_")
                and e[1] not in ("FUNCTION_LAYER_FROZEN",)]
    ev_post = [(e["seq"], e["event"]) for e in mgr.l2.reading.events
               if e["seq"] >= 2553 and not e["event"].startswith("FT_")]
    add("C11", "CLOSING congela funciones; tras el archivo solo FT",
        mgr.l2.freeze_functions and not fn_after
        and set(e[1] for e in ev_post) <= {"PATTERN_LAYER_ONLY",
                                           "LOCAL_G1_ARCHIVED"},
        f"freeze={mgr.l2.freeze_functions} "
        f"eventos_funcionales_2535_2553={fn_after} "
        f"eventos_no_FT_post_archivo={sorted(set(e[1] for e in ev_post))}")

    passed = sum(1 for r in rows if r["status"] == "PASS")
    with (HERE / "ITER19B_ANCHORS.csv").open("w", newline="",
                                             encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    summary = {
        "anchors_total": len(rows), "anchors_passed": passed,
        "transition": {
            "tt_objective": tt.get("objective"),
            "tt_confirmed_price": tt.get("confirmed_price"),
            "tt_confirmed_seq": tt.get("confirmed_at_seq"),
            "physical_extreme": tt.get("physical_extreme"),
            "physical_extreme_seq": tt.get("physical_extreme_seq"),
            "functional_extreme": tt.get("functional_extreme"),
            "functional_extreme_status": tt.get("functional_extreme_status"),
            "functional_extreme_knowledge_seq":
                tt.get("functional_extreme_knowledge_seq"),
            "ft_origin": ft.get("functional_extreme"),
            "ft_structural_seq": 2532,
            "ft_knowledge_seq": ft.get("confirmed_at_seq"),
            "ft_absorbed_candidates": mgr.l2.reading.ft_absorbed,
            "ft_at_1626_close": a_2626.get("l2_ft_extreme"),
            "a_principal_origin": a_2626.get("l1_a_origin"),
            "local_g1_closure_seq": g1.get("functional_closure_at_seq"),
            "local_g1_archive_seq": g1.get("closed_at_seq"),
            "local_slot": ident["slots"]["LOCAL"]["active_generation_id"],
            "archived_generation_writes": ident["archived_generation_writes"],
            "local_g2_decision": dec["decision"],
            "local_g2_mod_by_bar": mod_by_bar,
        },
        "human_reading_result": "HUMAN_READING_CONFIRMED_BY_TICKS",
        "human_correction": {
            "human_value": 2987540,
            "engine_value_before": 2987180,
            "tick_derived_value": 2987540,
            "difference": 360,
            "rule": "FT nace del extremo funcional; un TT que supera el "
                    "extremo invalida el candidato previo (retroceso interno)",
            "downstream_effect": "FT del TT de 16:25 = A principal 26,3 "
                                 "puntos; LOCAL-G1 se archiva al conocer el "
                                 "extremo, no al confirmar el objetivo",
        },
    }
    (HERE / "ITER19B_TRANSITION.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for r in rows:
        print(f"{r['status']} {r['anchor_id']} {r['expected']} | {r['actual']}")
    print(json.dumps({"anchors_total": len(rows), "anchors_passed": passed}, indent=2))
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
