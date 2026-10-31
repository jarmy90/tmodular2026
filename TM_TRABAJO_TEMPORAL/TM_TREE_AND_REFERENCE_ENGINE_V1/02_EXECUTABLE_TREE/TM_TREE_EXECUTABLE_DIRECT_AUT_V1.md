# ÁRBOL EJECUTABLE — AUT DIRECTO POR A (ITERACIÓN 08)

## Alcance

El intérprete de referencia `tm_reference_interpreter_v1_direct_aut.py` implementa:

```text
1 → 2 → 3 → módulo
  → recorrido contrario (CONTRARY_MOVE_PENDING)
  → A confirmada / absorbida
  → B candidata
      VÍA 1: B Grande (100 % .. 127 %+0,25) → AUT por B → nuevo 1
      VÍA 2: A supera ESTRICTAMENTE la base del módulo → AUT directo por A → nuevo 1
```

## VÍA 1 — AUT por B (sin cambios respecto a iteración 07)

```text
B < 100 % de A                 → B_CANDIDATE
100 % <= B <= 127 % + 0,25     → B_GRANDE          (límite inclusivo)
B > 127 % + 0,25               → AUT_CONFIRMED en el MISMO tick → NEW_ONE
```

Propiedad del nuevo 1: `origin = extreme_A`, `direction = direction_B`,
`structural_time = nacimiento de B`, `knowledge_time = tick de AUT`.
La extensión posterior pertenece al nuevo 1, nunca a B.

## VÍA 2 — AUT directo por A (nueva en iteración 08)

```text
A existe (CONTRARY_MOVE_PENDING / A_CONFIRMED)
A supera ESTRICTAMENTE la base del módulo (mod_origin)
  → AUT_DIRECT_BY_A en el MISMO tick
  → NEW_ONE
```

Reglas:

- no existe B en esta vía;
- no se aplica 127 % + 0,25;
- tocar exactamente la base NO dispara AUT;
- superarla por un cent sí dispara AUT;
- un salto de debajo a encima dispara AUT en el mismo tick;
- no se inventa tick intermedio.

Propiedad del nuevo 1:

```text
new_one.origin          = a_origin
new_one.direction       = a_direction
new_one.structural_time = structural_time_A
new_one.knowledge_time  = primer tick de cruce estricto
new_one.extreme         = precio del tick de AUT
```

Tras el AUT directo: `A = CONFIRMED_ARCHIVED`, `módulo = FROZEN_REFERENCE`,
`B` inexistente, `3` archivado si procedía, `active_function = NEW_ONE`.

## Política retirada

```text
P-AB-04_RETURN_JUMP_4 → REJECTED_EXPERIMENTAL_ASSUMPTION
```

El salto fijo de 4,0 puntos en un tick no confirma por sí solo el retorno.
La autonomía del retorno se decide causalmente: dirección contraria a A y
extensión de su propio extremo, o absorción por extensión de A. `RETURN_MIN`
(2,0 puntos) solo separa ruido físico.

## Anclas verificadas

| Ancla | Resultado |
|---|---|
| 16:15–16:18 | módulo 28,5; A 9,1; B Grande 16:18:34.125; AUT por B 16:18:34.926; nuevo 1 29857,6 → 29843,0 |
| L2 16:19–16:22 | 1 = 7,5; 2 = 12,3; 3 = 29830,3; módulo = 19,7; A = 20,5; AUT directo en la base 29850,0 con nuevo 1 alcista 29830,3 → 29850,8 |

## Fuera de alcance

```text
C · CUT · TT · FT · gap con nuevo 1 · concurrencia L1/L2
```

No se implementan ni se asumen.
