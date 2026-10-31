# REGLAS ABIERTAS Y POLÍTICAS — B GRANDE / AUT

## Políticas sustituidas

### P-AB-01 — A empieza obligatoriamente en la vela siguiente

```text
SUPERSEDED_EXPERIMENTAL_POLICY
```

A puede nacer dentro de la misma vela del módulo o de 3. Si 3 vuelve a extenderse, A se absorbe; si A adquiere autonomía, 3 se archiva en su extremo estructural real.

### P-AB-03 — El retorno exige dos ticks

```text
READER_EXPERIMENTAL_POLICY_NOT_CANON
```

No se usa densidad de ticks. El retorno se confirma por extensión de su propio extremo o por un salto estructural único de al menos 4,0 puntos. El mínimo de 2,0 puntos solo separa ruido.

## Políticas vigentes

### P-BG-01 — B Grande al 100 %

`TREE_SUPPORTED`. Primer tick con `B >= A`; `knowledge_time_B_GRANDE` queda fijado allí.

### P-BG-02 — Límite 127 % + 0,25 inclusivo

`TREE_SUPPORTED`. `B <= límite` sigue siendo B Grande. `B > límite` es AUT en el mismo tick.

### P-BG-03 — Salto directo a AUT

`TREE_SUPPORTED`. Se registra el cruce causal de B Grande y AUT en el mismo tick. El estado final es AUT; no se inventa un tick intermedio.

### P-BG-04 — Nuevo 1 desde B

`TREE_SUPPORTED`. Origen = origen de B = extremo de A; dirección = B; structural_time = inicio estructural de B; knowledge_time = tick AUT. La extensión posterior pertenece al nuevo 1, no a B.

### P-BG-05 — Archivo de autoridades

`TREE_SUPPORTED`. A, 3 y módulo conservan datos históricos, pero pierden autoridad activa. `historical_status` y `active_authority` son campos distintos.

### P-BG-06 — AUT directo por A

`OPEN_RULE_DEPENDENCY`. Se registra el cruce de la base del módulo, pero no se crea nuevo 1 por esa vía.

## Abierto

- C;
- CUT;
- TT;
- FT;
- nuevo 1 por AUT directo de A;
- gap con nuevo 1;
- concurrencia interna e integración de módulos;
- ciclo universal de 1.

## Gate

```text
GATE_B_GRANDE_AUT_PASS
```

Es un gate del intérprete de referencia. No congela el árbol ni autoriza motor oficial.

```text
NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_INCOMPLETE
```
