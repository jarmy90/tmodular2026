# TM — TESTS REQUERIDOS v1

- **Documento:** `control/TM_TESTS_REQUERIDOS_v1.md`
- **Versión:** 1.0
- **Fecha:** 2026-10-19
- **Árbol de referencia:** `TM_ARBOL_CANONICO_COMPLETO_v1.md`
- **Estado:** catálogo de diseño; no implementado.
- **Regla:** ningún test se ejecuta hasta que Javier cierre las dudas bloqueantes.

## Resumen

| Tipo | Cantidad |
|---|---:|
| Positivos | 15 |
| Negativos | 12 |
| Frontera | 8 |
| Cronología | 5 |
| Concurrencia | 5 |
| **Total** | **45** |

## Catálogo

| ID | Tipo | Nodo / rama | Objetivo | Entrada | Resultado esperado | Estado |
|---|---|---|---|---|---|---|
| T-001 | Positivo | N-001, N-006, N-007, N-040 | 1 y 2 confirmados | Vela 1 alcista rango 9,80; vela 2 A/B/AUT | L1 con 1, 2 confirmada; no 3 | Diseño |
| T-002 | Positivo | N-003 | Gap a favor de 1 | 1 alcista; gap +0,30 | A/B implícitas; TT pendiente; no evaluar 2 | Diseño |
| T-003 | Positivo | N-004 | Gap contrario a 1 | 1 alcista; gap -0,30 | A Grande en dirección del gap; no 2 | Diseño |
| T-004 | Positivo | N-002, N-005 | Apertura plana | Apertura dentro de ±0,25 del cierre anterior | Abre evaluación de 2 | Diseño |
| T-005 | Negativo | N-006, N-008 | 2 inválido por cola | Cola > 0,25 o rango 2 > rango 1 | No 2; módulo + A Grande | Diseño |
| T-006 | Positivo | N-036 | 2 confirmado no se borra | 2 confirmado; luego movimiento contrario | 1+2 módulo; contrario A Grande; 2 conservado | Diseño |
| T-007 | Positivo | N-009, N-010 | 3 con retroceso 50 % exacto | Retroceso 0–50 %; supera extremo de 2 | 3 confirmada | Diseño |
| T-008 | Negativo | N-009, N-010 | 3 inválido por retroceso | Retroceso > 50 % | No 3; 1+2 módulo + A Grande | Diseño |
| T-009 | Positivo | N-009, N-010 | 3 válido con nuevo extremo | Retroceso válido; nuevo extremo | 3 confirmada | Diseño |
| T-010 | Positivo | N-011 | 3 fallido | 2 confirmado; 3 no válido | 1+2 módulo; A Grande | Diseño |
| T-011 | Negativo | N-012 | Módulo mal calculado | Módulo de una vela o composición no cerrada | No calcular TT; PENDIENTE_JAVIER | Diseño |
| T-012 | Positivo | N-013, N-038 | A Grande multi-vela | A continúa en vela siguiente | A no se cierra en el primer extremo | Diseño |
| T-013 | Frontera | N-014 | B candidata 99,99 % | B < 100 % de A | B candidata; no B Grande | Diseño |
| T-014 | Positivo | N-015 | B Grande al 100 % | B = 100 % de A sin superar 127,25 % | B Grande confirmada; no AUT | Diseño |
| T-015 | Frontera | N-015, N-016 | B exactamente en 127 % + 0,25 | Toque exacto del nivel | No AUT; B continúa; C Grande después | Diseño |
| T-016 | Positivo | N-017 | AUT por superación | B > 127 % + 0,25 | AUT; B deja de existir | Diseño |
| T-017 | Cronología | N-018 | Secuencia AUT → TT pendiente | AUT con módulo; TT no alcanzado | TT_PENDIENTE; no confirmar TT | Diseño |
| T-018 | Positivo | N-019, N-039 | TT exacto al 100 % | Precio = objetivo TT | TT confirmado; nuevo 1 | Diseño |
| T-019 | Frontera | N-019 | TT con overshoot | Precio supera el objetivo | TT confirmado; guardar overshoot | Diseño |
| T-020 | Negativo | N-020 | TT fallido | No alcanza TT; toca fin de A | TT cancelado; módulo; retorno A Grande | Diseño |
| T-021 | Positivo | N-021 | Nuevo 1 después de TT | TT confirmado; extremo real | Nuevo 1 con rango real | Diseño |
| T-022 | Positivo | N-022 | C Grande después de B | B confirmada; movimiento contrario | C Grande; no CUT todavía | Diseño |
| T-023 | Frontera | N-023 | B crea nuevo extremo | C activa; B supera su extremo | C cancelada; B continúa; no CUT | Diseño |
| T-024 | Positivo | N-024 | CUT | C supera fin de A | CUT confirmado | Diseño |
| T-025 | Negativo | N-024, N-025 | C sin CUT | C no supera fin de A | No CUT; C continúa o C = nuevo 1 pendiente | Diseño |
| T-026 | Frontera | N-025 | C = nuevo 1 | C sin CUT; condición exacta pendiente | PENDIENTE_JAVIER; no automático | Diseño |
| T-027 | Negativo | N-026 | FT sin TT | Movimiento contrario sin TT previo | No FT | Diseño |
| T-028 | Frontera | N-026 | FT con TT | TT confirmado; pérdida de velocidad | FT solo si Javier cierra la regla | Diseño |
| T-029 | Concurrencia | N-028, N-030 | Abrir L2 con regla expresa | L1 activa; candidato L2; regla presente | L2 activa; L1 conservada | Diseño |
| T-030 | Negativo | N-028 | L2 por ver A/B/AUT en una vela | Segunda lectura no autorizada | No L2; movimiento interno de L1 | Diseño |
| T-031 | Negativo | N-032 | Ruido no abre lectura | Oscilación sin referencia TM | Sin lectura; no A/B/C/AUT/TT | Diseño |
| T-032 | Cronología | N-013, N-031 | Cambio de vela no cierra A | A activa; nueva vela continúa | A se extiende; no se cierra por vela | Diseño |
| T-033 | Frontera | N-033 | AUT y TT en el mismo tick | Salto cruza AUT y TT | Ambos confirmados; nuevo 1 | Diseño |
| T-034 | Cronología | N-027, N-031 | Reclasificación conserva historial | Corrección posterior | Estado nuevo; eventos anteriores conservados | Diseño |
| T-035 | Negativo | N-022 | C antes de B | Movimiento contrario sin B confirmada | No C; no CUT | Diseño |
| T-036 | Negativo | N-024 | CUT sin C | Intento de CUT sin C Grande | No CUT | Diseño |
| T-037 | Negativo | N-002, N-003 | Gap + regla de 2 | Gap confirmado; intento de evaluar 2 | No 2; ruta de gap | Diseño |
| T-038 | Frontera | N-002, N-005 | Apertura exactamente ±0,25 | Delta = 0,25 | Plano; evaluar 2 | Diseño |
| T-039 | Concurrencia | N-029 | Máximo tres lecturas | L1 y L2 activas; candidato L3 | L3 activa; nunca L4 | Diseño |
| T-040 | Concurrencia | N-029 | Cuarta lectura rechazada | L1/L2/L3 activas; candidato L4 | No L4; sin lectura nueva | Diseño |
| T-041 | Cronología | N-001, N-006 | Orden intravela | Ticks de 1 y 2 en la misma vela | 1 antes de 2; no usar OHLC global | Diseño |
| T-042 | Cronología | N-033 | Mismo tick no duplica eventos | AUT y TT en el mismo tick | Un solo tick; dos eventos confirmados | Diseño |
| T-043 | Concurrencia | N-030 | Prioridad en el mismo tick | L1/L2/L3 alcanzan nivel a la vez | PENDIENTE_JAVIER; no decidir por orden | Diseño |
| T-044 | Frontera | N-039 | Igualdad exacta en TT | Precio = objetivo exacto | TT confirmado si se acepta igualdad | Diseño |
| T-045 | Concurrencia | N-028, N-029 | No mezclar niveles | L1 y L2 activas con niveles distintos | Cada lectura conserva su módulo y TT | Diseño |

## Criterios de aceptación

1. Un test solo pasa si el resultado coincide con una regla cerrada o con una decisión de Javier.
2. Los tests de concurrencia no pueden aprobarse mientras `DUDA-J01` y `DUDA-J03` estén abiertas.
3. Los tests de FT no pueden aprobarse mientras `DUDA-J05` esté abierta.
4. Los tests de módulo general no pueden aprobarse mientras `DUDA-J02` esté abierta.
5. Todo resultado `PENDIENTE_JAVIER` no es un fallo del test: es una rama no implementable todavía.
