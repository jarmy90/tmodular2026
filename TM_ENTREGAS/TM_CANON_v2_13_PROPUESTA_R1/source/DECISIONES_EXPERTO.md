# DECISIONES DEL EXPERTO (Javier) — Memoria normativa TM

Este archivo es la memoria normativa del aprendizaje. No depende del chat.
Cada respuesta del experto se registra aquí (literal), se transforma en regla
general y genera primero un test rojo. El orquestador lo siembra; SCENE_QUESTIONER
lo mantiene actualizado.

---

## DEC-001

- **ID:** DEC-001
- **Fecha y hora:** 2026-10-18 (sesión ECC/OpenCode)
- **Agente que la origina:** ORQUESTADOR / SCENE_QUESTIONER (derivada de la duda «tolerancia exacta de salida en plano», §11 del prompt v2)
- **Estado:** cerrada (provisional hasta formalizar test rojo)
- **Regla TM afectada:** A1 / detección de «salida en plano» al abrir nueva vela

### Pregunta
¿Cuál es la tolerancia exacta, en ticks, para considerar que hay «salida en plano»
al abrir una nueva vela (sin gap), de modo que se pueda abrir «posible 2»?

### Contexto objetivo
- Al abrir nueva vela el núcleo comprueba primero gap y, si no hay gap, «salida en plano» (§10.2 del prompt v2).
- Sin este umbral, no es implementable el Bloque 1 (1 → salida en plano/gap → posible 2 → 2 → posible 3 → 3 fallido → módulo → A Grande).

### Respuesta literal del experto
> "en cuanto a salir en plano podemos darle un margen de 1 tick"

### Regla general extraída
- **Salida en plano** = la apertura de la nueva vela permanece dentro de **±1 tick**
  respecto del cierre de la vela anterior (y no existe gap). Es decir, tolerancia
  de **1 tick** de desviación.
- Si la desviación supera 1 tick, no se considera salida en plano (se evalúa gap u otro caso).

### Ejemplo
- Cierre vela N = 29811,60; apertura vela N+1 dentro de [29811,60 − 1 tick, 29811,60 + 1 tick] → salida en plano.

### Contraejemplo
- Apertura de vela N+1 con salto de precio superior a 1 tick → no es salida en plano.

### Vocabulario aprobado
`salida en plano`, `gap`, `posible 2`.

### Tests creados
- PENDIENTE: test rojo en Bloque 1 (aún no implementable hasta cerrar el resto del bloque).

### Archivos modificados
- `DECISIONES_EXPERTO.md` (este registro).

### Versión de implementación
- Núcleo: `0.0.1-scaffold` (sin cambios de lógica).

### Regresiones detectadas
- Ninguna (aún no hay implementación del Bloque 1).

### Estado de la regla
- **cerrada** en cuanto a tolerancia (1 tick). Queda pendiente su test rojo.

---

## Pendiente de registro (dudas abiertas que deben resolverse por escenas)
- Serie de precio exacta para el replay (Bid/Ask/Last/mid) — ver `AUDITORIA_DATOS.md`.
- Momento exacto en que un movimiento contrario deja de ser candidato y queda como A Grande / B Grande / C Grande.
- Criterios de reclasificación de varias velas como módulo o 1 conjunto.
- Permanencia de una lectura a través de nuevos movimientos.
- Reglas completas de FT.
- Contradicción objetiva vela 8 (CUT) — ver `CONTRADICCIONES.md` (agente RULES_ANALYST).

---

## Pendientes de pregunta (SCENE_QUESTIONER)

Dudas convertidas a **escena** (formato §7 del prompt v2) y enviadas a Javier. El detalle completo
—hechos objetivos, escenas A/B/C, pregunta concreta y efecto— vive en `PREGUNTAS_PENDIENTES.md`.
**No se borra DEC-001.** Cada respuesta se registrará aquí como `DEC-002`, `DEC-003`… (literal +
regla general + test rojo) y la duda pasará a *cerrada*.

| ID de duda | Contradicción | Regla afectada | Estado |
|---|---|---|---|
| **DUDA-001** | C1 — C Grande/CUT y final de A Grande (vela 8) | §10.7 / §10.4 | **BLOQUEANTE** |
| **DUDA-002** | C2 — unidad del nivel AUT (`0,25 puntos` vs `0,25 tick`) | §10.5 / B1 | **BLOQUEANTE** |
| **DUDA-003** | C3 — «tocar 127 % y volver» → AUT o C → CUT | §10.5 vs §20.16 | **BLOQUEANTE** |
| **DUDA-004** | C4 — vocabulario TM en concurrencia/reclasificación | §10.8 / D | **BLOQUEANTE** |
| **DUDA-005** | C6 — prioridad gap ↔ regla de 2 | §9.3 / §4.2 | **BLOQUEANTE** |

**Estado:** las 5 dudas están **pendientes de respuesta** (ninguna contestada todavía). Todas son
**BLOQUEANTES**. No bloquean el cierre del Bloque 1–2 salvo lo indicado en `CONTRADICCIONES.md`
(C1 bloquea el cierre de C Grande/CUT).

**Pendientes §11 aún NO convertidos a escena (NO BLOQUEANTES para los bloques 1–3):** serie de
precio del replay (`P2`, Bid ya fijado por `AUDITORIA_DATOS.md`), momento de confirmación
A/B/C Grande (`P3`), reclasificación de velas (`P4`), permanencia de una lectura (`P5`), reglas de
FT (`P6`).

---

## Decisiones registradas (segunda oleada) — DUDA-002 … DUDA-005

> Registro añadido por SCENE_QUESTIONER. **No modifica DEC-001 ni la sección anterior de
> «Pendientes».** Las dudas `DUDA-002` … `DUDA-005` quedan **CERRADAS** con estas decisiones y
> **sustituyen** el estado «pendiente» de la tabla anterior de «Pendientes de pregunta».
> `DUDA-001` permanece **BLOQUEANTE** (reformulada de forma más simple, ver `PREGUNTAS_PENDIENTES.md`).

---

## DEC-002

- **ID:** DEC-002
- **Fecha y hora:** 2026-10-18 12:10 (sesión ECC/OpenCode)
- **Agente que la origina:** SCENE_QUESTIONER (duda DUDA-002, contradicción C2)
- **Estado:** CERRADA
- **Regla TM afectada:** §10.5 / B1 — nivel de AUT (unidad del extra)

### Pregunta
¿El extra del nivel de AUT es **+0,25 puntos** del instrumento (equivalente a 1 tick en esta
muestra) o **+0,25 tick** del instrumento (0,0625 puntos en esta muestra)? ¿Cómo se expresa la
regla general en unidades del instrumento, sin depender del símbolo?
(Pregunta completa de origen: `PREGUNTAS_PENDIENTES.md` DUDA-002.)

### Contexto objetivo
- Contradicción C2: con 1 tick = 0,25 puntos, «0,25 puntos» y «0,25 tick» no coinciden.
- Hechos de tick de la muestra: R-A alcanza su nivel de AUT en 29743,715; R-D en 29703,51.
- Sin fijar la unidad, el nivel de AUT no es implementable en unidades del instrumento.

### Respuesta literal de Javier
> "un rik que es 0,25" (interpretado: «un tick que es 0,25»)

### Regla general extraída
- El extra de AUT es **1 tick**, que en el instrumento de la muestra vale **0,25 puntos**.
- **Nivel de AUT = 127 % del retroceso de A Grande + 1 tick**.
- Expresado sin depender del símbolo: el extra se mide en **1 tick** del instrumento, no en un
  número fijo de puntos.
- Con 1 tick = 0,25 puntos, «+0,25 puntos» y «+1 tick» **coinciden** en esta muestra; la regla
  general queda en **ticks**.

### Ejemplo
- R-A: A Grande = 60,50 pts. Nivel de AUT = 29820,80 − 1,27·60,50 − 0,25 = **29743,715** (1 tick).
- R-D: A Grande = 32,00 pts. Nivel de AUT = 29744,40 − 1,27·32,00 − 0,25 = **29703,51** (1 tick).

### Contraejemplo
- Leer el extra como **0,25 tick** (0,0625 puntos en esta muestra) desplaza el nivel y cambia el
  tick del AUT ⇒ **incorrecto**.

### Vocabulario aprobado
`AUT`, `127 %`, `tick`, `puntos`, `B Grande`, `A Grande`, `retroceso`.

### Tests creados
- Test rojo del nivel de AUT (extra = 1 tick = 0,25 puntos): `tests/rules.closed.red.test.js`
  (lo creará TDD_GUIDE).

### Archivos modificados
- `DECISIONES_EXPERTO.md` (este registro), `PREGUNTAS_PENDIENTES.md` (DUDA-002 → CERRADA).

### Versión de implementación
- Núcleo: `0.0.1-scaffold` (sin cambios de lógica).

### Regresiones detectadas
- Ninguna (aún no hay implementación del bloque de AUT).

### REDACCION NORMALIZADA (exacta) — SCENE_QUESTIONER, NO reabre el estado

- **margen de AUT = `aut_extra_points = 0.25`** (fijo, **no derivado del CSV**).
- **AUT se confirma solo al SUPERAR 127 % + 0,25.**
- Si alcanza la zona y se da la vuelta sin superarla: **B Grande continúa siendo B Grande** y
  el movimiento contrario comienza como **C Grande candidata**; **no existe AUT**.

### Estado de la regla
- **CERRADA** (unidad del extra de AUT = 1 tick = 0,25 puntos; y `aut_extra_points = 0.25` fijo,
  no derivado de la serie). Cierra C2.

---

## DEC-003

- **ID:** DEC-003
- **Fecha y hora:** 2026-10-18 12:10 (sesión ECC/OpenCode)
- **Agente que la origina:** SCENE_QUESTIONER (duda DUDA-003, contradicción C3)
- **Estado:** CERRADA
- **Regla TM afectada:** §10.5 frente a la hipótesis §20.16 — AUT ante «tocar 127 % + 0,25 y volver»

### Pregunta
¿«Tocar el 127 % + 0,25 **y volver**» activa **AUT de forma inmediata** (regla §10.5), o permite
que el recorrido continúe como **C Grande → CUT sin AUT** (hipótesis §20.16)?
(Pregunta completa de origen: `PREGUNTAS_PENDIENTES.md` DUDA-003.)

### Contexto objetivo
- Contradicción C3: dos comportamientos de AUT ante «tocar 127 % y volver».
- §20.16 estaba declarada no-regla; la fuente §10.5 tenía prioridad.
- Hechos: en la vela 6 B Grande supera el 100 %, alcanza 127 % + 0,25 y continúa; en la vela 8 la
  B Grande candidata toca el nivel de AUT y continúa hasta nuevo mínimo.

### Respuesta literal de Javier
> "no aut es su puera 127 +0,25 no se dio y dio la vuelta por tanto si llego hasta 127 +025 fue b grande y lo que sube es c grande no aut"

### Regla general extraída
- **AUT solo se confirma cuando B Grande SUPERA 127 % + 0,25.**
- Si B Grande **solo toca** 127 % + 0,25 **y vuelve** (no lo supera), **NO hay AUT**.
- En ese caso, el movimiento que tocó y volvió es **B Grande** y el movimiento alcista posterior
  es **C Grande** (no AUT).
- Confirma la hipótesis §20.16 y **precisa** §10.5: el disparador del AUT es la **superación**
  del nivel, no su mero contacto.

### Ejemplo
- B Grande **supera** 127 % + 0,25 y continúa ⇒ **AUT** inmediato en ese tick.

### Contraejemplo
- B Grande **toca** 127 % + 0,25 **y vuelve** ⇒ no hay AUT; ese movimiento es **B Grande** y el
  alcista posterior es **C Grande**.
- Activar AUT por el mero contacto del nivel (sin superarlo) ⇒ **incorrecto**.

### Vocabulario aprobado
`AUT`, `B Grande`, `C Grande`, `CUT`, `127 %`, `supera`, `toca`, `volver`, `movimiento contrario`.

### Tests creados
- Test rojo «tocar 127 % + 0,25 y volver ⇒ sin AUT; el alcista posterior = C Grande»:
  `tests/rules.closed.red.test.js` (lo creará TDD_GUIDE).

### Archivos modificados
- `DECISIONES_EXPERTO.md` (este registro), `PREGUNTAS_PENDIENTES.md` (DUDA-003 → CERRADA).

### Versión de implementación
- Núcleo: `0.0.1-scaffold` (sin cambios de lógica).

### Regresiones detectadas
- Ninguna (aún no hay implementación de AUT / C Grande / CUT).

### REDACCION NORMALIZADA (exacta) — SCENE_QUESTIONER, NO reabre el estado

- **margen de AUT = `aut_extra_points = 0.25`** (fijo, **no derivado del CSV**).
- **AUT se confirma solo al SUPERAR 127 % + 0,25.**
- Si alcanza la zona y se da la vuelta sin superarla: **B Grande continúa siendo B Grande** y
  el movimiento contrario comienza como **C Grande candidata**; **no existe AUT**.

> **NOTA PARA RULES_ANALYST (instrucción pendiente, NO ejecutada por SCENE_QUESTIONER):**
> **H8** y **H9** de `REGLAS_CERRADAS.md` deberán reescribirse con **esta misma redacción**
> (`aut_extra_points = 0.25` fijo, no derivado del CSV; AUT solo al SUPERAR 127 % + 0,25; si
> alcanza la zona y se da la vuelta sin superarla → B Grande continúa B Grande y el movimiento
> contrario comienza como C Grande candidata; no existe AUT). Mantener su estado **CERRADA**.

### Estado de la regla
- **CERRADA**. Cierra C3; precisa §10.5 / B1.

---

## DEC-004

- **ID:** DEC-004
- **Fecha y hora:** 2026-10-18 12:10 (sesión ECC/OpenCode)
- **Agente que la origina:** SCENE_QUESTIONER (duda DUDA-004, contradicción C4)
- **Estado:** CERRADA
- **Regla TM afectada:** §10.8 (concurrencia y reclasificación) y D (vocabulario obligatorio)

### Pregunta
¿Cuál es la redacción TM autorizada para nombrar la **segunda/tercera lectura** (alternativa a la
etiqueta prohibida «local») y para la **referencia de módulo de mayor alcance** (alternativa a la
etiqueta prohibida «superior»)?
(Pregunta completa de origen: `PREGUNTAS_PENDIENTES.md` DUDA-004.)

### Contexto objetivo
- Contradicción C4: los dossiers secundarios usan etiquetas que su propia capa funcional prohíbe.
- Sin vocabulario autorizado no puede escribirse la concurrencia/reclasificación en estados,
  eventos, golden ni documentación funcional.

### Respuesta literal de Javier
> "puedes poner lectura 1 ,2 y 3 eso esta fuera de la terminioloia estamos valorando lecturas no esta implicito en la lectura"

### Regla general extraída
- Las lecturas concurrentes se nombran **lectura 1 / lectura 2 / lectura 3**.
- Esa numeración está **fuera de la terminología TM**: es solo un **identificador**, no una
  función ni una clasificación implícita en la lectura.
- **Prohibido** como clasificación en la capa funcional: `local`, `superior`, `estructura`,
  `giro`, `B excesiva`, `observador`.

### Ejemplo
- Dos lecturas simultáneas ⇒ `lectura 1`, `lectura 2`.
- Tres lecturas válidas ⇒ `lectura 1`, `lectura 2`, `lectura 3`.

### Contraejemplo
- Nombrar la segunda lectura como «lectura local» ⇒ **incorrecto**.
- Nombrar la referencia de módulo mayor como «módulo superior» ⇒ **incorrecto**.

### Vocabulario aprobado
`lectura 1`, `lectura 2`, `lectura 3`, `lectura`, `lectura candidata`, `lectura confirmada`,
`lectura reclasificada`, `lectura integrada`, `lectura invalidada`, `lectura finalizada`.

### Tests creados
- Test rojo de vocabulario (aceptar `lectura 1/2/3`; rechazar `local`, `superior`, `estructura`,
  `giro`, `B excesiva`, `observador`): `tests/rules.closed.red.test.js` (lo creará TDD_GUIDE).

### Archivos modificados
- `DECISIONES_EXPERTO.md` (este registro), `PREGUNTAS_PENDIENTES.md` (DUDA-004 → CERRADA).
- Pendiente de aplicar: ampliar el vocabulario autorizado en `DICCIONARIO_TM.md`.

### Versión de implementación
- Núcleo: `0.0.1-scaffold` (sin cambios de lógica).

### Regresiones detectadas
- Ninguna (aún no hay implementación de concurrencia/reclasificación).

### Estado de la regla
- **CERRADA**. Cierra C4.

---

## DEC-005

- **ID:** DEC-005
- **Fecha y hora:** 2026-10-18 12:10 (sesión ECC/OpenCode)
- **Agente que la origina:** SCENE_QUESTIONER (duda DUDA-005, contradicción C6)
- **Estado:** CERRADA
- **Regla TM afectada:** prioridad entre el **gap** (§9.1 / §9.3) y la **regla de 2** (§4.2 / §10.2)

### Pregunta
Al abrir una vela nueva, ¿se evalúa **primero el gap** o **primero la regla de 2** (§4.2); y en
caso de **gap a favor de 1**, se activa el **posible TT** sin aplicar la regla de 2?
(Pregunta completa de origen: `PREGUNTAS_PENDIENTES.md` DUDA-005.)

### Contexto objetivo
- Contradicción C6: §4.2 (si falla una condición de 2 → módulo / A Grande) frente a §9.1 (el gap a
  favor de 1 contiene A y B implícitas); §9.3 estaba marcada «PROPUESTA, PENDIENTE DE CONFIRMAR».
- Fronteras de vela de la muestra con movimiento continuo (6→7, 7→8, 8→9).

### Respuesta literal de Javier
> "primero gap si hay gap no hay 2 ."

### Regla general extraída
- Al abrir una vela nueva se evalúa **primero el gap**.
- **Si hay gap, no se aplica la regla de 2.**
- La regla de 2 (§4.2) se evalúa **solo cuando no hay gap**.
- Confirma §9.3.

### Ejemplo
- Gap a favor de 1 ⇒ se lee el gap (A y B implícitas); **no** se aplica la regla de 2.

### Contraejemplo
- Sin gap y falla una condición de 2 ⇒ 1 pasa a **módulo** y el movimiento contrario es **A Grande**.
- Aplicar la regla de 2 existiendo gap ⇒ **incorrecto**.

### Vocabulario aprobado
`gap`, `regla de 2`, `2`, `módulo`, `A Grande`, `posible 2`, `salida en plano`, `TT`.

### Tests creados
- Test rojo de prioridad gap ↔ regla de 2: `tests/rules.closed.red.test.js` (lo creará TDD_GUIDE).

### Archivos modificados
- `DECISIONES_EXPERTO.md` (este registro), `PREGUNTAS_PENDIENTES.md` (DUDA-005 → CERRADA).

### Versión de implementación
- Núcleo: `0.0.1-scaffold` (sin cambios de lógica).

### Regresiones detectadas
- Ninguna (aún no hay implementación de módulo / 2 / 3).

### Estado de la regla
- **CERRADA**. Cierra C6; confirma §9.3.

---

## DEC-006

- **ID:** DEC-006
- **Fecha y hora:** 2026-10-18 (sesión ECC/OpenCode)
- **Agente que la origina:** SCENE_QUESTIONER (duda DUDA-001, contradicción C1)
- **Estado:** **PROVISIONAL** — respuesta ambigua; hay interpretación tentativa pero **NO cerrada** (ver DUDA-006 / DUDA-007)
- **Regla TM afectada:** §10.7 (C Grande y CUT), §10.4 (final de A Grande); inicio del movimiento contrario como B Grande candidata; concepto «A Grande acaba cuando supera el módulo».

### Pregunta
¿Cuál es el **final de A Grande** (referencia de CUT) y, con el recorrido de la vela 8, se confirma
**C Grande → CUT** o **B Grande → AUT** con la **C Grande candidata cancelada**?
(Pregunta completa de origen: `PREGUNTAS_PENDIENTES.md` DUDA-001, escenas A/B.)

### Contexto objetivo
- Contradicción C1: el golden atribuye **CUT dentro de la vela 8**, pero los ticks no permiten que
  C Grande alcance el final de A Grande hasta mucho después (§8 de `CRONOLOGIA_MOVIMIENTOS.md`).
- R-A: módulo vela 1+2 (rango 77,90 = 29838,20 − 29760,30); A Grande termina en **29820,80**;
  máximo del módulo = **29838,20**.
- R-C / R-D (vela 8): A Grande candidata = 32,00 pts; B Grande candidata alcanza el 100 % (29712,40)
  y **supera** el 127 % + 0,25 (nivel 29703,51) hasta **29683,20**.
- Serie de precio: **Bid** (`AUDITORIA_DATOS.md` §3).

### Respuesta literal de Javier
> "en cunato ala duda 1 si te refieres a la vela 8 , 1, a vela 9 sigue con a , baja esb solo si llega entre 100% y 127%+0,25 si lego ahsta ahi es b garnde peor creo tu tienes los ticks entonces sera b,aut si no supero b grande y se dio la vuelya sera b,c es sencillo peor preguntame cualquier duda . en caunto a las escenas solo es b grande si llega a los parametros que te eh dicho cuando llega es b grande, incio de un movimeinto contrario a a grande es elinicio no confirmado . otra pregunta conceptual cuadno termina a grande facil: a garnde acaba cuando supera el modulo, por ejemplo veja bajista a garnde sube si supera el modulo es aut y nuevo , y a garnde es mov contrario al modulo"

### Regla general candidata (interpretación tentativa — **NO CERRADA**)

> **Marca de estado:** lo que sigue es interpretación **tentativa** del transcript anterior. Está
> **PROVISIONAL** por ambigüedad de la respuesta. **No** pasa a `REGLAS_CERRADAS.md` ni a tests
> verdes hasta que DUDA-006 / DUDA-007 se respondan.

- **(a) Inicio del movimiento contrario a A Grande.** El movimiento contrario a A Grande comienza
  como **inicio no confirmado** (B Grande **candidata**); se confirma como **B Grande** al alcanzar
  sus parámetros: **100 %** y, al superar, **127 % + 0,25**.
  - Literal de apoyo: «incio de un movimeinto contrario a a grande es elinicio no confirmado»;
    «solo es b grande si llega a los parametros que te eh dicho cuando llega es b grande».
- **(b) Desenlace sin superar el nivel.** Si B Grande **no supera** el 127 % + 0,25 y **se da la
  vuelta** → es **B Grande** y el movimiento que sube después es **C Grande**.
  - Literal de apoyo: «si no supero b grande y se dio la vuelya sera b,c».
  - Coherente con DEC-003 (superar ≠ tocar): si supera → `b, AUT`; si no supera y vuelve → `b, C`.
- **(c) Afirmación conceptual sobre el final de A Grande.** «A Grande acaba cuando **supera el
  módulo**»; **A Grande = movimiento contrario al módulo**.
  - Literal de apoyo: «a garnde acaba cuando supera el modulo … y a garnde es mov contrario al
    modulo».
  - **⚠️ (c) NO ESTÁ CLARA y probablemente choca con los hechos** (ver *Comprobación contra los
    ticks*, Hecho 1). No se adopta como regla. Es el objeto de DUDA-007.

### Comprobación contra los ticks (hechos, sin golden)

- **Hecho 1 — (c) no aplica a esta muestra.** En la lectura principal (R-A) **A Grande termina en
  29820,80** y el **máximo del módulo es 29838,20** (vela 1). Por tanto **A Grande NO supera el
  módulo** (29820,80 < 29838,20). La afirmación (c) «A Grande acaba cuando supera el módulo» **no se
  puede aplicar tal cual** a este caso.
- **Hecho 2 — (a)/(b) producen AUT y C Grande posterior, no CUT en la vela 8.** En la **vela 8**,
  desde el máximo de A Grande (29744,40), **B Grande sí supera el 127 % + 0,25** (nivel 29703,51) y
  llega hasta **29683,20**. Según (a)/(b) → **AUT** en ese tick; después **C Grande** subiría, pero
  **no alcanza el final de A Grande dentro de la vela 8** (ningún tick ≥ 29738,40/29744,40 hasta la
  **vela 16/17**). Es decir: **el CUT no ocurre en la vela 8**; ocurriría cuando C Grande alcance el
  final de A Grande, más tarde.
- **Consecuencia:** los hechos refuerzan «B Grande → AUT → C Grande posterior» y **contradicen** el
  CUT de la vela 8 del golden. Queda **registrado**; **no** se mueve el evento de vela ni se reescribe
  el golden sin respuesta del experto (anti-spoiler).

### Ejemplo
- A Grande = 32,00 pts (máx. 29744,40). 100 % = 29712,40; 127 % + 0,25 (1 tick) = 29703,51.
  B Grande **supera** 29703,51 y llega a 29683,20 ⇒ **AUT** (según (a)).

### Contraejemplo
- B Grande que **toca** 127 % + 0,25 **y vuelve** sin superarlo ⇒ **no** AUT; es **B Grande** y el
  alcista posterior es **C Grande** (coincide con DEC-003).
- Aplicar (c) «A Grande acaba cuando supera el módulo» a R-A ⇒ **incorrecto** (A Grande = 29820,80,
  módulo = 29838,20; no lo supera).

### Vocabulario aprobado
`A Grande`, `B Grande`, `C Grande`, `módulo`, `movimiento contrario`, `inicio no confirmado`,
`candidata`, `100 %`, `127 % + 0,25`, `AUT`, `CUT`, `retroceso`, `lectura`.
(**Prohibido** como clasificación: `local`, `superior`, `estructura`, `giro`, `B excesiva`,
`observador`.)

### Tests creados
- **PENDIENTE** (no creable todavía): la regla está **PROVISIONAL**; requiere resolver DUDA-006 /
  DUDA-007 antes de generar test rojo. Tests afectados a futuro: C Grande / CUT y AUT en
  `tests/rules.closed.red.test.js`; golden vela 8 (`C_CANDIDATA`, `CUT`, hoy PENDIENTE).

### Archivos modificados
- `DECISIONES_EXPERTO.md` (este registro, DEC-006).
- `PREGUNTAS_PENDIENTES.md` (DUDA-001 → PARCIALMENTE RESPONDIDA; nuevas DUDA-006, DUDA-007).

### Versión de implementación
- Núcleo: `0.0.1-scaffold` (sin cambios de lógica).

### Regresiones detectadas
- Ninguna (aún no hay implementación del bloque C Grande / CUT).

### Estado de la regla
- **PROVISIONAL** (ambigua). Interpretación tentativa (a)/(b) registrada y marcada **NO cerrada**;
  (c) marcada **NO clara** y en conflicto con los hechos (Hecho 1). Cierra parcialmente DUDA-001;
  **no** desbloquea el cierre de C Grande/CUT hasta DUDA-006 / DUDA-007.

---

## DEC-007

- **ID:** DEC-007
- **Fecha y hora:** 2026-10-18 (sesión ECC/OpenCode)
- **Agente que la origina:** SCENE_QUESTIONER (respuestas literales del experto: ACLARACIÓN 1
  unidad de AUT · ACLARACIÓN 2 inicio y confirmación de B Grande · ACLARACIÓN 4 A Grande y
  módulo · ACLARACIÓN 5 salida en plano)
- **Estado:** **CERRADA** para ACLARACIONES 1, 2 y 4; **SALIDA EN PLANO = PENDIENTE DE REGLA
  EXPERTA** dentro de esta misma entrada (ACLARACIÓN 5, ABIERTA)
- **Regla TM afectada:** unidad/margen de **AUT**; **inicio y confirmación de B Grande**;
  **A Grande y módulo**; **salida en plano**
- **Título:** ACLARACIONES AUT / B GRANDE / A GRANDE / SALIDA EN PLANO

### Pregunta
¿Con qué unidad se fija el margen de AUT, cómo se inicia y confirma B Grande, qué significa
exactamente «A Grande es el movimiento contrario al módulo» y cuál es la tolerancia de la salida
en plano?

### Contexto objetivo
- El CSV muestra cambios de precio de **0,10**; el tick TM vale **0,25 puntos** (1 tick).
- El inicio del movimiento contrario a A Grande y su confirmación como B Grande admitían dos
  lecturas (inicio = B Grande vs inicio no confirmado → confirmación).
- «A Grande acaba cuando supera el módulo» (DEC-006) chocaba con los hechos.
- La tolerancia de la salida en plano seguía abierta (por debajo de DEC-001 seguía sin regla
  experta definitiva para este caso).

### Respuesta literal del experto (transcripción literal, entre comillas)

**ACLARACIÓN 1 (UNIDAD DE AUT):**
> "1 tick TM = 0,25 puntos. AUT = superar el 127 % de A Grande + 0,25 puntos. El hecho de que el CSV muestre cambios de precio de 0,10 no modifica esta regla. Esos cambios son incrementos observados en la serie de precios, pero el margen TM que utilizamos para AUT sigue siendo 0,25 puntos. La implementación debe expresar el margen como: aut_extra_points = 0.25. No debe derivarlo automáticamente del menor cambio consecutivo observado en el CSV. Regla cerrada: Alcanzar exactamente el 127 % no confirma AUT. Alcanzar exactamente 127 % + 0,25 tampoco basta si la regla exige superar. AUT se confirma cuando el precio supera 127 % + 0,25. Si alcanza la zona y se da la vuelta sin superarla: B Grande continúa siendo B Grande; el movimiento contrario comienza como C Grande candidata; no existe AUT."

**ACLARACIÓN 2 (INICIO Y CONFIRMACIÓN DE B GRANDE):**
> "El movimiento contrario a A Grande marca el posible inicio de B Grande, pero todavía no confirma B Grande. Secuencia: A Grande -> comienza movimiento contrario -> B Grande candidata. B Grande se confirma cuando alcanza el 100 % de A Grande. Después: Si B Grande queda entre el 100 % y 127 % + 0,25: B Grande confirmada, sin AUT. Si el precio supera 127 % + 0,25: AUT inmediato. Si B Grande no supera 127 % + 0,25 y comienza movimiento contrario: C Grande candidata. Si después B Grande crea un nuevo extremo: C Grande candidata se cancela; B Grande continúa. No escribas que el movimiento 'solo es B Grande' cuando alcanza el 100 %. Su inicio existe antes como B Grande candidata. El 100 % la confirma."

**ACLARACIÓN 4 (A GRANDE Y MÓDULO):**
> "A Grande es el movimiento contrario al módulo. Si ese movimiento supera el módulo, hay AUT y puede ser nuevo 1."

Instrucción literal del experto:
> "No traduzcas todavía esto como: 'A Grande siempre termina cuando supera el módulo.' Esa redacción puede ser incorrecta o incompleta. Registra provisionalmente: A Grande es el movimiento contrario al módulo. Si el movimiento contrario supera el autocorte correspondiente al módulo, se confirma AUT. Desde AUT ese movimiento puede considerarse posible 1, sin que su función definitiva quede decidida todavía."

**ACLARACIÓN 5 (SALIDA EN PLANO):**
> "La regla de salida en plano sigue ABIERTA. No deduzcas su tolerancia a partir de: el menor cambio de precio del CSV; el tick TM de 0,25; la diferencia de -0,80 de esta muestra. Son conceptos distintos. Registra: SALIDA EN PLANO = PENDIENTE DE REGLA EXPERTA."

### Regla general extraída
- **Margen de AUT:** `aut_extra_points = 0.25` (fijo, en puntos del instrumento; **no** derivado
  del menor cambio consecutivo observado en el CSV).
- **AUT** solo se confirma al **SUPERAR 127 % + 0,25**. Alcanzar exactamente el 127 % **no**
  confirma AUT; alcanzar exactamente 127 % + 0,25 **tampoco** basta. Si alcanza la zona y se da
  la vuelta sin superarla: **B Grande continúa siendo B Grande**, el movimiento contrario
  comienza como **C Grande candidata** y **no existe AUT**.
- **B Grande:** el movimiento contrario a A Grande marca el posible inicio (B Grande
  **candidata**) pero **no** confirma B Grande. Secuencia: A Grande → comienza movimiento
  contrario → B Grande candidata. **B Grande se confirma al alcanzar el 100 % de A Grande.**
  Luego: 100 % a 127 % + 0,25 → B Grande confirmada **sin** AUT; supera 127 % + 0,25 → **AUT
  inmediato**; no supera y comienza movimiento contrario → **C Grande candidata**; si después
  B Grande crea un nuevo extremo → **C Grande candidata se cancela** y **B Grande continúa**.
- **A Grande y módulo (provisional, según instrucción literal):** A Grande es el **movimiento
  contrario al módulo**. Si el movimiento contrario **supera el autocorte correspondiente al
  módulo**, se confirma **AUT**; desde AUT ese movimiento **puede considerarse nuevo 1** (alias
  «posible 1», unificado por **DEC-012**), sin que su función definitiva quede decidida. **No** se
  traduce todavía como «A Grande siempre termina cuando supera el módulo».
- **Salida en plano (ACLARACIÓN 5):** la tolerancia queda **PENDIENTE**; **no** se deduce del
  menor cambio del CSV, ni del tick TM de 0,25, ni de la diferencia de −0,80 de esta muestra.
  Registro: **SALIDA EN PLANO = PENDIENTE DE REGLA EXPERTA**.

### Ejemplo
- AUT: el precio **supera** 127 % + 0,25 (con `aut_extra_points = 0.25`) ⇒ AUT en ese tick.
- B Grande: movimiento contrario alcanza el 100 % de A Grande ⇒ **B Grande confirmada**; entre
  100 % y 127 % + 0,25 ⇒ B Grande confirmada, sin AUT.

### Contraejemplo
- Alcanzar exactamente 127 % ⇒ **no** AUT.
- Alcanzar exactamente 127 % + 0,25 ⇒ **no** basta; debe **superarlo**.
- Alcanzar la zona y volver sin superarla ⇒ **no** AUT; B Grande continúa siendo B Grande y el
  movimiento contrario comienza como **C Grande candidata**.
- Escribir que el movimiento «solo es B Grande» cuando alcanza el 100 % ⇒ **incorrecto** (su
  inicio existe antes como **B Grande candidata**).
- Derivar `aut_extra_points` del menor cambio del CSV ⇒ **incorrecto** (es fijo `0.25`).
- Traducir «A Grande siempre termina cuando supera el módulo» ⇒ **prohibido por ahora**
  (instrucción literal del experto).
- Deducir la tolerancia de salida en plano del CSV / del tick / de −0,80 ⇒ **incorrecto**.

### Vocabulario aprobado
`AUT`, `aut_extra_points`, `A Grande`, `B Grande`, `B Grande candidata`, `C Grande candidata`,
`módulo`, `autocorte`, `movimiento contrario`, `127 %`, `100 %`, `superar`, `salida en plano`,
`gap`, `nuevo 1` (alias `posible 1`, unificado por **DEC-012**).
(**Prohibido** como clasificación: `local`, `superior`, `estructura`, `giro`, `B excesiva`,
`observador`.)

### Tests creados
- **PENDIENTE** de TDD_GUIDE (no los crea SCENE_QUESTIONER): test rojo del margen fijo
  `aut_extra_points = 0.25`; test rojo «AUT solo al SUPERAR»; test rojo de la secuencia de
  B Grande (candidata → 100 % confirma → 100..127+0,25 sin AUT → AUT al superar → C Grande
  candidata si no supera y vuelve → cancelación de C Grande candidata si B Grande crea nuevo
  extremo).

### Versión de implementación
- Núcleo: `0.0.1-scaffold` (sin cambios de lógica).

### Estado de la regla
- **CERRADA** para ACLARACIÓN 1 (margen/unidad de AUT), ACLARACIÓN 2 (inicio y confirmación de
  B Grande) y ACLARACIÓN 4 (A Grande = movimiento contrario al módulo; AUT al superar el
  autocorte del módulo; nuevo 1 (alias «posible 1») sin función definitiva).
- **ABIERTA / PENDIENTE:** ACLARACIÓN 5 → **SALIDA EN PLANO = PENDIENTE DE REGLA EXPERTA**
  (registrada como **DUDA-008** en `PREGUNTAS_PENDIENTES.md`).

---

## DEC-008

- **ID:** DEC-008
- **Fecha y hora:** 2026-10-18 (sesión ECC/OpenCode)
- **Agente que la origina:** SCENE_QUESTIONER / RULES_ANALYST (respuesta literal del experto
  sobre la máquina de estados A Grande → B candidata → B Grande → C Grande / AUT)
- **Estado:** **CERRADA** (el experto lo da como definitivo y **calca ACLARACIÓN 2**)
- **Regla TM afectada:** inicio/confirmación de B Grande (H12), franja 100 %–127 % + 0,25,
  cambio de sentido → C Grande, superación → AUT / posible 1 (H13)
- **Título:** MÁQUINA DE ESTADOS — A GRANDE · B candidata · B Grande · C Grande · AUT

### Pregunta
¿Cómo debe leerse, paso a paso, el movimiento contrario a A Grande: cuándo es **B candidata**,
cuándo **B Grande**, cuándo **C Grande** y cuándo **AUT → posible 1**?

### Contexto objetivo
- El experto subraya que **esta parte debe quedar CLARA y MEMORIZADA**.
- Fija la franja numérica: `100 % ≤ recorrido ≤ 127 % + 0,25` → **B Grande**; `recorrido >
  127 % + 0,25` → **AUT inmediato**.
- El umbral de confirmación de B Grande es el **100 % de A Grande** (ya cerrado en DEC-007 /
  ACLARACIÓN 2); DEC-008 lo recalca y lo ordena como tabla de estados.

### Respuesta literal del experto (transcripción literal, entre comillas)
> "esta parte no la tienes clara y es importante quede claro y memorizado.
> A Grande → movimiento contrario.
> Si todavía no alcanza el 100 %: movimiento contrario sin confirmar como B Grande.
> Si alcanza el 100 % y no supera 127 % + 0,25: B Grande.
> Si estando en B Grande cambia de sentido: C Grande.
> Si supera 127 % + 0,25: AUT → posible 1 → se observa lo que ocurre después.
> Movimiento contrario a A Grande → B candidata. Si no alcanza el 100 %: B candidata (todavía no es B Grande).
> Si alcanza el 100 %, pero no supera 127 % + 0,25: 100 % ≤ recorrido ≤ 127 % + 0,25 → B Grande.
> Si supera 127 % + 0,25: recorrido > 127 % + 0,25 → AUT inmediato."

### Regla general extraída
- **A Grande** genera un **movimiento contrario**.
- Ese movimiento contrario comienza como **B candidata** (sin confirmar).
- Mientras **no alcanza el 100 %** de A Grande: sigue siendo **B candidata**; **todavía no es
  B Grande**.
- Si **alcanza el 100 %** y **no supera 127 % + 0,25** (es decir, `100 % ≤ recorrido ≤
  127 % + 0,25`): → **B Grande** (sin AUT).
- Si **estando en B Grande cambia de sentido**: → **C Grande**.
- Si **supera 127 % + 0,25** (`recorrido > 127 % + 0,25`): → **AUT inmediato → posible 1 → se
  observa lo que ocurre después**.

### Ejemplo
- Recorrido = 80 % de A Grande ⇒ **B candidata** (todavía no es B Grande).
- Recorrido = 100 %…127 % + 0,25 ⇒ **B Grande** (sin AUT).
- Recorrido > 127 % + 0,25 ⇒ **AUT inmediato → posible 1**.

### Contraejemplo
- Escribir «B Grande» con un recorrido **por debajo del 100 %** ⇒ **incorrecto** (es B candidata).
- Activar **AUT** dentro de la franja `100 %–127 % + 0,25` ⇒ **incorrecto** (es B Grande sin AUT).
- Llamar **C Grande** al movimiento contrario antes de existir B Grande ⇒ **incorrecto** (solo
  existe C Grande cuando B Grande cambia de sentido).

### Vocabulario aprobado
`A Grande`, `B candidata`, `B Grande`, `C Grande`, `100 %`, `127 % + 0,25`, `AUT`, `posible 1`,
`movimiento contrario`.
(**Prohibido** como clasificación: `local`, `superior`, `estructura`, `giro`, `B excesiva`,
`observador`.)

### Tests creados
- **PENDIENTE** de TDD_GUIDE (no lo crea SCENE_QUESTIONER): test rojo de la **tabla de estados**
  (contrario → B candidata; <100 % → B candidata; `100 % ≤ x ≤ 127 % + 0,25` → B Grande;
  B Grande cambia de sentido → C Grande; `x > 127 % + 0,25` → AUT inmediato → posible 1).

### Archivos modificados
- `DECISIONES_EXPERTO.md` (este registro, DEC-008).
- `REGLAS_CERRADAS.md` (H12/H13 reescritas + TABLA DE ESTADOS).
- `REGLAS_PROVISIONALES.md` (PR-m / PR-n alineadas).
- `DICCIONARIO_TM.md` (entrada `B candidata`; coherencia de `B Grande`, `C Grande`, `posible 1`, `AUT`).

### Versión de implementación
- Núcleo: `0.0.1-scaffold` (sin cambios de lógica).

### Regresiones detectadas
- Ninguna (aún no hay implementación del bloque B Grande / C Grande / AUT).

### Estado de la regla
- **CERRADA**. Calca ACLARACIÓN 2 (DEC-007); cierra la máquina de estados de B Grande / C Grande /
  AUT. No reabre C1 (C Grande/CUT en la vela 8), que sigue **BLOQUEANTE**.

---

## DEC-009

- **ID:** DEC-009
- **Fecha y hora:** 2026-10-18 (sesión ECC/OpenCode)
- **Agente que la origina:** SCENE_QUESTIONER / RULES_ANALYST (respuesta literal del experto a la duda abierta DUDA-008)
- **Estado:** CERRADA
- **Regla TM afectada:** salida en plano (A1 / A4) — frontera **plano ↔ gap**; interacción con la regla de 2 (H11)
- **Título:** SALIDA EN PLANO — TOLERANCIA (plano ≤ 1 tick TM = 0,25 puntos; > 1 tick = gap)

### Pregunta
¿Cuál es la **tolerancia exacta** de la **salida en plano** al abrir una vela nueva, sin deducirla
del menor cambio del CSV, del tick TM de 0,25 ni de la diferencia de −0,80 de esta muestra?
(Pregunta completa de origen: `PREGUNTAS_PENDIENTES.md` DUDA-008.)

### Contexto objetivo
- Al abrir una vela nueva el núcleo comprueba **primero el gap** y, si no hay gap, **salida en
  plano** (A4 / H11 / DEC-005).
- **DEC-007 / ACLARACIÓN 5** dejó la tolerancia de la salida en plano **PENDIENTE DE REGLA
  EXPERTA** (registrada como **DUDA-008**), prohibiendo deducirla del menor cambio del CSV, del
  tick TM o de la diferencia de −0,80 de la muestra.
- **DEC-001** había propuesto **±1 tick** de forma provisional (test rojo pendiente); **DEC-007 /
  ACLARACIÓN 5** la reabrió como PENDIENTE hasta nueva regla del experto.
- Sin este umbral no es implementable la frontera **plano ↔ gap** ni el arranque del **posible 2**
  del Bloque 1.

### Respuesta literal del experto
> "salida en plano damos un mini [margen] de un tick"

### Interpretación registrada (explícita)
- **SALIDA EN PLANO:** se considera **plano** si la diferencia entre el **cierre del movimiento
  anterior** y la **apertura de la vela siguiente** es **≤ 1 tick TM = 0,25 puntos**.
- Si la diferencia es **> 1 tick** → **GAP** (y si hay gap, **no** se aplica la regla de 2; ver
  **H11**).
- Esto **RESUELVE** la duda abierta **DUDA-008** y se fija **por regla del experto**, **NO**
  derivándola del **menor cambio del CSV** ni del **delta −0,80** de la muestra.

### Regla general extraída
- **Salida en plano** ⇔ `|cierre del movimiento anterior − apertura de la vela siguiente| ≤ 1 tick TM`.
- Con **1 tick TM = 0,25 puntos** en esta muestra ⇒ umbral **`plano_max_points = 0.25`** (fijo).
- Si `|diferencia| > 0,25` puntos ⇒ **gap**; **con gap no se aplica la regla de 2** (H11).
- Si es **plano** (no hay gap), se habilita el camino de **posible 2** (condicionado al resto de
  condiciones de 2, A1).
- El umbral es **fijo** y **no** se deriva del CSV ni del delta −0,80 de la muestra.

### Ejemplo y contraejemplo
- **Ejemplo (plano):** cierre del movimiento anterior = 29811,60; apertura de la vela siguiente =
  29811,50 ⇒ `|Δ| = 0,10 ≤ 0,25` ⇒ **salida en plano** ⇒ posible 2.
- **Contraejemplo (gap):** `|Δ| > 0,25` puntos ⇒ **no** es salida en plano ⇒ **gap** (con gap no se
  aplica la regla de 2, H11).
- **Nota:** el umbral **no** se deriva del delta −0,80 de la muestra; esta decisión **no**
  reclasifica eventos de vela ni toca el golden (anti-spoiler).

### Vocabulario aprobado
`salida en plano`, `gap`, `plano_max_points`, `posible 2`, `2`, `regla de 2`, `tick`, `puntos`.
(**Prohibido** como clasificación: `local`, `superior`, `estructura`, `giro`, `B excesiva`,
`observador`.)

### Tests creados
- **PENDIENTE** de TDD_GUIDE (no lo crea SCENE_QUESTIONER): **test rojo de H14** — frontera
  **plano ↔ gap** con umbral fijo **`plano_max_points = 0.25`** (no derivado del CSV).

### Registro operativo
- **Archivos modificados:** `DECISIONES_EXPERTO.md` (este registro, DEC-009);
  `REGLAS_CERRADAS.md` (**H14**); `REGLAS_PROVISIONALES.md` (**PR-p → CERRADA por DEC-009**);
  `CONTRADICCIONES.md` (nota: DUDA-008 resuelta por DEC-009); `PREGUNTAS_PENDIENTES.md`
  (**DUDA-008 → CERRADA**).
- **Versión de implementación:** Núcleo `0.0.1-scaffold` (sin cambios de lógica).
- **Regresiones detectadas:** Ninguna (aún no hay implementación de la frontera plano/gap).
- **Estado de la regla:** **CERRADA**. Cierra **DUDA-008**; rige A1 / A4 y H14. **NO** cierra el
  Gate Cero (siguen abiertas DUDA-001 reformulada y DUDA-009).

---

## DEC-010

- **ID:** DEC-010
- **Fecha y hora:** 2026-10-18 (sesión ECC/OpenCode)
- **Agente que la origina:** SCENE_QUESTIONER / RULES_ANALYST (respuesta literal del experto sobre
  el fin de A Grande: 29.738,40 frente a 29.744,40)
- **Estado:** **CERRADA** (fin de A Grande = extremo del movimiento, 29.744,40). La parte «y creo
  hace TT en esa vela» queda **TENTATIVA / pendiente de precisar** (no se cierra).
- **Regla TM afectada:** §10.4 — **final de A Grande** (referencia de CUT); coherencia entre velas;
  relación A Grande → B Grande → AUT.
- **Título:** FIN DE A GRANDE — COHERENCIA ENTRE VELAS (extremo 29.744,40, no 29.738,40)

### Pregunta
¿A Grande termina en **29.738,40** o en **29.744,40**? Y si termina en 29.738,40, ¿qué movimiento
es el tramo **29.738,40 → 29.744,40**?

### Contexto objetivo
- **A Grande = movimiento contrario al módulo** (DEC-006 / DEC-007 ACLARACIÓN 4 / candidato de
  `LECTURAS_VELAS_6_9.md`): ascenso `29712,40` (mín. vela 7) → extremo en la vela 8, alcista.
- El ascenso **cruza la frontera de vela 7→8 sin interrupción** y **crea un nuevo extremo** en la
  vela 8: candidatos de fin de A Grande = `29738,40` (máx. vela 7) o `29744,40` (máx. vela 8)
  (`LECTURAS_VELAS_6_9.md`, Parte E y Bloqueo 1).
- Hechos de tick (Bid): vela 7 máximo `29738,40` @16:36:34.774; vela 8 máximo `29744,40`
  @16:37:10.254; después la vela 8 **baja** hasta `29683,20` @16:37:59.175 (cierre `29689,10`).
- Bloqueo abierto relacionado: **C7** (A Grande / módulo) y **C1** (C Grande/CUT, vela 8).

### Respuesta literal del experto
> "¿A Grande termina en 29.738,40 o en 29.744,40? Y si termina en 29.738,40, ¿qué movimiento es el
> tramo 29.738,40 → 29.744,40? buena pregunta hay que usar la coherencia en esa vela subio con
> agarnde y continuo el moviemnto en la siguiente, esta no sale en plano por anto casism eguro hizo
> a, b aut y si huebria seguido para arriba 10 puntos por ejemplo hubirea sido tt, peor vemos
> quenostinuo poco y bajo portanto la subida de a grande es claramente hasta la sihuiente vala la
> cual baja y hace b,aut y creo hace tt ene sa vela"

### Interpretación registrada (explícita)
- **A Grande extiende / actualiza su extremo** mientras el movimiento **continúe en la vela
  siguiente** (coherencia entre velas). **A Grande NO termina en el primer máximo si la vela
  siguiente sigue subiendo sin volver.**
- **Aplicado a la muestra:** A Grande = **29.712,40 → 29.744,40** (cruza las velas 7 y 8). Por
  tanto el **extremo es 29.744,40**, **no** 29.738,40. El tramo 29.738,40 → 29.744,40 **no es un
  movimiento nuevo**: es la **misma A Grande** que extiende su extremo.
- Ese movimiento **no sale en plano** (no hay cambio de dirección al abrir la vela 8), así que
  «**casi seguro hizo A, B, AUT**».
- En esa vela (**vela 8**) baja → **B Grande → AUT**. El experto añade «**y creo hace TT en esa
  vela**»: se marca como **TENTATIVO del experto**; **«TT» aquí queda por precisar** (no se
  convierte en regla cerrada).
- Si el movimiento **hubiera seguido subiendo ~10 puntos**, habría sido **otra cosa (TT)**; como
  **continuó poco y bajó**, es **A Grande**.

### Regla general extraída
- **Fin de A Grande (coherencia entre velas):** el extremo de A Grande **se actualiza mientras el
  movimiento continúe en la vela siguiente sin volver**; el fin de A Grande es el **extremo del
  movimiento** (aquí **29.744,40**).
- **No** se cierra A Grande en el **primer máximo** (`29.738,40`) si la **vela siguiente lo
  extiende** (`29.744,40`).
- El tramo entre el primer máximo y el extremo extendido **pertenece a la misma A Grande** (no crea
  un movimiento adicional).
- Tras ese extremo, el **movimiento contrario bajista** es **B Grande**; al **superar 127 % + 0,25**
  ⇒ **AUT** (regla ya cerrada: H9 / DEC-003).
- Parte **TENTATIVA** (no cerrada): «TT en esa vela» — pendiente de precisar qué «TT» señala el
  experto en la vela 8.

### Ejemplo
- A Grande `29712,40 → 29744,40` (máx. vela 7 `29738,40` extendido a máx. vela 8 `29744,40`):
  el extremo de A Grande es **`29744,40`**; desde ahí, B Grande bajista y **AUT** al superar su
  `127 % + 0,25`.

### Contraejemplo
- Cerrar A Grande en el **primer máximo `29738,40`** aunque la vela siguiente lo extienda a
  `29744,40` ⇒ **incorrecto**.
- Leer el tramo `29738,40 → 29744,40` como un **movimiento nuevo** ⇒ **incorrecto** (es la misma
  A Grande que actualiza su extremo).
- Adoptar «y creo hace TT en esa vela» como **regla cerrada** ⇒ **incorrecto** (queda TENTATIVO).

### Vocabulario aprobado
`A Grande`, `B Grande`, `AUT`, `TT`, `módulo`, `movimiento contrario`, `extremo`, `coherencia`,
`127 % + 0,25`, `posible 1`.
(**Prohibido** como clasificación: `local`, `superior`, `estructura`, `giro`, `B excesiva`,
`observador`.)

### Tests creados
- **PENDIENTE** de TDD_GUIDE (no lo crea SCENE_QUESTIONER): test rojo del **fin de A Grande por
  coherencia entre velas** (A Grande extiende su extremo mientras el movimiento continúe en la vela
  siguiente sin volver; no cerrar en el primer máximo).

### Registro operativo
- **Archivos modificados:** `DECISIONES_EXPERTO.md` (este registro, DEC-010);
  `REGLAS_CERRADAS.md` (**H15**); `CONTRADICCIONES.md` (**C7** fin de A Grande → CERRADO por
  DEC-010/H15, módulo abierto; **C1** → PENDIENTE DE CONFIRMACIÓN); `PREGUNTAS_PENDIENTES.md`
  (**DUDA-009** → parcialmente respondida; nueva **DUDA-010**).
- **Versión de implementación:** Núcleo `0.0.1-scaffold` (sin cambios de lógica).
- **Regresiones detectadas:** Ninguna (aún no hay implementación del bloque A Grande / B Grande /
  AUT).

### Estado de la regla
- **CERRADA** para el **fin de A Grande** (extremo `29.744,40` por coherencia entre velas). **NO**
  cierra el **Gate Cero**; **NO** cierra **C1** (queda **PENDIENTE DE CONFIRMACIÓN** por
  **DUDA-010**); la parte «TT en esa vela» queda **TENTATIVA**.

---

## DEC-011

- **ID:** DEC-011
- **Fecha y hora:** 2026-10-18 (sesión ECC/OpenCode)
- **Agente que la origina:** SCENE_QUESTIONER / RULES_ANALYST (respuesta literal del experto a
  **DUDA-010**: confirmar la lectura de la **vela 8**)
- **Estado:** **CERRADA** (confirma **C1**: vela 8 = **A Grande + B Grande → AUT**; **NO** hay
  **C Grande** ni **CUT** en la vela 8). Introduce además la **concurrencia de lecturas**
  (**H16**) y el **módulo por descarte** (**H17**, PROVISIONAL).
- **Regla TM afectada:** §10.7 (C Grande y CUT), §10.4 (A Grande), §10.8 (concurrencia de
  lecturas); módulo por descarte
- **Título:** VELA 8 — A GRANDE + B GRANDE → AUT (NO C Grande / NO CUT) Y CONCURRENCIA DE LECTURAS

### 1. ID
DEC-011.

### 2. Fecha y hora
2026-10-18 (sesión ECC/OpenCode).

### 3. Agente que la origina
SCENE_QUESTIONER / RULES_ANALYST (duda **DUDA-010**, contradicción **C1**).

### 4. Estado
**CERRADA**. Cierra **C1** y **C8/C1b**. **NO** cierra el **Gate Cero** (siguen abiertas la
parte **módulo** de C7 / DUDA-009 y la nueva **DUDA-011**).

### 5. Regla TM afectada
§10.7 (C Grande y CUT); §10.4 (A Grande); §10.8 (concurrencia de lecturas); **módulo por
descarte**.

### 6. Título
VELA 8 — A GRANDE + B GRANDE → AUT (NO C Grande / NO CUT) Y CONCURRENCIA DE LECTURAS.

### 7. Pregunta
¿Confirmas que en la **vela 8** el recorrido es **A Grande (extremo `29.744,40`)** y después
**B Grande → AUT (posible 1)**, y que **NO** hay **C Grande** ni **CUT** en esa vela?
(Pregunta completa de origen: `PREGUNTAS_PENDIENTES.md` DUDA-010.)

### 8. Contexto objetivo
- **A Grande = movimiento contrario al módulo**; su extremo se actualiza por **coherencia entre
  velas** (**DEC-010 / H15**). En la muestra A Grande = `29712,40 → 29744,40` (cruza las velas
  7 y 8); extremo **`29.744,40`**, no `29.738,40`.
- Vela 8 (Bid): máximo `29744,40` @16:37:10.254; después **baja** hasta `29683,20` @16:37:59.175.
- Desde el extremo `29744,40`, el contrario bajista **supera el 127 % + 0,25** (`29703,51`)
  @16:37:55.363 ⇒ **AUT** (regla cerrada **H9 / DEC-003**).
- Ningún tick alcanza `29738,40`/`29744,40` dentro de la vela 8 después del máximo; el primer
  tick ≥ `29738,40` posterior es de la **vela 16/17** ⇒ ninguna C Grande puede confirmar **CUT**
  dentro de la vela 8.
- **Serie de precio:** **Bid** (`AUDITORIA_DATOS.md` §3).

### 9. Respuesta literal del experto
> "a evr es mu facil tienes q entender que peude haber 2 interpretacion leugo s evan
> resolviendo hay q estar atenta alas 2 en vela 8 en su incio si ha ido para arriba peude ser
> continua cion de a grande de la vela anterior de la vela 7 modulo por decarte y vela 8 a.b aut
> pero q como veras el restroceso de el final de vela 7 e inicio de vela 8 peude ser a grande moc
> cpontraio al modulo vela 7 y subir con b pewro se pasa lo entiendes"

### 10. Interpretación registrada (explícita y fiel)
- Puede haber **2 interpretaciones concurrentes**; **se van resolviendo después**; hay que
  **atender a las DOS** y nombrarlas **`lectura 1`** / **`lectura 2`** (vocabulario **DEC-004**).
- **Interpretación A / `lectura 1`:** en la **vela 8**, **al inicio, si ha ido para arriba**,
  puede ser **continuación de A Grande** de la vela anterior, con la **vela 7 como módulo por
  descarte** → **vela 8 = A, B, AUT**.
- **Interpretación B / `lectura 2`:** el **retroceso** del **final de la vela 7 / inicio de la
  vela 8** puede ser **A Grande** (movimiento contrario al **módulo = vela 7**) y luego **subir
  con B**, pero **«se pasa»**.
- **Confirmación clave:** la **vela 8 → A Grande, B Grande, AUT** (**NO** C Grande, **NO** CUT).

### 11. Regla general extraída
- **Concurrencia de lecturas (H16):** puede haber **2 interpretaciones simultáneas**
  (`lectura 1` / `lectura 2`); **se resuelven más adelante**; hay que **atender a ambas**.
- **Vela 8 (lectura 1):** si **al inicio ha ido para arriba**, puede ser **continuación de A
  Grande** de la vela anterior, con la **vela 7 como módulo por descarte** ⇒ **A Grande +
  B Grande → AUT**; **NO** C Grande, **NO** CUT.
- **Vela 8 (lectura 2):** el **retroceso** final de vela 7 / inicio de vela 8 puede leerse como
  **A Grande** (contrario al **módulo = vela 7**); después **sube con B**, **«pero se pasa»**
  (concepto a precisar → **DUDA-011**).
- **Módulo por descarte (H17, PROVISIONAL):** cuando no hay módulo claro, puede tomarse la
  **vela anterior** (p. ej. **vela 7**) como **módulo por descarte**, con su **A Grande
  contraria**. **NO cerrada**; la regla general del módulo sigue **PARCIAL** (C7 / DUDA-009).

### 12. Ejemplo
- **Lectura 1 (vela 8):** A Grande = `29712,40 → 29744,40` (extremo `29.744,40`) → desde ahí
  **B Grande** bajista → **supera** `29703,51` (`127 % + 0,25`) ⇒ **AUT**; **sin C Grande / CUT**
  en la vela 8.
- **Lectura 2 (vela 8):** retroceso final vela 7 / inicio vela 8 = **A Grande** del **módulo-vela
  7**; después **B** al alza, **«se pasa»**.

### 13. Contraejemplo
- Afirmar que la **vela 8** contiene **C Grande → CUT** ⇒ **incorrecto** (ningún tick alcanza
  `29738,40`/`29744,40` dentro de la vela 8).
- Leer la **vela 8** solo como **una** interpretación y descartar la **otra** antes de que se
  resuelva ⇒ **incorrecto** (hay **2 lecturas** que se atienden y se resuelven después).
- Adoptar el **módulo por descarte (vela 7)** como **regla cerrada general** ⇒ **incorrecto**
  (queda **PROVISIONAL**, H17).

### 14. Vocabulario aprobado
`A Grande`, `B Grande`, `C Grande`, `AUT`, `CUT`, `módulo`, `módulo por descarte`,
`movimiento contrario`, `retroceso`, `lectura 1`, `lectura 2`, `interpretación`,
`127 % + 0,25`, `posible 1`, `vela 8`.
(**Prohibido** como clasificación: `local`, `superior`, `estructura`, `giro`, `B excesiva`,
`observador`.)

### 15. Tests creados
- **PENDIENTE** de TDD_GUIDE (no lo crea SCENE_QUESTIONER): test rojo de la **lectura de la vela
  8** (A Grande + B Grande → AUT; **sin** C Grande / CUT en la vela 8) y test rojo de
  **concurrencia de 2 lecturas** (`lectura 1` / `lectura 2`) con resolución posterior.

### Registro operativo
- **Archivos modificados:** `DECISIONES_EXPERTO.md` (este registro, DEC-011);
  `CONTRADICCIONES.md` (**C1 → RESUELTA**; **C8/C1b → RESUELTA**; **C7** parte «módulo» →
  PARCIAL con módulo por descarte y 2 lecturas); `REGLAS_CERRADAS.md` (**H16** CERRADA;
  **H17** PROVISIONAL); `PREGUNTAS_PENDIENTES.md` (**DUDA-010 → CERRADA**; nueva **DUDA-011**).
- **Versión de implementación:** Núcleo `0.0.1-scaffold` (sin cambios de lógica).
- **Regresiones detectadas:** Ninguna (aún no hay implementación de C Grande / CUT /
  concurrencia).
- **Estado de la regla:** **CERRADA** para la lectura de la **vela 8** (A Grande + B Grande →
  AUT; **NO** C Grande / CUT) y para la **concurrencia de 2 lecturas** (H16). **H17** (módulo por
  descarte) queda **PROVISIONAL**. **NO** cierra el **Gate Cero**; **NO** toca el golden; **NO**
  mueve **CUT**.

---

## DEC-012

1. **ID:** DEC-012.
2. **Fecha y hora:** 2026-10-18 (sesión ECC/OpenCode).
3. **Agente que la origina:** SCENE_QUESTIONER / RULES_ANALYST (respuesta literal del experto a la
   duda **DUDA-011**: sentido de «se pasa» en la **lectura 2**).
4. **Estado:** **CERRADA**. Cierra **DUDA-011**. **NO** cierra el **Gate Cero** (sigue abierta
   **solo** la parte **módulo general** de **C7 / DUDA-009**).
5. **Regla TM afectada:** §10.4 (A Grande / módulo por descarte) y §10.5 (AUT / 127 % + 0,25).
6. **Título:** LECTURA 2 — «SE PASA» = B SUPERA 127 % + 0,25 → AUT → NUEVO 1.

7. **Pregunta:** En la **lectura 2**, el retroceso del final de la vela 7 / inicio de la vela 8 es
   **A Grande** del **módulo-vela 7**, y después **sube B «pero se pasa»**: ¿qué significa «se
   pasa» — que **B supera 127 % + 0,25** (**AUT**) o que **se pasa del extremo**?
   (Pregunta completa de origen: `PREGUNTAS_PENDIENTES.md` DUDA-011.)

8. **Contexto objetivo:**
   - **A Grande = movimiento contrario al módulo**; con **módulo por descarte** (vela 7) la lectura 2
     usa ese módulo (**DEC-011 / H17**, PROVISIONAL).
   - **H9 / DEC-003:** AUT se confirma **solo al SUPERAR 127 % + 0,25**; tocar y volver no es AUT.
   - **H16 / DEC-011:** coexisten **2 lecturas** (`lectura 1` / `lectura 2`) que **se resuelven más
     adelante**.
   - Serie de precio: **Bid** (`AUDITORIA_DATOS.md` §3).

9. **Respuesta literal del experto:**
   > "b se pasa es eso que super ael 127+0,25 y se convierte en aut y nuevo 1"

10. **Interpretación registrada (explícita):**
    - **«B se pasa» = B supera 127 % + 0,25** → **AUT**; ese movimiento **se convierte en nuevo 1**.
    - Corresponde a la **ESCENA A** de DUDA-011 (AUT) y **descarta** la **ESCENA B** (leer «se pasa»
      como rebasar el extremo de A Grande).
    - Coherente con **H9 / DEC-003** (AUT solo al **superar**) y con **DEC-008 / H13(c)**
      (`recorrido > 127 % + 0,25` → **AUT inmediato → nuevo 1**).
    - **Cierra DUDA-011.**

11. **Regla general extraída:**
    - En la **lectura 2**, «**se pasa**» significa que **B supera 127 % + 0,25**; en ese tick se
      confirma **AUT** y el movimiento **se convierte en nuevo 1**, sin que su función definitiva
      quede decidida todavía.
    - **Terminología unificada:** el término canónico es **nuevo 1** (**alias «posible 1»**),
      conforme a la unificación registrada en `DICCIONARIO_TM.md`.

12. **Ejemplo:** en la lectura 2, B supera el nivel `127 % + 0,25` de la A Grande del módulo-vela 7
    ⇒ **AUT → nuevo 1**.

13. **Contraejemplo:**
    - Leer «se pasa» como «rebasa el extremo de A Grande» (ESCENA B) ⇒ **incorrecto**.
    - Un B que **solo toca** 127 % + 0,25 **y vuelve** ⇒ **sin AUT** (H9 / DEC-003).

14. **Vocabulario aprobado:** `lectura 2`, `A Grande`, `B Grande`, `módulo por descarte`,
    `movimiento contrario`, `retroceso`, `127 % + 0,25`, `superar`, `AUT`, `nuevo 1` (alias
    `posible 1`).
    (**Prohibido** como clasificación: `local`, `superior`, `estructura`, `giro`, `B excesiva`,
    `observador`.)

15. **Tests creados:** **PENDIENTE** de TDD_GUIDE (no lo crea SCENE_QUESTIONER): test rojo
    «**lectura 2** — "se pasa" = supera 127 % + 0,25 → AUT → **nuevo 1**».

### Registro operativo
- **Archivos modificados:** `DECISIONES_EXPERTO.md` (este registro, DEC-012);
  `PREGUNTAS_PENDIENTES.md` (**DUDA-011 → CERRADA**); `CONTRADICCIONES.md` (**C7** sigue
  **PARCIAL**, solo módulo general abierto); unificación de terminología a **nuevo 1** (alias
  `posible 1`) en `REGLAS_CERRADAS.md` (H13(c)), `DECISIONES_EXPERTO.md` (DEC-007 / ACLARACIÓN 4),
  `REGLAS_PROVISIONALES.md` (PR-o), `PREGUNTAS_PENDIENTES.md` (DUDA-009) y `DICCIONARIO_TM.md`.
- **Versión de implementación:** Núcleo `0.0.1-scaffold` (sin cambios de lógica).
- **Regresiones detectadas:** Ninguna (aún no hay implementación de la lectura 2 / AUT).
- **Estado de la regla:** **CERRADA**. Cierra **DUDA-011**. **NO** cierra el **Gate Cero**; **NO**
  toca el golden; **NO** mueve **CUT**; **NO** cierra **C7** (sigue **PARCIAL**, solo módulo
  general).

---

## DEC-013

- **ID:** DEC-013
- **Fecha y hora:** 2026-10-18 (sesión ECC/OpenCode)
- **Agente que la origina:** RULES_ANALYST (respuesta literal del experto sobre la referencia de
  la salida en plano)
- **Estado:** **CERRADA** (regla del experto). Su **test rojo** queda **PENDIENTE** — los tests
  **no están autorizados** todavía.
- **Regla TM afectada:** A1 / H14 — **referencia de la salida en plano**; interacción con el gap
  (A4 / H11) y con la regla de 2.
- **Título:** SALIDA EN PLANO — REFERENCIA = CIERRE DE LA VELA ANTERIOR

### Pregunta
¿La salida en plano se mide contra el **cierre de la vela anterior** o contra el **cierre del
movimiento anterior**?

### Contexto objetivo
- **DEC-009 / H14** fijó el umbral de la salida en plano (`plano_max_points = 0.25`) pero la
  referencia quedó redactada como «cierre del movimiento anterior».
- Un movimiento puede atravesar varias velas; el cierre del movimiento y el cierre de la vela
  anterior pueden **no coincidir**. Sin fijar la referencia, la frontera plano ↔ gap es ambigua.

### Respuesta literal del experto
> "la salida en plano se mide contra el CIERRE DE LA VELA ANTERIOR (no contra el cierre del
> movimiento anterior)."

### Regla general extraída
- **La referencia de la salida en plano es el cierre de la VELA anterior**, **no** el cierre del
  movimiento anterior.
- Se considera **plano** si `|cierre de la vela anterior − apertura de la vela siguiente| ≤ 1 tick
  TM (0,25 puntos)`; si es **> 1 tick** es **gap**.
- **Con gap no hay salida en plano**, ni posible 2, ni 2 (H11 / A4).
- La referencia fija la **reescritura de H14** (`REGLAS_CERRADAS.md`) y de la entrada «Salida en
  plano» (`DICCIONARIO_TM.md`).

### Ejemplo y contraejemplo
- **Ejemplo (plano):** cierre de la **vela** anterior = 29811,60; apertura de la vela siguiente =
  29811,50 ⇒ `|Δ| = 0,10 ≤ 0,25` ⇒ **salida en plano**.
- **Contraejemplo:** medir el `|Δ|` contra el cierre del **movimiento** anterior cuando el
  movimiento abarca varias velas ⇒ **incorrecto** (la referencia es el cierre de la **vela**
  anterior).

### Vocabulario aprobado
`salida en plano`, `gap`, `plano_max_points`, `posible 2`, `2`, `regla de 2`, `tick`, `puntos`,
`cierre de la vela anterior`.
(**Prohibido** como clasificación: `local`, `superior`, `estructura`, `giro`, `B excesiva`,
`observador`.)

### Tests creados
- **PENDIENTE** (tests no autorizados aún): test rojo de H14 con la referencia **cierre de la vela
  anterior** y umbral fijo **`plano_max_points = 0.25`**.

### Registro operativo
- **Archivos modificados:** `DECISIONES_EXPERTO.md` (este registro, DEC-013);
  `REGLAS_CERRADAS.md` (**H14** reescrita), `DICCIONARIO_TM.md` (entrada «Salida en plano»),
  `AGENTS.md` (refuerzo del orden causal de la regla de 2 con la nueva referencia).
- **Versión de implementación:** Núcleo `0.0.1-scaffold` (sin cambios de lógica).
- **Regresiones detectadas:** Ninguna (aún no hay implementación de la frontera plano/gap).
- **Estado de la regla:** **CERRADA**. **NO** cierra el **Gate Cero** (sigue abierta la parte
  **módulo general** de C7 / DUDA-009); **NO** toca el golden.

---

## DEC-014

- **ID:** DEC-014
- **Fecha y hora:** 2026-10-18 (sesión ECC/OpenCode)
- **Agente que la origina:** RULES_ANALYST (respuesta literal del experto sobre los disparadores
  de AUT; reconcilia **IC-1**)
- **Estado:** **CERRADA** en cuanto a la **existencia de los DOS disparadores de AUT**. El
  **disparador (2)** depende de la **regla general del MÓDULO**, que sigue **ABIERTA** en
  **DUDA-009**: se documenta como **pendiente de DUDA-009**, **no** como regla completa.
- **Regla TM afectada:** §10.5 / B1 (disparadores de AUT) y §10.4 (A Grande / módulo); reconcilia
  **IC-1**; precisa **B5**.
- **Título:** AUT — DOS DISPARADORES (B Grande supera 127 % + 0,25 · A Grande contraria al módulo
  supera el inicio del módulo)

### Pregunta
¿Hay **uno** o **dos** disparadores de AUT? ¿Es contradicción que «B Grande supera 127 % + 0,25»
(H9) y «el movimiento contrario supera el autocorte del módulo» (DEC-007 / ACLARACIÓN 4) coexistan
como reglas de AUT (**IC-1**)?

### Contexto objetivo
- **IC-1** registraba un supuesto «doble disparador» de AUT sin distinguir el **sujeto** de cada uno.
- **B1 / H8 / H9 / DEC-002 / DEC-003** describen el AUT del **disparador (1)** (B Grande supera
  `127 % + 0,25`).
- **DEC-007 / ACLARACIÓN 4** describe un AUT del **disparador (2)** («el movimiento contrario
  supera el autocorte correspondiente al módulo»), cuya regla general del módulo sigue abierta
  (**DUDA-009**).

### Respuesta literal del experto
> "hay DOS disparadores de AUT: (1) cuando B Grande SUPERA 127 % + 0,25 → AUT; (2) cuando A Grande
> va en dirección CONTRARIA al módulo y SUPERA EL INICIO del módulo → AUT y 1."

### Regla general extraída
- **Disparador (1) — AUT por B Grande:** cuando **B Grande SUPERA `127 % + 0,25`** ⇒ **AUT**. Rige
  **B5**: al superarlo, el recorrido **deja de ser B Grande** ⇒ **AUT → nuevo 1** (alias «posible
  1»); **B Grande y AUT no coexisten**.
- **Disparador (2) — AUT por A Grande contra el módulo:** cuando **A Grande** (movimiento contrario
  al módulo) **va en dirección contraria al módulo y SUPERA el INICIO del módulo** ⇒ **AUT** y
  **1** (**nuevo 1**, alias «posible 1»).
- **Reconciliación de IC-1:** los dos disparadores **no** son contradicción porque operan sobre
  **sujetos distintos**: (1) sobre **B Grande**; (2) sobre **A Grande** contra el módulo. **Sí**
  sería contradicción si se pretendiera que (1) y (2) actúan sobre el **mismo objeto sin distinguir
  el sujeto**.
- **Pendiente:** el disparador (2) depende de la **regla general del MÓDULO** (**DUDA-009**,
  abierta). No se cierra como regla completa; queda **pendiente de DUDA-009**.

### Ejemplo y contraejemplo
- **Ejemplo (1):** B Grande **supera** `127 % + 0,25` ⇒ **AUT → nuevo 1**; B Grande deja de ser la
  clasificación vigente de ese recorrido.
- **Ejemplo (2):** A Grande contraria al módulo **supera el inicio del módulo** ⇒ **AUT** y **1**.
- **Contraejemplo:** tratar (1) y (2) como **el mismo disparador** sobre el mismo objeto, o hacer
  **coexistir B Grande y AUT** para el disparador (1) ⇒ **incorrecto** (B5).
- **Contraejemplo:** cerrar el disparador (2) como **regla completa** sin la regla general del
  módulo ⇒ **incorrecto** (DUDA-009 abierta).

### Vocabulario aprobado
`AUT`, `disparador`, `B Grande`, `A Grande`, `módulo`, `inicio del módulo`, `127 % + 0,25`,
`nuevo 1` (alias `posible 1`), `movimiento contrario`.
(**Prohibido** como clasificación: `local`, `superior`, `estructura`, `giro`, `B excesiva`,
`observador`.)

### Tests creados
- **PENDIENTE** de TDD_GUIDE (no los crea RULES_ANALYST; tests no autorizados aún): test rojo de
  los dos disparadores; el del disparador (2) queda condicionado a cerrar **DUDA-009**.

### Registro operativo
- **Archivos modificados:** `DECISIONES_EXPERTO.md` (este registro, DEC-014);
  `DICCIONARIO_TM.md` («Autocorte del módulo» reescrito como disparador (2)).
- **Versión de implementación:** Núcleo `0.0.1-scaffold` (sin cambios de lógica).
- **Regresiones detectadas:** Ninguna (aún no hay implementación de AUT).
- **Estado de la regla:** **CERRADA** para la **existencia de los dos disparadores** y la
  **reconciliación de IC-1**; el **disparador (2)** queda **pendiente de DUDA-009**. **NO** cierra
  el **Gate Cero**; **NO** toca el golden.

---

## DEC-015

- **ID:** DEC-015
- **Fecha y hora:** 2026-10-19 (sesión ECC/OpenCode)
- **Agente que la origina:** RULES_ANALYST / SCENE_QUESTIONER (respuesta literal del experto
  durante la revisión de la vela 3)
- **Estado:** **CERRADA** como criterio metodológico de concurrencia y filtro de ruido. El
  **umbral numérico** entre ruido y movimiento TM sigue **ABIERTO** (§20.5 / PR-g); esta decisión
  no lo fija.
- **Regla TM afectada:** §10.8 / §11 de los dossiers v3 y v4; **H16**; entrada «Lectura 1 /
  lectura 2 / lectura 3» del diccionario.
- **Título:** CONCURRENCIA HABITUAL — 2 LECTURAS NORMALMENTE, 3 EXCEPCIONALMENTE; RUIDO Y
  MICROMOVIMIENTOS NO SE CALCULAN

### Pregunta
¿La coexistencia de dos o tres lecturas es una excepción o la operativa normal? ¿Cómo deben
tratarse el ruido y los micromovimientos?

### Respuesta literal del experto
> "metelo en la documentacion eso ocurre todo el rato normalmente es maximo 2 lecturas alguna vez
> 3 hayq ue quigtar el ruido y las micro movieminto eso no los calculamos usamos la coherenceia
> en moviemintos"

Normalizado: «Mételo en la documentación. Eso ocurre todo el rato: normalmente es máximo 2
lecturas, alguna vez 3. Hay que quitar el ruido y los micromovimientos; eso no lo calculamos.
Usamos la coherencia en movimientos».

### Regla general extraída
- **La concurrencia es habitual.** No es una anomalía ni un caso excepcional: ocurre de forma
  normal en la lectura.
- **Normalmente, máximo 2 lecturas coherentes.** **Excepcionalmente, 3** (`lectura 1` /
  `lectura 2` / `lectura 3`), y solo si las tres siguen siendo **matemáticamente válidas y
  coherentes**. **No hay una cuarta lectura.**
- **Ruido y micromovimientos no se calculan.** No se clasifican, no se convierten en A, B, C,
  AUT, TT ni nuevo 1, y **no ocupan una lectura**. Se descartan.
- **Coherencia de movimientos.** La selección y permanencia de lecturas se decide por la
  coherencia del movimiento completo, no por cada oscilación aislada. No se abre una lectura por
  cada oscilación intravela.
- **Independencia.** Cada lectura conserva su propio módulo, A Grande, B Grande, AUT, TT, nuevo 1
  y nivel de invalidación. **Nunca se mezclan niveles de lecturas distintas.**
- **Ejemplo real (vela 3, 23:41):** coexisten dos TT válidos:
  - TT pequeño: `29187.40`, confirmado en `29188.00` @23:41:22; nuevo 1 de `7.30` puntos
    (`29182.00 → 29189.30`).
  - TT grande: `29189.00`, confirmado en `29189.00` @23:41:30; nuevo 1 de `10.10` puntos
    (`29179.20 → 29189.30`).
  Ambas lecturas se conservan; **no se descarta una por existir la otra**. El máximo común
  `29189.30` es el final de las dos nuevas 1, no un autocorte.
- **Límite:** esta decisión no fija el umbral numérico que separa ruido de movimiento TM; solo
  establece que el ruido y los micromovimientos **no se calculan como lectura**.

### Ejemplo y contraejemplo
- **Ejemplo correcto:** dos TT concurrentes en la misma vela, cada uno con su módulo, A, B, AUT,
  TT y nuevo 1; ambos se mantienen y se resuelven por sus propios niveles.
- **Ejemplo correcto:** descartar una oscilación que no alcanza ninguna referencia matemática TM
  y no asignarle función.
- **Contraejemplo:** descartar el TT pequeño solo porque existe el TT grande, o mezclar sus
  niveles.
- **Contraejemplo:** abrir una lectura nueva por cada micromovimiento o llamar «ruido» a un
  movimiento que sí alcanza referencias TM.

### Vocabulario aprobado
`lectura`, `lectura 1`, `lectura 2`, `lectura 3`, `concurrencia`, `coherencia de movimiento`,
`ruido`, `micromovimiento`, `módulo`, `A Grande`, `B Grande`, `AUT`, `TT`, `nuevo 1`.
(**Prohibido** como clasificación: `local`, `superior`, `estructura`, `giro`, `B excesiva`,
`observador`.)

### Tests creados
- **PENDIENTE** de TDD_GUIDE; tests no autorizados aún. No se crea test hasta que el experto lo
  autorice.

### Registro operativo
- **Archivos modificados:** `DECISIONES_EXPERTO.md` (este registro, DEC-015);
  `REGLAS_CERRADAS.md` (**H16** y §C); `DICCIONARIO_TM.md` («Lectura 1 / lectura 2 / lectura 3»);
  `Dossier_TM_v4_Concurrencia_Reclasificacion.txt` (§2 y §11);
  `Dossier_TM_v3_Lectura_Obligatoria.txt` (nota de actualización);
  `00_LEEME_PRIMERO_PRIORIDAD_DOCUMENTOS_TM.txt` (§D).
- **Versión de implementación:** Núcleo `0.0.1-scaffold` (sin cambios de lógica).
- **Regresiones detectadas:** Ninguna (aún no hay implementación de concurrencia).
- **Estado de la regla:** **CERRADA** para la concurrencia habitual (2 normal / 3 excepcional) y
  para el tratamiento metodológico de ruido y micromovimientos. El **umbral numérico** sigue
  **ABIERTO**. **NO** cierra el **Gate Cero** (sigue abierta la regla general del módulo,
  **DUDA-009**); **NO** toca el golden.
