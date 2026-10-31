# CHECKPOINT 13 — SANEAMIENTO NORMATIVO Y COMPARACIÓN HUMANA

**Baseline:** `TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT` (no es motor oficial)
**Nuevo patch:** `TM_CANON_ACTIVO/01_ARBOL/TM_PATCH_CANONICO_v2_20_PLANO_Y_CUT.md`
**Árbol v2.19:** sin modificar (`94A1408A…6B17`)

## Cambios

```text
1. frontera de plano fijada por escrito (< 0,25 plano; 0,25 exactos NO plano)
2. Q-CUT cerrada: CUT no crea nuevo 1 ni resetea; C sigue viva
3. cierre causal (tick TT) separado de la rotación administrativa (apertura siguiente)
4. FT reclasificado: 4 pruebas canon, 2 provisionales
5. métricas: 47 rotaciones, no «47 ciclos»
6. suite nueva de prioridad gap+TT y estados heredados (GP-01..GP-11)
7. comparación humana de los cuatro bloques con primer error localizado
```

## Anclas

```text
L1 16:15-16:18  coincide con la lectura humana vela a vela
L2 16:19-16:22  coincide salvo el instante de conocimiento del 1 de 16:19
B3 16:22-16:24  diverge en 16:23: falta la lectura local (Q-CONCURRENCY)
B4 16:24-16:25  nuevo 1 desde 29848,5 correcto; falta TT del gap (Q-GAP-TT)
```

## Pruebas

```text
nucleo 19 | A/retorno/B 32 | AUT directo 17 | C/CUT 18 | gap+conc 16 | TT 12 | iter12 18 | iter13 13
TOTAL 145 PASS 145
CANONICAL 79 | PROVISIONAL 62 | OPEN_RULE_BLOCK 4
```

## Rotaciones del feed

```text
47 rotaciones: 38 por gap · 2 por TT · 3 por C tendencia · 1 inicial · 3 por nuevo 1 de AUT
0 cascadas · 5 aplazamientos por nuevo 1 de tamaño cero
A 10 · B candidata 10 · B Grande 1 · AUT 7 · TT 2 · TT fallido 5 · FT 1 · CUT 2 · módulos 10
```

## Estado

```text
TREE_STATUS:              NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_STATUS:  REFERENCE_ENGINE_INCOMPLETE
PATTERN_ENGINE_STATUS:    PATTERN_ENGINE_INCOMPLETE
```
