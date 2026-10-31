# CHECKPOINT 8 — AUT DIRECTO POR A (ITERACIÓN 08)

Fecha: 2026-10-30
Intérprete: `tm_reference_interpreter_v1_direct_aut.py`
Versión: `TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT`

## 1. Qué se hizo

1. **Política de cuatro puntos retirada.** `P-AB-04_RETURN_JUMP_4` marcada
   `REJECTED_EXPERIMENTAL_ASSUMPTION`. No se sustituyó por otro número fijo.
   `return_jump` queda como campo histórico y siempre vale `False`.
2. **Pruebas afectadas reclasificadas.** A-14 y BG-15 reescritas como
   `TEST_DEPENDS_ON_REJECTED_POLICY` → `EXPERIMENTAL_POLICY_REMOVED`:
   - A-14: un salto único grande NO confirma A (queda `RETURN_MOVE_PENDING`).
   - BG-15: el retorno de varios ticks confirma A por extensión de su propio
     extremo, sin cuatro puntos.
3. **Vía 1 intacta.** B Grande (100 % .. 127 %+0,25 inclusivo) y AUT por B
   siguen exactamente como en iteración 07.
4. **Vía 2 implementada.** `AUT_DIRECT_BY_A`: A supera estrictamente la base
   del módulo → nuevo 1 en el mismo tick, con `origin=a_origin`,
   `structural_time=structural_time_A`, `knowledge_time=tick de cruce`.
   Sin B, sin 127 %+0,25, sin tick intermedio.
5. **Archivado.** A=`CONFIRMED_ARCHIVED`, 3=`ARCHIVED`, módulo=
   `FROZEN_REFERENCE`, `active_function=NEW_ONE`.
6. **Sin contaminación de B.** Corregido `_on_new_one_tick`: en la vía directa
   B no se escribe (antes marcaba `B=AUT` por herencia de la vía B).

## 2. Resultados de pruebas

```text
CORE .............. 19 / 19 PASS
A/B + BG ........... 32 / 32 PASS
AUT directo (AD) ... 16 / 16 PASS
TOTAL .............. 67 / 67 PASS
```

Detalle AD: AD-01..AD-14 + AD-DET + AD-PRE.

## 3. Ancla 16:15–16:18 (regresión intacta)

```text
módulo            29877,0 → 29848,5 = 28,5  (BY_DISCARD_1_2, owner=2)
A                 29848,5 → 29857,6 = 9,1   (una sola confirmación)
B candidata       desde 29857,6
B Grande          16:18:34.125  (B = 9,1 = 100 % de A)
AUT por B         16:18:34.926  (B = 12,3 > 127 % + 0,25 = 11,81)
nuevo 1           origin 29857,6 · dir bajista · extreme posterior 29843,0
                  structural_time 16:17:05.425 · knowledge_time 16:18:34.926
```

## 4. Ancla L2 16:19–16:22 (AUT directo)

```text
1 = 7,5 · 2 = 12,3 · 3 = 29830,3 · módulo = 19,7 · A = 20,5
base del módulo = 29850,0
A alcista 29830,3 → 29850,8
AUT_DIRECT_BY_A   16:22:52.576  precio 2985080
nuevo 1           origin 29830,3 · dir alcista
                  structural_time 16:21:54.482 (nacimiento de A)
                  knowledge_time 16:22:52.576 (primer cruce estricto)
A                 CONFIRMED_ARCHIVED
módulo            FROZEN_REFERENCE
B                 inexistente
```

## 5. Vías separadas

| | VÍA 1 (AUT por B) | VÍA 2 (AUT directo por A) |
|---|---|---|
| disparador | B > 127 %+0,25 de A | A > base del módulo (estricto) |
| B | existe | no existe |
| origin nuevo 1 | b_origin (= extreme_A) | a_origin |
| structural_time | nacimiento de B | structural_time_A |
| knowledge_time | tick de AUT | primer tick de cruce |
| límite 127 % | aplica | no aplica |

## 6. Fuera de alcance (sin cambios)

```text
C · CUT · TT · FT · gap con nuevo 1 · concurrencia L1/L2 · ciclo universal de 1
```

## 7. Estado

```text
GATE_AUT_DIRECT_BY_A_PASS
```

- política de cuatro puntos retirada: sí
- pruebas afectadas reclasificadas: sí
- L2 confirma AUT directo en el tick correcto: sí (16:22:52.576)
- nuevo 1 hereda A: sí (origin/structural_time)
- no aparece B en la vía directa: sí
- las dos vías permanecen separadas: sí
- regresiones anteriores pasan: 67/67
- ejecución determinista: sí
- prefijos consistentes: sí
- sin spoilers: la evaluación usa solo el tick actual

```text
NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_INCOMPLETE
```

No se modifica el motor oficial. No se congela el árbol.
