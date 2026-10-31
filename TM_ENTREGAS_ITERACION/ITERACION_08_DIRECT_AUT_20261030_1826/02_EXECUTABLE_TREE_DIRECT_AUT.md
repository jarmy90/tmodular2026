# ÁRBOL EJECUTABLE — AUT DIRECTO POR A

Base: núcleo 1->2->3->módulo, A/retorno/B candidata, B Grande/AUT por B.

## 1. AUT directo por A

Cuando A Grande ya existe y continúa en su propia dirección hasta superar
estrictamente la base del módulo:

```text
A_CONFIRMED
-> A extends in its own direction
-> if A strictly exceeds module base
-> AUT_DIRECT_BY_A
-> NEW_ONE_ACTIVE
```

No existe B en esta vía. No se aplica 127 % + 0,25. No se espera TT.

El nuevo 1 es el propio movimiento A transformado.

```text
new_one.origin          = a_origin
new_one.direction       = a_direction
new_one.structural_time = structural_time_A
new_one.knowledge_time  = primer tick de superación estricta de la base
new_one.extreme          = precio del tick de cruce
```

Si A continúa después del cruce, la extensión pertenece al nuevo 1.

## 2. Fronteras

```text
A toca exactamente la base -> no AUT directo todavía
A supera la base por un tick -> AUT directo
A salta desde debajo a encima en el mismo tick -> AUT directo en ese tick
A retrocede después de tocar base -> no AUT directo
A ya confirmado y retrocede -> no nuevo AUT directo
```

## 3. Autoridad

Al AUT directo:

```text
active_function = NEW_ONE
A = CONFIRMED_ARCHIVED
three = ARCHIVED if applicable
module = FROZEN_REFERENCE
B = inexistente
```

`historical_status` y `active_authority` son distintos.

## 4. Límites

No implementado:

- C;
- CUT;
- TT;
- FT;
- gap con nuevo 1;
- concurrencia interna;
- ciclo universal de 1.

## 5. Ancla L2

```text
module base = 29850,0
A = 29830,3 -> 29850,8 = 20,5
A cruza base estricta en 16:20:59.125
AUT directo nace en 16:20:59.125
nuevo 1 origin = 29830,3
extensión posterior = 29857,3
```
