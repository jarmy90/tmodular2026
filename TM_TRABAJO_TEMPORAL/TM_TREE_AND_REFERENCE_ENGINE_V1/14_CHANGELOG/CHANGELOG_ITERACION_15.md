# CHANGELOG — ITERACIÓN 15

## Intérprete `tm_reference_interpreter_v1_direct_aut.py`

1. `TWO_FROZEN_AT_CLOSE`: la 2 confirmada cierra su extremo al final de su vela;
   no se extiende con ticks de la vela siguiente (v2.13/v2.14).
2. `_on_three_live_tick`: 3 extiende su extremo real hasta el cierre de su vela;
   una oscilación interna no abre A.
3. `_open_contrary`: resetea `return_*` y `aut_direct_status` en cada A nueva
   (fin de la fuga de estado y del AUT directo único por lectura).
4. `_open_b_from_return`: B candidata reabrible para una A ya confirmada tras
   absorción.
5. Regla de reanudación: una A estructural (≥ 2 puntos y ≥ 35 % del dominante)
   se completa como B; una A interna se absorbe por extensión del módulo.
6. `_confirm_a_and_open_b`: guard por estado, no por contador acumulado;
   proporción del 35 % solo en la lectura local.
7. `a_dominant`: proporción de A contra el movimiento que la origina (nuevo 1 o
   módulo).
8. Lectura local: umbral de A tras el nuevo 1 = máx(2 puntos, 35 % del nuevo 1);
   AUT directo local sin exigir A_CONFIRMED previa y con base del módulo del AUT.
9. Snapshot: `l2_*` incluye dirección y extremo del nuevo 1.

## Pruebas

- A-01 reformulada: oscilación interna de 2,0 puntos (20 % de un módulo de 1000)
  absorbida; conserva el módulo 1100 como expectativa canónica.
- `run_iteration_15_all.py`: agrega las nueve suites → `ITER15_TEST_RESULTS.csv/json`.
- `run_tick_comparison.py`: activa la lectura local y evalúa las anclas L2;
  salidas `TICK_COMPARISON_ITER15.csv/json` y `FIRST_DIVERGENCE_ITER15.csv`.

## Resultados

- 146/146 PASS (128 canónicas, 16 provisionales, 2 open_rule).
- 4/4 bloques sin divergencia en sus anclas documentadas (14/14).
- Feed completo: 37 rotaciones, 8 módulos, 2 AUT, 2 TT, 3 CUT, 1 FT.

## No realizado

- Validación tick a tick de 16:25–17:29.
- Regla general de lectura local más allá del caso documentado.
- Congelación del árbol y motor oficial.

## Reglas TM modificadas

Ninguna regla canónica. Se aplica como **provisional** la referencia orientativa
del 35 % (v2.16) en la lectura local.
