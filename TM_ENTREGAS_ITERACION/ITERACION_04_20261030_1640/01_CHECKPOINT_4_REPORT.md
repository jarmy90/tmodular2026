# TM — CHECKPOINT 4
## Autonomía funcional de A, 50 % inclusivo, gap sin zona muerta y relectura v4

**Fecha:** 2026-10-30
**Lector:** `blind_reader_v4_functional_autonomy.py`
**Estado:** `V4_EXPERIMENTAL` · `GENERATIONS_NOT_APPROVED` · `TREE_NOT_FROZEN`
**Originales:** árbol `94A1408A…`, tickfeed `5F701BE2…`, v005 `F5D7550C…`: intactos. `originals_modified=false`, `engine_modified=false`, `goldens_modified=false`.

---

## 1. DECISIONES APLICADAS

### Q-AUT

- B no se evalúa antes de `A_CONFIRMED`.
- El recorrido contrario nace `CONTRARY_MOVE_PENDING`.
- Si la función dominante extiende su extremo, el contrario se absorbe (`ABSORBED_IN_ACTIVE_FUNCTION`).
- Si el contrario adquiere autonomía, `A_CONFIRMED`; solo entonces se abre B.
- Sin umbral fijo de puntos. v4 usa como referencia estructural el **punto medio del movimiento dominante** o su base completa.
- `structural_time` = origen real del recorrido contrario; `knowledge_time` = tick en que cruza la referencia.

### Q-3-50

```text
retroceso <= 50 % de 2  → posibilidad de 3 conservada
retroceso >  50 % de 2  → 3 IMPOSSIBLE
50 % exacto            → válido
```

Tocar el 50 % no confirma 3; solo conserva su posibilidad. La confirmación exige recuperación y superación estricta del extremo final de 2.

### GAP

- Se elimina `GAP_MIN = 200` como autoridad.
- Toda apertura con `|Open − Close_previo| >= 0,25` prohíbe 2 y entra en la rama funcional de gap.
- No queda la zona 0,25–1,99 sin tratamiento.
- El modo `classic` se conserva solo como comparación para aislar el efecto de A.

---

## 2. REGRESIÓN PRIORITARIA L2 16:19–16:24

```text
1:       29850,0 → 29842,5 = 7,5
2:       29844,8 → 29832,5 = 10,8   CONFIRMED
3 final: 29830,3                    CONFIRMED
módulo:  29850,0 → 29830,3 = 19,7   REGULAR_1_2_3
A:       29830,3 → 29850,8 = 20,5   TREND
nuevo 1: 29830,3 → 29850,8
```

Coincide exactamente con la decisión Q2 y con el caso 16:20. El A de 4,1 y el B de 4,9 no confirman A/B: quedan absorbidos y el 3 continúa hasta 29830,3.

---

## 3. EJECUCIÓN

| Ejecución | Generaciones | Invalid | 3 sin 2 |
|---|---:|---:|---:|
| 16:15–16:24 | 1 | 0 | 0 |
| 16:25–16:48 | 12 | 0 | 0 |
| 16:49–17:29 | 28 | 0 | 0 |
| **Feed completo (gap=all)** | **44** | **0** | **0** |
| Feed completo (gap=classic) | 4 | 0 | 0 |
| L2 16:19–16:24 | 4 | 0 | 0 |

Feed completo `all`:

```text
AUT_B              1
GAP               36
A_USED_AS_TREND    4
C_USED_AS_TREND    2
OPEN               1
TOTAL             44
```

Los segmentos son ejecuciones de estado fresco, no continuaciones. La cadena autorizada es el feed completo.

### 3.1 Antes / después

| Fuente | Generaciones | Primarias | Gap | Abierta |
|---|---:|---:|---:|---:|
| v3 (P-A-B100 + gap classic) | 51 | 41 | 9 | 1 |
| v4 classic (solo A funcional) | **4** | 4 | 0 | 0 |
| v4 all (A funcional + gap sin zona muerta) | **44** | 7 | 36 | 1 |
| L2 v4 | 4 | 1 | 2 | 1 |

- **47 generaciones desaparecen** al eliminar P-A-B100 con el gap clásico (51 → 4).
- La corrección de gap **añade 40** transiciones (4 → 44).
- Neto: **−7** (51 → 44).
- L2: 1 primaria, 2 duplicadas de L1, 1 abierta. Generaciones únicas v4: **46** (44 L1 + 2 L2).

Las 44 no se aprueban. La mayoría son transiciones de gap no plano; no son 44 módulos primarios.

---

## 4. AUDITORÍA DE PROPIEDAD

`06_REGRESSION/PHASE_4_GENERATION_AUDIT.csv` (48 filas: 44 L1 + 4 L2):

```text
INVALID_THREE_WITHOUT_CONFIRMED_TWO   0
CROSS_READING_REFERENCE_LEAK          0
CROSS_GENERATION_REFERENCE_LEAK       0
STALE_FUNCTION_STATE                  0
INVALID_MODULE_EXTENSION              0
INVALID_ABSORPTION                    0
INVALID_NEW_ONE_ORIGIN                0
ERRORES TOTALES                       0
```

Clasificación L1: 7 primarias, 36 integradas por gap, 1 abierta.
L2: 1 primaria, 2 duplicadas, 1 abierta.

Absorciones registradas en el feed completo:

```text
MODULE_EXTENDED_ABSORBS_A                 55
A_CONFIRMED_BY_STRUCTURAL_MIDPOINT       745
A_CANDIDATE_AFTER_3                      730
B_100_WITHOUT_A_CONFIRMED                  0
```

---

## 5. DETERMINISMO

- Doble ejecución: 20.335 líneas idénticas, SHA-256 `66099D49B0FCA16D…A9A`.
- Prefijos 16:30, 17:00 y 17:15: 3.829, 12.265 y 16.454 líneas; coincidencia línea a línea.
- Evidencia: `06_REGRESSION/PHASE_4_DETERMINISM.json`.

---

## 6. PRIMERA REGRESIÓN [A]: 16:15–16:18

v4 ya no reproduce el AUT de 16:18 del v005.

```text
16:15  1 bajista = 16,2
16:16  2 imposible al cierre
módulo 1+2 = 28,5
A: 29848,5 → 29857,6 = 9,1
B: 29857,6 → 29836,2 = 12,3
v005: B = 135 % de A → B Grande/AUT → nuevo 1 bajista
v4:   A 9,1 < punto medio del módulo (14,25) → pendiente
      B 12,3 hace nuevo extremo del módulo → absorbido
      el 1 sigue hasta 29828,1; no hay AUT
```

No es un error de propiedad. Es la referencia de autonomía: A 9,1 es **56 % del 1** (16,2) pero **32 % del módulo 1+2** (28,5).

### Pregunta Q-AUT-REF

**MOVIMIENTO**
Estábamos en el 1 bajista 29877,0 → 29848,5 (16,2). El 2 no alcanzó el 100 % y el módulo por descarte mide 28,5. El precio subió 9,1 (A) y bajó 12,3 (B = 135 % de A).

**PREGUNTA**
¿La autonomía de A se mide contra el **1** (16,2; A = 56 %, supera el punto medio 8,1) o contra el **módulo 1+2** (28,5; A = 32 %, no supera el punto medio 14,25)?

**SI contra el 1**
A se confirma; B 12,3 → B Grande/AUT; nuevo 1 bajista en 29857,6; se conserva el ancla [A] de 16:18. El conteo sube.

**SI contra el módulo**
A se absorbe; el 1 sigue hasta 29828,1; el AUT de 16:18 queda `HUMAN_READING_SUPERSEDED_BY_LATER_UNIVERSAL_RULE`. El conteo v4 es 44.

**CASOS DESBLOQUEADOS**
16:15–16:18, el ancla [A], el conteo 4/44 y la clasificación de las 51.

---

## 7. REGLAS PARA v2.20

Preparadas en `05_TREE_REVISIONS/TREE_REVISION_v2_20_DRAFT.md`:

- `R-AUTONOMY-01`: B 100 % solo después de A_CONFIRMED.
- `R-AUTONOMY-02`: contrario pendiente; absorción si la función dominante extiende; A confirmada por referencia estructural, sin umbral fijo de puntos.
- `R-THREE-50`: ≤ 50 % conserva; > 50 % imposibilita; 50 % exacto válido.
- `R-GAP-OPEN`: toda apertura no plana prohíbe 2 y entra en la rama de gap.
- `R-AUT-REF`: **abierta** (1 vs módulo 1+2).

No se sobrescribe v2.19.

---

## 8. RECOMENDACIÓN

```text
NEEDS_EXPERT_DECISION
```

La decisión Q-AUT se aplicó y la regresión L2 es exacta. Pero la referencia 1 vs módulo cambia el ancla [A] de 16:18 y el conteo. No se congelan las 44, no se aprueban las 51 y no se toca el motor oficial.

Si Javier responde Q-AUT-REF:

1. fijar la referencia;
2. reejecutar 16:15–17:29;
3. auditar de nuevo;
4. comparar [A], [B], [C], [D];
5. preparar la matriz de pruebas.

---

## 9. LIMITACIONES

- El modo `classic` solo aísla A; no es una lectura canónica.
- `gap=all` crea una transición por cada apertura no plana; 36 de las 44 son gaps.
- El punto medio es una referencia estructural implementada, no una regla cerrada.
- La auditoría verifica propiedad, no validez semántica.
- Los segmentos no son aditivos.
