# REGLAS ABIERTAS — ITERACIÓN 09

## Cerradas en esta iteración

### R-C-01 — C es función formal

Nace tras B Grande por movimiento estructural contrario (`>= 2,0` desde
`b_extreme`). `c_origin = b_extreme`, `c_dir = -b_dir`.
No se confirma C con el 100 % de A.

### R-C-02 — autoridad única

Al abrir C: `b_authority = ARCHIVED`, `c_authority = LIVE`,
`active_function = C`, `módulo = FROZEN_REFERENCE`. No coexisten B y C activas.

### R-C-03 — C usada como tendencia

`C_USED_AS_TREND` es `transition_reason`, no `FunctionType`. Cruce estricto de
la base del módulo → nuevo 1 con `origin/direction/structural_time` heredados
de C. Tocar la base no transforma.

### R-C-04 — extensión posterior

Solo el nuevo 1 actualiza el extremo. C queda archivada.

### R-AUT-DIRECT-PRECOND — precondición ejecutable

`AUT_DIRECT_BY_A` exige `A_CONFIRMED`. Un movimiento `CONTRARY_MOVE_PENDING`
que cruce la base produce `OPEN_RULE_BLOCK` y **no** nuevo 1.

## Política provisional

```text
PROVISIONAL_EXECUTABLE_POLICY
autonomía del retorno = dirección contraria a A + extensión de su propio extremo
```

No es regla canónica universal. Separada del total canónico en todas las
métricas. Bloquea la promoción de 58 pruebas al estatus canónico.

## OPEN_RULE_BLOCK

### CUT

No hay referencia única en el árbol para distinguir CUT de:

- C Grande;
- C usada como tendencia;
- superación del final de A;
- superación de la base del módulo.

**No se implementa.** No se inventa semántica. No bloquea ramas independientes.

### FT

Falta condición estructural cerrada para separar origen, confirmación,
extensión y autorización operativa. **No se implementa.**

### Gap con nuevo 1

Separación requerida (`NON_FLAT_OPEN_OBSERVED`, `NO_TWO_BY_NON_FLAT_OPEN`,
`GAP_IMPLICIT_TRANSITION`, `CONTINUATION_ACROSS_BAR`) especificada pero no
implementada en esta iteración.

### Concurrencia L1/L2

No implementada. Requiere `parent_reading_id` y referencias propias por lectura.

## Preguntas expertas (máximo tres)

1. **Q-CUT:** ¿cuál es la referencia única canónica de CUT, y en qué se
   distingue de “C usada como tendencia” y de la superación del final de A?
2. **Q-FT:** ¿qué condición estructural cierra la confirmación de FT sin
   recurrir a variables operativas?
3. **Q-RETURN:** ¿se promueve la autonomía del retorno (contrario + extensión
   propia) a regla canónica, o se mantiene provisional mientras no exista
   criterio funcional más fuerte?

## Estado

```text
TREE_STATUS: NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_STATUS: REFERENCE_ENGINE_INCOMPLETE
PATTERN_ENGINE_STATUS: PATTERN_ENGINE_BLOCKED
```
