# CASOS VALIDADOS TM

Registro de casos cerrados por autoridad y reproducidos causalmente por el motor.
Cada entrada enlaza la regla, la evidencia cruda y los gates.

---

## CV-001 — 16:23: A Grande bajista → B Grande alcista → C Grande bajista → CUT

- **Autoridad:** Javier (DECISION_AUTORIDAD_16_23_AB_C_CUT_JAVIER.md)
- **Estado:** PASS
- **Oráculos:** a_origin 29850,80 → a_end 29842,80 (a_size 800); b_extreme 29852,60
  (b_size 980, ratio 122,5 %); B Grande seq 1876; extremo final de B seq 1879;
  CUT primer cruce de a_end en seq 2015.
- **Reglas:** B Grande al 100 %; AUT solo por encima de 127 % + 0,25; C solo tras
  B Grande; CUT contra a_end congelado.
- **Evidencia:** `out/GATE_1623_ANCHORS.json`, `out/GATE_1623_EVENTS.csv`,
  `out/GATE_1623_ANCHOR_MUTATIONS.csv`.
- **Gates:** `repro/gate_1623_anchors.py`, `tests/test_anchor_gates.py`.

## CV-002 — POST-CUT: la C Grande que confirma CUT es el nuevo 1 dominante

- **Autoridad:** Javier (DEC-016,
  `DECISION_AUTORIDAD_POST_CUT_C_A_NUEVO_1_JAVIER.md`)
- **Estado:** PASS
- **Regla:** C_GRANDE → CUT_CONFIRMED → C_RECLASSIFIED_AS_NEW_1 → NEW_1_DOMINANT.
  Origen estructural = extremo de B Grande; confirmación = tick CUT.
- **Caso físico:** nuevo 1 bajista desde 29852,60; structural_sequence_id 1879;
  confirmation_sequence_id 2015; parent LR0002; owner LR0003; R0001 archivada con
  DOMINANCE_REPLACED_BY_CUT.
- **Evidencia:** `out/GATE_POST_CUT.json`, `out/GATE_POST_CUT_EVENTS.csv`.
- **Gates:** GATE 5 (`tests/test_post_cut_gates.py`), GATE 6
  (`repro/gate_post_cut.py`).

## CV-003 — 16:24: A Grande → B Grande → AUT bajista → nuevo 1 bajista

- **Autoridad:** Javier (FASE B de la decisión post-CUT)
- **Estado:** PASS
- **Lectura:** apertura con gap (no hay 2); A Grande contraria 29833,30 → 29840,60;
  B Grande bajista; B supera 127 % + 0,25 y confirma AUT bajista; nuevo 1 bajista
  dominante extendido; TT alcista pendiente/no alcanzado.
- **Evidencia:** `out/GATE_POST_CUT.json`, `out/CORE_RAW_OUTPUT.json`.
- **Gate:** GATE 7 (`repro/gate_post_cut.py`).

## CV-004 -- 16:25-16:29: ejecucion y comparacion contra v005

- **Estado:** EJECUTADA CON DIVERGENCIA DOCUMENTADA (MOTOR_DIVERGENT).
- **Resultado:** 9 MATCH, 2 RULE_OPEN, 4 MOTOR_DIVERGENT en 16:15-16:29.
- **Hueco declarado:** TT al 100 % y FT no se emiten en lecturas locales; primer
  tick afectado secuencia 1639 (16:22). Objetivo de R6, no aprobado.
- **Entrada 16:30:** v005 espera 1 bajista; R5 cierra en B_CAND +1.
- **Evidencia:** out/COMPARACION_v005_1615_1629.json, out/TABLA_CAUSAL_1625_1629.csv,
  out/ESTADO_ENTRADA_1630.json, out/STATE_TIMELINE_1615_1629.csv.

## CV-005 -- Gate legacy por firma conductual

- **Autoridad:** DEC-017 (2026-10-29).
- **Estado:** NOT_COMPARABLE (clasificado, no aprobado como equivalencia).
- **Motivo:** legacy fragmenta cada movimiento (86 lecturas); R5 consolida
  genealogia (12). El nombre de lectura deja de ser gate.
- **Sustituto:** firmas de hitos B100/AUT/CUT/TT/FT con precio y secuencia.
- **Evidencia:** out/LEGACY_STRUCTURAL_EQUIVALENCE.json.

## CV-006 -- Traza de estado por tick

- **Estado:** PASS.
- **Datos:** 3538 ticks, max 2 activas, 0 sin dominante, 0 violaciones de ancla,
  42 cambios de funcion, 0 errores.
- **Invariantes:** MULTIPLE_DOMINANT, FIRST_FUNCTION_NOT_1, B_WITHOUT_A_FULL,
  B_BELOW_100_PERCENT, B_NOT_MARKED_GRANDE, B_CAND_AFTER_GRANDE,
  AUT_WITHOUT_STRICT_LIMIT, C_WITHOUT_B_GRANDE, CUT_WITHOUT_CROSS.
- **Evidencia:** out/STATE_TRACE_VALIDATION.json, repro/state_trace.py.
