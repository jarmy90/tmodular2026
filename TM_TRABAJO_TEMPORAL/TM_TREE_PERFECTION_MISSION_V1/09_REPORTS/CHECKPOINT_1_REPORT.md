# TM — MISIÓN DE PERFECCIONAMIENTO FINAL DEL ÁRBOL
## CHECKPOINT 1 — LECTURA COMPLETA 16:15–17:29

**Fecha:** 2026-10-30
**Misión:** `TM_TREE_PERFECTION_MISSION_V1`
**Árbol:** `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md`
**Estado del árbol:** `WORKING_CANON_NOT_FROZEN`
**Estado del checkpoint:** `NOT_READY_TO_FREEZE`
**Gate 1:** `NEEDS_EXPERT_DECISION`

```text
tree_modified = false
engine_modified = false
goldens_modified = false
originals_modified = false
observational_only = true
```

---

## 1. MANDATO Y ENTRADAS

Mandato verificado: 22.206 bytes, 821 líneas, SHA-256
`993A597D24F16E39A1B2424E0C51003FDFF7E9C1269969047C9F81F562D06408`.

Entradas íntegras: árbol `94A1408A…`, tickfeed `5F701BE2…`, v005
`F5D7550C…`, R3 `71D9A97A…`, R5 auditado `9BD1BEDB…`, R5 empaquetado
`19A847C0…`. Manifiesto: `10_MANIFEST/INPUTS_MANIFEST.json`.

Lectura ciega: la Pasada A se ejecutó antes de consultar v005. La primera
salida se conservó con hash. Después se comparó con v005 y con los casos
canónicos 16:15–16:24.

---

## 2. RECORRIDO COMPLETO

Se procesaron **20.335 ticks**, 75 velas, sin huecos, con el lector
experimental v2 (`01_BLIND_READINGS/blind_reader_v2.py`).

| Modo | Generaciones | AUT_B | A_TREND | C_TREND | GAP | Abierta | Hash de traza |
|---|---:|---:|---:|---:|---:|---:|---|
| `b100` (A por B 100 %) | **51** | 20 | 18 | 3 | 9 | 1 | `19EB2200…F876` |
| `pending` (A sin confirmar) | **1** | 0 | 0 | 0 | 0 | 1 | `68AF32B2…4B0E` |
| `bturn` (A por giro de B) | **51** | 20 | 18 | 3 | 9 | 1 | `CF1D6246…042D` |

Doble ejecución `b100`: `19EB2200…F876` idéntico. Determinismo confirmado.

**Lectura del resultado:** las 51 generaciones **no son 51 lecturas
primarias**. Son los nuevos 1 de un instrumento de cadena única. El modo
`pending`, sin regla de autonomía de A, colapsa todo el feed en **un solo
módulo** que se extiende de 29.877,0 a 29.585,1 (291,9 puntos) y nunca
confirma A. La diferencia entre 1 y 51 no es un detalle: es exactamente el
problema de **concurrencia y escala** (Q1). El árbol limita a dos escalas
activas; el instrumento de cadena única no las separa.

### 2.1. Bloque 16:49–17:29

El bloque pendiente se procesó completo, tick a tick, sin consultar v005
(que lo marca [D]). En la cadena única produce **24 nuevos 1**:

```text
AUT_B ............. 11
A_USED_AS_TREND .... 7
GAP ................ 3
C_USED_AS_TREND .... 2
abierta ........... 1

primero: 16:49:00.813 (AUT_B, 1 bajista, origen 29.681,4)
último:  17:28:48.496 (A_USED_AS_TREND, nuevo 1 alcista, origen 29.594,4)
```

La cadena recorre 16:49–17:29 sin huecos, pero **no se valida como lectura
primaria**: hereda las divergencias D003–D009 de 16:19–16:24. El bloque
sigue ciego; no se usó ninguna lectura humana como respuesta.

---

## 3. ANCLA 16:15–16:24: v005 FRENTE AL LECTOR

| Hora | v005 [A] | v2 cadena única | v2 local desde 16:19 | Primera divergencia |
|---|---|---|---|---|
| 16:15 | 1 = 16,2 | 1 = 16,2 | — | sin divergencia |
| 16:16 | 2 = 12,6 < 16,2; módulo 28,5 | 2 = 12,6; módulo 28,5 | — | sin divergencia |
| 16:17 | A = 9,1 | A = 9,1 | — | sin divergencia |
| 16:18 | B 12,3; AUT bajista | B 12,3; AUT 16:18:34.926 | — | sin divergencia funcional |
| **16:19** | **AUT principal + 1 local 7,5** | **nuevo 1 principal 14,6; 2 imposible por gap** | **1 local 7,5** | **concurrencia L1/L2** |
| 16:20 | 2 = 12,3; confirmado | sin 2 | 2 confirma a 7,5 en 29836,1 | 2 se congela en el 100 % |
| 16:21 | 3 = 29830,3; módulo 19,7 | sin 3 | 3 = 29833,3 a las 16:20:22 | 3 se congela en la confirmación |
| 16:22 | A = 20,5; AUT en 29850,8 | A = 7,7 sobre módulo 5,5; nuevo 1 en 29838,0 | A = 17,5 sobre módulo 16,7; nuevo 1 en 29850,8 | origen de A y medida del módulo |
| 16:23 | A 8,0; B 9,8; AUT alcista | B Grande; C; CUT; C_TREND | B Grande; C; CUT; C_TREND | B/AUT en la base del módulo |
| 16:24 | A 7,3; B; AUT 29831,079 | C_TREND 16:24:44 | C_TREND 16:24:44 | propagación de 16:23 |
| 16:25 | gap 14,0; nuevo 1 29848,5 | gap 14,0; nuevo 1 29848,5 | gap 14,0; nuevo 1 29848,5 | dirección correcta; estado heredado distinto |

La secuencia 16:15–16:18 se reproduce **exactamente** con la regla propuesta
de A (A se confirma cuando B alcanza su 100 %). Es el ancla positiva del
lector. La primera divergencia aparece en **16:19**.

---

## 4. PRIMERA DIVERGENCIA CAUSAL: 16:19

```text
AUT principal bajista de 16:18:
  B = 12,3; nuevo 1 principal desde 29857,6 hasta 29843,0 (14,6).
16:19:
  abre 29848,9; máximo 29850,0; mínimo 29842,5; cierre 29845,0.
  La v005 conserva DOS lecturas:
    L1: el AUT principal sigue vigente; TT principal 29829,1 pendiente.
    L2: un 1 local bajista de 7,5 (29850,0 → 29842,5).
El lector de cadena única:
  usa el nuevo 1 principal 14,6 como único 1;
  evalúa 2 en 16:19 con gap -0,4 y lo declara imposible;
  no ve el 1 local de 7,5;
  por tanto no ve el 2 de 16:20, ni el 3 de 16:21, ni el A/AUT de 16:22.
```

**SÍNTOMA:** desaparece la secuencia local 16:19 = 1, 16:20 = 2,
16:21 = 3, 16:22 = A/AUT.

**ERROR LOCAL:** el lector no tiene dos lecturas con referencias
independientes; cada nuevo 1 reemplaza al anterior.

**ERROR CONCEPTUAL:** no representa la concurrencia L1/L2 que el árbol
ordena en v2.4, v2.5 y v2.14. OPEN-L2-01 sigue `PENDIENTE_JAVIER`.

**PROPAGACIÓN:** 16:22 nace en 29838,0 en vez de 29850,8; 16:23 no recorre
el A/B/AUT correcto; 16:24 no existe; la cadena de 51 generaciones es una
cadena de reemplazos, no una jerarquía de dos escalas.

---

## 5. SEGUNDA DIVERGENCIA: VIDA DE 2 Y 3

```text
16:20:
  2 candidata desde 29844,8.
  Alcanza el 100 % de 1 (7,5) en 29836,1 a las 16:20:14.
  Sigue bajando hasta 29832,5 al cierre.
16:21:
  mínimo 29830,3; cierre 29830,8.
La v005:
  2 = 12,3 (29844,8 → 29832,5).
  3 = 29830,3.
  Módulo local = 19,7; A de 16:22 = 20,5.
El lector v2:
  confirma 3 en 29833,3 a las 16:20:22;
  congela el módulo en 16,7 y el origen de A en 29833,3;
  A de 16:22 = 17,5.
```

**SÍNTOMA:** el módulo local mide 16,7 en vez de 19,7; el origen de A está
2,8 puntos alto; el nuevo 1 de 16:22 nace antes.

**ERROR LOCAL:** `module_1_2_3()` se ejecuta en el tick de confirmación de 3
y no vuelve a actualizar el extremo de 3 ni el origen de A.

**ERROR CONCEPTUAL:** confunde **tick de confirmación** con **extremo final
real**. El árbol dice que 3 se confirma en el primer tick que supera el
extremo de 2, pero también que A Grande nace desde el **extremo final real
de 3** (v2.15). El extremo de 2 puede seguir extendiéndose después del 100 %
y el de 3 después de la confirmación.

**PROPAGACIÓN:** cambia la medida del módulo, el objetivo TT y el punto de
nacimiento del nuevo 1; afecta a todos los módulos 1+2 y 1+2+3.

---

## 6. TERCERA DIVERGENCIA: B/AUT EN LA BASE DEL MÓDULO

```text
16:22:
  A alcista 29830,3 → 29850,8 = 20,5.
  Supera la base local 29850,0 en 0,8.
  AUT alcista; nuevo 1 alcista.
16:23:
  abre 29846,8; baja a 29842,8 (A = 8,0);
  sube a 29852,6 (B = 9,8 = 122,5 % de A).
La v005:
  B supera el inicio de A (29850,8) → AUT alcista.
El árbol v2.2/v2.18:
  100 % ≤ B ≤ 127 % + 0,25 → B Grande;
  AUT solo si B > 10,41.
```

**SÍNTOMA:** la v005 recorre un AUT alcista en 16:23 que el árbol clasifica
como B Grande; el 16:24 A 7,3/B/AUT 29831,079 no se alcanza en la rama del
lector.

**ERROR LOCAL:** el lector aplica 127 % + 0,25 y no comprueba la base del
módulo para B.

**ERROR CONCEPTUAL:** no está cerrado si la superación de la base del módulo
convierte a B en AUT antes del 127 % + 0,25, o si esa condición pertenece
solo a A usada como tendencia (v2.3 F) y a C usada como tendencia (v2.17).

**PROPAGACIÓN:** cambia la frontera B/AUT, el nuevo 1 de 16:23 y toda la
rama 16:24–16:25.

---

## 7. CONTRADICCIONES INTERNAS DEL ÁRBOL

| Nodo | Regla del árbol | Regla vigente del mandato/parche | Corrección propuesta |
|---|---|---|---|
| N-002 / N-005 | `|Δ| ≤ 0,25` = plano | `< 0,25` = plano; `0,25` exactos no es plano | usar `< 0,25` |
| N-006 | `rango_2 ≥ rango_1` como precondición | 2 candidata por plano, sin gap, sin cola y dirección; confirma al 100 % direccional | eliminar la precondición de rango |
| N-012 | `max(highs) − min(lows)` de las velas | extremos estructurales reales con propietario | sustituir la fórmula |
| N-021 | nuevo 1 después del TT al 100 % | nuevo 1 en el AUT; TT concurrente | mover el nacimiento al AUT |
| N-025 | C = nuevo 1 solo si no hay CUT; `PENDIENTE` | v2.17: C usada como tendencia al superar la base | cerrar con v2.17 |
| N-026 | FT con fórmula `PENDIENTE_JAVIER` | FT desde el extremo real del TT; confirmación por variables | definir referencia y condición |
| N-001 | 1 general `PROVISIONAL` | 1 inicial 16:15 validado; 1 de transición desde el origen del AUT | separar ambos casos |
| N-009/N-010 | retroceso 0–50 %; 3 confirmado | 50 % exacto debe investigarse | dejar el 50 % como frontera abierta |

La contradicción **N-012** es la raíz del error CE-2 (módulo 0→16 en vez de
0→10): el árbol mide el módulo por el rango bruto de las velas, exactamente
lo que el mandato prohíbe. La contradicción **N-021** es la raíz del
desplazamiento de la escalera: el árbol espera al TT para reconocer el nuevo
1, mientras que 4.5 lo confirma en el AUT.

---

## 8. REGLA UNIVERSAL PROPUESTA PARA A

La misión prohíbe umbrales fijos de autonomía (2, 6, 12, 20, 35 %). El
lector v2 aplica esta regla funcional:

```text
A nace en el extremo del módulo, en dirección contraria.
A permanece CONTRARY_MOVE_PENDING; no se confirma por tamaño.

A se confirma cuando:
  1. B alcanza el 100 % de A, o
  2. A supera estrictamente la base del módulo (A usada como tendencia).

STRUCTURAL_TIME_A = extremo del módulo donde nació A.
KNOWLEDGE_TIME_A = tick de B al 100 %, o tick de superación de la base.
```

Evidencia positiva: 16:15–16:18 se reproduce exactamente (A = 9,1; B = 12,3;
AUT 16:18:34.926). Evidencia negativa: el modo `pending`, sin esta regla,
colapsa el feed en un solo módulo y no abre ninguna A. La regla no usa
tamaño absoluto; usa la capacidad funcional de A de originar B o de superar
la base.

**Estado:** `PROPOSED_UNIVERSAL_RULE`, no canon. Requiere confirmación
expresa antes de congelar. Documento:
`05_TREE_REVISIONS/PROPOSED_REVISION_R1_A_FUNCTIONAL.md`.

---

## 9. CONCEPTOS ABIERTOS

| Concepto | Estado | Bloquea |
|---|---|---|
| Concurrencia L1/L2 y dominancia | `PENDIENTE_JAVIER` (OPEN-L2-01) | 51/16 generaciones, todo el bloque |
| Vida de 2 y 3: confirmación vs. extremo final | abierto | módulo, A, TT |
| B/AUT en la base del módulo antes del 127 % + 0,25 | abierto (v005 vs. árbol) | 16:23–16:24, 16:50, 17:18 |
| A autonomía sin umbral fijo | regla propuesta, no aprobada | toda la escalera A/B/AUT |
| FT estructural | `PENDIENTE_JAVIER` (N-026) | patrones, congelación |
| 50 % exacto en 3 | abierto | módulo 1+2 / 1+2+3 |
| CUT: referencia exacta y relación con C_TREND | árbol N-024 cerrado; falta normalizar | C / CUT |
| Inicio de lectura y 1 inicial | `PROVISIONAL` (N-001) | primer módulo |

---

## 10. CONTEO Y CLASIFICACIÓN

```text
Instrumento de cadena única: 51 nuevos 1.
  AUT_B ............. 20
  A_USED_AS_TREND ... 18
  C_USED_AS_TREND .... 3
  GAP ................ 9
  abierta al final ... 1

Lectura local 16:19–16:24: 4 nuevos 1.
  G1: 1 local 7,5; 2; 3; AUT_B 16:21:49.
  G2: nuevo 1 7,1; A_TREND 16:22:05.
  G3: nuevo 1 20,5; C_TREND 16:24:44.
  G4: nuevo 1 bajista abierto.

Lectura principal 16:15–16:18: 1 nuevo 1.
  G1: módulo 28,5; A 9,1; AUT 16:18:34.926; TT 29829,1.
```

Las 51 no se aprueban como lectura primaria. La jerarquía correcta
—cuántas son L1, cuántas L2 y cuántas se absorben— es Q1.

---

## 11. RECOMENDACIÓN

```text
NOT_READY_TO_FREEZE
```

No se congela el árbol. No se programa el motor definitivo. No se declara
la lectura de 51 generaciones como definitiva.

Motivos:

1. **Q1** decide la arquitectura de dos lecturas; sin ella, 51 y 1 son
   ambos incompletos.
2. **Q2** decide la medida del módulo y el origen de A; afecta a todos los
   módulos.
3. **Q3** decide la frontera B/AUT; afecta al encadenamiento 16:23–16:25.
4. El árbol tiene contradicciones internas vigentes (N-012, N-021, N-006,
   N-002) que impiden un árbol ejecutable sin corrección.
5. FT y el 50 % exacto siguen abiertos.

Si Javier responde Q1–Q3 y confirma la regla de A, la misión puede pasar a
Fase 2 (revisiones universales), Fase 3 (regresión) y Fase 4 (árbol
ejecutable y matriz de pruebas). La recomendación actual no es un fracaso:
es la evidencia de que el árbol aún no está listo para congelarse.

---

## 12. ARCHIVOS Y HASHES

| Archivo | Rol |
|---|---|
| `01_BLIND_READINGS/blind_reader_v2.py` | lector experimental v2 |
| `01_BLIND_READINGS/BLIND_V2_TRACE.jsonl` | traza tick a tick `b100` |
| `01_BLIND_READINGS/BLIND_V2_EVENTS.csv` | eventos `b100` |
| `01_BLIND_READINGS/BLIND_V2_GENERATIONS.csv` | 51 generaciones `b100` |
| `01_BLIND_READINGS/BLIND_V2_BAR_CLOSE.csv` | estado al cierre de vela |
| `01_BLIND_READINGS/BLIND_V2_SUMMARY.json` | resumen y hash de traza |
| `01_BLIND_READINGS/BLIND_V2_SUMMARY_pending.json` | modo sin autonomía de A |
| `01_BLIND_READINGS/BLIND_V2_SUMMARY_bturn.json` | modo A por giro de B |
| `02_MOVEMENT_ANALYSIS/PHASE_1_FIRST_DIVERGENCES.csv` | D001–D010 |
| `03_CONCEPTUAL_GAPS/TREE_CONTRADICTIONS.csv` | C001–C012 |
| `04_EXPERT_QUESTIONS/PHASE_1_EXPERT_QUESTIONS.md` | Q1–Q3 |
| `05_TREE_REVISIONS/PROPOSED_REVISION_R1_A_FUNCTIONAL.md` | regla A propuesta |
| `09_REPORTS/CHECKPOINT_1_REPORT.md` | este documento |

Los hashes completos y el manifiesto de salidas están en
`10_MANIFEST/PHASE_1_MANIFEST.json` y `10_MANIFEST/SHA256SUMS_PHASE_1.txt`.

---

## 13. INTEGRIDAD

| Comprobación | Resultado |
|---|---|
| Árbol modificado | no |
| R3 / R5 modificados | no |
| Tickfeed modificado | no |
| v005 modificada | no |
| Goldens modificados | no |
| Lector oficial modificado | no |
| Información futura | no usada en la Pasada A |
| Determinismo `b100` | `19EB2200…F876` idéntico en doble ejecución |
| Ticks procesados | 20.335 / 20.335 |
| Huecos | 0 |
| Prefijos | pendientes de la siguiente pasada |

**Limitaciones declaradas:** el lector v2 es un instrumento experimental, no
el motor oficial. La lectura de 51 generaciones es de cadena única y no
implementa todavía la jerarquía L1/L2. La comparación con v005 se hizo después
de bloquear la Pasada A. El bloque 16:49–17:29 sigue ciego: no se usó ninguna
lectura humana de ese bloque.
