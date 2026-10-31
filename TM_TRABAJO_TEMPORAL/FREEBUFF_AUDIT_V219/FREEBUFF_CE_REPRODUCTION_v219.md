# FREEBUFF_CE_REPRODUCTION_v219

**Reproducción independiente de las 21 secuencias CE**
**Fecha:** 2026-10-30
**Fuente:** `CE_TESTS_v219.md` (`DA697ADA…`) y árbol `94A1408A…`
**Motor analizado:** R5 `9BD1BEDB5DEC8C5A1C3A831338503E90CC04EE3CD776CF4E01D27CF8AA0EBEAE`
**Variante:** A — auditada (no la empaquetada `19A847C0…`)
**Versión documental:** 1.0 · **Versión del motor:** `0.7.5.2-R5`
**Método:** observacional, sin modificar motor, árbol, tests ni goldens
**tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

---

## 0. Qué se ejecutó

| Elemento | Ruta |
|---|---|
| Arnés | `04_CE_REPRODUCTION/run_ce_reproduction.py` |
| Salida bruta por tick | `04_CE_REPRODUCTION/ce_out/CE_REPRODUCTION_RAW.json` |
| Resumen | `04_CE_REPRODUCTION/ce_out/CE_REPRODUCTION_SUMMARY.json` |
| CSV de divergencias | `FREEBUFF_FIRST_DIVERGENCES_v219.csv` |
| Constructor del CSV | `04_CE_REPRODUCTION/build_divergences.py` |
| Feed legacy v010 | **no utilizado**; solo referencia `LEGACY_SUBSET_REFERENCE` |

Protocolo:

1. Cada secuencia se construye con los ticks publicados en `CE_TESTS_v219.md` (una lista = una vela; 1 s entre ticks).
2. Se instancia `CanonicalEngine`, se activa `trace_states` y se alimenta **un tick por llamada** a `feed_chunk`.
3. Antes y después de cada tick se registran: precio, vela, `phase` local, `armed`, `candidate_bar`, todas las lecturas, sus preguntas y los eventos emitidos en ese tick. El par `before`/`after` queda en `CE_REPRODUCTION_RAW.json`.

**Límite:** no se instrumenta el motor campo a campo (qué atributo se lee o se escribe en cada línea). Esa parte se documenta por análisis estático en `FREEBUFF_RC1_MOVEMENT_ANALYSIS_v219.md` §2.3 y en el mapa árbol→motor, no por traza dinámica.
4. Cada secuencia se ejecuta **dos veces** desde estado limpio y se compara la huella SHA-256 de eventos + lecturas **y el `state_log` completo tick a tick**.
5. Para cada uno de los 262 ticks se ejecuta un motor nuevo con el prefijo `1..k` y se compara su `state_log[k-1]` con el estado del tick `k` de la ejecución completa.
6. No se escribe ninguna expectativa dentro del motor. Las expectativas viven solo en el CSV, después de la ejecución.

## 1. Resumen

| Métrica | Resultado |
|---|---|
| Secuencias ejecutadas | 21/21 |
| Ticks totales | 262 |
| Doble ejecución idéntica (eventos + lecturas) | **21/21** |
| Doble ejecución idéntica (`state_log` completo) | **21/21** |
| Prefijos comprobados | **262** |
| Prefijos divergentes | **0** |
| Excepciones | 0 |
| Secuencias con alguna lectura | **7/21** |
| Secuencias con `2`, `3`, `A`, `B`, `C`, `AUT`, `CUT` o `TT` | **0/21** |
| PASS_CONCEPT | 0 |
| FAIL_CONCEPT | 13 |
| INCONCLUSIVE_TEST_SETUP | 8 |

Coincide con OpenBot en determinismo (21/21), prefijos (262/262), cero excepciones y reparto 13/8. **No coincide** en la atribución del primer tick de divergencia de CE-2 y CE-7 (ver §7).

## 2. Vocabulario realmente emitido

| Tipo de evento | Casos en que aparece |
|---|---|
| `LECTURA_CREADA` (función `1`, estado `MODULE`, motivo `FIRST`) | CE2-POS/NEG/FRON, CE4-NEG, CE7-AUT, CE7-C-NEG, CE7-C-FRON |
| `QUESTION` | los mismos 7 |
| `GAP` | CE3-NEG, CE5-POS, CE6-POS, CE6-FRON |
| `FIN_FEED` | 21/21 |

No aparece ni una sola vez: `2`, `3`, `A`, `B`, `C`, `AUT`, `CUT`, `TT`, `FT`, `B_GRANDE`, `B_CANDIDATA`, `MODULO_EXT`, `LOCAL_FUNCTION`, `LECTURA_CERRADA`.

El llamado `1:FIRST` **no es un estado**: es un evento `LECTURA_CREADA` cuyo campo `function` vale `"1"` y cuyo `origin_reason` vale `"FIRST"`. El estado interno de la lectura es `MODULE`.

## 3. Resultado por secuencia

| Caso | CE | Tick div. | Precio | Esperado en ese tick | Observado | Veredicto | 1.ª lectura | Módulo observado |
|---|---|---:|---:|---|---|---|---:|---|
| CE1-POS | CE-1 | 2 | 101,00 | `1` abierta (100→102) | sin lectura | FAIL | — | — |
| CE1-NEG | CE-1 | 2 | 101,00 | `1` abierta; luego `2` imposible | sin lectura | FAIL | — | — |
| CE1-FRON | CE-1 | 2 | 101,00 | `1` abierta; `2` en 104,00 | sin lectura | FAIL | — | — |
| CE2-POS | CE-2 | 2 | 4,00 | `1` desde 0,00 | sin lectura | FAIL | 19 | 0,00→16,00 |
| CE2-NEG | CE-2 | 2 | 4,00 | `1` desde 0,00 | sin lectura | INCONCLUSIVE | 19 | 0,00→16,00 |
| CE2-FRON | CE-2 | 2 | 4,00 | `1` desde 0,00; CUT en 0,00 | sin lectura | INCONCLUSIVE | 14 | 0,00→11,00 |
| CE3-POS | CE-3 | 2 | 3,00 | `1` desde 0,00; `2` candidata | sin lectura | FAIL | — | — |
| CE3-NEG | CE-3 | 2 | 3,00 | `1`; `2` imposible por 6,25 | sin lectura (solo `GAP` en tick 4) | INCONCLUSIVE | — | — |
| CE3-FRON | CE-3 | 2 | 3,00 | `1`; `2` en 12,00 | sin lectura | FAIL | — | — |
| CE4-POS | CE-4 | 2 | 5,00 | dos lecturas concurrentes | sin lectura | FAIL | — | — |
| CE4-NEG | CE-4 | 2 | 5,00 | `1` principal; módulo 20,00 | sin lectura | INCONCLUSIVE | 11 | 0,00→20,00 |
| CE4-FRON | CE-4 | 2 | 5,00 | `1`; B candidata desde 20,00 | sin lectura | INCONCLUSIVE | — | — |
| CE5-POS | CE-5 | 2 | 4,00 | `1`; TT en 16,00 con knowledge del tick | sin lectura | FAIL | — | — |
| CE5-NEG | CE-5 | 2 | 4,00 | `1`; TT pendiente | sin lectura | INCONCLUSIVE | — | — |
| CE5-FRON | CE-5 | 2 | 4,00 | TT en 16,00 exactos | sin lectura | FAIL | — | — |
| CE6-POS | CE-6 | 5 | 110,00 | A/B/A-tendencia implícitas; nuevo `1` en 110,00 | solo `GAP` | FAIL | — | — |
| CE6-NEG | CE-6 | 5 | 100,10 | sin gap; continúa lectura | sin lectura | INCONCLUSIVE | — | — |
| CE6-FRON | CE-6 | 5 | 100,25 | gap 0,25 + resolución implícita | solo `GAP` | FAIL | — | — |
| CE7-AUT | CE-7 | 2 | 5,00 | `1` (0→20); A desde 20,00 | sin lectura | FAIL | 8 | 0,00→20,00 |
| CE7-C-NEG | CE-7 | 2 | 20,00 | `1` bajista 25→0 | sin lectura | INCONCLUSIVE | 15 | 25,00→−0,25 |
| CE7-C-FRON | CE-7 | 2 | 20,00 | `1` bajista 25→0; CUT en 0,00 | sin lectura | FAIL | 14 | 25,00→−0,25 |

**Lectura del cuadro:** en 19 de 21 secuencias falta la estructura `1` (todas salvo CE6-POS/FRON, donde el fallo inmediato es el gap). En las 7 que llegan a tener lectura, esta nace entre 7 y 18 ticks después del primer desplazamiento y, en 5 de ellas (CE2-POS, CE2-NEG, CE2-FRON, CE7-C-NEG, CE7-C-FRON), con un módulo que no es el `1` canónico.

## 4. Primera divergencia causal

La primera divergencia **no es la etiqueta que falta**, sino el tick en que el motor no tiene ninguna estructura:

| Caso | Tick | Precio | Qué falta exactamente |
|---|---:|---:|---|
| CE1-POS/NEG/FRON | 2 | 101,00 | No nace `1` con el primer desplazamiento direccional; el motor exige 6,00 |
| CE2-POS/NEG/FRON | 2 | 4,00 | Ídem; la lectura no aparece hasta el tick 19/19/14 |
| CE3-POS/NEG/FRON | 2 | 3,00 | Ídem |
| CE4-POS/NEG/FRON | 2 | 5,00 | Ídem; además no hay segunda lectura |
| CE5-POS/NEG/FRON | 2 | 4,00 | Ídem |
| CE6-POS/FRON | 5 | 110,00 / 100,25 | Gap detectado sin resolución funcional |
| CE6-NEG | 5 | 100,10 | Sin gap, pero tampoco hay estructura `1` que continuar |
| CE7-AUT | 2 | 5,00 | Ídem; la lectura nace en el tick 8 con módulo 0→20 |
| CE7-C-NEG/FRON | 2 | 20,00 | Ídem; la lectura nace en el tick 15/14 con módulo 25→−0,25 |

En los 19 casos en que falta la estructura `1` —12 sin ninguna lectura y 7 con lectura tardía— la causa inmediata es la misma: `MovementBuilder` no tiene dirección hasta que el precio se aleja 6,00 de su origen. En los 2 casos de gap, la causa inmediata es distinta: el gap se detecta y se emite, pero no se resuelve.

## 5. Propagación

```text
sin 1 en el tick
→ no existe la pregunta por 2
→ no existe 3
→ no existe A Grande
→ no existe B candidata
→ no existe B Grande
→ no existe AUT
→ no existe C
→ no existe CUT
→ no existe TT ni FT
```

En las 7 secuencias donde por fin nace una lectura, esta nace ya como `MODULE` con la pregunta `DONDE_NACE_A` y permanece ahí hasta el final del feed. No hay una sola transición funcional posterior.

## 6. Evidencia de que no hay información futura

- 262 prefijos: el estado del prefijo `1..k` es idéntico al estado del tick `k` de la ejecución completa, en los 262 casos.
- La lectura tardía usa únicamente precios ya ocurridos (`movement.extreme_index <= confirm_index`).
- No se detectó ninguna lectura de golden, fichero o fixture desde el motor.
- La suite `test_transformations.py` verifica además ausencia de hardcodes de golden y ya pasa en 28/28.

**Matiz importante:** no usar información futura **no es lo mismo** que conocer a tiempo. R5 no espía el futuro, pero sí confirma tarde (ver §8).

## 7. Diferencias con OpenBot

| Punto | OpenBot | Esta reproducción | Comentario |
|---|---|---|---|
| Determinismo | 21/21 | 21/21 | coincide |
| Prefijos | 262/262 | 262/262 | coincide |
| PASS / FAIL / INCONCLUSIVE | 0 / 13 / 8 | 0 / 13 / 8 | coincide en el recuento |
| Primer tick CE-2 | tick 4 (10,00) | tick 2 (4,00); primera lectura tick 19 | OpenBot señala el tick del módulo esperado, no el primer tick sin estructura. La lectura real nace en el 19 |
| Primer tick CE-7 | tick 5 (20,00) | tick 2 (5,00); primera lectura tick 8 | misma diferencia de criterio |
| Atribución RC-1 | 18 secuencias | **19** secuencias | CE6-NEG también carece de `1`, pero OpenBot lo deja fuera del recuento 18+2 |
| Módulo CE-2 | 0→16 | 0→16 | coincide |
| Módulo CE-7 | 25→−0,25 | 25→−0,25 | coincide |
| "No hay errores locales independientes" | sí | **matizado**: el módulo solo se infla cuando la pata no retrocede 6,00; cuando es monótona, la medida es correcta (CE4-NEG: 0→20) | ver `FREEBUFF_RC1_MOVEMENT_ANALYSIS_v219.md` §4 |

Ninguna de estas diferencias cambia el veredicto. La más relevante es la tercera: **son 19, no 18, las secuencias en las que falta la estructura `1`**.

## 8. Hallazgo adicional no cubierto por las 21 CE

Las 21 secuencias terminan antes de que el motor pueda completar un ciclo A/B. Para comprobar si el motor **puede** llegar a TT se ejecutó una traza adicional (`03_CONCEPTUAL_DIAGNOSIS/probe_dual_authority.py`, salida en `probe_dual_authority.out`), sin relación con el feed real:

```text
0,4,8,10,12 | 14,16,18,20,14 | 14,12,10,8,16 | 18,24,30,36,40 | 38,36,34
```

Resultado observado:

- `B_GRANDE` y `AUT` se emiten **en el mismo tick** (tick 17, precio 24,00), con `b_grande_time == aut_time`.
- El objetivo TT es 28,00. El precio negocia 28, 30, 32, 36, 38 y 40 por encima del objetivo.
- **El TT no se confirma nunca**: `_check_tt` solo se invoca al procesar un movimiento cerrado, y el tramo 8→40 no retrocede el 25 % requerido antes del final del feed.
- La lectura local nace **después** del AUT, con `1` = 28→35 (rango de una vela), no con el `1` original.

Consecuencias:

1. El motor puede violar N-037 (B Grande y AUT no coexisten) sin ninguna excepción.
2. El TT puede perderse aunque el precio supere el objetivo en 12 puntos.
3. La lectura local no hereda el `1` del ciclo, sino un rango de vela posterior al AUT.

Este hallazgo es coherente con RC-1 y RC-3 y no está cubierto por `CE_TESTS_v219.md`.

## 9. Contradicciones documentales detectadas (no corregidas)

1. **0,25: plano o gap.** El árbol H14 dice `plano si |cierre−apertura| ≤ 0,25`; v2.13 dice `< 0,25`; `CE_TESTS` CE-6 dice que 0,25 exactos **es** gap. R5 aplica `< 0,25` (0,25 = gap) en `local_two_gate` y `_schedule_gap`. No se resuelve aquí: se registra como pregunta experta.
2. **Ventana de lecturas.** `v005` confirma hasta 16:39; 16:49–17:29 están `[D]`. No se usan como expectativa.
3. **Recuento de velas `[A]`.** El resumen de `v005` dice 14 velas `[A]` pero su propia lista incluye 16:25–16:29 como `[A]`; el recuento es internamente inconsistente. No se corrige.
4. **CE2-FRON.** La secuencia publicada en `CE_TESTS` usa `V4: 11,00 | 6,00 | 0,00`, mientras el texto del caso describe un recorrido distinto. Se ejecutó la secuencia publicada.
5. **CE-7 C.** El caso dice "C 25,00 al alza" y espera CUT contra `a_end`; con `a_end = 4,00`, C cruza 4,00 mucho antes de 25,00. La expectativa no distingue si el CUT se mide contra `a_end` o contra la base del módulo. Se registra como ambigüedad de la prueba, no del motor.

## 10. Conclusión de la reproducción

- El resultado de OpenBot es **reproducible** en lo esencial: 21/21 deterministas, 262/262 prefijos, 0 PASS, 13 FAIL, 8 INCONCLUSIVE, y ausencia total de la escalera funcional.
- La causa inmediata es única y verificable en código: **no existe `1` hasta que se cierra un movimiento de 6,00**.
- Las 21 CE **no pueden distinguir** entre las distintas causas de RC-1, porque todas mueren en el mismo tick. Para separarlas hacen falta las pruebas de `FREEBUFF_TEST_GAPS_v219.md`.
- El motor **sí** puede llegar a B Grande/AUT con una traza más larga, pero lo hace violando la separación de estados y perdiendo el TT. Eso demuestra que RC-1 no es solo "arranque": la granularidad de decisión afecta a todo el ciclo.
