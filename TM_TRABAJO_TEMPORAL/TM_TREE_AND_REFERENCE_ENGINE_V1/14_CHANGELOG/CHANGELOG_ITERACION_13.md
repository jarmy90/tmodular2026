# REGISTRO DE CAMBIOS — ITERACIÓN 13

| Archivo | Acción | Motivo |
|---|---|---|
| `TM_CANON_ACTIVO/01_ARBOL/TM_PATCH_CANONICO_v2_20_PLANO_Y_CUT.md` | CREATED | frontera de plano, cierre de Q-CUT, separación cierre/rotación, métricas |
| `05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py` | MODIFIED | campos `cycle_closed_at_tt`, `cycle_rotation_committed_at`, `cycle_rotation_via`; `cycle_closure` en `summary`; tt/ft/cut en `_snapshot` |
| `04_CONCEPT_TESTS/run_iteration_12_tests.py` | MODIFIED | FT-03 y FT-06 reclasificadas como PROVISIONAL |
| `04_CONCEPT_TESTS/run_iteration_13_tests.py` | CREATED | GP-01..GP-11 (gap+TT, estados heredados, plano, cierre/rotación) |
| `04_CONCEPT_TESTS/run_block_comparison.py` | CREATED | comparación humana de los cuatro bloques |
| `04_CONCEPT_TESTS/run_rotation_audit.py` | CREATED | auditoría de rotaciones por causa |
| `09_OPEN_RULES/OPEN_RULES_ITERACION_13.md` | CREATED | Q-CUT cerrada; nuevas abiertas |
| `10_REPORTS/AUDITORIA_ITERACION_13.md` | CREATED | informe completo con primer error por bloque |
| `10_REPORTS/CHECKPOINT_13.md` | CREATED | checkpoint |
| `08_TREE_PYTHON_COMPARISON/TREE_PYTHON_MATRIX_ITER13.csv` | CREATED | matriz actualizada |

## Sin cambios

- Árbol v2.19 (hash intacto).
- Tickfeed y lecturas humanas (hashes intactos).
- Motores históricos `v1`, `ab_candidate`, `bg_aut` y R5.

## Corrección de nomenclatura

Se elimina «ciclos» como nombre de la métrica. El feed informa `cycle_rotations`,
`cycles_closed_by_tt`, `cycles_started_by_gap`, `cycles_started_by_c_trend`, `initial_cycles`
e `incomplete_or_archived_cycles`, y afirma explícitamente que las 47 rotaciones **no** son
ciclos TM validados.
