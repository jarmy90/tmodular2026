# TM — FASE A — LECTURAS SECUNDARIAS 16:49–17:29

- **Fuente:** tickfeed maestro `5F701BE2…`; árbol v2.19 `94A1408A…`
- **Instrumento:** `blind_reader.py` (Fase A)
- **tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

> Este documento conserva lo que la lectura principal **no** convierte en
> función: patrones TT archivados, esbozos de resolución de gap, transiciones
> A/C usadas como tendencia y la lectura de R5 sobre el mismo bloque real.
> Nada de esto se usa como golden.

---

## 1. PATRONES TT POR GENERACIÓN

El TT es patrón, no función. Sobrevive a la transición que cierra su
generación (H6). En el bloque hay **6 TT confirmados** y **9 fallidos**; un
TT puede confirmarse después del AUT de su propia generación.

| Gen | Objetivo | Resultado | Hora | Detalle |
|---:|---:|---|---|---|
| 12 | 29717,2 | FAILED | 16:50:32,234 | retorna a la base 29666,4 |
| 13 | 29560,2 | FAILED | 16:55:12,557 | retorna a la base 29675,8 |
| 14 | 29648,7 | CONFIRMED | 16:54:29,847 | tick 29651,6; **2,4 s después del AUT** |
| 15 | 29613,5 | CONFIRMED | 16:56:32,746 | tick 29612,7; 27 s después del AUT |
| 16 | 29642,3 | CONFIRMED | 17:01:11,951 | tick 29643,1; 3 min después del AUT |
| 17 | 29643,1 | FAILED | 17:00:08,407 | retorna a la base 29623,6 |
| 18 | 29692,6 | FAILED | 17:07:02,648 | retorna a la base 29617,6 |
| 19 | 29682,1 | FAILED | 17:10:07,769 | retorna a la base 29616,9 |
| 20 | 29584,9 | FAILED | 17:11:49,457 | retorna a la base 29634,8 |
| 21 | 29650,2 | CONFIRMED | 17:13:19,308 | tick 29650,7; 1,6 s después del AUT |
| 22 | 29679,3 | FAILED | 17:15:34,383 | retorna a la base 29653,8 |
| 23 | 29697,0 | FAILED | 17:19:20,598 | retorna a la base 29656,1 |
| 24 | 29641,0 | CONFIRMED | 17:21:13,306 | tick 29639,8; 8 s antes del AUT |
| 25 | 29681,1 | FAILED | 17:25:41,128 | retorna a la base 29633,6 |
| 26 | 29596,0 | CONFIRMED | 17:28:42,077 | tick 29595,4; 51 s después del AUT |
| 27 | 29592,4 | POSSIBLE | — | abierto al final del feed |

**Lectura:** el TT no es un evento de cierre. Cinco de los seis TT
confirmados se confirmaron **después** de que su generación hubiera terminado
por AUT o por transición. Si el motor evaluara el TT sólo al cerrar un
movimiento —como hace R5— perdería esos cinco. Esto valida la regla 4.8 y
refuerza la auditoría CE: el TT debe evaluarse tick a tick.

**Fallo del TT:** se declara cuando el precio retorna a la **base del módulo**
antes de alcanzar el objetivo. No se declara cuando el precio vuelve al final
de A: volver al final de A es el propio comienzo del patrón. Ésta es una
decisión de política (Q_TT_FAILURE), no una regla cerrada del árbol.

---

## 2. ESBOZOS DE GAP

En el bloque hay **14 aperturas no planas** que impiden 2. Nueve de ellas
superan 1,00 punto y se registran además como `GAP_SIGNIFICANT_UNDEFINED`:

| Gen | Hora | Gap | Nuevo 1 observable |
|---:|---|---:|---|
| 12 | 16:50:00,152 | −3,10 | apertura 29686,8 |
| 14 | 16:54:00,162 | −1,40 | apertura 29640,7 |
| 15 | 16:56:00,073 | −3,50 | apertura 29643,8 |
| 16 | 16:58:00,025 | −1,20 | apertura 29622,1 |
| 17 | 17:00:00,205 | +2,10 | apertura 29635,9 |
| 18 | 17:02:00,082 | −3,00 | apertura 29663,1 |
| 19 | 17:09:00,169 | −2,30 | apertura 29649,9 |
| 20 | 17:11:00,103 | −1,10 | apertura 29590,7 |
| 21 | 17:13:00,059 | +1,90 | apertura 29637,7 |

Las otras cinco (0,60–0,80 puntos) son no planas pero no se marcan como gap
significativo. **El árbol no fija el umbral que separa “no plano” de “gap
significativo”.** La regla 4.6 exige que el tramo se represente como
A Grande implícita → B Grande implícita → A usada como tendencia implícita →
nuevo 1 desde la apertura, pero no dice a partir de cuántos puntos se activa.
El lector registra el esbozo (`H7`) y no desarrolla la escalera implícita.

Consecuencia práctica: si todo no-plano fuera gap, el bloque tendría 14
resoluciones implícitas; si el umbral fuera 1,00, tendría 9. El lector usa la
primera opción para 2 (no hay 2 en ningún caso no-plano) y la segunda sólo
para etiquetar. La diferencia queda como **Q_GAP**.

---

## 3. TRANSICIONES A/C USADAS COMO TENDENCIA

No son funciones nuevas. Son razones de transición y se conservan con su
trazabilidad:

| Gen | Hora | Transición | Valor | Base del módulo | Consecuencia |
|---:|---|---|---:|---:|---|
| 12 | 16:50:32,234 | C_USED_AS_TREND | 29666,1 | 29666,4 | nuevo 1 en 16:51 |
| 17 | 17:00:08,407 | A_USED_AS_TREND | A = 17,9 | 29623,6 | nuevo 1 en 17:01 |
| 18 | 17:07:02,847 | C_USED_AS_TREND | 29615,6 | 29617,6 | nuevo 1 en 17:08 |
| 20 | 17:11:49,457 | A_USED_AS_TREND | A = 51,0 | 29634,8 | nuevo 1 en 17:12 |
| 22 | 17:15:37,388 | A_USED_AS_TREND | A = 26,0 | 29653,8 | nuevo 1 en 17:16 |
| 25 | 17:25:41,128 | A_USED_AS_TREND | A = 46,2 | 29633,6 | nuevo 1 en 17:26 |

Las cuatro `A_USED_AS_TREND` son el antídoto contra el crecimiento infinito
de A. Sin ellas, la A de 17:10 habría seguido 27 minutos y habría absorbido
todo el bloque. La transición se dispara cuando A supera la **base del
módulo** (100 % del módulo), no cuando supera el final de A.

**Cuestión abierta:** el árbol define la conversión de C con la base del módulo
(v2.17), pero para A sólo dice “A usada como tendencia → AUT → nuevo 1”
(v2.18). No fija si la referencia es la base del módulo, el final de A o el
100 % del módulo. El lector adopta la base por analogía con C. Es **Q_BASE**.

---

## 4. LECTURA REGULAR Y LECTURA ALTERNATIVA

En el bloque **no se completó ningún módulo regular 1-2-3**. Las 16
generaciones son módulos por descarte. La razón está en 4.2: 2 exige apertura
plana y 100 % de 1.

- 14 de 16 velas abrieron con diferencia ≥ 0,25 → 2 imposible por no-plano.
- 1 vela abrió plana pero la 2 no llegó al 100 % y cerró (gen 25).
- 1 vela abrió plana pero tuvo cola inicial prohibitiva (gen 23).

La lectura alternativa de v2.14 (`1+2 = módulo → A desde el extremo de 2 →
B candidata`) **no se desarrolla en paralelo**. El lector sólo conserva la
lectura regular. Esto no invalida la lectura, pero deja sin cubrir la
concurrencia que el árbol autoriza después de 2 confirmado. Es **Q_CONCURRENCY**.

En el warm-up sí hubo un 1-2-3 regular: 16:19 (1 = 7,5), 16:20 (2 = 12,3),
16:21 (3 = 19,7), módulo 29850,0 → 29830,3. Es el único del tramo 16:15–17:29.
La lectura del bloque no lo repite.

---

## 5. R5 SOBRE EL BLOQUE REAL (EVIDENCIA, NO GOLDEN)

R5 auditado (`9BD1BEDB…`) se ejecutó sobre los mismos 11.414 ticks. Resultado:

```text
lecturas creadas: 29
eventos: 702
vocabulario: LECTURA_CREADA, A_INICIO, B_CANDIDATA, B_GRANDE, AUT, C, CUT,
             TT_100, TT_EXT, LECTURA_CERRADA, B_FALLIDA, B_OSCILACION,
             LOCAL_FUNCTION, QUESTION, GAP
```

**Esto corrige una conclusión de la auditoría CE.** En las 21 secuencias
sintéticas R5 no emitió 2, 3, A, B, C, AUT, CUT ni TT. En el feed real **sí
emite A, B, C, AUT, CUT y TT_100**. La ausencia era un artefacto del banco
sintético, no una incapacidad absoluta del motor. Lo que R5 no reproduce es
la **escalera causal del árbol**, no el vocabulario.

### 5.1 Primera divergencia

```text
secuencia 8922 · 16:49:00.012
LECTOR: ONE_CANDIDATE, 1 pendiente, apertura 29680,8
R5:     sin evento; la primera lectura aparece en 8951 (16:49:06,426)

secuencia 8951 · 16:49:06,426
R5:     R0001, función 1, módulo 29680,8 → 29666,4 = 14,4, dirección bajista
LECTOR: 1 aún candidata; la vela no cierra hasta 16:49:59,949

secuencia 9202 · 16:50:00,152
LECTOR: 1 alcista 29666,4 → 29699,9 = 33,5; módulo 33,5
R5:     R0001 sigue con módulo 14,4; R0002 (16:49:29,885) módulo
        29666,4 → 29686,1 = 19,7
```

La primera divergencia causal es la **definición de 1**: R5 toma el primer
tramo interno de la vela (apertura → mínimo), el lector toma la vela
direccional completa. No es un error de umbral: es un error de unidad.

### 5.2 Por qué importa

R5 crea 29 lecturas en 41 minutos, casi una cada 85 segundos, y cada una
reconstruye módulo/A/B/AUT sobre un tramo interno. El lector crea 16
generaciones, una cada 2,5 minutos, sobre velas completas. La diferencia de
granularidad no es cosmética: cambia qué extremo posee cada función y, por
tanto, todos los objetivos TT.

---

## 6. V005 Y EL ESTADO HEREDADO

v005 marca **16:49–17:29 como [D] PENDIENTES de certificación conjunta**. No
hay lectura humana del bloque. Lo único comparable es:

- 16:15–16:24 [A], usado para calibrar H1 (1 = rango de vela) y verificar la
  primera escalera.
- 16:42–16:48 [B], trabajado pero no normalizado; el lector llega a 16:49 con
  una transición C_TREND a las 16:48:15 que v005 no certifica.

En el warm-up el lector reproduce exactamente dos hitos de v005:

1. módulo 16:15+16:16 = 29877,0 → 29848,5 = 28,5;
2. TT principal objetivo 29829,1, confirmado a las 16:24:44,990 con 29829,0.

También reproduce el AUT bajista de 16:18 en 29845,3 (v005: 29843,0, con
frontera 29845,79). La diferencia de 2,3 puntos es el primer tick que cruza
la frontera, no un error de referencia.

En 16:22–16:24 el lector **sí reproduce** el caso canónico de v005. El 16:23
cierra un 1 bajista 29852,6 → 29837,3; el 16:24 abre con gap de −1,4 y el
módulo se extiende hasta 29833,3. A sube 29833,3 → 29840,6 = 7,3; B baja 9,6;
AUT en 29831,0. v005 fija la frontera AUT en 29831,079 y el mínimo en 29843,0
para el ciclo anterior; la diferencia de 2,3 puntos en 16:18 es el primer tick
que cruza la frontera (29845,3), no un cambio de referencia.

La lectura del warm-up queda así alineada con v005 en los hitos verificables:
módulo 28,5, TT 29829,1, A 9,1, AUT 29845,3 y A 7,3 con AUT 29831,0. No se
encontró una divergencia semántica en 16:15–16:24; las diferencias son de
`knowledge_time` frente a `structural_time`.

---

## 7. RESUMEN

| Elemento | Estado |
|---|---|
| TT por generación | 6 confirmados, 9 fallidos, 1 posible |
| TT confirmado después del AUT | 5 de 6 |
| Gaps no planos | 14; 9 marcados como significativos sin umbral canónico |
| A usada como tendencia | 4 |
| C usada como tendencia | 2 |
| Módulos regulares 1-2-3 | 0 |
| Lectura alternativa 1+2 | no desarrollada |
| R5 real | 29 lecturas, 702 eventos; vocabulario completo, semántica distinta |
| v005 del bloque | [D], sin golden |

Ninguna de estas lecturas secundarias se usa para corregir la principal. Se
conservan como evidencia para la Fase B.
