from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out_v075_audit2"


def load(name: str) -> dict:
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def main() -> int:
    a00 = load("A00_Resumen.json")
    a02 = load("A02_RegresionTramoComun.json")
    a08 = load("A08_LecturasGolden.json")
    a09 = load("A09_R0062.json")
    a11 = load("A11_PlanoGap.json")
    a13 = load("A13_Invariantes.json")
    a15 = load("A15_ResumenCobertura.json")
    a22 = load("A22_FTEstados.json")
    p00 = load("P00_PrefijosResumen.json")
    p03 = load("P03_R0062Prefijos.json")

    golden_fail = [row["bar_time"] for row in a08["rows"] if not int(row["cumple"])]
    gap_false = [row["bar_time"] for row in a11["failures"] if row["esperado"] == "PLANO_NO_GAP"]
    open_rules = a13["motor"]["pending"]
    coverage = a15["motor"]
    invariants_ok = {
        key: value
        for key, value in a13.items()
        if isinstance(value, bool)
    }

    verdicts = {
        "PACKAGE_READY": True,
        "PREFIX_INVARIANCE_READY": p00["failures"] == 0 and p00["cutoffs"] == 3327,
        "CAUSAL_ENGINE_READY": all(
            [
                a13["event_id_append_only"],
                a13["sequence_id_real"],
                a13["knowledge_time_valido"],
                p00["failures"] == 0,
            ]
        ),
        "GEOMETRY_REGRESSION_READY": a02["pass"] and a09["pass"],
        "CANONICAL_GOLDEN_READY": a08["mismatch"] == 0,
        "PLANO_GAP_READY": len(gap_false) == 0,
        "FT_FINAL_STATE_READY": a22["canonical"] == a22["ft_patterns"],
        "END_FEED_INTEGRITY_READY": a13["unexplained_structural_moves_sin_pendiente"] == 0,
        "FUNCTIONAL_COVERAGE_COMPLETE": coverage["causal_functional_count"]
        == coverage["structural_swing_count"],
        "OWNER_COVERAGE_COMPLETE": coverage["uncovered_tick_count"] == 0,
        "OPEN_RULES_PRESENT": len(open_rules) > 0,
        "AFS2_EXPERIMENTAL_READY": False,
        "AFS2_PRODUCTION_READY": False,
    }
    blocking = []
    if golden_fail:
        blocking.append(
            {
                "id": "GOLDEN",
                "severity": "ALTA",
                "bars": golden_fail,
                "detail": f"El motor no reproduce {len(golden_fail)} de 8 lecturas humanas 16:15-16:22.",
                "evidence": "A08_LecturasGolden.json",
            }
        )
    if gap_false:
        blocking.append(
            {
                "id": "GAP",
                "severity": "ALTA",
                "bars": gap_false,
                "detail": f"{len(gap_false)} GAP espurios con |gap| < 0.25.",
                "evidence": "A11_PlanoGap.json",
            }
        )
    if a13["unexplained_structural_moves_sin_pendiente"]:
        blocking.append(
            {
                "id": "FIN_FEED",
                "severity": "ALTA",
                "count": a13["unexplained_structural_moves_sin_pendiente"],
                "detail": "Movimientos estructurales no explicados sin PENDIENTE_POR_REGLA.",
                "evidence": "A13_Invariantes.json",
            }
        )
    if a22["canonical"] != a22["ft_patterns"]:
        blocking.append(
            {
                "id": "FT",
                "severity": "ALTA",
                "canonical": a22["canonical"],
                "total": a22["ft_patterns"],
                "detail": "Estados finales FT no canonicos; el motor usa CONFIRMADO.",
                "evidence": "A22_FTEstados.json",
            }
        )
    cli = a02.get("cli_con_barras_completas", {})
    if cli.get("events") != a02.get("events_base") or cli.get("gap_16_20"):
        blocking.append(
            {
                "id": "CLI_BARRAS",
                "severity": "MEDIA",
                "events": cli.get("events"),
                "expected": a02.get("events_base"),
                "detail": "Con barras completas el CLI produce GAP espurio en 16:20 y 874 eventos.",
                "evidence": "A02_RegresionTramoComun.json",
            }
        )
    if coverage["causal_functional_count"] != coverage["structural_swing_count"]:
        blocking.append(
            {
                "id": "COBERTURA_FUNCIONAL",
                "severity": "MEDIA",
                "covered": coverage["causal_functional_count"],
                "total": coverage["structural_swing_count"],
                "detail": "Cobertura funcional causal incompleta.",
                "evidence": "A15_ResumenCobertura.json",
            }
        )
    if coverage["uncovered_tick_count"]:
        blocking.append(
            {
                "id": "OWNER",
                "severity": "MEDIA",
                "uncovered": coverage["uncovered_tick_count"],
                "total": coverage["tick_count"],
                "detail": "Ticks sin owner funcional.",
                "evidence": "A15_ResumenCobertura.json",
            }
        )
    if open_rules:
        blocking.append(
            {
                "id": "REGLAS_ABIERTAS",
                "severity": "MEDIA",
                "rules": open_rules,
                "detail": "Reglas TM abiertas; no cerrar por inferencia.",
                "evidence": "A13_Invariantes.json",
            }
        )

    readiness = {
        "audit": "v075_audit2",
        "motor_version": a00["version"],
        "overall": "AUDITORIA_COMPLETA_NO_APTO_AFS2_PRODUCCION",
        "verdicts": verdicts,
        "headline": {
            "feed_ticks": a00["feed"]["nuevo_filas"],
            "readings": a00["motor"]["readings"],
            "events": a00["motor"]["events"],
            "movements": a00["motor"]["movements"],
            "prefix_cutoffs": p00["cutoffs"],
            "prefix_failures": p00["failures"],
            "r0062_cutoffs": p00["r0062_cutoffs"],
            "r0062_failures": p00["r0062_failures"],
            "golden_match": f"{a08['match']}/{a08['bars']}",
            "gap_false": len(gap_false),
            "ft_canonical": f"{a22['canonical']}/{a22['ft_patterns']}",
            "unexplained": a13["unexplained_structural_moves_sin_pendiente"],
            "functional_coverage": f"{coverage['causal_functional_count']}/{coverage['structural_swing_count']}",
            "owner_uncovered": coverage["uncovered_tick_count"],
        },
        "blocking_findings": blocking,
        "invariants": invariants_ok,
        "rule_freezes": {
            "motor_immutable": True,
            "tests_immutable": True,
            "no_new_version": True,
            "no_afs2_development": True,
        },
        "evidence": {
            "feed": "A01_FeedAuditoria.json",
            "regression": "A02_RegresionTramoComun.json",
            "r0062": "A09_R0062.json",
            "prefixes": "P00_PrefijosResumen.json",
            "golden": "A08_LecturasGolden.json",
            "gap": "A11_PlanoGap.json",
            "coverage": "A15_ResumenCobertura.json",
            "ft": "A22_FTEstados.json",
            "invariants": "A13_Invariantes.json",
        },
    }
    (OUT / "R00_Readiness.json").write_text(
        json.dumps(readiness, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(readiness["verdicts"], ensure_ascii=False, indent=2))
    print(readiness["overall"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
