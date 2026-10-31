# ÁRBOL EJECUTABLE — C GRANDE (ITERACIÓN 09)

## Baseline endurecido

| Regla | Estado |
|---|---|
| AUT directo exige `A_CONFIRMED` previa | CANÓNICA |
| A pendiente que cruza la base | `OPEN_RULE_BLOCK` (no se inventa causalidad) |
| Autonomía del retorno (contrario + extensión propia) | `PROVISIONAL_EXECUTABLE_POLICY` |
| Clasificación de pruebas | CANONICAL / PROVISIONAL / OPEN_RULE_BLOCK |

El AUTo directo ya no confirma A y AUT en el mismo gesto: si el movimiento está
pendiente, emite `AUT_DIRECT_REQUIRES_A_CONFIRMED` y no crea nuevo 1.

## C Grande — función formal

```text
A Grande → B candidata → B Grande → movimiento estructural contrario → C Grande
```

C **no** es confianza, indicación, cadena de pensamiento ni patrón: es función
formal de la ontología TM.

```text
c_origin          = extremo final de B Grande
c_direction       = dirección contraria a B Grande
c_structural_time = nacimiento físico del movimiento contrario
c_knowledge_time  = primer tick con evidencia funcional suficiente
c_extreme         = extremo vivo del recorrido C
```

Al abrir C:

- B Grande queda histórica (`b_authority = ARCHIVED`);
- B pierde autoridad activa;
- el módulo continúa como referencia (`FROZEN_REFERENCE`);
- `active_function = C`.

Condición ejecutable: movimiento contrario desde `b_extreme` con
`contrario >= RETURN_MIN` (2,0 puntos). No se usa el 100 % de A para confirmar C.

## C usada como tendencia

```text
C_GRANDE → supera ESTRICTAMENTE la base del módulo → C_USED_AS_TREND → NEW_ONE
```

No es una `FunctionType` nueva: se registra `transition_reason = C_USED_AS_TREND`.

El nuevo 1 hereda:

```text
origin          = c_origin
direction       = c_direction
structural_time = c_structural_time
knowledge_time  = primer tick de superación estricta de la base
```

- tocar exactamente la base no transforma C;
- superarla mínimamente produce nuevo 1 en ese mismo tick;
- un salto sobre la base produce nuevo 1 en ese tick;
- la extensión posterior pertenece al nuevo 1, no a C.

## Verificación

```text
CORE 19 · A/B+BG 32 · AD 17 · C 14  =  82 / 82 PASS
CANONICAL 23 · PROVISIONAL 58 · OPEN_RULE_BLOCK 1
```

## Bloqueado (no inventado)

```text
CUT  → OPEN_RULE_BLOCK (sin referencia única en el árbol)
FT   → OPEN_RULE_BLOCK (falta condición estructural cerrada)
gap con nuevo 1, concurrencia L1/L2 → pendientes
```
