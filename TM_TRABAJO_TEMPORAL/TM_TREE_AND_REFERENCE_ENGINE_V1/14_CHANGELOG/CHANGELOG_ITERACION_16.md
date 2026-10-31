# CHANGELOG — ITERACION 16

## Motor `05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py`

- Cabecera sustituida por la tabla de estado real
  (IMPLEMENTADO_CANONICO / IMPLEMENTADO_PROVISIONAL / OPEN_RULE_BLOCK /
  NO_IMPLEMENTADO).
- `PROVISIONAL_INTERNAL_RATIO = 35` como constante documentada; eliminados los
  literales `35` del codigo.
- `n_bar` y `a_origin_reason`: trazabilidad de la vela de nacimiento del nuevo 1
  y del motivo de nacimiento de A.
- `tt_archived`: el TT de un ciclo archivado queda congelado para FT y
  trazabilidad; no se extiende ni arbitra en la estructura nueva (RC-2).
- `_rotate_cycle_after_tt`: solo rota con TT cerrado o con nuevo 1 de
  `C_USED_AS_TREND` (RC-1). Eliminada la rotacion administrativa por `NEW_ONE`.
- A principal desde un nuevo 1 nacido de gap: se abre solo en una vela posterior
  a la del nuevo 1 y con retroceso funcionalmente claro
  (`MAIN_NEW_ONE_RETRACE`).
- Snapshot ampliado con `ft_origin`, `ft_dir`, `ft_extreme`.
- Intentos RC-3 y RC-4 aplicados y revertidos en la misma iteracion por romper
  anclas ya validadas; el motivo queda en el codigo y en la auditoria.

## Pruebas `04_CONCEPT_TESTS`

- `run_core_tests.py`: eliminado `_gap_ok` y su fallback historico; T-015
  endurecida; campo `classification` en CSV.
- `run_ab_candidate_tests.py`: campo `classification` y clasificacion explicita
  de A-01, BG-15 y BG-16 como provisionales.
- `run_iteration_10_tests.py`: GAP-05 corregida conforme a v005 16:25-16:26 (el
  nuevo 1 de gap no rota sin TT).
- `run_iteration_16_all.py`: nuevo agregador con binding obligatorio de motor y
  autoridad estructurada.
- `run_human_segments_16.py`: nuevo comparador de segmentos humanos
  16:15-16:32 con metricas corregidas.
- `tm_reader_guard.py`: ya existia; ahora es obligatorio en las 8 suites.

## Resultados

```text
pruebas           146/146 PASS
CANONICAL_PASS    104
PROVISIONAL        39
OPEN_RULE_BLOCK     3
anclas humanas    6/19
bloques           1/4
```
