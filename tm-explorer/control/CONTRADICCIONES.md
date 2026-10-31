# CONTRADICCIONES — Núcleo TM Explorer

Registro de contradicciones entre fuentes y contra hechos objetivos.

**Marca BLOQUEANTE** si la contradicción afecta a: medida de 1 · medida de 2 · posible 3 ·
fallo de 3 · formación del módulo · A Grande · B Grande · AUT · TT · C Grande · CUT ·
concurrencia · reclasificación.

Una contradicción **no** se resuelve aquí por suposición. Se eleva al experto por escenas
y se registra en `DECISIONES_EXPERTO.md`. **No se crea regla nueva a partir del golden.**

## Estado actual (historial conservado)

| Contradicción | Estado | Resolución |
|---|---|---|
| **C1** — C Grande/CUT y final de A Grande (vela 8) | **RESUELTA ✅** | **DEC-011 / H16** (respuesta a DUDA-010): en la **vela 8** el recorrido es **A Grande + B Grande → AUT**; **NO** hay **C Grande** ni **CUT**. **DEC-010/H15** fija el **fin de A Grande = `29.744,40`**. Golden de vela 8 («C Grande → CUT») queda **pendiente de corrección del golden** (NO se toca ahora) |
| **C2** — Unidad del nivel AUT | **RESUELTA ✅** | **DEC-002 / DUDA-002** (extra = 1 tick = 0,25) |
| **C3** — §20.16 vs AUT | **RESUELTA ✅** | **DEC-003 / DUDA-003** (AUT exige superar) |
| **C4** — Vocabulario en concurrencia/reclasificación | **RESUELTA ✅** | **DEC-004 / DUDA-004** (lectura 1/2/3) |
| **C5** — Dos enumeraciones de estados | NO BLOQUEANTE ⚪ | sin cambios |
| **C6** — Gap vs regla de 2 | **RESUELTA ✅** | **DEC-005 / DUDA-005** (gap primero) |
| **C7** — «A Grande acaba cuando supera el módulo» vs hechos | **PARCIAL: fin de A Grande CERRADO ✅ / módulo PARCIAL 🔴** | **DEC-010 / H15** cierra el **fin de A Grande** (extremo `29.744,40`, coherencia entre velas); **DEC-011 / H17** admite **módulo por descarte (vela 7)** y **2 lecturas**; `DUDA-011` CERRADA → **DEC-012** (lectura 2: «se pasa» = supera 127 % + 0,25 → AUT → nuevo 1); la **regla general del módulo** sigue **PARCIAL**, pendiente → **DUDA-009** |
| **C8 / C1b** — ¿CUT en la vela 8? (subcuestión de C1) | **RESUELTA ✅** | **DEC-011** (respuesta a DUDA-010): el **CUT no ocurre en la vela 8**; la vela 8 es **A Grande + B Grande → AUT** |
| **C9** — Definición de FT incompleta (ex C7) | NO BLOQUEANTE ⚪ | sin cambios |
| **C10** — Notas de consistencia documental (ex C8) | NO BLOQUEANTE ⚪ | sin cambios |

> **Nota de renumeración (RULES_ANALYST, 2026-10-18):** las contradicciones **C7** y **C8**
> anteriores (FT incompleta y notas de consistencia documental, ambas NO BLOQUEANTE) pasan a
> **C9** y **C10** para liberar los identificadores **C7** (nueva, BLOQUEANTE) y **C8 / C1b**
> (subcuestión de C1) pedidos por la orquestación. Se conserva su contenido íntegro; solo cambia
> la etiqueta. Requiere confirmación humana.

Las secciones C2, C3, C4 y C6 **se conservan íntegras** (historial); solo se marcan como
resueltas con su referencia `DEC`/`DUDA`.

> **NOTA DE CONTROL — DUDA-008 (salida en plano) RESUELTA por DEC-009.** La tolerancia de la
> **salida en plano** (registrada como **DUDA-008**, fila ligada a C1) queda **CERRADA** por
> **DEC-009**: **plano** si `|cierre del movimiento anterior − apertura de la vela siguiente| ≤ 1
> tick TM = 0,25 puntos`; si es **> 1 tick** es **gap** (con gap no se aplica la regla de 2, H11).
> Umbral **`plano_max_points = 0.25`**, **fijo**, no derivado del CSV ni del delta −0,80.
> Trasladada a `REGLAS_CERRADAS.md` **H14**; PR-p retirada en `REGLAS_PROVISIONALES.md`.
> **Esta nota NO resuelve C1:** C1 (C Grande/CUT, vela 8) **sigue BLOQUEANTE ABIERTA**. No mueve
> eventos de vela ni toca el golden.

---

## C1 — Tolerancia a la contradicción: RESUELTA ✅ por DEC-011 (CUT · C Grande)

**Regla afectada:** CUT (C Grande alcanza el final de A Grande dentro de la referencia);
prompt v2 §10.7, dossier §6.2, H1/H3.

**Contradicción objetiva (hecho verificado):** la lectura profesional exige **CUT dentro de
la vela 8**, pero los ticks **no** permiten que C Grande alcance el final de A Grande
(≈ 29.738,40) hasta mucho después.

**Datos objetivos del caso (solo para documentar la contradicción; el motor NO los usa):**

| Hecho | Valor |
|---|---|
| Final de A Grande (referencia de CUT) | ≈ 29.738,40 |
| Vela 8 (precio bid) — máximo | 29.744,40 (~10 s desde el inicio de la vela) |
| Vela 8 (precio bid) — mínimo | 29.683,20 |
| Vela 8 (precio bid) — cierre | 29.689,10 |
| Retorno alcista posterior dentro de la vela 8 | **ninguno** |
| Primer tick que alcanza ≈ 29.738,40 | vela 16 |

**Por qué es bloqueante:** si CUT solo se confirma cuando C Grande alcanza el final de A
Grande, y ese nivel no se alcanza dentro de la vela 8, entonces el golden de la vela 8
(C Grande → CUT en la misma vela) **no es reproducible** con las reglas cerradas sobre los
ticks disponibles.

**Instrucción de registro (anti-spoiler):**
- NO es una regla nueva.
- NO se mueve el evento a otra vela.
- La vela 8 del golden queda marcada **PENDIENTE / inconsistente con ticks** hasta que
  Javier resuelva por escena.
- No bloquear el resto del Bloque 1–2; **sí** bloquea el cierre de C Grande/CUT.

**Pregunta pendiente para Javier:** ¿C Grande puede confirmar CUT con una referencia distinta
del final de A Grande, o el evento CUT de la vela 8 es un error de vela en la lectura
profesional? (Formular por escenas, no como "¿hay CUT en la vela 8?").

> **ESTADO: ABIERTA (BLOQUEANTE).** Reescrita como **DUDA-001** por SCENE_QUESTIONER
> (`PREGUNTAS_PENDIENTES.md`). **Sin respuesta** de Javier. **No** la cierra ninguna de las
> decisiones DEC-002…DEC-005. Bloquea el cierre de C Grande/CUT.
>
> **Subcuestión añadida — C8 / C1b (DUDA-006):** confirmar que el CUT **no** ocurre en la vela 8.
> C1 **permanece abierta**; la subcuestión se detalla en la sección **C8 / C1b**.
>
> **ACTUALIZACIÓN — DEC-010 / H15 (RULES_ANALYST): PENDIENTE DE CONFIRMACIÓN.** El experto fija el
> **fin de A Grande = `29.744,40`** (coherencia entre velas) y describe la vela 8 como
> **A Grande + B Grande → AUT** («casi seguro hizo A, B, AUT»), **sin mencionar C Grande**. Por
> tanto, para la vela 8 la lectura apunta a **A Grande (extremo `29.744,40`) + B Grande → AUT** y
> **NO C Grande / CUT**. **C1 NO se cierra todavía:** queda **PENDIENTE DE CONFIRMACIÓN** explícita
> del experto mediante **DUDA-010** (`PREGUNTAS_PENDIENTES.md`). La parte «y creo hace TT en esa
> vela» de DEC-010 queda **TENTATIVA**. **No** se mueve el evento de vela ni se toca el golden.
>
> **RESOLUCIÓN — DEC-011 / H16 (RULES_ANALYST, 2026-10-18): C1 RESUELTA ✅.** Por **regla del
> experto** (respuesta a **DUDA-010**), en la **vela 8** el recorrido es **A Grande + B Grande →
> AUT**; **NO hay C Grande ni CUT en la vela 8**. El experto además admite **2 lecturas
> concurrentes** (`lectura 1` / `lectura 2`), con la **vela 7 como módulo por descarte** y la
> **vela 8 = A, B, AUT** (lectura 1). **NOTA (golden):** la entrada del golden que afirmaba
> **«C Grande → CUT en vela 8» queda PENDIENTE DE CORRECCIÓN DEL GOLDEN**; **NO** se toca el golden
> ahora. **NO** se mueve **CUT** de vela en el motor. Con esto **C1 se cierra** (queda solo el
> registro documental de la corrección del golden).

---

## C2 — Unidad del nivel AUT: puntos vs tick vs 0,025: RESUELTA ✅ por DEC-002 (AUT)

**Regla afectada:** nivel de AUT (B1). Fuentes:
- prompt v2 §10.5: "127 % + **0,25 puntos**";
- dossier v3 §5.2: "100 % a 127 % + **0,25 tick**";
- histórico `v3.0/v3.2`: **0,025**; adenda v4 y `REGLAS_CERRADAS` B1: **0,25**.

**Contradicción:** el valor `0,025` vs `0,25` está cerrado en B1 (gana `0,25`). Persiste la
unidad: "puntos" (prompt v2, B1) vs "tick" (dossier). Con 1 tick = 0,25 puntos en el
instrumento de la muestra, "0,25 tick" y "0,25 puntos" **no** coinciden.

**Marca:** BLOQUEANTE (AUT) hasta fijar unidad de forma general (no dependiente del símbolo).

**Pendiente (histórico):** confirmar si el extra es `+0,25` **puntos** o `+1 tick`. Registrar
como regla general en unidades del instrumento.

> **RESOLUCIÓN — DEC-002 / DUDA-002 (cerrada por Javier).** El extra del nivel AUT es
> **1 tick = 0,25 puntos**. Regla general: `Nivel AUT = B Grande en 1,27 × A Grande + 0,25
> (1 tick)`. Trasladada a `REGLAS_CERRADAS.md` B1 y H8. El valor histórico `0,025` queda
> anulado.

---

## C3 — Hipótesis del nivel AUT (§20.16) vs regla cerrada §10.5: RESUELTA ✅ por DEC-003 (AUT · C Grande · CUT)

**Regla afectada:** AUT y su relación con C Grande/CUT.

- **Cerrado (prompt v2 §10.5 / B1 / adenda v4 §1):** AUT se activa cuando B Grande alcanza
  **127 % + 0,25**, inmediato.
- **Hipótesis (dossier v3 §20.16, explícitamente "NO ES REGLA"):** AUT aparece solo cuando B
  **se pasa** de la franja; un B que solo toca el 127 % y vuelve continuaría como C → CUT
  **sin AUT**.

**Contradicción:** dos comportamientos de AUT ante "tocar 127 % y volver".

**Marca:** BLOQUEANTE (AUT/C Grande/CUT) según el criterio. Matiz: la hipótesis §20.16 está
declarada como no-regla, por lo que la fuente cerrada (§10.5) tiene prioridad; se puede
neutralizar con confirmación explícita de Javier.

**Pendiente (histórico):** confirmar si "tocar 127 % + 0,25 y volver" activa AUT o permite
C → CUT.

> **RESOLUCIÓN — DEC-003 / DUDA-003 (cerrada por Javier).** AUT solo se confirma cuando
> B Grande **SUPERA** 127 % + 0,25. Si B Grande solo **toca** el nivel y vuelve, **no** hay
> AUT: ese movimiento es **B Grande** y el que sube después es **C Grande**. La hipótesis
> §20.16 (declarada no-regla) queda neutralizada. Trasladada a `REGLAS_CERRADAS.md` B1, B3,
> H7 y H9.

---

## C4 — Vocabulario prohibido en dossiers secundarios: RESUELTA ✅ por DEC-004 (concurrencia · reclasificación)

**Regla afectada:** concurrencia y reclasificación; vocabulario (D).

- Prompt v2 §5 (motor) y §1.7 (dossier v3) **prohíben** como clasificación:
  `local`, `superior`, `estructura`, `giro`, `B excesiva`, `observador`.
- La **adenda v4 §2** usa la etiqueta "lectura `local`".
- El **dossier v2.1 §5.5 / v2.3 §5.5.1, §16.6** usan "lectura `superior`" y "modulo
  `superior`".

**Contradicción:** los dossiers emplean términos que su propia capa funcional prohíbe.

**Marca:** BLOQUEANTE (concurrencia / reclasificación) para la capa funcional: no puede
usarse ese vocabulario en estados, eventos, golden ni documentación funcional.

**Pendiente (histórico):** fijar el vocabulario TM autorizado para la segunda/tercera lectura
(p. ej. "lectura alternativa") y para la referencia de módulo de mayor alcance, sin usar los
términos prohibidos.

> **RESOLUCIÓN — DEC-004 / DUDA-004 (cerrada por Javier).** Las lecturas concurrentes se
> nombran **lectura 1 / lectura 2 / lectura 3** (numeración fuera de la terminología TM,
> solo identificador). Sustituye a «local» / «superior» en la capa funcional. Trasladada a
> `REGLAS_CERRADAS.md` C, D y H10.

---

## C5 — Dos enumeraciones de estados: NO BLOQUEANTE ⚪ (reclasificación)

- Dossier v3 §1.6: `CONFIRMADO, PENDIENTE, NO EXISTE, FALLIDO, SIN REGLA ESCRITA`.
- Adenda v4 §4 / `REGLAS_CERRADAS` F: `CANDIDATA, ACTIVA, CONFIRMADA, PENDIENTE,
  RECLASIFICADA, INTEGRADA, INVALIDADA, FINALIZADA`.
- Dossier v2.3 §6.4 D: estado de B = `NO EXISTE, PENDIENTE, CONFIRMADO`.

**Naturaleza:** no es contradicción, son **ámbitos distintos** (clasificación TM vs ciclo de
vida de una lectura vs estado de B). Se documenta para que el motor no las confunda.

**Marca:** NO BLOQUEANTE.

---

## C6 — Prioridad entre la regla de 2 y los gaps (§9.3 vs §4.2): RESUELTA ✅ por DEC-005 (módulo · 2 · 3)

**Regla afectada:** formación del módulo, 2 y 3.

- §4.2: si falla cualquier condición de 2, 1 pasa a módulo y el movimiento contrario es A Grande.
- §9.1: un gap a favor de 1 contiene A y B implícitas.
- §9.3 propone evaluar **primero** el gap y aplicar §4.2 solo cuando no hay gap.

**Estado:** el propio dossier marca §9.3 como **"PROPUESTA, PENDIENTE DE CONFIRMAR"**.

**Marca:** BLOQUEANTE (formación del módulo / 2 / 3) hasta confirmación.

**Pendiente (histórico):** confirmar el orden gap ↔ regla de 2 (corresponde a §20.13; ver
`REGLAS_PROVISIONALES.md` PR-k).

> **RESOLUCIÓN — DEC-005 / DUDA-005 (cerrada por Javier).** Al abrir una vela nueva se evalúa
> **primero el gap**; si hay gap **no** se aplica la regla de 2. Trasladada a
> `REGLAS_CERRADAS.md` A4 y H11. La propuesta §9.3 queda confirmada.

---

## C7 — «A Grande acaba cuando supera el módulo» contradice los hechos: PARCIAL — fin de A Grande CERRADO ✅ / módulo PARCIAL 🔴 (A Grande · módulo)

**Regla afectada:** final de A Grande y su relación con el módulo. Fuente: la **respuesta ambigua
del experto registrada como DEC-006** (por SCENE_QUESTIONER; literal aún sin volcar a
`DECISIONES_EXPERTO.md`).

**Afirmación del experto (DEC-006):** «A Grande acaba cuando **supera el módulo**» (A Grande =
movimiento contrario al módulo).

**Contradicción objetiva (hecho verificado; solo para documentar la contradicción, el motor NO
los usa):**

| Hecho | Valor |
|---|---|
| Final de A Grande (máximo de A Grande) | 29820,80 |
| Máximo del módulo (velas 1+2) | 29838,20 |
| ¿A Grande supera el módulo? | **NO** (29820,80 < 29838,20) |

**Por qué es relevante (no bloqueante):** si A Grande solo acabara al **superar el módulo**, A
Grande no habría terminado en su máximo (29820,80), que queda **por debajo** del máximo del módulo
(29838,20). La afirmación choca con el recorrido de ticks y condiciona el final de A Grande, que es
referencia de CUT. Permanece **PROVISIONAL** a la espera de **DUDA-009**.

**Instrucción de registro (anti-spoiler):**
- NO es una regla nueva; no se cierra.
- NO se mueve ningún evento a otra vela.
- NO se resuelve mirando el golden.

**Pregunta pendiente para Javier (DUDA-009; relacionada con DUDA-007):** ¿A Grande acaba al
**superar el módulo** o al **crear su propio extremo**, con independencia del máximo del módulo?

**ESTADO: PARCIAL.** Sin cierre total. La aclaración **DEC-007 (ACLARACIÓN 4)** fija la redacción
provisional (A Grande = movimiento contrario al módulo; AUT al superar el autocorte; nuevo 1 (alias
«posible 1») tras AUT). Configuración actual de C7:

- **Parte «fin de A Grande» — CERRADA ✅ por DEC-010 / H15.** El fin de A Grande es el **extremo del
  movimiento** actualizado por **coherencia entre velas**: en la muestra **`29.744,40`**, **no**
  `29.738,40`; **no** se cierra en el primer máximo si la vela siguiente lo extiende (§10.4).
  Trasladada a `REGLAS_CERRADAS.md` **H15**. La afirmación «A Grande acaba cuando supera el módulo»
  queda **superada** para el fin de A Grande.
- **Parte «qué módulo usa la lectura» — PARCIAL 🔴 (actualizada por DEC-011 / H17 y DEC-012).** El
  experto (**DEC-011**) **admite** dos cosas: (1) puede haber **2 interpretaciones concurrentes**
  (`lectura 1` / `lectura 2`) que **se resuelven más adelante** y a las que hay que **atender**
  (→ **H16**, CERRADA); y (2) cuando **no hay módulo claro**, puede tomarse la **vela anterior**
  (p. ej. **vela 7**) como **módulo por descarte**, con su **A Grande contraria** (→ **H17**,
  **PROVISIONAL**, **no cerrada**). La **lectura 2** queda aclarada por **DEC-012** («se pasa» = B
  supera 127 % + 0,25 → **AUT → nuevo 1**; cierra **DUDA-011**). **La regla general del módulo sigue
  PARCIAL** y es **el único punto abierto de C7**: queda pendiente **DUDA-009**
  (`PREGUNTAS_PENDIENTES.md`) — **¿el módulo es siempre de 2 velas o puede ser de una sola vela /
  vela anterior por descarte?** — y qué significa «superar el autocorte correspondiente al módulo».
  Marcada **PROVISIONAL** en `REGLAS_PROVISIONALES.md` **PR-o**.
- La parte **«y creo hace TT en esa vela»** de DEC-010 queda **TENTATIVA** (no cerrada).

**NO** se cierra C7 en su totalidad (sigue **PARCIAL**); **NO** se toca el golden ni se mueve ningún
evento de vela.

---

## C8 / C1b — Subcuestión de C1: confirmar que el CUT NO ocurre en la vela 8: RESUELTA ✅ por DEC-011 (C Grande · CUT)

**Regla afectada:** CUT (C Grande alcanza el final de A Grande); prompt v2 §10.7, dossier §6.2.

**Enunciado:** subcuestión añadida a **C1**, que **permanece abierta y BLOQUEANTE** (no la
sustituye). Se pide a Javier **confirmar explícitamente** que el **CUT no ocurre en la vela 8**
(el retorno de C Grande hasta el final de A Grande no se da dentro de la vela 8).

**Hechos que la sostienen:** tras el máximo de la vela 8 (29744,40) el primer tick ≥ 29738,40
posterior aparece en la **vela 16**. No existe retorno alcista dentro de la vela 8 ⇒ ninguna
C Grande puede confirmar CUT dentro de la vela 8.

**Instrucción:** mantener **C1 abierta**; NO cerrar C Grande/CUT; NO mover el evento; NO usar el
golden.

**Pregunta pendiente para Javier (DUDA-006):** ¿se confirma que el CUT **no** se produce dentro de
la vela 8?

**ESTADO: RESUELTA ✅ por DEC-011.** El experto confirma (respuesta a **DUDA-010**) que en la
**vela 8** el recorrido es **A Grande + B Grande → AUT** y que **NO** hay **C Grande** ni **CUT**
en esa vela. Queda **cerrada** la subcuestión: **el CUT NO ocurre en la vela 8**. La entrada del
golden que afirmaba «C Grande → CUT en vela 8» queda **pendiente de corrección del golden** (NO se
toca el golden ahora); **NO** se mueve **CUT** de vela.

---

## C9 — Definición de FT incompleta (ex C7): NO BLOQUEANTE ⚪ (FT)

**Regla afectada:** FT (§8.4 / §20.4). Falta referencia exacta, desplazamiento mínimo, caída
de velocidad y caso TT+FT en la misma vela.

**Marca:** NO BLOQUEANTE para los bloques 1–3: FT no forma parte del primer objetivo de
validación (1 → … → CUT). Pasa a PROVISIONAL (`REGLAS_PROVISIONALES.md` P6).

---

## C10 — Notas de consistencia documental (ex C8, NO BLOQUEANTE ⚪)

- El archivo `Dossier_TM_v4_Concurrencia_Reclasificacion.txt` declara internamente
  "VERSION: 2.0" y cierra como "FIN DEL DOSSIER TM v2.0", aunque el nombre de archivo diga
  v4. Es un dossier v2.0 + "ADENDA v4". No afecta a reglas; solo a trazabilidad.
- El prompt v2 resume §10.2 sin las 4 condiciones de 2 (§4.2: dirección, rango, salida en
  plano, cola de base). No es contradicción; se completó en `REGLAS_CERRADAS.md` A1.
- El orden por tick de la adenda v4 §5 (10 pasos) y el del prompt v2 §12 (20 pasos) son
  compatibles (detalle de implementación), no contradictorios.
