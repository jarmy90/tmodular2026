# REGLAS ABIERTAS Y POLÍTICAS — ITERACIÓN 08 (AUT DIRECTO POR A)

## Políticas retiradas

### P-AB-04_RETURN_JUMP_4 — salto fijo de 4,0 puntos

```text
REJECTED_EXPERIMENTAL_ASSUMPTION
```

```text
RETURN_JUMP = RETURN_MIN × 2
salto único >= 4,0 puntos → retorno estructural confirmado
```

No es regla TM canónica y no se sustituye por otro número fijo.
`RETURN_MIN` (2,0 puntos) solo separa ruido físico de movimiento potencial.

**Estado en el código:** retirada. `return_jump` se conserva como campo
histórico y permanece siempre en `False`; nunca es autoridad.
**Pruebas afectadas:** A-14 y BG-15 quedaron reclasificadas como
`TEST_DEPENDS_ON_REJECTED_POLICY` y reescritas sin cuatro puntos.

### P-AB-01 / P-AB-03 (heredadas)

```text
P-AB-01 → SUPERSEDED_EXPERIMENTAL_POLICY
P-AB-03 → READER_EXPERIMENTAL_POLICY_NOT_CANON
```

A puede nacer dentro de la misma vela; el retorno no depende de un número
obligatorio de ticks.

## Reglas cerradas en esta iteración

### R-AUT-DIRECT-01 — superación estricta de la base

A supera `mod_origin` con `(a_extreme - mod_origin) * a_dir > 0`.
Tocar exactamente la base no dispara AUT. No se inventa tick intermedio.

### R-AUT-DIRECT-02 — nueva función sin B

En la vía directa `B` no existe: `b_status` queda vacío, `b_grande_status`
vacío y `aut_status` (vía B) vacío. No se aplica 127 % + 0,25.

### R-AUT-DIRECT-03 — propiedad del nuevo 1

```text
origin          = a_origin
direction       = a_direction
structural_time = structural_time_A
knowledge_time  = primer tick de cruce estricto
extreme         = precio del tick de AUT
```

### R-AUT-DIRECT-04 — archivado

`A = CONFIRMED_ARCHIVED`, `3 = ARCHIVED` si procedía,
`módulo = FROZEN_REFERENCE`, `active_function = NEW_ONE`.

Solo el nuevo 1 actualiza el extremo después del cruce.

### R-RETURN-AUTONOMY-01 — autonomía sin umbral fijo

El retorno confirma autonomía cuando conserva dirección contraria a A y
extiende su **propio** extremo (`return_extended`). Un salto grande de un
solo tick no confirma.

## Abierto (no implementado, no asumido)

- C Grande;
- C usada como tendencia;
- CUT;
- TT;
- FT;
- gap con nuevo 1;
- concurrencia L1/L2 e integración de módulos;
- ciclo universal de 1 (inicio/fin).

## Gates

```text
GATE_AUT_DIRECT_BY_A_PASS
```

Gate del intérprete de referencia. No congela el árbol ni autoriza motor
oficial.

```text
NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_INCOMPLETE
```
