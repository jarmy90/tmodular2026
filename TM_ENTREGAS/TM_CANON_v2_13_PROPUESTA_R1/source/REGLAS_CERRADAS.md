# REGLAS CERRADAS — Núcleo TM Explorer

Documento de cierre de ambigüedades. Solo contiene reglas **decididas por el autor**
(Javier Armada López) o **cerradas en documentos normativos vigentes**. Nada aquí es
inferido por la IA observando el resultado esperado.

- Base: `C:\Users\hp\Documents\Teoria Modular`
- Documento normativo vigente: `Prompt_ECC_OpenCode_TM_Aprendizaje_Experto_Orquestacion_v2.txt`
- Dossiers de referencia: `Dossier_TM_v3_Lectura_Obligatoria.txt`,
  `Dossier_TM_v4_Concurrencia_Reclasificacion.txt`,
  `Dossier_TM_Mejorado_Reglas_Vocabulario_Protocolo_v2.txt`,
  `Cline\Dossier_TM_Mejorado_..._v2_1.txt`, `Cline\Dossier_TM_Mejorado_..._v2_3.txt`
- Golden oficial: `tests/golden/golden_velas_1_9.json` (externo al motor).
- Estado: **cerrado para el bloque de comprensión**. Pendiente generalización a velas 9–20.
- Vigencia: bloque **A–G** mantenido y reconciliado con el prompt v2 **§10.1–§10.8**
  (ver §4 Tabla de reconciliación). Conflictos → `CONTRADICCIONES.md`.

Regla operativa heredada (dossier §21): `LEER REGLAS → NO SUPONER → MEDIR →
CLASIFICAR → SEPARAR MOVIMIENTOS Y PATRONES`.

---

## 0. FUENTES Y PRECEDENCIA

1. **Prompt v2 §10** (reglas ya cerradas TM) — fuente de máximo rango para el bloque 1.
2. **Dossier v3** (protocolo, §18 errores) y **adenda v4** (AUT, concurrencia, reclasificación).
3. **Dossier v2.3** (Cline) — última revisión consolidada del dossier "Mejorado".
4. **DECISIONES_EXPERTO.md** — respuestas literales de Javier (DEC-001 · DEC-002 · DEC-003 ·
   DEC-004 · DEC-005).

Regla de conflicto: gana la decisión literal del experto; si no existe, gana la fuente
de mayor rango; toda discrepancia no resuelta se marca en `CONTRADICCIONES.md`.

---

## 1. REGLAS CERRADAS BASE — MOVIMIENTOS Y VELAS (prompt v2 §10.1)

- **BASE-1.** La TM estudia movimientos, no colores de velas.
- **BASE-2.** Un cambio de vela **no** termina automáticamente un movimiento.
- **BASE-3.** El orden intravela es obligatorio.
- **BASE-4.** Una vela puede contener varios movimientos.
- **BASE-5.** Un movimiento puede atravesar varias velas.
- **BASE-6.** (dossier §3.2) Un cambio de dirección solo crea un movimiento TM nuevo
  cuando alcanza una referencia TM relevante; si no, permanece integrado en el activo.

---

## 2. REGLAS CERRADAS A–G (mantenidas y reconciliadas)

### A. MEDIDAS

#### A1. Medida de 1 y 2
Se compara el **desplazamiento direccional** del movimiento, **no** el `High−Low`
completo.

- `1`: movimiento que inicia el módulo y define la dirección.
- `2`: exige, simultáneamente (dossier v3 §4.2) — (a) misma dirección que 1,
  (b) rango de 2 ≥ rango de 1, (c) salida en plano,
  (d) cola observable ≤ 0,25 (alcista `Low(2)=Open(2)`; bajista `High(2)=Open(2)`).
- **Cola observable > 0,25 ⇒ no hay 2.** La tolerancia de la cola es de 1 tick (0,25 puntos),
  igual que la salida en plano (**H14**).
- La confirmación de `2` es **por desplazamiento direccional** que alcanza el tamaño
  de 1 (no por `High−Low` de la vela).
- **Orden causal de la regla de 2:** apertura nueva → gap → (si no hay gap) salida en plano
  (referencia = **cierre de la vela anterior**) ≤ 0,25 → cola observable ≤ 0,25 → posible 2 →
  **2 confirmado** al alcanzar el tamaño direccional de 1.
- Si falla cualquier condición de `2`: 1 pasa a **módulo** por descarte y el movimiento
  contrario se clasifica **A Grande**.

> Coincide con prompt v2 §10.2. Completa el resumen de §10.2 con las 4 condiciones de §4.2.
> Cierra §20.15 (dossier v3).

#### A2. Medida del módulo
Cuando falla el `3`, las velas `1` y `2` forman **módulo**. El rango para la expansión
es el **`High−Low` completo del conjunto** de velas que lo forman. Deben conservarse:
máximo, mínimo, rango completo, velas implicadas, timestamps y lectura de origen.

> Coincide con prompt v2 §10.3. Cierra §20.1.

#### A3. Proyección del TT
El TT se proyecta desde el **final de A Grande** con el **rango completo** del módulo:

- TT bajista = final de A Grande − rango del módulo.
- TT alcista = final de A Grande + rango del módulo.
- La comprobación se hace contra el extremo correspondiente y contra los ticks.

> Coincide con prompt v2 §10.6 y dossier §7.2. Cierra §20.15.

#### A4. Orden entre el gap y la regla de 2
Al abrir una vela nueva se evalúa **primero el gap** (§9.1 / §9.2). Si hay gap **no** se
aplica la regla de 2 (§4.2): el intervalo se resuelve por el gap (gap a favor de 1 → A y B
implícitas y posible TT; gap contrario a 1 → A Grande). La regla de 2 solo se aplica cuando
**no hay gap**.

> Cierra §9.3, que el dossier marcaba como «PROPUESTA, PENDIENTE DE CONFIRMAR». Incorpora
> **DEC-005 / DUDA-005** → resuelve `CONTRADICCIONES.md` C6.

---

### B. AUT, TT Y CUT

#### B1. Nivel AUT
El extra del nivel AUT es **1 tick = 0,25 puntos** (no `0,025`).

```
B Grande SUPERA 127 % de A Grande + 0,25 puntos (1 tick)
→ AUT confirmado inmediatamente en ese tick
```

- Regla general (**DEC-002 / DUDA-002**): `Nivel AUT = B Grande en 1,27 × A Grande + 0,25
  (1 tick)`. La unidad es el **tick** del instrumento, expresado aquí como 0,25 puntos de la
  muestra.
- AUT exige **SUPERAR** el nivel, no solo **tocarlo** (**DEC-003 / DUDA-003**). Si B Grande
  solo **toca** 127 % + 0,25 y vuelve, **no** hay AUT: ese movimiento es B Grande y el que
  sube después es **C Grande**. Esto neutraliza la hipótesis §20.16 (que no era regla).
- **No** debe existir `B_EXCESIVA` por superar ese nivel. Se anula el mecanismo
  `v3_2_BEX_FIX`; la adenda v4 §1 lo confirma.

> Coincide con prompt v2 §10.5. Unidad y valor histórico `0,025` cerrados por DEC-002;
> «tocar y volver» cerrado por DEC-003 → `CONTRADICCIONES.md` C2 y C3 **RESUELTAS**.

#### B2. Consecuencias de AUT
`AUT` **no** confirma definitivamente que el movimiento sea un nuevo 1. En AUT se
mantienen abiertas las posibilidades: la lectura con módulo conserva su TT pendiente;
el movimiento que alcanza AUT **puede** ser 1; puede existir otra lectura simultánea;
movimientos posteriores pueden reclasificar velas anteriores.

```
AUT = hecho inmediato
1   = posibilidad cuya función se confirma o reclasifica después
```

> Coincide con prompt v2 §10.5 ("AUT no confirma definitivamente un nuevo 1").

#### B3. Secuencia intravela cuando B Grande alcanza AUT y existe módulo
1. B Grande alcanza el 100 %.
2. B Grande queda confirmada.
3. B Grande **supera** 127 % + 0,25 (1 tick).
4. AUT se confirma inmediatamente.
5. Existe módulo ⇒ el TT queda pendiente.
6. El precio alcanza el objetivo TT ⇒ **TT confirmado** (puede ser en la misma vela, en
   tick distinto **o en el mismo tick** si un salto atraviesa ambos niveles).
7. El movimiento bajista **puede** mantenerse también como posible 1.

Orden causal obligatorio: B Grande confirmada → AUT → TT.

> Coincide con prompt v2 §10.6.

#### B4. AUT y CUT coexisten
Sí coexisten; corresponden a momentos distintos de la misma lectura.
Desde el máximo de A Grande → B Grande → AUT inmediato → después C Grande → CUT cuando
C Grande **supera** el final de A Grande. Secuencia: `B → AUT → C → CUT`.

> Coincide con prompt v2 §10.7.

#### B5. Coexistencia B Grande / AUT y frontera con la regla de 2

- **B Grande y AUT no coexisten** como clasificación vigente del mismo recorrido tras
  **superar el autocorte (127 % + 0,25)**: al superarlo, el recorrido deja de ser B Grande y se
  confirma **AUT** (**H9 / H13(c)**).
- **Con gap no hay salida en plano, ni posible 2, ni 2** (**H11 / A4 / DEC-005**): si al abrir la
  vela nueva `|Δ| > 0,25` respecto del **cierre de la vela anterior** (**H14 / DEC-013**), el
  intervalo se resuelve por el gap y **no** se evalúa la regla de 2.

> Refuerza B1/B3 y A4; referencia de la comparación por **DEC-013**.

---

### C. CONCURRENCIA

- La concurrencia es **habitual**: normalmente **dos** lecturas; **excepcionalmente tres**,
  máximo operativo **3**, mientras todas sean matemáticamente válidas y coherentes.
- **No se calculan ruido ni micromovimientos**: no se clasifican y no ocupan lectura. Se
  descartan; la selección se decide por **coherencia de movimiento**, no por cada oscilación.
- Las lecturas concurrentes se nombran **lectura 1 / lectura 2 / lectura 3** (numeración
  fuera de la terminología TM, solo identificador) — **DEC-004 / DUDA-004 / DEC-015**. Sustituye
  a «local» / «superior» en la capa funcional.
- Los espacios de lectura solo los ocupan lecturas TM válidas; una oscilación intravela
  **no** ocupa automáticamente una lectura.
- Una lectura puede ser **confirmada, reclasificada, integrada, invalidada o finalizada**.

> Coincide con prompt v2 §10.8. Vocabulario de concurrencia cerrado por DEC-004 →
> `CONTRADICCIONES.md` C4 **RESUELTA**.

---

### D. VOCABULARIO OBLIGATORIO

Usar **solo** vocabulario TM:
`1 · 2 · 3 · módulo · A Grande · B Grande · C Grande · AUT · TT · CUT · FT ·
movimiento contrario · retroceso · salida en plano · gap · lectura ·
lectura 1 · lectura 2 · lectura 3 (identificador de concurrencia, DEC-004) ·
lectura candidata · lectura confirmada · lectura reclasificada · lectura integrada ·
lectura invalidada · lectura finalizada`.

**Prohibido** como clasificación: `local · superior · estructura · giro · B excesiva ·
observador`.

Los nombres internos de código pueden diferir, pero **estados, eventos, golden y
documentación funcional** usan vocabulario TM.

> Coincide con prompt v2 §10 y §5 del prompt de motor.

---

### E. LECTURA GOLDEN CERRADA (velas 1 a 9) — *resultado golden, NO regla general*

> Bloque **anti-spoiler**: esta sección es golden/ejemplo. El núcleo productivo **nunca**
> la lee. Se conserva solo para GOLDEN_CURATOR y E2E_VALIDATOR. No contiene reglas.

```
Vela 1 → 1.
Vela 2 → salida en plano; posible 2; 2 confirmado; posible 3.
Vela 3 → movimiento contrario > 50 %; 3 fallido; módulo 1-2; comienza A Grande.
Vela 4 → A Grande alcanza su máximo; comienza B Grande.
Vela 5 → continúa B Grande.
Vela 6 → B Grande 100 %; B Grande confirmada; B Grande 127 % + 0,25; AUT inmediato;
          TT pendiente (existe módulo); TT confirmado; movimiento disponible como posible 1.
Vela 7 → el movimiento continúa hasta el mínimo; termina el posible 1;
          dentro de la misma vela comienza el movimiento contrario → A Grande.
Vela 8 → desde el máximo de A Grande comienza movimiento contrario;
          B Grande; B Grande 127 % + 0,25; AUT inmediato;
          después movimiento contrario → C Grande; C Grande alcanza el final de A Grande;
          CUT confirmado.
Vela 9 → se mantienen y actualizan las lecturas todavía válidas;
          no se borran lecturas válidas por el cambio de vela.
```

> **Bloqueante activo:** la vela 8 de este golden choca con el orden intravela real de
> los ticks. Ver `CONTRADICCIONES.md` C1.

---

### F. RECLASIFICACIÓN LIVE

El motor no acierta desde el primer tick. Debe poder:
`crear candidata → actualizar → confirmar → reclasificar → integrar → invalidar →
finalizar`. **Reclasificar no significa borrar.**

- **CSV de eventos**: conserva la historia (lo que se sabía en cada tick).
- **CSV de estados**: fotografía de la clasificación vigente.

Estados permitidos: `CANDIDATA, ACTIVA, CONFIRMADA, PENDIENTE, RECLASIFICADA, INTEGRADA,
INVALIDADA, FINALIZADA`.

> Coincide con prompt v2 §10.8 y adenda v4 §4. Cierra §20.6.

---

### G. PLATAFORMA Y VALIDACIÓN (aprobado)

1. **Replay offline determinista desde CSV** = núcleo de validación (TDD).
2. Destino final = **MQL5 on-tick**, mismo orden de eventos y sin reinterpretar reglas.
3. Arquitectura: núcleo TM determinista + adaptador de replay + adaptador MQL5 OnTick.
4. **Golden** = lectura detallada, fuera del motor, sin precios ni números de vela
   cableados en la lógica.
5. Primera validación: velas 1–9. Segunda: velas 10–20.

---

## 3. REGLAS CERRADAS AÑADIDAS (dossiers v2.1 / v2.3 y adenda v4)

Estas reglas están cerradas en el dossier consolidado y **no** estaban en A–G.

- **H1 (v2.3 §5.4).** C Grande **no** termina obligatoriamente en CUT: tras A y B, C
  puede cerrar la referencia y pasar a ser **nuevo 1** del ciclo siguiente. El desenlace
  `C = nuevo 1` queda validado; la condición matemática exacta que lo consolida sigue
  pendiente (§20.7) → ver `REGLAS_PROVISIONALES.md`.
- **H2 (v2.3 §5.5).** `C = nuevo 1` pertenece a la lectura modular; `FT` pertenece a la
  lectura de patrones. Coexisten sin contradicción (planos distintos).
- **H3 (v2.3 §5.5.1 + ERROR 9A).** Al aparecer C Grande deben comprobarse tres funciones
  del mismo recorrido, en orden: (1) CUT si C supera el final de A; (2) C como nuevo 1;
  (3) C como A Grande de una referencia de lectura mayor, si existe. No se crean
  movimientos adicionales.
- **H4 (v2.3 §5.6).** El cambio de vela **no** cierra automáticamente A: A puede ocupar
  dos velas y B comenzar dentro de la segunda, confirmándose al 100 %–127 % + 0,25.
- **H5 (v2.3 §6.4).** **Doble medición Fibonacci obligatoria e independiente**:
  - retroceso de A (desde su final hacia su inicio) → **solo** confirma B;
  - expansión del módulo proyectada desde el final de A → **solo** confirma TT.
  - Prohibido mezclarlas (ERROR 5A / 5B).
- **H6 (v2.3 §11.5 / adenda v4 §2).** Con dos lecturas coherentes, cada una puede tener
  su propio autocorte; se conservan ambos y se registran por separado.
- **H7 (v4 §1).** AUT es inmediato al **superar** 127 % + 0,25 (DEC-003); **no** se usa
  `B_EXCESIVA`.

#### Decisiones del experto incorporadas como reglas cerradas (DEC-002 … DEC-005)

- **H8 (DEC-002 / DUDA-002 — estado CERRADA).** `aut_extra_points = 0.25` (fijo; 1 tick TM =
  0,25 puntos). El margen se declara así y NO se deriva del menor cambio consecutivo del CSV
  (aunque el CSV muestre incrementos de 0,10). Nivel AUT = extremo final de A Grande ±
  (1,27 · tamaño(A Grande) + 0,25). Especifica B1; cierra `CONTRADICCIONES.md` C2.
- **H9 (DEC-003 / DUDA-003 — estado CERRADA).** AUT se confirma SOLO al SUPERAR 127 % + 0,25.
  Alcanzar exactamente el 127 % no confirma AUT; alcanzar exactamente 127 % + 0,25 tampoco
  basta si la regla exige superar. Si el precio alcanza la zona y se da la vuelta sin
  superarla: B Grande continúa siendo B Grande; el movimiento contrario comienza como C Grande;
  no existe AUT. Neutraliza la hipótesis §20.16; cierra `CONTRADICCIONES.md` C3.
- **H10 (DEC-004 / DUDA-004).** Las lecturas concurrentes se nombran **lectura 1 /
  lectura 2 / lectura 3** (numeración fuera de la terminología TM, solo identificador).
  Sustituye a «local» / «superior» en la capa funcional. Rige C y D; cierra
  `CONTRADICCIONES.md` C4.
- **H11 (DEC-005 / DUDA-005).** Al abrir una vela nueva se evalúa **primero el gap**; si hay
  gap **no** se aplica la regla de 2. Formaliza §9.3; rige A4; cierra `CONTRADICCIONES.md`
  C6.

#### Decisiones del experto incorporadas como reglas cerradas (DEC-007 / DEC-008)

- **H12 (DEC-007 / ACLARACIÓN 2 + DEC-008 — estado CERRADA).** El **movimiento contrario a
  A Grande** es **B candidata** (sin confirmar) **mientras NO alcance el 100 % de A Grande**.
  Mientras esté por debajo del 100 % sigue siendo **B candidata**: **todavía NO es B Grande**.
  No escribir que «solo es B Grande» cuando alcanza el 100 %: su inicio existe antes como
  **B candidata**; el **100 % la confirma**.
- **H13 (DEC-007 / ACLARACIÓN 2 + DEC-008 — estado CERRADA).** Desde B Grande:
  (a) si **alcanza el 100 %** y **NO supera 127 % + 0,25** (`100 % ≤ recorrido ≤ 127 % + 0,25`)
  → **B Grande** (**sin AUT**);
  (b) si **estando en B Grande cambia de sentido** → **C Grande**;
  (c) si **supera 127 % + 0,25** (`recorrido > 127 % + 0,25`) → **AUT inmediato → nuevo 1 →
  se observa lo que ocurre después** (**nuevo 1** = término canónico; alias «posible 1»;
  unificación por **DEC-012**);
  (d) si después **B Grande crea un nuevo extremo** → la **C Grande se CANCELA** y
  **B Grande continúa**.

> **Por qué H12/H13 se cierran:** el experto entregó la secuencia de inicio/confirmación de
> B Grande como **definitiva** (DEC-007 / ACLARACIÓN 2 y **DEC-008**, que la **calca**). Esa
> secuencia **no figura** en la lista de reglas pendientes del control de documentos
> (`00_LEEME_PRIMERO_PRIORIDAD_DOCUMENTOS_TM.txt`, §7). No es hipótesis.

#### TABLA DE ESTADOS (memorizar) — DEC-008

| # | Situación | Estado resultante |
|---|---|---|
| 1 | Movimiento contrario a A Grande | **B candidata** |
| 2 | No alcanza el 100 % de A Grande | **B candidata** (todavía no es B Grande) |
| 3 | `100 % ≤ recorrido ≤ 127 % + 0,25` | **B Grande** (sin AUT) |
| 4 | Estando en B Grande cambia de sentido | **C Grande** |
| 5 | `recorrido > 127 % + 0,25` | **AUT inmediato → nuevo 1 → se observa lo que ocurre después** |

> **NOTA DE TERMINOLOGÍA (DEC-012).** El término canónico es **nuevo 1** (alias «posible 1»). Las
> menciones previas del experto («posible 1») se conservan en las citas literales; en la capa
> funcional se usa **nuevo 1**. Ver la constancia en `DICCIONARIO_TM.md`.

#### Decisión del experto incorporada como regla cerrada (DEC-009)

- **H14 (DEC-009 / DEC-013 / DUDA-008 — estado CERRADA).** **SALIDA EN PLANO:** la referencia es
  el **cierre de la VELA anterior** (no el cierre del movimiento anterior, **DEC-013**); si
  `|cierre de la vela anterior − apertura de la vela siguiente| ≤ 1 tick TM (0,25 puntos)` se
  considera **plano**; si es **> 1 tick** es **gap** (con gap **no** se aplica la regla de 2, **H11**).
  Umbral declarado **`plano_max_points = 0.25`**, **fijo**, **no derivado del CSV**. La referencia
  **cierre de la vela anterior** la fija **DEC-013**. Rige A1 / A4.
  Cierra **DUDA-008** y retira **PR-p** de `REGLAS_PROVISIONALES.md`.

#### Decisión del experto incorporada como regla cerrada (DEC-010)

- **H15 (DEC-010 — estado CERRADA).** **FIN DE A GRANDE — coherencia entre velas.**
  **A Grande** es el **movimiento contrario al módulo**; su **extremo se actualiza mientras el
  movimiento continúe en la vela siguiente sin volver**. El **fin de A Grande es el extremo del
  movimiento** (en la muestra, **`29.744,40`**). **No** se cierra A Grande en el **primer máximo**
  (`29.738,40`) si la **vela siguiente lo extiende** (`29.744,40`); el tramo entre ambos máximos
  **pertenece a la misma A Grande** (no crea movimiento nuevo). Tras ese extremo, el contrario
  bajista es **B Grande** y, al **superar 127 % + 0,25**, ⇒ **AUT** (H9). Rige §10.4.
  - **TENTATIVA / pendiente (NO cerrada):** la parte «y creo hace TT en esa vela» (DEC-010) queda
    como **TENTATIVA del experto**; **no** se convierte en regla cerrada. «TT» en la vela 8 queda
    **por precisar**.
  - Cierra la parte «fin de A Grande» de **C7**; **no** cierra la parte «qué módulo usa la lectura»
    de C7 (sigue abierta) ni **C1** (queda **PENDIENTE DE CONFIRMACIÓN**).

#### Decisión del experto incorporada como regla cerrada (DEC-011)

- **H16 (DEC-011 / DEC-015 — estado CERRADA).** **CONCURRENCIA DE LECTURAS.** La concurrencia es
  **habitual**: normalmente hay **2 interpretaciones simultáneas** (`lectura 1` / `lectura 2`) y,
  **excepcionalmente, 3** (`lectura 3`) si las tres siguen siendo matemáticamente válidas y
  coherentes. **No se calculan ruido ni micromovimientos**: no se clasifican, no se convierten en
  A, B, C, AUT, TT ni nuevo 1 y **no ocupan lectura**; se descartan. La permanencia se decide por
  **coherencia de movimiento**, no por cada oscilación. Las lecturas **se resuelven más adelante**;
  hay que **atender a todas** (no descartar una antes de que se resuelva). Vocabulario de las
  lecturas según **DEC-004 / H10**. Rige §10.8. Cierra la lectura de la **vela 8** (**C1**): el
  recorrido de la vela 8 es **A Grande + B Grande → AUT**; **NO** hay **C Grande** ni **CUT** en la
  vela 8.
  - **NOTA (golden, fuera del motor):** la entrada del golden que afirmaba «C Grande → CUT en vela
    8» queda **pendiente de corrección del golden**; **NO** se toca el golden ahora y **NO** se
    mueve **CUT**.

- **H17 (DEC-011 — estado PROVISIONAL, NO cerrada).** **MÓDULO POR DESCARTE.** Cuando **no hay
  módulo claro**, puede tomarse la **vela anterior** (p. ej. la **vela 7**) como **módulo por
  descarte**, con su **A Grande contraria**. **No** se cierra como regla general: la regla general
  del módulo sigue **PARCIAL** (ver **C7 / DUDA-009**). No crear test hasta cerrarla.

---

## 4. TABLA DE RECONCILIACIÓN — prompt v2 §10 ↔ A–G

| Prompt v2 §10 | Reglas A–G | Estado |
|---|---|---|
| §10.1 Movimientos y velas | (nuevo) BASE-1…BASE-6 | **AÑADIDA** como base |
| §10.2 1, 2, 3 | A1, A4 | Coincide; completado con las 4 condiciones de §4.2 y el orden gap↔2 (DEC-005) |
| §10.3 Módulo | A2 | Coincide |
| §10.4 A Grande y B Grande | (implícito en B / A3) | Coincide; completado con H4 |
| §10.5 AUT | B1, B2, H8, H9 | Coincide; C2/C3 **resueltas** por DEC-002/DEC-003 |
| §10.6 TT | A3, B3 | Coincide |
| §10.7 C Grande y CUT | B4 | Coincide; completado con H1/H2/H3 y H9 |
| §10.8 Concurrencia | C, F, H10 | Coincide; C4 **resuelta** por DEC-004 |

---

## 5. CONFLICTOS DETECTADOS

Todos los conflictos entre fuentes, con su marca BLOQUEANTE / NO BLOQUEANTE, viven en
`CONTRADICCIONES.md` (C1–C10). Ninguno se resuelve por suposición en este archivo.

**Resueltas por decisión del experto:** C1 (**DEC-011 / H16**), C2 (DEC-002), C3 (DEC-003), C4
(DEC-004), C6 (DEC-005), C8/C1b (**DEC-011**). **Parcial:** C7 (fin de A Grande CERRADO por
DEC-010/H15; **módulo PARCIAL** — módulo por descarte PROVISIONAL H17, DUDA-009 pendiente).

---

## 6. TRAZABILIDAD REGLA → DECISIÓN

| Regla TM | Apartado dossier | Decisión | Artefacto |
|---|---|---|---|
| Medida de 1 y 2 | §4.2, §20.15 | A1 | `src/core/engine.js` |
| Orden gap ↔ regla de 2 | §9.3 | A4 / H11 (DEC-005) | `src/core/engine.js` |
| Rango del módulo | §7.2, §20.1 | A2 | `src/core/engine.js` |
| Proyección TT | §7.2 | A3 | `src/core/engine.js` |
| Nivel AUT (unidad) | §6.3, §20.16 | B1 / H8 (DEC-002) | `src/core/engine.js` |
| AUT exige superar | §10.5 | B1 / B3 / H9 (DEC-003) | `src/core/engine.js` |
| Nombre de lecturas concurrentes | §10.8 | C / D / H10 (DEC-004) | `src/core/engine.js` |
| AUT ≠ 1 | Adenda v4 §1 | B2 | `src/core/engine.js` |
| AUT + TT en la misma referencia | §7.3 | B3 | `src/core/engine.js` |
| CUT | §6.2 | B4 | `src/core/engine.js` |
| C = nuevo 1 | v2.3 §5.4 | H1 | `src/core/engine.js` |
| Doble Fibonacci | v2.3 §6.4 | H5 | `src/core/engine.js` |
| Límite de lecturas | §11.3, Adenda v4 §2 | C | `src/core/engine.js` |
| Vocabulario | §1.1/1.2/1.7/18 | D | `src/core/engine.js` |
| Reclasificación | Adenda v4 §4 | F | `src/core/engine.js` |
| Replay/golden | §19 | G | `src/replay/*`, `tests/*` |

## 7. PENDIENTE (sin regla cerrada → `REGLAS_PROVISIONALES.md`)

- Serie de precio exacta del replay (Bid/Ask/Last/punto medio).
- Momento en que un movimiento contrario queda confirmado como A/B/C Grande.
- Criterios de reclasificación de varias velas como módulo o 1 conjunto.
- Prioridad y permanencia entre lecturas concurrentes en el mismo tick.
- Reglas completas de FT.
- Condición de C Grande cuando no alcanza CUT (C = nuevo 1).
- Filtro de ruido; umbral entre movimiento TM y micromovimiento.

> Cerradas y retiradas de esta lista por decisión del experto: tolerancia de «salida en
> plano» (DEC-001), unidad del nivel AUT (DEC-002), AUT «superar» (DEC-003), nombre de
> lecturas concurrentes (DEC-004), orden gap↔regla de 2 (DEC-005).

## 8. BLOQUEANTE CERRADO (C1)

La contradicción C1 (C Grande/CUT y final de A Grande en la vela 8) queda **RESUELTA ✅** por
**DEC-011 / H16**: en la **vela 8** el recorrido es **A Grande + B Grande → AUT**; **NO** hay
**C Grande** ni **CUT** en esa vela. La entrada del golden que afirmaba «C Grande → CUT en vela 8»
queda **pendiente de corrección del golden** (no se toca ahora). Ver `CONTRADICCIONES.md` C1.
