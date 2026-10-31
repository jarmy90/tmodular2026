# FREEBUFF_EXPERT_QUESTIONS_v219

**Preguntas expertas que siguen abiertas después de recorrer árbol, parches, lecturas, ticks, tests y código**
**Fecha:** 2026-10-30
**Árbol:** `94A1408A…` (WORKING_CANON_NOT_FROZEN) · **Motor:** R5 `9BD1BEDB…` (`0.7.5.2-R5`)
**Versión documental:** 1.0
**tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

---

## 0. Lo que **no** se pregunta porque el árbol ya lo cierra

| Concepto | Fuente que lo cierra |
|---|---|
| `2` exige plano, sin gap, cola ≤ 0,25, misma dirección y 100 % de `1` | N-006, N-007, v2.13 |
| Con gap no hay `2` | N-002, v2.19 §E |
| `B Grande` al 100 % de `A`; `AUT` solo al superar estrictamente 127 % + 0,25 | N-016, H9, v2.2 §E |
| `TT` se confirma al alcanzar el 100 % del objetivo | N-019, N-039 |
| `C Grande` solo después de `B Grande` | N-022 |
| Después de `3` viene `A Grande` desde el extremo real de `3` | v2.15 |
| Un `2` confirmado no se borra | N-036 |
| `A`, `B`, `C` no exigen 6,00; el filtro de 6,00 es operativo | v2.5 §D y §H |
| El filtro de ruido es 2,00; por debajo no hay función | §2 del árbol |
| El gap se resuelve como A/B/A-tendencia implícitas y nuevo `1` en la apertura | v2.19 §A-C |
| `A` y `C` usadas como tendencia son transformaciones, no lecturas nuevas | v2.16, v2.17, v2.19 |

Solo quedan las ocho ambigüedades siguientes. Todas afectan a la implementación; ninguna se resuelve por preferencia del programador.

---

## Q1 — Nacimiento y congelación de `1`

**MOVIMIENTO**

Estábamos sin lectura. El precio avanzó 4,00 puntos en una dirección, retrocedió 1,00 y volvió a avanzar hasta 8,00. Después giró 3,00 en contra.

**DUDA**

¿En qué momento exacto queda `1` confirmada y congelada su medida?

**CONSECUENCIA A**

Si se confirma **al cierre de la vela** en la que nace, la medida es el extremo de esa vela y el módulo/TT se proyectan desde ahí. Un giro dentro de la misma vela queda absorbido.

**CONSECUENCIA B**

Si se confirma con el **primer movimiento contrario estructural** (2,00), la medida es el extremo anterior al contrario y `1` puede atravesar varias velas. Cambia el módulo, la puerta de `2` y todos los objetivos TT.

**NODOS DESBLOQUEADOS**

N-001, N-006, N-007, N-012, N-013, N-018, N-019, N-040.
Pruebas: T-01..T-05, T-06, T-13.

---

## Q2 — 0,25 exactos: plano o gap

**MOVIMIENTO**

Una vela cierra en 100,00. La siguiente abre en 100,25 y empieza a bajar.

**DUDA**

¿Esa apertura es plano —y por tanto `2` es evaluable— o es gap —y por tanto `2` es imposible y se activa la resolución implícita—?

**CONSECUENCIA A**

Si 0,25 es **plano**: hay `2` posible; la lectura sigue la rama regular.

**CONSECUENCIA B**

Si 0,25 es **gap**: no hay `2`; se registran A/B/A-tendencia implícitas y nace un nuevo `1` en 100,25.

**NODOS DESBLOQUEADOS**

N-002, N-005, H14, v2.13, v2.19 §E.
Pruebas: T-24, T-25, CE3-NEG, CE6-FRON.

> El árbol contiene las dos formulaciones: H14 dice `≤ 0,25`; v2.13 y CE-6 usan `< 0,25`. R5 aplica `< 0,25`. No se corrige sin esta respuesta.

---

## Q3 — Referencia del CUT

**MOVIMIENTO**

Estábamos en `C Grande`, después de `B Grande`. C avanzó y alcanzó el final de A, pero todavía no la base del módulo. Después siguió o giró.

**DUDA**

¿El CUT se mide contra el **final de A** o contra la **base del módulo**?

**CONSECUENCIA A**

Si el CUT es contra el **final de A** (N-024), el ciclo se cierra al cruzar ese nivel y C se reclasifica como nuevo `1`. La base del módulo solo se usa para la transformación en tendencia.

**CONSECUENCIA B**

Si el CUT es contra la **base del módulo** (v1.2/v2.17), C puede seguir siendo C después de superar el final de A y el cierre llega más tarde. Cambia el tick de CUT y la genealogía.

**NODOS DESBLOQUEADOS**

N-024, N-025, N-034, v1.2 §13, v2.17.
Pruebas: T-21, T-28..T-30, CE-2, CE-7.

---

## Q4 — Nuevo `1`: en AUT o en TT

**MOVIMIENTO**

Estábamos en `B Grande`. El precio superó el 127 % + 0,25 (**AUT**) sin cruzar la base del módulo. Después continuó hasta el 100 % del objetivo TT.

**DUDA**

¿El nuevo `1` nace en el tick del AUT o en el tick del TT?

**CONSECUENCIA A**

Si nace en el **AUT**, el nuevo `1` empieza en el extremo de B y el TT se mide como desarrollo de ese `1`. La lectura anterior conserva el módulo como referencia del TT.

**CONSECUENCIA B**

Si nace en el **TT**, el módulo anterior sigue siendo la referencia hasta el 100 % y el nuevo `1` empieza después. Cambia qué función mide el TT y qué lectura posee el módulo.

**NODOS DESBLOQUEADOS**

N-017, N-018, N-021, N-031, N-033, v2.3 §F, v1.2 §13.7.9.
Pruebas: T-20, T-22, T-31, T-32.

> El árbol ya distingue el caso en que el AUT cruza la base del módulo (nuevo `1` en ese movimiento, v2.3 §F). La duda es el AUT que **no** cruza la base.

---

## Q5 — Medida del módulo `1-2-3`

**MOVIMIENTO**

El `1` recorrió 0,00 → 10,00. La vela de ese recorrido tuvo un mínimo de −2,00 por una mecha inicial. Después vinieron `2` y `3` y el conjunto se expandió hasta 18,00.

**DUDA**

¿El módulo se mide por el **desplazamiento direccional** (0→18 = 18,00) o por la **expansión máxima del conjunto** (mínimo −2,00 a máximo 18,00 = 20,00)?

**CONSECUENCIA A**

Si es **desplazamiento direccional**, el módulo es 18,00 y el TT se proyecta 18,00 desde el final de A. Las mechas no cuentan.

**CONSECUENCIA B**

Si es **expansión del conjunto**, el módulo es 20,00 y el TT se proyecta 20,00. Las mechas y los solapes sí cuentan.

**NODOS DESBLOQUEADOS**

N-012, N-040, A2, N-018.
Pruebas: T-13..T-17.

> N-012 habla de `max(high) − min(low)` del conjunto; N-040 habla de desplazamiento direccional. Para una pata monótona coinciden; con mechas o solapes no.

---

## Q6 — Tick y condición del FT

**MOVIMIENTO**

El TT se confirmó al 100 %, se extendió hasta el 130 % y después retrocedió 6,00 puntos y siguió bajando.

**DUDA**

¿El FT se declara en el **primer tick contrario**, cuando se **pierde el origen estructural del TT**, o solo cuando las **variables** lo confirman?

**CONSECUENCIA A**

Si es en el **primer tick contrario**, el FT se registra muy pronto y puede ser ruido; el patrón queda cerrado antes de saber si el TT se reanuda.

**CONSECUENCIA B**

Si exige **pérdida de estructura** (o variables), el FT llega más tarde pero es significativo. Cambia el tick de FT, la gestión y la relación con la lectura siguiente.

**NODOS DESBLOQUEADOS**

N-026, N-035, N-039, R-02.
Pruebas: T-30, CE-5.

> El árbol deja el tick y las variables del FT como `PENDIENTE_JAVIER`; no se inventa un umbral.

---

## Q7 — Apertura y prioridad de lecturas concurrentes

**MOVIMIENTO**

Existe una lectura principal con módulo 20,00 y una lectura local con módulo 5,00. El precio alcanza el objetivo TT de la local y, más tarde, el de la principal. Ambos objetivos son válidos.

**DUDA**

¿Qué lectura posee el tick cuando ambas lo reclaman, y pueden confirmarse los dos TT?

**CONSECUENCIA A**

Si la **principal conserva la propiedad** y la local solo se registra, el TT local se confirma pero no altera la lectura principal; el tick pertenece a la principal.

**CONSECUENCIA B**

Si la **estructura decide la propiedad** (por referencia rota, no por tamaño), el tick puede pertenecer a la local y la principal seguir pendiente. Cambia la dominancia y la genealogía.

**NODOS DESBLOQUEADOS**

N-028, N-029, N-030, R-04.
Pruebas: T-33, CE-4.

---

## Q8 — Frontera exacta del retroceso de `3`

**MOVIMIENTO**

`2` confirmada. El precio retrocedió exactamente el 50 % del rango de `2` y después superó el extremo de `2`.

**DUDA**

¿El 50 % exacto confirma `3` o degrada la secuencia a módulo `1+2`?

**CONSECUENCIA A**

Si el 50 % es **inclusivo**, hay `3` y módulo regular `1-2-3`.

**CONSECUENCIA B**

Si el 50 % es **exclusivo**, no hay `3`; `1+2` forman módulo y el contrario es `A Grande`.

**NODOS DESBLOQUEADOS**

N-009, N-010, N-011.
Pruebas: T-10, T-11, T-12.

---

## 1. Impacto conjunto

| Pregunta | Sin respuesta, queda bloqueado |
|---|---|
| Q1 | todo el ciclo: `1`, módulo, `2`, TT |
| Q2 | `2` y la rama de gap |
| Q3 | `C`, `CUT`, reset y genealogía |
| Q4 | `AUT`, `TT`, nuevo `1` |
| Q5 | objetivo TT y base de CUT |
| Q6 | `FT` completo |
| Q7 | concurrencia y dominancia |
| Q8 | `3` y módulo regular |

## 2. Forma de responder

No hace falta código ni nombres internos. Basta indicar, para cada pregunta, **A**, **B** o una tercera opción descrita en términos de movimiento. Las respuestas se incorporarán al árbol como parche con fecha y autoridad, y solo entonces se reflejarán en pruebas y motor.

## 3. Lo que **no** se pregunta

- No se pregunta por umbrales de velocidad, solapamiento, tiempo M1/M3 o estructura: pertenecen a la capa 2 y no modifican la lectura.
- No se pregunta por el tamaño mínimo de `1`, `A`, `B` o `C`: el árbol ya lo cierra en 2,00 de ruido y prohíbe el 6,00 estructural.
- No se pregunta por la existencia de `2` con gap: ya está prohibida.
- No se pregunta por `B Grande` al 100 % ni por `AUT` estricto: ya están cerrados.
