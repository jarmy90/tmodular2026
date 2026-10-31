# REGISTRO DE CAMBIOS — ITERACIÓN 11

Sólo se modificó el intérprete de referencia, sus pruebas y su documentación.
**No** se modificó el árbol normativo, ningún golden humano ni ningún motor oficial.

| Archivo | Acción | Motivo |
|---|---|---|
| `05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py` | MODIFIED | rama de gap v2.19; TT; CUT; limpieza B en AUT directo; `prev_price` |
| `04_CONCEPT_TESTS/run_core_tests.py` | MODIFIED | helper `_gap_ok`; T-015 verifica secuencia v2.19 |
| `04_CONCEPT_TESTS/run_iteration_09_tests.py` | MODIFIED | CUT-01..CUT-04 |
| `04_CONCEPT_TESTS/run_iteration_10_tests.py` | MODIFIED | GAP-03/03b/05 reescritos; GAP-06..09 |
| `04_CONCEPT_TESTS/run_iteration_11_tests.py` | CREATED | TT-01..TT-12 |
| `04_CONCEPT_TESTS/run_full_feed.py` | MODIFIED | TT fuera de `not_implemented`; ancla TT |
| `09_OPEN_RULES/OPEN_RULES_ITERACION_11.md` | CREATED | sustituye al archivo de la iteración 07 |
| `08_TREE_PYTHON_COMPARISON/TREE_PYTHON_MATRIX_ITER11.csv` | CREATED | equivalencia árbol-Python |
| `10_REPORTS/AUDITORIA_ITERACION_11.md` | CREATED | informe de auditoría |
| `10_REPORTS/CHECKPOINT_11.md` | CREATED | checkpoint técnico |

## Detalle semántico

### Gap (v2.19)

Antes:

```text
apertura no plana -> 2 IMPOSSIBLE_NO_FLAT -> MODULE_BY_DISCARD -> A CONTRARY_MOVE_PENDING
```

Ahora:

```text
apertura no plana -> 2 IMPOSSIBLE_NO_FLAT
                  -> GAP_IMPLICIT_SEQUENCE (A Grande, B Grande, A usada como tendencia)
                  -> GAP_IMPLICIT_NEW_ONE (origen = OPEN, st = kt = primer tick)
```

### TT (v2.6 / v2.7)

```text
AUT (por B o directo por A) -> TT_PENDING (objetivo = final_A +/- modulo)
primer tick que alcanza el objetivo -> TT_CONFIRMED
continuacion -> TT_EXTENDED (extremo real)
final_A tocado antes -> TT_FAILED (+ OPEN_RULE_BLOCK por Q-CYCLE-1)
```

### CUT (v2.13 §6)

```text
C > final real de A -> CUT_CONFIRMED (+ OPEN_RULE_BLOCK por el reset pendiente)
```

## Nota de integridad

El árbol `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md` no fue modificado.
Los intérpretes históricos (`tm_reference_interpreter_v1.py`, `..._ab_candidate.py`,
`..._bg_aut.py`) y el motor R5 no fueron modificados.
