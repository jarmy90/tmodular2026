# AUDITORIA ITERACION 17

## Regla causal de descubrimiento de L2

En la apertura de 16:20, con 16:19 ya cerrada: L1 conserva el AUT bajista y el TT principal pendiente 29829,1. La vela 16:19 tiene rango 7,5 y queda dentro del corredor (máximo 29850,0 < origen del nuevo 1 29857,6; mínimo 29842,5 > objetivo TT 29829,1). Se crea L2 sembrada con los ticks de 16:19 desde su máximo. El 1 local resulta 7,5.

## Hipotess aceptadas

1. L2 sembrada desde el extremo direccional de la vela, no desde la primera impresión (1 local 7,5, no 6,4).
2. `tt_keep_first_pending` en L2: el TT 29870,5 de 16:22 no se sustituye por AUT posteriores.
3. `tt_no_invalidate` en L2: el TT sobrevive a los mínimos de 16:23–16:24 y confirma en 16:25 (Decisión 1).
4. A de L1 nacida del extremo de un nuevo 1: no se procesa como reanudación del módulo anterior; se exige retorno >= 35 % de A (provisional) para confirmarla. Esto produjo A 26,3 en 16:26.

## Hipotess rechazadas

- Rotación administrativa por `NEW_ONE` (iteración 16, RC-1 revertida entonces): creaba un ciclo por vela.
- A de 115 puntos sin confirmación: rompía 16:23/16:24.
- `local_mode` sin `tt_no_invalidate`: TT 29870,5 fallaba en 16:24.

## Primera divergencia por intento

| Intento | Primera divergencia |
|---|---|
| L2 desde 16:18 | 1 local 6,4 en vez de 7,5 |
| L2 desde 16:19 sin local_mode | 16:23 sin nuevo 1 29852,6→29837,3 |
| L2 con local_mode | 16:23 resuelto; 16:24 TT fallaba |
| L2 con no_invalidate | 16:19–16:25 resueltos; 16:26 L2 deriva a B de 17,9 |
| L1 16:26 | A 12,8 prematura; corregida a 26,3 con retorno 35 % |
| 16:27 | L1 confirma A y abre B candidata, pero no reproduce A/B/A-tendencia con TT pendiente |

## Propietario de cada TT

- L1: TT 29829,1 (ciclo 16:15–16:24), confirmado y extendido hasta 29828,1.
- L2: TT 29870,5 (lectura local 16:19), pendiente 16:22–16:24, confirmado y extendido a 29875,4 en 16:25.

## Causa raíz pendiente

El motor sigue sin una regla de transición A → B → A usada como tendencia para 16:27, y sin soporte de dos TT pendientes en lecturas distintas más allá de 16:26. L2 deriva a una B de gran tamaño en 16:26 en lugar de FT + módulo por descarte. No se inventó ninguna regla; queda documentado.
