# Hipótesis confirmadas y rechazadas

## Confirmadas

| Hipótesis | Evidencia v0.7.4 | Estado |
|---|---|---|
| El módulo `29667.30 -> 29602.10` existe y mide `65.20`. | `R0062`, `x=65.20`. | Confirmada |
| El TT de esa lectura es `29615.20`. | `R0062.tt_target=29615.20`, alcanzado en `29614.20`. | Confirmada |
| El TT se alcanza y luego se confirma FT. | `R0062.tt_hit=1`, `ft=1`, FT `16:57:34.937`. | Confirmada |
| La lectura pertenece a una estructura previa. | `R0062.parent_reading_id=R0061`, `origin_reason=B_CONFIRMADA_NEW1`. | Confirmada |
| Un A mayor que el módulo puede seguir siendo válido. | `R0062.a=78.30`, `x=65.20`, sin `A_INVALIDA_MODULO`. | Confirmada |
| El máximo local de `29667.30` es un origen válido aunque no sea el máximo macro. | Builder 25%/6 produce el movimiento; el macro 35/40 no lo produce. | Confirmada |
| El recorrido necesita más que las 5 velas de `16:52–16:56`. | La lectura se crea en `16:52:48.559` y su FT llega en `16:57:34.937`. | Confirmada |
| El movimiento de `65.20` no se obtiene con legs fijos de 20–40. | Los legs de 35/40 producen `143.00`, `78.30` y `80.20`, no `65.20`. | Confirmada |
| Un solo movement builder de 25% / mínimo 6.00 captura la estructura local. | 264 movimientos; `65.20` confirmado. | Confirmada |
| B puede oscilar sin convertir cada oscilación en C. | `R0062` registra `B_OSCILACION`, B y B Grande antes del TT. | Confirmada |
| v0.7.3 absorbía el TT y perdía la lectura local. | Salida ciega: `R0007` se extiende a `29600.70`, sin `LECTURA_CREADA`. | Confirmada |
| v0.7.6 conserva absorción local pese a declarar cobertura. | `minor_tt_absorbed=1`, `post_tt_opportunities_lost=4`, `R0007` con TT a `29600.70`. | Confirmada |
| La causalidad por prefijo puede verificarse sobre eventos y lecturas creadas. | Test de prefijo hasta `16:59` aprobado. | Confirmada |

## Rechazadas

| Hipótesis | Evidencia v0.7.4 | Estado |
|---|---|---|
| El mínimo de B debe ser exactamente `29600.70`. | El mínimo real es `29600.20`; el TT y el FT no cambian. | Rechazada como condición estructural |
| Un A mayor que el módulo invalida la lectura. | `A=78.30` sobre `x=65.20` sigue produciendo TT y FT. | Rechazada |
| Cada oscilación interna de B es una B fallida. | `B_CAND` y `B_OSCILACION` permiten nuevos extremos sin cerrar. | Rechazada |
| Un contrario que supera `a_end` por 1.90 puntos debe cortar el TT. | El buffer de 2.00 puntos no corta; el TT sigue vivo. | Rechazada |
| El TT anterior debe bloquear una lectura local nueva. | `R0062` nace dentro de `R0061` y desarrolla su propio TT. | Rechazada |
| La macro de 35/40 puntos contiene el módulo de 65.20. | La macro produce `143.00`; no produce `65.20`. | Rechazada |
| La cobertura de v0.7.6 es funcional por declarar `TM_COVERAGE_OK`. | La propia salida registra absorción y oportunidades perdidas. | Rechazada |
| La lectura clave es `R0063` también en v0.7.4. | En v0.7.4 es `R0062`; `R0063` es otra lectura abierta al final. | Rechazada como numeración; confirmada como geometría |
| El FT debe entrar en el mismo instante del TT. | El FT se confirma después del TT, con contrario posterior. | Rechazada |

## No decididas

| Hipótesis | Motivo | Estado |
|---|---|---|
| El límite de A debe ser 2x el módulo. | Guardia provisional sin validación experta. | Pendiente |
| El buffer de CUT debe ser siempre 2.00. | Confirmado en el caso; falta generalización. | Pendiente |
| El máximo de 3 lecturas activas es universal. | Aplicado y probado, sin decisión canónica explícita. | Pendiente |
| El FT debe expirar por tiempo o por precio. | No hay regla cerrada. | Pendiente |
| `post_tt_fallido` debe abrir una función nueva. | No hay regla cerrada. | Pendiente |
| La granularidad local de `16:45` es `11.00` o `25.30`. | Dos lecturas posibles; falta decisión experta. | Pendiente |
