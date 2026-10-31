# POLÍTICAS EXPERIMENTALES — LECTOR v3

**Lector:** `blind_reader_v3_owned_states.py`
**Hash:** `AE559A31AAB3222A6F04029999102DCA6347D83201F2009888557CED60C1029F`
**Base:** `blind_reader_v2.py` (no sobrescrito)
**Estado:** corrección de propiedad; ninguna política `EXPERIMENTAL_ASSUMPTION` valida el árbol ni se congela.

| ID | Problema | Política | Resultado | Estado |
|---|---|---|---|---|
| P-OWN-01 | 3 sobrevivía con 2 IMPOSIBLE | 3 solo es legal desde `module_1_2_3`, con 2 CONFIRMED | 0 `INVALID_THREE_WITHOUT_CONFIRMED_TWO` | `TREE_SUPPORTED` |
| P-OWN-02 | `module_by_discard` dejaba `three_extreme` vivo | Al pasar a módulo por descarte: 3 IMPOSSIBLE, extremo 0, `three_legal=False` | 0 estados stale | `TREE_SUPPORTED` |
| P-OWN-03 | B Grande se invalidaba por un nuevo extremo de A | B falla solo mientras es candidata; con B Grande, el contrario es C | 16:23 = B Grande → C | `TREE_SUPPORTED` (Q3) |
| P-OWN-04 | Un retroceso de 2 puntos congelaba el 3 | A candidata no congela 3; el 3 sigue actualizando su extremo | 3 conserva su extremo final | `TREE_SUPPORTED` (Q2) |
| P-OWN-05 | AUT_B heredaba el tiempo del extremo de A | Nuevo 1 de AUT_B: origen y `st` de B | 0 `INVALID_NEW_ONE_ORIGIN` | `TREE_SUPPORTED` |
| P-OWN-06 | Referencias sin dueño | `reading_id`, `branch_id`, `refs_owner`, `three_owner`, `mod_owner_*` | 0 fugas | `TREE_SUPPORTED` |
| P-L1L2 | L2 inyectaba referencias en L1 | Ejecuciones separadas con `reading_id` distinto; sin estado compartido | L2 2 únicas + 2 duplicadas | `TREE_SUPPORTED` (Q1) |
| P-A-B100 | A se confirma con B = 100 % | Gate conservador; no es canon | 51 generaciones | `EXPERIMENTAL_ASSUMPTION` |
| P-DUP | L2 contada como lectura nueva | Comparar 1: origen, extremo, tamaño | 2 duplicados detectados | `AUDIT_METHOD` |
| P-GAP | Gap con ticks inventados | A/B/A trend implícitas; nuevo 1 desde la apertura | 9 gap integrados | `TREE_SUPPORTED` (4.6) |
| P-MOD | Módulo por rango bruto | Extremos estructurales con propiedad | 0 extensión inválida | `TREE_SUPPORTED` (N-012) |
| P-TT | TT al cierre del swing | TT al primer tick que alcanza el objetivo | sin cambios | `TREE_SUPPORTED` (v2.17) |

## Uso

1. `TREE_SUPPORTED` aplica el árbol; no crea reglas.
2. `EXPERIMENTAL_ASSUMPTION` no se congela ni se usa como golden.
3. `AUDIT_METHOD` solo clasifica evidencia.
4. Si Javier decide Q-AUT, la política elegida pasa a `TREE_SUPPORTED`; la otra queda como comparación.
