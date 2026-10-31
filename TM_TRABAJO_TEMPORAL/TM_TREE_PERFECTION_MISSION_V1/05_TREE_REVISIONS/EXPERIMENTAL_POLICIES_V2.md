# POLÍTICAS EXPERIMENTALES — LECTOR v2 CORREGIDO

**Lector:** `01_BLIND_READINGS/blind_reader_v2.py`
**Hash actual:** `164CFBB25A56D111DF79F99A17CFCA92408E2A933437DCD62BC3AA054A56ABFB`
**Hash anterior:** `NOT_ARCHIVED` (versión pre-Q2/Q3; evidencia en Checkpoint 1, traza `19EB2200…F876`)
**Estado:** experimental. Ninguna política `EXPERIMENTAL_ASSUMPTION` valida el árbol ni puede congelarse.

---

## Tabla de políticas

| ID | Versión | Problema observado | Regla / decisión | Resultado anterior | Resultado posterior | Ticks afectados | Estado |
|---|---|---|---|---|---|---|---|
| P-Q1 | v2-Q1 | El 1 local de 16:19 se perdía al sustituir L1 | L1 principal + L2 local; máximo dos escalas; referencias, genealogías, módulos y TT separados | 1 cadena única | L2-G1 única + L1-G3/G4 compartidas | 16:19–16:24 | `TREE_SUPPORTED` (Q1 + v2.4) |
| P-Q2 | v2-Q2 | 2 y 3 se congelaban en el tick de confirmación | `knowledge_time` en el primer tick válido; `extreme` final real; módulo y A con extremos finales | L2 16,7 / A 17,5 | L2 19,7 / A 20,5 | 16:20–16:24 | `TREE_SUPPORTED` (Q2) |
| P-Q3 | v2-Q3 | B al 122,5 % se clasificaba AUT | B < 100 % candidata; 100–127 % + 0,25 B Grande; > 127 % + 0,25 AUT; base del módulo no da AUT por B | AUT falso en 16:23 | B Grande en 16:23 | 16:23 | `TREE_SUPPORTED` (Q3) |
| P-GAP | v2 | Gap medido como A única o con ticks inventados | Gap = A → B → A trend implícitas; nuevo 1 desde la apertura; sin ticks internos | módulo de gap inflado | 6 generaciones de gap integradas | 16:25, 16:28, 16:47, 16:56, 17:02, 17:09 | `TREE_SUPPORTED` (4.6) |
| P-MOD | v2 | Módulo por `max(highs) − min(lows)` | Módulo por extremos estructurales con propiedad; 2 no encoje; extremo de A excluido | módulo bruto | módulo por extremos finales | todo el feed | `TREE_SUPPORTED` (N-012/Q2) |
| P-A-B100 | v2 | A sin condición de confirmación | A se confirma cuando B alcanza el 100 % de A (o A cruza la base del módulo) | 51 generaciones | 26 generaciones | 15 transiciones `A_USED_AS_TREND` | `EXPERIMENTAL_ASSUMPTION` |
| P-A-BTURN | v2 | A confirmada demasiado tarde | A se confirma cuando B falla su 100 % y gira, con filtro de ruido | 51 generaciones | 26 generaciones | las mismas 15 transiciones | `EXPERIMENTAL_ASSUMPTION` |
| P-DUP | v2 | L2 contada como tres lecturas nuevas | Comparar origen/extremo/tamaño del 1; si coincide con L1, marcar duplicado estructural | 3 L2 | 1 L2 única + 2 duplicados | 16:22–16:24 | `AUDIT_METHOD` (no es regla de lectura) |
| P-DOM | v2 | Un AUT local cambiaba la dominancia | AUT local no cambia dominancia; se exige transición estructural posterior | dominancia por AUT | L1 conserva dominancia | 16:19–16:24 | `TREE_SUPPORTED` (Q1) |
| P-TT | v2 | TT evaluado al cierre de un swing | TT se confirma en el primer tick que alcanza el objetivo | TT tardío | TT al primer tick | todo el feed | `TREE_SUPPORTED` (v2.17/N-025) |
| P-ONT | v2 | Nombres locales como funciones nuevas | Solo 1, 2, 3, A, B, C, AUT, CUT; A/C trend son `transition_reason` | ontología expandida | ontología cerrada | todo el feed | `TREE_SUPPORTED` (invariante) |

---

## Regla de uso

1. `TREE_SUPPORTED` puede citarse como aplicación del árbol, no como árbol nuevo.
2. `EXPERIMENTAL_ASSUMPTION` no se convierte en regla, no se congela y no se usa como golden.
3. `AUDIT_METHOD` solo clasifica evidencia; no crea semántica.
4. Si Javier decide Q-AUT, la política elegida pasa a `TREE_SUPPORTED` en v2.20 y la otra se conserva como comparación.
5. El lector v2 no es autoridad. La autoridad es el árbol aprobado.
