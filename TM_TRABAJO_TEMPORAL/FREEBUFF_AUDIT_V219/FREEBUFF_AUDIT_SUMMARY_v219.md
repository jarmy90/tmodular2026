# FREEBUFF_AUDIT_SUMMARY_v219

**Auditoría conceptual profunda de R5 y preparación del motor ejecutable**
**Fecha:** 2026-10-30
**Árbol:** `94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17` (WORKING_CANON_NOT_FROZEN)
**Motor auditado:** R5 `9BD1BEDB5DEC8C5A1C3A831338503E90CC04EE3CD776CF4E01D27CF8AA0EBEAE`
**Variante empaquetada:** R5 `19A847C078E124616495E85A832F9D2FA12A371413046CBAEB7E9644D47C6A36` (no usada como línea base)
**Versión documental:** 1.0 · **Versión del motor:** `0.7.5.2-R5`
**Estado:** auditoría terminada, sin cambios en motor, árbol, tests, goldens ni ZIP
**tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

---

## 0. Qué se ejecutó y qué se verificó

| Comprobación | Resultado |
|---|---|
| 21 secuencias CE desde ticks sintéticos | 21/21 ejecutadas |
| Doble ejecución limpia | 21/21 idénticas |
| Prefijos comparados | 262/262 sin divergencia |
| Excepciones | 0 |
| Uso de información futura | no detectado |
| Dependencia de goldens desde el motor | no detectada |
| Integridad de entradas | árbol, tickfeed, v005, R3 y R5 con hash esperado |
| Copia de evidencia externa | 6 archivos, bytes y hash preservados |
| Suite existente contra R5 | 28/28 tests pasan |
| Secuencias con `2/3/A/B/C/AUT/CUT/TT` | 0/21 |
| Secuencias con alguna lectura | 7/21 |

No se activó ninguna condición de parada temprana: las 21 secuencias son reproducibles, R5 es ejecutable, no hay información futura, no hay no-determinismo, no hay dependencia encubierta de goldens y los inputs están íntegros.

La única diferencia relevante con OpenBot es de atribución: **19** secuencias carecen de estructura `1`, no 18; CE6-NEG también carece de `1` aunque su premisa sea distinta. Se detalla en `FREEBUFF_CE_REPRODUCTION_v219.md` §7.

## A. ¿Cuál es el primer error conceptual real de R5?

**La unidad de decisión es el movimiento cerrado, no el estado funcional por tick.**

R5 no decide "qué función cumple este desplazamiento ahora"; decide "qué función cumplía el movimiento que acaba de cerrarse". `MovementBuilder` solo cierra un movimiento cuando el precio retrocede `max(6,00; 25 %)` desde su extremo (R5:333-390). Hasta ese tick no hay dirección, ni origen funcional, ni pregunta.

Ese error se materializa por primera vez en el tick 2 de CE-1: el precio ya se ha desplazado 1,00 punto y el árbol ya exige `1`; R5 no tiene nada.

## B. ¿Qué movimiento no comprende?

No comprende el **movimiento en curso**. Comprende el movimiento ya terminado y lo etiqueta retrospectivamente.

- No comprende un `1` que nace, crece y todavía no ha sido puesto a prueba.
- No comprende una `2` que se desarrolla dentro de su vela con vibraciones internas.
- No comprende una `A` que empieza en el extremo y aún no ha retrocedido 6,00.
- No comprende una `B` que oscila sin superar el 100 %.
- No comprende un gap como tramo funcional sin ticks.

## C. ¿Qué representa incorrectamente?

| Concepto | R5 representa | El árbol exige |
|---|---|---|
| `1` | movimiento cerrado de ≥ 6,00, etiquetado `MODULE` | función desde el primer desplazamiento, con candidatura y congelación |
| módulo | recorrido total de la pata (`origin→extreme`) | referencia de la función `1` (y de `2/3` cuando existan) |
| `2` | fase local que solo se arma tras un AUT primario | pregunta inmediata tras `1` |
| `3` | nuevo extremo ≥ 2,00 | retroceso 0–50 % + superación del extremo de `2` |
| `A` | movimiento contrario cerrado de ≥ 6,00 | primer contrario estructural ≥ 2,00 |
| `B` | movimiento contrario cerrado de ≥ 6,00 | recorrido contrario con oscilaciones absorbidas |
| `C` | excursión de ≥ 6,00 (local) o cualquier tick (primaria) | contrario posterior a `B Grande` |
| `AUT` | superación estricta correcta, pero con `a_size ≥ 6,00` | superación estricta sin mínimo de tamaño |
| `TT` | evento al cerrar movimiento | confirmación en el tick que toca el objetivo |
| gap | evento informativo | resolución funcional implícita + nuevo `1` |
| función/patrón/evento | un solo campo `state` | tres capas que coexisten |

## D. ¿Qué funciones posteriores quedan inaccesibles?

Sin `1` funcional:

```text
2 → 3 → A → B → B Grande → AUT → C → CUT → TT → FT
```

Además:

- sin `AUT` primario no se arma la máquina `LOCAL`, que es la única que contiene `2/3`;
- sin movimiento contrario cerrado no hay `A`, aunque el giro sea evidente;
- sin `B Grande` no hay `C` ni `CUT`;
- sin `TT` confirmado no hay `FT`.

En las 21 CE no se emite **ninguna** de esas funciones. En la traza adicional sí se alcanzan `B Grande` y `AUT`, pero se pierde el TT y se viola N-037 (ambos en el mismo tick).

## E. ¿Por qué mide incorrectamente los módulos?

Porque el módulo se identifica con el **movimiento completo**, no con la función `1`:

```text
_create_reading: module_origin = movement.origin
                 module_extreme = movement.extreme      (R5:879-884)
_update MODULE:  module_extreme = movement.extreme      (R5:1074-1093)
module_size   = |module_extreme − module_origin|        (R5:254)
```

Cuando la pata contiene oscilaciones internas menores de 6,00, el constructor las absorbe y el módulo las incluye:

- CE-2: 0→16 en vez de 0→10;
- CE-7-C: 25→−0,25 en vez de 25→0.

**Matiz:** cuando la pata es monótona, el módulo es correcto (CE-4-NEG: 0→20). El error no es la fórmula, sino **la pertenencia de los ticks al movimiento**. Por eso no se corrige cambiando `module_size`, sino cambiando qué es un movimiento.

## F. ¿Es RC-1 una sola causa o varias causas?

**Una premisa, cuatro causas independientes.**

| Causa | Qué falla | Se puede corregir sola | Efecto aislado |
|---|---|---|---|
| RC-1.1 | no hay `ONE_CANDIDATE`; `1` exige movimiento cerrado | sí | habría `1`, pero la pregunta primaria seguiría siendo `A` |
| RC-1.2 | la escalera primaria no tiene `2/3`; la local exige AUT | sí | habría `2/3`, pero nunca arrancarían |
| RC-1.3 | el módulo absorbe `2/3` | sí | el módulo mediría bien, pero nacería tarde |
| RC-1.4 | A/B/C/AUT exigen 6,00 | sí | existirían funciones pequeñas, pero sobre un `1` inexistente |

La premisa común es "una función solo existe cuando un movimiento se cierra". Por eso **no basta un parche local**: hay que sustituir la unidad de decisión.

## G. ¿RC-2 depende de RC-1?

**Parcialmente.**

| Pieza de RC-2 | Depende de RC-1 |
|---|---|
| Detección del gap | no |
| `NO_TWO` con gap | no |
| Registro de A/B/A-tendencia implícitas | no (pueden ser eventos sin precios) |
| Nuevo `1` desde la apertura | **sí** (necesita el ciclo de vida de `1`) |
| Continuación tick a tick desde la apertura | **sí** |
| Rama local de gap | **sí** (LOCAL no se arma sin AUT) |

Orden correcto: primero el bootstrap de `1`, después la resolución del gap. Intentarlo al revés crearía otra lectura `MODULE` tardía.

## H. ¿Qué partes de R5 son reutilizables?

| Clasificación | Componentes |
|---|---|
| **KEEP** (14) | ingesta, `Pt/Bar`, normalización de precios, orden de ticks, serialización, eventos, knowledge/snapshot, serializadores, comparador de prefijos, `BigBTracker`, `local_two_gate`, cruces estrictos, tests de B/AUT, CLI |
| **KEEP_WITH_ADAPTER** (10) | esquema de eventos, comparadores v005/golden, `_two_impossible`, detección de gap, `_maybe_aut`, límite de 3 lecturas, `_reclassify_c_as_new_1`, `_shadow_compare`, tests de anclas, tests post-CUT |
| **REFACTOR** (5) | `Reading`, `_process_local_sequence`, `_advance_primary_question`, `_owner`, `dominant` |
| **REPLACE_SEMANTICS** (10) | `MovementBuilder` como unidad de decisión, `_create_reading`, `_update`, `_open_candidate`, `_process_movement`, `_close_candidate_bar`, `_new_local_reading_after_aut`, `_check_tt`, `_check_cut`, `MOVE` como umbral de lectura |
| **SHADOW_ONLY** (2) | `build_movements`, `_legacy_tick_decision` |
| **DEAD_CODE** (2 filas) | `A_SIGNIFICATIVA` / `A_DESPROPORCIONADA_MODULO`, `MIN_MODULE` |
| **UNKNOWN_PENDING_ANALYSIS** (1) | `coverage` / `AFS2` |

Detalle en `FREEBUFF_COMPONENT_REUSE_MATRIX_v219.csv` (44 componentes).

## I. ¿Qué decisiones expertas siguen abiertas?

Ocho, y solo ocho:

| ID | Duda |
|---|---|
| Q1 | cuándo se confirma y congela `1` |
| Q2 | 0,25 exactos: plano o gap |
| Q3 | CUT contra final de A o contra base del módulo |
| Q4 | nuevo `1` en AUT o en TT cuando el AUT no cruza la base |
| Q5 | módulo por desplazamiento direccional o por expansión del conjunto |
| Q6 | tick y condición del FT |
| Q7 | apertura y prioridad de lecturas concurrentes |
| Q8 | 50 % exacto en el retroceso de `3` |

Formato y consecuencias en `FREEBUFF_EXPERT_QUESTIONS_v219.md`. No se pregunta lo que el árbol ya cierra (2 con gap, B Grande al 100 %, AUT estricto, TT ≥ 100 %, C tras B, etc.).

## J. ¿Qué pruebas deben pasar antes de programar?

No es posible que las 38 pruebas funcionales pasen antes de implementar: hoy fallarían todas. Lo que debe cumplirse antes de escribir código es:

1. **Reproducibilidad de la auditoría** — 21/21 deterministas, 262/262 prefijos, cero excepciones. **Ya se cumple.**
2. **Aceptación del plan de pruebas** de `FREEBUFF_TEST_GAPS_v219.md` (38 pruebas, 8 bloques).
3. **Respuestas a Q1–Q8** o marca `BLOCKED` en las pruebas afectadas.
4. **Decisión sobre el hash autoritativo** de R5 (A vs B).
5. **Confirmación de que el árbol no se declarará congelado** por esta fase.

Las pruebas deben escribirse antes de cada corrección y **fallar por la razón esperada**. Una prueba que pasa antes de implementar no mide el concepto.

## K. ¿Qué arquitectura conceptual mínima se recomienda?

Quince conceptos, sin código, en `FREEBUFF_ARCHITECTURE_CONCEPTS_v219.md`:

```text
C-01 Reading
C-02 ONE_CANDIDATE / ONE_CONFIRMED
C-03 TWO_CANDIDATE / TWO_CONFIRMED / TWO_IMPOSSIBLE
C-04 THREE_CANDIDATE / THREE_CONFIRMED / THREE_IMPOSSIBLE
C-05 MÓDULO derivado
C-06 A_CANDIDATE / A_GRANDE / A_USED_AS_TREND
C-07 B_CANDIDATE / B_GRANDE
C-08 AUT
C-09 C_CANDIDATE / C_GRANDE / C_USED_AS_TREND
C-10 CUT / reset
C-11 TT_POSSIBLE / TT_CONFIRMED / TT_EXTREME / FT
C-12 GAP_IMPLICIT
C-13 Autoridad única de pregunta
C-14 Genealogía y transformación
C-15 Capas separadas
```

Principio rector:

> **Una lectura, un tick, una pregunta.**

Con una sola autoridad, decisión por tick, `MOVE` fuera de la lectura y el gap como resolución funcional.

## L. ¿Es seguro comenzar la implementación después de responder las dudas?

**No todavía.** Responder Q1–Q8 es necesario, pero no suficiente. Faltan tres condiciones:

1. **Resolver la ambigüedad A/B del motor.** Hoy el paquete entregado contiene `19A847C0…` y la auditoría se hizo contra `9BD1BEDB…`. Implementar sobre uno y entregar el otro repetiría el problema.
2. **Aceptar formalmente el plan de pruebas** y el criterio de "fallar por la razón esperada".
3. **Fijar el alcance de la primera implementación**: solo lectura (funciones y patrones), sin capa operativa, sin variables y sin ejecución de órdenes.

Con esas tres condiciones y Q1–Q8 respondidas, **sí sería seguro** comenzar una rama de prototipo, con estas restricciones:

- no tocar R3;
- no declarar el árbol congelado;
- no modificar goldens ni lecturas;
- no introducir umbrales no escritos;
- no usar el 6,00 como umbral de lectura;
- no conectar la capa operativa.

Sin ellas, la implementación sería una decisión de diseño no autorizada.

## 1. Conclusión en una frase

R5 no falla por siete errores separados: falla porque **decide sobre movimientos ya cerrados en lugar de sobre funciones vivas**, y porque el filtro operativo de 6,00 sustituyó a la ontología del árbol. Todo lo demás —`2/3` ausentes, módulo inflado, gap irresuelto, TT perdido, capas mezcladas— es propagación de esa premisa.

## 2. Entregables

| # | Documento | Ruta |
|---:|---|---|
| 1 | Manifiesto de entradas | `FREEBUFF_INPUTS_MANIFEST_v219.json` |
| 2 | Comparación de variantes R5 | `01_INTEGRITY/R5_VARIANT_COMPARISON.md` |
| 3 | Reproducción CE | `FREEBUFF_CE_REPRODUCTION_v219.md` |
| 4 | Primeras divergencias | `FREEBUFF_FIRST_DIVERGENCES_v219.csv` |
| 5 | Causas raíz conceptuales | `FREEBUFF_CONCEPTUAL_ROOT_CAUSES_v219.md` |
| 6 | Análisis RC-1 | `FREEBUFF_RC1_MOVEMENT_ANALYSIS_v219.md` |
| 7 | Análisis RC-2 | `FREEBUFF_RC2_GAP_ANALYSIS_v219.md` |
| 8 | Arquitectura conceptual | `FREEBUFF_ARCHITECTURE_CONCEPTS_v219.md` |
| 9 | Matriz de reutilización | `FREEBUFF_COMPONENT_REUSE_MATRIX_v219.csv` |
| 10 | Preguntas expertas | `FREEBUFF_EXPERT_QUESTIONS_v219.md` |
| 11 | Huecos de prueba | `FREEBUFF_TEST_GAPS_v219.md` |
| 12 | Resumen de auditoría | `FREEBUFF_AUDIT_SUMMARY_v219.md` (este documento) |
| 13 | Hashes | `SHA256SUMS.txt` |

Evidencia adicional:

- `01_INTEGRITY/R5_variant_unified_diff.txt` (422 líneas).
- `02_TREE_MAPPING/TREE_TO_ENGINE_MAP_v219.csv` (24 reglas).
- `03_CONCEPTUAL_DIAGNOSIS/probe_dual_authority.py` y `.out`.
- `04_CE_REPRODUCTION/run_ce_reproduction.py`, `ce_out/CE_REPRODUCTION_RAW.json`, `ce_out/CE_REPRODUCTION_SUMMARY.json`.
- `08_MANIFEST/EXTERNAL_EVIDENCE_INDEX_v219.csv`.

## 3. Límites de esta auditoría

- No se ha modificado ni ejecutado ninguna corrección.
- No se ha validado el motor contra el feed real; la reproducción es sintética y observacional.
- No se ha auditado R3 en profundidad; solo se ha verificado su hash y su condición de congelado.
- No se han usado los bloques `[D]` de `v005` como expectativa.
- No se ha resuelto ninguna de las ocho preguntas expertas.
- No se ha declarado el árbol congelado ni el motor listo.
- No se ha empaquetado ni sustituido ninguna variante de R5.
