# REGLAS ABIERTAS Y POLÍTICAS — A / B CANDIDATA V1

## Implementado

- CONTRARY_MOVE_PENDING;
- RETURN_MOVE_PENDING;
- ABSORBED_IN_A;
- ABSORBED_IN_ACTIVE_FUNCTION;
- A_CONFIRMED;
- B_CANDIDATE;
- absorción de B por A;
- flags de frontera B 100 % y 127 % + 0,25;
- flag AUT directo por A, sin nuevo 1.

## Políticas declaradas

### P-AB-01 — A empieza en la vela siguiente al módulo/3

`TREE_SUPPORTED`. Evita que una vibración posterior a la confirmación de 3 fragmente 3 o abra A dentro de la misma vela. El módulo/3 conserva su extremo final.

### P-AB-02 — Mínimo estructural del retorno = 2,0 puntos

`TREE_SUPPORTED_MINIMUM`. El filtro de 2 puntos separa ruido físico de movimiento potencial; no confirma A ni B por sí solo.

### P-AB-03 — Continuidad del retorno = dos ticks

`READER_OPERATIONAL_POLICY`. Es una condición de continuidad, no un umbral de autonomía. No se usa como canon ni para congelar el árbol.

### P-AB-04 — A confirma una sola vez

`TREE_SUPPORTED`. Una A absorbida antes de confirmar no crea B. Una A confirmada no se vuelve a confirmar.

### P-AB-05 — B conserva el origen en el extremo final de A

`TREE_SUPPORTED`. `extremes` y `origin` no se confunden con el tick de confirmación.

### P-AB-06 — AUT directo por A

`OPEN_RULE_DEPENDENCY`. Se registra el cruce de la base del módulo, pero no se crea el nuevo 1. Falta la transición de reset y la genealogía del nuevo 1.

## Abierto

- B Grande y AUT por B: bloqueados.
- C, CUSADA COMO TENDENCIA y CUT: bloqueados.
- TT y FT: bloqueados.
- Nuevo 1 por AUT directo: bloqueado.
- Gap con nuevo 1: bloqueado.
- Concurrencia interna L1/L2 e integración de módulos: bloqueada.
- Ciclo universal de 1: no congelado.

## Gate

`GATE_A_B_CANDIDATE_PASS` significa que el intérprete de referencia implementa y prueba A/retorno/B candidata. No significa que el árbol completo esté congelado ni que el motor oficial exista.

```text
NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_INCOMPLETE
```
