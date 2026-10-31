# POLÍTICAS EXPERIMENTALES — LECTOR v4

**Lector:** `blind_reader_v4_functional_autonomy.py`
**SHA-256:** `EA5720ABD9CC121BA84197B4A1CE2D7D9030102B39F12533044EA227EE30A746`
**Base:** v3 (no sobrescrito)
**Estado:** experimental; no válida para congelar.

| ID | Política | Evidencia | Estado |
|---|---|---|---|
| P-AUT-01 | B no se evalúa antes de `A_CONFIRMED` | 0 `B_100_WITHOUT_A_CONFIRMED` | `TREE_SUPPORTED` (Q-AUT) |
| P-AUT-02 | Contrario pendiente; absorción si la función dominante extiende | 55 `MODULE_EXTENDED_ABSORBS_A` | `TREE_SUPPORTED` (Q-AUT) |
| P-AUT-03 | A se confirma al cruzar el punto medio del movimiento dominante o su base | 745 confirmaciones | `OPEN_RULE_DEPENDENCY` (Q-AUT-REF) |
| P-THREE-50 | Retroceso ≤ 50 % conserva 3; > 50 % imposibilita; 50 % exacto válido | L2 16:20; 3 legal | `TREE_SUPPORTED` (Q-3-50) |
| P-GAP-ALL | Toda apertura no plana prohíbe 2 y entra en gap | 36 gaps L1 | `TREE_SUPPORTED` (R-GAP-OPEN) |
| P-GAP-CLASSIC | `GAP_MIN=200` solo como comparación | 4 generaciones classic | `AUDIT_METHOD` |
| P-OWN-01 | 3 solo con 2 CONFIRMED | 0 `INVALID_THREE_WITHOUT_CONFIRMED_TWO` | `TREE_SUPPORTED` |
| P-OWN-02 | Módulo por descarte invalida 3 | 0 stale | `TREE_SUPPORTED` |
| P-OWN-03 | B Grande tiene precedencia; después C | 0 `INVALID_MODULE_EXTENSION` | `TREE_SUPPORTED` (Q3) |
| P-OWN-04 | A candidata no congela 3 | 730 `A_CANDIDATE_AFTER_3` | `TREE_SUPPORTED` (Q2) |
| P-OWN-05 | Nuevo 1 hereda origen de la transición | 0 `INVALID_NEW_ONE_ORIGIN` | `TREE_SUPPORTED` |
| P-L1L2 | L1/L2 separados por `reading_id` | 0 fugas | `TREE_SUPPORTED` (Q1) |

## Uso

1. `TREE_SUPPORTED` aplica una decisión; no crea ontología.
2. `OPEN_RULE_DEPENDENCY` no se congela; P-AUT-03 depende de Q-AUT-REF.
3. `AUDIT_METHOD` no es lectura canónica.
4. v4 no es autoridad; el árbol aprobado lo es.
