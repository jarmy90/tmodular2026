# REGISTRO DE CAMBIOS — ITERACIÓN 12

Sin tocar el árbol normativo, los goldens humanos ni los motores oficiales.

| Archivo | Acción | Motivo |
|---|---|---|
| `05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py` | MODIFIED | reinicio de ciclo, FT, CUT, extremo real TT, fin del estado sin salida `A_ABSORBED` |
| `04_CONCEPT_TESTS/run_ab_candidate_tests.py` | MODIFIED | BG-09 según P-CYCLE-03 (TT pendiente bloquea 2) |
| `04_CONCEPT_TESTS/run_direct_aut_tests.py` | MODIFIED | AD-04 idem para AUT directo |
| `04_CONCEPT_TESTS/run_iteration_10_tests.py` | MODIFIED | GAP-05: la función viva se convierte en 1 y abre 2 |
| `04_CONCEPT_TESTS/run_iteration_09_tests.py` | MODIFIED | C-10/C-12 con trazabilidad en `prev_cycle` |
| `04_CONCEPT_TESTS/run_iteration_12_tests.py` | CREATED | CR-01..07, CUT-CHAIN-01..03, FT-01..06, determinismo y prefijo |
| `04_CONCEPT_TESTS/run_full_feed.py` | MODIFIED | métricas de ciclo/AUT/TT/FT/gaps |

## Cambios semánticos

### Reinicio del ciclo

```text
antes: NEW_ONE_ACTIVE permanente (un solo ciclo en todo el feed)
ahora: TT 100 % -> tt_cycle_closed -> al abrir la vela siguiente:
       prev_cycle archiva el ciclo cerrado, el nuevo 1 pasa a ser 1 y se
       evalúa plano/gap/cola/dirección/medida para 2
       con TT pendiente NO se abre nada (v2.7 B)
```

### FT

```text
antes: inexistente
ahora: FT_POSSIBLE -> FT_CONFIRMED -> FT_EXTENDED desde el extremo REAL del TT,
       capa independiente de la función activa; sin variables operativas
```

### CUT

```text
antes: registraba la confirmación y nada más
ahora: la confirmación no crea nuevo 1, no resetea; la tendencia sólo nace al
       superar la base del módulo (fronteras distintas, trazabilidad B->C->CUT->tendencia)
```

### Fin del estado sin salida

```text
antes: A_ABSORBED sin handler -> 17.532 de 20.335 ticks congelados
ahora: _on_a_absorbed_tick extiende el módulo y reabre la pregunta contraria
       sólo desde un extremo distinto al que absorbió
```

## Corrección documental

Se retira la afirmación de la iteración 11 «el feed no contiene gaps»: el feed contiene gaps
reales (14,00 / 1,50 / 1,50 / 0,80 / 3,60 puntos). El error provenía de que el lector nunca
volvía a evaluar una apertura.

## Integridad

Árbol `94A1408A…6B17`, tickfeed `5F701BE2…C9FF`, lecturas `F5D7550C…4226`: sin cambios.
