# REVISIÓN DE VOCABULARIO TM — TM_VOCABULARY_REVIEWER

- **Agente:** TM_VOCABULARY_REVIEWER (Gate Cero, §5 del prompt v2)
- **Proyecto:** `C:\Users\hp\Documents\Teoria Modular\tm-explorer`
- **Norma aplicada:** `Prompt_ECC_OpenCode_TM_Aprendizaje_Experto_Orquestacion_v2.txt`, §5
  (TM_VOCABULARY_REVIEWER) y §7/§16 (vocabulario: permitido vs prohibido).
- **Fecha:** 2026-10-18
- **Alcance:** vocabulario de reglas, golden, eventos, estados y documentación funcional.
  No se revisó lógica de datos (DATA_AUDITOR) ni implementación (scaffold, sin reglas).

---

## 1. Método

1. Fijar el **vocabulario TM permitido**: `1 · 2 · 3 · módulo · A Grande · B Grande ·
   C Grande · AUT · TT · CUT · FT · movimiento contrario · retroceso · salida en plano ·
   gap · lectura · lectura candidata/confirmada/reclasificada/integrada/invalidada/finalizada`.
2. Fijar los **términos prohibidos como clasificación funcional**: `local · superior ·
   estructura · giro · B excesiva · observador` (+ variantes de código `B_EXCESIVA`,
   `BEX`, `v3_2_BEX_FIX`).
3. Barrido por regex (`\blocal\b`, `\bsuperior\b`, `estructura`, `\bgiro\b`, `excesiva`,
   `\bobservador\b`, `BEX`) sobre los 10 archivos del encargo + `src/**` + golden.
4. Clasificar cada aparición: **PERMITIDO** / **PROHIBIDO** / **PERMITIDO-solo-interno**
   (cita normativa, negación explícita, referencia a mecanismo anulado o nombre de código).
5. Distinguir **uso lingüístico** (p. ej. "superior a 1 tick") de **clasificación
   funcional** (lo único prohibido).
6. Verificar la revisión de preguntas: `PREGUNTAS_PENDIENTES.md` **no existe todavía**.

Criterio clave (`§5`/`§13`): los nombres internos de código pueden ser descriptivos,
pero **no** deben contaminar eventos TM, estados, golden ni documentación funcional.

---

## 2. Tabla por archivo

| Archivo | Término problemático | Línea / contexto | Veredicto | Corrección sugerida |
|---|---|---|---|---|
| `REGLAS_CERRADAS.md` | `B_EXCESIVA`, `v3_2_BEX_FIX` | L95–96 | PERMITIDO-solo-interno | Negación explícita ("No debe existir B_EXCESIVA") + nombre de mecanismo anulado. Conservar como cita; no introducir el término como estado/evento. |
| `REGLAS_CERRADAS.md` | `local · superior · estructura · giro · B excesiva · observador` | L158–159 | PERMITIDO-solo-interno | Declaración de **vocabulario prohibido** (§D). Es la norma, no su uso. |
| `REGLAS_CERRADAS.md` | `B_EXCESIVA` | L245 | PERMITIDO-solo-interno | Regla H7: "no se usa". Negación normativa. |
| `REGLAS_PROVISIONALES.md` | `1 compuesto` / `1 conjunto` | L45–48 | PERMITIDO-solo-interno | Variantes descriptivas del módulo 1 (no son clasificación prohibida). Opcional: unificar a "módulo (1 conjunto)" y registrar en glosario. |
| `CONTRADICCIONES.md` | `local`, `superior`, `estructura`, `giro`, `B excesiva`, `observador` | L95–98 | PERMITIDO-solo-interno | Marca C4: **cita** los términos prohibidos presentes en dossiers secundarios. Uso meta correcto. |
| `DICCIONARIO_TM.md` | `local · superior · estructura · giro · B excesiva · observador` | L12–13 | PERMITIDO-solo-interno | Declaración de vocabulario prohibido. |
| `DICCIONARIO_TM.md` | `B excesiva` | L96 | PERMITIDO-solo-interno | Negación ("No existe `B excesiva` por superar ese nivel"). |
| `AUDITORIA_DATOS.md` | — | — | SIN HALLAZGOS | Documento de datos; no contiene vocabulario funcional TM ni términos prohibidos. |
| `CRONOLOGIA_MOVIMIENTOS.md` | **`máx. local`** | **L90** (columna RETROCESO, fila `16:35:16.001`) | **PROHIBIDO** | Sustituir por vocabulario TM: `retroceso dentro de B Grande (extremo intermedio)`. Eliminar "local". |
| `tests/golden/golden_eventos_velas_1_8.json` | — | — | PERMITIDO | Eventos en vocabulario TM (`1`, `2`, `POSIBLE_2/3`, `MODULO`, `A/B/C`, `AUT`, `TT`, `CUT`). Nota: usa abreviaturas `A/B/C` en vez de `A Grande/B Grande/C Grande` (abreviatura interna aceptable; opcional documentar equivalencia). |
| `tests/golden/golden_estados_velas_1_8.json` | — | — | PERMITIDO | Estados = ciclo de vida permitido (`CONFIRMADO`, `POSIBILIDAD_VALIDA`, `PENDIENTE`, `INVALIDADO`); sin términos prohibidos. |
| `tests/golden/GOLDEN_EXPLICADO.md` | `superior`, `giro`, `estructura` | L53–54 | PERMITIDO-solo-interno | **Negación explícita** ("no 'superior', no 'giro', no 'estructura'"). Uso meta correcto. |
| `DECISIONES_EXPERTO.md` | `superior` ("superior a 1 tick") | L39 | PERMITIDO (no funcional) | Comparativo lingüístico, **no** clasificación. Opcional por higiene: "mayor que 1 tick". |
| `PREGUNTAS_PENDIENTES.md` | No existe | — | N/A | Revisión de preguntas **PENDIENTE** (ver §4). |
| `tests/harness.test.js` | `Infraestructura` | L4 | PERMITIDO | Falso positivo: "Infra**estructura**" es subcadena, no el término `estructura`. |
| `src/**` (engine, replay, golden format) | — | — | PERMITIDO | Sin términos prohibidos. Estados y vocabulario modular/patrones correctos (`VOCABULARIO_MODULAR`, `VOCABULARIO_PATRONES`, `ESTADOS`). |

---

## 3. Lista de términos prohibidos encontrados

| Término prohibido | Apariciones | Naturaleza |
|---|---|---|
| `local` | 1 | **Funcional real**: `CRONOLOGIA_MOVIMIENTOS.md` L90 (`máx. local`). → **corregir**. |
| `local` (meta) | 1 | Cita normativa en `CONTRADICCIONES.md` L95–96. → permitido-solo-interno. |
| `superior` | 1 | **Lingüístico** (comparativo) en `DECISIONES_EXPERTO.md` L39. → no es clasificación; opcional reescribir. |
| `superior` (meta) | 3 | Citas/negaciones en `CONTRADICCIONES.md` L97–98, `DICCIONARIO_TM.md` L12, `GOLDEN_EXPLICADO.md` L53. → permitido-solo-interno. |
| `estructura` | 1 (real) | `tests/harness.test.js` L4 → **falso positivo** ("Infraestructura"). |
| `estructura` (meta) | 2 | Declaración/negación en `DICCIONARIO_TM.md` L12, `GOLDEN_EXPLICADO.md` L54. → permitido-solo-interno. |
| `giro` | 0 real | Solo meta en `CONTRADICCIONES.md` L95, `GOLDEN_EXPLICADO.md` L53. → permitido-solo-interno. |
| `B excesiva` / `B_EXCESIVA` / `BEX` | 0 real | Solo negación (`REGLAS_CERRADAS.md` L95, L245; `DICCIONARIO_TM.md` L96). → permitido-solo-interno. |
| `observador` | 0 real | Solo meta en `CONTRADICCIONES.md` L95, `DICCIONARIO_TM.md` L13, `REGLAS_CERRADAS.md` L159. → permitido-solo-interno. |

**Conclusión del barrido:** **1 violación funcional real** (`máx. local`), **1 uso
lingüístico no funcional** (`superior a 1 tick`), **1 falso positivo** (`Infraestructura`).
Todo el resto son **citas normativas / negaciones / mecanismos anulados** (permitido-solo-interno).

### Términos TM usados pero fuera de la lista explícita del encargo (observación)
`autocorte`, `posible 1/2/3`, `1 conjunto/1 compuesto`, `referencia (de lectura)`.
No están en la lista de prohibidos y son términos de dossier TM; se clasifican
**PERMITIDO-solo-interno**. Recomendación: ampliar el glosario autorizado con el experto
para no dejarlos en zona gris.

---

## 4. Estado de la revisión de preguntas

- `PREGUNTAS_PENDIENTES.md` **NO existe** en `tm-explorer\` (verificado por `Test-Path`).
- Por tanto la **revisión de preguntas queda PENDIENTE** (no hay artefacto que revisar).
  > **SUPERADO por §6 (segunda pasada):** el artefacto ya existe y ha sido revisado.
  > El estado vigente de la revisión de preguntas es el de §6, no el de este §4.
- Cuando SCENE_QUESTIONER cree `PREGUNTAS_PENDIENTES.md`, TM_VOCABULARY_REVIEWER lo revisará
  contra la checklist siguiente.

### Checklist que SCENE_QUESTIONER debe cumplir (términos prohibidos)

- [ ] No usar `local`, `superior`, `estructura`, `giro`, `B excesiva`, `observador` como
      **clasificación** en ninguna pregunta, escena o campo.
- [ ] Usar solo vocabulario TM: `1 · 2 · 3 · módulo · A Grande · B Grande · C Grande · AUT ·
      TT · CUT · FT · movimiento contrario · retroceso · salida en plano · gap · lectura`
      (+ estados de lectura: candidata/confirmada/reclasificada/integrada/invalidada/finalizada).
- [ ] Separar **hechos objetivos** (ticks) de **posibilidades** (clasificación TM no confirmada).
- [ ] No presentar como hecho una clasificación no confirmada.
- [ ] No preguntar basándose solo en color, cuerpo, High-Low sin orden, cierre o apariencia.
- [ ] Respetar la plantilla obligatoria de pregunta (§7) y las escenas de movimiento (§8/§12).

---

## 5. Conclusión

**APROBADO CON CAMBIOS.**

- Vocabulario TM **correcto** en `REGLAS_CERRADAS.md`, `CONTRADICCIONES.md`,
  `DICCIONARIO_TM.md`, ambos golden JSON, `GOLDEN_EXPLICADO.md` y en `src/**`.
- **1 cambio requerido:** eliminar `máx. local` (`CRONOLOGIA_MOVIMIENTOS.md` L90) y
  sustituirlo por vocabulario TM.
- **1 cambio opcional:** reescribir "superior a 1 tick" (`DECISIONES_EXPERTO.md` L39).
- Revisión de preguntas **PENDIENTE** hasta que exista `PREGUNTAS_PENDIENTES.md`.

### Bloqueos
1. **Corrección obligatoria** de `máx. local` antes de cerrar el artefacto de cronología.
2. **Revisión de preguntas bloqueada** por ausencia de `PREGUNTAS_PENDIENTES.md`.
3. Sigue abierto **C4** (`CONTRADICCIONES.md`): falta fijar vocabulario TM autorizado para la
   segunda/tercera lectura (y para el módulo de mayor alcance) sin recurrir a los términos
   prohibidos. Afecta a concurrencia/reclasificación (capa funcional).

---

## 6. Revisión de `PREGUNTAS_PENDIENTES.md` (segunda pasada)

- **Agente:** TM_VOCABULARY_REVIEWER (segunda oleada, §6, paralelo a SCENE_QUESTIONER).
- **Fecha:** 2026-10-18.
- **Objeto revisado:** `tm-explorer\PREGUNTAS_PENDIENTES.md` — **5 dudas**
  (`DUDA-001` … `DUDA-005`), **todas BLOQUEANTES**.
- **Método:** (a) cotejo campo a campo con la plantilla exacta del **§7**; (b) barrido regex
  `\blocal\b|\bsuperior\b|\bestructura\b|\bgiro\b|excesiv|\bobservador\b|BEX`;
  (c) lectura semántica para separar **hecho objetivo** de **clasificación no confirmada**;
  (d) comprobación de no repetir la duda ya cerrada por **DEC-001**.
- Esta sección **actualiza** el estado de §4 y §5 en lo relativo a la revisión de preguntas.

### 6.1 Cumplimiento de la estructura §7

| DUDA | Estructura §7 | Observación |
|---|---|---|
| `DUDA-001` | **CUMPLE** | Todos los campos + **ESCENA C** (marcada imprescindible, §7). |
| `DUDA-002` | **CUMPLE** | Todos los campos; escenas A/B. |
| `DUDA-003` | **CUMPLE** | Todos los campos; escenas A/B. |
| `DUDA-004` | **CUMPLE** | Duda de **redacción**; campos de recorrido = «no aplica» (correcto, §7 no exige tick cuando no aplica). |
| `DUDA-005` | **CUMPLE** | Todos los campos; escenas A/B. |

Las 5 dudas incluyen, en este orden: `ID DE DUDA`, `AGENTE QUE LA ORIGINA`, `ESTADO`,
`REGLA AFECTADA`, `HECHOS OBJETIVOS` (Timestamp inicial/final, Vela o velas, Apertura,
Extremos en orden temporal, Precio final, Serie de precio usada, Movimientos reconstruidos,
Lecturas activas), `LO QUE SABEMOS POR TM` (Regla 1/2…), `LO QUE NO SABEMOS` (Punto exacto
no resuelto), `ESCENAS POSIBLES` (A/B[/C] con sus 5 subcampos), `PREGUNTA CONCRETA A JAVIER`
y `EFECTO DE LA RESPUESTA` (regla / tests / bloque). **Conforme al §7.**

### 6.2 Vocabulario prohibido (barrido regex)

| Línea | Término | Contexto | Veredicto |
|---|---|---|---|
| L3 | `estructura` | «la **estructura** exacta del §7» | **PERMITIDO (lingüístico)** — no es clasificación TM. Higiene opcional: «formato/plantilla exacta del §7». |
| L18–19 | `local · superior · estructura · giro · B excesiva · observador` | Cabecera «Prohibido: …» | **PERMITIDO-solo-interno** (declaración de vocabulario prohibido, §D). |
| L168 | `B excesiva` | «no existe `B excesiva` por superar ese nivel» | **PERMITIDO-solo-interno** (negación normativa). |
| L231 | `B excesiva` | «no existe `B excesiva`» | **PERMITIDO-solo-interno** (negación normativa). |
| L294–295 | `local · superior · estructura · giro · B excesiva · observador` | Regla 2 (D): lista de prohibidos | **PERMITIDO-solo-interno** (declaración normativa). |
| L322 | `local` / `superior` | «alternativa a «local»» / «alternativa a «superior»» | **PERMITIDO-solo-interno** (cita meta para declararlos prohibidos). |

**0 violaciones funcionales de vocabulario.** Ningún término prohibido se usa como
**clasificación**. Todas las apariciones son **meta / lingüísticas / negación normativa**.

### 6.3 Clasificación no confirmada presentada como hecho

**CUMPLE.** Las clasificaciones no confirmadas se rotulan con `posible`, `candidata(s)` o
`cancelada(s)`, y los desenlaces se colocan siempre bajo `ESCENAS POSIBLES → Clasificación TM
posible` (p. ej. `A Grande alcista candidata`, `B Grande bajista candidata`, `C Grande
candidata(s) cancelada(s)`, `posible 1`). No hay ninguna clasificación no confirmada afirmada
como hecho en `HECHOS OBJETIVOS` ni en `LO QUE SABEMOS POR TM`.

### 6.4 No repetición de la duda ya respondida (DEC-001)

**CUMPLE.** La duda cerrada por Javier — tolerancia de **salida en plano = 1 tick** (DEC-001) —
**no** se vuelve a preguntar. El encabezado lo hace explícito (L12–13). `DUDA-005` menciona
`salida en plano` solo como **contexto**; su pregunta es otra: **prioridad gap ↔ regla de 2**
(§9.3 vs §4.2), no la tolerancia.

### 6.5 Hallazgo de consistencia (no bloqueante, no vocabular)

`DUDA-005` (L348–352) usa como ejemplo la frontera **1→2** con delta **−0,80** y lo etiqueta
como **«salida en plano»** (golden `golden_estados_velas_1_8.json`, vela 2, hoy `PENDIENTE`).
Verificado en `data/velas_USTEC_2026-10-16_16-30.csv`: vela 1 `close = 29811.60`, vela 2
`open = 29810.80`, `gap = −0.80`.
Con **DEC-001** (±1 tick = ±0,25 pts), −0,80 pts = **3,2 ticks**, que **supera** la tolerancia
⇒ estrictamente **no** sería «salida en plano» (sería **gap** contrario). Recomendación **antes
de enviar**: reencuadrar ese ejemplo de `DUDA-005` para no afirmar la etiqueta `salida en plano`
de la vela 2 (o marcarla explícitamente como inconsistente con DEC-001) y revisar el ítem
pendiente del golden vela 2. **No es violación de vocabulario** ni bloqueo; es coherencia entre
`PREGUNTAS_PENDIENTES.md`, `DECISIONES_EXPERTO.md` y el golden.

### 6.6 Estado de la corrección `máx. local` (CRONOLOGIA_MOVIMIENTOS.md)

**RESUELTA — ya NO aparece.** `CRONOLOGIA_MOVIMIENTOS.md` L90 dice ahora
«**máximo intermedio**» (columna RETROCESO) y su función es «retroceso dentro de B Grande».
Barrido de `local` en **todo** el archivo: **0 apariciones**. El **bloqueo 1** de §5 queda
**cerrado**.

### 6.7 Veredicto

> **APROBADO CON CAMBIOS** (cambios **no bloqueantes**, de higiene y consistencia).
> **0 violaciones de vocabulario**; estructura **§7 conforme** en las 5 dudas; no se repite
> DEC-001; ninguna clasificación no confirmada se afirma como hecho.

- Cambio 1 (higiene, opcional): L3 `estructura` → «formato/plantilla».
- Cambio 2 (consistencia, recomendado antes de enviar): reencuadrar el ejemplo de vela 2 en
  `DUDA-005` conforme a §6.5.

### 6.8 Bloqueos

- **Vocabulario: ninguno.** No hay ningún término prohibido que deba corregirse antes de
  enviar las preguntas a Javier.
- Sigue abierto **C4** por diseño: `DUDA-004` **es** la petición de fijar el vocabulario TM
  autorizado para la segunda/tercera lectura y para la referencia de módulo de mayor alcance;
  se cierra con la respuesta del experto, no antes.

---

*Artefacto del agente TM_VOCABULARY_REVIEWER. Revisa vocabulario; no implementa reglas ni
toca el núcleo productivo. Alimenta la segunda oleada del Gate Cero.*
