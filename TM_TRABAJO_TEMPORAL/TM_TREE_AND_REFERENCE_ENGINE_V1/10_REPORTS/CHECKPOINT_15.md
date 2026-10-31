# CHECKPOINT — ITERACIÓN 15

## Baseline

```
TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT
```

## Implementado y verificado

- núcleo 1/2/3/módulos, con 2 y 3 pertenecientes a su vela;
- A / retorno / B candidata, con estado de retorno propio por A;
- B Grande y AUT por B (100 % → 127 % + 0,25);
- AUT directo por A (A_CONFIRMED) y AUT directo por estructura en la lectura local;
- nuevo 1 por ambas vías, con módulo del AUT (`aut_mod_*`) separado del módulo del ciclo;
- C Grande, C usada como tendencia, CUT;
- TT (pendiente/confirmado/extendido/fallido) y FT;
- gap con nuevo 1 implícito y doble pertenencia TT+gap;
- lectura local anidada: 1-2-3 módulo 19,7, A 20,5, AUT directo y cadena de AUT locales en 16:23.

## Comparación tick a tick

```
B1 16:15–16:18  4/4 anclas   sin divergencia
B2 16:19–16:22  4/4 anclas   sin divergencia
B3 16:22–16:24  3/3 anclas   sin divergencia
B4 16:24–16:25  3/3 anclas   sin divergencia
```

## Pruebas

```
146/146 PASS · canónicas 128 · provisionales 16 · open_rule 2
```

## Feed completo

37 rotaciones internas, 8 módulos, 2 AUT, 2 TT confirmados, 3 CUT, 1 FT.

## Límites declarados

- La referencia del 35 % es orientativa (`PROVISIONAL`), no frontera canónica.
- La lectura local no está validada fuera de 16:19–16:23.
- 16:25–17:29 tiene lectura humana pero no comparación tick a tick.

## Estado

```
TREE_STATUS              NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_STATUS  REFERENCE_ENGINE_CONSISTENT_IN_VALIDATED_BLOCKS
PATTERN_ENGINE_STATUS    PATTERN_ENGINE_INCOMPLETE
```

No se congela el árbol. No se modifica el motor oficial. No se opera en real.
