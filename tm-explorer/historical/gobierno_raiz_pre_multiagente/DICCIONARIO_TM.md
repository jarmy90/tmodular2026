# DICCIONARIO TM — Definiciones operativas generales

Definiciones **generales**, válidas para cualquier instrumento y cualquier muestra.
No contienen precios, fechas, símbolo ni número de vela (política anti-spoiler). El motor
no debe leer el golden.

**Vocabulario permitido:** `1 · 2 · 3 · módulo · A Grande · B Grande · C Grande · AUT · TT ·
CUT · FT · nuevo 1 (alias posible 1) · movimiento contrario · retroceso · salida en plano · gap ·
lectura · lectura 1 · lectura 2 · lectura 3 · lectura candidata · lectura confirmada ·
lectura reclasificada · lectura integrada · lectura invalidada · lectura finalizada`.

**Vocabulario prohibido en la capa funcional:** `local · superior · estructura · giro ·
B excesiva · observador`.

Principio rector: `REGLA → MEDICIÓN → CLASIFICACIÓN`.

---

## Movimientos y referencia

### Movimiento
Recorrido direccional del precio entre dos extremos (inicio y final). Es la **unidad real**
de la TM, no la vela. Un movimiento puede compartir vela con otros o atravesar varias velas.

### Movimiento contrario
Movimiento en dirección opuesta al movimiento de referencia vigente. Un movimiento contrario
**no** ocupa automáticamente una lectura: solo crea una función TM nueva si alcanza una
referencia TM relevante.

### Retroceso
Movimiento de signo opuesto que no supera una referencia TM relevante y, por tanto,
permanece **integrado** en el movimiento activo. Todo movimiento contrario es, primero,
posible retroceso.

---

## Módulo regular

### 1
Movimiento que **inicia** el módulo y fija la dirección inicial (alcista o bajista). No
exige rango mínimo teórico. Su clasificación definitiva puede depender de los movimientos
posteriores. Para comparar su tamaño con 2 se usa el **desplazamiento direccional**, no el
`High−Low` completo.

### 2
Movimiento, en la **misma dirección** que 1, que cumple simultáneamente:
(a) rango ≥ rango de 1; (b) salida en plano respecto al cierre de 1; (c) cola de base igual a
cero. Se confirma cuando su desplazamiento direccional alcanza el tamaño de 1. Si falla
cualquier condición, 1 pasa a módulo por descarte y el movimiento contrario es A Grande.

### 3
Movimiento posterior a 2 que cumple, a la vez: (a) retroceso entre 0 % y 50 % del rango de 2;
(b) superación del extremo de 2. El "posible 3" **no** se confirma dentro de la misma vela
solo por hacer un nuevo extremo. Si el movimiento contrario supera el 50 %, **3 falla**.

### Módulo
Movimiento o conjunto de movimientos de referencia (1, 1+2, 1+2+3 o un recorrido
reclasificado) a los que se opone A Grande. Cuando 3 falla, 1 y 2 forman módulo. El rango
del módulo es el `High−Low` completo del conjunto de velas que lo forman; se conservan
máximo, mínimo, rango, velas implicadas, timestamps y lectura de origen.

### Autocorte del módulo
Referencia del módulo que, si el **movimiento contrario** la supera, confirma **AUT**; desde AUT ese movimiento puede considerarse **nuevo 1** (alias «posible 1») (DEC-007 / ACLARACIÓN 4 / DEC-012). Término **PROVISIONAL** (origen **PR-o** / **DUDA-009**); pendiente de cierre.

---

## Movimientos grandes

### A Grande
Primer movimiento contrario al módulo. Si el módulo es alcista, A Grande es bajista; si el
módulo es bajista, A Grande es alcista. Su **final** es una referencia esencial: sirve para
medir B Grande y actúa como nivel de invalidación del posible TT. Los retrocesos internos
pequeños pertenecen al mismo A Grande mientras no creen una referencia TM nueva. Puede
empezar en una vela y terminar en otra.

### B Grande
Movimiento contrario a A Grande. Se mide por el **retroceso de A Grande**, desde su final
hacia su inicio. Solo existe (se confirma) cuando alcanza la franja del **100 % a 127 % +
0,25**. Por debajo del 100 % todavía no es B Grande. No se confirma B usando la expansión del
módulo.

> Franja de B = `100 % a 127 % + 0,25`, donde **0,25 = 1 tick** (DEC-002 / DUDA-002).

> **Secuencia CERRADA (DEC-007 / ACLARACIÓN 2 + DEC-008 / H12-H13):** el movimiento contrario a
> **A Grande** comienza como **B candidata** y se confirma **B Grande** al alcanzar el **100 %**.
> `100 % ≤ recorrido ≤ 127 % + 0,25` → **B Grande (sin AUT)**; `recorrido > 127 % + 0,25` →
> **AUT inmediato → nuevo 1** (alias «posible 1»). (Ver TABLA DE ESTADOS en `REGLAS_CERRADAS.md` §3.)

### C Grande
Movimiento contrario a B Grande (y, por tanto, en la misma dirección que A Grande). Aparece
después de B Grande. Al aparecer, deben comprobarse sus funciones: **CUT** si supera el final
de A Grande; posible **nuevo 1** si se consolida; posible **A Grande** de una referencia de
lectura de mayor alcance. Puede empezar en una vela y continuar en otra.

### Movimiento contrario candidato
Movimiento contrario que aún no alcanza la referencia que le daría función TM (A, B o C
Grande). Se mantiene como candidato y se **cancela** si el movimiento de referencia crea un
nuevo extremo que lo invalida.

### Inicio no confirmado
Movimiento contrario a **A Grande** que todavía no alcanza los parámetros que lo confirmarían
como **B Grande**; es la **B Grande candidata**. Se confirma como **B Grande** al alcanzar sus
parámetros (**100 %**; y, al superar, **127 % + 0,25**). Término **PROVISIONAL** (origen **DEC-006**,
`REGLAS_PROVISIONALES.md` **PR-m**); pendiente de cierre.

### B Grande candidata
Sinónimo de **inicio no confirmado**: movimiento contrario a **A Grande** aún no confirmado como **B Grande**; se confirma al alcanzar el **100 %** (DEC-007 / ACLARACIÓN 2 / **H12**).

### B candidata
Forma corta de **B Grande candidata**: movimiento contrario a **A Grande** mientras **no alcanza el 100 %**; todavía no es B Grande (DEC-008 / **H12**).

---

## Eventos y patrones

### AUT
"A usada como tendencia". Hecho **inmediato**: se confirma en el mismo tick en que B Grande
**supera 127 % + 0,25**, donde **0,25 = 1 tick** (DEC-002 / DUDA-002). Regla general:
`Nivel AUT = B Grande en 1,27 × A Grande + 0,25 (1 tick)`.

- AUT exige **superar** el nivel, no solo **tocarlo** (DEC-003 / DUDA-003): si B Grande toca
  127 % + 0,25 y vuelve, **no** hay AUT; ese movimiento es **B Grande** y el que sube después
  es **C Grande**.
- No existe `B excesiva` por superar ese nivel. AUT **no** confirma definitivamente que el
  movimiento sea un nuevo 1, ni confirma TT: deja el TT **pendiente**.

### Nuevo 1
**(alias «posible 1».)** Movimiento que, tras **AUT**, puede considerarse candidato a **1** sin que
su función definitiva quede decidida (DEC-007 / ACLARACIÓN 4). Se confirma en el mismo instante en
que B supera 127 % + 0,25 → **AUT → nuevo 1** (**DEC-012**; también en la **lectura 2**, donde «se
pasa» = B supera 127 % + 0,25). Puede pasar a **1** o reclasificarse. Término **PROVISIONAL**
(origen **PR-o** / **DUDA-009** / **DEC-012**); pendiente de cierre.

> **CONSTANCIA DE UNIFICACIÓN (DEC-012, 2026-10-18).** A partir de esta decisión, el término TM
> canónico es **`nuevo 1`**; **`posible 1`** se conserva como **alias** en el resto de los
> documentos (`REGLAS_CERRADAS.md` **H13(c)** y TABLA DE ESTADOS, `DECISIONES_EXPERTO.md`
> **DEC-007 / ACLARACIÓN 4**, `REGLAS_PROVISIONALES.md` **PR-o**, `PREGUNTAS_PENDIENTES.md`
> **DUDA-009**). El experto usó «nuevo 1» (DEC-007 / ACLARACIÓN 4 y DEC-012). Las citas
> **literales** del experto se conservan **sin alterar**.

### TT
Patrón Tendencia-Tendencia. Requiere módulo válido. AUT lo activa. Se confirma cuando la
expansión alcanza el **100 %** del módulo proyectada desde el final de A Grande:
- TT bajista = final de A Grande − rango del módulo.
- TT alcista = final de A Grande + rango del módulo.
No se confirma TT usando el retroceso de A Grande. La expansión es una expansión, no un
retroceso.

### CUT
Se confirma cuando **C Grande alcanza el final de A Grande**. No se confirma por superar una
base cualquiera ni por el color de la vela. Debe reconstruirse C Grande y comprobar el final
exacto de A Grande.

### FT
Patrón Fin de Tendencia. **Sin TT confirmado no existe FT.** Requiere TT previo confirmado,
pérdida de velocidad después del TT y un **movimiento contrario claro**. Un micromovimiento
posterior al TT no es FT. La definición matemática exacta está pendiente.

---

## Precio de apertura / continuidad

### Salida en plano
Apertura de un movimiento **igual al cierre del anterior**: `Open(2) = Close(1)`. Con
tolerancia provisional de **±1 tick** (DEC-001). Al abrir una vela nueva se comprueba primero
gap y, si no hay gap, salida en plano. La salida en plano puede abrir el **posible 2**.

### Gap
Apertura distinta del cierre anterior. Se evalúa **antes** que la regla de 2:
- **Gap a favor de 1:** el intervalo contiene A y B implícitas; activa el posible TT (el TT
  solo se confirma al 100 %).
- **Gap contrario a 1:** el movimiento es A Grande en la dirección del gap.

---

## Lecturas y su ciclo de vida

### Lectura
Conjunto coherente de funciones TM que el motor mantiene mientras siga siendo
matemáticamente válido. Cada lectura guarda: módulo de referencia, dirección, inicio y final
de A Grande, B Grande y porcentaje alcanzado, referencia de autocorte, AUT o C Grande,
objetivo TT, final de A Grande como invalidación y estado actual. Nunca se mezclan niveles de
dos lecturas distintas.

### Lectura 1 / lectura 2 / lectura 3
Identificador de las lecturas **concurrentes** cuando coexisten dos (normal) o tres (máximo
operativo). La numeración (1, 2, 3) es un simple **identificador de orden**, fuera de la
terminología TM funcional (**DEC-004 / DUDA-004**). Sustituye a «local» / «superior» en la
capa funcional (estados, eventos, golden y documentación). Las lecturas concurrentes siguen
siendo lecturas TM completas con sus propios niveles independientes.

### Lectura candidata
Lectura creada pero aún no confirmada; puede actualizarse o cancelarse sin dejar de
registrarse.

### Lectura confirmada
Lectura cuyas condiciones matemáticas de su función actual se cumplen (p. ej. 2 confirmado,
B Grande confirmada, TT confirmado).

### Lectura reclasificada
Lectura cuya función cambia al reasignarse los movimientos (p. ej. un recorrido anterior pasa
a módulo). **Reclasificar no significa borrar**: el historial se conserva.

### Lectura integrada
Lectura absorbida por otra de referencia (p. ej. varias velas se integran como módulo o como
1 conjunto/1 compuesto).

### Lectura invalidada
Lectura que toca su nivel de invalidación y deja de ser válida. Solo se invalida por
imposibilidad matemática o por sustitución según prioridad, nunca por el cambio de vela.

### Lectura finalizada
Lectura que alcanzó una resolución matemática definitiva (p. ej. TT confirmado al 100 % o
CUT confirmado).

> Los estados de ciclo de vida son: `CANDIDATA, ACTIVA, CONFIRMADA, PENDIENTE,
> RECLASIFICADA, INTEGRADA, INVALIDADA, FINALIZADA`. No confundir con los estados de
> clasificación TM (`CONFIRMADO, PENDIENTE, NO EXISTE, FALLIDO, SIN REGLA ESCRITA`).
