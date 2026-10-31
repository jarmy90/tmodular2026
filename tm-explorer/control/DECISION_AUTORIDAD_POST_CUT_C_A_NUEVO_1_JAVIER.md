# DECISIÓN DE AUTORIDAD — POST-CUT: C GRANDE SE RECLASIFICA COMO NUEVO 1

**Autoridad:** Javier
**Fecha:** 2026-10-29
**Ámbito:** TM Core v0.7.5.2-R4, transición posterior a CUT
**Estado:** CERRADA — normativa

---

## 1. Regla normativa

> Cuando C Grande supera el final congelado de A y confirma CUT, la genealogía
> A-B-C queda cerrada. La C Grande completa se reclasifica como nuevo 1
> dominante desde su origen estructural. El tick CUT es su confirmación, no su
> origen.

## 2. Transición obligatoria

```
C_GRANDE
  → CUT_CONFIRMED
  → C_RECLASSIFIED_AS_NEW_1
  → NEW_1_DOMINANT
```

- `CUT` sigue siendo una función formal.
- `C_RECLASSIFIED_AS_NEW_1` es un evento de estado/genealogía, no una función
  formal adicional.
- No se abre un 1 nuevo desde el tick de CUT.

## 3. Metadatos de la lectura reclasificada

| Campo | Valor |
|---|---|
| `parent_reading_id` | lectura que cerró A-B-C con CUT |
| `owner_reading_id` | la propia lectura reclasificada |
| `structural_sequence_id` | secuencia del origen de C (= extremo de B Grande) |
| `confirmation_sequence_id` | secuencia del tick que confirma CUT |
| `knowledge_sequence_id` | secuencia en que CUT se conoce causalmente |
| `dominance_replaced_reading_id` | lectura dominante anterior reemplazada |
| `dominance_change_reason` | `CUT_CONFIRMED` |

## 4. Tratamiento de lecturas anteriores

Una lectura primaria viva que no comparte genealogía con el CUT no puede
bloquear el nuevo 1 dominante confirmado. Debe:

- conservarse históricamente (nunca borrar eventos);
- archivarse o degradarse a secundaria;
- registrar `DOMINANCE_REPLACED_BY_CUT`;
- no abrir una cuarta lectura.

Máximo global: 3 lecturas activas. Funcionamiento normal: principal dominante +
mini módulo actual.

## 5. Caso físico 16:23 (oráculos de validación, no hardcodes)

- `c_origin = b_extreme = 29852,60`
- C bajista; CUT al cruzar `a_end_frozen = 29842,80`
- `confirmation_sequence_id = 2015`
- `structural_time` = origen estructural de C
- `confirmation_time` = tick que confirma CUT
- El nuevo 1 dominante es toda la C bajista iniciada en 29852,60.

## 6. Gates

- GATE 5: sintético en ambas direcciones (A → B Grande → C → CUT → C es nuevo 1
  dominante), con archivo de lectura no relacionada, sin 1 artificial en el tick
  de CUT, máximo 3 lecturas y ninguna huérfana. → `tests/test_post_cut_gates.py`
- GATE 6: caso físico 16:23 (LR0002 → hija genealógica LR0003, origen 29852,60,
  confirmación 2015, R0001 desbloqueada). → `repro/gate_post_cut.py`

## 7. FASE B — 16:24

Con 1 bajista dominante, la apertura con gap no admite 2. La rama estructural
reproduce: A Grande contraria → B Grande → B supera la referencia funcional y
confirma AUT bajista → nuevo 1 bajista dominante extendido; TT alcista
pendiente/no alcanzado, sin TT por aproximación.

## 8. Evidencia

- `out/GATE_POST_CUT.json`
- `out/GATE_POST_CUT_EVENTS.csv`
- `out/CORE_RAW_OUTPUT.json` (16:15–17:30)
- `python/TM_CORE_PYTHON_v0752_CANONICAL_R5.py`
