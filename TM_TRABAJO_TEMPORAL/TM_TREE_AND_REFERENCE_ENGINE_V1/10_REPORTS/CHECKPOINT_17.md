# CHECKPOINT 17 — Motor multilectura L1/L2

**Baseline:** `TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT` + `TMReadingManager`
**Pruebas:** 146/146 PASS (104 canónicas, 39 provisionales, 3 open rule)
**Anclas humanas:** 13/19 · bloques: 1/4
**L2 descubierta automáticamente:** SÍ, en seq 1145 (apertura 16:20, sembrada con la vela cerrada 16:19).

## Validado

- 16:15–16:18 (4 anclas L1).
- L2 16:19: 1 = 7,5 · 16:20: 2 = 12,3 · 16:21: 3 y módulo 19,7 · 16:22: AUT directo y nuevo 1 hasta 29850,8.
- 16:23: L2 nuevo 1 29852,6 → 29837,3.
- 16:24: L2 TT alcista **pendiente**, objetivo 29870,5 (Decisión 1).
- 16:25: L2 TT confirmado y extendido a 29875,4 · L1 nuevo 1 desde la apertura 29848,5.
- 16:26: L1 A principal desde 29875,4, tamaño 26,3.

## No validado

16:27 A/B/A-tendencia con TT pendiente; 16:28 dos TT pendientes; 16:29 dos TT confirmados; 16:30 módulo 53,6; 16:31 FINAL_A 29810,8 y TT 29757,2; 16:32 TT fallido y módulo conjunto 16:30–16:31.

## Arquitectura

`TMReadingManager` alimenta tick a tick L1 y L2. L2 se descubre cuando L1 mantiene un TT pendiente y una vela cerrada queda dentro del corredor del TT (máximo por debajo del origen del nuevo 1, mínimo por encima del objetivo) con recorrido >= 2,0. Se siembra con los ticks ya cerrados de esa vela, desde su extremo direccional.

Cada lectura es un `Reader` independiente. No se copian módulos, final_A, TT, A, B, C ni extremos. Cada TT declara propietario (`L1`/`L2`). Políticas de la lectura local: `tt_keep_first_pending` (el TT pendiente no se reescribe) y `tt_no_invalidate` (no falla por final_A en la lectura local, según v005 16:24).

## Estado

```text
TREE_STATUS              NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_STATUS  REFERENCE_ENGINE_INCOMPLETE
PATTERN_ENGINE_STATUS    PATTERN_ENGINE_INCOMPLETE
GATE_17                  13/19 anclas — GATE_FAILED
```
No se avanzó a 16:33.
