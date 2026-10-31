# ITERACIÓN 20B — ROTACIÓN POST-TT, RECLASIFICACIÓN DE R20-1 Y PRIMERA DIVERGENCIA MEDIDA

Fecha: 2026-10-31
Baseline: `TM_ITERATION_20A_REVIEW.zip`
Estado: `ITER20B_STATUS = POST_TT_ROTATION_COMPLETE`

---

## 1. Reclasificación exigida (aplicada)

| Regla | Autoridad 20A | Autoridad 20B |
|---|---|---|
| `A_DELIMITED_AT_CLOSE` (R20-1) | CANONICAL_DERIVATION | **PROVISIONAL_CONTEXTUAL_POLICY** |
| `PATTERN_OWNERSHIP` (`a_trend_owner`) | CANONICAL_RULE | CANONICAL_RULE (solo impide reescritura; no decide A) |
| Lectura humana de 16:27 | CORRECTED_BY_TICKS | **PARTIALLY_UNRESOLVED** |

R20-1 no se transfiere de la función 1 a la función A. La norma vigente dice que
A puede comenzar al final de una vela y continuar en la siguiente sin
reiniciarse; R20-1 solo se aplica cuando la A realmente termina dentro de su
vela (extremo en la vela, sin retorno autónomo desde ese extremo y sin módulo
regular en la misma dirección). Sus condiciones funcionales completas siguen
abiertas.

La corrección humana de 16:27 queda **parcial**: los 1,7 puntos se midieron
contra la A principal de 26,3. La B local solo puede medirse contra una A local
de LOCAL-G2, que esta iteración **no** ha construido. No se afirma que no exista
B Grande local.

---

## 2. Cambio estructural implementado: rotación post-TT

### Regla

```
TICK QUE CONFIRMA TT (cualquier via valida: AUT por B, AUT directo,
                        A usada como tendencia, modulo por descarte):
    cycle_closed_at_tt = tick causal
    si la fase previa NO era NEW_ONE_ACTIVE:
        nuevo 1:  n_origin  = tt_final_A
                  n_extreme = precio del tick de confirmacion
                  n_dir     = tt_dir
                  n_kt      = tick causal
        phase = NEW_ONE_ACTIVE
APERTURA DE LA VELA SIGUIENTE:
    archivar el ciclo por TT
    promover el nuevo 1 a 1 del ciclo nuevo
    abrir la pregunta por 2 con la apertura de la vela
```

No depende de la fase previa, ni de la hora, ni de un precio. Es la regla que ya
existía para `AUT` por B; ahora cubre también `B_LIVE` y la vía de tendencia.

### Código

* `_new_one_from_tt_trend(t)` — crea el nuevo 1 en el tick de confirmación.
* `_trend_rotation(t)` — archiva el ciclo, promueve el nuevo 1 a `one_*` y llama
  a `_eval_opening`.
* `_on_bar_open` — rama para `transition_reason == TT_TREND_NEW_ONE`.

---

## 3. Hecho estructural de 16:29–16:32 (medido, no supuesto)

Prefijo 16:15–16:32, `TMReadingManager`, tickfeed canónico.

| Hecho | seq | hora | precio |
|---|---|---|---|
| TT mayor confirma objetivo | 3543 | 16:29:59.827 | 29822.1 |
| ciclo 1 archivado por TT | 3544 | 16:30:00.026 | 29820.6 |
| nuevo 1 (29849.1→29822.1) promovido | 3544 | 16:30 | 27.0 |
| A nuevas de ciclo 2 | 3840 | 16:31:03.573 | 29810.7 desde 29784.6 (26.1) |
| B Grande ciclo 2 | 3846 | 16:31:03.573 | — |
| C_GRANDE (objetivo alcanzado) | 3851 | 16:31:04.575 | — |

Extremos físicos de las velas (verificados sobre el tickfeed):

| Vela | máximo | mínimo |
|---|---|---|
| 16:29 | 29841.5 | 29822.1 |
| 16:30 | **29838.2** | **29784.6** |
| 16:31 | **29810.8** | **29760.3** |
| 16:32 | 29820.8 | 29794.1 |

### Reclamaciones humanas que los ticks confirman

| Reclamación | Valor humano | Derivado de ticks | Resultado |
|---|---|---|---|
| final_A 16:31 | 29810.8 | 29810.7 (A = 26.1 desde 29784.6) | CONFIRMED_BY_TICKS |
| mínimo 16:31 | 29760.3 | 29760.3 | CONFIRMED_BY_TICKS |
| módulo 16:30 | 53.6 | 53.6 (= 29838.2 − 29784.6) | magnitud CONFIRMED; origen estructural distinto |
| objetivo TT 16:31 | 29757.2 | 29783.8 (motor) | NO resuelto |

---

## 4. Primera divergencia exacta de 16:30–16:32

**Momento:** seq 3544 (apertura de 16:30), evento `TWO_IMPOSSIBLE_NO_FLAT`
seguido de `MODULE_BY_DISCARD`.

* El motor prohíbe la 2 porque la apertura de 16:30 no es plana respecto del
  cierre anterior y aplica la rama de gap implícito (v2.7).
* Sin 2, el módulo por descarte se mide desde el **origen del 1** (29849.1) hasta
  el extremo alcanzado (29784.6) = **64.5**; el motor conserva como módulo el
  movimiento de confirmación del TT (29849.1→29822.1 = **27.0**).
* La lectura humana mide **53.6**, que corresponde exactamente al retroceso
  físico 29838.2→29784.6: es decir, cuenta como 2 el retroceso de 16.1 puntos
  hasta el máximo de 16:30 (29838.2), y mide el módulo desde el extremo de ese 2.

Consecuencia en cadena:

| | motor 20B | lectura humana |
|---|---|---|
| módulo | 27.0 | 53.6 |
| final_A | 29810.7 | 29810.8 |
| objetivo TT | 29783.8 | 29757.2 |
| mínimo real 16:31 | 29760.3 | 29760.3 |
| resultado | **C_GRANDE** (objetivo cruzado) | **TT pendiente por 3.1** |
| 16:32 | C extendida/CUT | TT no alcanza objetivo → `TT_FAILED` |

El mínimo de 16:31 (29760.3) queda **3.1 puntos por encima** del objetivo
humano y **23.5 puntos por debajo** del objetivo del motor: la diferencia de
26.6 puntos entre ambos objetivos es exactamente la diferencia de módulos. Es
una divergencia de **una sola magnitud**, no de cronología ni de propietario.

### Hipótesis registradas

| id | hipótesis | resultado |
|---|---|---|
| H1 | el módulo debe medirse desde el extremo del 2 (29838.2) | **mejor explicación**; requiere que exista 2 (hoy prohibida por `TWO_IMPOSSIBLE_NO_FLAT`) |
| H2 | la 2 no debe prohibirse cuando el retroceso supera el ruido | compatible con H1, no implementada |
| H3 | el módulo debe medirse desde el origen del 1 (64.5) | rechazada: objetivo 29746.2, el mínimo 29760.3 quedaría 14.1 corto y 16:32 fallaría por otra vía |
| H4 | el nuevo 1 del TT debe nacer en el extremo del 2, no en final_A | rechazada: desplaza el origen a 29822.1 y rompe 20A |
| H5 | el objetivo debe recalcularse al confirmarse la A | rechazada: introduce dependencia del resultado esperado |

Se implementó H1/H2 de forma general (`MODULE_BY_DISCARD_FAILED_TWO`) y se
**revirtió**: con la topología de gap actual la 2 nunca llega a existir en el
ciclo, por lo que la regla no se ejecuta y quedaría como código muerto sin
prueba. Se deja documentada como regla abierta con su condición de disparo
explícita: *existe 2 confirmada y la 3 no se confirma*.

---

## 5. Estado de LOCAL-G2 (FASE 3 no completada)

No se construyó el `Reader` limpio de LOCAL-G2. Lo medido y registrado:

* el slot LOCAL está libre desde el archivo de LOCAL-G1 (seq 2553);
* la sonda con el slot sin archivar forma un módulo local propio (450) en
  16:26–16:29, por lo que el módulo local **no** es inexistente, contra lo que
  afirmaba 20A;
* `LOCAL_G2 = PENDING`; la lectura humana de 16:27 y 16:28 queda
  `PARTIALLY_UNRESOLVED` hasta sembrar LOCAL-G2 limpia en 16:26.

Escenas a evaluar sin elegir: A (sin lectura local), B (módulo local por
descarte en 16:26), C (candidato confirmado retroactivamente en 16:27).

---

## 6. Deuda declarada: seis anclas con `False` fijo

`run_iteration_17_anchors.py` mantiene seis anclas escritas con `False` fijo
(B4-4 … B4-9). **No se han sustituido en esta iteración.** No cuentan como
aprobadas: el marcador 13/19 incluye únicamente las 13 evaluadas contra
snapshots reales.

---

## 7. Métricas verificadas (ejecutadas, no estimadas)

| Métrica | Valor |
|---|---|
| `run_iteration_16_all.py` (9 suites ligadas) | **169 / 169, fail 0** |
| `run_iteration_19b_tests.py` | **23 / 23** |
| Anclas de transición 19B | **12 / 12** |
| Anclas 20A/20B | **10 / 10** |
| Anclas humanas evaluadas | **13 / 19** (6 con `False` fijo, sin sustituir) |
| Fugas entre generaciones | 0 |
| Escrituras en generación archivada | 0 |
| Determinismo / consistencia de prefijo | true / true |
| Reglas por hora o precio en el motor | 0 |

---

## 8. Changelog 20B

1. `_new_one_from_tt_trend`, `_trend_rotation` y rama de apertura en
   `_on_bar_open`: rotación post-TT independiente de la fase previa.
2. R20-1 reclasificada a política contextual provisional.
3. `HUMAN_READING_PARTIALLY_UNRESOLVED` sustituye a la corrección definitiva.
4. Descarte de 2 fallida revertido por no ejecutarse en el tramo real (queda como
   regla abierta, no como código muerto).
5. Anclas D4/D6 de 20A reespecificadas al hecho estructural verificable.
6. Tabla de hechos 16:29–16:32 con seq, hora y precio, y primera divergencia
   reducida a una única magnitud (módulo 27.0 vs 53.6).
