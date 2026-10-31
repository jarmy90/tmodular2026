# CHECKPOINT 7 — B GRANDE → AUT → NUEVO 1

## 1. Correcciones previas

### P-AB-01 sustituida

```text
SUPERSEDED_EXPERIMENTAL_POLICY
```

A puede nacer dentro de la misma vela del módulo o de 3. Si 3 vuelve a extenderse, A se absorbe y 3 conserva la autoridad. Si A adquiere autonomía, 3 queda archivado en su extremo estructural real. La vela no es frontera obligatoria.

### P-AB-03 no canónica

```text
READER_EXPERIMENTAL_POLICY_NOT_CANON
```

Se eliminó `return_ticks >= 2`. El retorno se confirma por extensión de su propio extremo o por un salto estructural único de al menos 4,0 puntos. El mínimo de 2,0 puntos solo separa ruido.

### T-001

La descripción decía `10000->9600` con size 200. La medida física de ese tramo sería 400. El fixture correcto es `10000->9800` (size 200); el segundo tramo pertenece a la vela siguiente. Se corrigió la descripción y **no** la expectativa. Documento: `04_CONCEPT_TESTS/T001_CORRECTION.md`.

## 2. B Grande y AUT

```text
B < 100 % de A          → B_CANDIDATE
B >= 100 % de A         → B_GRANDE
B <= 127 % de A + 0,25  → B_GRANDE
B > 127 % de A + 0,25   → AUT en el mismo tick
```

Si un tick cruza 100 % y AUT, se registra `B_GRANDE_CAUSAL_CROSS`; el estado final es AUT y B Grande no queda vigente.

## 3. Ancla 16:15–16:18

```text
módulo: 29877,0 -> 29848,5 = 28,5
A:      29848,5 -> 29857,6 = 9,1

B Grande:
16:18:34.125
B = 9,1

AUT:
16:18:34.926
B = 12,3
límite = 11,807 (127% + 0,25)

nuevo 1:
origin          = 29857,6
structural_time = 16:17:05.425
knowledge_time  = 16:18:34.926
extremo en AUT  = 29845,3
extensión       = 29843,0
```

B no se informa con 14,6. El movimiento B/AUT es 12,3; 14,6 es la extensión posterior del nuevo 1.

## 4. Autoridad

Al confirmar A:

```text
three_authority = ARCHIVED
module_authority = FROZEN_REFERENCE
active_function = B_CANDIDATE
```

Al AUT:

```text
A / 3 / módulo sin autoridad activa
active_function = NEW_ONE
historical_status conservado
```

## 5. Ancla L2

```text
1 = 7,5
2 = 12,3
3 = 29830,3
módulo = 19,7
A = 20,5 desde 29830,3
AUT directo por A = flag, no nuevo 1
```

El núcleo permanece intacto. El nuevo 1 por AUT directo de A sigue bloqueado.

## 6. Pruebas

```text
Núcleo:          19/19 PASS
A/B/BG/AUT:      32/32 PASS
Total:           51/51 PASS
```

Cubre:

- BG-01 a BG-16;
- B exactamente al 100 %;
- B en el intervalo;
- límite exacto 127 % + 0,25;
- límite + 1;
- salto directo a AUT;
- nuevo 1 en el mismo tick;
- origen y tiempos del nuevo 1;
- extensión posterior del nuevo 1;
- B y AUT sin vigencia simultánea;
- archivo de A/3/módulo;
- A dentro de la misma vela;
- A entre velas;
- retorno sin dos ticks;
- retorno absorbido.

Determinismo L1: idéntico. Prefijo L1: consistente.

## 7. Gate

```text
GATE_B_GRANDE_AUT_PASS
```

Condiciones cumplidas:

- núcleo 19/19;
- A/B 32/32;
- AUT en 16:18:34.926;
- nuevo 1 desde B;
- extensión posterior en nuevo 1;
- sin autoridad anterior activa;
- sin doble estado B/AUT;
- sin spoilers;
- determinismo y prefijos.

## 8. Límites

```text
NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_INCOMPLETE
```

No implementado:

- C;
- CUT;
- TT;
- FT;
- nuevo 1 por AUT directo de A;
- gap con nuevo 1;
- concurrencia interna;
- ciclo universal de 1.

No se modificaron originales, motor oficial, R3, R5 ni goldens.
