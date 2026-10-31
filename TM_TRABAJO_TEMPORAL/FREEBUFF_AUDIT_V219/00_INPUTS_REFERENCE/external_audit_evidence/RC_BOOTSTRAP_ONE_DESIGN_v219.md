# RC_BOOTSTRAP_ONE — Diseño conceptual (sin código)

2026-10-30 · R5 `9BD1BEDB…` intacto · árbol `94A1408A…` intacto · goldens intactos.
Objetivo: fijar el ciclo de vida de `1` antes de tocar nada.

## 1. Por qué RC-1 y RC-1a son un solo defecto

`MovementBuilder` no tiene dirección hasta que el precio se aleja **6,00** del primer tick (`min_move=MOVE=600`, R5:337, 351-362). Por eso:

- un `1` de 2,00 no existe;
- la lectura nace ya como `MODULE` (`_create_reading`, R5:857-897) cuando un movimiento de 6,00 se confirma por retroceso `max(6,00; 25 %)` (R5:363-381);
- el "módulo" es el recorrido `origin→extreme` de ese movimiento, que ya contiene tramos de otras funciones. CE-2: `0,00→16,00`; CE-7: `25,00→−0,25`.

No es un cálculo mal hecho: **falta la frontera funcional entre `1` y lo que viene después**. Por eso se agrupan como `RC-BOOTSTRAP-ONE`.

## 2. Mapa temporal del ciclo de vida de 1

```text
NO_ACTIVE_READING
   │  primer desplazamiento direccional con referencia válida (sin mínimo)
   ▼
ONE_CANDIDATE  ──(nuevo extremo)──► ONE_CANDIDATE   (medida provisional crece)
   │  condición canónica de confirmación
   ▼
ONE_CONFIRMED  (medida congelada)
   │  fin de vela / apertura siguiente
   ▼
WAIT_NEW_BAR ──► EVALUATE_OPENING ──► TWO_CANDIDATE
                       │
                       └─ imposible (gap, plano, cola) ──► siguiente función
```

Regla de oro: **el origen no cambia nunca** durante la candidatura; el extremo sí. La medida congelada nunca se amplía después.

### 2.1 ONE_CANDIDATE — campos mínimos

| Campo | Definición | Se actualiza |
|---|---|---|
| `direction` | +1/−1 del primer desplazamiento | nunca |
| `structural_origin` | precio del tick de referencia (apertura/cierre previo o primer tick) | nunca |
| `current_extreme` | precio más lejano en la dirección | cada tick que amplía |
| `current_measure` | `abs(current_extreme − structural_origin)` | derivada |
| `structural_time` | timestamp del origen | nunca |
| `candidate_status` | `OPEN` / `STRETCHED` / `AT_RISK` | por tick |
| `owning_bar` | vela donde nació la candidata | al cambiar de vela pasa a `WAIT_NEW_BAR` sin perderla |
| `confirmation_condition` | condición canónica (pendiente de Javier) | fija |
| `impossibility_condition` | qué la anula (p. ej. retroceso total al origen) | fija |

### 2.2 ONE_CONFIRMED — campos congelados

`origin_1`, `extreme_1`, `measure_1`, `direction_1`, `structural_time_1`, `knowledge_time_1`, `bar_1`.

`knowledge_time_1` = tick de confirmación, nunca posterior. Ningún extremo de `A`, `2`, `3`, `B` o `C` puede reescribir `extreme_1` ni `measure_1`. El módulo de la lectura (base para TT y CUT) se deriva de estos campos congelados, no de `module_extreme` móvil.

## 3. Funciones R5 que hoy leen/escriben cada campo

| Campo | Hoy vive en | Escritor actual | Lector actual | Defecto |
|---|---|---|---|---|
| `direction` | `MovementBuilder.direction` (R5:346) | `feed` 355/359, solo con 6,00 | `_open_candidate` 1408 | no hay dirección antes de 6,00 |
| `structural_origin` | `MovementBuilder.origin` (344) → `Reading.module_origin` (879) | `feed`/`_reanchor` 384-389; `_create_reading` | `_owner` 1572; `module_size` 254 | el origen es el del movimiento de 6,00, no el del primer desplazamiento |
| `current_extreme` | `MovementBuilder.ext` (345) → `module_extreme` | `feed` 364-381; `_advance_*` 3037-3160; local 3446 | TT target 1008; CUT; `_owner` | se reescribe con extremos de A/B (CE-2: 16,00) |
| `current_measure` | `Movement.size` (35), `Reading.module_size` (254) | derivada | 2/B/TT/CUT | medida contaminada |
| `candidate_status` | `Reading.question["candidate_status"]` | `_q` 3296-3302 (solo al consolidar MODULE) | auditoría | describe la candidata de `A`, no la de `1` |
| `confirmation_time` | no existe para `1` | — | — | no se distingue creación de confirmación |
| `knowledge_time` | `_record_knowledge` 1584; `tt_knowledge_time` | snapshot | auditoría | no hay conocimiento de `1` |
| `bar_1` | `Reading.created_bar` | `_create_reading` | `_record_knowledge` 1588 | es la vela del movimiento de 6,00 |

Nombres de diseño (no existen aún, no programar): `open_one_candidate`, `update_one_candidate`, `confirm_one`, `freeze_one`, `open_two_question`. Deberían ser los únicos escritores de los campos de §2.

## 4. Propuesta de estados

| Estado | Entrada | Salida | Invariante |
|---|---|---|---|
| `NO_ACTIVE_READING` | inicio / cierre de lectura | primer desplazamiento | sin lectura no hay funciones |
| `ONE_CANDIDATE` | primer desplazamiento | confirmación o imposibilidad | origen inmutable; extremo móvil |
| `ONE_CONFIRMED` | condición canónica | cambio de vela | medida congelada; no se amplía |
| `WAIT_NEW_BAR` | cierre de vela con `1` viva | primera apertura evaluable | no se pierde la candidata |
| `EVALUATE_OPENING` | primera apertura | `TWO_CANDIDATE` o imposible | plano/cola/gap deciden |
| `TWO_CANDIDATE` | apertura válida | confirmación de `2` | `rango2 ≥ measure_1` |

Prohibido: pasar de `ONE_CONFIRMED` a `TWO_CANDIDATE` sin `EVALUATE_OPENING`; ampliar `measure_1` en `ONE_CONFIRMED`; crear `MODULE` directamente desde `NO_ACTIVE_READING`.

## 5. Consecuencias de confirmar 1 al cierre vs al umbral estructural

| Criterio | Ventaja | Riesgo | Efecto en TT/CUT | ¿Requiere regla experta? |
|---|---|---|---|---|
| **Al cierre de vela** | origen y extremo quedan en una frontera observable; encaja con N-002 (2 se evalúa tras plano de apertura); conocimiento no retroactivo | el extremo de la vela puede incluir ticks que ya pertenecen a `A`; si `A` empieza dentro de la misma vela, la medida de `1` se contamina | el módulo sería el cierre de la vela, no el primer tramo | sí: ¿la vela o el primer contrario? |
| **Al umbral estructural** | congela en el tick exacto en que el movimiento deja de ser `1` | no hay umbral canónico: usar 2,00/6,00 sería inventar (v2.6 §F, "NO INVENTAR UMBRALES"); cualquier número fijo contradice N-001 | el módulo sería el tramo hasta el primer contrario, generalmente menor | sí: hay que definir el disparador |
| **Al primer contrario** | separa limpiamente `1` de `A`; la medida queda en el extremo antes de `A` | exige saber cuándo un contrario es "estructural" y no una oscilación interna | módulo más pequeño y estable; TT se proyecta desde `fin_A + measure_1` | sí: tamaño mínimo del contrario (R-01/R-05) |

Consecuencia común: si `1` no se congela antes de `A`, el TT y el CUT heredan una referencia falsa. Confirmar al cierre y confirmar al umbral producen módulos distintos; la elección cambia CE-2, CE-3, CE-5 y CE-7, no solo CE-1.

## 6. Pruebas afectadas

| Prueba | Cambio de expectativa |
|---|---|
| CE1-POS/NEG/FRON | se dividen en **CE1-A bootstrap** (existe `ONE_CANDIDATE` con origen conservado) y **CE1-B confirmación** (`ONE_CONFIRMED` y medida congelada). No se exige `1 confirmada` en el tick 2 hasta resolver §5. |
| CE2 | el módulo debe medir el tramo de `1` (10,00), no el recorrido total (16,00) |
| CE3 | `2` usa `measure_1` congelada como referencia |
| CE4 | el módulo de cada lectura nace de su propio `1` |
| CE5 | el objetivo TT se proyecta desde `measure_1`, con `knowledge_time` del tick |
| CE6 | el nuevo 1 del gap usa el mismo ciclo (origen = apertura) |
| CE7 | la base del módulo y el CUT se derivan de `measure_1` congelada |

Las expectativas restantes de `CE_TESTS_v219.md` no se modifican.

## 7. Pregunta experta para Javier

> Cuando nace la función `1`, ¿en qué momento exacto queda **confirmada** y **congelada** su medida?
>
> 1. Al **cierre de la vela** en la que nace, tomando como extremo el de esa vela.
> 2. En el **primer tick en que el precio deja de ampliar** su extremo.
> 3. Cuando aparece el **primer movimiento contrario** que la pone a prueba, tomando el extremo anterior a ese contrario.
>
> Y en el caso 3: ¿qué tamaño mínimo debe tener ese contrario para cerrar `1` sin considerarse una oscilación interna?

Esta respuesta fija `confirmation_condition` y `freeze` de `ONE_CANDIDATE`, y desbloquea CE1-B, CE2, CE3, CE5 y CE7. Sin ella no se implementa RC-BOOTSTRAP-ONE.
