# TM State Engine v0.7.2 - Changelog

## Objetivo
Corregir la continuidad de un TT ya confirmado: no restaurarlo como `TT_PENDING`, seguir su extremo real, abrir el FT posterior y procesar una lectura local concurrente sin fragmentar TTs autononos.

## Cambios principales

### Estados y semilla
- Añadidos `TT_CONFIRMED`, `TT_EXTENDING`, `POST_TT_FT_WINDOW`, `TT_COMPLETED`.
- `Seed.tt_state` y carga explícita de TT confirmado, TT100 histórico y extremo real.
- `--seed tt` es ambiguo y exige `--seed-state`; se aceptan alias `tt_pending`, `tt_confirmed`, `tt_extending`, `post_tt`.
- Validaciones nuevas: `INVALID_SEED_MISSING_TT100`, `INVALID_SEED_TT100_BEFORE_TARGET`, `INVALID_SEED_REAL_EXTREME`.
- `TT_100_RESTORED` y `TT_REAL_EXTREME_RESTORED` se emiten una sola vez al restaurar, sin recrear el 100 % en ticks posteriores.

### Arquitectura post-TT
- `_post_tt_step` separa tres funciones que ya no se excluyen:
  1. `TRACK_TT_EXTENSION`: actualiza extremo real y emite `TT_REAL_EXTREME_UPDATED`.
  2. `TRACK_FT_FROM_REAL_EXTREME`: abre/confirma/absorbe FT.
  3. `TRACK_LOCAL_CONCURRENT_READING`: mantiene el hijo local.
- La extensión TT se sigue procesando aunque `track_ft=False`, para que una lectura local también actualice su extremo real.
- `_module_step` conserva la rama legacy de hijo dominante y solo bloquea nuevos TT autononos cuando el ancla post-TT es un TT mayor confirmado.
- `_ft_candidate_step` exige módulo local completo (`>= MIN_MODULE_STUDY`) antes de abrir A local.
- El módulo del hijo FT solo se actualiza mientras el hijo sigue en `MODULE`; no se corrompe una lectura local ya iniciada.
- Absorciones FT/TT actualizan Lecturas y Patrones de forma consistente; se limpia `ft_child` y `ft_candidate`.

### Patrones y CSV
- `final_status` obligatorio y coherente en Patrones.
- `_set_pattern_by_id` actualiza estado, `origin_*`, `end_*`, `size` y detalle.
- El FT fija su origen en el extremo real del TT, no en `reading.a_end`.
- Lecturas ampliadas con `parent_tt_id`, `coexisting_function`, `ft_status`, `tt_confirmed`, `tt_100_sequence_id`, `tt_real_extreme_*`, `coverage_role`.
- Siguen siendo exactamente tres CSV por ejecución.

### Cobertura
- `evaluate_coverage` separa `validation` de `TM_COVERAGE_OK`.
- Los swings estructurales no cubiertos generan `UNEXPLAINED_STRUCTURAL_MOVE`, `PENDIENTE_POR_REGLA`, `pending` y `coverage_unresolved`.
- `_covered` usa rangos de lecturas; no hay lista vacía artificial.

### Scheduler
- `post_tt_anchor` se actualiza independientemente de la lectura local activa.
- Se impide que la lectura local desplace al ancla TT.
- Límite de dos lecturas operativas y escala 0/1 validado en cada ejecución.

## Pruebas
- `SELFTEST OK v0.7.2: 15 comprobaciones`.
- `TESTS OK v0.7.2: 16 comprobaciones`:
  - `TEST-SEED-TT-001/002/003`
  - `TEST-POST-TT-001..005`
  - `TEST-CSV-001`
  - `TEST-COVERAGE-001`
  - `TEST-REG-1642-1644`
  - `TEST-REG-1645-1648`
  - metamórficos: precio, tiempo, simetría, número de ticks.

## Resultados
- `v072_regression_1642_1648/v072_1642_*`: 802 ticks, 9 lecturas, 71 eventos, 8 patrones, `active_operational=2`, `pending=[]`, `TM_COVERAGE_OK=true`.
- `v072_regression_1642_1648/v072_1645_*`: 1106 ticks, 6 lecturas, 116 eventos, 8 patrones, `active_operational=2`, `pending=[]`, `TM_COVERAGE_OK=true`.

## Compatibilidad
- No se modificó ni sobrescribió v0.7.1.
- El feed y el árbol v2.14 no se alteran.
- Salida determinista: dos ejecuciones consecutivas producen hashes idénticos en los seis CSV.

## Limitaciones conocidas
- `TT_COMPLETED` y `FT_WINDOW_EXPIRED` están definidos pero no se usan como cierre automático; el final de feed deja el TT en `TT_EXTENDING` para no borrar la extensión real.
- La semántica exacta de `FT_CONFIRMED` (confirmación con el primer tick adverso adicional) es una decisión conservadora; el prompt no fija el número de ticks.
- La lectura local de 16:45 se resuelve con módulo `29745.10 -> 29734.10` (11.00), A `5.20`, TT local `29728.30`; es una lectura completa de escala inferior, no el módulo de referencia `25.30`. No se mezclan niveles, pero la granularidad local sigue siendo una decisión abierta.
- `post_tt_fallido` no tiene regla cerrada; no se inventa.
- v2.13.3 no está disponible físicamente; se usa v2.14 como autoridad.
- Las lecturas manuales de 16:58/16:30 no son causales y no se usan como validación.
