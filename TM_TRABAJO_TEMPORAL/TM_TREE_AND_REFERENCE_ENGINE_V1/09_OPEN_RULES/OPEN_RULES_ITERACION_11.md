# REGLAS ABIERTAS — ITERACIÓN 11

Este archivo sustituye a `OPEN_RULES_B_GRANDE_AUT_V1.md` como referencia vigente.
Las clasificaciones se separan en tres bloques que **no se suman** entre sí.

---

## 1. CANON (regla cerrada, soportada por el árbol)

| Id | Regla | Fuente |
|---|---|---|
| P-BG-01 | B Grande al primer tick con `B >= A` | v2.4 / v2.18 |
| P-BG-02 | `100 % <= B <= 127 % + 0,25` inclusive | v2.4 |
| P-BG-03 | `B > 127 % + 0,25` → AUT en ese tick | v2.4 / v2.18 |
| P-BG-04 | Nuevo 1 desde el origen de B | v2.18 |
| P-BG-05 | Autoridades previas archivadas | v2.15 / v2.18 |
| P-AD-01 | AUT directo por A exige `A_CONFIRMED` y superación estricta de la base del módulo | v2.18 |
| P-C-01 | C Grande sólo después de B Grande | v2.17 |
| P-C-02 | C > base del módulo → C usada como tendencia → nuevo 1 | v2.17 |
| P-CUT-01 | C > final real de A → CUT confirmado | v2.13 §6 |
| P-TT-01 | `OBJETIVO_TT_100 = final_A ± tamaño_módulo` | v2.6 |
| P-TT-02 | TT se confirma en el primer tick que alcanza el objetivo | v2.6 / v2.7 |
| P-TT-03 | Árbitro cronológico objetivo vs final_A | v2.7 |
| P-TT-04 | TT confirmado puede extenderse hasta su extremo real | v2.6 D |
| P-GAP-01 | Gap → A/B Grande/A tendencia implícitas → nuevo 1 desde la apertura | v2.19 |
| P-GAP-02 | Sin precios internos ni ticks simulados en el gap | v2.19 C |
| P-GAP-03 | Prohibido medir el gap como una única A desde el extremo previo | v2.19 F |

## 2. PROVISIONAL_EXECUTABLE_POLICY (no canon)

### P-AB-05 — Autonomía del retorno

```text
PROVISIONAL_EXECUTABLE_POLICY
```

La secuencia `recorrido contrario + extensión de su propio extremo → A_CONFIRMED / B_CANDIDATE`
es una política **ejecutable provisional**. El árbol (v2.16) prohíbe un umbral universal y exige
evaluar posición, claridad, continuidad, autonomía y absorción posterior. El 2,0 sólo separa ruido
físico de movimiento estructural potencial; no confirma por sí solo.

Afecta a: A-*, BG-*, AD-*, C-*. Se contabiliza aparte del canon (58 pruebas).

## 3. OPEN_RULE_BLOCK (decisión humana pendiente)

### Q-CYCLE-1 — reinicio del ciclo tras el nuevo 1

Tras AUT directo, AUT por B o TT confirmado existe un nuevo 1, pero el árbol no fija qué tick
reabre la pregunta por 2. El lector se queda extendiendo el nuevo 1.

### Q-CUT — secuencia posterior a CUT

La condición de CUT está cerrada; el reset posterior no (`PENDIENTE_JAVIER`, v2.13 §6). El intérprete
registra `CUT_CONFIRMED` y emite `OPEN_RULE_BLOCK`; no inventa reset ni nuevo 1.

### Q-TT-FAIL — reapertura tras TT fallido

v2.7 D ordena «módulo por descarte + A Grande nueva», pero la medición de esa A depende de
Q-CYCLE-1. Se registra `TT_FAILED_FINAL_A_FIRST` y el bloqueo.

### Q-FT — punto decisivo FT

FT es patrón, no función. Faltan las condiciones estructurales cerradas y las variables. No se
inventa umbral.

### Q-GAP-DATA — validación empírica del gap

El feed 16:15–17:29 no contiene ningún gap ≥ 0,25. La rama v2.19 está verificada sólo con
fixtures y con el ancla canónica 16:24–16:25.

## 4. Políticas retiradas

| Id | Estado |
|---|---|
| P-AB-01 (A empieza en la vela siguiente) | `SUPERSEDED_EXPERIMENTAL_POLICY` |
| P-AB-03 (retorno exige dos ticks) | `READER_EXPERIMENTAL_POLICY_NOT_CANON` |
| P-AB-04 (salto de 4 puntos) | `REJECTED_EXPERIMENTAL_ASSUMPTION` |

## 5. Estado

```text
TREE_STATUS:              NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_STATUS:  REFERENCE_ENGINE_INCOMPLETE
PATTERN_ENGINE_STATUS:    PATTERN_ENGINE_BLOCKED
```
