# TM_READING_FAILURES_v0753 - REGISTRO DE FALLOS DE LECTURA

Version de referencia: v0753_FASE0 (motor R3, SHA `71d9a97a...`)
Actualizado: 2026-10-29

| Campo | F-001 | F-002 | F-003 | F-004 |
|---|---|---|---|---|
| FAILURE_ID | F-001 | F-002 | F-003 | F-004 |
| estado | OPEN | OPEN | OPEN | OPEN |
| version motor | v0752_R3 | v0752_R3 | v0752_R3 | v0752_R3 |
| entrada | TM_TICKFEED_1615_1730.csv | sintetica T3-004 | sintetica T3-005 | 16:21 feed |
| vela / tramo | 16:21 | tramo WAIT_THREE | tramo WAIT_THREE | 16:21 tras 1590 |
| primer tick divergente | seq 1446 (16:21:14,734) | primer tick tras 52,85 % | primer tick nuevo extremo | seq 1601 (16:21:54,482) |
| lectura esperada | 3 confirmada en 1446 | 3 imposible; modulo 1+2 + A | 2_EXTIENDE, sin 3 | pata 3 = 29830,3 |
| lectura obtenida | 3 confirmada en 1590 | 3 confirmada en 29830,4 | 3 confirmada en 29830,4 | pata 3 = 29830,5 |
| funcion actual | 2 confirmada | 2 confirmada | 2 confirmada | 3 confirmada |
| funcion esperada | 3 | 3 | 3 (con separacion) | 3 (extension) |
| pregunta activa | ? existe superacion valida? | ? el retroceso permite 3? | ? hay separacion funcional? | ? nuevo extremo de 3? |
| condicion pendiente | retroceso valido + superacion estricta | ratio <= 0,50 | retroceso previo | actualizacion del extremo |
| condicion real | distancia >= 2,00 pts | ninguna (no se mide) | ninguna (no se mide) | solo `module_extreme` |
| origen funcional | 29844,8 | 29844,8 | 29844,8 | 29832,5 |
| extremo funcional | 29832,5 | 29832,5 | 29832,5 | 29830,3 |
| structural_time | 16:20:41,153 | sintetico | sintetico | 16:21:54,482 |
| knowledge_time | 16:21:14,734 | sintetico | sintetico | 16:21:54,482 |
| tipo de fallo | regla mal implementada | regla canonica ausente | regla canonica ausente | extremo congelado |
| regla canonica | 3: retroceso 0-50 % + superacion estricta | igual | 2_EXTIENDE != 3 | extremo de 3 se actualiza |
| causa raiz | `WAIT_THREE` linea 2568 usa `STRUCTURAL_MOVE` | no se registra retroceso | no se exige separacion | la pata no se reescribe |
| prueba minima | T3-010, replay_1621 | T3-004 | T3-005 | T3-007 |
| correccion | pendiente Fase 3 | pendiente Fase 3 | pendiente Fase 3 | pendiente Fase 3 |
| archivos | motor 2565-2574 | idem | idem | 2575-2603 |
| resultado focal | 1590 != 1446 | confirma 3 | confirma 3 | 29830,5 != 29830,3 |
| resultado regresion | 3/12 T3 | 3/12 T3 | 3/12 T3 | 3/12 T3 |
| efectos laterales | adelanta modulo/TT/A | reclasifica 3 | reclasifica 3 | extremo/TT |
| estado final | OPEN | OPEN | OPEN | OPEN |

## Bloqueados por regla abierta

| ID | Depende de | Estado |
|---|---|---|
| F-005 minimo de retroceso funcional | Q-005 | BLOCKED_BY_RULE |
| F-006 fin de 3 | TM-3-004 | BLOCKED_BY_RULE |

## Infraestructura

| ID | Descripcion | Estado |
|---|---|---|
| INFRA-001 | `run_all.py` reescribio el ZIP congelado en la primera ejecucion desde la copia. Restaurado desde 3 copias con SHA original; guarda anadida en `repro/run_all_safe.py`. | FIXED |
