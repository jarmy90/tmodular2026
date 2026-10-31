# ÁRBOL EJECUTABLE — A / RETORNO / B CANDIDATA V1

Base: núcleo 1→2→3→módulo, sin cambios semánticos.

## 1. Apertura de A

Cuando termina el módulo (por descarte, 1+2 o 1+2+3), el recorrido contrario nace desde el extremo final del módulo:

```text
a_status = CONTRARY_MOVE_PENDING
a_origin = module_extreme
a_dir = -module_dir
a_structural_time = module_extreme_time
```

No se usa porcentaje, punto medio ni umbral de autonomía.

La candidatura empieza en la vela siguiente al cierre del módulo/3. El módulo no se amplía por ticks posteriores de la misma vela.

## 2. Extensión y absorción

Mientras A está pendiente:

- si el precio hace un nuevo extremo en `a_dir`, se actualiza `a_extreme`;
- si el módulo/3 extiende su extremo en su dirección, A se absorbe:
  `ABSORBED_IN_ACTIVE_FUNCTION`, sin B;
- si A no tiene recorrido propio, un tick posterior de la vela del módulo no reescribe el módulo.

## 3. Retorno

Un movimiento contra A abre `RETURN_MOVE_PENDING` cuando alcanza al menos 2,0 puntos de desplazamiento estructural. Ese mínimo es el filtro de ruido; no confirma A ni B por sí solo.

El retorno se confirma como estructura si:

- mantiene al menos dos ticks de continuidad;
- conserva el desplazamiento mínimo;
- A no ha hecho un nuevo extremo.

Si A extiende su extremo, el retorno se absorbe:

```text
RETURN_MOVE_PENDING -> ABSORBED_IN_A
A sigue viva
no existe B
```

## 4. A confirmada

Solo tras el retorno estructural:

```text
A_CONFIRMED (una vez)
extreme_A fijado
B_CANDIDATE
```

`structural_time_A` es el nacimiento de A en el extremo del módulo. `knowledge_time_A` es el tick del retorno que permite conocer la autonomía. No se presentan como el mismo instante.

## 5. B candidata

```text
b_origin = extreme_A
b_dir = return_dir
b_structural_time = primer tick del retorno
b_knowledge_time = tick de confirmación de A/B
```

B actualiza su extremo mientras conserva finalidad. Si A recupera su dirección y supera su extremo, B se absorbe en A y no queda B formal.

## 6. Límites

No implementado:

- B Grande;
- AUT por B;
- C;
- CUT;
- TT;
- FT;
- nuevo 1 por AUT directo.

Cuando B alcanza el 100 % o el 127 % + 0,25 se registra un flag, no una clasificación:

```text
B_100_REACHED_NOT_IMPLEMENTED
B_AUT_LIMIT_REACHED_NOT_IMPLEMENTED
```

Cuando A supera la base del módulo se registra:

```text
AUT_DIRECT_BY_A_NOT_IMPLEMENTED
```

No se crea un nuevo 1 todavía.

## 7. Invariantes

- B no existe sin A confirmada.
- A confirma una sola vez.
- El origen de A no cambia.
- El extremo de A se congela al abrir B.
- Un retorno absorbido no crea B.
- Una B absorbida no se convierte en formal.
- No hay referencias cruzadas.
- `structural_time <= knowledge_time`.
- No se usa información futura.
