# TM — MISIÓN DE PERFECCIONAMIENTO FINAL
## PREGUNTAS EXPERTAS — CHECKPOINT 1

**Fecha:** 2026-10-30
**Bloque leído:** 16:15–17:29 completo (20.335 ticks)
**Regla:** solo se pregunta lo que el árbol no resuelve. Las tres preguntas
bloquean más de cinco casos cada una; no son dudas locales.

---

## Q1 — DOS LECTURAS EN 16:19: AUT PRINCIPAL Y 1 LOCAL

**MOVIMIENTO**

```text
Estábamos en el AUT bajista principal de 16:18 (B = 12,3; nuevo 1 desde 29857,6).
El precio siguió bajando hasta 29843,0 al cierre de 16:18.
En 16:19 el precio abrió en 29848,9, subió a 29850,0 y bajó a 29842,5:
un recorrido local de 7,5 puntos.
La lectura humana v005 registra simultáneamente:
  - la continuación del AUT principal;
  - un nuevo 1 local bajista de 7,5 (29850,0 → 29842,5).
El lector de cadena única usa como 1 el nuevo 1 principal de 14,6
(29857,6 → 29843,0) y no ve el 1 local de 7,5.
```

**CONCEPTO NO RESUELTO**

El árbol ordena máximo dos escalas activas (v2.4/v2.5), y v2.14 admite
lecturas concurrentes con referencias independientes. Pero OPEN-L2-01
—"AUT local que puede ser nuevo 1 y TT pequeño"— sigue `PENDIENTE_JAVIER`.
No está cerrado si el 1 local de 16:19 abre L2 y convive con L1, o si
sustituye a L1.

**PREGUNTA**

¿El 1 local de 16:19 (7,5) abre una lectura secundaria L2 mientras el AUT
principal sigue gobernando L1, o el 1 local pasa a ser la lectura principal?

**SI L2 SECUNDARIA**

```text
L1 conserva su AUT/TT (objetivo 29829,1).
L2 desarrolla 16:20 = 2, 16:21 = 3, 16:22 = A/AUT.
Las 51 generaciones del lector de cadena única se reparten entre L1 y L2;
la mayoría son ciclos locales, no nuevos 1 primarios.
El TT principal sigue siendo el patrón dominante.
```

**SI L1 SUSTITUIDA**

```text
El 1 local de 7,5 reemplaza al AUT principal.
El TT 29829,1 queda como patrón secundario o se cancela.
Cada AUT local abre una lectura nueva y la cadena de 51 generaciones
se convierte en la lectura principal.
```

**CASOS DESBLOQUEADOS**

16:19–16:24, 16:49–16:52, 17:00–17:05, 17:10–17:18, 17:18–17:29; las 16
generaciones anteriores y las 51 del lector v2.

---

## Q2 — VIDA DE 2 Y 3: CONFIRMACIÓN FRENTE A EXTREMO FINAL

**MOVIMIENTO**

```text
Estábamos en el 1 local de 16:19 (7,5).
16:20 abrió en plano y bajó: 2 candidata.
El 2 alcanzó el 100 % de 1 en 29836,1 a las 16:20:14.
Siguió bajando hasta 29832,5 al cierre de 16:20.
En 16:21 marcó 29830,3 y cerró en 29830,8.
La v005 lee 2 = 12,3 (29844,8 → 29832,5) y 3 = 29830,3.
El lector v2 confirma 3 en 29833,3 a las 16:20:22, antes del mínimo final
de 16:21, y congela ahí el módulo y el origen de A.
```

**CONCEPTO NO RESUELTO**

El árbol dice que 2 se confirma en el primer tick que alcanza el 100 % de 1
(v2.13) y que 3 se confirma en el primer tick que supera estrictamente el
extremo de 2. Pero también dice que A Grande nace desde el **extremo final
real de 3** (v2.15). No está cerrado si el extremo de 2/3 se congela en la
confirmación o sigue extendiéndose hasta su extremo final.

**PREGUNTA**

Cuando 2 confirma al 100 % y después sigue haciendo extremo, y cuando 3
confirma y después sigue haciendo extremo, ¿el módulo y el origen de A se
fijan en el tick de confirmación o en el extremo final real de 2 y 3?

**SI EXTREMO FINAL**

```text
Módulo local = 29850,0 → 29830,3 = 19,7.
A = 29830,3 → 29850,8 = 20,5.
A supera la base local 29850,0 en 0,8 → AUT alcista en 29850,8.
Se reproduce la v005 de 16:22.
```

**SI TICK DE CONFIRMACIÓN**

```text
Módulo local = 29850,0 → 29833,3 = 16,7.
A = 29833,3 → 29850,8 = 17,5.
El nuevo 1 de 16:22 nace antes y el TT local cambia 3,0 puntos.
La cadena de 16:23–16:24 se adelanta y no reproduce la v005.
```

**CASOS DESBLOQUEADOS**

Todos los módulos 1+2 y 1+2+3; 16:20–16:24; 16:50–16:52; 17:18–17:22;
la medida del TT local y principal.

---

## Q3 — B/AUT CUANDO B SUPERA LA BASE DEL MÓDULO ANTES DEL 127 % + 0,25

**MOVIMIENTO**

```text
Estábamos en el 3 local de 16:21 (29830,3).
16:22 desarrolló A alcista 29830,3 → 29850,8 (20,5) y superó la base local
29850,0 en 0,8: AUT alcista y nuevo 1 alcista.
16:23 abrió en 29846,8; bajó a 29842,8 (A = 8,0) y subió a 29852,6 (B = 9,8).
B alcanzó el 122,5 % de A.
La v005 dice que B supera el inicio de A (29850,8) y confirma AUT alcista.
El árbol v2.2/v2.18 dice que entre 100 % y 127 % + 0,25 B es B Grande;
AUT exige superar estrictamente 127 % + 0,25 = 10,41.
```

**CONCEPTO NO RESUELTO**

La v005 [A] aplica la superación de la base del módulo como condición de AUT
para un B que todavía no alcanzó 127 % + 0,25. El árbol reserva la base del
módulo para A usada como tendencia (v2.3 F) y para C usada como tendencia
(v2.17). No está cerrado si B también puede convertir el módulo en tendencia
al superar su base antes del 127 % + 0,25.

**PREGUNTA**

Cuando B supera la base del módulo pero no alcanza 127 % + 0,25, ¿sigue
siendo B Grande hasta el límite, o confirma AUT por la superación de la base?

**SI B GRANDE HASTA 127 % + 0,25**

```text
B = 9,8 < 10,41 → B Grande.
El giro posterior es C Grande; CUT en 29841,8; C_TREND en 29829,9.
El 16:24 A 7,3/B/AUT 29831,079 no se recorre en esta rama.
```

**SI AUT POR BASE DEL MÓDULO**

```text
B = 9,8 supera 29850,8 → AUT alcista en 16:23:12.
El AUT alcista es nuevo 1; el 16:24 A 7,3/B/AUT 29831,079 se recorre.
La v005 de 16:23–16:24 se reproduce.
```

**CASOS DESBLOQUEADOS**

16:23–16:24, 16:50–16:52, 17:18–17:22, 17:25–17:29; la frontera B/AUT y la
diferencia entre B Grande y C usada como tendencia.

---

## ORDEN DE PRIORIDAD

```text
Q1 (concurrencia L1/L2) → Q2 (vida de 2/3) → Q3 (B/AUT en la base)
```

Q1 decide cuántas lecturas existen. Q2 decide la medida del módulo y el
origen de A. Q3 decide la frontera B/AUT y el encadenamiento de 16:23–16:24.

Ninguna de las tres puede resolverse con un umbral fijo. Las tres tienen
consecuencias sobre más de cinco casos.
