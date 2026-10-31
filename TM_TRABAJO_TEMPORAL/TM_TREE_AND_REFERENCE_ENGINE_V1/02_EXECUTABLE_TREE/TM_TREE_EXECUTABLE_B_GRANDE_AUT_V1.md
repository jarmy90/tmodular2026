# ÁRBOL EJECUTABLE — B GRANDE / AUT / NUEVO 1

Base: núcleo 1→2→3→módulo y A/retorno/B candidata.

## 1. Correcciones previas

### A puede nacer dentro de la vela

`THREE_CONFIRMED_LIVE → CONTRARY_MOVE_PENDING` puede ocurrir en la misma vela de 3.

Si 3 vuelve a extender su extremo:

```text
A pendiente → ABSORBED_IN_ACTIVE_FUNCTION
3 conserva la autoridad
```

Si A adquiere autonomía, 3 queda archivado en su extremo estructural real. La vela no divide ni reinicia A.

`P-AB-01` queda `SUPERSEDED_EXPERIMENTAL_POLICY`.

### Retorno sin contador de ticks

`P-AB-03` queda `READER_EXPERIMENTAL_POLICY_NOT_CANON`.

`RETURN_MOVE_PENDING` conserva origen, extremo, dirección, tiempo, medida y propietario. El retorno se confirma por:

- extensión de su propio extremo; o
- salto estructural único de al menos 4,0 puntos.

El mínimo de 2,0 puntos solo separa ruido. No hay `return_ticks >= 2` como condición.

## 2. B Grande

```text
B < 100 % de A          → B_CANDIDATE
B >= 100 % de A         → B_GRANDE
B <= 127 % de A + 0,25  → B_GRANDE
B > 127 % de A + 0,25   → AUT en el mismo tick
```

`knowledge_time_B_GRANDE` es el primer tick que alcanza el 100 %. El límite superior es inclusivo.

## 3. AUT

Si B supera estrictamente el límite:

```text
B deja de ser función vigente
AUT_CONFIRMED
NEW_ONE_ACTIVE
```

No se retrasa AUT, no se espera TT y no se mantiene B vigente.

Si un solo tick cruza 100 % y AUT:

- se registra `B_GRANDE_CAUSAL_CROSS`;
- el estado final es AUT;
- B Grande no queda vigente.

## 4. Nuevo 1

```text
new_one.origin          = b_origin = extreme_A
new_one.direction       = b_direction
new_one.structural_time = structural_time_B
new_one.knowledge_time  = tick AUT
new_one.extreme          = precio del tick AUT
```

Después de AUT, solo el nuevo 1 actualiza su extremo. B conserva su último valor en el cruce.

## 5. Autoridad

Al confirmar A:

- `three_authority = ARCHIVED`;
- `module_authority = FROZEN_REFERENCE`;
- `active_function = B_CANDIDATE`.

Al AUT:

- A, 3 y módulo quedan sin autoridad activa;
- `active_function = NEW_ONE`;
- sus datos históricos se conservan.

## 6. Límites

No implementado:

- C;
- CUT;
- TT;
- FT;
- nuevo 1 por AUT directo de A;
- gap con nuevo 1;
- concurrencia interna.

## 7. Ancla

```text
B Grande: 16:18:34.125, B = 9,1
AUT:      16:18:34.926, B = 12,3
nuevo 1:  origin 29857,6
          structural_time 16:17:05.425
          knowledge_time 16:18:34.926
          extensión posterior 29843,0
```

B no se informa con 14,6: 12,3 es el movimiento B/AUT; 14,6 es la extensión del nuevo 1.
