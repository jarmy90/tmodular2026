# TM — CHECKPOINT 2
## Relectura corregida, mapa L1/L2 y auditoría de generaciones

**Fecha:** 2026-10-30
**Estado:** `EXPERIMENTAL_HIERARCHY_V1_NOT_CANON`
**Árbol:** v2.19 intacto · revisión propuesta v2.20 en `05_TREE_REVISIONS/`
**Originales:** `originals_modified=false` · `engine_modified=false` · `goldens_modified=false`

---

## 1. QUÉ SE APLICÓ

Se aplicaron las tres decisiones del Checkpoint 1 en el lector experimental v2:

| Decisión | Implementación | Verificación |
|---|---|---|
| Q1 | L1 principal + L2 local, referencias y genealogías separadas | L2 aislado 16:19–16:24 |
| Q2 | 2 y 3 confirman en el primer tick válido y siguen actualizando su extremo final | módulo 19,7 / A 20,5 |
| Q3 | B < 100 % candidata; 100–127 % + 0,25 B Grande; > 127 % + 0,25 AUT; base del módulo no da AUT por B | 16:23 = B Grande, no AUT |

No se aplicó como canon la regla restrictiva de A (`B = 100 %` o `A > base`). Se conserva `CONTRARY_MOVE_PENDING` y se midió el intervalo entre dos gates experimentales.

---

## 2. RELECTURA COMPLETA 16:15–17:29

Mismos 20.335 ticks, 75 velas, sin huecos, sin información futura.

| Modo de autonomía de A | Generaciones | AUT_B | A_TREND | GAP | Abierta | Traza SHA-256 |
|---|---:|---:|---:|---:|---:|---|
| `b100` (conservador) | **26** | 4 | 15 | 6 | 1 | `9d0416ee760d0fdb…` |
| `bturn` (giro de B) | **26** | 4 | 15 | 6 | 1 | `8a8d1da95b4800ed…` |
| `pending` (sin autonomía) | **1** | 0 | 0 | 0 | 1 | `9875d1c1bf666f37…` |

**Hallazgo:** el número de generaciones es **invariante** al gate de A (26 en ambos). El gate cambia el `structural_time` de A, no la existencia de la transición. Sin ningún gate, todo el feed colapsa en un solo módulo de 291,9 puntos que nunca confirma A: la autonomía es necesaria, pero su instante exacto sigue abierto.

### 2.1 Corrección Q2 verificada

L2 aislado 16:19–16:24:

```text
1:       29850,0 → 29842,5 = 7,5
2:       29844,8 → 29832,5 = 10,8   CONFIRMED
3 final: 29830,3                    CONFIRMED
módulo:  29850,0 → 29830,3 = 19,7   REGULAR_1_2_3
A:       29830,3 → 29850,8 = 20,5   TREND
nuevo 1: 29830,3 → 29850,8 = 20,5
```

Coincide con la lectura humana local. El lector anterior daba 16,7 / 17,5 por congelar 2 y 3 en el tick de confirmación.

### 2.2 Corrección Q3 verificada

16:23: A = 8,0; B = 9,8 = 122,5 %; límite AUT = 10,41. La frontera B/AUT se aplica: **no hay AUT**. Pero el lector **no produce B Grande**: el tick que supera el extremo de 3 se registra como `THREE_EXTENDED_ABSORBS_AB` (extensión de 3) y el tramo posterior como **A trend**. El nuevo 1 coincide con la C trend de v005 en tick (16:24:44.788), origen (29852,6) y dirección (bajista), pero la etiqueta funcional difiere: **3/A vs B/C**. Es una contradicción entre Q2 (3 sigue actualizando su extremo) y Q3 (B al 122,5 % es B Grande), no un error de precio. La lectura v005 que clasificaba AUT queda `HUMAN_READING_SUPERSEDED_BY_LATER_UNIVERSAL_RULE`; no se modificó el árbol para reproducirla.

---

## 3. MAPA L1 / L2

Archivo: `02_MOVEMENT_ANALYSIS/PHASE_2_L1_L2_MAP.csv` (29 filas: 26 L1 + 3 L2).

| Capa | Clasificación | Filas |
|---|---|---:|
| L1 principal | `VALID_PRIMARY` | **19** |
| L1 principal | `INTEGRATED_IN_LARGER_MODULE` (gap implícito) | **6** |
| L1 principal | `VALID_PRIMARY_PENDING` (abierta al final) | **1** |
| L2 secundaria | `VALID_SECONDARY` (1 local único) | **1** |
| L2 secundaria | `INTEGRATED_IN_LARGER_MODULE` (duplicado estructural de L1) | **2** |

### 3.1 Las tres L2 no son tres lecturas nuevas

- **L2-G1** es la única generación secundaria única: 1 bajista local 29850,0 → 29842,5 (7,5), 2 de 10,8, 3 en 29830,3, módulo 19,7, A 20,5.
- **L2-G2** tiene el mismo 1 (29830,3 → 29850,8, 20,5), el mismo 3 (29852,6) y el mismo módulo (22,3) que **L1-G3**. Es la misma generación estructural, no una segunda lectura.
- **L2-G3** tiene el mismo 1 (29852,6 → 29828,1, 24,5) que **L1-G4**. Es la misma generación, no una segunda lectura.

**Generaciones únicas totales: 27** = 26 L1 + 1 L2.

### 3.2 Qué pasó con las 51 generaciones anteriores

La relectura anterior producía 51 generaciones. La corrección Q2/Q3 deja **26**. Las **25 restantes** desaparecen por dos errores del lector experimental, no por ambigüedad del árbol:

1. congelar 2 y 3 en el tick de confirmación desplazaba el módulo y el origen de A;
2. tratar B al 122,5 % como AUT creaba nuevos 1 falsos.

Clasificación agregada: `ARTIFICIAL_FRAGMENTATION_BY_READER` (25). No son `ARTIFICIAL_FRAGMENTATION` del árbol: el árbol no las autorizaba. No se reintroducen. **Limitación:** la diferencia 51 → 26 está verificada; la atribución fila a fila a Q2 y Q3 es por construcción de la regla, no por un diff individual de las 51 filas.

### 3.3 Determinismo

- Doble ejecución completa: archivo de traza idéntico, SHA-256 `5CB8354F6626B88D…F3FE`. El hash `9D0416EE…F876` del resumen es el hash canónico de estados, no el del archivo JSONL.
- Prefijos 16:30, 17:00 y 17:15: 3.829, 12.265 y 16.454 líneas; cada prefijo coincide línea a línea con el prefijo de la traza completa. Sin divergencias.
- Evidencia: `06_REGRESSION/PHASE_2_DETERMINISM.json`.

---

## 4. PRIMERA DIVERGENCIA CAUSAL

| Tick | v005 | Lector corregido | Estado |
|---|---|---|---|
| 16:19 | L1 AUT principal + L2 local 1 (7,5) | L1 continúa; L2 local 1 (7,5) | **Q1 resuelta**: dos lecturas |
| 16:20 | 2 local = 29832,5 | 2 local = 29832,5 (10,8) | coincide |
| 16:21 | 3 = 29830,3 | 3 = 29830,3 | coincide |
| 16:22 | módulo 19,7; A 20,5 | módulo 19,7; A 20,5 | **Q2 verificada** |
| 16:23 | B 9,8 = 122,5 % → AUT | sin AUT; extensión de 3 + A trend (no B Grande) | **Q3 aplicada en la frontera; etiqueta B/C vs 3/A abierta** |
| 16:24 | A/B/A trend, TT pendiente | A trend, nuevo 1, TT abierto | compatible con Q3 |

La primera divergencia ya no es un hueco del árbol: es una lectura humana sustituida por una regla universal posterior. No se corrige el árbol para acomodarla.

---

## 5. AUDITORÍA DE GENERACIONES

Para cada generación L1 se conserva: origen, extremo, función que la creó, pregunta activa, condición de confirmación, módulo, capa, autonomía, absorción y TT. El detalle está en `PHASE_2_L1_L2_MAP.csv`.

- **19 primarias**: 4 `AUT_B`, 15 `A_USED_AS_TREND` con A > módulo. Todas cruzan la base del módulo o nacen de un AUT; ninguna se aprueba solo por dirección. **Dos de ellas (L1-G3 y L1-G4) tienen la etiqueta funcional pendiente** por la contradicción Q2/Q3: la transición existe, pero no está decidido si el tramo es B Grande + C o extensión de 3 + A.
- **6 integradas por gap**: el gap resuelve A → B → A trend de forma implícita; el nuevo 1 nace de la apertura. No se inventan ticks ni se contabilizan como módulos independientes.
- **1 abierta**: el último 1 alcista (29585,1 → 29660,2, 75,1 puntos) sigue vivo al final del feed; su A contraria mide 91,5 y está en `CONTRARY_MOVE_PENDING`, con B provisional de 21,7. No se cierra por conveniencia.
- **1 secundaria única**: L2-G1.
- **0 `PENDING_EXPERT_DECISION`** por generación: las dudas restantes son de regla, no de existencia.

`A_CONFIRMATION_TIME` es el único campo global marcado `EXPERIMENTAL`: las 15 transiciones `A_USED_AS_TREND` existen con ambos gates, pero su instante exacto cambia.

---

## 6. PREGUNTAS RESTANTES

**Preguntas activas: Q-B3, Q-AUT y Q-3-50.** Q-INIT queda registrada como regla abierta, no preguntada en este checkpoint.

### Q-B3 — extensión de 3 frente a B Grande (contradicción Q2/Q3)

**MOVIMIENTO**
Estábamos en el 1 alcista 29830,3 → 29850,8 (L1-G3). El precio bajó a 29842,8 (A = 8,0), subió a 29852,6 (B = 9,8 = 122,5 % de A) superando el extremo de 3 (29850,8), y después bajó a 29829,9.

**PREGUNTA**
¿El tramo que supera el extremo de 3 es **extensión de 3** (Q2: 3 sigue actualizando su extremo) o **B Grande** (Q3: B entre 100 % y 127 % + 0,25)?

**SI extensión de 3**
El tramo posterior es A; A usada como tendencia → nuevo 1 bajista. No hay C.

**SI B Grande**
El tramo posterior es C; C usada como tendencia → nuevo 1 bajista. No hay A.

**CONSECUENCIA**
El nuevo 1 coincide en tick, origen y dirección; cambian la etiqueta funcional, la genealogía y la existencia de C. Afecta a L1-G3, L1-G4 y L2-G2.

**CASOS DESBLOQUEADOS**
16:23–16:24, la ruta B Grande → C, la ruta 3 → A y la auditoría de etiquetas de las 19 primarias.

---

### Q-AUT — condición mínima de autonomía de A

**MOVIMIENTO**
Estábamos en el 1 principal de 16:18 (29847,3 → 29832,5). El precio bajó otros 14,8 puntos y después giró con continuidad. El lector conservador confirma A solo cuando B alcanza su 100 % o A cruza la base del módulo; el lector de giro la confirma cuando B falla y gira.

**PREGUNTA**
¿Qué condición **universal y observable** confirma A como autónoma antes del 100 % de B, sin umbral fijo de puntos?

**SI se exige B = 100 % o base cruzada**
A se confirma tarde; el `structural_time` de A se desplaza; el nuevo 1 hereda un origen posterior.

**SI se admite el giro de B con filtro de ruido**
A se confirma antes; el origen del nuevo 1 es el extremo de B; el conteo de generaciones no cambia (26 en ambos).

**CASOS DESBLOQUEADOS**
Las 15 transiciones `A_USED_AS_TREND`, el `structural_time` de A y la genealogía de los nuevos 1.

---

### Q-INIT — primer 1 del feed (abierta, no preguntada en este checkpoint)

**MOVIMIENTO**
El feed comienza en 16:15:00.016. El primer lector toma el primer tramo como 1 inicial (16:15 1 bajista de 16,2). No hay vela anterior ni cierre previo dentro del feed.

**PREGUNTA**
¿El primer 1 nace en el primer tick, o en el primer tramo que cumple una condición funcional de apertura (plano/no plano, gap, cola)?

**SI primer tick**
El módulo inicial se mide desde 29877,0; la cadena relativa posterior no cambia.

**SI primer tramo funcional**
El módulo inicial puede empezar más tarde; cambia solo el primer módulo, no las 26 generaciones posteriores.

**CASOS DESBLOQUEADOS**
El ancla 16:15–16:18 y la comparación absoluta del primer módulo. Se conserva como regla abierta; no bloquea las 27 generaciones.

---

### Q-3-50 — 50 % exacto de 2

**MOVIMIENTO**
En un 3, el retroceso de 2 toca exactamente el 50 %. El árbol exige “retroceso funcional válido” pero no dice si el 50 % exacto lo conserva o lo invalida.

**PREGUNTA**
¿Tocar exactamente el 50 % de 2 conserva la posibilidad de 3 o la invalida?

**SI conserva**
3 puede confirmarse en el siguiente tick válido; el módulo sigue regular.

**SI invalida**
3 pasa a IMPOSSIBLE; el módulo se resuelve por descarte y cambia el origen de A.

**CASOS DESBLOQUEADOS**
Todos los 3 con retroceso exacto del 50 %, el módulo 1+2+3 y la matriz de pruebas de 3.

---

## 7. REGLAS ABIERTAS NO PREGUNTADAS AÚN

- **CUT**: significado funcional propio y referencia exacta.
- **FT**: condición de confirmación estructural, separada de la autorización operativa.
- **C usada como tendencia**: falta un caso puro en el feed; no se fuerza.

No bloquean el mapa de generaciones; se investigarán en la Fase B conceptual.

---

## 8. RECOMENDACIÓN

```text
NEEDS_EXPERT_DECISION
```

Motivo: la existencia y el número de generaciones están estabilizados (26 L1 + 1 L2 única = 27), pero hay una **contradicción constitucional** entre Q2 y Q3 en 16:23 (extensión de 3 vs B Grande), el `structural_time` de A sigue abierto y el 50 % exacto no está cerrado. Sin Q-B3 no se puede fijar la etiqueta de L1-G3/G4; sin Q-AUT no se puede fijar la genealogía de A; sin Q-3-50 no se puede cerrar la matriz de 3. No se congela el árbol.

Si Javier responde Q-B3, Q-AUT y Q-3-50, el siguiente paso es:

1. incorporar las respuestas a v2.20;
2. regresión completa 16:15–17:29;
3. auditoría final de las 27 generaciones;
4. matriz de pruebas de la Fase C.

---

## 9. ARCHIVOS Y HASHES

Se calculan en `10_MANIFEST/PHASE_2_MANIFEST.json` al cierre. Entradas principales:

- `01_BLIND_READINGS/BLIND_V3_GENERATIONS.csv` — 26 L1;
- `01_BLIND_READINGS/L2_1619_1624_GENERATIONS.csv` — 3 L2;
- `02_MOVEMENT_ANALYSIS/PHASE_2_L1_L2_MAP.csv` — 29 filas;
- `02_MOVEMENT_ANALYSIS/PHASE_2_SUMMARY.json`;
- `05_TREE_REVISIONS/TREE_REVISION_v2_20_DRAFT.md`;
- `05_TREE_REVISIONS/EXPERIMENTAL_POLICIES_V2.md`;
- `06_REGRESSION/PHASE_2_DETERMINISM.json`;
- este informe.

Originales: árbol `94A1408A…`, tickfeed `5F701BE2…`, v005 `F5D7550C…`, R3 `71D9A97A…`, R5 auditado `9BD1BEDB…`, R5 empaquetado `19A847C0…`: intactos.
