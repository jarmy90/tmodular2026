# AUDITORÍA Y CORRECCIÓN — ITERACIÓN 11

**Baseline auditado:** `TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT`
**Fuente normativa:** `TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md`
**Fecha:** 2026-10-30
**Estado:** árbol NO congelado. Motor oficial NO creado. Sin órdenes reales.

---

## 1. Resumen ejecutivo

Reconstruí el estado desde los archivos, comparé el árbol v2.19 con el intérprete Python y
encontré una **divergencia semántica grave y una ausencia**: (a) el intérprete trataba el gap
como «2 imposible → módulo por descarte → A pendiente», cuando v2.19 exige «A Grande implícita
→ B Grande implícita → A usada como tendencia implícita → nuevo 1 desde la apertura»;
(b) TT no existía. Corregí ambas causas raíz, añadí CUT con su condición cerrada y dejé
bloqueado explícitamente lo que el árbol no cierra (reset tras CUT, reinicio del ciclo,
FT). No toqué el árbol ni ningún motor oficial.

## 2. Inventario de archivos revisados

| Archivo | Finalidad | Autoridad |
|---|---|---|
| `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md` | árbol normativo acumulado | **NORMATIVA PRINCIPAL** |
| `TM_ARBOL_ACTIVO.md` | espejo del árbol | normativa (duplicada) |
| `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_12/13*.md` | versiones históricas | histórica |
| `TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v005.txt` | lecturas humanas | golden humano |
| `TM_REFERENCE_ENGINE/tm_reference_interpreter_v1*.py` | intérpretes v1 → direct_aut | implementación |
| `04_CONCEPT_TESTS/run_*.py` | suites de contrato | pruebas |
| `09_OPEN_RULES/*.md` | reglas abiertas | documentación |
| `TM_CORE_PYTHON_v0752_CANONICAL_R5.py` | motor histórico R5 | histórica (no modificado) |

## 3. Fuente normativa utilizada

Se aplicó el orden de precedencia declarado en §0 del árbol v2.19: corrección expresa más
reciente de Javier > reglas consolidadas (ruido 2 puntos, aclaraciones 2026-10-21) > patch v1.2
> v1.1 > v1.0 > v0.9 > v1 > históricas. Los anexos («FUENTE INTEGRA») se tratan como material
de origen, no como norma vigente cuando contradicen un patch posterior.

## 4. Estado inicial encontrado

- núcleo 1/2/3/módulos: implementado y probado (19/19).
- A/retorno/B candidata: implementado con política **provisional**.
- B Grande, AUT por B, nuevo 1 por B: implementado y probado.
- AUT directo por A: implementado, con precondición `A_CONFIRMED`.
- C Grande y C usada como tendencia: implementado.
- **Gap: implementado con semántica equivocada.**
- **TT: inexistente.**
- **CUT: inexistente.**
- **FT: inexistente.**
- Árbol no congelado; motor oficial no creado.

## 5. Posibles pérdidas de contexto por el cambio de cuenta

Comprobación de continuidad: el baseline en disco (`direct_aut`), sus 9 módulos de prueba y los
anclas 16:15–16:18 y L2 16:19–16:22 reproducen exactamente los valores esperados
(módulo 28,5 · A 9,1 · AUT 16:18:34.926 · L2 1=7,5 · 2=12,3 · 3=29830,3 · módulo 19,7).
**No se detectó pérdida de contexto.** La única «pérdida» fue documental: `OPEN_RULES` seguía
describiendo el salto de 4 puntos como política vigente y el AUT directo como no implementado.

## 6. Cambios incorrectos detectados

### 6.1 Gap leído como módulo por descarte (CRÍTICO)

- Norma v2.19 §0.0.-3: el gap se resuelve como A/B Grande/A usada como tendencia **implícitas** y
  **nuevo 1 desde la apertura**; prohibido medirlo como una única A desde el extremo previo.
- Código anterior: `NON_FLAT_OPEN_OBSERVED → TWO_IMPOSSIBLE_NO_FLAT → MODULE_BY_DISCARD → A pendiente`.
- Efecto: tras cualquier gap la lectura nacía como A sobre un módulo inventado y **nunca** producía
  el nuevo 1 que la norma exige desde la apertura.
- Causa raíz: traducción del árbol a Python desactualizada (regla v2.3 aplicada sin el patch v2.19).
- Corrección: rama nueva `GAP_IMPLICIT_SEQUENCE` + `GAP_IMPLICIT_NEW_ONE`; origen = apertura,
  `structural_time = knowledge_time = primer tick negociado`, sin precios internos ni ticks simulados.

### 6.2 TT ausente (CRÍTICO por omisión)

No existía ningún estado TT, pese a que v2.6/v2.7 fijan objetivo y árbitro. Implementado.

### 6.3 CUT ausente

Existía sólo como mención. v2.13 §6 y el cuerpo v2.19 fijan la condición cerrada
(«C Grande supera el final real de A Grande»). Implementada la confirmación; reset bloqueado.

### 6.4 Contaminación de estado en AUT directo

`_on_new_one_tick` escribía `b_status = "AUT"` también en la vía directa por A, donde B no existe.
Corregido: sólo escribe si `aut_status == AUT_CONFIRMED`.

### 6.5 Metadatos obsoletos

`OPEN_RULES_B_GRANDE_AUT_V1.md` seguía declarando la política de 4 puntos como vigente y el AUT
directo como bloqueado; `run_full_feed.py` listaba TT como no implementado. Ambos actualizados.

## 7. Errores conceptuales encontrados

Ninguno en el árbol. El árbol es coherente: C no depende del 100 % de A, el 127 % + 0,25 es
inclusivo, AUT exige superación estricta, y la base del módulo es la referencia de C-tendencia y
de AUT directo. Los errores fueron **de traducción**, no de teoría.

## 8. Errores en el árbol

No se modificó el árbol. Se detectaron dos **tensiones documentales** (no contradicciones activas):

1. Anexo 6 §13.11 dice «si C supera la base [del módulo], activa CUT, nuevo 1 y reset», mientras
   v2.17 (posterior, `CONFIRMADO_JAVIER`) dice que superar la base del módulo produce
   **C usada como tendencia**. Por precedencia se aplica v2.17; CUT queda ligado al final real de
   A. Registrado como `Q-CUT`.
2. v2.7 D ordena que, tras TT fallido, el recorrido anterior sea «módulo por descarte» y el retorno
   «A Grande nueva», pero no fija cómo se reabre el ciclo. Registrado como `Q-CYCLE-1`.

## 9. Errores en Python

Los del punto 6 (gap, TT, CUT, contaminación B/AUT directo, metadatos). Todos corregidos en el
baseline; ninguno se resolvió con parches específicos de un ejemplo.

## 10. Causas raíz

- Traducción del árbol congelada en una versión anterior (v2.3) sin re-aplicar v2.19.
- Crecimiento por iteraciones: cada patch añadió pruebas para lo nuevo sin volver a recorrer las
  ramas ya implementadas (gap, apertura).
- Documentación de reglas abiertas sin sincronizar con el código.

## 11. Correcciones realizadas

1. Rama de gap v2.19 con funciones implícitas y nuevo 1 desde la apertura.
2. TT completo: `TT_PENDING → TT_CONFIRMED → TT_EXTENDED`, `TT_FAILED`, árbitro cronológico y
   objetivo `final_A ± tamaño_módulo`.
3. CUT como condición cerrada, sin inventar el reset.
4. Limpieza de la contaminación B en AUT directo.
5. Tests: T-015 reescrito, GAP-03/03b/05 reescritos y GAP-06..09 añadidos, TT-01..12 y CUT-01..04.

## 12. Archivos modificados

- `05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py`
- `04_CONCEPT_TESTS/run_core_tests.py`
- `04_CONCEPT_TESTS/run_iteration_09_tests.py`
- `04_CONCEPT_TESTS/run_iteration_10_tests.py`
- `04_CONCEPT_TESTS/run_iteration_11_tests.py` (nuevo)
- `04_CONCEPT_TESTS/run_full_feed.py`
- `09_OPEN_RULES/OPEN_RULES_ITERACION_11.md` (nuevo)

Ningún motor oficial, ningún golden humano, ningún árbol normativo.

## 13. Tabla de equivalencia árbol–Python

| Nodo del árbol | Condición | Implementación | Resultado |
|---|---|---|---|
| §0.0.0 A (2 candidata) | apertura plana + dirección | `_eval_opening` | OK |
| §0.0.0 C (tras 3) | 3 confirmado | `_on_three_live_tick` | OK |
| §0.0.-2 A→B→BG→AUT | B > 127 %+0,25 | `_confirm_aut` | OK |
| §0.0.-1 C Grande | giro contrario a B | `_open_c` | OK |
| §0.0.-1 C tendencia | C > base módulo | `_confirm_c_as_trend` | OK |
| v2.13 §6 CUT | C > final real de A | bloque CUT en `_on_c_tick` | OK (reset abierto) |
| §0.0.-3 gap | apertura no plana | rama gap de `_eval_opening` | OK (corregido) |
| §0.6 TT 100 % | precio alcanza final_A ± módulo | `_arm_tt` / `_on_tt_tick` | OK |
| §0.7 árbitro | primera frontera tick a tick | `_on_tt_tick` | OK |
| §0.7 D TT fallido | final_A antes del objetivo | `_on_tt_tick` | OK (reapertura abierta) |
| FT | patrón con variables | — | NOT_IMPLEMENTED |
| reinicio del ciclo | — | — | OPEN_RULE |

## 14. Pruebas añadidas o modificadas

- T-015: ahora verifica la secuencia de gap v2.19 además de la prohibición de 2.
- GAP-03/03b/05: reescritas a v2.19. GAP-06/07/08/09: ancla 16:24–16:25, no medición desde el
  cierre previo, ausencia de precios inventados, archivo de autoridades previas.
- TT-01..TT-12 (nuevo): armado en AUT, inexistencia antes de AUT, ancla 29829,1, confirmación en
  el tick, frontera 0,10 antes, extensión, fallo, salto único, independencia de B, autoridad del
  nuevo 1, determinismo, prefijo.
- CUT-01..CUT-04 (nuevo): toque exacto, superación estricta, no invención de reset, inexistencia
  antes de B Grande.

## 15. Resultado completo de las pruebas

| Bloque | Total | PASS | FAIL |
|---|---|---|---|
| Núcleo 1/2/3/módulos | 19 | 19 | 0 |
| A/retorno/B candidata (A-*) | 32 | 32 | 0 |
| AUT directo por A (AD-*) | 17 | 17 | 0 |
| C / CUT (C-*, CUT-*) | 18 | 18 | 0 |
| Gap y concurrencia (GAP-*, CONC-*) | 16 | 16 | 0 |
| TT (TT-*) | 12 | 12 | 0 |
| **Total** | **114** | **114** | **0** |

Feed completo 16:15–17:29: 20.335 ticks, determinista, prefijo consistente, 551 eventos,
`TT_EXTENDED` 214, cero fugas entre lecturas.

## 16. Casos que todavía fallan

Ninguno de las pruebas definidas. Limitaciones reales:

- El feed real **no contiene ningún gap ≥ 0,25**, así que la rama de gap sólo se ejercita con
  fixtures y con el ancla canónica 16:24–16:25; no hay evidencia empírica del feed sobre ella.
- Tras TT confirmado la lectura no vuelve a abrir 2/3/A: depende de `Q-CYCLE-1`.
- 58 pruebas de A/B/C dependen de la política **provisional** de autonomía del retorno; no son canon.

## 17. Dudas conceptuales pendientes

1. **Q-CYCLE-1.** Después de un nuevo 1 (por AUT o por TT), ¿qué tick reabre la pregunta por 2?
   Ejemplo: nuevo 1 bajista desde 29857,6 que sigue hasta 29843,0; ¿la vela siguiente abre ya 2
   candidata, o primero debe aparecer un retroceso contrario con autonomía?
2. **Q-CUT.** Cuando C Grande supera el final real de A (CUT confirmado), ¿el reset es inmediato en
   ese tick —como en TT— o se espera a que C supere también la base del módulo?
3. **Q-FT.** ¿De qué función confirmada se deriva el punto decisivo FT y con qué condición
   estructural se declara «guardable», sin usar variables operativas?

## 18. Riesgos existentes

- Interpretar la autonomía del retorno con una heurística provisional puede crear A/B donde la
  teoría no las reconocería.
- La rama de gap no está validada contra datos reales del feed.
- Sin reinicio de ciclo, el lector se queda en un único ciclo en series largas.

## 19. Valoración honesta

El núcleo y las transiciones cerradas (1, 2, 3, módulo, A, B, B Grande, AUT por B, AUT directo por
A, C, C tendencia, CUT, gap, TT) están implementadas y verificadas: **114/114**. Eso **no** es un
lector completo: faltan FT, el reinicio del ciclo y la validación de la rama de gap con datos
reales. Fidelidad estimada: alta en las ramas cerradas, **no demostrada** en las abiertas.

## 20. Próximos pasos recomendados

1. Responder Q-CYCLE-1 (desbloquea TT fallido, reinicio y buena parte del feed).
2. Responder Q-CUT y Q-FT.
3. Validar el gap con una fuente que sí contenga gaps (M1 con aperturas discontinuas).
4. Sólo después, recorrer el feed completo por bloques y comparar con las lecturas humanas.
