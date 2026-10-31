# AUDITORÍA — ITERACIÓN 13

**Baseline:** `TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT`
**Normativa:** árbol v2.19 (intacto) + `TM_PATCH_CANONICO_v2_20_PLANO_Y_CUT.md` (nuevo, posterior)
**Fecha:** 2026-10-30

---

## 1. Correcciones documentales aplicadas

### 1.1 Frontera de plano (patch v2.20 A)

Se añade el patch como archivo **independiente** (`TM_CANON_ACTIVO/01_ARBOL/TM_PATCH_CANONICO_v2_20_PLANO_Y_CUT.md`)
para no alterar el árbol acumulado ya auditado (`94A1408A…6B17`). Regla vigente:

```text
|Open - Close_anterior| <  0,25  -> PLANO
|Open - Close_anterior| >= 0,25  -> NO PLANO -> 2 prohibido
```

El texto histórico («0,1 o 0,2 son plano») se conserva como trazabilidad. El motor ya aplicaba
esta frontera; ahora está fijada por escrito y probada en los tres puntos (GP-08/09/10).

### 1.2 Q-CUT cerrada

CUT = C supera **estrictamente** el final real de A; no crea nuevo 1, no resetea, C sigue activa.
Si después C supera **estrictamente** la base del módulo → `C_USED_AS_TREND` → nuevo 1 → rotación
general. `Q-CUT` sale de `OPEN_RULE_BLOCK`.

### 1.3 Cierre causal vs rotación administrativa

```text
cycle_closed_at_tt              = tick que confirma TT (16:19:00.100 en el ancla)
cycle_rotation_committed_at     = primer tick de la vela siguiente (16:20:00.000)
cycle_rotation_via              = TT | NEW_ONE
```

Ambos se exponen en `summary()["cycle_closure"]` y se prueban distintos (GP-11).

### 1.4 Reclasificación de las pruebas FT

| Prueba | Antes | Ahora |
|---|---|---|
| FT-01 no existe antes de TT | CANONICAL | CANONICAL |
| FT-02 origen en el extremo real | CANONICAL | CANONICAL |
| FT-04 coexiste con el ciclo nuevo | CANONICAL | CANONICAL |
| FT-05 FT no es función activa | CANONICAL | CANONICAL |
| FT-03 tick exacto de confirmación | CANONICAL | **PROVISIONAL** |
| FT-06 filtro de 2 puntos como confirmación | CANONICAL | **PROVISIONAL** |

### 1.5 Métricas de rotación (no «ciclos»)

Ver `ROTATION_AUDIT.json`:

```text
cycle_rotations                          47
cycles_closed_by_tt                       2
cycles_started_by_gap                    38
cycles_started_by_c_trend                 3
initial_cycles                            1
consecutive_rotations_no_closure          0
zero_size_new_one_deferrals               5
```

No se declara ningún «ciclo TM completo». Son **rotaciones internas** sin validar contra la
lectura humana.

---

## 2. Fase 2 — prioridad gap + estados heredados

| Prueba | Caso | Resultado | Clasificación |
|---|---|---|---|
| GP-01 | TT pendiente + gap alcanza el objetivo TT | TT confirmado en ese tick | CANONICAL |
| GP-02 | TT pendiente + gap cruza final_A | TT fallido, sin reset | CANONICAL |
| GP-03 | un tick cruza ambas fronteras | gana final_A (primera geométrica) | CANONICAL |
| GP-04 | gap durante B candidata | no se inventa resolución | OPEN_RULE_BLOCK |
| GP-05 | gap durante C | no se inventa resolución | OPEN_RULE_BLOCK |
| GP-06 | gap tras CUT y antes de la base | CUT conservado, sin reset | OPEN_RULE_BLOCK |
| GP-07 | FT del ciclo anterior tras un gap | FT sigue activo | CANONICAL |
| GP-08 | 0,24 | plano → 2 candidata | CANONICAL |
| GP-09 | 0,25 exactos | no plano → 2 prohibido | CANONICAL |
| GP-10 | 0,26 | no plano → 2 prohibido | CANONICAL |
| GP-11 | cierre causal ≠ rotación | instantes distintos | CANONICAL |
| GP-DET / GP-PRE | determinismo y prefijo | idénticos | CANONICAL |

Nota honesta: GP-04/05/06 comprueban que el motor **no inventa**. El árbol no fija qué ocurre
con un gap mientras hay B candidata, C viva o CUT recién confirmado; queda para decisión experta.

---

## 3. Fase 3 — comparación humana bloque a bloque

Comando: `python 04_CONCEPT_TESTS/run_block_comparison.py`
Salida: `HUMAN_BLOCK_COMPARISON.csv`. Las expectativas se copiaron de v005 antes de mirar el motor.

### Bloque 1 — 16:15–16:18

| Vela | Humano | Python | Divergencia |
|---|---|---|---|
| 16:15 | 1 bajista 16,2 | 1 confirmada, 1620 | ninguna |
| 16:16 | módulo por descarte; conjunto 28,5 | `BY_DISCARD_1_2`, 2850 | ninguna |
| 16:17 | A Grande 9,1 | A 910 confirmada | ninguna |
| 16:18 | AUT bajista; TT 29829,1 pendiente | AUT confirmado; TT pendiente, obj 29829,1 | ninguna |

**Primer error del bloque: ninguno.** Coincide tick a tick con la lectura humana.

### Bloque 2 — 16:19–16:22

| Vela | Humano | Python | Divergencia |
|---|---|---|---|
| 16:19 | 1 local 7,5 | 1 candidata (medida aún 0) | **timing** |
| 16:20 | 2 confirmado 12,3 | 2 confirmado 1230 | ninguna |
| 16:21 | 3 confirmado, mínimo 29830,3 | 3 = 2983030 | ninguna (el motor además abre y absorbe una A interna, sin crear función) |
| 16:22 | A 20,5 + AUT directo + nuevo 1 | A 2050 + `AUT_DIRECT_BY_A` + nuevo 1 | ninguna |

**Primer error del bloque: 16:19.** El motor confirma el 1 al abrir la vela siguiente, no al cierre.
Causa raíz: `_freeze_one` fija `one_kt` en el primer tick de la vela siguiente. Regla: el árbol
exige que la medida esté disponible cuando la información la permite; el cierre de la vela ya la
contiene. Clasificación: **PROVISIONAL** (no cambia ninguna función, sólo el instante de
conocimiento). Pregunta: ¿el 1 debe quedar medido al cierre de su vela?

### Bloque 3 — 16:22–16:24 (leído en continuidad desde 16:15)

| Vela | Humano | Python | Divergencia |
|---|---|---|---|
| 16:23 | A bajista 29850,8→29842,8; B a 29852,6 → AUT alcista; luego AUT bajista | sigue en L1: A 910, AUT de 16:18, nuevo 1 desde 29857,6 | **sí, 16:23** |
| 16:24 | A→B→AUT dentro de la vela; TT alcista no alcanzado | igual que 16:23 (sin cadena local) | **sí** |

**Primer error del bloque: 16:23**, primer tick de la vela. Causa raíz: el motor lee una sola
lectura; no descubre la lectura local que la humana mantiene en paralelo (`Q-CONCURRENCY`).
Clasificación: **OPEN**. No es un error de regla, es una capacidad ausente.

### Bloque 4 — 16:24–16:25 (leído en continuidad)

| Vela | Humano | Python | Divergencia |
|---|---|---|---|
| 16:24 | cierre 29834,5; TT alcista pendiente | L1 sin cadena local (misma causa de B3) | **sí** |
| 16:25 | gap +14,0 → nuevo 1 desde 29848,5; TT **alcista** confirmado en la vela | nuevo 1 desde **2984850** ✓, 2 prohibido ✓, pero TT sigue siendo el bajista anterior extendido | **sí, TT** |

**Primer error del bloque: 16:24** (herencia de B3) y, dentro de 16:25, **el TT**.
Causa raíz: el ciclo abierto por un gap no fija `final_A` explícito, así que no se arma un TT
nuevo. El árbol v2.19 reconoce A/B Grande/A-usada-como-tendencia **implícitas** en el gap, pero
no define con qué `final_A` implícito se calcula el objetivo TT. Clasificación: **OPEN**.

---

## 4. Fase 4 — control de las 47 rotaciones

| Causa | Nº | Comentario |
|---|---|---|
| Gap (v2.19) | 38 | gaps reales (14,00 / 1,50 / 1,50 / 0,80 / 3,60 puntos) |
| TT confirmado | 2 | cierre causal correcto |
| C usada como tendencia | 3 | cadena B→C→CUT→tendencia |
| Inicialización | 1 | primera lectura |
| Otra | 3 | nuevo 1 por AUT directo/absorción |

- **Cascadas**: 0 rotaciones consecutivas sin cierre causal intermedio.
- **Nuevo 1 de tamaño cero**: 5 aplazamientos (`ONE_ZERO_SIZE_DEFERRAL`), corregidos por la regla
  de aplazamiento (no se inventa medida).
- **Rotaciones por política provisional**: las de gap no dependen de la autonomía del retorno.
- **Ciclos archivados sin módulo/A/AUT/TT**: sí existen (los abiertos por gap puro); están
  registrados como rotaciones, no como ciclos completos.

Conclusión: **47 rotaciones internas**, no 47 ciclos TM.

---

## 5. Pruebas

```text
nucleo 19 | A/retorno/B 32 | AUT directo 17 | C/CUT 18 | gap+conc 16 | TT 12 | iter12 18 | iter13 13
TOTAL 145 PASS 145
CANONICAL_PASS 79 | PROVISIONAL_POLICY_PASS 62 | OPEN_RULE_BLOCK 4
```

## 6. Preguntas abiertas (cortas y numéricas)

1. **Bloque 2 / 16:19.** El 1 local mide 7,5 (29850,0 → 29842,5). ¿Debe quedar medido y
   confirmado **al cierre de su propia vela** 16:19, o al abrir 16:20 como hace el motor?
2. **Bloque 4 / 16:25.** Con gap de +14,0 y las funciones implícitas, ¿cuál es el `final_A` con el
   que se calcula el objetivo del TT alcista que se completa dentro de la vela?
3. **Bloque 3 / 16:23.** La lectura local (A 29850,8→29842,8; B a 29852,6; AUT) convive con la
   principal. ¿Qué condición autoriza al motor abrir esa lectura local: el retroceso desde
   29850,8, el máximo de 16:19 como referencia, o el gap textual de 16:23?

## 7. Integridad

Árbol v2.19 `94A1408A…6B17`, tickfeed `5F701BE2…C9FF`, lecturas v005 `F5D7550C…4226`: sin cambios.
Patch v2.20 añadido como archivo nuevo. Motores oficiales sin tocar.
