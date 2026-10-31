# CHANGELOG — ITERACIÓN 14

## Intérprete `tm_reference_interpreter_v1_direct_aut.py`

1. `Reader.feed(tick)` público y `Reader.run()` como bucle de `feed`.
   Permite lectura en streaming y lecturas secundarias sin reejecutar todo.
2. `_confirm_one_at_close`: el 1 se confirma al cierre de su propia vela
   (`knowledge_time` = último tick de la vela). `_on_bar_close` ya no deja el 1
   pendiente hasta consumir la apertura siguiente.
3. `aut_mod_*`: el módulo integrado por el AUT (base = origen del nuevo 1) se
   guarda en campos propios; el módulo del ciclo no se reescribe, de modo que el
   TT conserva su objetivo.
4. `local_mode` (AUT local al 100 % del origen de A) y `local_probe`
   (lectura local secundaria). **Sonda apagada por defecto**: no forma parte del
   intérprete verificado.
5. Snapshot aditivo: `cycle_id`, `a_kt`, `a_origin_st`, `n_kt`,
   `aut_direct_kt`, `tt_kt`, `tt_final_a`, `one_kt`, `l2_*`.

## Pruebas

- `04_CONCEPT_TESTS/run_tick_comparison.py` (nuevo): comparación humana tick a
  tick de los cuatro bloques, con primera divergencia por bloque.
  Salidas: `TICK_COMPARISON_ITER14.csv`, `FIRST_DIVERGENCE_ITER14.csv`,
  `TICK_COMPARISON_ITER14.json`.
- `04_CONCEPT_TESTS/run_iteration_14_all.py` (nuevo): agrega las nueve suites.
  Salidas: `ITER14_TEST_RESULTS.csv`, `ITER14_TEST_RESULTS.json`.
- `run_iteration_13_tests.py`: GP-01 actualizado (doble pertenencia) y nueva
  prueba GP-12.

## Resultados generados

- `ITER14_TEST_RESULTS.csv/json` — 146 PASS, 0 FAIL.
- `TICK_COMPARISON_ITER14.csv` — 6.684 filas tick a tick.
- `FIRST_DIVERGENCE_ITER14.csv` — tres bloques sin divergencia; B3 con la
  divergencia en seq 1846.
- `HUMAN_BLOCK_COMPARISON.csv/json` — actualizados.

## No realizado

- Lectura local anidada declarada canónica.
- Descubrimiento automático de lecturas.
- Congelación del árbol.
- Motor oficial.

## Reglas TM modificadas

Ninguna.
