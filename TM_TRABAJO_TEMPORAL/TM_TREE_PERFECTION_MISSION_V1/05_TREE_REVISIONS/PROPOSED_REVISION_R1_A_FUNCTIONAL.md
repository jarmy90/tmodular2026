# TM — REVISIÓN UNIVERSAL PROPUESTA R1
## FUNCIÓN A: CONFIRMACIÓN FUNCIONAL SIN UMBRAL FIJO

**Fecha:** 2026-10-30
**Estado:** `PROPOSED_UNIVERSAL_RULE` — **no es canon, no está aprobada**
**Árbol de origen:** v2.19 (`94A1408A…`)
**Motivo:** v2.16 deja A como "recorrido contrario pendiente" y prohíbe el
35 % como frontera; v2.5 usa 6 puntos solo como filtro operativo, no como
autonomía. El lector anterior convirtió el filtro operativo de 6 puntos en
una condición ontológica de A. Esta revisión separa ambas cosas.

---

## 1. PROBLEMA

Después de un módulo, el primer recorrido contrario es A. El árbol no fija
un tamaño mínimo de A. Sin una condición funcional, el lector no puede
decidir entre:

```text
A autónoma  → B candidata → B Grande → AUT
A absorbida → el módulo sigue → no hay A
```

El 6 % / 6 puntos no es una regla de A: v2.5 dice expresamente que el filtro
de 6 puntos **no altera A, B, AUT, TT, C, CUT ni FT**. El 35 % es
"referencia aproximada", no frontera. Cualquier umbral fijo (2, 6, 12, 20,
35 %) está prohibido por el mandato.

---

## 2. REGLA PROPUESTA

```text
A NACE:
  origen = extremo final del módulo
  dirección = contraria al módulo
  estado = CONTRARY_MOVE_PENDING
  structural_time = tick del extremo del módulo
  knowledge_time = 0 (aún no conocido)

A SE CONFIRMA en el primer tick en que ocurre una de estas dos cosas:

  (1) B alcanza el 100 % de A.
      B se mide desde el extremo de A en dirección contraria a A.
      En ese tick, simultáneamente:
        A = CONFIRMED
        B = B_GRANDE
        knowledge_time_A = tick de B al 100 %

  (2) A supera estrictamente la base del módulo.
      A = A_USED_AS_TREND
      AUT en la dirección de A
      nuevo 1 en el movimiento que produce el cruce
      knowledge_time_A = tick del cruce

A SE ABSORBE si, antes de (1) o (2), el precio supera el extremo del módulo
en la dirección del módulo:

  A = ABSORBED_IN_ACTIVE_FUNCTION
  el módulo se extiende
  no se abre B ni AUT
```

**No se usa ningún tamaño absoluto de A.** La autonomía se demuestra por la
capacidad de A de originar B completa o de superar la base del módulo.

---

## 3. CASO POSITIVO — 16:15–16:18

```text
Módulo 16:15-16:16: 29.877,0 → 29.848,5 = 28,5.
A alcista: 29.848,5 → 29.857,6 = 9,1.
B bajista desde 29.857,6.
B alcanza el 100 % de A en 29.848,5.
A CONFIRMED; B GRANDE.
B supera 127 % + 0,25 = 11,807 en 29.845,793.
AUT bajista; nuevo 1 desde 29.857,6.
```

La v005 confirma este caso [A]. La regla lo reproduce sin usar 6 puntos.

---

## 4. CASO NEGATIVO — A ABSORBIDA

```text
Módulo bajista 29.877,0 → 29.848,5.
A alcista hasta 29.850,0 (1,5).
El precio vuelve a bajar y supera 29.848,5.
A no alcanzó B al 100 % ni superó la base 29.877,0.
A = ABSORBED_IN_ACTIVE_FUNCTION.
El módulo se extiende; no hay B, AUT ni nuevo 1.
```

Esto evita que un retroceso pequeño cree una función nueva.

---

## 5. CASO FRONTERA — A QUE SUPERA LA BASE ANTES DE B

```text
Módulo 29.850,0 → 29.830,3.
A alcista 29.830,3 → 29.850,8.
A supera la base 29.850,0 en 0,8 antes de que B alcance el 100 %.
A = A_USED_AS_TREND; AUT alcista; nuevo 1 desde 29.830,3.
```

La base del módulo es la referencia; no se exige un tamaño previo de A.
Este es el caso de 16:22 de la v005.

---

## 6. TIEMPOS

```text
STRUCTURAL_TIME_A = extremo del módulo donde nació A.
KNOWLEDGE_TIME_A:
  - tick de B al 100 %, o
  - tick de superación de la base del módulo.
```

No se presenta knowledge_time como structural_time. A puede existir
estructuralmente desde el extremo del módulo y conocerse mucho después.

---

## 7. INVARIANTES

1. No hay B Grande sin A confirmada en el mismo tick o antes.
2. B candidata provisional puede existir antes de A confirmada; no se
   registra como B Grande hasta que A se confirma.
3. A no se confirma por tamaño.
4. A no se confirma por color de vela.
5. A no se confirma por el cierre de una vela.
6. Si el módulo se extiende, A se absorbe y no se abre B.
7. Si A supera la base, AUT y nuevo 1 en el mismo tick.
8. No se usan 2, 6, 12, 20 ni 35 % como umbral de A.

---

## 8. PRUEBAS

| ID | Caso | Esperado |
|---|---|---|
| A-01 | A 9,1; B 12,3 (16:18) | A confirmada; B Grande; AUT |
| A-02 | A 1,5; módulo se extiende | A absorbida; sin B |
| A-03 | A 20,5; base local 29.850,0; A 29.850,8 | A usada como tendencia; AUT; nuevo 1 |
| A-04 | A 3,0; B 2,0 y módulo se extiende | A absorbida |
| A-05 | A 5,0; B 5,0 exacto | A confirmada; B Grande en el 100 % |
| A-06 | A 5,0; B 6,35 exacto | B Grande; no AUT |
| A-07 | A 5,0; B 6,36 | AUT |
| A-08 | A entre velas | A conserva origen; no se reinicia por cambio de vela |
| A-09 | A con vibraciones internas | A no se fragmenta; conserva extremo |
| A-10 | A y B simultáneas | A knowledge_time = B 100 %; no antes |

---

## 9. IMPACTO

- Sustituye el uso ontológico del filtro de 6 puntos.
- No cambia el filtro operativo de 6 puntos de v2.5.
- Permite que el lector avance sin umbral fijo.
- Deja Q1 (L1/L2) y Q2 (vida de 2/3) como decisiones separadas.
- **No se aplica al árbol congelado hasta aprobación expresa de Javier.**

---

## 10. FUENTES

- v2.16: A posterior a AUT/nuevo 1 no se clasifica por distancia fija.
- v2.18: A → B → B Grande → AUT en casos inequívocos.
- v2.5 D/H: el filtro de 6 puntos es operativo y no altera A/B/AUT/TT.
- Mandato 2026-10-30 §7: prohibición de umbrales provisionales de autonomía.
- v005 16:18 y 16:22: casos [A] con A = 9,1 y A = 20,5.
