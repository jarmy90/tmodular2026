# FREEBUFF_TEST_GAPS_v219

**Qué no prueban las 21 CE y qué debe probarse antes de implementar**
**Fecha:** 2026-10-30
**Árbol:** `94A1408A…` · **Motor actual:** R5 `9BD1BEDB…` (`0.7.5.2-R5`)
**Versión documental:** 1.0
**tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

---

## 0. Por qué las 21 CE no bastan

Las 21 secuencias mueren en el mismo punto: el tick 2. Todas comprueban el mismo síntoma (no hay `1`) y por eso no pueden separar:

- si falta el bootstrap de `1`;
- si falta la escalera `2/3` en la máquina primaria;
- si el módulo se compone mal;
- si los umbrales de 6,00 bloquean A/B/C;
- si el gap se resuelve o no.

Una prueba que falla en el primer tick no informa sobre los siguientes. Se necesita una prueba por **concepto aislado**, con su caso negativo y su frontera.

## 1. Principios del plan

1. **Una prueba = un concepto.** Si falla, debe identificar una sola causa.
2. **Sin fixtures dentro del motor.** Precios y tiempos viven en la prueba, nunca en el código.
3. **Tres variantes por concepto:** positivo, negativo, frontera exacta.
4. **Estado por tick.** No basta la etiqueta final; se compara el `state_log` de cada tick.
5. **Prefijo.** Cada prueba se ejecuta también truncada en cada tick y debe coincidir.
6. **Sin información futura.** El estado del tick `k` no puede depender de ticks `> k`.
7. **Repetición.** Dos ejecuciones limpias deben ser idénticas.
8. **Replay real como corroboración, no como golden total.** `v005` solo hasta 16:39; `[D]` no se usa como expectativa.

## 2. Pruebas que faltan

### 2.1 Bloque RC-1.1 — bootstrap de `1`

| ID | Secuencia mínima | Aserción | Nodo | Causa |
|---|---|---|---|---|
| T-01 | 100,00 → 101,00 → 102,00 | en 101,00 existe `ONE_CANDIDATE` con origen 100,00, extremo 101,00, medida 1,00 | N-001, N-040 | RC-1.1 |
| T-02 | 100,00 → 102,00 → 104,00 → 103,00 | `1` conserva origen 100,00 y actualiza extremo a 104,00; la medida crece sin reiniciar | N-013, N-038 | RC-1.1 |
| T-03 | `1` que cruza tres velas | la misma lectura sobrevive los cambios de vela; no se crea un `1` por vela | BASE-2, N-038 | RC-1.1 |
| T-04 | 0,00 → 1,00 → 0,00 | `1` se invalida/absorbe según Q1; no se crea módulo | N-001 | RC-1.1 |
| T-05 | `1` de 5,99 y de 6,00 | ambos existen; el tamaño no decide la existencia | v2.5 §D/§H | RC-1.4 |

### 2.2 Bloque RC-1.2 — escalera `2/3`

| ID | Secuencia mínima | Aserción | Nodo | Causa |
|---|---|---|---|---|
| T-06 | `1` 0→10; vela siguiente plana 10→11→12 | `2_CANDIDATA` en 11, `2_CONFIRMADA` en 12 (100 % de 1) | N-006, N-007 | RC-1.2 |
| T-07 | `2` con vibración interna de 3,00 | sigue siendo la misma `2`; no nace A; no se reinicia el origen | v2.13, N-032 | RC-1.2, RC-1.4 |
| T-08 | `2` que no confirma en su vela y sigue en la siguiente | sigue `PENDING`, no `IMPOSSIBLE`; confirma al 100 % | N-007, N-008 | RC-1.2 |
| T-09 | `2` imposible por gap | `MODULE_POR_DESCARTE` + `A_CANDIDATE`; no se crea `2` | N-008, v2.19 §E | RC-1.2, RC-2 |
| T-10 | `2` confirmada + retroceso 30 % + nuevo extremo | `3_CONFIRMADO` | N-009, N-010 | RC-1.2 |
| T-11 | `2` confirmada + retroceso 70 % + nuevo extremo | `1+2` = módulo; el contrario es A; no hay `3` | N-011 | RC-1.2 |
| T-12 | retroceso exactamente 50 % | decisión experta; la prueba debe marcarse `BLOCKED` hasta Q5 | N-010 | RC-1.2 |

### 2.3 Bloque RC-1.3 — módulo

| ID | Secuencia mínima | Aserción | Nodo | Causa |
|---|---|---|---|---|
| T-13 | `1` 0→10, A 10→6, B 6→11, C 11→7 | módulo = 10,00; no 16,00 | N-012 | RC-1.3 |
| T-14 | pata monótona 0→20 | módulo = 20,00 (control positivo) | N-012 | RC-1.3 |
| T-15 | pata con mechas y solapes | módulo = max(high) − min(low) del conjunto (si Q5 lo confirma) | N-012 | RC-1.3 |
| T-16 | `1+2` sin `3` | módulo = 1+2, no la pata completa | N-011 | RC-1.3 |
| T-17 | después de B Grande y C | el módulo no se amplía con B ni con C | N-012 | RC-1.3 |

### 2.4 Bloque RC-1.4 / A / B / AUT

| ID | Secuencia mínima | Aserción | Nodo | Causa |
|---|---|---|---|---|
| T-18 | A de 2,00 exactos | `A_GRANDE` confirmada; no se exige 6,00 | N-013, filtro 2,00 | RC-1.4 |
| T-19 | A de 1,99 | ruido; no hay A | filtro 2,00 | RC-1.4 |
| T-20 | A cruza la base del módulo | `A_USED_AS_TREND` + AUT + nuevo `1` en el mismo movimiento, con genealogía | v2.3 §F, v2.16 | RC-1.4 |
| T-21 | B = 99,99 % / 100 % / 127 %+0,25 / 127 %+0,01 | candidata / B Grande / B Grande / AUT | N-016, H9 | RC-1.4 |
| T-22 | B salta de 90 % a 140 % en un tick | nunca `B_GRANDE` y `AUT` en el mismo tick; primero B Grande, luego AUT en el tick siguiente | N-037 | RC-1.4, RC-4 |

### 2.5 Bloque RC-2 — gap

| ID | Secuencia mínima | Aserción | Nodo | Causa |
|---|---|---|---|---|
| T-23 | cierre 100,00, apertura 110,00 | A/B/A-tendencia implícitas sin precios + nuevo `1` con origen 110,00 | v2.19 §A-C | RC-2 |
| T-24 | apertura 100,10 | sin gap, sin implícitas | H14 | RC-2 |
| T-25 | apertura 100,25 | expectativa `BLOCKED` hasta Q2 | H14 vs v2.13 | RC-2 |
| T-26 | gap + TT pendiente heredado | primero se resuelve TT/final de A (v2.7), después la rama de gap | v2.7 §B, v2.19 | RC-2 |
| T-27 | gap tras `1`, `2` imposible | `NO_TWO` + resolución implícita + nuevo `1` | v2.19 §E | RC-2 |

### 2.6 Bloque RC-3 — capas

| ID | Secuencia mínima | Aserción | Nodo | Causa |
|---|---|---|---|---|
| T-28 | C activa mientras TT está en `TT_EXT` | la función sigue siendo C; el patrón sigue siendo TT; coexisten | v1.2 §13.6 | RC-3 |
| T-29 | TT confirmado y CUT en el mismo tick | ambos se registran; ninguno borra al otro | N-031, N-034 | RC-3 |
| T-30 | TT confirmado y FT posterior | FT no borra el TT; se registra como patrón distinto | N-026 | RC-3 |

### 2.7 Bloque RC-4 / conocimiento

| ID | Secuencia mínima | Aserción | Nodo | Causa |
|---|---|---|---|---|
| T-31 | TT objetivo 28; precios 28→40 sin cierre de movimiento | TT confirmado en el primer tick que toca 28 | N-019, N-039 | RC-4 |
| T-32 | TT confirmado y retroceso posterior | el TT no se retira | N-019 | RC-4 |
| T-33 | dos lecturas con módulos 20 y 5 | cada TT usa su propio módulo; el dueño se decide por estructura | N-028..N-030 | RC-4 |
| T-34 | traza de dos autoridades (B Grande + AUT) | una sola transición por tick y por lectura | N-036, N-037 | RC-4 |

### 2.8 Bloque constitucional

| ID | Secuencia mínima | Aserción | Nodo | Causa |
|---|---|---|---|---|
| T-35 | cualquier secuencia | el motor no lee goldens, ficheros ni fixtures | — | constitución |
| T-36 | traslación de precio/tiempo e inversión de dirección | la genealogía se conserva | — | determinismo |
| T-37 | ejecución completa y por prefijos | mismo estado en cada tick | — | causalidad |
| T-38 | doble ejecución | huella idéntica | — | determinismo |

## 3. Cobertura por causa raíz

| Causa | Pruebas | Nº |
|---|---|---:|
| RC-1.1 bootstrap | T-01..T-05 | 5 |
| RC-1.2 escalera | T-06..T-12 | 7 |
| RC-1.3 módulo | T-13..T-17 | 5 |
| RC-1.4 umbrales/A/B/AUT | T-18..T-22 | 5 |
| RC-2 gap | T-23..T-27 | 5 |
| RC-3 capas | T-28..T-30 | 3 |
| RC-4 autoridad/conocimiento | T-31..T-34 | 4 |
| Constitucional | T-35..T-38 | 4 |
| **Total** | | **38** |

## 4. Pruebas existentes que habrá que revisar (no modificar ahora)

| Prueba | Por qué |
|---|---|
| `test_anchor_gates.py` | Presupone que A se congela al empezar B; con el nuevo ciclo de vida el punto de congelación puede cambiar |
| `test_post_cut_gates.py` | Presupone CUT y genealogía actuales; Q3 puede cambiar la referencia |
| `test_big_b_aut.py` | La matemática de B/AUT se conserva, pero la prueba debe añadir que B Grande y AUT no coexisten |
| `test_transformations.py` | Debe seguir pasando sin cambios: es la guardia constitucional |

## 5. Qué debe pasar **antes** de programar

No es razonable exigir que las 38 pruebas funcionales pasen antes de implementar: hoy fallarían todas. Lo que debe cumplirse antes de escribir código es:

1. **Reproducibilidad de la auditoría:** 21/21 deterministas, 262/262 prefijos, cero excepciones. **Ya se cumple.**
2. **Aceptación del plan de pruebas** por el propietario del proyecto.
3. **Respuestas a Q1–Q7** de `FREEBUFF_EXPERT_QUESTIONS_v219.md`, o marca explícita de `BLOCKED` en las pruebas afectadas.
4. **Decisión sobre el hash autoritativo** de R5 (A vs B).
5. **Confirmación de que el árbol sigue WORKING_CANON_NOT_FROZEN** y de que la implementación no lo declarará congelado.

Sin 2–5, cualquier implementación introduciría decisiones de diseño no autorizadas.

## 6. Orden de ejecución recomendado (cuando se autoricen)

```text
1. T-35..T-38  (constitucionales, deben pasar siempre)
2. T-01..T-05  (bootstrap de 1)
3. T-06..T-12  (2 y 3)
4. T-13..T-17  (módulo)
5. T-18..T-22  (A, B, AUT)
6. T-23..T-27  (gap)
7. T-31..T-34  (autoridad y conocimiento)
8. T-28..T-30  (capas, cuando existan TT/FT/CUT)
```

Las pruebas de cada bloque deben escribirse **antes** de la corrección correspondiente y fallar por la razón esperada. Una prueba que pasa antes de implementar no está midiendo el concepto.
