# REGLAS ABIERTAS — ITERACIÓN 13

Vigente tras el patch v2.20. Sustituye a `OPEN_RULES_ITERACION_12.md`.

---

## 1. Cerrado en esta iteración

| Id | Regla | Estado |
|---|---|---|
| P-PLANO-01 | `< 0,25` plano · `>= 0,25` no plano · 0,25 exactos NO es plano | CERRADO (patch v2.20 A) |
| P-CUT-01 | C > final real de A → CUT; no crea nuevo 1, no resetea, C sigue viva | CERRADO (v2.20 B) |
| P-CUT-02 | C > base del módulo → C usada como tendencia → nuevo 1 | CERRADO (v2.20 B) |
| P-CYCLE-06 | `cycle_closed_at_tt` (causal) ≠ `cycle_rotation_committed_at` (apertura siguiente) | CERRADO (v2.20 C) |
| P-METRIC-01 | No llamar «ciclos» a las rotaciones | CERRADO (v2.20 D) |

`Q-CUT` deja de existir como regla abierta.

## 2. Abierto

### Q-CONCURRENCY — descubrimiento de lectura local

Bloque 3 (16:23) diverge porque el motor no abre la lectura local que la humana mantiene en
paralelo. Falta la condición que autoriza abrir L2. Hoy sólo se componen lecturas suministradas
externamente.

### Q-GAP-TT — objetivo TT después de un gap

Bloque 4 (16:25): el gap abre un nuevo 1 correctamente desde 29848,5, pero no se arma TT nuevo
porque `final_A` es implícito. Falta decidir con qué `final_A` se calcula el objetivo.

### Q-ONE-AT-CLOSE — instante de conocimiento del 1

Bloque 2 (16:19): el 1 local mide 7,5 al cierre de su vela; el motor lo confirma al abrir 16:20.

### Q-GAP-HEREDADO — gap con función viva

Gap durante B candidata, C viva o justo después de CUT: el árbol no fija resolución. El motor no
inventa (GP-04/05/06).

### Q-FT-VARS — capa operativa

Variables de FT: fuera de alcance por decisión expresa.

## 3. Provisional (no canon)

`P-AB-05` autonomía del retorno: A/B/C y la confirmación de FT (tick exacto y filtro de 2 puntos
como suficiente). 62 pruebas dependen de esta política.

## 4. Estado

```text
TREE_STATUS:              NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_STATUS:  REFERENCE_ENGINE_INCOMPLETE
PATTERN_ENGINE_STATUS:    PATTERN_ENGINE_INCOMPLETE
```

Pruebas: 145 · 79 CANONICAL_PASS · 62 PROVISIONAL_POLICY_PASS · 4 OPEN_RULE_BLOCK.
