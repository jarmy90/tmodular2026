from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "out_v075_audit2"


def load(name: str) -> dict:
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def test_feed_common_exact_and_sequence_offset() -> None:
    feed = load("A01_FeedAuditoria.json")
    common = feed["tramo_comun"]
    assert common["old_count"] == common["new_common_count"] == 11120
    assert common["sequence_offsets"] == [1145]
    assert common["mismatch_count"] == 0
    assert common["pass"] is True


def test_regression_common_exact() -> None:
    regression = load("A02_RegresionTramoComun.json")
    assert regression["pass"] is True
    assert regression["event_compare"]["mismatch_count"] == 0
    assert regression["reading_compare"]["mismatch_count"] == 0
    assert regression["cli_con_barras_completas"]["events"] == 874
    assert regression["cli_con_barras_completas"]["gap_16_20"]


def test_r0062_maps_to_r0064_and_geometry_is_exact() -> None:
    r0062 = load("A09_R0062.json")
    assert r0062["full"] == "R0064"
    assert r0062["pass"] is True
    assert r0062["eventos_base"] == r0062["eventos_full"] == 26
    assert r0062["eventos_diff"] == []
    assert r0062["critico"]["module"] == "29667.30->29602.10 X=65.20"
    assert r0062["critico"]["tt_target"] == "29615.20"


def test_prefix_matrix_is_complete_and_clean() -> None:
    prefixes = load("P00_PrefijosResumen.json")
    assert prefixes["cutoffs"] == 3327
    assert prefixes["pass"] == 3327
    assert prefixes["failures"] == 0
    assert prefixes["r0062_cutoffs"] == 1782
    assert prefixes["r0062_failures"] == 0
    assert prefixes["category_counts"]["cierre_vela"] == 75
    assert prefixes["category_counts"]["aleatorio_500"] == 500


def test_golden_keeps_known_canonical_mismatches_visible() -> None:
    golden = {row["bar_time"]: row for row in load("A08_LecturasGolden.json")["rows"]}
    assert int(golden["16:15"]["cumple"]) == 0
    assert int(golden["16:18"]["cumple"]) == 1
    assert "GAP" in golden["16:16"]["observado"]
    assert "AUT=16:22:05.219" in golden["16:22"]["observado"]
    assert "TT=16:22:05.219" in golden["16:22"]["observado"]
    assert int(golden["16:22"]["cumple"]) == 0


def test_gap_rule_threshold_failures() -> None:
    gap = load("A11_PlanoGap.json")
    assert gap["false_gap"] == 12
    assert {"16:16", "16:20", "16:27"} <= {row["bar_time"] for row in gap["failures"]}
    assert all(row["abs_gap"] < 25 for row in gap["failures"])


def test_ft_states_are_not_canonical_yet() -> None:
    ft = load("A22_FTEstados.json")
    assert ft["ft_patterns"] == 37
    assert ft["canonical"] == 0
    assert all(row["final_status"] == "CONFIRMADO" for row in ft["non_canonical"])


def test_coverage_and_owner_findings() -> None:
    coverage = load("A15_ResumenCobertura.json")
    assert coverage["motor"]["structural_swing_count"] == 2238
    assert coverage["motor"]["causal_functional_count"] == 2166
    assert coverage["swings"]["causal_functional_uncovered"] == 72
    assert coverage["owner"]["uncovered"] == 434
    assert coverage["owner"]["reasons"] == {
        "PRE_LECTURA": 6,
        "PRECIO_FUERA_RANGO_ACTIVO": 421,
        "SIN_LECTURA_ACTIVA": 7,
    }


def test_end_feed_integrity_is_explicitly_not_ready() -> None:
    invariants = load("A13_Invariantes.json")
    assert invariants["unexplained_structural_moves_sin_pendiente"] == 72
    assert invariants["integridad_fin_feed"] is False
    assert invariants["plano_gap_regla_canonica"] is False
    assert invariants["event_id_append_only"] is True
    assert invariants["knowledge_time_valido"] is True


def test_readiness_verdicts_are_separated() -> None:
    readiness = load("R00_Readiness.json")
    verdicts = readiness["verdicts"]
    assert verdicts["PREFIX_INVARIANCE_READY"] is True
    assert verdicts["GEOMETRY_REGRESSION_READY"] is True
    assert verdicts["CAUSAL_ENGINE_READY"] is True
    assert verdicts["CANONICAL_GOLDEN_READY"] is False
    assert verdicts["PLANO_GAP_READY"] is False
    assert verdicts["FT_FINAL_STATE_READY"] is False
    assert verdicts["END_FEED_INTEGRITY_READY"] is False
    assert verdicts["AFS2_PRODUCTION_READY"] is False
    assert readiness["overall"] == "AUDITORIA_COMPLETA_NO_APTO_AFS2_PRODUCCION"
