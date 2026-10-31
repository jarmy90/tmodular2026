# CHECKPOINT 9 — BASELINE ENDURECIDO + C GRANDE (ITERACIÓN 09)

Fecha: 2026-10-30
Intérprete: `tm_reference_interpreter_v1_direct_aut.py`
Versión: `TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT` (revisión 09)

## 1. Correcciones de baseline

### AUT directo — precondición canónica

```text
ANTES: A pendiente + cruce base → AUT directo (confirmaba A y AUT a la vez)
AHORA: A_CONFIRMED + cruce base → AUT directo
       A pendiente + cruce base → OPEN_RULE_BLOCK, sin nuevo 1
```

Evento `AUT_DIRECT_REQUIRES_A_CONFIRMED`. No se inventa causalidad.
`_confirm_aut_direct` ya no confirma A: si no hay confirmación previa, bloquea.

### Autonomía del retorno — política provisional

```text
PROVISIONAL_EXECUTABLE_POLICY
dirección contraria a A + extensión del propio extremo
```

Separada del total canónico. 58 pruebas dependen de ella.

### Clasificación de pruebas

```text
CANONICAL_PASS           23
PROVISIONAL_POLICY_PASS  58
OPEN_RULE_BLOCK           1  (A-04: A pendiente cruzando la base)
```

## 2. C Grande — función formal

Implementada en el intérprete:

- nace por movimiento contrario `>= 2,0` desde `b_extreme` tras B Grande;
- `c_origin = b_extreme`, `c_dir = -b_dir`, `c_st = tick del contrario`,
  `c_kt =` primer tick con evidencia;
- B queda `ARCHIVED`, C `LIVE`, módulo `FROZEN_REFERENCE`;
- no usa el 100 % de A;
- C usada como tendencia: cruce estricto de la base → nuevo 1 con
  `transition_reason = C_USED_AS_TREND`, heredando origen, dirección y
  `structural_time` de C;
- tocar la base no transforma; el salto la resuelve en el mismo tick;
- la extensión posterior pertenece al nuevo 1.

## 3. Resultados

```text
CORE ................ 19 / 19
A/B + BG ............ 32 / 32
AD (AUT directo) .... 17 / 17
C (C Grande/tend.) ... 14 / 14
TOTAL ............... 82 / 82 PASS
```

Determinismo y prefijos verificados en los cuatro bloques (T-011, T-012,
A-13, AD-DET, AD-PRE, C-DET, C-PRE).

## 4. Anclas intactas

```text
16:15–16:18  módulo 28,5 · A 9,1 · B Grande 16:18:34.125
             AUT por B 16:18:34.926 · nuevo 1 29857,6 → 29843,0
L2 16:19–16:22  1=7,5 · 2=12,3 · 3=29830,3 · módulo=19,7 · A=20,5
             AUT directo 16:22:52.576 (base 29850,0) · nuevo 1 alcista 29830,3 → 29850,8
```

## 5. Bloqueado sin invención

```text
CUT → OPEN_RULE_BLOCK
FT  → OPEN_RULE_BLOCK
gap con nuevo 1 → especificado, no implementado
concurrencia L1/L2 → no implementada
```

## 6. Gate

```text
GATE_C_GRANDE_TREND_PASS
```

- regresiones anteriores intactas: sí (82/82)
- AUT directo exige `A_CONFIRMED`: sí
- pruebas provisionales separadas: sí
- cero fugas entre vías: sí (B vacía en vía directa; C no coexiste con B)
- determinismo: sí
- prefijos: sí
- ausencia de spoilers: evaluación solo con el tick actual

## 7. Preguntas expertas

1. **Q-CUT** — referencia única canónica de CUT.
2. **Q-FT** — condición estructural de confirmación de FT.
3. **Q-RETURN** — promoción de la autonomía del retorno a regla canónica.

## 8. Estado

```text
TREE_STATUS: NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_STATUS: REFERENCE_ENGINE_INCOMPLETE
PATTERN_ENGINE_STATUS: PATTERN_ENGINE_BLOCKED
```

No se modificó el motor oficial. No se ejecutaron órdenes reales. No se
congeló el árbol.
