# PREGUNTAS PENDIENTES — SCENE_QUESTIONER (Gate Cero, segunda oleada)

Dudas reales convertidas a **ESCENAS** para el experto Javier, con la estructura exacta del
**§7** (`Prompt_ECC_OpenCode_TM_..._v2.txt`).

- **Agente que mantiene este archivo:** SCENE_QUESTIONER.
- **Base:** `CONTRADICCIONES.md` (C1, C2, C3, C4, C6), `CRONOLOGIA_MOVIMIENTOS.md`,
  `AUDITORIA_DATOS.md`, `REGLAS_CERRADAS.md`, `REGLAS_PROVISIONALES.md`, `DICCIONARIO_TM.md`,
  `tests/golden/golden_estados_velas_1_8.json`, `GOLDEN_EXPLICADO.md`.
- **Método:** cada duda se pregunta **una cada vez**, salvo las que dependen de la misma regla
  (agrupadas). Se describe **primero el recorrido real de ticks** y **después** la clasificación
  posible (§8). No se pregunta lo ya respondido (p. ej. tolerancia de salida en plano = 1 tick,
  **DEC-001**). Ninguna clasificación no confirmada se presenta como hecho.
- **Serie de precio de los hechos:** **Bid** (`AUDITORIA_DATOS.md` §3).
- **Anti-spoiler:** este documento es de consulta; el núcleo productivo no lo lee.
- **Vocabulario:** `1 · 2 · 3 · módulo · A Grande · B Grande · C Grande · AUT · TT · CUT · FT ·
  movimiento contrario · retroceso · salida en plano · gap · lectura · candidata / confirmada /
  reclasificada / integrada / invalidada / finalizada`. Prohibido: `local · superior ·
  estructura · giro · B excesiva · observador`.

**Resumen:** 11 dudas (`DUDA-001` … `DUDA-011`). `DUDA-001` **PARCIALMENTE RESPONDIDA**
(**DEC-006**) y **REFORMULADA (ver ACLARACIÓN 3)**; derivó en `DUDA-006` y `DUDA-007`.
`DUDA-002` … `DUDA-005` **CERRADAS** (respuestas del experto registradas en `DECISIONES_EXPERTO.md`
**DEC-002 … DEC-005**). `DUDA-008` (salida en plano) **CERRADA → `DEC-009`**; `DUDA-009`
(A Grande / módulo) **PARCIALMENTE RESPONDIDA → `DEC-010`** (A Grande sí; **módulo general sigue
abierto**); **`DUDA-010`** (confirmar vela 8 = A Grande + B Grande → AUT, sin C Grande/CUT)
**CERRADA → `DEC-011`** (cierra **C1**). **`DUDA-011`** (sentido de «se pasa» en la **lectura 2**)
**CERRADA → `DEC-012`** («se pasa» = B supera 127 % + 0,25 → **AUT → nuevo 1**). Aclaraciones de
AUT / B Grande / A Grande / salida en plano registradas en `DECISIONES_EXPERTO.md` **DEC-007**,
**DEC-010**, **DEC-011** y **DEC-012** (y `REGLAS_PROVISIONALES.md` PR-m/PR-n). **Única duda viva:**
la parte **módulo general** de `DUDA-009`.

---

## ESTADO DEL GATE CERO

- **Estado:** **ABIERTO**.
- **Abierta (única):** la parte **módulo general** de `DUDA-009` — **¿el módulo es siempre de 2
  velas o puede ser de una sola vela / vela anterior por descarte?** (regla general del módulo).
- **Cierres recientes:** **`DUDA-011` CERRADA → `DEC-012`** («se pasa» = B supera 127 % + 0,25 →
  **AUT → nuevo 1** en la lectura 2). **`DUDA-010` CERRADA → `DEC-011`** (cierra **C1**: vela 8 =
  A Grande + B Grande → AUT, sin C Grande/CUT). **`DUDA-008` CERRADA → `DEC-009`**; **`DUDA-009`
  parcialmente respondida → `DEC-010`** (A Grande sí, módulo no).
- **Prohibido hasta cerrar el Gate Cero:** **NO lanzar CORE_TM_ENGINEER**; **NO modificar el
  golden**; **NO mover CUT de vela**.

---

## Índice

| ID | Contradicción | Regla afectada | Estado |
|---|---|---|---|
| DUDA-001 | C1 — C Grande/CUT y final de A Grande (vela 8) | §10.7 / §10.4 | PARCIALMENTE RESPONDIDA (DEC-006) |
| DUDA-002 | C2 — unidad del nivel AUT | §10.5 / B1 | CERRADA → DEC-002 |
| DUDA-003 | C3 — "tocar 127 % y volver" → AUT o C → CUT | §10.5 vs §20.16 | CERRADA → DEC-003 |
| DUDA-004 | C4 — vocabulario TM en concurrencia/reclasificación | §10.8 / D | CERRADA → DEC-004 |
| DUDA-005 | C6 — prioridad gap ↔ regla de 2 | §9.3 / §4.2 | CERRADA → DEC-005 |
| DUDA-006 | C1 — CUT: ¿vela 8 o cuando C Grande alcance el final de A Grande? | §10.7 / CUT | CERRADA → DEC-011 (CUT no en vela 8) |
| DUDA-007 | C1 — "A Grande acaba cuando supera el módulo" (definición) | §10.4 / final de A Grande | BLOQUEANTE (nueva) |
| DUDA-008 | C1 — tolerancia de la salida en plano (usada en la muestra) | salida en plano | CERRADA → DEC-009 |
| DUDA-009 | C1 — "A Grande = movimiento contrario al módulo" + nuevo 1 (módulo general ABIERTO) | §10.4 / A Grande | PARCIALMENTE RESPONDIDA (DEC-010): A Grande sí, módulo general no |
| DUDA-010 | C1 — confirmar vela 8 = A Grande + B Grande → AUT (sin C Grande/CUT) | §10.4 / §10.7 | CERRADA → DEC-011 (cierra C1) |
| DUDA-011 | C1 / lectura 2 — sentido de «se pasa» en el retroceso final vela 7 / inicio vela 8 | §10.4 / §10.5 | CERRADA → DEC-012 («se pasa» = B supera 127 % + 0,25 → AUT → nuevo 1) |

---

## DUDA-001

**ID DE DUDA:** DUDA-001 (origen C1)
**AGENTE QUE LA ORIGINA:** SCENE_QUESTIONER
**ESTADO:** **PARCIALMENTE RESPONDIDA (DEC-006)** y **REFORMULADA (ver ACLARACIÓN 3)** — el
experto respondió, pero la interpretación queda **PROVISIONAL** (ambigua). Derivó en `DUDA-006` y
`DUDA-007` (ambas **BLOQUEANTES**).
**REGLA AFECTADA:** §10.7 (C Grande y CUT) y §10.4 (final de A Grande).

> **REFORMULACIÓN (ACLARACIÓN 3):** primero entregar **LECTURA 1/2/3 con niveles y ticks**; **no
> usar C Grande ni CUT como conclusión**; plantear **una sola pregunta conceptual**.

> Reformulada de forma más simple y en vocabulario TM a petición del experto
> («la duda 1 … hazle de nuevo de forma mas simple con tm vocabulario»).
> Sin muros de números: solo el recorrido en TM y dos escenas.

### HECHOS OBJETIVOS
- **(1)** Un **posible 1** bajista termina en un **mínimo**.
- **(2)** Después, un **movimiento contrario** alcista crea un **máximo** (**A Grande**).
- **(3)** En la **vela siguiente** el precio sube un poco más (**nuevo extremo**) y después **baja
  fuerte** (**B Grande**).
- **(4)** Después, un **movimiento contrario** alcista (**C Grande candidata**).

### LO QUE SABEMOS POR TM
- **Regla 1 (§10.7):** C Grande solo puede aparecer después de B Grande; el movimiento contrario
  tras B Grande comienza como C Grande candidata; si B Grande crea un nuevo extremo, la C Grande
  candidata se cancela; **CUT se confirma cuando C Grande alcanza el final de A Grande**.
- **Regla 2 (§10.4):** A Grande puede continuar durante varias velas; si A Grande crea un nuevo
  extremo, la B Grande candidata se cancela.

### LO QUE NO SABEMOS
- Cuál es el **final de A Grande** (referencia de CUT) en este recorrido: el **primer máximo** o el
  **máximo más alto** (nuevo extremo de la vela siguiente).
- Y, en consecuencia, si con este recorrido se confirma **C Grande → CUT** o **B Grande → AUT** con
  la **C Grande candidata cancelada**.

### ESCENAS POSIBLES

**ESCENA A**
- **Secuencia de movimientos:** el **nuevo extremo** de la vela siguiente **extiende A Grande**;
  **final de A Grande = el máximo más alto**; desde ahí baja fuerte = **B Grande**.
- **Clasificación TM posible:** A Grande termina en el máximo más alto; B Grande desde ese máximo.
- **Eventos que produciría:** B Grande (y, si corresponde, AUT); C Grande candidata desde el
  contrario alcista posterior.
- **Condición que la confirmaría:** que el nuevo extremo se lea como extensión de A Grande.
- **Condición que la cancelaría:** que B Grande empiece ya en el primer máximo (ESCENA B).

**ESCENA B**
- **Secuencia de movimientos:** **B Grande ya desde el primer máximo**; el nuevo extremo de la vela
  siguiente no alarga A Grande.
- **Clasificación TM posible:** final de A Grande = el primer máximo; B Grande medida desde ahí.
- **Eventos que produciría:** B Grande (y, si corresponde, AUT); C Grande candidata desde el
  contrario alcista posterior.
- **Condición que la confirmaría:** que B Grande empiece en el primer máximo.
- **Condición que la cancelaría:** que el nuevo extremo se lea como extensión de A Grande (ESCENA A).

### PREGUNTA CONCRETA A JAVIER
- ¿Cuál es el **final de A Grande** (referencia de CUT) y, con este recorrido, se confirma
  **C Grande → CUT** o **B Grande → AUT** con la **C Grande candidata cancelada**?

### EFECTO DE LA RESPUESTA
- **Regla que se podrá cerrar:** referencia de CUT (final de A Grande) y desenlace del recorrido
  (C Grande → CUT frente a B Grande → AUT con C Grande candidata cancelada).
- **Tests afectados:** test de C Grande / CUT en `tests/rules.closed.red.test.js` (lo creará
  TDD_GUIDE); golden vela 8 (`C_CANDIDATA`, `CUT`, hoy PENDIENTE).
- **Bloque de implementación desbloqueado:** **Bloque 3** (C Grande candidata, cancelación de
  C Grande candidata, CUT).

---

## DUDA-002

**ID DE DUDA:** DUDA-002 (origen C2)
**AGENTE QUE LA ORIGINA:** SCENE_QUESTIONER (unidad detectada por RULES_ANALYST)
**ESTADO:** CERRADA → `DECISIONES_EXPERTO.md` **DEC-002** (respuesta del experto; extra de AUT = 1 tick = 0,25 puntos).
**REGLA AFECTADA:** §10.5 / B1 — nivel de AUT (unidad de medida: puntos vs tick).

### HECHOS OBJETIVOS
- **Timestamp inicial:** 16:35:35.448 (vela 6, primer nivel de AUT de la muestra alcanzado).
- **Timestamp final:** 16:37:55.363 (vela 8, nivel de AUT candidato de R-D alcanzado).
- **Vela o velas:** 6 y 8.
- **Apertura:** vela 6 = 29766,40; vela 8 = 29734,80 @16:37:00.038.
- **Extremos en orden temporal:** vela 6 → MÁXIMO 29780,30 @16:35:16.001, después MÍNIMO 29717,60
  @16:35:57.701; vela 8 → MÁXIMO 29744,40 @16:37:10.254, después MÍNIMO 29683,20 @16:37:59.175.
- **Precio final:** 29689,10 @16:37:59.977 (cierre vela 8).
- **Serie de precio usada:** Bid.
- **Movimientos reconstruidos:** R-A: A Grande = 60,50 pts; B Grande alcanza el 100 % y el nivel
  127 % + 0,25 en **29743,715** @16:35:35.448 (29820,80 − 1,27·60,50 − 0,25). R-D candidata:
  A Grande = 32,00 pts; nivel **29703,51** @16:37:55.363 (29744,40 − 1,27·32,00 − 0,25).
- **Lecturas activas antes de la duda:** R-A (módulo rango 77,90; A Grande 29820,80; B Grande en
  curso, AUT/TT alcanzados en vela 6); R-D (B Grande candidata).

### LO QUE SABEMOS POR TM
- **Regla 1 (§10.5 / B1):** AUT se confirma **inmediatamente** cuando B Grande alcanza
  **127 % + 0,25**.
- **Regla 2 (B1):** el valor histórico `0,025` quedó cerrado a favor de `0,25`; no existe
  `B excesiva` por superar ese nivel.

### LO QUE NO SABEMOS
- Punto exacto no resuelto: la **unidad** del extra `0,25` — ¿**0,25 puntos** del instrumento
  (prompt v2 §10.5 / B1) o **0,25 tick** (dossier v3 §5.2)? Con 1 tick = 0,25 puntos en el
  instrumento de la muestra, «0,25 puntos» y «0,25 tick» **no** coinciden.

### ESCENAS POSIBLES

**ESCENA A**
- **Secuencia de movimientos:** B Grande alcanza **127 % + 0,25 puntos** del instrumento.
- **Clasificación TM posible:** AUT inmediato con el extra medido en **puntos**.
- **Eventos que produciría:** AUT en el nivel `127 % + 0,25 puntos`.
- **Condición que la confirmaría:** que el nivel resultante coincida con el tick real del AUT.
- **Condición que la cancelaría:** que el nivel calculado no corresponda al tick del AUT observado.

**ESCENA B**
- **Secuencia de movimientos:** B Grande alcanza **127 % + 0,25 tick** del instrumento
  (0,0625 puntos en esta muestra).
- **Clasificación TM posible:** AUT inmediato con el extra medido en **ticks**.
- **Eventos que produciría:** AUT en el nivel `127 % + 0,25 tick`.
- **Condición que la confirmaría:** que el nivel desplazado coincida con el tick real del AUT.
- **Condición que la cancelaría:** que el nivel cambie el tick del AUT respecto a los hechos.

### PREGUNTA CONCRETA A JAVIER
- ¿El extra del nivel de AUT es **+0,25 puntos** del instrumento (equivalente a 1 tick en esta
  muestra) o **+0,25 tick** del instrumento (0,0625 puntos en esta muestra)? ¿Cómo se expresa la
  regla general en unidades del instrumento, sin depender del símbolo?

### EFECTO DE LA RESPUESTA
- **Regla que se podrá cerrar:** B1 / §10.5, con la unidad del nivel de AUT fijada en unidades del
  instrumento.
- **Tests afectados:** test del nivel de AUT (velas 6 y 8); cálculo de AUT en el núcleo.
- **Bloque de implementación desbloqueado:** **Bloque 2** (AUT / TT).

---

## DUDA-003

**ID DE DUDA:** DUDA-003 (origen C3)
**AGENTE QUE LA ORIGINA:** SCENE_QUESTIONER (contradicción §10.5 vs hipótesis §20.16, RULES_ANALYST)
**ESTADO:** CERRADA → `DECISIONES_EXPERTO.md` **DEC-003** (respuesta del experto: AUT solo al superar 127 % + 0,25; tocar y volver = B Grande + C Grande, sin AUT).
**REGLA AFECTADA:** §10.5 (AUT inmediato) frente a la hipótesis §20.16 («tocar 127 % y volver →
C → CUT sin AUT», declarada **no-regla**).

### HECHOS OBJETIVOS
- **Timestamp inicial:** 16:35:33.046 (vela 6, B Grande cruza el 100 % de A Grande).
- **Timestamp final:** 16:37:55.363 (vela 8, nivel de AUT candidato de R-D alcanzado).
- **Vela o velas:** 6 y 8.
- **Apertura:** vela 6 = 29766,40; vela 8 = 29734,80 @16:37:00.038.
- **Extremos en orden temporal:** vela 6 → MÁXIMO 29780,30 @16:35:16.001, después MÍNIMO 29717,60
  @16:35:57.701; vela 8 → MÁXIMO 29744,40 @16:37:10.254, después MÍNIMO 29683,20 @16:37:59.175.
- **Precio final:** 29689,10 @16:37:59.977 (cierre vela 8).
- **Serie de precio usada:** Bid.
- **Movimientos reconstruidos:** vela 6 → B Grande cruza el 100 % (29760,30) a 16:35:33.046 y alcanza
  127 % + 0,25 (29743,715) a 16:35:35.448; el movimiento **continúa bajando** (no vuelve de
  inmediato). Vela 8 → B Grande candidata cruza el 100 % (29712,40) a 16:37:35.310 y el nivel de AUT
  (29703,51) a 16:37:55.363; **continúa** hasta 29683,20 (por debajo del nivel), sin retorno alcista.
- **Lecturas activas antes de la duda:** R-A (con TT confirmado), R-B (posible 1), R-D (B Grande
  candidata).

### LO QUE SABEMOS POR TM
- **Regla 1 (§10.5):** AUT es **inmediato** al alcanzar 127 % + 0,25; AUT **no** confirma
  definitivamente un nuevo 1; no existe `B excesiva`.
- **Regla 2 (§10.6):** AUT activa **TT**.

### LO QUE NO SABEMOS
- Punto exacto no resuelto: si cuando B Grande **toca** el 127 % + 0,25 **y vuelve** (sin continuar)
  se activa **AUT** igualmente (regla cerrada), o si permite un desenlace **C Grande → CUT sin AUT**
  (hipótesis §20.16).

### ESCENAS POSIBLES

**ESCENA A**
- **Secuencia de movimientos:** B Grande toca el 127 % + 0,25 **y vuelve** → en ese tick se activa
  **AUT inmediato**.
- **Clasificación TM posible:** AUT **confirmado**; después continúa la lectura con C Grande
  candidata.
- **Eventos que produciría:** AUT inmediato; TT pendiente/confirmado según módulo.
- **Condición que la confirmaría:** los hechos de vela 6 (AUT al tocar el nivel, §10.5).
- **Condición que la cancelaría:** que el contacto sin continuación impida el AUT.

**ESCENA B**
- **Secuencia de movimientos:** B Grande toca el 127 % + 0,25 **y vuelve** → **no** AUT; el
  recorrido continúa como **C Grande → CUT** sin AUT.
- **Clasificación TM posible:** sin AUT; C Grande → CUT.
- **Eventos que produciría:** C Grande y CUT **sin** AUT.
- **Condición que la confirmaría:** la hipótesis §20.16 (declarada **no-regla**).
- **Condición que la cancelaría:** la regla cerrada §10.5 (AUT inmediato).

### PREGUNTA CONCRETA A JAVIER
- ¿«Tocar el 127 % + 0,25 **y volver**» activa **AUT de forma inmediata** (regla cerrada §10.5), o
  permite que el recorrido continúe como **C Grande → CUT sin AUT** (hipótesis §20.16)?

### EFECTO DE LA RESPUESTA
- **Regla que se podrá cerrar:** relación AUT ↔ C Grande/CUT; se neutraliza o se confirma §20.16
  frente a §10.5.
- **Tests afectados:** test de AUT ante «tocar y volver»; golden velas 6 y 8.
- **Bloque de implementación desbloqueado:** **Bloques 2 y 3** (AUT / C Grande / CUT).

---

## DUDA-004

**ID DE DUDA:** DUDA-004 (origen C4)
**AGENTE QUE LA ORIGINA:** SCENE_QUESTIONER (a instancia de TM_VOCABULARY_REVIEWER)
**ESTADO:** CERRADA → `DECISIONES_EXPERTO.md` **DEC-004** (respuesta del experto: lecturas concurrentes = `lectura 1 / lectura 2 / lectura 3`).
**REGLA AFECTADA:** §10.8 (concurrencia y reclasificación) y D (vocabulario obligatorio).

### HECHOS OBJETIVOS
- **Timestamp inicial:** no aplica (duda de **redacción**, no de recorrido).
- **Timestamp final:** no aplica.
- **Vela o velas:** no aplica (afecta a la concurrencia general y a la vela 8, con R-D y R-E
  simultáneas).
- **Apertura:** no aplica.
- **Extremos en orden temporal:** no aplica.
- **Precio final:** no aplica.
- **Serie de precio usada:** Bid.
- **Movimientos reconstruidos:** en la vela 8 coexisten **R-D** (B Grande) y **R-E** (C Grande
  candidata) — dos lecturas simultáneas; en general, «normalmente dos lecturas» (§10.8).
- **Lecturas activas antes de la duda:** R-A, R-D, R-E.

### LO QUE SABEMOS POR TM
- **Regla 1 (§10.8 / C):** normalmente pueden coexistir **dos** lecturas; máximo operativo **tres**;
  una lectura puede quedar confirmada, reclasificada, integrada, invalidada o finalizada;
  **reclasificar no significa borrar**.
- **Regla 2 (D):** vocabulario permitido = `lectura` + sus estados; **prohibido** `local · superior ·
  estructura · giro · B excesiva · observador` en estados, eventos, golden y documentación funcional.

### LO QUE NO SABEMOS
- Punto exacto no resuelto: la **redacción TM autorizada** para (a) la segunda/tercera **lectura
  concurrente** y (b) la **referencia de módulo de mayor alcance**, sin usar los términos
  prohibidos.

### ESCENAS POSIBLES

**ESCENA A**
- **Secuencia de movimientos:** no aplica (nomenclatura).
- **Clasificación TM posible:** segunda/tercera lectura = «**lectura alternativa**»; referencia de
  módulo mayor = «**referencia de lectura de mayor alcance**».
- **Eventos que produciría:** nombres de lectura y de referencia sin términos prohibidos.
- **Condición que la confirmaría:** que la jerarquía quede clara sin ambigüedad.
- **Condición que la cancelaría:** que el término introduzca una noción ajena a la TM.

**ESCENA B**
- **Secuencia de movimientos:** no aplica (nomenclatura).
- **Clasificación TM posible:** segunda/tercera lectura = «**lectura concurrente**» (o «segunda
  lectura»); referencia de módulo mayor = «**módulo de referencia mayor**».
- **Eventos que produciría:** nombres de lectura y de referencia sin términos prohibidos.
- **Condición que la confirmaría:** que Javier ratifique el término como TM.
- **Condición que la cancelaría:** que el término se solape con otro ya en uso.

### PREGUNTA CONCRETA A JAVIER
- ¿Cuál es la redacción TM autorizada para nombrar la **segunda/tercera lectura** (alternativa a
  «local») y para la **referencia de módulo de mayor alcance** (alternativa a «superior»)?

### EFECTO DE LA RESPUESTA
- **Regla que se podrá cerrar:** vocabulario de concurrencia/reclasificación aplicable a estados,
  eventos, golden y documentación funcional.
- **Tests afectados:** test de vocabulario (`REVISION_VOCABULARIO_TM.md`); nombres en el golden.
- **Bloque de implementación desbloqueado:** normalización de reglas **C** y **F** (concurrencia /
  reclasificación) para Bloque 3.

---

## DUDA-005

**ID DE DUDA:** DUDA-005 (origen C6)
**AGENTE QUE LA ORIGINA:** SCENE_QUESTIONER (propuesta §9.3 detectada por RULES_ANALYST)
**ESTADO:** CERRADA → `DECISIONES_EXPERTO.md` **DEC-005** (respuesta del experto: primero el gap; si hay gap no se aplica la regla de 2).
**REGLA AFECTADA:** prioridad entre el **gap** (§9.1 / §9.3) y la **regla de 2** (§4.2 / §10.2).

### HECHOS OBJETIVOS
- **Timestamp inicial:** 16:35:59.907 (cierre vela 6) → 16:36:00.107 (apertura vela 7).
- **Timestamp final:** 16:37:59.977 (cierre vela 8) → 16:38:00.178 (apertura vela 9).
- **Vela o velas:** fronteras **1→2, 6→7, 7→8, 8→9**.
- **Apertura:** vela 7 = 29719,10; vela 8 = 29734,80; vela 9 = 29688,30.
- **Extremos en orden temporal:** no aplica (duda de frontera de vela).
- **Precio final:** no aplica.
- **Serie de precio usada:** Bid.
- **Movimientos reconstruidos:** en las fronteras **6→7, 7→8 y 8→9** el movimiento **no** se
  interrumpe y produce nuevo extremo (delta de apertura −1,60; −0,90; −0,80). En la frontera
  **1→2** el delta es **−0,80** y la lectura previa lo clasificó como **salida en plano**
  (`golden_estados_velas_1_8.json`, vela 2, hoy PENDIENTE).
- **Lecturas activas antes de la duda:** R-A / R-B (frontera 6→7), R-C (7→8), R-D (8→9).

### LO QUE SABEMOS POR TM
- **Regla 1 (§10.2 / §4.2 / A1):** al abrir una vela nueva se comprueba primero **gap o salida en
  plano**; si falla cualquier condición de 2, 1 pasa a **módulo** y el movimiento contrario es
  **A Grande**.
- **Regla 2 (§9.1):** un **gap a favor de 1** contiene A y B **implícitas** y activa el **posible
  TT** (que solo se confirma al 100 %).
- **Regla 3 (§9.3, marcada «PROPUESTA, PENDIENTE DE CONFIRMAR»):** evaluar **primero** el gap y
  aplicar la regla de 2 **solo cuando no hay gap**.

### LO QUE NO SABEMOS
- Punto exacto no resuelto: qué se evalúa **primero** al abrir una vela nueva — el **gap** o la
  **regla de 2** (§4.2); es decir, si §9.3 (gap primero) **sustituye** o solo **completa** a §4.2.

### ESCENAS POSIBLES

**ESCENA A**
- **Secuencia de movimientos:** al abrir vela se evalúa **primero el gap**; con **gap a favor de 1**
  el intervalo contiene A y B implícitas y activa el posible TT; la regla de 2 (§4.2) se aplica
  **solo cuando no hay gap**.
- **Clasificación TM posible:** gap con **prioridad** sobre la regla de 2.
- **Eventos que produciría:** posible TT activado por gap.
- **Condición que la confirmaría:** la propuesta §9.3.
- **Condición que la cancelaría:** §4.2 aplicándose siempre, con o sin gap.

**ESCENA B**
- **Secuencia de movimientos:** al abrir vela se evalúa **primero la regla de 2**; el gap solo se
  considera cuando no se cumplen las condiciones de 2 (o cuando supera su umbral).
- **Clasificación TM posible:** **regla de 2** con prioridad sobre el gap.
- **Eventos que produciría:** módulo / A Grande antes de considerar el gap.
- **Condición que la confirmaría:** §4.2 como regla general.
- **Condición que la cancelaría:** §9.3 (gap primero).

### PREGUNTA CONCRETA A JAVIER
- Al abrir una vela nueva, ¿se evalúa **primero el gap** o **primero la regla de 2** (§4.2); y en
  caso de **gap a favor de 1**, se activa el **posible TT** sin aplicar la regla de 2?

### EFECTO DE LA RESPUESTA
- **Regla que se podrá cerrar:** prioridad gap ↔ regla de 2 (`PR-k` / §9.3 frente a §4.2).
- **Tests afectados:** test de gap / salida en plano / posible 2 (golden vela 2, hoy PENDIENTE);
  formación del módulo.
- **Bloque de implementación desbloqueado:** **Bloque 1** (módulo / 2 / 3).

---

## DUDA-006

**ID DE DUDA:** DUDA-006 (origen C1, derivada de DUDA-001 / DEC-006)
**AGENTE QUE LA ORIGINA:** SCENE_QUESTIONER
**ESTADO:** **CERRADA → `DECISIONES_EXPERTO.md` DEC-011** (el CUT **no** ocurre en la vela 8)
**REGLA AFECTADA:** §10.7 — CUT (C Grande alcanza el final de A Grande).

> **RESOLUCIÓN — DEC-011.** Por regla del experto, en la **vela 8** el recorrido es **A Grande +
> B Grande → AUT**; **NO** hay **C Grande** ni **CUT** en la vela 8. Cierra la subcuestión
> **C8/C1b** y, junto con DUDA-010, **cierra C1**. El golden de vela 8 («C Grande → CUT») queda
> **pendiente de corrección del golden** (no se toca ahora).

### HECHOS OBJETIVOS
- Vela 8 (Bid): apertura 29734,80; MÁXIMO **29744,40** @16:37:10.254; después MÍNIMO **29683,20**
  @16:37:59.175 (último tick de la vela).
- Desde el máximo, B Grande (R-D) alcanza el 100 % (29712,40) @16:37:35.310 y **supera** el
  127 % + 0,25 (29703,51) @16:37:55.363, llegando a 29683,20.
- Tras el máximo de la vela 8 **no hay ningún tick ≥ 29738,40/29744,40** hasta la **vela 16/17**.

### LO QUE SABEMOS POR TM
- **Regla 1 (DEC-003):** si B Grande **supera** 127 % + 0,25 ⇒ **AUT**; si no supera y vuelve ⇒
  B Grande + C Grande.
- **Regla 2 (§10.7 / B4):** C Grande solo tras B Grande; **CUT se confirma cuando C Grande alcanza
  el final de A Grande**.

### LO QUE NO SABEMOS
- Si en la vela 8 el recorrido B Grande → AUT con C Grande posterior (que **no** alcanza el final
  de A Grande dentro de la vela 8) confirma **CUT en la vela 8** o el CUT queda **pendiente** hasta
  que C Grande alcance el final de A Grande (más tarde, vela 16/17).

### PREGUNTA CONCRETA A JAVIER
- Con los ticks, en la vela 8 el recorrido es **B Grande (supera 127 % + 0,25) → AUT**, y **C Grande**
  sube después pero **no alcanza el final de A Grande dentro de la vela 8**. ¿Confirmas que el
  **CUT no es en la vela 8** sino cuando **C Grande alcance el final de A Grande** (más tarde)?

### EFECTO DE LA RESPUESTA
- **Regla que se podrá cerrar:** referencia e instante del **CUT** cuando C Grande no alcanza el
  final de A Grande en la vela de B Grande. Cierra C1.
- **Tests afectados:** test de C Grande / CUT; golden vela 8 (`C_CANDIDATA`, `CUT`).
- **Bloque desbloqueado:** **Bloque 3** (C Grande candidata, cancelación, CUT).

---

## DUDA-007

**ID DE DUDA:** DUDA-007 (origen C1, derivada de DUDA-001 / DEC-006)
**AGENTE QUE LA ORIGINA:** SCENE_QUESTIONER
**ESTADO:** **BLOQUEANTE**
**REGLA AFECTADA:** §10.4 — final de A Grande («A Grande acaba cuando supera el módulo»).

### HECHOS OBJETIVOS
- R-A: módulo vela 1+2, rango 77,90 (29838,20 − 29760,30); **A Grande termina en 29820,80**;
  **máximo del módulo = 29838,20**.
- A Grande = **movimiento contrario al módulo** (afirmación del experto, DEC-006).

### LO QUE SABEMOS POR TM
- **Regla 1 (DEC-006, tentativa):** «A Grande acaba cuando **supera el módulo**».
- **Regla 2 (A2):** el módulo conserva máximo, mínimo y rango completo; la expansión (TT) usa el
  rango completo del módulo.

### LO QUE NO SABEMOS
- Qué significa exactamente **«supera el módulo»** para el final de A Grande, dado que en esta
  muestra **A Grande termina en 29820,80** y el **módulo llega a 29838,20** (A Grande **no** supera
  el máximo del módulo).

### PREGUNTA CONCRETA A JAVIER
- Aclara «A Grande acaba cuando **supera el módulo**»: ¿a qué se refiere exactamente **«superar el
  módulo»** para el final de A Grande, dado que en esta muestra A Grande termina en 29820,80 y el
  módulo llega a 29838,20?

### EFECTO DE LA RESPUESTA
- **Regla que se podrá cerrar:** definición operativa del **final de A Grande** (referencia de CUT)
  en función del módulo.
- **Tests afectados:** medida del módulo / final de A Grande; referencia de CUT.
- **Bloque desbloqueado:** **Bloques 2–3** (A Grande / B Grande / C Grande / CUT).

---

## DUDA-008

**ID DE DUDA:** DUDA-008 (SALIDA EN PLANO)
**AGENTE QUE LA ORIGINA:** SCENE_QUESTIONER (ACLARACIÓN 5 / DEC-007)
**ESTADO:** **CERRADA → `DECISIONES_EXPERTO.md` DEC-009** (tolerancia fijada por el experto)
**REGLA AFECTADA:** tolerancia de la **salida en plano** (apertura de vela nueva sin gap).

> **RESOLUCIÓN — DEC-009 (ex DUDA-008).** El experto fijó la tolerancia: **salida en plano** si
> `|cierre del movimiento anterior − apertura de la vela siguiente| ≤ 1 tick TM = 0,25 puntos`; si
> es **> 1 tick** es **gap** (y con gap no se aplica la regla de 2, **H11**). Umbral
> **`plano_max_points = 0.25`**, **fijo**, no derivado del CSV ni del delta −0,80. Trasladada a
> `REGLAS_CERRADAS.md` **H14**. Se conserva el historial de abajo (estado ABIERTO previo), superado
> por esta decisión.

### HECHOS OBJETIVOS
- La regla de **salida en plano sigue ABIERTA**: su **tolerancia queda PENDIENTE**.
- **No** debe deducirse a partir de: el **menor cambio de precio del CSV**; el **tick TM de
  0,25**; la **diferencia de −0,80** de esta muestra. Son conceptos distintos.
- Registro literal del experto: **SALIDA EN PLANO = PENDIENTE DE REGLA EXPERTA**.

### LO QUE SABEMOS POR TM
- **Regla 1 (§10.2 / A1 / A4):** al abrir una vela nueva se comprueba **primero el gap** y, si no
  hay gap, **salida en plano**; la salida en plano puede abrir el **posible 2**.
- **Regla 2 (DEC-001):** existe una tolerancia provisional de **±1 tick** (su test rojo sigue
  pendiente), pero para este caso el experto mantiene la tolerancia **PENDIENTE**.

### LO QUE NO SABEMOS
- La **tolerancia exacta** con la que se decide **plano** frente a **gap** al abrir una vela nueva.

### DATOS QUE SE PRESENTARÁN AL PREGUNTAR
- **Cierre exacto del movimiento anterior.**
- **Apertura exacta de la vela siguiente.**
- **Diferencia** entre ambas.
- **Máximo y mínimo iniciales de la nueva vela.**
- **Serie de precio usada** (Bid).
- **Lectura TM vigente** en ese instante.
- **Escenas posibles:** **plano** o **gap**.

### ESCENAS POSIBLES

**ESCENA A**
- **Secuencia de movimientos:** la apertura de la vela siguiente permanece **dentro de la
  tolerancia** del cierre del movimiento anterior (sin gap) → **plano**.
- **Clasificación TM posible:** **salida en plano**; habilita el **posible 2**.
- **Eventos que produciría:** posible 2.
- **Condición que la confirmaría:** que la diferencia quede dentro de la tolerancia que fije Javier.
- **Condición que la cancelaría:** que la diferencia supere la tolerancia (→ gap).

**ESCENA B**
- **Secuencia de movimientos:** la apertura de la vela siguiente **salta** respecto del cierre
  anterior más allá de la tolerancia → **gap**.
- **Clasificación TM posible:** **gap** (a favor o contrario a 1).
- **Eventos que produciría:** A y B implícitas / posible TT (gap a favor) o A Grande (gap contrario).
- **Condición que la confirmaría:** que la diferencia supere la tolerancia que fije Javier.
- **Condición que la cancelaría:** que la diferencia quede dentro de la tolerancia (→ plano).

### PREGUNTA CONCRETA A JAVIER
- ¿Cuál es la **tolerancia exacta** de la **salida en plano** al abrir una vela nueva, sin
  deducirla del menor cambio del CSV, del tick TM de 0,25 ni de la diferencia de −0,80?

### EFECTO DE LA RESPUESTA
- **Regla que se podrá cerrar:** tolerancia de la salida en plano (frontera plano ↔ gap).
- **Tests afectados:** test de gap / salida en plano / posible 2; formación del módulo.
- **Bloque desbloqueado:** **Bloque 1** (módulo / 2 / 3).

---

## DUDA-009

**ID DE DUDA:** DUDA-009 (A GRANDE / MÓDULO)
**AGENTE QUE LA ORIGINA:** SCENE_QUESTIONER (ACLARACIÓN 4 / DEC-007)
**ESTADO:** **PARCIALMENTE RESPONDIDA → `DEC-010`** (A Grande **sí**; **módulo general ABIERTO**)
**REGLA AFECTADA:** §10.4 — «A Grande es el movimiento contrario al módulo»; nuevo 1 (alias
«posible 1», unificado por **DEC-012**) tras AUT.

> **ÚNICA DUDA VIVA DEL GATE CERO.** Lo único que mantiene abierta esta duda es la **regla general
> del módulo**: **¿el módulo es siempre de 2 velas o puede ser de una sola vela / vela anterior por
> descarte?** (junto con qué significa «superar el autocorte correspondiente al módulo»). El resto
> (A Grande = movimiento contrario al módulo) quedó respondido en **DEC-010**.

> **RESOLUCIÓN PARCIAL — DEC-010.** El experto confirma que **A Grande sí** es el movimiento
> contrario al módulo y, sobre el **fin de A Grande**, fija que su **extremo se actualiza por
> coherencia entre velas** (en la muestra **`29.744,40`**, no `29.738,40`): hecho registrado en
> **DEC-010 / H15**. **La parte «qué módulo usa la lectura» sigue ABIERTA** (qué módulo usa la
> lectura y qué significa «superar el autocorte correspondiente al módulo»). Por eso `DUDA-009`
> queda **solo parcialmente respondida** y **no cierra C7**.

### HECHOS OBJETIVOS
- **A Grande = movimiento contrario al módulo** (afirmación del experto, DEC-006 / ACLARACIÓN 4).
- Instrucción literal: **NO** traducir todavía esto como «A Grande siempre termina cuando supera
  el módulo» (puede ser incorrecta o incompleta).
- Registro provisional: **A Grande es el movimiento contrario al módulo**; si el movimiento
  contrario **supera el autocorte correspondiente al módulo**, se confirma **AUT**; desde AUT ese
  movimiento **puede considerarse nuevo 1** (alias «posible 1»), sin que su función definitiva
  quede decidida.

### LO QUE SABEMOS POR TM
- **Regla 1 (§10.4):** A Grande puede continuar durante varias velas; si A Grande crea un nuevo
  extremo, la B Grande candidata se cancela.
- **Regla 2 (B2):** AUT **no** confirma definitivamente que el movimiento sea un nuevo 1.

### LO QUE NO SABEMOS
- La **interpretación completa** de «A Grande es el movimiento contrario al módulo».
- Si un movimiento que **supera el módulo** (el autocorte correspondiente al módulo) es un
  **nuevo 1** (alias «posible 1»), permaneciendo su **función definitiva sin decidir**.

### ESCENAS POSIBLES

**ESCENA A**
- **Secuencia de movimientos:** movimiento contrario al módulo lo **supera**; se confirma AUT.
- **Clasificación TM posible:** AUT; ese movimiento **puede considerarse nuevo 1** (alias «posible 1») (función
  definitiva sin decidir).
- **Eventos que produciría:** AUT; nuevo 1 en observación.
- **Condición que la confirmaría:** que la superación del autocorte del módulo confirme AUT.
- **Condición que la cancelaría:** que el movimiento no supere el autocorte correspondiente.

**ESCENA B**
- **Secuencia de movimientos:** movimiento contrario al módulo **no** lo supera.
- **Clasificación TM posible:** sigue siendo el movimiento contrario (A Grande / candidato) sin
  AUT por superación del módulo.
- **Eventos que produciría:** sin AUT por esa vía.
- **Condición que la confirmaría:** que no se alcance el autocorte correspondiente al módulo.
- **Condición que la cancelaría:** que el movimiento supere el autocorte correspondiente.

### PREGUNTA CONCRETA A JAVIER
- Aclara la interpretación completa de **«A Grande es el movimiento contrario al módulo»** y
  confirma si un movimiento que **supera el módulo** es un **nuevo 1** (alias «posible 1») (con su función
  definitiva sin decidir todavía).

### EFECTO DE LA RESPUESTA
- **Regla que se podrá cerrar:** definición operativa de A Grande respecto del módulo y del
  nuevo 1 (alias «posible 1») tras AUT.
- **Tests afectados:** medida del módulo / A Grande; AUT; nuevo 1.
- **Bloque desbloqueado:** **Bloques 2–3** (A Grande / B Grande / AUT / nuevo 1).

---

## DUDA-010

**ID DE DUDA:** DUDA-010 (CONFIRMAR C1 — vela 8)
**AGENTE QUE LA ORIGINA:** SCENE_QUESTIONER / RULES_ANALYST (a partir de DEC-010)
**ESTADO:** **CERRADA → `DECISIONES_EXPERTO.md` DEC-011** (cierra **C1**)
**REGLA AFECTADA:** §10.4 (fin de A Grande) y §10.7 (C Grande y CUT).

> **RESOLUCIÓN — DEC-011.** El experto confirma que en la **vela 8** el recorrido es **A Grande
> (extremo `29.744,40`) + B Grande → AUT (posible 1)** y que **NO** hay **C Grande** ni **CUT** en
> esa vela. Además admite **2 lecturas concurrentes** (`lectura 1` / `lectura 2`), con la **vela 7
> como módulo por descarte** (→ **H16** CERRADA, **H17** PROVISIONAL). Cierra **C1** y **C8/C1b**.
> El golden de vela 8 («C Grande → CUT») queda **pendiente de corrección del golden** (no se toca
> ahora). Derivó en **DUDA-011**.

### HECHOS OBJETIVOS
- **A Grande = movimiento contrario al módulo**; su **extremo se actualiza por coherencia entre
  velas**: en la muestra A Grande = **`29712,40 → 29744,40`** (cruza las velas 7 y 8); extremo
  **`29.744,40`**, **no** `29.738,40` (**DEC-010 / H15**).
- Vela 8 (Bid): máximo `29744,40` @16:37:10.254; después **baja** hasta `29683,20` @16:37:59.175.
- Desde el extremo `29744,40`, el contrario bajista **supera el 127 % + 0,25** (`29703,51`)
  @16:37:55.363 ⇒ **AUT** (regla cerrada H9 / DEC-003).
- El experto describe la vela 8 como **«casi seguro hizo A, B, AUT»** y **no menciona C Grande**.

### LO QUE SABEMOS POR TM
- **Regla 1 (DEC-010 / H15):** fin de A Grande = **extremo del movimiento** (`29.744,40`).
- **Regla 2 (H9 / DEC-003):** B Grande que **supera** 127 % + 0,25 ⇒ **AUT inmediato → posible 1**.
- **Regla 3 (§10.7 / B4):** C Grande solo puede aparecer **después de B Grande**; **CUT** se
  confirma cuando C Grande **alcanza el final de A Grande**.

### LO QUE NO SABEMOS
- Si la vela 8 queda confirmada como **A Grande (extremo `29.744,40`) + B Grande → AUT (posible 1)**,
  **sin** C Grande ni CUT en esa vela; es decir, si se cierra **C1** retirando el C Grande/CUT de la
  vela 8 del golden (sin mover el evento: se registraría como inconsistencia resuelta).

### ESCENAS POSIBLES

**ESCENA A**
- **Secuencia de movimientos:** extremo de A Grande `29744,40` → **B Grande** bajista → supera
  `127 % + 0,25` → **AUT** (paso a **posible 1**); **no** hay **C Grande** ni **CUT** en la vela 8.
- **Clasificación TM posible:** A Grande + B Grande → AUT (posible 1).
- **Eventos que produciría:** AUT; posible 1; sin C Grande/CUT en la vela 8.
- **Condición que la confirmaría:** que el experto confirme «A, B, AUT» sin C Grande en la vela 8.
- **Condición que la cancelaría:** que exista **C Grande** y **CUT** en la vela 8 (ESCENA B).

**ESCENA B**
- **Secuencia de movimientos:** tras **B Grande → AUT**, un contrario alcista **C Grande** alcanza el
  final de A Grande **dentro de la vela 8** → **CUT** en la vela 8.
- **Clasificación TM posible:** B Grande → AUT → C Grande → CUT.
- **Eventos que produciría:** C Grande y CUT en la vela 8.
- **Condición que la confirmaría:** los ticks mostrando C Grande alcanzando `29.744,40` en la vela 8.
- **Condición que la cancelaría:** que ningún tick alcance `29.744,40` en la vela 8 (hecho: el primer
  tick ≥ `29738,40`/`29744,40` posterior es de la **vela 16/17**).

### PREGUNTA CONCRETA A JAVIER
- ¿Confirmas que en la **vela 8** el recorrido es **A Grande (extremo `29.744,40`)** y después
  **B Grande → AUT (posible 1)**, y que **NO** hay **C Grande** ni **CUT** en esa vela?

### EFECTO DE LA RESPUESTA
- **Regla que se podrá cerrar:** cierre de **C1** (C Grande/CUT y final de A Grande, vela 8).
- **Tests afectados:** test de C Grande / CUT; golden vela 8 (`C_CANDIDATA`, `CUT`, hoy PENDIENTE).
- **Bloque desbloqueado:** **Bloque 3** (C Grande candidata, cancelación, CUT).

---

## DUDA-011

**ID DE DUDA:** DUDA-011 (LECTURA 2 — sentido de «se pasa»)
**AGENTE QUE LA ORIGINA:** SCENE_QUESTIONER / RULES_ANALYST (a partir de DEC-011)
**ESTADO:** **CERRADA → `DECISIONES_EXPERTO.md` DEC-012** («se pasa» = B supera 127 % + 0,25 →
**AUT → nuevo 1**)
**REGLA AFECTADA:** §10.4 (A Grande / módulo por descarte) y §10.5 (AUT / 127 % + 0,25).

> **RESOLUCIÓN — DEC-012.** Respuesta literal del experto: «b se pasa es eso que super ael
> 127+0,25 y se convierte en aut y nuevo 1». Por tanto **«se pasa» = B supera 127 % + 0,25 →
> AUT → nuevo 1** (corresponde a la **ESCENA A**); se descarta la **ESCENA B** (rebasar el extremo
> de A Grande). **Cierra DUDA-011.** La **regla general del módulo** (`DUDA-009`) sigue **abierta**.

### HECHOS OBJETIVOS
- **A Grande = movimiento contrario al módulo** (**DEC-011 / H17**, módulo por descarte).
- **Lectura 2 (DEC-011):** el **retroceso** del **final de la vela 7 / inicio de la vela 8** se lee
  como **A Grande** del **módulo = vela 7**; después **sube con B**, **«pero se pasa»**.
- Serie de precio usada: **Bid**.

### LO QUE SABEMOS POR TM
- **Regla 1 (H9 / DEC-003):** **AUT** se confirma **solo al SUPERAR 127 % + 0,25**; si B solo
  **toca** y vuelve, no hay AUT y el movimiento contrario comienza como **C Grande candidata**.
- **Regla 2 (H16 / DEC-011):** coexisten **2 lecturas** (`lectura 1` / `lectura 2`) que **se
  resuelven más adelante**; hay que **atender a ambas**.

### LO QUE NO SABEMOS
- El **sentido exacto** de **«se pasa»** en la **lectura 2**: si significa que **B supera
  127 % + 0,25** (es decir, **AUT**), o si significa que **B se pasa del extremo** (supera el
  extremo de A Grande).

### ESCENAS POSIBLES

**ESCENA A**
- **Secuencia de movimientos:** en la **lectura 2**, tras la **A Grande** del **módulo-vela 7**,
  **B sube** y **supera 127 % + 0,25** → **«se pasa»** = **AUT**.
- **Clasificación TM posible:** **AUT** (nuevo 1).
- **Eventos que produciría:** AUT; nuevo 1.
- **Condición que la confirmaría:** que **B** supere el nivel `127 % + 0,25` de esa lectura.

**ESCENA B**
- **Secuencia de movimientos:** en la **lectura 2**, **B sube** y **se pasa del extremo** (supera el
  extremo de A Grande) — **«se pasa»** = rebasa el **extremo**.
- **Clasificación TM posible:** movimiento contrario que **excede el extremo** (reclasificación /
  nuevo extremo).
- **Eventos que produciría:** nuevo extremo; posible **colisión con la lectura 1**.
- **Condición que la confirmaría:** que **B** supere el **extremo de A Grande** de esa lectura.

### PREGUNTA CONCRETA A JAVIER
- En la **lectura 2**, el **retroceso** del **final de vela 7 / inicio de vela 8** es **A Grande**
  del **módulo-vela 7**, y después **sube B «pero se pasa»**: ¿qué significa **«se pasa»** — que
  **B supera 127 % + 0,25** (**AUT**) o que **se pasa del extremo**?

### EFECTO DE LA RESPUESTA
- **Regla que se podrá cerrar:** sentido de **«se pasa»** en la **lectura 2**; relación con **AUT**
  y con el **extremo** de A Grande.
- **Tests afectados:** test de **AUT** en la lectura 2; resolución de las **2 lecturas**
  concurrentes (`lectura 1` / `lectura 2`).
- **Bloque desbloqueado:** cierre de la parte **módulo** (C7 / DUDA-009) y de la **concurrencia**.

---

## Anexo — Pendientes §11 aún NO convertidos a escena (NO BLOQUEANTES para los bloques 1–3)

Se mantienen en `REGLAS_PROVISIONALES.md` y se convertirán a escena cuando su bloque dependiente lo
requiera. No se pregunta lo ya respondido.

- **P2** — Serie de precio del replay (Bid/Ask/Last/mid). `AUDITORIA_DATOS.md` fija **Bid** de forma
  inequívoca en esta muestra; queda solo la ratificación del experto (no bloqueante).
- **P3** — Momento exacto en que un movimiento contrario queda confirmado como A/B/C Grande (más
  allá del umbral numérico ya cerrado).
- **P4** — Criterios de reclasificación de varias velas como módulo o 1 conjunto/1 compuesto.
- **P5** — Permanencia de una lectura a través de nuevos movimientos (afecta a `POSIBLE_1_FIN`, vela 7).
- **P6** — Reglas completas de FT (FT no aparece en la lectura cerrada de velas 1–8).

---

*Artefacto del agente SCENE_QUESTIONER. Alimenta a TM_VOCABULARY_REVIEWER (§6, segunda oleada) y la
pausa obligatoria ante Javier. No se programa núcleo TM antes del gate de comprensión.*
