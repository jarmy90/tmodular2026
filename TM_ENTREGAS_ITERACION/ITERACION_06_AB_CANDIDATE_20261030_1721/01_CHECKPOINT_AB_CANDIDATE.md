# CHECKPOINT 6 — A / RETORNO / B CANDIDATA

## 1. Alcance

Se creó `tm_reference_interpreter_v1_ab_candidate.py` sin modificar el núcleo aprobado.

Añadido:

- `CONTRARY_MOVE_PENDING`;
- `RETURN_MOVE_PENDING`;
- `ABSORBED_IN_A`;
- `ABSORBED_IN_ACTIVE_FUNCTION`;
- `A_CONFIRMED`;
- `B_CANDIDATE`;
- absorción de B por A;
- flags de B 100 %, B 127 % + 0,25 y AUT directo por A.

No implementado: B Grande, AUT por B, C, CUT, TT, FT, nuevo 1 por AUT directo y gap con nuevo 1.

## 2. Ancla 16:15–16:18

```text
módulo 29877,0 -> 29848,5 = 28,5
A        29848,5 -> 29857,6 = 9,1
retorno  29857,6 -> 29855,0
B        origin 29857,6 -> extremo 29843,0 = 14,6
```

Resultado:

```text
A_CONFIRMED una sola vez
A structural_time = 16:16:17.809
A knowledge_time  = 16:17:05.621
B_CANDIDATE
B structural_time = 16:17:05.425
B knowledge_time  = 16:17:05.621
```

B registra las fronteras 100 % y 127 % + 0,25 sin clasificar B Grande ni AUT.

## 3. Ancla L2

Se conserva el núcleo:

```text
1 = 7,5
2 = 12,3
3 = 29830,3
módulo = 19,7
```

Después:

```text
A origin = 29830,3
A extreme = 29850,8
A = 20,5
A_CONFIRMED una sola vez
AUT_DIRECT_BY_A_NOT_IMPLEMENTED
```

El cruce de la base del módulo se registra, pero no se crea nuevo 1.

## 4. Correcciones durante la implementación

1. **3 no se corta por una vibración de un tick.** A empieza en la vela siguiente al cierre de 3; 3 conserva su extremo final 29830,3.
2. **A no se confirma dos veces.** La confirmación directa y la confirmación por retorno comparten un único contador; solo la primera emite `A_CONFIRMED`.
3. **Una absorción de A por 3 devuelve el control a 3** para que 3 alcance su extremo final; no se cierra la lectura antes.
4. **Una A sin recorrido propio no reescribe el módulo**; evita alterar el módulo 1+2 por un tick posterior.

## 5. Pruebas

```text
Núcleo sobre la versión nueva: 19/19 PASS
A/B candidata:                 14/14 PASS
Total:                         33/33
Determinismo L1:               idéntico
Prefijo L1:                    consistente
```

Contratos cubiertos:

- absorción de A por extensión del módulo;
- A confirmada por retorno autónomo;
- retorno absorbido dentro de A;
- A supera la base antes de B;
- A entre velas;
- A confirma una sola vez;
- B conserva origen en A;
- tiempos estructurales y de conocimiento separados;
- ninguna B antes de A;
- ninguna confirmación repetida;
- L1 y L2;
- doble ejecución y prefijo.

## 6. Gate

```text
GATE_A_B_CANDIDATE_PASS
```

Condiciones:

- núcleo 19/19;
- A/B 14/14;
- A = 9,1 en 16:15–16:18;
- L2 conserva 1/2/3/módulo;
- sin umbral fijo de autonomía;
- sin confirmaciones repetidas;
- sin spoilers;
- doble ejecución idéntica;
- prefijos consistentes.

## 7. Límites

El gate es del intérprete de referencia, no del árbol completo.

```text
NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_INCOMPLETE
```

Pendiente:

- B Grande y AUT por B;
- C, C usada como tendencia y CUT;
- TT y FT;
- nuevo 1 por AUT directo;
- gap con nuevo 1;
- concurrencia interna e integración de módulos;
- ciclo universal de 1.

## 8. Archivos

- `05_REFERENCE_ENGINE/tm_reference_interpreter_v1_ab_candidate.py`
- `03_TRANSITION_SPECS/TM_TREE_TRANSITIONS_AB_CANDIDATE_V1.csv`
- `04_CONCEPT_TESTS/run_ab_candidate_tests.py`
- `04_CONCEPT_TESTS/AB_CANDIDATE_TEST_RESULTS.csv`
- `06_SYNTHETIC_REPLAYS/ab_state_1615_1618.json`
- `07_REAL_REPLAYS/ab_state_L2_1619_1622.json`
- `08_TREE_PYTHON_COMPARISON/AB_TREE_PYTHON_MATRIX_V1.csv`
- `09_OPEN_RULES/OPEN_RULES_AB_CANDIDATE_V1.md`

Originales intactos. No se modificó el motor oficial, R3, R5, goldens ni lecturas.
