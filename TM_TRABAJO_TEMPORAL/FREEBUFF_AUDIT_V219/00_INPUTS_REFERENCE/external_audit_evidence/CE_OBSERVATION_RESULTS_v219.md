# CE_OBSERVATION_RESULTS_v219

Ejecución observacional · 2026-10-30 · motor `0.7.5.2-R5` (`9BD1BEDB…`, sin modificar) · árbol `94A1408A…` · 21 secuencias sintéticas + prefijos + doble ejecución.

## 0. CHECKPOINT TEMPRANO (fallo constitucional)

**Concepto:** CE-1 / CE-3 — el lector primario no construye la escalera funcional. No existe un `1` estructural: el motor solo consolida un `MODULE` cuando aparece un movimiento adverso **≥ 6,00** y, al hacerlo, se detiene en la pregunta `DONDE_NACE_A`. Nunca emite `2`, `3`, `A`, `B`, `C`, `TT`, `CUT` ni `AUT` en ninguna de las 21 secuencias.

- **Primer tick divergente:** CE-1, tick 2 (precio 101,00): debería existir `1`; el motor no tiene ninguna lectura.
- **Causa raíz:** RC-1 — el módulo se materializa tarde y como subproducto de `A`, en lugar de que `1` sea la estructura desde su primer desplazamiento.
- **Secuencias afectadas:** 18 de 21 (CE-1 ×3, CE-2 ×3, CE-3 ×3, CE-4 ×3, CE-5 ×3, CE-7 ×3). Sobre CE-6 pesa además RC-2.
- **¿Es seguro continuar en observación?** Sí: es determinista, no usa información futura a nivel de estado y no inventa semántica en las ramas abiertas. El bloqueo es de cobertura funcional, no de estabilidad.

Consecuencia: ninguna prueba puede clasificarse `BLOCKED` por R-01/R-02/R-04, porque el motor no llega a esas ramas; se registran como no evaluables por RC-1.

## 1. Resumen ejecutivo

| Métrica | Valor |
|---|---|
| Secuencias ejecutadas | 21/21 |
| PASS_CONCEPT | 0 |
| FAIL_CONCEPT | 13 |
| INCONCLUSIVE_TEST_SETUP | 8 |
| FAIL_LOCAL_IMPLEMENTATION | 0 |
| BLOCKED | 0 |
| ENGINE_EXCEPTION | 0 |
| EXPECTATION_CONTRADICTION | 0 |
| TREE_PRECEDENCE_CONFLICT | 0 |
| Determinismo | 21/21 |
| Consistencia de prefijos | 21/21 |
| Vocabulario de eventos observado | `1:FIRST`, `1:MODULO_CONSOLIDADO_CONFIRMADO`, `GAP` |

Una sola causa raíz (RC-1) explica 18 secuencias; una segunda (RC-2) explica la resolución del gap. No hay siete fallos: hay **dos errores conceptuales** y varios efectos propagados.

## 2. Resultado de las 21 secuencias

| Caso | CE | Variante | Tick | Precio | Esperado | Obtenido | Estado |
|---|---|---|---|---|---|---|---|
| CE1-POS | CE-1 | positivo | 2 | 101,00 | `1` abierta | sin lectura | FAIL_CONCEPT |
| CE1-NEG | CE-1 | negativo | 2 | 101,00 | `1` abierta; `2` imposible | sin lectura | FAIL_CONCEPT |
| CE1-FRON | CE-1 | frontera | 2 | 101,00 | `2` en 104,00 exactos | sin lectura | FAIL_CONCEPT |
| CE2-POS | CE-2 | positivo | 4 | 10,00 | módulo 0→10; A/B/C/TT | sin lectura | FAIL_CONCEPT |
| CE2-NEG | CE-2 | negativo | 4 | 10,00 | premisa C activa | sin lectura | INCONCLUSIVE |
| CE2-FRON | CE-2 | frontera | 4 | 10,00 | CUT en 0,00 exactos | sin lectura | INCONCLUSIVE |
| CE3-POS | CE-3 | positivo | 2 | 3,00 | `1`; `2` candidata/confirmada | sin lectura | FAIL_CONCEPT |
| CE3-NEG | CE-3 | negativo | 2 | 3,00 | premisa `1` con cierre 6,00 | sin lectura | INCONCLUSIVE |
| CE3-FRON | CE-3 | frontera | 2 | 3,00 | `2` en 12,00 exactos | sin lectura | FAIL_CONCEPT |
| CE4-POS | CE-4 | positivo | 2 | 5,00 | dos lecturas concurrentes | sin lectura | FAIL_CONCEPT |
| CE4-NEG | CE-4 | negativo | 2 | 5,00 | premisa módulo 20 | sin lectura | INCONCLUSIVE |
| CE4-FRON | CE-4 | frontera | 2 | 5,00 | premisa módulo 20 | sin lectura | INCONCLUSIVE |
| CE5-POS | CE-5 | positivo | 2 | 4,00 | TT con knowledge en el tick | sin lectura | FAIL_CONCEPT |
| CE5-NEG | CE-5 | negativo | 2 | 4,00 | premisa TT pendiente | sin lectura | INCONCLUSIVE |
| CE5-FRON | CE-5 | frontera | 2 | 4,00 | TT en 16,00 exactos | sin lectura | FAIL_CONCEPT |
| CE6-POS | CE-6 | positivo | 5 | 110,00 | A/B/A-tendencia + nuevo 1 | GAP solamente | FAIL_CONCEPT |
| CE6-NEG | CE-6 | negativo | 5 | 100,10 | premisa `1` y apertura plana | sin lectura | INCONCLUSIVE |
| CE6-FRON | CE-6 | frontera | 5 | 100,25 | gap + resolución implícita | GAP solamente | FAIL_CONCEPT |
| CE7-AUT | CE-7 | A/base | 5 | 20,00 | módulo 20; AUT + nuevo 1 | sin lectura | FAIL_CONCEPT |
| CE7-C-NEG | CE-7 | C sin CUT | 5 | 25,00 | premisa módulo 25 y C=7 | sin lectura | INCONCLUSIVE |
| CE7-C-FRON | CE-7 | C/CUT | 5 | 25,00 | CUT en 25,00 | sin lectura | FAIL_CONCEPT |

## 3. Cobertura por CE

| CE | Secuencias | FAIL | INCONCLUSIVE | PASS | Concepto observable |
|---|---|---|---|---|---|
| CE-1 | 3 | 3 | 0 | 0 | no |
| CE-2 | 3 | 1 | 2 | 0 | no |
| CE-3 | 3 | 2 | 1 | 0 | no |
| CE-4 | 3 | 1 | 2 | 0 | no |
| CE-5 | 3 | 2 | 1 | 0 | no |
| CE-6 | 3 | 2 | 1 | 0 | parcial (solo umbral de gap) |
| CE-7 | 3 | 2 | 1 | 0 | no |

## 4. Primera divergencia causal

| Caso | Tick | Precio | Condición lógica que diverge | Función/línea responsable | Propagación |
|---|---|---|---|---|---|
| CE1-POS | 2 | 101,00 | no nace `1` al primer desplazamiento | `MovementBuilder.feed` 351 + consolidación en `_update` | sin `1` no hay `2` |
| CE1-NEG | 2 | 101,00 | ídem | ídem | sin `2`, sin A Grande |
| CE1-FRON | 2 | 101,00 | ídem | ídem | sin frontera evaluable |
| CE2-POS | 4 | 10,00 | módulo no es el movimiento `1` | `_create_module`/consolidación | A/B/C/TT nunca |
| CE2-NEG | 4 | 10,00 | ídem | ídem | premisa ausente |
| CE2-FRON | 4 | 10,00 | ídem | ídem | premisa ausente |
| CE3-POS | 2 | 3,00 | no nace `1` | `MovementBuilder` | `2` inexistente |
| CE3-NEG | 2 | 3,00 | ídem | ídem | premisa ausente |
| CE3-FRON | 2 | 3,00 | ídem | ídem | `2` inexistente |
| CE4-POS | 2 | 5,00 | no hay lectura principal ni local | `_make_local_reading` nunca invocada | concurrencia imposible |
| CE4-NEG | 2 | 5,00 | ídem | ídem | premisa ausente |
| CE4-FRON | 2 | 5,00 | ídem | ídem | premisa ausente |
| CE5-POS | 2 | 4,00 | no nace `1` | `MovementBuilder` | TT nunca evaluado |
| CE5-NEG | 2 | 4,00 | ídem | ídem | premisa ausente |
| CE5-FRON | 2 | 4,00 | ídem | ídem | TT inexistente |
| CE6-POS | 5 | 110,00 | gap no resuelve funciones | `_schedule_gap` 1545 / rama gap 3009 | sin nuevo 1 |
| CE6-NEG | 5 | 100,10 | premisa `1` ausente | `MovementBuilder` | premisa ausente |
| CE6-FRON | 5 | 100,25 | gap correcto; resolución ausente | `_schedule_gap` | sin nuevo 1 |
| CE7-AUT | 5 | 20,00 | módulo no existe hasta el primer adverso ≥6,00 | consolidación | AUT nunca |
| CE7-C-NEG | 5 | 25,00 | ídem | ídem | premisa ausente |
| CE7-C-FRON | 5 | 25,00 | ídem | ídem | CUT nunca |

## 5. Errores conceptuales confirmados

1. **RC-1 — `1` no es estructura.** El módulo se crea solo ante un movimiento adverso ≥6,00 (`MOVE`) y su extremo es el máximo recorrido previo, no el movimiento `1`. Evidencia: CE2 tick 19, módulo `0,00 → 16,00` cuando el `1` canónico es `0,00 → 10,00`; CE7 tick 15, módulo `25,00 → −0,25`.
2. **RC-2 — el gap no resuelve funciones.** El evento `GAP` se registra con el valor correcto, pero no hay A/B/A-tendencia implícitas ni nuevo 1 desde la apertura.
3. **Ausencia total de `2` y `3`** en el lector primario: el vocabulario de eventos no los contiene en ninguna secuencia.

## 6. Errores locales independientes

Ninguno confirmado. Los fallos locales observados (módulo tardío, módulo sobredimensionado, TT no evaluado) son consecuencias de RC-1, no defectos aislados.

## 7. Efectos propagados

- `2`/`3` ausentes → `A` no nace → `B`/`B Grande` no nacen → `C` no nace → `TT`/`CUT` nunca se evalúan.
- `AUT` no se dispara porque depende de `B`/`A`; la lectura local nunca se arma.
- `ft` queda siempre `False`; `aut_time`, `b_grande_time` y `cut_confirmed` nunca se llenan.
- La pregunta activa permanece `DONDE_NACE_A` de forma indefinida.

## 8. Casos bloqueados por R-01/R-02/R-04

No evaluables: el motor no alcanza `TERCERO`, `FT` ni `L2/L3`. No hay evidencia de que R5 invente una resolución; simplemente no llega. R-03, R-05, R-06 y R-07 tampoco se ejercitan.

## 9. Riesgos de información futura

Ninguno detectado: los 262 prefijos ejecutados coinciden con el estado del tick correspondiente en la ejecución completa. El módulo tardío usa solo precios pasados (extremo ya ocurrido), no futuros.

## 10. Determinismo

21/21 deterministas: mismos eventos, estados, extremos y tiempos en dos ejecuciones limpias. Sin `NON_DETERMINISTIC_ENGINE`.

## 11. Corroboración con replays reales

No ejecutados en esta fase: la prueba mínima ya identifica la causa y el replay no puede sustituirla. El replay de 16:22-16:29 queda disponible como corroboración posterior (mismo concepto: lectura que solo aparece tras un adverso ≥6,00).

## 12. Agrupación por causa raíz

| Causa | Secuencias | Estado |
|---|---|---|
| RC-1 (escalera funcional/módulo) | 18 | 13 FAIL + 5 INCONCLUSIVE |
| RC-2 (resolución del gap) | 2 (CE6-POS/FRON) | FAIL |
| RC-1a (medida del módulo) | subconjunto de RC-1 | efecto, no causa |

## 13. Conceptos que R5 comprende correctamente

- Umbral plano/gap: 0,10 no es gap; 0,25 exactos sí (CE3-NEG, CE6-FRON).
- Determinismo y ausencia de información futura en el estado.
- No inventa `TT`, `FT`, `CUT`, `AUT` ni `2`/`3` cuando no corresponden (no resuelve ramas abiertas).
- Límite de lecturas activas respetado.

## 14. Conceptos que comprende parcialmente

- **CE-6:** detecta el gap y su frontera, pero no su resolución funcional.
- **CE-1:** mide desplazamiento direccional para consolidar, pero con umbral 6,00 y sin `1` previo.

## 15. Conceptos ausentes o incorrectos

- CE-1 (finalidad vs tamaño), CE-2 (capas función/patrón/estado), CE-3 (autoridad única y `2` pendiente), CE-4 (escalas concurrentes), CE-5 (tiempo de conocimiento del TT), CE-7 (transformación funcional).

## 16. Preguntas expertas todavía necesarias

Solo las tres ya abiertas: R-01 (velocidad), R-02 (tick/variables del FT), R-04 (apertura y prioridad L2/L3). R-03, R-05, R-06 y R-07 no se ejercitan en estas secuencias.

## 17. Nodos y pruebas que desbloquearía cada respuesta

| Respuesta | Desbloquea |
|---|---|
| R-01 | CE-7 rama TERCERO; TEST-C-001…004; N-023, N-027 |
| R-02 | CE-5 FT; N-026, N-039; golden de velas 8-9 |
| R-04 | CE-3/CE-4 concurrencia; N-028…N-030 |

## 18. Orden recomendado de corrección (sin programar aún)

1. **RC-1:** `1` como estructura desde el primer desplazamiento y escalera `1/2/3/A/B/C` en el lector primario.
2. **RC-1a:** módulo = movimiento `1`, no recorrido total al extremo.
3. **RC-2:** resolución funcional del gap (v2.19 §A-C).
4. **R-02** y **R-01/R-04** solo después de que la escalera exista y sea observable.

Ninguna corrección se aplica en esta fase: motor, goldens y árbol intactos.

