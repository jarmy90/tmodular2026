# AUDITORÍA — ITERACIÓN 15

## 1. Objetivo

Aprender operativamente de las lecturas humanas: localizar la primera divergencia
de cada bloque, reconstruir el estado vivo, corregir la causa raíz y repetir hasta
que la lectura emitida coincida tick a tick, sin preguntar salvo ambigüedad real.

## 2. Método aplicado por divergencia

1. Primer tick divergente.
2. Retroceso al último estado coincidente.
3. Reconstrucción de funciones, patrones y referencias vivas.
4. Recorrido del árbol desde ese estado.
5. Tres o más causas candidatas.
6. Contraste con árbol, lectura humana, ticks anteriores y posteriores y pruebas.
7. Clasificación del defecto.
8. Corrección de la causa raíz.
9. Reejecución desde el inicio del bloque y del feed.
10. Rechazo de la corrección si rompía una lectura anterior.

## 3. Divergencias encontradas y resueltas

| # | Divergencia | Causa raíz | Corrección |
|---|---|---|---|
| 1 | 1 de 16:15 no confirmado al cierre | se confirmaba al consumir la apertura siguiente | `_confirm_one_at_close` con `knowledge_time` = último tick de su vela |
| 2 | 2 de 16:20 se extendía dentro de 16:21 | 2 no se cerraba al final de su vela | `TWO_FROZEN_AT_CLOSE` (v2.13/v2.14) |
| 3 | 3 nacía en 29832,3 y no en 29830,3 | una A prematura dentro de la vela de 3 bloqueaba la extensión | absorción de la oscilación interna + extensión real de 3 |
| 4 | A de 16:23 nacía con origen 29847,8 | estado de retorno heredado de la A anterior | reset de `return_*` al abrir cada A |
| 5 | solo se permitía un AUT directo por lectura | `aut_direct_status` era global | AUT directo por estructura (reset al abrir A) |
| 6 | B no reabría tras ser absorbida por A | A confirmada no admitía nueva B | `_open_b_from_return` para A ya confirmada |
| 7 | la reanudación del módulo absorbía una A estructural | absorción sin criterio funcional | absorción reservada a oscilación < 35 % del dominante |

## 4. Secuencia 16:22–16:23 verificada

```
16:22:52.576  AUT_DIRECT_BY_A  A = 20,5 desde 29830,3
              nuevo 1 alcista 29830,3 -> 29850,8
16:23:02.021  A Grande bajista 29850,8 -> 29842,8 (8,0)
16:23:10.943  B 8,6 -> AUT local alcista
              nuevo 1 29842,8 -> 29851,4 -> 29852,6
16:23:48-49   la bajada supera la base 29842,8
              AUT bajista: nuevo 1 29852,6 -> 29837,3
```

## 5. Comparación tick a tick

| Bloque | Ticks | Anclas | Divergencias |
|---|---|---|---|
| B1 16:15–16:18 | 937 | 4/4 | 0 |
| B2 16:19–16:22 | 898 | 4/4 | 0 |
| B3 16:22–16:24 | 2.297 | 3/3 | 0 |
| B4 16:24–16:25 | 2.552 | 3/3 | 0 |

Coincidencia causal de anclas documentadas: **14/14 (100 %)**.
No equivale a fidelidad completa del feed: solo los cuatro bloques tienen lectura
humana tick a tick.

## 6. Pruebas

```
146/146 PASS
canónicas 128 | provisionales 16 | open_rule 2
```

Cambios de prueba: A-01 reformulada para la oscilación interna (< 35 %) según
v2.16; el resto de suites sin cambios.

## 7. Feed completo

```
rotaciones 37 | módulos 8 | A confirmadas 7 | B candidatas 15
B Grande 1 | AUT 2 | TT confirmados 2 | FT 1 | CUT 3
nuevo 1 de tamaño cero: 5 (diferidos, no inventados)
```

Siguen siendo rotaciones internas, no ciclos TM completos validados.

## 8. Qué es provisional

- La referencia del 35 % (v2.16 la declara orientativa, no frontera aprobada).
  Las clasificaciones A/B que dependen de ella se marcan `PROVISIONAL`.
- El nacimiento de la lectura local: primera vela del nuevo 1 dominante,
  declarada por su AUT directo. Funciona en 16:19–16:23, no está probado en
  otros bloques.
- El AUT local de nivel 3 (nuevo recorrido supera la base del módulo AUT).

## 9. Qué queda abierto

- Fidelidad tick a tick de 16:25–17:29 (lectura humana disponible, no validada).
- TT/FT de cada estructura local tras AUT encadenados.
- CUT y FT en lecturas locales.

## 10. Estado

```
TREE_STATUS              NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_STATUS  REFERENCE_ENGINE_CONSISTENT_IN_VALIDATED_BLOCKS
PATTERN_ENGINE_STATUS    PATTERN_ENGINE_INCOMPLETE
```
