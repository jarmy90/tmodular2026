# TM — REVISIÓN ACUMULADA v2.20 — BORRADOR R2

**Estado:** `DRAFT_NOT_FROZEN`
**Base:** `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md`
**SHA-256 base:** `94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17`
**R1:** `TREE_REVISION_v2_20_DRAFT.md` (Q1/Q2/Q3)
**R2 añade:** Q-AUT, Q-3-50, GAP sin zona muerta y regresión v4.
**No sustituye v2.19. No es autoridad ejecutable.**

---

## 1. REGLAS CERRADAS EN R2

### R-AUTONOMY-01 — B solo después de A

```text
B >= 100 % de un recorrido contrario
→ NO crea A Grande retrospectivamente
```

Secuencia:

```text
recorrido contrario → CONTRARY_MOVE_PENDING
función dominante extiende → ABSORBED_IN_ACTIVE_FUNCTION
contrario adquiere autonomía → A_CONFIRMED
solo después de A_CONFIRMED → evaluar B
```

Después de A_CONFIRMED:

```text
B < 100 %                    → B candidata
100 % <= B <= 127 % + 0,25   → B Grande
B > 127 % + 0,25             → AUT
```

### R-AUTONOMY-02 — Absorción y autonomía

- Si la función dominante vuelve a extender su extremo, el contrario pendiente se absorbe.
- Si el contrario adquiere autonomía, se confirma A.
- `structural_time` = origen real del recorrido contrario.
- `knowledge_time` = tick en que la autonomía resulta conocible.
- Sin umbral fijo de puntos: no 2, 6, 12, 20 ni 35 %.
- La referencia estructural implementada en v4 es el punto medio del movimiento dominante o su base completa. **La referencia exacta 1 vs módulo 1+2 queda abierta (R-AUT-REF).**

### R-THREE-50 — Frontera inclusiva

```text
retroceso <= 50 % de 2  → posibilidad de 3 conservada
retroceso >  50 % de 2  → 3 IMPOSSIBLE
50 % exacto             → válido
```

Tocar el 50 % no confirma 3; solo conserva su posibilidad. Después:

- recuperación de la dirección de 2;
- superación estricta del extremo final de 2;
- confirmación de 3 en ese tick;
- el extremo final de 3 puede seguir actualizándose mientras A no se confirme.

### R-GAP-OPEN — Sin zona muerta

```text
|Open − Close_previo| <  0,25  → plano; 2 permitido si el resto se cumple
|Open − Close_previo| >= 0,25  → no plano; 2 prohibido
                               → rama funcional de gap v2.19
```

No existe la zona 0,25–1,99 sin tratamiento. Cualquier apertura no plana:

- impide 2;
- registra la transición de gap;
- crea el nuevo 1 observable desde la apertura;
- no inventa ticks ni precios internos.

---

## 2. REGLAS QUE SE MANTIENEN

- N-002/N-005: plano `< 0,25`; 0,25 no plano.
- N-006: condiciones de 2; sin 2 → módulo por descarte.
- N-012: módulo por extremos estructurales finales; 2/3 conservan conocimiento y extremo.
- N-021: AUT → nuevo 1 inmediato.
- N-025: TT al primer tick que alcanza el objetivo.
- Q1: L1/L2, máximo dos escalas, referencias separadas.
- Q2: 2/3 confirman al primer tick válido y actualizan su extremo final.
- Q3: B < 100 candidata; 100–127 % + 0,25 B Grande; > 127 % + 0,25 AUT.
- Q-B3: cerrada como error de propiedad del lector v2; no es contradicción del árbol.
- Q-3-50: cerrada inclusiva.

---

## 3. REGLA ABIERTA

### R-AUT-REF — referencia de autonomía de A

Caso 16:15–16:18:

```text
1 = 16,2
módulo 1+2 = 28,5
A = 9,1  (56 % del 1; 32 % del módulo)
B = 12,3 (135 % de A)
```

- Si A se mide contra el **1**: A se confirma; B Grande/AUT; nuevo 1 bajista; se conserva el ancla [A].
- Si A se mide contra el **módulo**: A se absorbe; el 1 sigue; el AUT de 16:18 queda sustituido.

La decisión cambia el conteo y el ancla [A]. No se inventa respuesta.

Otras abiertas: `OPEN-INIT-01` (primer 1), `OPEN-CUT-01` (CUT), `OPEN-FT-01` (confirmación estructural de FT).

---

## 4. IMPLEMENTACIÓN v4

- `blind_reader_v4_functional_autonomy.py`.
- `P-A-B100` eliminado como autoridad.
- `CONTRARY_MOVE_PENDING`, `ABSORBED_IN_ACTIVE_FUNCTION`, `A_CONFIRMED`.
- B solo después de A_CONFIRMED.
- 3 solo con 2 CONFIRMED; invalidación por rama.
- 50 % inclusivo.
- `gap=all` por defecto; `gap=classic` solo comparación.
- L1/L2 separados por `reading_id`, sin estado compartido.

---

## 5. EVIDENCIA

- L2 16:19–16:24: 1=7,5; 2=10,8; 3=29830,3; módulo=19,7; A=20,5.
- v3 51 → v4 classic 4 (−47 por autonomía de A).
- v4 classic 4 → v4 all 44 (+40 por gap sin zona muerta).
- v4 full: 44 (7 primarias, 36 gap, 1 abierta); 0 errores de propiedad.
- Doble ejecución `66099D49…`; prefijos 16:30, 17:00, 17:15 coincidentes.
- El ancla 16:18 no se reproduce bajo la referencia módulo.

---

## 6. PRUEBAS AFECTADAS

- B 100 % sin A confirmada → prohibido.
- A absorbida por extensión dominante.
- A confirmada por referencia estructural; `structural_time` y `knowledge_time`.
- 50 % exacto de 2: 3 posible; > 50 %: 3 imposible.
- Cualquier apertura no plana: 2 prohibido y gap.
- Gap con nuevo 1 desde la apertura, sin ticks internos.
- L1/L2 sin fugas.
- New 1 con origen heredado según la transición.

---

## 7. ESTADO

```text
NOT_READY_TO_FREEZE
```

No se congela. No se aprueban 44 ni 51. Falta R-AUT-REF y la regresión [A] completa.
