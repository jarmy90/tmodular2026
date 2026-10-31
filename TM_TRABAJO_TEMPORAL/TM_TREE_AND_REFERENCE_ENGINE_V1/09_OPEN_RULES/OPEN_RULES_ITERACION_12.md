# REGLAS ABIERTAS — ITERACIÓN 12

Sustituye a `OPEN_RULES_ITERACION_11.md` como referencia vigente.

---

## 1. CANON (cerrado en la iteración 12)

| Id | Regla | Fuente |
|---|---|---|
| P-CYCLE-01 | TT 100 % cierra el ciclo; el movimiento que lo confirma/extiende ES el nuevo 1 | Decisión 12.1 |
| P-CYCLE-02 | La pregunta por 2 se abre al comenzar la vela siguiente al nuevo 1 | Decisión 12.1 |
| P-CYCLE-03 | Con TT pendiente no se abre estructura nueva (prioridad absoluta) | v2.7 B |
| P-CYCLE-04 | Gap en esa apertura → 2 prohibido y rama de gap | v2.19 |
| P-CYCLE-05 | Cola inicial > 0,25 → 2 prohibido y rama de módulo/A | v2.13 |
| P-CUT-01 | C > final real de A → CUT confirmado; CUT no crea nuevo 1 | Decisión 12.2 |
| P-CUT-02 | C posteriormente > base del módulo → C usada como tendencia → nuevo 1 | v2.17 / Decisión 12.2 |
| P-FT-01 | Antes del 100 % de TT no existe FT | Decisión 12.3 |
| P-FT-02 | FT se origina en el extremo REAL del TT, no en el nivel del 100 % | Decisión 12.3 |
| P-FT-03 | FT es patrón: nunca es función activa y no altera la autoridad del ciclo | Decisión 12.3 |
| P-BG-01..05 | B Grande / límite inclusivo / AUT / nuevo 1 desde B / archivo de autoridades | v2.4-v2.18 |
| P-TT-01..04 | objetivo, confirmación en el tick, árbitro, extensión | v2.6-v2.7 |
| P-GAP-01..03 | A/B/tendencia implícitas, sin precios inventados | v2.19 |

## 2. PROVISIONAL_EXECUTABLE_POLICY

### P-AB-05 — Autonomía del retorno (62 pruebas)

```text
PROVISIONAL_EXECUTABLE_POLICY
```

A/B/C/FT se confirman por extensión del propio extremo con el filtro de 2 puntos como mínimo
estructural. El árbol exige además evaluación funcional (claridad, continuidad, autonomía,
absorción) que no es computable con las reglas cerradas actuales. **No es canon.**

## 3. OPEN_RULE_BLOCK

### Q-CUT — reset posterior a CUT

La condición de CUT está cerrada; la secuencia posterior está `PENDIENTE_JAVIER`. El intérprete
registra `CUT_CONFIRMED` y sigue con C viva hasta la base del módulo. No inventa reset.

### Q-CONCURRENCY — apertura de lectura secundaria

No existe regla que autorice al motor abrir L2 por sí mismo. `CompositeReader` sólo compone
lecturas suministradas externamente.

### Q-FT-VARS — capa operativa

Las variables no crean, cancelan ni reclasifican FT. Su definición queda fuera de alcance.

## 4. Estado

```text
TREE_STATUS:              NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_STATUS:  REFERENCE_ENGINE_INCOMPLETE
PATTERN_ENGINE_STATUS:    PATTERN_ENGINE_INCOMPLETE
```

Pruebas: 132 total · 69 CANONICAL_PASS · 62 PROVISIONAL_POLICY_PASS · 1 OPEN_RULE_BLOCK.
