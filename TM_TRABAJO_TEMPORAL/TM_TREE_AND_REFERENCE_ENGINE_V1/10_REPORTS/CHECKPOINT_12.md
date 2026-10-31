# CHECKPOINT 12 — REINICIO DE CICLO, CUT→TENDENCIA, FT

**Baseline:** `TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT` (no es motor oficial)
**Árbol:** v2.19, no modificado, no congelado

## Decisiones expertas incorporadas

```text
1. TT 100 % -> cierre de ciclo -> el movimiento = nuevo 1 (resto de su vela)
   -> al abrir la vela siguiente: plano/gap, cola, direccion, medida -> 2
2. CUT (C > final real de A) != C usada como tendencia (C > base del modulo)
   CUT no crea nuevo 1; la trazabilidad es B -> C -> CUT -> tendencia -> nuevo 1
3. FT es patron estructural desde el extremo REAL del TT (no del nivel 100 %)
   Las variables no crean, cancelan ni reclasifican FT
```

## Reglas de implementación

```text
- con TT pendiente NO se abre estructura nueva (v2.7 B)
- el nuevo 1 se promueve a 1 al abrir la vela siguiente cuando el TT ya no está pendiente
- prev_cycle archiva módulo, A, B, C, CUT, TT (objetivo y extremo real) del ciclo cerrado
- FT se evalúa en capa aparte y no toca la autoridad de la función activa
```

## Anclas

```text
L1 16:15-16:18  modulo 28,5 | A 9,1 | AUT 16:18:34.926 | TT objetivo 29829,1
TT extremo real 29829,1 -> FT origen 29820,1 cuando el TT se extiende a ese nivel
L2 16:19-16:22  1 = 7,5 | 2 = 12,3 | 3 = 29830,3 | modulo 19,7
```

## Feed completo 16:15-17:29

```text
ticks 20.335 | deterministico | prefijo consistente | 1.596 eventos
ciclos 47 | modulos 8 | A confirmadas 10 | B candidatas 10 | AUT 5 (2 directos)
C 3 | CUT 2 | C tendencia 3 | TT 100 % 2 | FT 1 | gaps reales resueltos 38
```

Gaps reales observados en el feed: 14,00 / 1,50 / 1,50 / 0,80 / 3,60 puntos.
La afirmación de la iteración 11 («el feed no contiene gaps») era **falsa**: se basaba en que
el lector nunca volvía a evaluar una apertura.

## Pruebas

```text
nucleo 19 | A/retorno/B 32 | AUT directo 17 | C/CUT 18 | gap+conc 16 | TT 12 | iter12 18
TOTAL 132 PASS 132
canonical 69 | provisional 62 | open_rule_block 1
```

## Estado

```text
TREE_STATUS:              NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_STATUS:  REFERENCE_ENGINE_INCOMPLETE
PATTERN_ENGINE_STATUS:    PATTERN_ENGINE_INCOMPLETE
```

Abierto: reset posterior a CUT (Q-CUT), descubrimiento automático de lecturas concurrentes
(Q-CONCURRENCY), variables operativas de FT (fuera de alcance).
