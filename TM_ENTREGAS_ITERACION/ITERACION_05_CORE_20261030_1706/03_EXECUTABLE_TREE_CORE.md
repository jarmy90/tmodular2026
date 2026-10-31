# ÁRBOL EJECUTABLE — NÚCLEO V1

Estado: `CORE_IMPLEMENTED_AND_TESTED`
Árbol fuente: v2.19 `94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17`

Este documento contiene solo las transiciones implementadas y probadas en `TM_REFERENCE_INTERPRETER_V1`. A/B/C/AUT/CUT/TT/FT no forman parte de esta versión.

## 1. Inicio

```text
primer tick
→ 1 PENDING
origen = primer precio
dirección = sin dirección
extremo = origen
```

La dirección de 1 se fija en el primer desplazamiento de al menos `0,25` puntos respecto del origen:

```text
precio - origen >= 0,25  → 1 alcista
origen - precio >= 0,25  → 1 bajista
```

## 2. Fin de 1

Cuando 1 tiene dirección, cada nuevo extremo en su dirección actualiza `extreme` y `extreme_time`. La medida de 1 queda congelada en el primer tick de la vela siguiente:

```text
one_size = |one_extreme - one_origin|
one_status = CONFIRMED (medida congelada)
→ abrir pregunta TWO
```

El cierre de vela no reinicia 1: la lectura cruza velas.

## 3. Apertura

```text
|open - close_previo| < 0,25   → plano
|open - close_previo| >= 0,25  → no plano
```

`0,25` exactos **no** son plano.

## 4. Pregunta TWO

Solo si `1` tiene dirección y la apertura es plana:

```text
two_origin = open
two_dir = one_dir
two_status = CANDIDATE
```

No hay 2 con:

- apertura no plana;
- gap;
- cola inicial > `0,25` antes de avanzar en la dirección de 1.

## 5. 2 candidata

Mientras es candidata:

- conserva un único origen;
- las vibraciones internas no la fragmentan;
- actualiza solo su extremo direccional;
- no se convierte en A Grande.

## 6. 2 confirmada

```text
two_size >= one_size
→ TWO CONFIRMED en el primer tick que cumple
```

`two_extreme` sigue actualizándose mientras 2 conserva su finalidad, aunque ya esté confirmada.

La candidatura de 2 pertenece a su vela: una vibración interna de esa vela no abre 3. La pregunta por 3 comienza en la vela siguiente, cuando el retroceso ya puede ser funcional.

## 7. 2 imposible

```text
cierre de vela sin two_size >= one_size
→ TWO IMPOSSIBLE
→ MODULE_BY_DISCARD
→ siguiente pregunta = A Grande
```

2 no continúa pendiente en la vela siguiente.

## 8. Módulo por descarte

```text
module_origin = one_origin
module_extreme = extremo estructural más lejano de 1 o 2
module_dir = one_dir
```

No se encoje por un retroceso de 2. No incorpora extremos de A.

## 9. Pregunta THREE

Solo si 2 fue confirmada y ha comenzado la vela siguiente.

```text
retroceso desde el extremo final de 2 en contra de two_dir
retroceso <= 50 % de two_size  → 3 posible
retroceso >  50 % de two_size  → 3 IMPOSSIBLE
```

El 50 % exacto conserva la posibilidad y **no** confirma 3.

## 10. 3 confirmada

Tras un retroceso válido:

```text
precio recupera two_dir
precio supera estrictamente two_extreme
→ THREE CONFIRMED
```

3 actualiza su extremo hasta que comienza A Grande.

## 11. Módulo regular

```text
1 + 2 + 3
module_origin = one_origin
module_extreme = three_extreme
```

## 12. Fuera de alcance

No implementado en el núcleo:

- A Grande y autonomía de A;
- B candidata / B Grande / AUT;
- C Grande / C usada como tendencia / CUT;
- TT / FT;
- concurrencia L1/L2 dentro del mismo proceso;
- gap implícito completo.

Se marcan como `BLOCKED_BY_OPEN_RULE` o `NOT_IMPLEMENTED_CORE`. No se simulan.
