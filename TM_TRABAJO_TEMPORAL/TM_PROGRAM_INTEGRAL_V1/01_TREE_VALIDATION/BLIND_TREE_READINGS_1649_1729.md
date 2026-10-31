# TM — FASE A — LECTURA CIEGA 16:49–17:29

- **Fuente física:** `TM_CANON_ACTIVO/02_TICKS/TM_TICKFEED_1615_1730.csv`
- **SHA-256 del tickfeed:** `5F701BE2307352CB559ABBD7BB856A6FD2A1F91E5D269A93DCC9AE2992E2C9FF`
- **Árbol:** `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md`
- **SHA-256 del árbol:** `94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17`
- **Estado del árbol:** `WORKING_CANON_NOT_FROZEN`
- **Instrumento:** `blind_reader.py` (lector de Fase A; **no** es el motor oficial)
- **Bloque:** 16:49:00.012 → 17:29:59.897 (secuencias 8922–20335, 11.414 ticks)
- **tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

> **ERRATA 2026-10-30.** La auditoría funcional de las 16 generaciones
> (`PHASE_A_GENERATION_AUDIT.md`) corrige dos datos de este acta: el recuento
> de AUT es **9**, no 8 (13, 14, 15, 16, 19, 21, 23, 24, 26), y la gen 23 tiene
> módulo **24,7** (29656,1 → 29680,8) y AUT **17:18:09.401**, no 17:18:07.395.
> El acta se conserva como evidencia original de la Pasada A; la fuente de
> verdad de la tabla es `BLIND_TREE_GENERATIONS_1649_1729.csv`.
>
> Esta es **una lectura válida bajo políticas explícitas**, no la lectura canónica.
> Las políticas H1–H7 están declaradas en §1 y sus consecuencias se auditan en
> `BLIND_TREE_CONCEPTUAL_GAPS.md`. La Pasada A se bloqueó antes de consultar
> v005. v005 marca todo el bloque como **[D] PENDIENTE**, por lo que no existe
> golden humano contra el que comparar.

---

## 0. ESTADO HEREDADO A 16:48:59.811

La lectura no empieza de cero. El bloque anterior se leyó con el mismo
instrumento desde 16:15 y entrega este estado vivo:

```text
SECUENCIA 8921 · 16:48:59.811
LECTURA R001 · GENERACIÓN 12
FASE: WAIT_ONE
FUNCIÓN ACTIVA: 1 (pendiente de la vela siguiente)
MOTIVO DE TRANSICIÓN: C_USED_AS_TREND a las 16:48:15.900
  C = 29666,1 supera la base del módulo = 29666,4
PATRÓN ARCHIVADO: TT generación 11
  objetivo = 29781,1 · estado = FAILED
```

La transición de 16:48 proviene de una C que supera la base del módulo por
0,3 puntos. El lector la trata como `C_USED_AS_TREND` y abre una nueva
generación. La primera vela del bloque, 16:49, es el nuevo 1.

---

## 1. POLÍTICA DE LECTURA

### 1.1 Reglas cerradas aplicadas

| Regla | Aplicación en el lector |
|---|---|
| 4.1 plano | `|Open − Close_previo| < 0,25` estricto; 0,25 no es plano |
| 4.2 función 2 | misma dirección que 1, apertura plana, sin cola prohibitiva, 100 % de 1 |
| 4.3 función 3 | retroceso válido, recuperación y superación estricta del extremo de 2 |
| 4.4 A/B/C/AUT | 100 % de A; 127 % + 0,25 inclusive; AUT estricto |
| 4.5 AUT | abre nuevo 1; la siguiente vela es la nueva 1 local |
| 4.6 gap | sin 2; resolución implícita; no se inventan ticks |
| 4.7 umbral 2 puntos | distingue ruido; no crea función por sí solo |
| 4.8 TT | patrón; confirma en el primer tick que alcanza el objetivo |
| 4.9 concurrencia | patrones TT y transiciones se conservan por generación |
| 4.10 tiempos | `structural_time` y `knowledge_time` separados |

### 1.2 Políticas explícitas (H), no canónicas

| ID | Política | Justificación | Riesgo |
|---|---|---|---|
| **H1** | 1 se mide por el rango direccional de su vela: origen = mínimo (alcista) o máximo (bajista), extremo = opuesto | v005 16:15: 1 bajista = 16,2 = rango de la vela; 16:16 = 12,6 | una vela no monótona puede tener dos lecturas de 1 |
| **H2** | A se confirma con **6,00 puntos** contrarios (mínimo teórico v2.5) | evita que 2 puntos creen A; v005 usa A de 7,3 y 9,1 | el bloque cambia con 12,00 puntos (16 → 9 generaciones) |
| **H3** | retroceso válido de 2: ≥ 2,00 puntos y ≤ 50 % de 2 | 50 % es la frontera que el mandato manda investigar | exactamente 50 % queda pendiente, no confirmado |
| **H4** | B Grande es hito monotónico; A puede seguir extendiéndose antes de B | v2.18: A conserva origen y actualiza extremo | A puede crecer después de B Grande |
| **H5** | TT se evalúa en cada tick | 4.8: no espera cierre de movimiento | ninguno |
| **H6** | el TT de una generación sobrevive al AUT como patrón | 4.8 y 4.9 | el TT puede confirmarse después de la transición |
| **H7** | el gap se registra como resolución implícita esbozada; no se desarrolla como escalera completa | 4.6 prohíbe inventar ticks | el lector no mide la A/B implícitas del gap |

### 1.3 Reglas abiertas que el lector no decide

`Q_ONE_DEFINITION`, `Q_A_AUTONOMY`, `Q_GAP`, `Q_MODULE_MEASURE`,
`Q_TWO_LIFECYCLE`, `Q_BASE`, `Q_AUT_NEW_ONE`, `Q_DOMINANCE`,
`Q_CONCURRENCY`, `Q_FT`, `Q_50`, `Q_TT_FAILURE`, `Q_AB_ABSORPTION`,
`Q_C_ABSORPTION`. Se detallan en `BLIND_TREE_CONCEPTUAL_GAPS.md`.

---

## 2. LECTURA — 16 GENERACIONES

Precios en puntos. `1` es la vela del nuevo ciclo; `M` el módulo; `A`, `B` las
funciones contrarias; `TT` el objetivo del patrón. `FIN` es la transición que
cierra la generación.

| Gen | 1 (kt) | 1 origen → extremo | 1 | M origen → extremo | M | A | B | FIN | TT |
|---:|---|---|---:|---|---:|---:|---:|---|---:|
| 12 | 16:49:59,949 | 29666,4 → 29699,9 | 33,5 | 29666,4 → 29699,9 | 33,5 | 16,2 | 17,1 | C_TREND 16:50:32,234 | 29717,2 |
| 13 | 16:51:59,859 | 29675,8 → 29611,2 | 64,6 | 29675,8 → 29611,2 | 64,6 | 13,6 | 17,7 | AUT 16:52:17,291 | 29560,2 |
| 14 | 16:53:59,965 | 29622,9 → 29642,1 | 19,2 | 29622,9 → 29642,3 | 19,4 | 13,0 | 17,3 | AUT 16:54:27,442 | 29648,7 |
| 15 | 16:55:59,872 | 29680,4 → 29647,1 | 33,3 | 29680,4 → 29643,8 | 36,6 | 6,3 | 8,5 | AUT 16:56:05,283 | 29613,5 |
| 16 | 16:57:59,821 | 29600,2 → 29625,1 | 24,9 | 29600,2 → 29625,1 | 24,9 | 7,7 | 12,7 | AUT 16:58:04,242 | 29642,3 |
| 17 | 16:59:59,791 | 29623,6 → 29641,1 | 17,5 | 29623,6 → 29641,1 | 17,5 | 17,9 | — | A_TREND 17:00:08,407 | 29643,1 |
| 18 | 17:01:59,880 | 29617,6 → 29671,8 | 54,2 | 29617,6 → 29671,8 | 54,2 | 33,4 | 38,7 | C_TREND 17:07:02,847 | 29692,6 |
| 19 | 17:08:59,967 | 29616,9 → 29653,6 | 36,7 | 29616,9 → 29653,6 | 36,7 | 8,2 | 10,7 | AUT 17:09:23,432 | 29682,1 |
| 20 | 17:10:59,902 | 29634,8 → 29590,2 | 44,6 | 29634,8 → 29585,1 | 49,7 | 51,0 | 2,0 | A_TREND 17:11:49,457 | 29584,9 |
| 21 | 17:12:59,859 | 29615,3 → 29635,8 | 20,5 | 29615,3 → 29637,7 | 22,4 | 9,9 | 13,5 | AUT 17:13:17,706 | 29650,2 |
| 22 | 17:14:59,961 | 29653,8 → 29679,3 | 25,5 | 29653,8 → 29679,3 | 25,5 | 26,0 | 3,9 | A_TREND 17:15:37,388 | 29679,3 |
| 23 | 17:16:59,990 | 29656,1 → 29680,8 | 24,7 | 29656,1 → 29680,8 | 24,7 | 8,5 | 13,6 | AUT 17:18:09,401 | 29697,0 |
| 24 | 17:19:59,908 | 29669,8 → 29641,6 | 28,2 | 29669,8 → 29641,6 | 28,2 | 27,6 | 37,9 | AUT 17:21:21,925 | 29641,0 |
| 25 | 17:22:59,838 | 29633,6 → 29678,3 | 44,7 | 29633,6 → 29678,3 | 44,7 | 46,2 | 0,0 | A_TREND 17:25:41,128 | 29681,1 |
| 26 | 17:26:59,964 | 29640,1 → 29616,7 | 23,4 | 29640,1 → 29611,9 | 28,2 | 12,3 | 17,1 | AUT 17:27:51,920 | 29596,0 |
| 27 | 17:28:59,932 | 29618,1 → 29594,4 | 23,7 | 29618,1 → 29594,4 | 23,7 | 21,7 | 3,7 | ABIERTA AL FINAL | 29592,4 |

**Recuento de transiciones:** AUT 9 · A_USED_AS_TREND 4 · C_USED_AS_TREND 2 ·
abierta 1. **Módulos regulares 1-2-3: 0.** **Módulos por descarte: 16/16.**

El dato estructural más importante del bloque no es una etiqueta: en 41 velas
**no se completó ni un solo módulo regular 1-2-3**. La causa es la regla 4.2:
2 exige apertura plana y 100 % de 1; catorce de las dieciséis velas abrieron
con diferencia ≥ 0,25 y nunca hubo 2. El bloque se leyó entero como módulos
por descarte. Esto es coherente con el árbol, pero convierte la medida del
módulo y la propiedad del extremo en el problema central (Q_MODULE_MEASURE).

---

## 3. CASOS PRINCIPALES

### 3.1 16:49–16:50 — primer ciclo del bloque (gen 12)

La vela 16:49 abre 29680,8, baja a 29666,4 y sube a 29699,9; cierra 29689,9.
H1 la lee como 1 alcista de 33,5. La vela 16:50 abre 29686,8, con gap de
−3,1 respecto del cierre 29689,9: **no hay 2**. El módulo es 1 solo,
29666,4 → 29699,9 = 33,5.

A baja desde 29699,9. Se confirma a los 6,00 puntos en 29693,9 y se extiende
hasta 29683,7 (A = 16,2). B sube; B Grande al recuperar 29699,9 (B = 17,1);
C baja y cruza el final de A en 29683,7 (CUT 16:50:24,206); después cruza la
base del módulo 29666,4 y se convierte en `C_USED_AS_TREND` (16:50:32,234).
El TT de la generación apunta a 29717,2 y queda `POSSIBLE`.

Este caso fija la diferencia con R5: R5 crea su primera lectura a las
16:49:06 con módulo 29680,8 → 29666,4 = 14,4 (el primer tramo bajista dentro
de la vela), no con la vela completa. La divergencia es de definición de 1,
no de umbral.

### 3.2 16:51–16:52 — el mayor 1 del bloque (gen 13)

La vela 16:51 abre 29675,8 y cae a 29611,2: 1 bajista de 64,6. La vela 16:52
abre 29617,1, con gap de −0,7: no hay 2. Módulo = 64,6.

A sube desde 29611,2. Se confirma en 29617,2 y se extiende a 29624,8 (A = 13,6).
Frontera AUT:

```text
13,6 × 1,27 + 0,25 = 17,522
nivel AUT = 29624,8 − 17,522 = 29607,278
primer tick por debajo = 29607,1  →  AUT 16:52:17,291
```

B Grande se había confirmado al recuperar 29611,2 (100 % de A). TT objetivo:
29624,8 − 64,6 = 29560,2. La generación termina por AUT; el TT sigue vivo como
patrón y se confirmará o fallará en las generaciones siguientes.

### 3.3 17:01–17:07 — módulo grande y C que se convierte en tendencia (gen 18)

La vela 17:01 abre 29624,9 y sube a 29671,8: 1 alcista de 54,2. La vela 17:02
abre 29663,1, gap −0,9: sin 2. Módulo 54,2.

A baja hasta 29638,4 (A = 33,4, el 61,6 % del módulo). B sube hasta 29676,3
(B = 38,7) y confirma B Grande. C baja; cruza el final de A en 29638,4
(CUT 17:05:41,048) y sigue hasta 29615,6, por debajo de la base 29617,6:
`C_USED_AS_TREND` a las 17:07:02,847. El TT (29692,6) queda `FAILED` porque el
precio retorna a la base antes de alcanzarlo.

Este caso es la aplicación literal de 4.4 y v2.17. La discusión abierta no es
la transición, sino si C debe medirse contra el final de A, contra la base del
módulo o contra ambas (Q_BASE).

### 3.4 17:10–17:11 — V y A usada como tendencia (gen 20)

La vela 17:10 abre 29633,8 y cae a 29590,2: 1 bajista de 44,6. La vela 17:11
abre 29590,7, gap −0,1: plano. La 2 se evalúa al alza, pero la vela sube con
fuerza; el módulo se extiende a 29634,8 → 29585,1 = 49,7.

A sube desde 29585,1. A los 6,00 puntos se confirma en 29591,1; sigue subiendo
hasta 29636,1. En ese punto:

```text
A = 29636,1 − 29585,1 = 51,0  >  módulo = 49,7
→ A_USED_AS_TREND 17:11:49,457
→ nuevo 1 desde la vela 17:12
```

A supera la base del módulo por 1,3 puntos. Es la transición que impide que A
crezca indefinidamente y la que sostiene la lectura del giro. Sin ella, el
lector habría extendido A durante 27 minutos y habría perdido toda la
estructura posterior; fue el primer defecto detectado en la pasada de prueba.

### 3.5 17:19–17:21 — A profunda, B Grande y AUT (gen 24)

La vela 17:19 abre 29669,8 y cae a 29641,6: 1 bajista de 28,2. La vela 17:20
abre 29664,6, gap −0,8: sin 2. Módulo 28,2.

A sube desde 29641,6 hasta 29669,2 (A = 27,6, el 97,9 % del módulo). B baja.
Frontera AUT:

```text
27,6 × 1,27 + 0,25 = 35,302
nivel AUT = 29669,2 − 35,302 = 29633,898
B Grande en 29641,6 (100 %)
AUT en 29631,3  →  17:21:21,925
```

TT objetivo = 29669,2 − 28,2 = 29641,0. Se confirma durante B y se extiende
hasta 29631,3. Es el único TT del bloque que termina `EXTENDED`.

### 3.6 17:22–17:25 — módulo por descarte con 2 que no supera a 1 (gen 25)

La vela 17:22 abre 29638,1, sube a 29678,3 y cierra 29664,1: 1 alcista de 44,7.
La vela 17:23 abre 29664,3, con diferencia +0,2 (plano). La 2 se evalúa al alza,
pero solo alcanza 29664,4 y retrocede: no llega al 100 % de 1 y termina la vela.
Módulo por descarte:

```text
origen = 29633,6
extremo = máximo(1 = 29678,3; 2 = 29664,4) = 29678,3
medida = 44,7
```

Este caso obligó a corregir la propiedad del extremo: si el módulo se midiera
solo con el extremo de 2, mediría 30,8 y perdería 13,9 puntos de 1. La regla
adoptada (H1 + extremo más lejano) es la que sostiene la lectura.

A baja desde 29678,3. A = 46,2 > módulo 44,7 en 29632,1:
`A_USED_AS_TREND` a las 17:25:41,128. El TT (29681,1) queda `POSSIBLE`.

### 3.7 17:26–17:29 — último ciclo y estado abierto (gen 26 y 27)

La vela 17:26 abre 29635,2 y cae a 29616,7: 1 bajista de 23,4. La vela 17:27
abre 29618,7, con diferencia +0,6: sin 2. Pero el módulo se extiende con el
mínimo de 17:26 (29611,9): 28,2.

A sube a 29624,2 (A = 12,3); B baja; AUT en 29607,1 a las 17:27:51,920.
La vela 17:28 abre 29607,1 y cae a 29594,4: nuevo 1 bajista de 23,7.
La vela 17:29 abre 29603,6, con diferencia −0,8: sin 2. Módulo 23,7.

A sube desde 29594,4 hasta 29616,1 (A = 21,7). B baja hasta 29612,4 y queda
**B candidata con 3,7 puntos** cuando termina el feed a las 17:29:59,897.
No hay AUT ni cierre: la lectura queda abierta, con TT `POSSIBLE` en 29592,4.

---

## 4. LECTURA MACRO Y DOMINANCIA

El bloque no es una tendencia única. Es una secuencia de dieciséis ciclos
funcionales dentro de un rango de 109,7 puntos:

```text
máximo 16:49 = 29699,9
mínimo 17:10 = 29590,2
máximo 17:18 = 29685,9
mínimo 17:28 = 29594,4
cierre 17:29 = 29612,4
```

Los cuatro desplazamientos dominantes, medidos por el tamaño de su 1, son:

| Ventana | 1 | Dirección | Función que la cierra |
|---|---:|---|---|
| 16:51 | 64,6 | bajista | AUT 16:52:17 |
| 17:01 | 54,2 | alcista | C_TREND 17:07:02 |
| 17:10 | 44,6 (módulo 49,7) | bajista | A_TREND 17:11:49 |
| 17:22 | 44,7 | alcista | A_TREND 17:25:41 |

Si se lee por ciclos, la dominante es una alternancia de impulsos grandes y
retrocesos de 6–46 puntos. Si se lee por tramos, el bloque contiene tres
tramos humanos evidentes:

1. **16:49–17:10:** descenso de 29699,9 a 29590,2 (−109,7), con el 1 de 64,6
   como impulso principal y dos ciclos intermedios.
2. **17:10–17:18:** recuperación de 29590,2 a 29685,9 (+95,7), con el
   `A_USED_AS_TREND` de 51,0 como giro y el 1 de 36,7 de 17:08 como primer
   tramo.
3. **17:18–17:29:** descenso de 29685,9 a 29594,4 (−91,5), con los 1 de 28,2
   y 23,4/23,7.

**El lector no produce esa lectura de tres tramos.** Produce dieciséis
generaciones y no tiene ninguna regla para agregarlas en un movimiento
dominante. La lectura macro de arriba es una reconstrucción humana sobre la
salida, no una salida del instrumento. Ésta es la diferencia entre *trazabilidad
de funciones* y *lectura dominante*, y queda registrada como Q_DOMINANCE.

---

## 5. VERIFICACIÓN

| Comprobación | Resultado |
|---|---|
| Ticks del bloque | 11.414 (8922–20335), sin huecos |
| Secuencias | consecutivas; `sequence_id` inicial 8922, final 20335 |
| Generaciones | 16 (12–27) |
| Módulos regulares 1-2-3 | 0 |
| Módulos por descarte | 16 |
| Doble ejecución | hash `b219049b26d1221905b7451a92ba4710ea6b7103e54f7088fa74ca230656eede` idéntico |
| Prefijos | 41/41 idénticos al estado del tick correspondiente |
| Excepciones | 0 |
| Información futura | no usada; prefijos consistentes |
| Hardcoding | ninguno: no hay horas, precios ni secuencias en el código |
| Originales modificados | ninguno |

El detalle por tick está en `BLIND_TREE_TRACE_1649_1729.jsonl`; los eventos en
`BLIND_TREE_EVENTS_1649_1729.csv`; el estado al cierre de cada vela en
`BLIND_TREE_STATE_AT_BAR_CLOSE.csv`; la tabla de generaciones en
`BLIND_TREE_GENERATIONS_1649_1729.csv`.

---

## 6. LÍMITES

1. **No hay golden humano del bloque.** v005 lo marca [D]. La comparación con
   v005 sólo alcanza al estado heredado y al warm-up 16:15–16:24.
2. **La lectura depende de H1, H2 y H7.** Con A = 12,00 puntos el bloque pasa
   de 16 a 9 generaciones; con A = 20,00, a 11. La cifra 16 no es canónica.
3. **La concurrencia es parcial.** Se conservan los TT por generación y se
   registran las transiciones A/C usadas como tendencia, pero no se desarrolla
   en paralelo la lectura alternativa 1+2 → A → B de v2.14.
4. **El gap no se mide.** Se registra la resolución implícita y el nuevo 1
   observable, pero no se inventan los extremos internos de A/B (H7).
5. **FT queda bloqueado.** No se emite confirmación estructural de FT porque el
   árbol no fija su condición exacta (Q_FT).
6. **La lectura macro no es salida del instrumento.** Es una reconstrucción
   humana; el instrumento sólo entrega la cadena de generaciones.

---

## 7. CONCLUSIÓN DE LA PASADA A

El árbol **sí puede recorrer los 11.414 ticks** y producir una lectura
funcional completa, determinista y sin información futura. No necesita
inventar funciones: usa 1, 2, 3, A, B, C, AUT y CUT, y conserva TT como patrón.

Lo que el árbol **no decide** es:

- cuál es la unidad de 1 cuando la vela no es monótona;
- cuánta autonomía necesita A para ser A y no ruido;
- cuándo un hueco de apertura es un gap funcional y cuándo sólo un no-plano;
- cómo se agregan dieciséis ciclos en una lectura dominante;
- cómo conviven la lectura regular y la alternativa sin mezclar referencias.

Esos cinco puntos son la materia de la Fase B. Ninguno impide avanzar: el
Gate A se cumple porque la lectura es trazable, determinista, por prefijos y
sin spoilers. **GATE A = PASS CON CUESTIONES ABIERTAS.**
