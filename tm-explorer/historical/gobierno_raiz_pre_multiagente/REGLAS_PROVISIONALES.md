# REGLAS PROVISIONALES — Núcleo TM Explorer

Todo lo que **no** está cerrado. Recorte vigente tras las decisiones **DEC-001 … DEC-005**:
se retiran los puntos ya cerrados y se conservan solo los pendientes vivos.

- Nada aquí se asume: cada punto es **PROVISIONAL** (hay indicio, falta formalizar) o
  **PENDIENTE** (falta el dato o la respuesta del experto).
- Cada punto se resolverá **por escenas de movimiento** y se registrará en
  `DECISIONES_EXPERTO.md`; después pasará a `REGLAS_CERRADAS.md`.
- Bloqueo de implementación vigente: **ninguno bloqueante salvo la parte abierta de C7**
  (**módulo general**, `DUDA-009`); **C1 está RESUELTA** (DEC-011) y **DUDA-011 CERRADA**
  (DEC-012). Ver `CONTRADICCIONES.md`.

Leyenda: `PROVISIONAL` = enunciada pero no formalizada · `PENDIENTE` = sin enunciado.

## Cerradas y retiradas de este documento (historial)
- Salida en plano = **±1 tick** — **DEC-001** (test rojo pendiente en Bloque 1).
  **REABIERTA como PENDIENTE por DEC-007 / ACLARACIÓN 5 → ver PR-p (DUDA-008).**
- Salida en plano = **≤ 1 tick TM (0,25 puntos); > 1 tick = gap** — **DEC-009** (ex DUDA-008):
  umbral **`plano_max_points = 0.25`** fijo, **no derivado del CSV**. **CIERRA PR-p.** Trasladada a
  `REGLAS_CERRADAS.md` **H14**.
- Unidad del nivel AUT = **1 tick = 0,25 puntos** — **DEC-002** (ex C2).
- AUT exige **superar** 127 % + 0,25 (tocar y volver ≠ AUT) — **DEC-003** (ex C3).
- Lecturas concurrentes = **lectura 1 / lectura 2 / lectura 3** — **DEC-004** (ex C4).
- Orden **gap antes de la regla de 2** — **DEC-005** (ex C6).

---

## P2 — Serie de precio del replay
- **Estado:** PENDIENTE.
- **Duda:** si los datos mezclan Bid, Ask, Last o punto medio, ¿qué serie usa el replay?
- **Responsable:** DATA_AUDITOR (`AUDITORIA_DATOS.md` fija **Bid** en esta muestra; falta la
  ratificación del experto). RULES_ANALYST no la decide.

## P3 — Momento de confirmación del movimiento contrario como A/B/C Grande
- **Estado:** PROVISIONAL.
- **Enunciado parcial cerrado:** A Grande candidata se cancela si A Grande crea nuevo extremo
  (→ B Grande candidata se cancela y A continúa); B Grande candidata se cancela si B Grande
  crea nuevo extremo.
- **Falta:** el tick exacto en que un movimiento contrario pasa de candidato a confirmado
  como A Grande, B Grande o C Grande, más allá del umbral numérico ya cerrado (100 % para B;
  C Grande conforme a H1).

## P4 — Reclasificación como módulo o 1 conjunto/1 compuesto
- **Estado:** PROVISIONAL.
- **Indicio (adenda v4 §3):** si una vela posterior corrige, las velas anteriores pueden
  reclasificarse como módulo o 1 compuesto; la corrección pasa a ser A Grande.
- **Falta:** criterios exactos (qué corrección, qué umbral, cuántas velas).

## P5 — Prioridad y permanencia entre lecturas concurrentes
- **Estado:** PROVISIONAL.
- **Indicio:** una lectura permanece activa hasta una resolución matemática (alcanzar TT al
  100 %, confirmar CUT, tocar su invalidación o quedar sustituida por otra más coherente).
- **Falta:** la prioridad formal cuando dos o tres lecturas alcanzan nivel **en el mismo
  tick**, y la regla de sustitución entre **lectura 1 / lectura 2 / lectura 3**.

## P6 — Reglas completas de FT
- **Estado:** PENDIENTE.
- **Cerrado solo:** sin TT confirmado no existe FT; FT requiere pérdida de velocidad y un
  movimiento contrario claro; un micromovimiento posterior a TT no es FT.
- **Falta (dossier §8.4 / §20.4):** referencia exacta a atravesar, desplazamiento mínimo del
  movimiento contrario, caída de velocidad necesaria y tratamiento cuando TT y FT ocurren en
  la misma vela.

## PR-e — C Grande cuando no alcanza CUT
- **Estado:** PROVISIONAL.
- **Indicio (§5.4 / §20.7):** tras A y B, C puede cerrar la referencia y pasar a ser **nuevo
  1** del ciclo siguiente. El desenlace `C = nuevo 1` está validado; falta la condición
  matemática exacta que lo consolida.

## PR-g — Umbral entre movimiento TM y ruido
- **Estado:** PENDIENTE.
- **Duda (§3.3 / §20.5):** umbral que separa movimiento TM relevante de micromovimiento.
  Candidatos (sin fijar): mínimo absoluto en puntos, mínimo relativo al módulo, duración,
  número de ticks, llegada a una referencia TM.

---

## PROVISIONALES NUEVAS — origen DEC-006 (respuesta ambigua, NO cerradas)

> Registro de RULES_ANALYST. La nueva respuesta del experto (registrada como **DEC-006** por
> SCENE_QUESTIONER) es **AMBIGUA**. Se transcriben aquí como **reglas CANDIDATAS** marcadas
> **PROVISIONAL**. **No** se pasan a `REGLAS_CERRADAS.md` y **no** se crea test hasta cerrar la
> regla.

## PR-m — Inicio no confirmado (B candidata) y confirmación de B Grande
- **Estado:** PROVISIONAL (origen **DEC-006**, reformulado con **ACLARACIÓN 2 / DEC-007** y
  **DEC-008**; no cerrar).
- **Cubierta por H12 / H13 (CERRADAS)** — `REGLAS_CERRADAS.md` §3, incluida la **TABLA DE
  ESTADOS (memorizar)** de **DEC-008**. La secuencia de inicio/confirmación de B Grande **ya está
  cerrada** como **H12/H13**: se mantiene aquí **solo** como PROVISIONAL por el **tick exacto de
  confirmación** (relación con **P3**). **No** se duplica como cerrada.
- **Enunciado candidato (secuencia, ACLARACIÓN 2 / DEC-007 + DEC-008):** el movimiento contrario a
  **A Grande** marca el **posible inicio de B Grande**, pero **no** confirma B Grande.
  1. A Grande.
  2. Comienza movimiento contrario.
  3. **B candidata** (inicio no confirmado).
  4. **B Grande se confirma al alcanzar el 100 % de A Grande.**
  5. `100 % ≤ recorrido ≤ 127 % + 0,25` → **B Grande, sin AUT**.
  6. `recorrido > 127 % + 0,25` → **AUT inmediato → posible 1**.
  7. **B Grande cambia de sentido** → **C Grande**
     (si después B Grande crea un nuevo extremo → **C Grande candidata se cancela** y
     **B Grande continúa**).
- **No escribir** que el movimiento «solo es B Grande» cuando alcanza el 100 %: su inicio existe
  antes como **B candidata**; el **100 % la confirma**.
- **Falta:** validar el enunciado y fijar el tick exacto de confirmación (relación con **P3**).
- **Nota:** no crear test hasta cerrar la regla.

## PR-n — Si B Grande no supera 127 % + 0,25 y se da la vuelta
- **Estado:** PROVISIONAL (origen **DEC-006**, reformulado con **ACLARACIÓN 2 / DEC-007** y
  **DEC-008**; no cerrar).
- **Cubierta por H13 (CERRADA)** — `REGLAS_CERRADAS.md` §3 y la **TABLA DE ESTADOS (memorizar)**
  de **DEC-008**. Las salidas de **H13** (`100 %–127 % + 0,25` sin AUT; `> 127 % + 0,25` → AUT
  inmediato → posible 1; B Grande cambia de sentido → C Grande; nuevo extremo → C Grande candidata
  cancelada) **ya están cerradas**. Se mantiene aquí **solo** como PROVISIONAL por el **tick
  exacto** (relación con **P3**). **No** se duplica como cerrada.
- **Enunciado candidato (secuencia, ACLARACIÓN 2 / DEC-007 + DEC-008):** si **B Grande no supera**
  127 % + 0,25 y **cambia de sentido** → **C Grande**; si después **B Grande crea un nuevo extremo**,
  la **C Grande candidata se cancela** y **B Grande continúa**. Si B Grande queda en
  `100 % ≤ recorrido ≤ 127 % + 0,25` → **B Grande, sin AUT**.
- **Nota:** coincide en apariencia con **DEC-003** (tocar y volver = B Grande + C Grande). Se
  mantiene **PROVISIONAL** hasta cerrar la regla; **no** se cierra ni se retira DEC-003.

## PR-o — A Grande y módulo (AUT / nuevo 1)
- **Estado:** PROVISIONAL (ver `CONTRADICCIONES.md` **C7**, **DUDA-009**). No cerrar.
- **Enunciado (redacción del experto, DEC-007 / ACLARACIÓN 4):** **A Grande es el movimiento
  contrario al módulo. Si el movimiento contrario supera el autocorte correspondiente al módulo,
  se confirma AUT; desde AUT ese movimiento puede considerarse nuevo 1 (alias «posible 1»), sin
  que su función definitiva quede decidida.**
- **Terminología unificada (DEC-012):** el término canónico es **nuevo 1**; «posible 1» se
  conserva solo como **alias**. Ver `DICCIONARIO_TM.md` (entrada `nuevo 1`).
- **Registro explícito:** esto **NO** se traduce a «A Grande **siempre** termina cuando supera el
  módulo». Esa redacción **puede ser incorrecta o incompleta** y queda **prohibida por ahora**
  (instrucción literal del experto).
- **Falta:** aclaración completa de Javier (**DUDA-009**, parte **módulo general**): **¿el módulo
  es siempre de 2 velas o puede ser de una sola vela / vela anterior por descarte?** No crear test;
  no implementar.

## PR-p — Salida en plano (tolerancia) — **CERRADA por DEC-009** ✅
> **ESTADO ACTUAL: CERRADA-por-DEC-009 (ex DUDA-008).** El experto fijó la tolerancia: **plano** si
> `|cierre del movimiento anterior − apertura de la vela siguiente| ≤ 1 tick TM = 0,25 puntos`; si
> es **> 1 tick** es **gap** (con gap no se aplica la regla de 2, **H11**). Umbral
> **`plano_max_points = 0.25`**, **fijo**, **no derivado del CSV**. Trasladada a
> `REGLAS_CERRADAS.md` **H14**. Se conserva a continuación el **historial** del estado PENDIENTE
> previo (superado por DEC-009).

- **Estado (histórico, superado):** **PENDIENTE DE REGLA EXPERTA** (origen **DEC-007 / ACLARACIÓN 5** → **DUDA-008**).
- **Registro literal (histórico):** **SALIDA EN PLANO = PENDIENTE DE REGLA EXPERTA.** La regla seguía **ABIERTA**.
- **No** se fijaba tolerancia. **No** se deducía del menor cambio del CSV, ni del tick TM, ni de
  diferencias observadas en esta muestra: son conceptos distintos.
- **Nota (histórica):** DEC-001 (±1 tick) quedó **reabierta** como PENDIENTE por DEC-007 / ACLARACIÓN 5.
- **Resuelto por:** respuesta de Javier a DUDA-008 → **DEC-009** (umbral ≤ 1 tick; > 1 tick = gap).
