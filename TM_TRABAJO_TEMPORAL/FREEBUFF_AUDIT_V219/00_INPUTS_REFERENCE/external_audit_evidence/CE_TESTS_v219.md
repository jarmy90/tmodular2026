# CE_TESTS_v219

**Pruebas de concepto CE-1…CE-7** · 2026-10-30
Expectativas tomadas del árbol (`94A1408A…`) y de `SEMANTIC_TRANSITIONS.csv`. El motor R5 (`9BD1BEDB…`) no se modifica y su salida no define la expectativa.

## Protocolo

Cada prueba verifica la cadena causal completa:

```text
estado recibido -> pregunta activa -> movimiento observado -> funcion pendiente
-> confirmacion o imposibilidad -> transicion siguiente
```

- No basta una etiqueta final: se comprueba el `state_log` de cada tick.
- Precios en puntos, ticks de 0,25. `|` separa velas.
- Si R5 falla: se conserva la salida original, se identifica el **primer tick divergente**, se informa el error conceptual y **no** se corrige el Python, **no** se adapta la expectativa y **no** se toca ningún golden.
- Las secuencias son sintéticas y no deben convertirse en fixtures.

---

## CE-1 — El tamaño no sustituye a la finalidad

1. **CONCEPTO TM:** una función existe por su desplazamiento direccional y su referencia, no por superar un tamaño. v2.5 §D: la lectura se realiza siempre.
2. **ERROR QUE EVITA:** F-01/F-02/F-03/F-04/F-05: `1` desde el high-low de la vela, funciones que nacen por 2,00/6,00, `3` por magnitud, módulo como diagonal, FT por retroceso.
3. **MOVIMIENTO MÍNIMO:** `1` alcista de 2,00 puntos y `2` que alcanza exactamente 2,00 desde su apertura.
4. **ESTADO ESTRUCTURAL RECIBIDO:** `SIN_LECTURA`.
5. **SECUENCIA DE TICKS SINTÉTICA:**

```text
V1: 100,00 | 101,00 | 102,00 | 101,75 | 102,00
V2: 102,00 | 102,75 | 103,50 | 104,00 | 104,25
```

6. **PREGUNTA ACTIVA:** ¿el primer recorrido direccional abre `1` aunque mida 2,00? ¿`2` se confirma al alcanzar el desplazamiento de `1`?
7. **RESULTADO ESPERADO:** `1` abierta en 101,00 (origen 100,00, extremo 102,00, rango 2,00); `2_CANDIDATA` al abrir V2 en plano; `2_CONFIRMADA` en 104,00 (desplazamiento 2,00 = rango de 1) y vigente en 104,25.
8. **RESULTADO PROHIBIDO:** no abrir lectura hasta 6,00; ignorar V1; crear `1` con rango 0; confirmar `2` por high-low; exigir 6,00 para cualquier función.
9. **CASO POSITIVO:** la secuencia completa.
10. **CASO NEGATIVO:** V2 abre 102,00 y cae a 101,50 → `2` imposible, `1` = módulo por descarte y A Grande bajista (no hay `2`).
11. **CASO FRONTERA:** `2` alcanza 104,00 exactos → confirma (≥), no queda pendiente.
12. **PREFIJO ANTES DE CONFIRMACIÓN:** en 102,75 y 103,50 el estado debe decir `2_CANDIDATA` con medida 0,75/1,50.
13. **CONTINUIDAD ENTRE VELAS:** V1 cierra en 102,00 y V2 abre en 102,00 (plano); `1` no se cierra al cambiar de vela.
14. **LECTURA CONCURRENTE:** no aplica.
15. **INVARIANTES:** ninguna confirmación antes de su condición; medida = desplazamiento direccional; 0,25 exactos no es plano; sin umbral inventado.
16. **NODOS AFECTADOS:** N-001, N-002, N-006, N-007, N-012, N-040.
17. **FUNCIONES R5 AFECTADAS:** `MovementBuilder`, `_close_candidate_bar`, `_process_local_sequence`.
18. **REPLAY REAL DE APOYO:** vela 14 y 16:22 de v005 (solo como apoyo).

---

## CE-2 — Función, patrón y estado son capas distintas

1. **CONCEPTO TM:** `C` es función; `TT` es patrón; `CUT` es evento. Ninguno borra al otro (v1.2 §13.6, N-031, N-034).
2. **ERROR QUE EVITA:** F-06: TT/FT/CUT escritos en `state`; C emitida sobre `TT_EXT`; CUT como `fail_reason`.
3. **MOVIMIENTO MÍNIMO:** módulo de 10,00, A de 4,00, B de 5,00, C de 4,00 y TT al 100 % mientras C sigue activa.
4. **ESTADO ESTRUCTURAL RECIBIDO:** `MODULO` confirmado.
5. **SECUENCIA DE TICKS SINTÉTICA:**

```text
V1: 0,00 | 4,00 | 8,00 | 10,00
V2: 10,00 | 8,00 | 6,00
V3: 6,00 | 8,00 | 10,00 | 11,00
V4: 11,00 | 9,00 | 7,00
V5: 7,00 | 12,00 | 16,00
V6: 16,00 | 10,00 | 3,90
```

6. **PREGUNTA ACTIVA:** al confirmarse el TT, ¿sigue existiendo la función C? ¿el CUT se mide contra la base del módulo o contra `fin_A ± 2,00`?
7. **RESULTADO ESPERADO:** B Grande en 10,00 (100 % de A, sin AUT: 5,00 < 5,33); C en 7,00; TT confirmado en 16,00 (`fin_A` 6,00 + módulo 10,00); con el precio en 3,90 la función sigue siendo `C` y **no hay CUT** (C no alcanzó la base 0,00); el historial conserva TT confirmado.
8. **RESULTADO PROHIBIDO:** sustituir `C` por `TT_EXT`; emitir `C` estando en `TT_EXT`; CUT en 4,00 (`fin_A − 2,00`); cerrar la lectura por FT/CUT sin condición.
9. **CASO POSITIVO:** la secuencia completa.
10. **CASO NEGATIVO:** en V4 el precio cae a 0,00 (base) → CUT + nuevo 1 + reset; la función C deja de ser vigente por evento, no por patrón.
11. **CASO FRONTERA:** C llega exactamente a 0,00 → CUT (v1.2: «alcanza o supera»).
12. **PREFIJO ANTES DE CONFIRMACIÓN:** en V5 con 12,00 el patrón debe estar `TT_POSIBLE` y la función `C` vigente.
13. **CONTINUIDAD ENTRE VELAS:** el TT cruza de V4 a V5 sin reiniciar la lectura.
14. **LECTURA CONCURRENTE:** no aplica en este caso; se cubre en CE-4.
15. **INVARIANTES:** función, patrón y evento coexisten; TT no cierra la lectura; CUT exige condición; historial no se borra.
16. **NODOS AFECTADOS:** N-017, N-018, N-019, N-021, N-022, N-024, N-031, N-034.
17. **FUNCIONES R5 AFECTADAS:** `_update`, `_check_tt`, `_check_cut`, `_pattern`, `begin_c`.
18. **REPLAY REAL DE APOYO:** 16:23 y velas 8-9 de v005.

---

## CE-3 — Una sola autoridad de «qué función viene ahora»

1. **CONCEPTO TM:** por lectura y tick existe una sola función esperada y una sola condición de confirmación.
2. **ERROR QUE EVITA:** F-07/F-08: dos máquinas en paralelo, «pendiente» confundido con «imposible».
3. **MOVIMIENTO MÍNIMO:** `1` de 6,00 y `2` que no confirma en su vela pero sigue cumpliendo N-006.
4. **ESTADO ESTRUCTURAL RECIBIDO:** `1_ACTIVA`.
5. **SECUENCIA DE TICKS SINTÉTICA:**

```text
V1: 0,00 | 3,00 | 6,00
V2: 6,00 | 7,00 | 8,00 | 9,00 | 10,00 | 11,00 | 11,75
V3: 11,75 | 12,25
```

6. **PREGUNTA ACTIVA:** ¿`2` sigue pendiente al cerrar V2 sin alcanzar 6,00? ¿cuántas lecturas y transiciones produce el mismo tick?
7. **RESULTADO ESPERADO:** una sola lectura; `2_CANDIDATA` con 5,75 al cierre de V2; `2_CONFIRMADA` en 12,25 de V3 (6,25 ≥ 6,00); un único `next_function` por tick en el `state_log`.
8. **RESULTADO PROHIBIDO:** declarar `2` imposible al cerrar V2; crear `LR####` sin regla expresa; dos lecturas para el mismo tramo; emitir dos transiciones contradictorias en el mismo tick.
9. **CASO POSITIVO:** la secuencia completa.
10. **CASO NEGATIVO:** V2 abre con gap (Δ > 0,25) → `2` imposible de inmediato y rama de gap (CE-6).
11. **CASO FRONTERA:** V2 cierra en 12,00 exactos → `2` confirmada en el cierre, sin prórroga.
12. **PREFIJO ANTES DE CONFIRMACIÓN:** los cinco ticks de V2 deben mostrar `2_CANDIDATA` creciente.
13. **CONTINUIDAD ENTRE VELAS:** V2→V3 con apertura plana; la candidata sobrevive.
14. **LECTURA CONCURRENTE:** ninguna apertura automática por AUT/CUT mientras no exista regla (N-028/N-029).
15. **INVARIANTES:** una autoridad; `pendiente` mientras exista camino; `imposible` solo si una condición queda negada; sin duplicados.
16. **NODOS AFECTADOS:** N-006, N-007, N-008, N-028, N-029, N-030, N-036.
17. **FUNCIONES R5 AFECTADAS:** `feed_chunk`, `_process_movement`, `_advance_primary_question`, `_process_local_sequence`, `_legacy_tick_decision`.
18. **REPLAY REAL DE APOYO:** secuencia 1639 de v005 (dos lecturas).

---

## CE-4 — Escalas y referencias concurrentes

1. **CONCEPTO TM:** cada lectura tiene su módulo y su objetivo; la dominancia se decide por estructura.
2. **ERROR QUE EVITA:** F-09: un `module_size` global, `_owner` por tamaño, TT de la lectura equivocada.
3. **MOVIMIENTO MÍNIMO:** lectura principal con módulo 20,00 y objetivo 30,00; lectura local con módulo 5,00 y objetivo 15,00.
4. **ESTADO ESTRUCTURAL RECIBIDO:** dos lecturas activas (principal y local).
5. **SECUENCIA DE TICKS SINTÉTICA:**

```text
14,75 | 15,00 | 15,50 | 20,00 | 29,75 | 30,00
```

6. **PREGUNTA ACTIVA:** al tocar 15,00, ¿qué TT se confirma y a qué lectura pertenece el tick?
7. **RESULTADO ESPERADO:** TT local confirmado en 15,00 (objetivo local); TT principal `PENDIENTE`; dueño del tick = lectura local por estructura; TT principal confirmado en 30,00.
8. **RESULTADO PROHIBIDO:** confirmar el TT principal en 15,00; cerrar la lectura principal; elegir dueño por `module_size`; recalcular el objetivo local con el módulo principal.
9. **CASO POSITIVO:** la secuencia completa.
10. **CASO NEGATIVO:** solo lectura principal activa → 15,00 no confirma nada.
11. **CASO FRONTERA:** 15,00 exactos → TT local confirmado (≥).
12. **PREFIJO ANTES DE CONFIRMACIÓN:** en 14,75 ambos TT deben estar `POSIBLE`, cada uno con su objetivo.
13. **CONTINUIDAD ENTRE VELAS:** no aplica.
14. **LECTURA CONCURRENTE:** es el objeto de la prueba; ninguna lectura borra a la otra.
15. **INVARIANTES:** objetivo por lectura; dominancia por estructura; sin mezcla de módulos; máximo 3 lecturas.
16. **NODOS AFECTADOS:** N-012, N-014, N-018, N-028, N-029, N-030, N-034.
17. **FUNCIONES R5 AFECTADAS:** `_make_local_reading`, `_owner`, `tt_target`, `_snapshot_state`.
18. **REPLAY REAL DE APOYO:** 16:22 de v005.

---

## CE-5 — Tiempo estructural y momento de conocimiento

1. **CONCEPTO TM:** el TT se confirma en el primer tick que alcanza el 100 %; el conocimiento no puede llegar después (v2.6 §C, N-019, N-039).
2. **ERROR QUE EVITA:** F-10: TT/FT descubiertos al cerrar un movimiento; confirmaciones retroactivas.
3. **MOVIMIENTO MÍNIMO:** objetivo TT de 16,00 alcanzado y perdido en ticks posteriores.
4. **ESTADO ESTRUCTURAL RECIBIDO:** `TT_PENDIENTE` con `fin_A` 6,00 y módulo 10,00.
5. **SECUENCIA DE TICKS SINTÉTICA:**

```text
14,00 | 15,75 | 16,00 | 15,75 | 15,50 | 15,25 | 15,00 | 14,00
```

6. **PREGUNTA ACTIVA:** ¿en qué tick queda confirmado el TT y qué `knowledge_time` se registra?
7. **RESULTADO ESPERADO:** TT confirmado en 16,00, con `knowledge_time` = tick de 16,00; sigue confirmado tras el retroceso; FT no se declara (variables pendientes, R-02).
8. **RESULTADO PROHIBIDO:** confirmar el TT en 10,00 (tras 6,00 de retroceso); confirmarlo al cerrar un movimiento; retirar la confirmación al retroceder; declarar FT por 6,00.
9. **CASO POSITIVO:** la secuencia completa.
10. **CASO NEGATIVO:** el precio llega a 15,75 y gira → TT sigue `PENDIENTE`.
11. **CASO FRONTERA:** 16,00 exactos → confirmado; 15,75 → no.
12. **PREFIJO ANTES DE CONFIRMACIÓN:** 14,00 y 15,75 con TT `POSIBLE` y objetivo 16,00.
13. **CONTINUIDAD ENTRE VELAS:** la confirmación en 16,00 se conserva al cambiar de vela.
14. **LECTURA CONCURRENTE:** el retroceso no crea nueva lectura sin regla.
15. **INVARIANTES:** `structural_time ≤ confirmation_time ≤ knowledge_time`; confirmación no retroactiva; TT no se retira por retroceso.
16. **NODOS AFECTADOS:** N-013, N-019, N-021, N-026, N-039.
17. **FUNCIONES R5 AFECTADAS:** `_process_movement`, `_check_tt`, `_record_knowledge`, `_snapshot_state`.
18. **REPLAY REAL DE APOYO:** velas 8-9 de v005.

---

## CE-6 — El gap como resolución funcional

1. **CONCEPTO TM:** el tramo no negociado resuelve A → B Grande → A usada como tendencia implícitas y el nuevo 1 nace en la apertura de la segunda vela (v2.19 §A-C).
2. **ERROR QUE EVITA:** F-11: gap tratado como bloqueo o dato raro.
3. **MOVIMIENTO MÍNIMO:** cierre 100,00 y apertura 110,00.
4. **ESTADO ESTRUCTURAL RECIBIDO:** `1_ACTIVA` con cierre previo 100,00.
5. **SECUENCIA DE TICKS SINTÉTICA:**

```text
V1: ... | 100,00
V2: 110,00 | 110,50 | 109,75 | 111,00
```

6. **PREGUNTA ACTIVA:** ¿qué funciones resuelve el gap y dónde nace el nuevo 1?
7. **RESULTADO ESPERADO:** A Grande implícita, B Grande implícita y A usada como tendencia implícita registradas sin precios internos; nuevo 1 con origen 110,00, `structural_time` = `knowledge_time` = 110,00; lectura tick a tick desde 110,00; `2` prohibida.
8. **RESULTADO PROHIBIDO:** una sola A Grande de 100,00 a 110,00; nuevo 1 desde el cierre previo; inventar precios internos; evaluar `2`; continuar desde una referencia anterior a la apertura.
9. **CASO POSITIVO:** la secuencia completa.
10. **CASO NEGATIVO:** apertura 100,10 (plano) → sin funciones implícitas.
11. **CASO FRONTERA:** apertura 100,25 exactos → gap (0,25 no es plano).
12. **PREFIJO ANTES DE CONFIRMACIÓN:** el evento de gap debe preceder a las funciones implícitas en el mismo tick de apertura.
13. **CONTINUIDAD ENTRE VELAS:** V1 cierra 100,00; V2 abre 110,00; no se mide desde 100,00 tras la apertura.
14. **LECTURA CONCURRENTE:** el nuevo 1 no borra el historial del módulo previo.
15. **INVARIANTES:** ningún precio inventado; origen = OPEN; no `2` con gap; tiempos canónicos.
16. **NODOS AFECTADOS:** N-002, N-003, N-004 (sustituidos), N-021.
17. **FUNCIONES R5 AFECTADAS:** `_schedule_gap`, `_process_local_sequence` (rama gap), `_make_local_reading`.
18. **REPLAY REAL DE APOYO:** 16:24-16:25 de v005 (gap 14,00).

---

## CE-7 — Transformación funcional, no sustitución

1. **CONCEPTO TM:** una función se transforma conservando identidad y genealogía; el nuevo 1 es el resultado de la transformación (v2.17, v2.19, v1.2 §13).
2. **ERROR QUE EVITA:** F-12: nueva lectura dominante en cada cruce, motivos no canónicos, `TERCERO` ausente.
3. **MOVIMIENTO MÍNIMO:** A que cruza la base del módulo; C que supera la base del módulo.
4. **ESTADO ESTRUCTURAL RECIBIDO:** `MODULO` con A Grande activa.
5. **SECUENCIA DE TICKS SINTÉTICA (caso A):**

```text
V1: 0,00 | 5,00 | 10,00 | 15,00 | 20,00
V2: 20,00 | 15,00 | 10,00 | 5,00 | -1,00 | -3,00
```

**Secuencia (caso C, módulo 20,00):** `1` 25,00 a la baja, A 4,00 al alza, B 4,25 a la baja, C 25,00 al alza.

6. **PREGUNTA ACTIVA:** ¿el cruce de la base transforma la función o crea otra lectura? ¿qué motivo de transición se registra?
7. **RESULTADO ESPERADO (A):** al cruzar 0,00, AUT bajista + nuevo 1 en el mismo movimiento + reset; `transition_reason = A_USED_AS_TREND`; misma genealogía, sin lectura independiente.
   **Resultado esperado (C):** C recorre 25,00 > módulo 20,00 → CUT + nuevo 1 + reset inmediato; motivo `C_USED_AS_TREND` en el historial.
8. **RESULTADO PROHIBIDO:** crear lectura dominante nueva por el cruce; medir el CUT contra `fin_A ± 2,00`; convertir C en nuevo 1 sin comprobar la base; elegir rápido/lento por apariencia.
9. **CASO POSITIVO:** ambos casos.
10. **CASO NEGATIVO:** C de 7,00 sobre módulo 20,00 → C Grande sigue, sin CUT y sin reset.
11. **CASO FRONTERA:** C = 20,00 exactos → CUT («alcanza o supera»).
12. **PREFIJO ANTES DE CONFIRMACIÓN:** C debe mostrarse como `C_GRANDE` con su medida desde el extremo de B antes de comparar la base.
13. **CONTINUIDAD ENTRE VELAS:** el cruce puede ocurrir en vela distinta a la de B; la referencia no se reinicia antes del evento.
14. **LECTURA CONCURRENTE:** la transformación no borra el TT pendiente de la lectura mayor (doble pertenencia, v1.2 §13).
15. **INVARIANTES:** identidad conservada; motivo canónico; CUT contra base; reset solo tras CUT/AUT que lo exija; rama de velocidad bloqueada (R-01).
16. **NODOS AFECTADOS:** N-017, N-021, N-022, N-024, N-025, N-034.
17. **FUNCIONES R5 AFECTADAS:** `_new_local_reading_after_aut`, `_reclassify_c_as_new_1`, `_check_cut`, `cut_crosses`, `BigBTracker`.
18. **REPLAY REAL DE APOYO:** 16:23 de v005; TEST-C-001…004 de v1.2 §13.10.

---

## Cierre

| CE | Casos | Regla abierta que solo bloquea una rama |
|---|---|---|
| CE-1 | 3 | ninguna |
| CE-2 | 3 | ninguna |
| CE-3 | 3 | R-04 (L2/L3) |
| CE-4 | 3 | R-04 |
| CE-5 | 3 | R-02 (tick/variables de FT) |
| CE-6 | 3 | ninguna |
| CE-7 | 3 | R-01 (velocidad → TERCERO) |

Ninguna prueba exige respuesta de Javier para ejecutarse: las ramas bloqueadas se marcan `BLOCKED` y el resto se verifica con la expectativa canónica. Si R5 falla, el resultado se registra como hallazgo; no se corrige el motor en esta fase.
