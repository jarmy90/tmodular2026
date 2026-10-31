# -*- coding: utf-8 -*-
"""Component reuse matrix for R5 (CSV)."""
from __future__ import annotations

import csv
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "FREEBUFF_COMPONENT_REUSE_MATRIX_v219.csv"

ROWS = [
    ("load_feed", "ingesta y validación de columnas", "286-323", "KEEP", "Aritmética entera, orden por sequence_id, detección de duplicados"),
    ("Pt / Bar", "estructuras de tick y vela", "124-146", "KEEP", "Sin floats; base de todo el motor"),
    ("price_i / price_s / ms_to_*", "normalización y formato", "67-122", "KEEP", "Precios en centésimas y tiempos deterministas"),
    ("feed_chunk (orden y causalidad)", "guardia de orden estricto", "3418-3425", "KEEP", "Rechaza seq/tiempo no creciente"),
    ("serialize_state / restore_state", "checkpoint", "3480-3490", "KEEP", "Necesario para prefijos y reproducibilidad"),
    ("_emit / esquema de eventos", "telemetría causal", "752-827", "KEEP_WITH_ADAPTER", "Añadir capa función/patrón/evento y flag implicit"),
    ("_record_knowledge / _snapshot_state", "auditoría por tick", "1584-1622 / 2610-2677", "KEEP", "Única salida válida para comparar estado"),
    ("write_outputs / serializadores", "CSV/JSON de salida", "2117-2350", "KEEP", "Formato estable para comparadores"),
    ("compare_prefix / run_prefix_matrix", "verificación de causalidad", "2391-2450", "KEEP", "Ya demuestra 262/262"),
    ("compare_v005 / compare_golden", "comparadores", "repro/*", "KEEP_WITH_ADAPTER", "Golden v005 es parcial; no convertirlo en total"),
    ("BigBTracker", "100 %, 127 %+0,25, AUT estricto, C", "445-496", "KEEP", "28/28 tests; matemática correcta"),
    ("local_two_gate", "puerta ordenada de 2", "555-558", "KEEP", "Gap/cola/dirección/tamaño en orden"),
    ("strict_crosses / cut_crosses", "cruces estrictos", "498-506", "KEEP", "Igualdad no cruza"),
    ("_two_impossible", "rama de módulo por descarte", "2988-3004", "KEEP_WITH_ADAPTER", "Concepto correcto; falta rama de fallo de 3"),
    ("_schedule_gap (evento)", "detección de gap", "1540-1558", "KEEP_WITH_ADAPTER", "Conservar detección; añadir resolución"),
    ("_maybe_aut", "AUT por B", "918-940", "KEEP_WITH_ADAPTER", "Quitar a_size>=6,00 y separar de B Grande"),
    ("MAX_ACTIVE / archivado", "límite de 3 lecturas", "35, 1520-1535", "KEEP_WITH_ADAPTER", "Mantener tope; cambiar criterio de dominancia"),
    ("MovementBuilder", "constructor de movimientos", "333-390", "REPLACE_SEMANTICS", "No puede ser la unidad de decisión; usable solo como detector auxiliar de swings"),
    ("build_movements", "movimientos de todo el feed", "392-407", "SHADOW_ONLY", "Solo para comparación retrospectiva"),
    ("Reading (dataclass)", "modelo de lectura", "162-284", "REFACTOR", "Separar función, patrón, evento y referencias por función"),
    ("_create_reading", "creación de lectura", "857-897", "REPLACE_SEMANTICS", "Nace MODULE cerrada; debe nacer ONE_CANDIDATE"),
    ("_update", "máquina por movimiento", "1060-1381", "REPLACE_SEMANTICS", "Decide al cerrar movimiento; debe decidir por tick"),
    ("_open_candidate", "apertura de lecturas", "1383-1493", "REPLACE_SEMANTICS", "FIRST/A_SIGNIFICATIVA/B_CONFIRMADA/CUT_NEW1 no son funciones canónicas"),
    ("_process_movement", "despacho por movimiento", "1494-1539", "REPLACE_SEMANTICS", "Eliminar como autoridad; conservar solo como evento de swing"),
    ("_process_local_sequence", "máquina de fases local", "3005-3281", "REFACTOR", "Esqueleto de estados útil; fases y umbrales incorrectos"),
    ("_close_candidate_bar", "1 local desde vela cerrada", "2792-2836", "REPLACE_SEMANTICS", "1 = high-low de vela con span>=6; debe ser movimiento direccional"),
    ("_new_local_reading_after_aut", "nuevo 1 tras AUT", "2837-2885", "REPLACE_SEMANTICS", "Cierra y crea lectura; debe transformar con genealogía"),
    ("_reclassify_c_as_new_1", "C como nuevo 1", "2925-2987", "KEEP_WITH_ADAPTER", "Conserva genealogía; falta transition_reason canónico"),
    ("_check_tt", "confirmación TT", "1027-1058", "REPLACE_SEMANTICS", "Solo al cerrar movimiento; debe evaluarse cada tick"),
    ("_check_cut", "CUT primario", "942-970", "REPLACE_SEMANTICS", "Usa a_end +/- 2,00; referencia pendiente Q3"),
    ("_legacy_tick_decision", "tercera autoridad tick", "3330-3417", "SHADOW_ONLY", "Útil como oráculo de comparación; no como ejecutor"),
    ("_shadow_compare", "comparación local/legacy", "3314-3329", "KEEP_WITH_ADAPTER", "Diagnóstico valioso; no arbitra"),
    ("_advance_primary_question", "autoridad de pregunta", "3282-3313", "REFACTOR", "Debe ser la única autoridad y cubrir 2/3/A/B/C"),
    ("_owner", "propietario del tick", "1560-1583", "REFACTOR", "Dominancia por module_size; debe ser por estructura"),
    ("dominant flag", "dominancia", "889, 2705-2712", "REFACTOR", "Bandera única sin genealogía"),
    ("A_SIGNIFICATIVA / A_DESPROPORCIONADA_MODULO", "lecturas por proporción", "1450-1475 / 1533", "DEAD_CODE", "No tienen respaldo en el árbol"),
    ("MIN_MODULE", "mínimo de módulo para A significativa", "31", "DEAD_CODE", "Solo alimenta la ruta anterior"),
    ("MOVE=600 como umbral de lectura", "mínimo estructural", "22 y usos", "REPLACE_SEMANTICS", "Debe quedar solo para elegibilidad operativa"),
    ("tests BigBTracker", "unit tests de B/AUT", "tests/test_big_b_aut.py", "KEEP", "28/28; conservar"),
    ("tests anchor gates", "anclas de A", "tests/test_anchor_gates.py", "KEEP_WITH_ADAPTER", "Válidos si A se congela correctamente"),
    ("tests post-CUT", "genealogía post-CUT", "tests/test_post_cut_gates.py", "KEEP_WITH_ADAPTER", "Válidos si CUT se redefine"),
    ("tests transformations", "determinismo y no hardcodes", "tests/test_transformations.py", "KEEP", "Guardia constitucional"),
    ("CLI / main", "ejecución", "3547-3579", "KEEP", "Interfaz estable"),
    ("coverage / AFS2", "métricas de cobertura", "1783-1858 / 2451-2555", "UNKNOWN_PENDING_ANALYSIS", "No se evaluó su semántica en esta fase"),
]

with OUT.open("w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["component", "role", "lines_or_path", "classification", "rationale"])
    w.writerows(ROWS)
print("wrote", OUT, len(ROWS), "rows")
