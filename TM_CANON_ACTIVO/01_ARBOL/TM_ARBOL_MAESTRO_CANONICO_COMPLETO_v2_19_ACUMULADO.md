# TM - ARBOL MAESTRO CANONICO COMPLETO v2.19 ACUMULADO

- **Fecha de consolidacion:** 2026-10-22
- **Revision v2.1:** correccion canonica de concurrencia en velas 5 y 6 (23:43-23:44).
- **Revision v2.2:** continuidad integral de B, oscilaciones internas absorbidas y conversion de A Grande en modulo por descarte.
- **Revision v2.3:** arbol determinista posterior a 1 y bifurcacion cronologica completa de gap: primero sube o primero baja.
- **Revision v2.4:** simplificacion de escalas, maximo modulo principal mas un mini modulo, integracion condicional y definicion obligatoria de movimientos.
- **Revision v2.5:** prioridad de modulos grandes, separacion lectura/operabilidad y filtro minimo teorico de 6 puntos.
- **Revision v2.6:** puntos decisivos operativos conceptuales AUT y FT; primer nivel de gestion en TT 100 %, sin cierre automatico; variables pendientes.
- **Revision v2.7:** prioridad cronologica absoluta cuando existe TT pendiente: comprobar TT antes de final de A; TT primero cierra y resetea, final de A primero invalida y reclasifica.
- **Revision v2.8:** ontologia formal cerrada: funciones 1, 2, 3, A, B, C, AUT, CUT; patrones TT y FT; cinco variables exclusivas.
- **Revision v2.9:** fundamento teorico de probabilidad condicionada y marco preliminar de las cinco variables.
- **Revision v2.10:** cierre teorico de Variable 1 Patron y Variable 2 Velocidad; separacion absoluta entre lectura TM y consulta de variables.
- **Revision v2.11:** definicion teorica de Variable 3 Solapamiento frente a verticalidad, escala visual 0-10 y arquitectura futura para codigo.
- **Revision v2.12:** Variable 4 Tiempo M1/M3, Variable 5 Estructura y principio constitucional de independencia absoluta entre lectura, variables y decision.
- **Revision v2.13:** continuidad integral de 2 candidata dentro de su vela; vibraciones internas absorbidas; confirmación al 100 % de 1 y descarte al cierre si no lo alcanza.
- **Revision v2.14:** concurrencia posterior a 2 confirmado: lectura regular de 3 y lectura alternativa módulo-A-B-AUT con referencias separadas.
- **Revision v2.15:** después de 3 viene A Grande del módulo regular completo 1-2-3, desde el extremo final real de 3.
- **Revision v2.16:** el retroceso posterior a AUT/nuevo 1 no se clasifica automáticamente como A Grande por distancia fija; queda pendiente hasta disponer de evidencia funcional suficiente.
- **Autoridad experta:** Javier Armada Lopez
- **Estado:** MAESTRO CANONICO CONSOLIDADO
- **Objeto:** arbol profesional unico de Teoria Modular (TM), con reglas activas, precedencia, ramas, escenarios, parches y trazabilidad integra.
- **Principio de integridad:** no se elimina informacion historica. Las reglas posteriores corrigen o completan las anteriores sin borrar el rastro documental.

> **REGLA DE USO OBLIGATORIA:** antes de responder sobre una secuencia de velas o ticks se recorre el arbol completo, se reconstruye el orden cronologico real y se exponen todos los escenarios TM coherentes. Normalmente habra una o dos lecturas; excepcionalmente tres. Nunca se inventa una cuarta lectura ni se omite una alternativa matematicamente valida.

- **Revision v2.17:** después de B Grande, si C Grande supera la base del módulo, C se convierte en C Grande usada como tendencia y en nuevo 1 en su propia dirección. La referencia decisiva es la base del módulo, no únicamente el final de A.
- **Revision v2.18:** aplicación directa y obligatoria de la secuencia básica tras nuevo 1: recorrido contrario funcional = A Grande; giro contrario a A = B candidata; 100 %-127 % + 0,25 = B Grande; superación estricta = AUT. No volver a consultar esta transición cuando las referencias sean inequívocas.
- **Revision v2.19:** lectura funcional del gap: entre el cierre de una vela y la apertura distante de la siguiente se consideran recorridas implícitamente A Grande, B Grande y A Grande usada como tendencia; esta última nace en la apertura de la segunda vela y pasa a ser el nuevo 1 desde el que continúa la lectura observable.
## 0. PRECEDENCIA CANONICA

En caso de solapamiento o contradiccion, se aplica este orden:

1. Correccion expresa mas reciente de Javier.
2. Reglas consolidadas posteriores: filtro de ruido de 2 puntos y aclaraciones de 2026-10-21.
3. `TM_PATCH_CANONICO_v1_2_C_CUT_TERCERO_RESET.md`.
4. `TM_PATCH_CANONICO_v1_1_RESET_TT_VELAS8_9.md`.
5. `TM_PATCH_CANONICO_v1_0_TT_FT_CONCURRENCIA_VELA7.md`.
6. `TM_ARBOL_MAESTRO_CANONICO_v0_9_SALIDA_MOVIMIENTOS_PATRONES_TT.md`.
7. `TM_ARBOL_CANONICO_COMPLETO_v1.md`, salvo donde sus dudas hayan quedado resueltas por reglas posteriores.
8. Versiones v0.8, v0.7, v0.6, v0.5 y v0.1 como trazabilidad historica y apoyo.

## 0.0.-3. PATCH CANONICO v2.19 - LECTURA FUNCIONAL DEL GAP COMO A-B-AUT IMPLICITOS
**Estado:** `CONFIRMADO_JAVIER`

**Finalidad:** fijar la lectura causal del tramo no negociado entre el cierre de una vela y una apertura con gap significativo. El gap no se trata como una única A Grande medida desde el extremo anterior hasta el primer precio negociado. Dentro del tramo implícito se consideran recorridas las funciones necesarias A Grande, B Grande y A Grande usada como tendencia.

### A. Regla funcional del gap
Si una vela cierra y la siguiente abre a una distancia significativa en sentido contrario o de resolución respecto de la estructura activa:

```text
CIERRE VELA ANTERIOR
→ tramo de gap no observado tick a tick
→ A GRANDE implícita
→ B GRANDE implícita
→ A GRANDE USADA COMO TENDENCIA implícita
→ APERTURA DE LA SEGUNDA VELA = origen operativo del nuevo 1
```

El motor debe reconocer que en el tramo del gap se han producido funcionalmente A Grande, B Grande y A Grande usada como tendencia, aunque no existan ticks intermedios para reconstruir sus extremos exactos.

### B. Origen del nuevo 1
A Grande usada como tendencia termina causalmente en la apertura negociada de la segunda vela. Desde esa apertura nace la referencia operativa del nuevo 1:

```text
ORIGEN_NUEVO_1 = OPEN de la segunda vela
STRUCTURAL_TIME_NUEVO_1 = primer tick negociado de la segunda vela
KNOWLEDGE_TIME_NUEVO_1 = primer tick negociado de la segunda vela
```

La lectura posterior continúa desde esa apertura. No se mide el nuevo 1 desde el cierre anterior ni desde el extremo previo al gap.

### C. Tratamiento de las funciones implícitas
Las funciones internas del gap deben conservar estas propiedades:

1. Se registran como implícitas por ausencia de ticks intermedios.
2. No se inventan precios internos exactos para A o B.
3. No se simulan ticks inexistentes.
4. Sí se conserva la secuencia funcional `A → B Grande → A usada como tendencia`.
5. La apertura observable fija el origen de la nueva tendencia/nuevo 1.
6. Después de la apertura, la lectura vuelve a ser completamente tick a tick.

### D. Caso canónico 16:24-16:25
```text
Cierre 16:24 = 29834,5
Apertura 16:25 = 29848,5
Gap alcista = 14,0 puntos
```

En el tramo del gap:

```text
A Grande implícita
→ B Grande implícita
→ A Grande usada como tendencia implícita
```

Por tanto:

```text
Apertura 16:25 en 29848,5
→ origen operativo del nuevo 1 alcista
```

El avance posterior desde `29848,5` se mide como desarrollo del nuevo 1 alcista. No debe medirse como una única A Grande desde el mínimo previo `29828,1` hasta `29860,1`.

### E. Relación con la prohibición de 2
La presencia de gap impide abrir 2 según la rama regular. Esta prohibición no deja el tramo sin lectura: activa la resolución funcional implícita del gap y entrega un nuevo 1 desde la apertura.

```text
GAP
→ NO_TWO
→ resolución A/B/A usada como tendencia implícita
→ nuevo 1 desde la apertura
```

### F. Prohibiciones de regresión
- No medir todo el gap como una única A Grande desde el extremo anterior.
- No fijar el origen del nuevo 1 en el cierre previo.
- No inventar extremos internos exactos sin ticks.
- No omitir B Grande implícita dentro de la resolución del gap.
- No permitir 2 cuando existe gap.
- No continuar la lectura posterior desde una referencia anterior a la apertura.

## 0.0.-2. PATCH CANONICO v2.18 - EJECUCION DIRECTA DE A-B-AUT
**Estado:** `CONFIRMADO_JAVIER`

Cuando un nuevo 1 está confirmado y el recorrido contrario posee autonomía funcional suficiente para ser A Grande, la secuencia posterior se aplica directamente, sin volver a pedir confirmación experta en casos inequívocos:

```text
NUEVO 1
→ A GRANDE contraria
→ giro contrario a A = B CANDIDATA
→ 100 % de A hasta 127 % de A + 0,25 inclusive = B GRANDE
→ superación estricta de 127 % + 0,25 = AUT
```

Caso 16:24:

```text
nuevo 1 bajista continúa hasta 29833,3
A Grande alcista: 29833,3 → 29840,6 = 7,3 puntos
B bajista desde 29840,6
B Grande al alcanzar 29833,3
AUT bajista al bajar estrictamente de 29831,079
extensión posterior hasta 29828,1
```

La oscilación interna que vuelve a `29833,3` antes de alcanzar `29840,6` no fragmenta A Grande: A conserva su origen `29833,3` y actualiza su extremo hasta `29840,6`.

**Prohibición de regresión:** no volver a preguntar una transición básica A→B→B Grande→AUT cuando el árbol, los extremos y las fronteras matemáticas la resuelvan inequívocamente. Solo preguntar ante una ambigüedad real no cubierta por el árbol.

## 0.0.-1. PATCH CANONICO v2.17 - C GRANDE USADA COMO TENDENCIA
**Estado:** `CONFIRMADO_JAVIER`

**Finalidad:** cerrar la transición posterior a B Grande cuando C Grande continúa, supera la base del módulo y adquiere función de tendencia.

### A. Secuencia de entrada
La precondición es una lectura que ya contiene módulo, A Grande, B Grande confirmada y C Grande vigente:

```text
MÓDULO
→ A GRANDE
→ B GRANDE confirmada entre 100 % y 127 % + 0,25 de A
→ giro contrario a B
→ C GRANDE
```

Antes de B Grande no puede existir C Grande.

### B. Referencia decisiva
Mientras C Grande no supere la base del módulo, continúa como C Grande de la lectura activa y se evalúan las demás referencias aplicables.

Cuando C Grande supera la base del módulo en su propia dirección:

```text
C GRANDE supera la BASE DEL MÓDULO
→ C GRANDE USADA COMO TENDENCIA
→ NUEVO 1 en la dirección de C
```

La superación de la base del módulo es la condición funcional decisiva para esta conversión. No basta únicamente con superar el final de A si la base del módulo todavía no ha sido superada.

### C. Ejemplo conceptual confirmado
```text
Módulo = 15 puntos
A Grande = 5 puntos
B Grande = 5 puntos = 100 % de A
C Grande = 25 puntos
```

Si C Grande continúa y supera la base del módulo:

```text
C Grande
→ C Grande usada como tendencia
→ nuevo 1
```

La magnitud de 25 puntos no es por sí sola la regla; lo determinante es que C Grande, ya válida después de B Grande, supera la base estructural del módulo.

### D. Caso canónico 16:23
Referencias:

```text
A Grande bajista: 29850,8 → 29842,8 = 8,0 puntos
B alcista: 29842,8 → 29852,6 = 9,8 puntos
B alcanza el 100 % en 29850,8
Límite AUT alcista = 29853,21
Máximo real de B = 29852,6
```

Como B alcanza el 100 % sin superar el límite AUT, queda confirmada como B Grande. La bajada posterior es C Grande.

Si esa C Grande supera la base del módulo aplicable:

```text
C Grande bajista
→ C Grande usada como tendencia
→ nuevo 1 bajista
```

La salida del motor debe nombrar expresamente la conversión y conservar la trazabilidad previa de A Grande, B Grande y C Grande.

### E. Historial y tiempo causal
```text
STRUCTURAL_TIME_NUEVO_1 = extremo/origen desde el que comenzó C Grande
KNOWLEDGE_TIME_NUEVO_1 = primer tick en que C supera la base del módulo
```

C Grande no se borra al convertirse en tendencia. Queda registrada como la función que originó el nuevo 1.

### F. Prohibiciones de regresión
- No llamar C Grande antes de B Grande confirmada.
- No convertir C en nuevo 1 solo por su tamaño absoluto.
- No utilizar únicamente el final de A cuando la regla exige superar la base del módulo.
- No mantener C como simple C Grande después de superar la base del módulo.
- No borrar A, B o C del historial al nacer el nuevo 1.
- No mezclar la base de otra lectura concurrente.

## 0.0.0. PATCH CANONICO ACUMULADO v2.13-v2.16
**Estado:** `CONFIRMADO_JAVIER`

### A. Continuidad intravela de 2 candidata (v2.13)
Después de 1, si la vela siguiente abre en plano (`|Open-Close previo| < 0,25`), no presenta cola inicial prohibitiva y avanza en dirección de 1, abre una única `2_CANDIDATA`.

```text
2 BAJISTA: origen = máximo de salida en plano; extremo = mínimo direccional.
2 ALCISTA: origen = mínimo de salida en plano; extremo = máximo direccional.
```

Las vibraciones internas, incluso de 2 puntos o más, no cancelan ni fragmentan 2, no crean A Grande y no reinician su origen. Si el recorrido alcanza el 100 % de 1, 2 se confirma en ese primer tick. Si termina la vela sin alcanzarlo, 2 queda no confirmada y el recorrido se resuelve como módulo por descarte. El descarte se conoce al cierre, no durante una vibración anterior.

Caso 16:15-16:16: 1 bajista mide 16,2; la vela siguiente abre en plano, recorre 12,6 y contiene vibraciones. Sigue siendo 2 candidata durante la vela. Como termina por debajo del 100 %, no confirma 2 y queda como módulo por descarte.

### B. Concurrencia posterior a 2 confirmado (v2.14)
Después de 2 confirmado y extendido pueden coexistir dos lecturas con referencias independientes:

```text
LECTURA REGULAR:
2 confirmado → retroceso válido → recuperación de la dirección de 2
→ superación estricta del extremo de 2 → 3 confirmado.

LECTURA ALTERNATIVA:
1+2 = módulo → retroceso contrario desde el extremo de 2 = A Grande
→ giro contrario a A = B candidata.
```

Para B:

```text
recorrido_B < 100 % de A → B candidata
100 % de A <= recorrido_B <= 127 % de A + 0,25 → B Grande
recorrido_B > 127 % de A + 0,25 → AUT
```

Tocar exactamente `127 % + 0,25` mantiene B Grande; AUT exige superación estricta. El mismo recorrido puede ser 3 en la lectura regular y B/B Grande/AUT en la alternativa sin mezclar referencias.

Caso 16:20-16:21: extremo de 2 bajista `29832,5`; subida a `29837,0` prepara 3 y simultáneamente es A Grande alternativa de 4,5. La bajada posterior confirma 3 al superar `29832,5`; en la alternativa, B es candidata antes de `29832,5`, B Grande al 100 % y AUT al bajar estrictamente de `29831,035`.

### C. Después de 3 viene A Grande (v2.15)
Cuando 3 queda confirmado, `1-2-3` constituyen el módulo regular completo. La siguiente función regular es A Grande, contraria al módulo, desde el extremo final real de 3.

```text
1 → 2 → 3 CONFIRMADO
→ MODULO REGULAR 1-2-3
→ A GRANDE contraria desde el extremo final real de 3
```

Caso 16:19-16:22: `16:19=1`, `16:20=2`, `16:21=3` con extremo final `29830,3`; la subida de 16:22 es A Grande alcista desde `29830,3`. Un TT alternativo no producido no desplaza esta lectura regular.

### D. Retroceso posterior a AUT/nuevo 1 (v2.16)
Después de AUT y del nacimiento de un nuevo 1, el primer recorrido contrario no se etiqueta automáticamente como A Grande por superar un número fijo de puntos.

```text
AUT → NUEVO 1 ACTIVO → recorrido contrario
→ ¿A Grande autónoma o desarrollo interno del nuevo 1?
```

No existe umbral universal. Un retroceso de 3-4 puntos puede ser A Grande frente a un 1 pequeño y quedar absorbido frente a un movimiento dominante grande. El umbral general de 2 puntos solo distingue ruido físico mínimo de movimiento estructural potencial; no obliga a crear función nueva.

La decisión considera conjuntamente proporción, claridad, autonomía, continuidad posterior, capacidad de originar la secuencia siguiente y contexto de cambio de vela. Una referencia aproximada del 35 % puede orientar en movimientos pequeños, pero no es frontera matemática aprobada.

Mientras falte evidencia, se conserva como recorrido contrario pendiente. Si posteriormente se demuestra A Grande:

```text
STRUCTURAL_TIME_A = extremo del nuevo 1 donde comenzó el retroceso
KNOWLEDGE_TIME_A = primer tick posterior con evidencia funcional suficiente
```

Si el nuevo 1 vuelve a extenderse y absorbe el retroceso, no se abre A.

Caso 16:22: después del AUT alcista directo en `29850,8`, la bajada a `29846,5` (4,3 puntos) queda pendiente; los ticks siguientes decidirán si era A Grande desde `29850,8` o desarrollo interno absorbido.

### E. Prohibiciones acumuladas
- No romper 2 candidata por vibraciones internas.
- No llamar B Grande antes del 100 % de A ni mantenerla tras superar estrictamente AUT.
- No eliminar lecturas concurrentes válidas ni mezclar referencias.
- No preguntar qué viene después de 3: viene A Grande.
- No medir A posterior a 3 desde un punto distinto del extremo final real de 3.
- No convertir automáticamente todo retroceso de 2 puntos o más en A Grande.
- No usar el 35 % orientativo como umbral matemático.
- No usar información futura como conocida antes: separar tiempo estructural y tiempo de conocimiento.

## 0.1. PATCH CANONICO v2.1 - VELAS 5 Y 6 (23:43-23:44)

**Estado:** `CONFIRMADO_JAVIER`

**Finalidad:** corregir y fijar la lectura concurrente entre la culminacion del TT anterior, el FT de la vela 5 y el nuevo ciclo modular que culmina en TT durante la vela 6. Esta seccion prevalece sobre cualquier redaccion anterior incompatible.

### A. Vela 5, 23:43

1. La vela 5 alcanza el objetivo del TT alcista anterior y lo confirma.
2. El TT alcista se extiende hasta su extremo real en `29192,10`.
3. Desde `29192,10` el precio baja hasta `29185,60`.
4. La bajada de `6,50` puntos se clasifica simultaneamente como:
   - `FT` del TT alcista anterior; y
   - `A Grande bajista` de la lectura anterior.
5. Desde `29185,60` comienza una subida que, en la lectura anterior, es `B candidata alcista`.
6. Esa misma subida se abre simultaneamente como `nuevo 1 alcista` de una lectura concurrente.
7. Al producirse posteriormente el retroceso estructural, ese nuevo 1 alcista queda como `modulo por descarte`.
8. El cambio de vela no borra la B candidata heredada ni el modulo concurrente.

```text
VELA 5
TT ALCISTA ANTERIOR CONFIRMADO Y EXTENDIDO HASTA 29192,10
-> FT: 29192,10 -> 29185,60
-> simultaneamente A GRANDE BAJISTA: 6,50 puntos
-> B CANDIDATA ALCISTA desde 29185,60
-> simultaneamente NUEVO 1 ALCISTA
-> MODULO POR DESCARTE de la nueva lectura
```

### B. Cambio de vela 5 a vela 6

```text
Ultimo BID vela 5: 29189,30
Primer BID vela 6: 29189,70
Delta: +0,40 puntos
```

Como `0,40 > 0,25`, existe `gap alcista`. Por tanto, no hay 2. El gap no cancela las lecturas heredadas.

### C. Vela 6, 23:44 - lectura modular principal

La cronologia relevante es:

```text
29185,60 -> 29191,50 -> 29188,80 -> 29200,50
```

1. El modulo alcista nace en `29185,60`, cruza el cambio de vela y termina en `29191,50`.
2. Medida del modulo: `29191,50 - 29185,60 = 5,90` puntos.
3. Desde `29191,50` el precio baja hasta `29188,80`: `A Grande bajista = 2,70` puntos.
4. Desde `29188,80` nace `B candidata alcista`.
5. Al alcanzar `29191,50`, B llega al 100 % de A Grande y se confirma `B Grande`.
6. Frontera AUT: `2,70 x 1,27 + 0,25 = 3,679` puntos.
7. Nivel AUT: `29188,80 + 3,679 = 29192,479`.
8. Al superar `29192,479`, B Grande deja de estar vigente y se confirma `AUT alcista`.
9. Objetivo TT: `29188,80 + 5,90 = 29194,70`.
10. Al alcanzar `29194,70`, se confirma `TT alcista`.
11. El TT continua hasta su extremo real en `29200,50`.

```text
VELA 6 - LECTURA MODULAR PRINCIPAL
MODULO ALCISTA: 29185,60 -> 29191,50 = 5,90
-> A GRANDE BAJISTA: 29191,50 -> 29188,80 = 2,70
-> B CANDIDATA ALCISTA
-> B GRANDE en 29191,50
-> AUT ALCISTA al superar 29192,479
-> TT ALCISTA confirmado en 29194,70
-> TT extendido hasta 29200,50
```

### D. Lectura anterior concurrente

La subida iniciada en la vela 5 permanece simultaneamente como B candidata de la A Grande de `6,50` puntos:

1. B Grande de esta lectura se confirma en `29192,10`.
2. Frontera AUT: `6,50 x 1,27 + 0,25 = 8,505` puntos.
3. Nivel AUT: `29185,60 + 8,505 = 29194,105`.
4. Al superar `29194,105`, se confirma `AUT alcista` en esta lectura concurrente.

### E. Salida obligatoria del motor

```text
LECTURA 1 - HEREDADA
A GRANDE BAJISTA DE 6,50
-> B CANDIDATA ALCISTA
-> B GRANDE EN 29192,10
-> AUT ALCISTA AL SUPERAR 29194,105

LECTURA 2 - MODULAR PRINCIPAL
SUBIDA FINAL DE VELA 5 = NUEVO 1 ALCISTA
-> MODULO POR DESCARTE
-> VELA 6: A GRANDE BAJISTA DE 2,70
-> B CANDIDATA
-> B GRANDE
-> AUT ALCISTA
-> TT ALCISTA CONFIRMADO
-> TT EXTENDIDO HASTA 29200,50

PATRON SUPERIOR
VELA 5: FT DEL TT ALCISTA ANTERIOR
```

### F. Prohibiciones de regresion

- No convertir toda la subida de la vela 6 en mera continuacion del TT anterior.
- No omitir que la subida final de la vela 5 funciona como modulo por descarte de la nueva lectura.
- No borrar la B candidata heredada al cambiar de vela.
- No llamar 2 en la vela 6, porque existe gap de `+0,40`.
- No atribuir A Grande al gap; A Grande nace del retroceso real `29191,50 -> 29188,80`.
- No omitir la secuencia `A -> B -> AUT -> TT` de la vela 6.
- No mantener B Grande vigente despues de superar la frontera AUT.
- No fundir las dos lecturas concurrentes en una sola.

## 0.2. PATCH CANONICO v2.2 - CONTINUIDAD DE B Y MODULO POR DESCARTE

**Estado:** `CONFIRMADO_JAVIER`

**Finalidad:** impedir la fragmentacion de B por oscilaciones internas y fijar el momento exacto en que B candidata pasa a B Grande. Esta seccion prevalece sobre cualquier rama historica incompatible, especialmente sobre `TM-B-005` cuando esa rama interprete un retroceso interno como cancelacion automatica de B.

### A. Inicio de B despues de A Grande

Cuando existe una `A Grande` confirmada, el primer recorrido estructural en direccion contraria a A abre una unica `B candidata`.

```text
A GRANDE CONFIRMADA
-> recorrido contrario a A
-> B CANDIDATA
```

Las referencias quedan congeladas:

```text
ORIGEN_B = extremo/final real de A Grande
REFERENCIA_100_B = extremo opuesto de A Grande
TAMANO_A = distancia entre los dos extremos de A Grande
```

B se mide siempre desde `ORIGEN_B` hasta el extremo mas lejano alcanzado en la direccion propia de B.

### B. Zona de baile interna de B

Mientras el precio permanezca desarrollandose entre las referencias de A Grande y B, todos los avances y retrocesos internos pertenecen a una sola funcion B.

```text
B CANDIDATA
-> avance en direccion de B
-> retroceso interno
-> nuevo avance en direccion de B
-> nuevo retroceso interno
-> TODO SIGUE SIENDO LA MISMA B
```

Reglas obligatorias:

1. Un retroceso interno no cancela B.
2. Un retroceso interno no divide B en varias B.
3. Un retroceso interno no crea automaticamente una nueva A.
4. Un retroceso interno no crea C, porque C exige B Grande previamente confirmada.
5. El filtro estructural de 2 puntos no se utiliza para romper una B candidata activa.
6. Aunque una oscilacion interna supere 2 puntos, queda absorbida dentro de B mientras no exista una regla TM posterior que cierre o reclasifique expresamente la lectura completa.
7. El cambio de vela no reinicia ni cancela B.
8. Para medir B se conserva el extremo direccional mas lejano alcanzado desde el final real de A Grande; los retrocesos intermedios no cambian el origen de B.

### C. Confirmacion de B Grande

B sigue siendo `B candidata` mientras no alcance la referencia completa de A Grande.

```text
SI recorrido_B < TAMANO_A:
    B = CANDIDATA
```

B se convierte en `B Grande` solo cuando el recorrido contrario a A alcanza o supera el 100 % de A Grande y cruza la referencia opuesta/final aplicable de A.

```text
SI recorrido_B >= TAMANO_A:
    B = B GRANDE
```

Equivalencia direccional:

```text
A GRANDE ALCISTA -> B debe desarrollarse BAJISTA
A GRANDE BAJISTA -> B debe desarrollarse ALCISTA
```

No basta con que el precio oscile dentro del rango de A. Debe recorrer A en direccion contraria y alcanzar o superar la referencia del 100 %.

### D. A Grande se convierte en modulo por descarte

Cuando B recorre completamente A Grande y alcanza o supera su referencia del 100 %, A Grande queda simultaneamente disponible como `modulo por descarte` para la lectura concurrente correspondiente.

```text
A GRANDE
-> B CANDIDATA
-> B alcanza/supera el 100 % de A
-> B GRANDE
-> A GRANDE = MODULO POR DESCARTE en la lectura concurrente
```

Esta conversion no borra la trazabilidad historica de A Grande. Deben conservarse ambas funciones por lectura:

```text
LECTURA DE ORIGEN:
A GRANDE -> B GRANDE

LECTURA CONCURRENTE:
A GRANDE ANTERIOR = MODULO POR DESCARTE
-> aplicar A -> B -> AUT -> TT que corresponda
```

### E. Frontera AUT despues de B Grande

Una vez alcanzado el 100 %, B es B Grande mientras no supere la frontera AUT.

```text
LIMITE_AUT = 127 % de A Grande + 0,25 puntos
```

```text
SI 100 % <= recorrido_B <= LIMITE_AUT:
    B = B GRANDE

SI recorrido_B > LIMITE_AUT:
    B deja de ser la clasificacion vigente
    -> AUT confirmado inmediatamente
```

Tocar exactamente `127 % + 0,25` mantiene B Grande. AUT exige superacion estricta.

### F. Ejemplo canonico simplificado

Supuesto:

```text
A Grande = 7 puntos
```

Despues de A, el precio desarrolla B en direccion contraria con oscilaciones internas. Mientras B no alcance los 7 puntos medidos desde el final real de A:

```text
B = CANDIDATA
```

Los retrocesos internos quedan absorbidos:

```text
avance B
-> retroceso interno
-> avance B
-> retroceso interno
-> sigue siendo una unica B
```

Cuando el extremo direccional de B alcanza o supera los 7 puntos:

```text
B CANDIDATA -> B GRANDE
A GRANDE -> MODULO POR DESCARTE en la lectura concurrente
```

Si despues B supera estrictamente `7 x 1,27 + 0,25 = 9,14` puntos:

```text
B GRANDE deja de estar vigente
-> AUT confirmado
```

### G. Ejemplo de recorrido irregular absorbido

```text
Despues de A:
B avanza 7
-> retrocede 4
-> vuelve a avanzar 3
-> retrocede 6
```

La lectura no se fragmenta por cada giro. Todo el desarrollo pertenece a una unica B y se evalua por su extremo direccional acumulado respecto del final real de A.

```text
UNA SOLA B
-> candidata antes del 100 %
-> B Grande al alcanzar/superar el 100 %
-> AUT solo al superar 127 % + 0,25
```

### H. Aplicacion canonica a la vela 14 del registro 23:52

Referencias heredadas:

```text
A Grande: 29177,70 -> 29185,70
TAMANO_A = 8,00 puntos
ORIGEN_B = 29185,70
REFERENCIA_100_B = 29177,70
```

Recorrido observado de B:

```text
29185,70
-> 29179,10
-> retroceso interno hasta 29182,30
-> nuevo avance bajista hasta 29176,70
```

El retroceso `29179,10 -> 29182,30` queda absorbido dentro de la misma B. No cancela ni divide B.

```text
RECORRIDO_B = 29185,70 - 29176,70 = 9,00 puntos
PORCENTAJE_B = 9,00 / 8,00 = 112,50 %
```

Resultado obligatorio:

```text
B CANDIDATA
-> alcanza 100 % en 29177,70
-> B GRANDE confirmada
-> se extiende hasta 29176,70
-> permanece B GRANDE porque no supera AUT
```

Frontera AUT:

```text
8,00 x 1,27 + 0,25 = 10,41 puntos
NIVEL_AUT_BAJISTA = 29185,70 - 10,41 = 29175,29
```

Como `29176,70 > 29175,29`, no hay AUT en ese extremo.

### I. Salida obligatoria del motor

```text
A GRANDE CONFIRMADA
-> B CANDIDATA EN DIRECCION CONTRARIA
-> OSCILACIONES INTERNAS ABSORBIDAS
-> MEDIR B DESDE EL FINAL REAL DE A HASTA SU EXTREMO DIRECCIONAL
-> SI B < 100 %: B CANDIDATA
-> SI B >= 100 %: B GRANDE
-> A GRANDE PASA SIMULTANEAMENTE A MODULO POR DESCARTE EN LA LECTURA CONCURRENTE
-> SI B > 127 % + 0,25: AUT
```

### J. Prohibiciones de regresion

- No cancelar B por un retroceso interno.
- No dividir una B en varias B por oscilaciones intermedias.
- No reiniciar B por cambiar de vela.
- No llamar C antes de confirmar B Grande.
- No usar el filtro de 2 puntos para cortar automaticamente una B candidata activa.
- No confirmar B Grande antes del 100 % de A Grande.
- No omitir la conversion simultanea de A Grande en modulo por descarte cuando B alcanza o supera completamente A.
- No borrar la funcion historica A Grande al abrir la lectura concurrente del modulo por descarte.
- No mantener B Grande despues de superar estrictamente `127 % + 0,25`.
- No confundir una oscilacion interna con el cierre de la funcion B completa.

## 0.3. PATCH CANONICO v2.3 - PRIORIDAD DESPUES DE 1 Y ARBOL COMPLETO DE GAP

**Estado:** `CONFIRMADO_JAVIER`

**Finalidad:** convertir la lectura posterior a un `1` en un procedimiento determinista. Ninguna vela posterior a 1 puede clasificarse como simple continuacion antes de contestar las preguntas de apertura y reconstruir el primer recorrido tick a tick.

### A. Pregunta prioritaria obligatoria despues de 1

Cuando una vela ha quedado definida como `1`, al abrir la vela siguiente se aplica obligatoriamente este orden:

```text
1 CONFIRMADO
-> ¿APERTURA EN PLANO?
-> ¿SIN GAP?
-> ¿COLA INICIAL <= 0,25?
-> ¿RECORRIDO EN DIRECCION DE 1?
-> ¿MIDE IGUAL O MAS QUE 1?
```

Solo si todas las respuestas son afirmativas puede existir `2`.

```text
SI todas = SI:
    2 posible / 2 confirmado segun medida
SINO:
    2 imposible
    1 = MODULO POR DESCARTE
    recorrer A -> B -> B Grande/AUT -> TT
```

**Prohibicion absoluta:** la vela posterior a 1 no puede etiquetarse primero como continuacion de 1. Primero se resuelve `plano/gap`, cola, direccion y medida.

### B. Con gap nunca hay 2

```text
SI |apertura nueva - cierre anterior| > 0,25:
    GAP = SI
    2 = imposible
```

Despues de detectar el gap, el motor debe reconstruir obligatoriamente el orden de los primeros ticks:

```text
GAP
-> ¿EL PRECIO SUBE PRIMERO?
-> ¿EL PRECIO BAJA PRIMERO?
```

No se permite analizar la vela solo por OHLC, color o cierre.

### C. Rama 1 - despues del gap el precio sube primero

Esta rama se aplica cuando el modulo/1 activo es alcista y el gap abre a favor o el primer recorrido efectivo se desarrolla hacia arriba.

```text
GAP
-> SUBE PRIMERO
-> A/B implicitas del gap
-> continuidad alcista
-> evaluar AUT
-> evaluar TT
```

Reglas:

1. El gap no crea 2.
2. El gap y el primer recorrido alcista se leen mediante la secuencia `A -> B -> AUT` propia de la rama de gap.
3. Si alcanza el objetivo completo del modulo desde el final real de A, confirma `TT`.
4. Si no alcanza TT y aparece un descenso estructural, el recorrido alcista inicial queda como `modulo por descarte` de la lectura siguiente.
5. El descenso posterior es `A Grande bajista` de esa nueva lectura.
6. Si esta A Grande supera la base/inicio del modulo alcista y baja por debajo de su minimo/base, confirma `AUT bajista` y el movimiento que lo produce es simultaneamente `nuevo 1 bajista`.
7. Si A no supera la base y el precio vuelve a subir, nace `B candidata alcista`.
8. B candidata se mide desde el final real de A Grande hasta su maximo direccional, absorbiendo oscilaciones internas.
9. Si B alcanza entre `100 %` y `127 % + 0,25`, se confirma `B Grande`.
10. Si B supera estrictamente `127 % + 0,25`, deja de ser B Grande vigente y confirma `AUT alcista`.
11. Tras AUT se evalua TT con el tamaño completo del modulo activo.

### D. Rama 2 - despues del gap el precio baja primero

Esta rama se aplica cuando, despues de abrir con gap, el primer recorrido efectivo va hacia abajo.

```text
VELA 1 ANTERIOR + EXTREMO/MAXIMO DEL GAP
-> MODULO
DESCENSO POSTERIOR
-> A GRANDE BAJISTA
```

Reglas:

1. Con gap, 2 es imposible.
2. El `1` anterior y el extremo maximo alcanzado por el gap forman la referencia completa del modulo alcista.
3. El primer descenso desde ese maximo es `A Grande bajista`.
4. Si despues el precio sube, nace `B candidata alcista`.
5. Si B no alcanza el 100 % de A, sigue candidata.
6. Si B alcanza entre `100 %` y `127 % + 0,25`, confirma `B Grande`.
7. Si B supera estrictamente `127 % + 0,25`, confirma `AUT alcista`.
8. Tras AUT se proyecta TT desde el final real de A usando la medida completa del modulo.
9. Las oscilaciones internas no dividen B.

### E. Esquema direccional simetrico

Las dos ramas se aplican de forma simetrica para modulos bajistas:

```text
MODULO BAJISTA + GAP
-> si baja primero: rama a favor, A/B implicitas, AUT y TT
-> si sube primero: extremo del gap completa modulo; subida = A Grande
-> giro bajista posterior = B candidata
-> 100-127 % + 0,25 = B Grande
-> supera limite = AUT
```

### F. Reinicio por superacion de la base del modulo

Cuando una A Grande posterior a un modulo por descarte atraviesa la base/inicio del modulo y supera su minimo o maximo opuesto:

```text
A GRANDE supera base del MODULO
-> AUT en la nueva direccion
-> NUEVO 1 en el movimiento que produce AUT
-> reset de referencias para el ciclo nuevo
```

No se espera a la vela siguiente para reconocer el nuevo 1.

### G. Caso canonico de regresion - vela 16, 23:54

Referencias de entrada:

```text
VELA 15 = 1 alcista
MINIMO VELA 15 = 29182,00
MAXIMO VELA 15 = 29189,80
X15 = 7,80 puntos
CIERRE VELA 15 = 29189,70
APERTURA VELA 16 = 29190,20
GAP = +0,50
```

Orden real de ticks de la vela 16:

```text
29190,20
-> 29191,20  (sube primero)
-> 29188,50
-> 29193,00
-> 29186,10
-> 29188,70 aproximadamente
```

#### G1. Primera rama del gap

```text
GAP ALCISTA
-> 2 imposible
-> sube primero hasta 29191,20
-> A/B implicitas del gap
-> AUT alcista de la rama de gap
-> no alcanza TT
```

Al aparecer el descenso a `29188,50` antes del TT:

```text
recorrido alcista inicial = MODULO POR DESCARTE
descenso 29191,20 -> 29188,50 = A GRANDE BAJISTA de 2,70
```

El modulo completo de esta lectura se mide desde `29182,00` hasta `29191,20`:

```text
MODULO = 9,20 puntos
```

#### G2. B posterior

Desde `29188,50` el precio sube hasta `29193,00`:

```text
B CANDIDATA ALCISTA = 4,50 puntos
A GRANDE = 2,70 puntos
100 % de A = 29191,20
AUT = 2,70 x 1,27 + 0,25 = 3,679
NIVEL AUT = 29192,179
```

Resultado:

```text
B CANDIDATA
-> B GRANDE en 29191,20
-> supera 29192,179
-> AUT ALCISTA en 29192,179
```

Objetivo TT:

```text
29188,50 + 9,20 = 29197,70
```

Como el maximo es `29193,00`:

```text
TT ALCISTA = no confirmado
```

#### G3. Caida posterior y nueva direccion

Desde `29193,00` el precio baja hasta `29186,10`:

```text
recorrido AUT alcista 29188,50 -> 29193,00
-> MODULO POR DESCARTE
caida 29193,00 -> 29186,10
-> A GRANDE BAJISTA de 6,90 puntos
```

La A Grande bajista atraviesa la base `29188,50` del modulo alcista y baja hasta `29186,10`:

```text
A supera base/minimo del modulo
-> AUT BAJISTA
-> NUEVO 1 BAJISTA
```

La subida final desde `29186,10` hasta aproximadamente `29188,70` es el primer recorrido contrario del ciclo nuevo y debe conservarse para la siguiente decision TM; no puede borrar el nuevo 1 bajista.

### H. Salida compacta obligatoria para vela 16

```text
VELA 16
GAP ALCISTA
-> 2 IMPOSIBLE
-> SUBE PRIMERO
-> A/B IMPLICITAS DEL GAP
-> AUT ALCISTA
-> NO TT
-> MODULO POR DESCARTE
-> A GRANDE BAJISTA
-> B CANDIDATA ALCISTA
-> B GRANDE
-> AUT ALCISTA
-> NO TT
-> MODULO POR DESCARTE
-> A GRANDE BAJISTA SUPERA BASE DEL MODULO
-> AUT BAJISTA
-> NUEVO 1 BAJISTA
```

### I. Prohibiciones de regresion

- No tratar la vela posterior a 1 como simple continuacion antes de evaluar 2.
- No omitir la pregunta `¿sube primero o baja primero despues del gap?`.
- No usar solo OHLC para ordenar A, B, AUT y TT.
- No llamar 2 cuando existe gap.
- No omitir A/B implicitas del gap.
- No confirmar TT si no alcanza el objetivo completo del modulo.
- No omitir el modulo por descarte cuando aparece el movimiento contrario antes del TT.
- No omitir AUT y nuevo 1 cuando A Grande supera la base/minimo del modulo.
- No confundir la rama `sube primero` con la rama `baja primero`.
- No mezclar las referencias matematicas de lecturas concurrentes.

## 0.4. PATCH CANONICO v2.4 - SIMPLIFICACION DE MODULOS Y DEFINICION TOTAL DE MOVIMIENTOS

**Estado:** `CONFIRMADO_JAVIER`

**Finalidad:** evitar cadenas infinitas de mini modulos, impedir la distorsion de la lectura y obligar al motor a definir cada movimiento por su lectura, origen, extremo, direccion, funcion, medida y estado.

### A. Limite operativo de escalas activas

Por defecto se mantienen como maximo dos escalas modulares activas:

```text
LECTURA PRINCIPAL = MODULO PRINCIPAL
LECTURA INTERNA = UNICO MINI MODULO ACTUAL
```

Reglas:

1. No se abre un nuevo mini modulo por cada oscilacion.
2. No se permite una cadena `M1 -> M2 -> M3 -> M4`.
3. Si aparece otra oscilacion, se absorbe dentro de A o B de una de las dos lecturas activas.
4. La tercera lectura solo puede existir excepcionalmente por una regla TM expresa distinta, nunca por encadenamiento automatico de mini modulos.
5. El objetivo es conservar solo las referencias necesarias para comprobar el TT del modulo principal y el TT del mini modulo actual.

### B. Variables obligatorias

```text
M1 = modulo principal
M2 = unico mini modulo actual
A2 = A Grande nacida despues de M2
```

Cada modulo guarda:

```text
ID_LECTURA
ORIGEN
EXTREMO
DIRECCION
BASE
MEDIDA_X
OBJETIVO_TT
ESTADO
```

Cada movimiento guarda:

```text
FUNCION
LECTURA
ORIGEN_PRECIO
EXTREMO_PRECIO
DIRECCION
MEDIDA
ESTADO
TIMESTAMP_ORIGEN
TIMESTAMP_EXTREMO
```

Si falta cualquiera de esos campos, no se emite una clasificacion definitiva.

### C. Integracion condicional de M1 y M2

Despues de M2 nace A2 contraria al mini modulo.

```text
¿A2 SUPERA LA BASE DE M2?
```

#### C1. A2 no supera la base de M2

```text
M1 permanece como modulo principal
M2 permanece como unico mini modulo
A2 sigue perteneciendo a M2
```

Si el precio gira de nuevo en direccion de M2:

```text
nace/continua B de M2
```

No se crea M3. Se mantienen solamente:

```text
LECTURA 1: TT posible/pendiente de M1
LECTURA 2: A -> B -> AUT -> TT posible de M2
```

#### C2. A2 supera la base de M2

```text
M1 + M2 = MODULO CONJUNTO M12
```

La misma A2 no termina ni se reinicia:

```text
A2 de M2
-> supera base de M2
-> A2 pasa a ser A Grande de M12
```

Se conserva la trazabilidad histórica de M1 y M2, pero operativamente queda una sola referencia conjunta:

```text
MODULO ACTIVO = M12
A GRANDE ACTIVA = A2
```

#### C3. A2 supera tambien la base de M12

```text
A2 supera base/opuesto de M12
-> AUT en la direccion de A2
-> movimiento que produce AUT = nuevo 1
-> reset de referencias
```

### D. Regla de no proliferacion

Si A2 no supera M2 y el precio vuelve a subir o bajar en direccion del mini modulo:

```text
NO crear otro mini modulo
NO recalcular una tercera escala
NO encadenar modulos
```

La oscilacion se asigna a B de M2 y, simultaneamente, se sigue comprobando la expansion TT de M1 si ambas lecturas siguen matematicamente activas.

### E. Orden obligatorio para definir cualquier movimiento

Antes de nombrar un movimiento, el motor debe responder:

```text
1. ¿En que lectura ocurre?
2. ¿Cual es el modulo activo de esa lectura?
3. ¿Cual es el origen exacto del movimiento?
4. ¿Cual es su extremo real actual?
5. ¿Cual es su direccion?
6. ¿Que funcion puede nacer desde el estado anterior?
7. ¿Que frontera matematica ha alcanzado?
8. ¿Cual es su estado: candidato, confirmado, integrado, reclasificado o pendiente?
```

Salida mínima:

```text
MOVIMIENTO:
  lectura: L1/L2
  funcion: 1/2/3/A/B/AUT/C/CUT
  origen: precio + timestamp
  extremo: precio + timestamp
  direccion: alcista/bajista
  medida: puntos
  referencia: modulo/A/B/base/TT aplicable
  estado: candidato/confirmado/integrado/reclasificado/pendiente
```

### F. Prioridad de absorcion

Para evitar distorsion, todo movimiento nuevo se intenta asignar en este orden:

```text
1. Continuacion de A activa
2. Continuacion de B activa, con oscilaciones internas absorbidas
3. Resolucion AUT/TT/C/CUT de una lectura activa
4. Integracion M1 + M2 si A2 supera la base de M2
5. Apertura excepcional de lectura solo con regla expresa
```

Nunca se abre un mini modulo nuevo si el recorrido puede explicarse correctamente como A o B de M1 o M2.

### G. Caso conceptual canonico

```text
M1 = modulo principal de vela 14
M2 = mini modulo posterior
A2 = descenso posterior a M2
```

#### Si A2 no supera la base de M2 y el precio vuelve a subir

```text
LECTURA PRINCIPAL:
M1 -> comprobar TT principal

LECTURA INTERNA:
M2 -> A2 -> B2 -> comprobar B Grande/AUT/TT interno

MODULOS ACTIVOS = 2
NO M3
```

#### Si A2 supera la base de M2

```text
M1 + M2 = M12
A2 continua como A Grande de M12
```

Después:

```text
si A2 no supera base de M12 y gira:
    B candidata de M12

si A2 supera base de M12:
    AUT
    nuevo 1
    reset
```

### H. Correccion de la rama de vela 16

La lectura de vela 16 debe conservar simultaneamente, como maximo:

```text
L1: modulo principal procedente del 1 de vela 14/TT principal aplicable
L2: unico mini modulo actual producido dentro de vela 16
```

Cuando la A Grande bajista posterior al mini modulo cae:

```text
SI no supera base de M2:
    mantener M1 y M2
    giro alcista = B de M2

SI supera base de M2:
    integrar M1 + M2 = M12
    la misma bajada = A Grande de M12
```

No se permite crear un tercer mini modulo por el rebote siguiente.

### I. Prohibiciones absolutas v2.4

- No encadenar indefinidamente mini modulos.
- No mantener mas de un mini modulo actual junto al modulo principal.
- No crear M3 por una oscilacion que cabe dentro de A o B.
- No integrar M1 y M2 antes de que A2 supere la base de M2.
- No reiniciar A2 al integrar M1 y M2.
- No borrar la trazabilidad de M1 o M2 después de la integración.
- No seguir usando las referencias separadas de M1 y M2 como activas después de formar M12, salvo trazabilidad.
- No declarar AUT del modulo conjunto por superar solamente la base de M2.
- No perder la lectura TT principal mientras M1 siga válida.
- No perder la lectura TT interna mientras M2 siga válida.
- No emitir una función sin lectura, origen, extremo, dirección, medida, referencia y estado.
- No usar una etiqueta genérica como `movimiento contrario` cuando la función puede determinarse matemáticamente.
- Si la función no puede determinarse, escribir `PENDIENTE_POR_REGLA` y no inventar.

### J. Salida obligatoria simplificada

```text
LECTURA 1 - PRINCIPAL
MODULO: M1 o M12
A/B/AUT: estado actual
TT: objetivo y estado

LECTURA 2 - MINI MODULO ACTUAL, solo si existe
MODULO: M2
A/B/AUT: estado actual
TT: objetivo y estado

INTEGRACION:
NO, si A2 no supera base de M2
SI, si A2 supera base de M2; entonces M1 + M2 = M12

PROHIBIDO:
abrir otro mini modulo por cada oscilacion
```

## 0.5. PATCH CANONICO v2.5 - PRIORIDAD DE MODULOS GRANDES Y SEPARACION LECTURA/OPERABILIDAD

**Estado:** `CONFIRMADO_JAVIER`

**Finalidad:** conservar la lectura TM completa de todas las escalas, pero dar prioridad explicativa y de seguimiento a los modulos grandes. Los patrones menores siguen detectandose y registrandose, aunque una capa operativa futura pueda excluirlos por tamaño.

### A. Dos planos obligatoriamente separados

```text
PLANO 1 = LECTURA TM ESTRUCTURAL
PLANO 2 = ELEGIBILIDAD OPERATIVA FUTURA
```

El plano de lectura nunca se apaga:

1. Se detectan continuamente 1, 2, 3, modulo, A, B, AUT, C, CUT, TT y FT.
2. Se conservan lecturas principales e internas conforme al limite de escalas de v2.4.
3. Un patron pequeño sigue siendo una estructura TM valida aunque no sea elegible para una posicion.
4. La falta de elegibilidad operativa no cancela, borra ni reclasifica el patron.

### B. Prioridad de los modulos grandes

Los modulos grandes tienen prioridad porque producen objetivos TT mayores y constituyen la lectura economica principal.

Orden obligatorio de salida:

```text
1. MODULO PRINCIPAL O MODULO CONJUNTO GRANDE
2. A GRANDE, B GRANDE, AUT Y TT DE ESE MODULO
3. UNICO MINI MODULO ACTUAL, SI EXISTE
4. PATRONES PEQUEÑOS INTERNOS
```

Reglas:

- Nunca ocultar el TT del modulo grande por atender un mini modulo.
- Nunca sustituir la lectura principal por una estructura interna menor.
- Si existe modulo conjunto integrado, la referencia principal es el conjunto.
- Mostrar siempre medida del modulo grande, final real de A Grande, nivel de B Grande, nivel AUT y objetivo TT.
- Las estructuras pequeñas se muestran después y separadas.

### C. Clasificacion por tamaño

Para cada modulo y su TT asociado se calcula:

```text
TAMANO_MODULO = |extremo - base|
OBJETIVO_TT = final_A +/- TAMANO_MODULO
```

Clasificacion de seguimiento:

```text
SI TAMANO_MODULO >= 6,00 puntos:
    CLASE = PRINCIPAL_ELEGIBLE_PARA_ESTUDIO_OPERATIVO

SI TAMANO_MODULO < 6,00 puntos:
    CLASE = LECTURA_ESTRUCTURAL_NO_ELEGIBLE
```

La frontera es exacta:

```text
6,00 puntos = cumple el filtro
menos de 6,00 puntos = no cumple el filtro
```

### D. Filtro mínimo teórico de 6 puntos

La lectura TM se realiza siempre, sin importar el tamaño. Sin embargo, para la futura capa de posiciones:

```text
MODULO/TT < 6,00 puntos
-> leer y registrar
-> no elegir para entrada

MODULO/TT >= 6,00 puntos
-> leer y registrar
-> candidato para evaluación operativa futura
```

Este filtro no autoriza por sí solo ninguna posición. Solo clasifica la escala por tamaño. La decisión operativa requerirá reglas separadas y completas de riesgo, objetivo, sesión, velocidad, invalidación y ejecución.

### E. Zona conceptual futura de activación

Se registra, sin activarla todavía como orden ejecutable, la hipótesis de trabajo siguiente:

```text
ZONA CONCEPTUAL DE ACTIVACION
= autocorte / superacion estricta de la frontera de B Grande
= confirmacion AUT
```

Interpretación estructural:

1. B alcanza el 100 % de A: `B Grande`.
2. B permanece B Grande hasta `127 % + 0,25` inclusive.
3. La superación estricta de `127 % + 0,25` confirma `AUT`.
4. AUT abre el seguimiento del posible TT.
5. En una fase futura, la entrada podrá estudiarse exactamente en AUT, pero esta versión del árbol sigue siendo de lectura y no contiene todavía una regla operativa completa.

### F. Etiquetas obligatorias en cada lectura

Toda salida debe incluir:

```text
ESCALA:
  PRINCIPAL / MINI

TAMANO_MODULO:
  puntos

CLASE_TAMANO:
  >=6 PRINCIPAL_ELEGIBLE_PARA_ESTUDIO_OPERATIVO
  <6 LECTURA_ESTRUCTURAL_NO_ELEGIBLE

NIVEL_B_GRANDE:
  precio

NIVEL_AUT:
  precio

OBJETIVO_TT:
  precio

ESTADO_TT:
  pendiente / confirmado / fallido / extendido
```

### G. Concurrencia simplificada y prioridad económica

Con máximo dos escalas activas:

```text
L1 = modulo principal/grande
L2 = unico mini modulo actual
```

Salida obligatoria:

```text
PRIMERO L1:
medida -> A Grande -> B Grande -> AUT -> TT

DESPUES L2:
medida -> A -> B -> AUT -> TT
```

Si L2 se integra con L1:

```text
L1 + L2 = modulo conjunto
-> el modulo conjunto pasa a ser la unica referencia principal
-> recalcular clase de tamaño y objetivo TT conjunto
```

### H. Prohibiciones v2.5

- No omitir un modulo grande por describir primero uno pequeño.
- No presentar un mini TT como lectura principal si existe un TT de módulo grande activo.
- No dejar de leer patrones inferiores a 6 puntos.
- No marcar como elegible una estructura inferior a 6 puntos.
- No confundir `lectura válida` con `entrada elegible`.
- No convertir AUT en una orden ejecutable sin la futura capa operativa completa.
- No afirmar que tamaño mayor implica resultado garantizado.
- No usar el filtro de 6 puntos para alterar A, B, AUT, TT, C, CUT o FT.
- No mezclar niveles AUT de distintas escalas.
- No calcular TT pequeño con la medida del módulo grande ni TT grande con la medida del mini módulo.

### I. Plantilla compacta obligatoria

```text
LECTURA PRINCIPAL - MODULO GRANDE
Origen/extremo:
Tamaño:
Clase >=6 o <6:
A Grande:
B Grande:
AUT:
TT objetivo:
TT estado:

LECTURA INTERNA - MINI MODULO, SI EXISTE
Origen/extremo:
Tamaño:
Clase >=6 o <6:
A:
B:
AUT:
TT objetivo:
TT estado:

PRIORIDAD:
El modulo grande se explica y sigue primero.
El mini modulo se conserva sin desplazar la lectura principal.
```

### 0.6. PATCH CANONICO v2.6 - PUNTOS DECISIVOS AUT, TT 100 % Y FT

**Estado:** `CONFIRMADO_JAVIER`

**Alcance:** esta sección fija la arquitectura conceptual de activación y gestión. No constituye todavía una orden automática ni una regla operativa completa, porque las variables de decisión se incorporarán posteriormente.

#### A. Dos puntos decisivos de posible incorporación

La TM reconoce dos zonas estructurales distintas en las que, en una fase operativa posterior, podrá evaluarse la incorporación de una posición:

```text
PUNTO DECISIVO 1 = AUTOCORTE / AUT
PUNTO DECISIVO 2 = FT POSTERIOR A TT CONFIRMADO
```

Ambos puntos requieren una lectura TM válida y referencias matemáticas cerradas. Ninguno debe activarse si faltan las precondiciones de su patrón.

#### B. Punto decisivo 1: AUT como inicio del patrón TT

Secuencia causal obligatoria:

```text
A GRANDE
-> B CANDIDATA
-> B GRANDE al alcanzar 100 % de A
-> B permanece B GRANDE hasta 127 % + 0,25 inclusive
-> superación estricta de 127 % + 0,25
-> AUT / AUTOCORTE
-> comienza TT POSIBLE
```

Reglas:

1. El 100 % de A confirma `B Grande`, pero todavía no confirma AUT.
2. Tocar exactamente `127 % + 0,25` mantiene B Grande.
3. AUT exige superar estrictamente `127 % + 0,25`.
4. En el tick de superación se registra el `AUTOCORTE`.
5. AUT es el punto estructural exacto desde el que comienza el seguimiento del patrón TT posible.
6. AUT es el primer punto decisivo en el que podrá evaluarse una incorporación de posición cuando exista la futura capa operativa.
7. AUT no garantiza que TT llegue al 100 %.
8. Tras AUT debe conservarse el precio exacto de activación, dirección, lectura, módulo, final de A y objetivo TT.

#### C. Nivel del 100 % de TT: primera opción de gestión o SL

```text
OBJETIVO_TT_100 = final_A +/- tamaño_modulo
```

Cuando el precio alcanza el 100 %:

```text
TT POSIBLE -> TT CONFIRMADO
```

El nivel del 100 % cumple simultáneamente estas funciones:

1. Es el mínimo matemático que confirma TT.
2. Es la primera zona en la que podrá evaluarse proteger o cortar la posición iniciada en AUT.
3. Es la primera opción conceptual de `SL de protección/gestión` para la posición, no una salida automática.
4. Alcanzar el 100 % no obliga a cerrar la posición.
5. Alcanzar el 100 % no termina necesariamente el TT.
6. El TT puede extenderse más allá del 100 % hasta su extremo real.
7. Las variables futuras decidirán entre:
   - cerrar;
   - proteger;
   - mover SL;
   - realizar salida parcial;
   - continuar con la posición.

**Prohibición:** no convertir el 100 % del TT en cierre obligatorio ni en SL automático fijo antes de incorporar y validar las variables de gestión.

#### D. Extremo real del TT

Una vez confirmado el TT al 100 %:

```text
TT = confirmado
EXTREMO_TT = máximo real si TT alcista
EXTREMO_TT = mínimo real si TT bajista
```

El TT continúa mientras siga ampliando su extremo y no aparezca el retroceso estructural que marque FT. Por tanto:

```text
100 % TT = confirmación mínima y primera zona de gestión
EXTREMO REAL TT = punto desde el que nace FT
```

Nunca debe medirse FT desde el nivel exacto del 100 % si el TT continuó extendiéndose.

#### E. Punto decisivo 2: incorporación en FT

FT solo puede evaluarse después de un TT confirmado.

Secuencia obligatoria:

```text
TT alcanza como mínimo el 100 %
-> TT confirmado
-> TT puede continuar y extenderse
-> se fija el extremo real del TT
-> aparece retroceso contrario desde ese extremo
-> evaluar variables
-> FT
```

Reglas:

1. Antes del 100 % no existe FT.
2. FT no empieza automáticamente en el nivel del 100 %.
3. FT comienza cuando aparece un movimiento contrario desde el extremo real del TT.
4. El extremo real puede coincidir con el 100 % o quedar más allá.
5. El retroceso posterior al extremo real abre la zona FT.
6. Las variables futuras aportarán la información necesaria para decidir si el FT es guardable/operable y el tick exacto de incorporación.
7. El punto decisivo FT debe conservar:
   - TT de origen;
   - nivel 100 %;
   - extremo real del TT;
   - primer tick contrario;
   - dirección geométrica del FT;
   - variables de confirmación;
   - estado candidato/confirmado/descartado.
8. FT puede coexistir con A Grande, módulo por descarte o nuevo ciclo modular, sin que una lectura borre la otra.

#### F. Variables pendientes

Las variables serán definidas en profundidad en una fase posterior. Hasta entonces el motor debe:

```text
CALCULAR Y GUARDAR DATOS DISPONIBLES
NO INVENTAR UMBRALES
NO CERRAR AUTOMATICAMENTE EN 100 %
NO CONFIRMAR ENTRADA FT SIN VARIABLES SUFICIENTES
```

Campos mínimos reservados:

```text
VARIABLES_TT_GESTION:
  velocidad
  aceleracion/desaceleracion
  sentimiento
  continuidad
  retroceso
  extension
  riesgo
  contexto

VARIABLES_FT_CONFIRMACION:
  perdida_de_velocidad
  giro_contrario
  recorrido_contrario
  persistencia
  estructura
  sentimiento
  riesgo
```

El nombre, fórmula, ventana y umbral exactos de cada variable quedan pendientes de la futura definición experta.

#### G. Separación lectura, señal y gestión

```text
CAPA 1 - LECTURA:
A -> B Grande -> AUT -> TT -> FT

CAPA 2 - POSIBLE ACTIVACION:
AUT o FT

CAPA 3 - GESTION:
TT 100 %, extremo real, variables y continuidad
```

Reglas:

- La lectura se realiza siempre.
- AUT y FT son puntos decisivos diferentes.
- El 100 % de TT es una primera zona de gestión, no una nueva entrada TT por sí misma.
- Una posición nacida en AUT puede continuar más allá del 100 %.
- Una posible posición FT pertenece al movimiento contrario posterior al TT.
- No se mezclan posiciones, SL ni gestión entre lecturas concurrentes.

#### H. Filtro de tamaño y prioridad

La prioridad de v2.5 se mantiene:

```text
MODULO >= 6 puntos:
  lectura prioritaria para estudio operativo

MODULO < 6 puntos:
  lectura estructural continua
  no elegible por tamaño para incorporación AUT en la regla actual
```

La elegibilidad del FT se evaluará posteriormente con sus propias variables y reglas; no debe inferirse automáticamente solo por el tamaño del recorrido FT ni por el tamaño del módulo de origen.

#### I. Máquina de estados conceptual

```text
SIN_POSICION
-> AUT_CONFIRMADO
-> CANDIDATO_ENTRADA_AUT
-> POSICION_AUT_PENDIENTE_DE_REGLAS
-> TT_100_ALCANZADO
-> PRIMERA_OPCION_GESTION_SL
-> DECISION_VARIABLES: CERRAR / PROTEGER / PARCIAL / CONTINUAR
-> TT_EXTENDIDO
-> EXTREMO_REAL_TT
-> RETROCESO_CONTRARIO
-> CANDIDATO_FT
-> DECISION_VARIABLES_FT
-> FT_GUARDABLE / FT_NO_GUARDABLE
```

Esta máquina es conceptual. Los estados de ejecución permanecen pendientes hasta definir variables, riesgo y reglas de orden.

#### J. Datos obligatorios por evento

```text
EVENTO AUT:
  lectura
  dirección
  precio_AUT
  timestamp_AUT
  nivel_B_100
  nivel_127_mas_025
  módulo
  final_A
  objetivo_TT_100
  tamaño_módulo
  clase_tamaño

EVENTO TT_100:
  precio_objetivo
  timestamp_confirmación
  overshoot
  posición_asociada
  primera_opción_SL = sí
  cierre_obligatorio = no
  decisión_variables = pendiente

EVENTO EXTREMO_TT:
  precio_extremo_real
  timestamp_extremo
  extensión_sobre_100

EVENTO FT:
  TT_origen
  extremo_real_TT
  primer_tick_contrario
  dirección_FT
  variables
  estado_operable
  timestamp
```

#### K. Prohibiciones v2.6

- No anticipar entrada antes de AUT en la rama TT.
- No llamar AUT al 100 % de B.
- No llamar AUT por tocar exactamente `127 % + 0,25`.
- No omitir el autocorte en el tick que supera estrictamente esa frontera.
- No confundir AUT con TT confirmado.
- No cerrar obligatoriamente la posición al 100 % de TT.
- No afirmar que el TT termina en el 100 %.
- No medir FT desde el 100 % si TT se extendió.
- No llamar FT antes de TT confirmado.
- No confirmar incorporación FT sin las futuras variables suficientes.
- No inventar thresholds de velocidad, sentimiento o riesgo.
- No mezclar el SL conceptual de una lectura con otra lectura concurrente.
- No convertir esta arquitectura conceptual en orden automática antes de completar la capa operativa.

#### L. Salida obligatoria futura

```text
LECTURA:
Modulo -> A -> B Grande -> AUT -> TT -> FT

PUNTO DECISIVO AUT:
precio / timestamp / dirección / tamaño / elegibilidad

TT 100 %:
objetivo / alcanzado / primera opción de gestión-SL / no cierre automático

TT EXTENDIDO:
extremo real / extensión

PUNTO DECISIVO FT:
TT origen / extremo real / primer retroceso / variables / estado guardable
```

## 0.7. PATCH CANONICO v2.7 - ARBITRO CRONOLOGICO DE TT PENDIENTE

**Estado:** `CONFIRMADO_JAVIER`

**Finalidad:** resolver sin ambigüedad una vela que comienza con un TT pendiente y puede alcanzar tanto el objetivo TT como el final de A. El motor debe decidir exclusivamente por el primer tick cronológico que toca una de las dos fronteras.

### A. Referencias congeladas de entrada

Cuando una lectura entra en una vela con `TT pendiente`, se congelan antes de leer el primer tick:

```text
LECTURA_TT
MODULO_ACTIVO
TAMANO_MODULO
FINAL_REAL_A
OBJETIVO_TT_100
DIRECCION_TT
NIVEL_AUT
EXTREMO_TT_ACTUAL
```

La apertura, el gap y las oscilaciones de la vela nueva no recalculan estas referencias antes de resolver el TT pendiente.

### B. Pregunta prioritaria absoluta

Antes de abrir una nueva A, B, módulo conjunto o lectura concurrente, el motor debe preguntar:

```text
¿QUE FRONTERA SE ALCANZA PRIMERO TICK A TICK?

1. OBJETIVO_TT_100
2. FINAL_REAL_A
```

No se permite decidir por OHLC, color, cierre, forma visual de la vela ni proximidad aparente.

### C. Rama TT primero

```text
SI el precio alcanza primero OBJETIVO_TT_100:
    TT = CONFIRMADO
    CICLO_ANTERIOR = CERRADO
    RESET = INMEDIATO
    MOVIMIENTO QUE CONFIRMA TT = NUEVO 1
```

Consecuencias obligatorias:

1. El módulo anterior deja de ser referencia activa.
2. La A Grande anterior deja de ser referencia activa para nuevas mediciones.
3. La misma vela tiene doble pertenencia: TT del ciclo cerrado y nuevo 1 del ciclo nuevo.
4. Toda evolución posterior de esa vela se analiza solo con referencias recalculadas desde el nuevo 1.
5. Queda prohibido reutilizar el módulo anterior para crear una nueva A Grande después del reset.
6. Si TT continúa más allá del 100 %, se conserva su extremo real para el futuro FT.

### D. Rama final de A primero

```text
SI el precio toca o supera primero FINAL_REAL_A
Y TT aun no alcanzo el 100 %:
    TT = FALLIDO
    AUT anterior = conservado en trazabilidad
    RECORRIDO ANTERIOR = MODULO POR DESCARTE
    RETORNO = A GRANDE NUEVA
```

Consecuencias obligatorias:

1. No hay FT porque TT no fue confirmado.
2. No hay reset por TT.
3. Se aplica reclasificación o integración según el árbol vigente.
4. La nueva A Grande se mide desde la referencia correcta de la rama cronológica, incluido el tratamiento del gap.
5. Si la vela abrió con gap, después de declarar TT fallido se recorre la rama `sube primero / baja primero` sin mezclar el mínimo previo del módulo con el origen nuevo creado por el gap.

### E. Empate en el mismo tick

Si un único salto de precio cruza ambas fronteras en el mismo tick:

```text
RECONSTRUIR DIRECCION DEL SALTO
APLICAR LA PRIMERA FRONTERA GEOMETRICA CRUZADA DESDE EL PRECIO PREVIO
```

Si la fuente de ticks no permite determinar el orden:

```text
ESTADO = PENDIENTE_POR_ORDEN_INTRATICK
NO INVENTAR RESET
NO INVENTAR RECLASIFICACION
```

### F. Caso de regresión 16:30-16:32

Referencias heredadas al terminar 16:31:

```text
MODULO VELA 1:
29838,20 -> 29784,60
X = 53,60 puntos

FINAL_A:
29810,80

OBJETIVO_TT_BAJISTA:
29810,80 - 53,60 = 29757,20

MINIMO VELA 2:
29760,30

TT:
pendiente; faltan 3,10 puntos
```

Vela 3, 16:32:

```text
APERTURA = 29796,70
MINIMO = 29794,10
MAXIMO = 29820,80
```

Comprobación cronológica:

```text
¿Alcanza 29757,20?
NO

¿Alcanza/supera 29810,80?
SI, a las 16:32:23; tick 29811,80
```

Resultado obligatorio:

```text
TT BAJISTA = FALLIDO
NO RESET POR TT
VELAS 1 Y 2 = MODULO CONJUNTO APLICABLE
VELA 3 = NUEVA A GRANDE SEGUN RAMA DE GAP
```

Si la vela 3 hubiera alcanzado primero `29757,20`:

```text
TT BAJISTA = CONFIRMADO
RESET INMEDIATO
VELA 3 = NUEVO 1
PROHIBIDO reutilizar velas 1 y 2 como modulo activo para una A posterior
```

### G. Plantilla obligatoria de salida

```text
TT PENDIENTE DE ENTRADA:
  lectura:
  objetivo_TT_100:
  final_A:

ORDEN CRONOLOGICO:
  primer_tick_objetivo_TT:
  primer_tick_final_A:
  frontera_primera:

RESOLUCION:
  TT_confirmado / TT_fallido / pendiente_intratik
  reset:
  modulo_activo_posterior:
  nueva_funcion:
```

### H. Prohibiciones v2.7

- No calcular una nueva A Grande antes de resolver el TT pendiente heredado.
- No confirmar TT porque la vela quedó cerca del objetivo.
- No declarar TT fallido por el cierre si antes alcanzó el objetivo.
- No mantener activo el módulo anterior después de TT confirmado y reset.
- No reutilizar el módulo anterior para una A nueva después del reset.
- No declarar FT si TT no alcanzó el 100 %.
- No mezclar el mínimo anterior del módulo con el origen de A creado por una rama nueva de gap.
- No decidir con OHLC si los ticks permiten conocer el orden.
- No omitir timestamps de las fronteras decisivas.

## 0.8. ONTOLOGIA FORMAL CERRADA

```text
FUNCIONES TM: 1, 2, 3, A, B, C, AUT, CUT
PATRONES TM: TT, FT
VARIABLES TM:
1. Patron
2. Velocidad
3. Solapamiento frente a verticalidad
4. Tiempo de vela de 3 y de 1
5. Estructura
```

La TM es un lenguaje cerrado. Quedan prohibidos conceptos e indicadores externos. Los terminos direccionales, de tiempo, precio y medida solo aclaran la conversacion; no crean entidades TM.

---

## 0.9. PRINCIPIO DE SEPARACION ENTRE LECTURA Y VARIABLES

**Estado:** `CONFIRMADO_JAVIER`

```text
CAPA 1: LECTURA TM
CAPA 2: CONSULTA DE VARIABLES
CAPA 3: DECISION
```

### A. Lectura TM inalterable

La lectura se construye exclusivamente con funciones y patrones TM, siguiendo ticks, referencias y orden cronologico.

```text
LAS VARIABLES NO MODIFICAN LA LECTURA.
LAS VARIABLES NO RECLASIFICAN FUNCIONES.
LAS VARIABLES NO CREAN NI CANCELAN TT O FT.
```

Si la lectura confirma `1`, `A`, `B`, `AUT`, `TT` o cualquier otra entidad TM, esa lectura no cambia porque una variable resulte favorable o desfavorable.

### B. Consulta de variables

Las variables se observan continuamente cuando corresponda, pero se consultan especialmente en los momentos de decision:

```text
AUT -> decision asociada a TT
EXTREMO REAL DE TT Y MOVIMIENTO CONTRARIO -> decision asociada a FT
```

Las variables solo modifican la probabilidad condicionada y la decision de incorporacion, continuidad o gestion. Nunca modifican la lectura.

---

## 0.10. VARIABLE 1 - PATRON

**Estado:** `DEFINICION_TEORICA_CERRADA`

### A. Patrones formales

```text
TT = Tendencia a Tendencia
FT = Fin de Tendencia
```

Sin TT ni FT no existe decision de incorporacion.

### B. TT

```text
AUT -> TT posible
TT alcanza 100 % desde final de A usando medida del modulo -> TT confirmado
```

El 100 % es:

```text
- confirmacion minima de TT;
- primera referencia posible de salida o gestion;
- no final obligatorio del patron.
```

TT puede extenderse por encima del 100 % hasta su extremo real. La gestion posterior depende de las variables.

### C. FT

```text
TT confirmado al menos al 100 %
-> TT alcanza extremo real
-> aparece movimiento contrario
-> FT posible
```

FT siempre ocurre despues de TT. FT expresa una probabilidad elevada de desplazamiento contrario a TT, condicionada por las demás variables.

FT no dispone de una salida minima fija equivalente al 100 % de TT. La salida y gestion de FT dependen de la lectura de variables.

---

## 0.11. VARIABLE 2 - VELOCIDAD

**Estado:** `DEFINICION_TEORICA_CERRADA_PENDIENTE_DE_FORMULA`

### A. Definicion

```text
VELOCIDAD = percepcion temporal observable del ritmo
con el que se desplaza el punto precio.
```

La velocidad traduce a movimiento observable la impresion profesional de que una decision institucional esta siendo ejecutada. Esta formulacion es una hipotesis teorica; no identifica a un operador concreto ni garantiza el resultado.

La velocidad es una observacion visual y temporal que debera convertirse progresivamente en mediciones para el futuro EA. Todavia no existe una formula definitiva.

### B. Importancia

Velocidad es, despues de Patron, la variable mas importante para la decision. Se consulta durante toda la sesión y especialmente:

```text
- en el proceso que conduce a AUT para TT;
- cerca del extremo real de TT y en el movimiento contrario para FT.
```

Velocidad no confirma ni cancela funciones o patrones. Solo condiciona la decision.

### C. Horario de observacion

```text
OBSERVACION PREVIA: 9:15-9:30, hora de Nueva York
SESION: 9:30-12:30, hora de Nueva York
```

La conversion al servidor de IC Markets debe ser dinamica por cambios horarios; no debe codificarse una diferencia fija permanente.

### D. Brokeraje

```text
BROKERAJE = fase inicial posterior a 9:30
con velocidad excepcional que despues se estabiliza.
```

No tiene duracion fija. Puede durar aproximadamente 2, 3, 4, 5 minutos o lo que determine el desplazamiento real.

El brokeraje:

```text
- puede ser operable;
- puede contener patrones validos;
- debe identificarse separadamente;
- no debe definir por si solo la velocidad normal del resto de la sesion.
```

### E. Regimen de sesion

Clasificacion conceptual inicial:

```text
LENTA
MEDIA
RAPIDA
MUY RAPIDA
TSUNAMI
```

Estas categorias no tienen aun umbrales matematicos. `Tsunami` describe una velocidad extrema que puede justificar no operar, pero la regla definitiva queda pendiente de validacion.

### F. Dos formas favorables

```text
1. VELOCIDAD SOSTENIDA:
la sesion ya mantiene un ritmo adecuado y el proceso hacia AUT
continua dentro del mismo regimen.

2. CAMBIO DE VELOCIDAD:
la sesion venia con menor ritmo y aparece un aumento relevante
durante el proceso hacia AUT.
```

No es obligatorio que exista un cambio de velocidad justo antes de AUT. Una sesion limpia y sostenidamente rapida puede desarrollar patrones de forma continua sin aceleracion adicional en cada AUT.

Tampoco es valida la regla `cuanta mas velocidad, mejor`. Una velocidad extrema puede ser inadecuada.

### G. Ventana adaptativa

Velocidad no se mide siempre desde un punto fijo ni exclusivamente desde B.

```text
Primera referencia: B.
Si B no contiene informacion suficiente: A + B.
Si A + B no contienen informacion suficiente: parte final de 1 + A + B.
```

Ejemplo experto:

```text
Una B cercana a 6 puntos normalmente puede aportar espacio y tiempo
suficientes para observar velocidad.
```

Los 6 puntos son referencia conceptual, no umbral universal aprobado.

Si `1` se desarrolla con velocidad, `A` es breve y `B` tambien es breve, la lectura de velocidad debe conservar el tramo final de `1`; no debe limitarse a los milisegundos de B.

La ventana sigue funciones, no cambios de vela.

### H. Principio de informacion suficiente

La seleccion futura de ventana dependera probablemente de:

```text
- medida;
- duracion;
- cantidad de ticks;
- estabilidad de la estimacion.
```

Todavia no se define una condicion fija. El objetivo es seleccionar el tramo minimo que represente adecuadamente el ritmo de llegada a AUT.

### I. Arquitectura futura para MQL5

La primera implementacion debe ser un registrador, no un filtro automatico.

En cada AUT debe guardar, como minimo:

```text
- hora Nueva York y hora servidor;
- fase previa, brokeraje o sesion estabilizada;
- inicio/final, medida, duracion y ticks de 1, A y B;
- velocidad de sesion;
- velocidad reciente;
- velocidad de B;
- velocidad de A+B;
- velocidad de parte final de 1+A+B;
- estado sostenido o cambio de velocidad;
- resultado posterior de TT;
- tiempo hasta 100 %;
- extension maxima;
- fallo antes del 100 %.
```

Mediciones candidatas para registrar, no reglas definitivas:

```text
velocidad neta = desplazamiento neto / tiempo
velocidad dirigida = desplazamiento en direccion de AUT / tiempo
velocidad por funcion = V1, VA, VB
comparaciones relativas entre sesion, entorno reciente y llegada a AUT
```

### J. Salida teorica provisional

```text
VARIABLE: VELOCIDAD
Regimen de sesion: lenta/media/rapida/muy rapida/tsunami
Fase: previa/brokeraje/estabilizada
Modo: sostenido/cambio/indeterminado
Ventana usada: B / A+B / final de 1+A+B
Estado: PENDIENTE_DE_FORMULA_Y_VALIDACION
```

### K. Prohibiciones

- No reducir Velocidad a B en todos los casos.
- No exigir siempre aceleracion antes de AUT.
- No usar una ventana temporal fija universal.
- No imponer B minima fija de 6 puntos.
- No convertir la observacion ocular en certeza.
- No permitir que Velocidad cambie la lectura TM.
- No crear una regla de operacion antes de validar formulas y datos.
- No mezclar Velocidad con Solapamiento frente a verticalidad.

### L. Estado actual

```text
CONCEPTO: definido
FINALIDAD: definida
HORARIO: definido
BROKERAJE: definido conceptualmente
VENTANA ADAPTATIVA: definida conceptualmente
FORMULAS: pendientes
UMBRALES: pendientes
VALIDACION: pendiente
```

---

## 0.12. VARIABLE 3 - SOLAPAMIENTO FRENTE A VERTICALIDAD

**Estado:** `DEFINICION_TEORICA_CERRADA_PENDIENTE_DE_FORMULA`

### A. Definicion

```text
SOLAPAMIENTO FRENTE A VERTICALIDAD = variable TM que describe
como se distribuye espacialmente el desplazamiento del punto precio
a traves de las velas observadas desde el inicio de la sesion
y en el entorno reciente del momento de decision.
```

La variable no mide Velocidad. Una configuracion puede ser lenta, media o rapida y, de forma independiente, ser vertical o solapada.

La variable tampoco modifica la lectura TM. Solo condiciona la decision en AUT o en FT.

### B. Escala conceptual

```text
0 = SOLAPAMIENTO MAXIMO
10 = VERTICALIDAD MAXIMA
```

La puntuacion inversa puede expresarse como:

```text
SOLAPAMIENTO = 10 - VERTICALIDAD
```

Ejemplo:

```text
Verticalidad = 7/10
Solapamiento = 3/10
```

La escala 0-10 es por ahora una clasificacion profesional visual. Todavia no contiene una formula definitiva.

### C. Aspectos observables

Para valorar la variable se observa exclusivamente:

```text
- longitud espacial de las velas;
- progresion de extremos entre velas consecutivas;
- porcentaje visual de superposicion entre los espacios de las velas;
- cantidad de retorno a espacios ya recorridos;
- continuidad espacial del desplazamiento;
- estabilidad o cambios de regimen dentro de la sesion.
```

No se utilizan Velocidad, indicadores externos ni conceptos ajenos a TM para asignar la puntuacion.

### D. Tipologias de vela y configuracion

Una configuracion puede combinar tamaño y disposicion:

```text
VELAS PEQUEÑAS Y VERTICALES
VELAS MEDIANAS Y VERTICALES
VELAS LARGAS Y VERTICALES

VELAS PEQUEÑAS Y SOLAPADAS
VELAS MEDIANAS Y SOLAPADAS
VELAS LARGAS Y SOLAPADAS
```

El tamaño de vela no determina por si solo la variable:

```text
vela larga puede estar solapada;
vela pequeña puede formar progresion vertical;
```

Por tanto, la puntuacion debe describir la relacion espacial conjunta y no una equivalencia automatica entre tamaño y verticalidad.

### E. Lectura desde el inicio de la sesion

La observacion comienza desde el inicio de la sesion TM y se actualiza continuamente.

Se conservan dos escalas obligatorias:

```text
VERTICALIDAD_SESION
VERTICALIDAD_RECIENTE
```

`VERTICALIDAD_SESION` resume la configuracion acumulada desde el inicio de la sesion.

`VERTICALIDAD_RECIENTE` describe el tramo cercano al momento de decision, sin borrar la referencia de sesion.

Una sola puntuacion global puede ocultar cambios internos. Por ello deben conservarse segmentos o cambios de regimen.

Ejemplo conceptual:

```text
Sesion general: 7/10 vertical
Tramo intermedio: 4/10 vertical
Tramo reciente: 8/10 vertical
```

### F. Interpretacion profesional

Hipotesis teorica:

```text
Mayor verticalidad y menor solapamiento
-> mayor claridad espacial del desplazamiento
-> puede elevar la calidad probabilistica de TT o FT

Mayor solapamiento
-> mayor retorno a espacios anteriores
-> requiere mayor cautela en la decision
```

Esto no es una regla absoluta. Ninguna puntuacion confirma o cancela TT, FT, AUT ni ninguna funcion TM.

### G. Presencia de multiples patrones

Una sesion con predominio de verticalidad puede contener varios desarrollos TT y FT observables. La cantidad de patrones no se deduce automaticamente de la puntuacion.

En una imagen de sesion pueden coexistir:

```text
- varios TT;
- varios FT;
- tramos verticales;
- tramos solapados intermedios;
- cambios de configuracion dentro de la misma sesion.
```

La deteccion exacta del numero de TT y FT corresponde a la lectura TM tick a tick. La imagen sirve para clasificar visualmente la variable, no para sustituir el arbol.

### H. Caso visual canonico USTECM1

En la imagen `USTECM1.png`, tomando como inicio la linea vertical roja proxima a 16:29, la clasificacion profesional preliminar es:

```text
VERTICALIDAD GENERAL = 7/10
SOLAPAMIENTO GENERAL = 3/10
```

Descripcion:

```text
- predominan velas medianas y largas con progresion espacial;
- existen tramos claramente verticales;
- aparecen tramos intermedios con mayor superposicion;
- el conjunto no es verticalidad maxima;
- el conjunto tampoco es una configuracion predominantemente solapada.
```

Segmentacion visual aproximada:

```text
16:29-16:36 -> verticalidad alta
16:36-16:42 -> mayor solapamiento
16:42-16:48 -> verticalidad intermedia
16:48-16:55 -> verticalidad alta
16:55-17:00 -> configuracion mas mixta
```

La imagen permite reconocer multiples desarrollos compatibles visualmente con TT y FT, pero su etiquetado formal requiere la lectura TM.

### I. Arquitectura futura para codigo

La primera implementacion debe registrar datos, no decidir mediante un umbral fijo.

Por cada vela de 1 minuto se propone guardar:

```text
- hora de inicio y final;
- maximo y minimo;
- rango total;
- espacio compartido con vela anterior;
- porcentaje de solapamiento con vela anterior;
- progreso de maximos y minimos;
- desplazamiento neto del conjunto;
- rango acumulado del conjunto;
- posicion dentro del segmento de sesion;
```

Medida candidata de solapamiento entre dos velas:

```text
INTERSECCION = max(0, min(max_1, max_2) - max(min_1, min_2))
UNION = max(max_1, max_2) - min(min_1, min_2)
SOLAPAMIENTO_RELATIVO = INTERSECCION / UNION
```

Esta formula es candidata de investigacion, no definicion final. No capta por si sola progresion, secuencia ni cambios de regimen.

Medidas candidatas adicionales:

```text
PROGRESION_NETA = distancia entre inicio y extremo del segmento
RECORRIDO_ACUMULADO = suma de recorridos de las velas
EFICIENCIA_ESPACIAL = PROGRESION_NETA / RECORRIDO_ACUMULADO
```

La futura puntuacion 0-10 podria combinar:

```text
- solapamiento relativo medio;
- eficiencia espacial;
- progresion de extremos;
- persistencia del regimen;
```

No se aprueban pesos ni umbrales en esta version.

### J. Ventanas futuras

Deben registrarse simultaneamente diferentes horizontes:

```text
SESION COMPLETA DESDE 9:30 NY
TRAMO RECIENTE DE VARIAS VELAS
TRAMO INMEDIATO AL MOMENTO DE DECISION
```

No se fija todavia el numero definitivo de velas del tramo reciente. Debera calibrarse sin mezclar la Variable 3 con Velocidad.

### K. Salida provisional del motor

```text
VARIABLE: SOLAPAMIENTO_FRENTE_A_VERTICALIDAD
Verticalidad_sesion: 0-10
Solapamiento_sesion: 10-Verticalidad_sesion
Verticalidad_reciente: 0-10
Solapamiento_reciente: 10-Verticalidad_reciente
Tipo_visual: pequeña/mediana/larga + vertical/mixta/solapada
Cambios_de_regimen: lista temporal
Estado: PENDIENTE_DE_FORMULA_Y_VALIDACION
```

### L. Prohibiciones

- No usar Velocidad para calcular esta variable.
- No deducir verticalidad solo por el tamaño de una vela.
- No deducir solapamiento solo porque existan retrocesos.
- No usar una unica puntuacion de sesion si existen cambios de regimen relevantes.
- No permitir que esta variable cambie la lectura TM.
- No contar TT o FT solo mediante inspeccion visual cuando existan ticks.
- No fijar pesos, umbrales ni decisiones automaticas antes de validarlos.
- No importar conceptos externos.

### M. Estado actual

```text
CONCEPTO: definido
ESCALA VISUAL 0-10: definida
OBSERVACION DE SESION Y RECIENTE: definida
TIPOLOGIAS: definidas
CASO VISUAL CANONICO: registrado
FORMULA FINAL: pendiente
UMBRALES: pendientes
VALIDACION: pendiente
```

---

## 0.13. PRINCIPIO CONSTITUCIONAL REFORZADO: LECTURA, VARIABLES Y DECISION

**Estado:** `CONFIRMADO_JAVIER`

### A. Tres capas independientes

```text
CAPA 1: LECTURA TM
CAPA 2: CONSULTA CONJUNTA DE VARIABLES
CAPA 3: DECISION Y GESTION
```

### B. Independencia absoluta de la lectura

La lectura TM se resuelve unicamente con el arbol, los ticks, el orden cronologico y las referencias matematicas de la TM.

```text
VARIABLES FAVORABLES
NO crean funciones ni patrones.

VARIABLES DESFAVORABLES
NO borran funciones ni patrones.

LA DECISION DE PARTICIPAR O NO
NO altera la lectura.
```

Queda prohibido:

```text
- cambiar 1, 2, 3, A, B, C, AUT o CUT por una variable;
- confirmar o anular TT o FT por una variable;
- reclasificar un movimiento porque no se participa;
- adaptar retrospectivamente la lectura al resultado de la decision.
```

Ejemplos obligatorios:

```text
TT valido + variables limitantes + no participacion
-> TT sigue siendo valido.

FT valido + variables favorables + participacion
-> FT ya era valido antes de la decision.
```

### C. Organismo conjunto de variables

Las cinco variables se interpretan como un organismo conectado:

```text
Patron
Velocidad
Solapamiento frente a verticalidad
Tiempo de vela de 3 y de 1
Estructura
```

Ninguna variable aislada funciona como veto automatico ni como garantia.

```text
UNA VARIABLE LIMITANTE
puede quedar compensada por informacion muy favorable
de las restantes.

VARIAS VARIABLES LIMITANTES
pueden justificar paciencia y espera.
```

No se utilizara una cadena rigida de filtros `aprobado/rechazado`. La evaluacion futura debe representar probabilidad condicionada conjunta.

### D. Seleccion y paciencia

La TM no busca una cantidad fija de posiciones por sesion.

```text
Una sesion puede ofrecer muchas decisiones validas.
Otra sesion puede ofrecer pocas.
Otra puede no ofrecer ninguna suficientemente seleccionable.
```

La paciencia y la seleccion forman parte de la decision profesional, no de la lectura.

---

## 0.14. VARIABLE 4 - TIEMPO DE VELA DE 3 Y DE 1

**Estado:** `DEFINICION_TEORICA_CERRADA_PENDIENTE_DE_VALIDACION`

### A. Definicion

```text
TIEMPO M1/M3 = posicion temporal exacta del momento de decision
dentro de la vela activa de 1 minuto y de 3 minutos.
```

La variable registra el tiempo transcurrido y restante en ambas velas. Su finalidad es informar del espacio temporal disponible para desarrollar o continuar TT o FT.

### B. Consulta

Se observa continuamente y se registra especialmente en:

```text
AUT
TT al 100 %
extremo real de TT
inicio de FT
```

### C. Datos objetivos

```text
M1_transcurrido_seg
M1_restante_seg
M3_transcurrido_seg
M3_restante_seg
```

Las velas M3 se alinean desde las 9:30 de Nueva York:

```text
9:30-9:33
9:33-9:36
9:36-9:39
...
```

### D. Interpretacion no limitante

Poco tiempo restante es una advertencia, no una prohibicion.

```text
Quedan 5 segundos
+ resto de variables muy favorable
-> la decision puede seguir siendo posible.

Quedan 5-10 segundos
+ velocidad poco favorable
+ configuracion solapada
+ estructura sin informacion positiva suficiente
-> puede ser preferible esperar.
```

Queda prohibida cualquier regla universal como:

```text
SI quedan menos de X segundos -> NO participar.
```

### E. Configuraciones temporales

Deben distinguirse, sin resultado automatico:

```text
mucho tiempo M1 + mucho tiempo M3
poco tiempo M1 + mucho tiempo M3
mucho tiempo M1 + poco tiempo M3
poco tiempo M1 + poco tiempo M3
```

### F. Mediciones posteriores

Tambien se registran:

```text
tiempo desde AUT hasta TT 100 %
tiempo desde TT 100 % hasta extremo real
tiempo desde extremo real hasta FT
```

### G. Salida futura

```text
VARIABLE: TIEMPO_M1_M3
Timestamp servidor
Timestamp Nueva York
M1 inicio/final/transcurrido/restante
M3 inicio/final/transcurrido/restante
Evento: AUT / TT_100 / EXTREMO_TT / FT
Estado: DATO_OBJETIVO_SIN_VETO_AUTOMATICO
```

### H. Prohibiciones

- No permitir que Tiempo modifique la lectura.
- No convertir segundos restantes en veto automatico.
- No interpretar M1 sin conservar M3.
- No interpretar M3 sin conservar M1.
- No asignar umbrales definitivos antes del estudio historico.

---

## 0.15. VARIABLE 5 - ESTRUCTURA

**Estado:** `DEFINICION_TEORICA_CERRADA_PENDIENTE_DE_EXPLORER_Y_VALIDACION`

### A. Definicion

```text
ESTRUCTURA = relacion del punto precio con dos bandas
del grafico de 3 minutos:

SMA de 7 periodos aplicada a High
SMA de 7 periodos aplicada a Low
```

Las bandas son referencias propias de Estructura TM. No deben denominarse soporte, resistencia, pivote ni mediante ningun concepto externo.

### B. Hipotesis profesionales

Observaciones teoricas no deterministas:

```text
Salida fuera de las bandas
-> puede existir tendencia probabilistica a continuar fuera.

Movimiento desde una banda hacia dentro
-> puede existir tendencia probabilistica a recorrer hacia la banda contraria.

Separacion amplia respecto de las bandas
-> puede existir tendencia probabilistica de retorno a una banda
   y nueva decision posterior.
```

Ninguna observacion implica continuidad, giro, retorno o llegada obligatoria.

### C. Elementos observables

```text
- posicion por encima, dentro o por debajo de las bandas;
- proximidad a banda superior o inferior;
- distancia absoluta y normalizada;
- ancho entre bandas;
- permanencia fuera;
- retorno hacia una banda;
- recorrido entre bandas;
- separacion maxima;
- configuracion en AUT, TT 100 %, extremo real y FT.
```

### D. Aprendizaje por entrenamiento

Estructura requiere experiencia acumulada. La finalidad del Explorer es transformar miles de sesiones observadas profesionalmente en:

```text
- biblioteca visual;
- datos sincronizados;
- etiquetas expertas;
- hipotesis medibles;
- futura logica programable.
```

### E. Explorer historico

Periodo propuesto:

```text
Instrumento: USTEC de IC Markets
Historico inicial: 2 años
Ampliacion: 3 años
Observacion previa: 9:15-9:30 Nueva York
Sesion TM: 9:30-12:30 Nueva York
Marco estructural: M3
Bandas: SMA7 High y SMA7 Low
```

El horario se define desde `America/New_York` y se convierte a servidor por fecha. No se programara una diferencia fija con Madrid.

### F. Integracion de todas las variables en Explorer

El Explorer debe recoger juntas, pero sin fusionarlas ni hacerlas decidir todavía:

```text
Lectura TM
Patron
Velocidad
Solapamiento frente a verticalidad
Tiempo M1/M3
Estructura
Resultado posterior
Valoracion profesional
```

Especialmente para Velocidad:

```text
DATOS OBJETIVOS
VALORACION PROFESIONAL
FORMULA AUTOMATICA: pendiente
```

### G. Maximo de tres CSV

La arquitectura aprobada del Explorer genera como maximo:

```text
1. Barras y variables observables
2. Eventos TM y valoracion profesional
3. Resumen de sesiones
```

El Explorer observa, registra y compara. No opera, no modifica la lectura, no inventa patrones y no aplica umbrales definitivos.

### H. Metodo cientifico de trabajo

```text
RECOGER AHORA
DEFINIR DESPUES
VALIDAR ANTES DE DECIDIR
```

El estudio debe separar muestra de exploracion y muestra posterior de validacion. Queda prohibido seleccionar solo configuraciones que confirmen una hipotesis.

### I. Prohibiciones

- No interpretar las bandas con conceptos externos.
- No afirmar `fuera = continuidad`.
- No afirmar `banda = giro`.
- No afirmar `separacion = retorno obligatorio`.
- No permitir que Estructura cambie la lectura.
- No convertir el Explorer en ejecutor de posiciones.
- No mezclar datos candidatos con formulas TM definitivas.

---

## 0.16. ESTADO DE DEFINICION DE VARIABLES

```text
VARIABLE 1 - PATRON
Concepto: cerrado
Formulas estructurales: cerradas por el arbol

VARIABLE 2 - VELOCIDAD
Concepto: cerrado
Formula y umbrales: pendientes de Explorer y validacion

VARIABLE 3 - SOLAPAMIENTO FRENTE A VERTICALIDAD
Concepto y escala visual: cerrados
Formula y umbrales: pendientes de Explorer y validacion

VARIABLE 4 - TIEMPO M1/M3
Concepto y calculo objetivo: cerrados
Interpretacion: conjunta y no limitante
Umbrales: no aprobados

VARIABLE 5 - ESTRUCTURA
Concepto y bandas: cerrados
Reglas fijas: no existen
Formalizacion: pendiente de Explorer y entrenamiento
```

---

## 1. REGLAS CONSTITUCIONALES

1. TM estudia movimientos del punto precio, no el color ni el cierre aislado de una vela.
2. Los ticks reconstruyen la cronologia. Un cambio de vela no termina automaticamente un movimiento.
3. Una vela puede contener varios movimientos y participar simultaneamente en mas de una lectura cuando exista fundamento TM.
4. Cada lectura conserva sus propias referencias: modulo, A Grande, B, AUT, TT, C, CUT, Tercero y FT. No se mezclan niveles.
5. Reclasificar no borra el historial. Lo anterior queda registrado como candidato, confirmado, cancelado, reclasificado o integrado.
6. La salida debe separar siempre **MOVIMIENTOS/FUNCIONES** de **PATRONES**.
7. El analisis debe mostrar todos los escenarios validos, normalmente uno o dos y como maximo tres.

## 2. FILTRO ESTRUCTURAL DE RUIDO, CERRADO

- Una excursion contraria **inferior a 2,00 puntos** es ruido.
- El ruido no crea movimiento TM y no activa A, B, C, AUT, CUT, TT, Tercero ni FT.
- Al alcanzar **exactamente 2,00 puntos**, el movimiento se confirma retroactivamente desde el extremo anterior.
- Tras B Grande, un retroceso de 2,00 puntos confirma la C Grande minima.
- El filtro se aplica antes de abrir funciones o lecturas y evita calcular micromovimientos.

## 3. APERTURA DE VELA: GAP, COLA Y POSIBLE 2

Orden obligatorio:

1. Evaluar el gap entre cierre anterior y apertura nueva.
2. Si existe gap, **no hay 2**.
3. Sin gap, observar la cola inicial.
4. Si aparece cola observable superior a 1 tick TM, 0,25 puntos, **no hay 2**.
5. Solo la salida en plano, sin gap y sin cola observable superior a 0,25, permite evaluar 2.
6. Un 2 ya confirmado no se borra por una evolucion posterior.

## 4. SECUENCIA MODULAR CENTRAL

### 4.1. 1, 2, 3 y modulo

- 1 abre la lectura.
- 2 exige continuidad en la misma direccion, salida en plano, ausencia de cola prohibitiva y desplazamiento suficiente.
- 3 solo se evalua despues de 2 confirmado y conforme a sus fronteras canonicas.
- Si falla 2, el 1 puede quedar como modulo por descarte y el contrario pasa a A Grande.
- Si falla 3, 1+2 forman modulo y el contrario es A Grande.

### 4.2. A Grande

- A Grande es el movimiento contrario al modulo.
- Puede atravesar varias velas y termina en su extremo real, no en el primer extremo provisional.
- Un cambio de vela no cierra A Grande.

### 4.3. B candidata, B Grande y AUT

- Antes del 100 % de A Grande, el movimiento contrario es **B candidata**.
- Al alcanzar al menos el 100 % de A Grande sin superar el limite AUT, se confirma **B Grande**.
- Limite AUT: 127 % de A Grande + 0,25 puntos.
- Tocar exactamente el limite sin superarlo mantiene B Grande.
- Superar estrictamente el limite confirma **AUT inmediatamente** y B deja de ser la clasificacion vigente del recorrido.

### 4.4. C Grande, CUT y Tercero

- Una vez confirmada B Grande, todo movimiento estructural posterior contrario a B es C Grande, no C candidata.
- El minimo estructural de C Grande es 2,00 puntos por el filtro de ruido.
- Si B crea un nuevo extremo antes de CUT, la C queda cancelada como vigente, pero no se borra del historial.
- CUT se evalua con la referencia canonica del final de A y conforme al parche v1.2.
- Tras C/CUT se evalua Tercero y el reset exactamente en el orden fijado por v1.2.

## 5. AUT, TT, RESET Y DOBLE PERTENENCIA

- AUT habilita TT posible, pero TT solo se confirma al alcanzar el 100 % de la expansion del modulo desde el final de A Grande.
- El 100 % es el minimo de confirmacion. TT puede extenderse mas alla del 100 % hasta su extremo real.
- El movimiento que confirma TT es simultaneamente cierre del patron anterior y nuevo 1 del ciclo siguiente.
- Puede existir doble pertenencia: una vela que alcanza AUT puede ser a la vez un 1 y un TT pequeno; velas posteriores pueden completar el TT del 1 original.
- Al confirmarse TT existe reset de lectura para analizar el nuevo 1 sin borrar el TT que acaba de cerrarse.
- AUT y TT pueden confirmarse en el mismo tick si el salto cruza ambas referencias.

## 6. FT POSTERIOR A TT

- FT solo existe despues de un TT confirmado.
- TT se mide hasta su extremo real, no se detiene artificialmente en el 100 %.
- El movimiento contrario posterior, claro y estructural, se evalua como FT del TT anterior.
- FT puede coexistir con funciones modulares de una nueva lectura. Debe declararse por separado en la capa PATRONES.
- Nunca se oculta un FT claro por estar analizando simultaneamente un modulo, un 1 o una A Grande.

## 7. CONCURRENCIA Y RECLASIFICACION

- Normalmente se mantienen una o dos lecturas; excepcionalmente tres.
- Una misma vela puede pertenecer al TT de una lectura y al nuevo 1 de otra fase de esa misma lectura.
- Retrocesos posteriores pueden reclasificar conjuntamente velas previas como modulo o como 1.
- Cada escenario debe conservar su matematica y sus referencias independientes.
- La respuesta final enumera todos los escenarios coherentes, sin seleccionar uno por intuicion si los ticks no permiten cerrarlo.

## 8. CASO CANONICO VELAS 8 Y 9

1. El analisis independiente comienza en la vela 8 descendente, clasificada como 1.
2. La vela 9 abre con gap de retroceso, por lo que no puede ser 2.
3. En la vela 9 aparecen A, B, AUT y posible TT segun el orden intravela.
4. A Grande se mide desde el final de la vela 8 hasta el maximo real de la vela 9.
5. El modulo de la vela 8 se mide desde su maximo hasta su minimo y vale X.
6. Desde el final de A Grande, en el maximo de la vela 9, se mide el descenso.
7. Si el descenso alcanza X, llega al 100 % y confirma TT.
8. Al confirmar TT, la vela 9 puede cerrar el patron anterior y actuar como nuevo 1 para el ciclo siguiente.

## 9. FORMATO OBLIGATORIO DE RESPUESTA TM

Para cada vela o tramo:

1. **Cronologia intravela:** recorrido real por ticks.
2. **Lectura 1:** movimientos/funciones.
3. **Lectura 2:** si existe.
4. **Lectura 3:** solo excepcionalmente.
5. **Patrones:** TT y FT, separados de los movimientos.
6. **Niveles matematicos:** modulo, final de A, 100 %, 127 % + 0,25, TT, CUT y demas referencias aplicables.
7. **Estado:** candidato, confirmado, cancelado, reclasificado, integrado o pendiente por falta de ticks.
8. **Escenarios completos:** no omitir alternativas coherentes.

## 10. PROHIBICIONES ABSOLUTAS

- No llamar 2 sin evaluar antes gap y cola.
- No llamar B Grande antes del 100 %.
- No mantener B como vigente despues de superar AUT.
- No llamar C antes de B Grande confirmada.
- No tratar como movimiento una excursion inferior a 2 puntos.
- No confirmar TT antes del 100 %.
- No detener TT en el 100 % si el movimiento continua.
- No llamar FT sin TT previo.
- No mezclar movimientos y patrones en una sola lista ambigua.
- No borrar clasificaciones previas al reclasificar.
- No responder con una sola lectura si existe otra lectura TM matematicamente coherente.

## 11. DOCUMENTO NORMATIVO COMPLETO

A continuacion se incorpora integramente el arbol canónico v1, seguido de los parches y de todas las versiones fuente relevantes. Esta incorporacion literal garantiza trazabilidad y evita perdida de reglas. Si una frase historica contradice las secciones 0-10 o un parche posterior, prevalece la regla mas reciente segun la precedencia de la seccion 0.


---

# ANEXO 1 - FUENTE INTEGRA: `TM_ARBOL_CANONICO_COMPLETO_v1.md`

- **SHA-256:** `e9d4b419868233949b4459f9b97294b8b5487e84c7c4ee5a92aa3289113cfd3e`
- **Integridad:** contenido incorporado sin recortes.

# TM — ÁRBOL CANÓNICO COMPLETO v1

- **Documento:** `control/TM_ARBOL_CANONICO_COMPLETO_v1.md`
- **Versión:** 1.0
- **Fecha:** 2026-10-19
- **Autoridad experta:** Javier Armada López
- **Estado:** BORRADOR CANÓNICO PARA REVISIÓN DE JAVIER
- **Uso:** documento maestro de ramas, estados y transiciones. No es código, no es golden y no sustituye a las fuentes.
- **Regla de control:** si una rama no está cerrada por una fuente o por una decisión expresa de Javier, se escribe `PENDIENTE_JAVIER`. No se completa por intuición.

## 0. CONTROL DE FUENTES Y ALCANCE

### 0.1. Fuentes leídas

1. `00_LEEME_PRIMERO_PRIORIDAD_DOCUMENTOS_TM.txt`
2. `AGENTS.md`
3. `control/DECISIONES_EXPERTO.md`
4. `control/REGLAS_CERRADAS.md`
5. `Dossier_TM_v3_Lectura_Obligatoria.txt`
6. `Dossier_TM_v4_Concurrencia_Reclasificacion.txt`
7. `control/CONTRADICCIONES.md`
8. `control/REGLAS_PROVISIONALES.md`
9. `control/DICCIONARIO_TM.md`
10. `PROMPT_OPENBOT_TM_ARBOL_CANONICO.txt` (instrucción de esta fase)

No existe `control/CASOS_VALIDADOS.md` en la fecha de creación.

### 0.2. Precedencia aplicada

1. Corrección expresa de Javier.
2. `DECISIONES_EXPERTO.md`.
3. `REGLAS_CERRADAS.md`.
4. Dossier v3.
5. Adenda v4.
6. Resto de documentación, solo como apoyo.

Si dos fuentes discrepan y no hay corrección expresa, la rama queda `PENDIENTE_JAVIER` y se registra en `TM_DUDAS_PENDIENTES_JAVIER.md`.

### 0.3. Prohibiciones de esta fase

- No programar.
- No generar MQL5.
- No modificar golden.
- No modificar tests.
- No modificar documentos vigentes.
- No abrir una lectura nueva sin regla TM expresa.
- No etiquetar una función si falta su precondición.
- No usar análisis técnico externo.
- No tratar conversaciones de asistentes como normativa.

---

## 1. MAPA DE REGLAS CONFIRMADAS Y PENDIENTES

### 1.1. Reglas cerradas que gobiernan el árbol

| ID | Regla | Fuente | Nodo |
|---|---|---|---|
| BASE-1 | La TM estudia movimientos, no colores de velas. | `REGLAS_CERRADAS` BASE-1 | N-001, N-032 |
| BASE-2 | Un cambio de vela no termina automáticamente un movimiento. | BASE-2 | N-013, N-038 |
| BASE-3 | El orden intravela es obligatorio. | BASE-3 | N-001, N-038 |
| BASE-4 | Una vela puede contener varios movimientos. | BASE-4 | N-001, N-028 |
| BASE-5 | Un movimiento puede atravesar varias velas. | BASE-5 | N-013, N-038 |
| BASE-6 | Un cambio de dirección solo crea movimiento TM nuevo si alcanza referencia TM; si no, queda integrado. | BASE-6 | N-032 |
| A1 | `2` exige misma dirección, rango ≥ rango de 1, salida en plano y cola ≤ 0,25; confirmación por desplazamiento direccional. | A1 | N-005, N-006, N-007, N-008 |
| A2 | Módulo regular 1+2: rango de expansión = `High−Low` completo del conjunto. | A2 | N-012 |
| A3 | TT = final de A ± rango del módulo. | A3 | N-018, N-019 |
| A4 | Primero gap; con gap no se aplica la regla de 2. | A4 / H11 | N-002, N-003, N-004 |
| B1 | AUT = B Grande supera `127 % + 0,25` (1 tick). | B1 / H8 | N-017 |
| B2 | AUT no confirma por sí solo nuevo 1 ni TT; deja TT pendiente si hay módulo. | B2 | N-018 |
| B3 | Orden causal B Grande confirmada → AUT → TT; TT puede confirmarse en el mismo tick. | B3 | N-017, N-018, N-019, N-033 |
| B4 | AUT y CUT pueden coexistir en momentos distintos de la misma lectura. | B4 | N-024 |
| B5 | B Grande y AUT no coexisten como clasificación vigente del mismo recorrido. | B5 | N-017, N-037 |
| H1 | C Grande puede desembocar en CUT o en nuevo 1; la condición exacta de `C = nuevo 1` sigue pendiente. | H1 | N-025 |
| H2 | `C = nuevo 1` pertenece a la lectura modular; FT pertenece a la lectura de patrones. | H2 | N-025, N-026 |
| H3 | Ante C Grande se comprueban, en orden: CUT; C como nuevo 1; C como A Grande de una lectura mayor. | H3 | N-034 |
| H4 | A Grande puede ocupar dos velas; B puede comenzar dentro de la segunda. | H4 | N-013, N-038 |
| H5 | Doble medición Fibonacci independiente: retroceso de A solo confirma B; expansión del módulo solo confirma TT. | H5 | N-014, N-019 |
| H6 | Cada lectura concurrente puede tener su propio autocorte. | H6 | N-028, N-029 |
| H9 | AUT exige superar, no solo tocar, `127 % + 0,25`. | H9 | N-016, N-017 |
| H10 | Lecturas concurrentes se nombran lectura 1 / 2 / 3. | H10 | N-028, N-029 |
| H11 | Gap primero; con gap no hay salida en plano, ni posible 2, ni 2. | H11 | N-002, N-003, N-004 |
| H12 | B candidata antes del 100 %; el 100 % confirma B Grande. | H12 | N-014, N-015 |
| H13 | Desde B Grande: 100–127 % + 0,25 → B Grande; cambio de sentido → C Grande; superar → AUT; nuevo extremo de B cancela C. | H13 | N-015, N-016, N-017, N-022, N-023 |
| H14 | Plano si `|cierre vela anterior − apertura siguiente| ≤ 0,25`; si > 0,25 es gap. | H14 | N-002, N-005 |
| H15 | A Grande no se cierra en el primer extremo si la vela siguiente lo extiende; el fin es el extremo real. | H15 | N-013, N-038 |
| H16 | Concurrencia habitual: normalmente 2 lecturas, excepcionalmente 3; no se calculan ruido ni micromovimientos. | H16 / DEC-015 | N-028, N-029, N-032 |
| H17 | Módulo por descarte (vela anterior) es PROVISIONAL, no regla general. | H17 | N-012 |
| DEC-004 | Vocabulario de concurrencia: lectura 1 / 2 / 3. | DEC-004 | N-028, N-029 |
| DEC-015 | Concurrencia habitual y filtro metodológico de ruido/micromovimientos. | DEC-015 | N-032 |

### 1.2. Ramas pendientes que condicionan el árbol

| ID | Pendiente | Fuente | Nodo |
|---|---|---|---|
| P2 | Serie de precio definitiva (Bid/Ask/Last/medio). En la muestra se usa Bid, sin ratificación experta. | `REGLAS_PROVISIONALES` P2 | N-001, N-019 |
| P3 | Tick exacto de confirmación de A/B/C Grande más allá del umbral numérico. | P3 | N-013, N-014, N-022 |
| P4 | Criterios exactos de reclasificación como módulo o 1 conjunto. | P4 | N-027 |
| P5 | Prioridad y permanencia cuando dos o tres lecturas alcanzan nivel en el mismo tick. | P5 | N-030 |
| P6 | Regla matemática completa de FT. | P6 | N-026 |
| PR-e | Condición exacta de `C = nuevo 1` cuando C no alcanza CUT. | PR-e | N-025 |
| PR-g | Umbral numérico entre ruido y movimiento TM. | PR-g | N-032 |
| DUDA-009 | Regla general del módulo: ¿siempre 2 velas o una sola / vela anterior por descarte? | DUDA-009 | N-012 |
| DUDA-J01 | Regla expresa para abrir L2/L3. | Esta auditoría | N-028, N-029 |
| DUDA-J02 | Módulo general. | Esta auditoría | N-012 |
| DUDA-J03 | Prioridad mismo tick. | Esta auditoría | N-030 |
| DUDA-J04 | `C = nuevo 1`. | Esta auditoría | N-025 |
| DUDA-J05 | FT. | Esta auditoría | N-026 |

---

## 2. ARQUITECTURA A — CONTROLADOR DE CONCURRENCIA L1-L3

### 2.1. Slots

| Slot | Nombre funcional | Función |
|---|---|---|
| L1 | `lectura 1` | Lectura de referencia principal. |
| L2 | `lectura 2` | Segunda lectura coherente, solo con regla expresa. |
| L3 | `lectura 3` | Tercera lectura coherente, solo con regla expresa. |

`L1`, `L2` y `L3` son identificadores de slot; la capa funcional usa `lectura 1`, `lectura 2` y `lectura 3` (DEC-004 / H10).

### 2.2. Regla central

- No se abre L2 o L3 por observar varios movimientos dentro de una vela.
- Una lectura nueva solo se abre si existe una **regla TM expresa**.
- Cada función pertenece a una lectura concreta.
- No se mezclan referencias entre lecturas.
- La concurrencia es habitual: normalmente 2 lecturas; excepcionalmente 3; nunca 4.
- El ruido y los micromovimientos no se calculan, no se clasifican y no ocupan lectura.

### 2.3. Condiciones de apertura

| ID | Condición | Estado | Consecuencia |
|---|---|---|---|
| OPEN-L2-01 | AUT local que puede ser nuevo 1 y TT pequeño. | `PENDIENTE_JAVIER` | Si se confirma, abre L2; si no, el movimiento pertenece a L1. |
| OPEN-L2-02 | Reclasificación de velas anteriores como módulo o 1 conjunto. | `PENDIENTE_JAVIER` | Si se confirma, puede abrir o transformar L2. |
| OPEN-L2-03 | Segunda lectura ya contenida en una referencia mayor. | `PENDIENTE_JAVIER` | No se abre hasta que Javier fije la regla. |
| OPEN-L3-01 | Tercera lectura matemáticamente válida y coherente. | `PENDIENTE_JAVIER` | Solo puede existir si L1 y L2 siguen válidas y hay regla expresa. |

### 2.4. Prioridad y permanencia

- Una lectura permanece activa hasta una resolución matemática: TT confirmado, CUT confirmado, invalidación por final de A, reclasificación/integración o pérdida de coherencia.
- La prioridad cuando dos o tres lecturas alcanzan nivel en el mismo tick es `PENDIENTE_JAVIER` (P5 / DUDA-J03).
- No se resuelve por preferencia del agente, por color de vela ni por resultado posterior.
- Cada lectura conserva su propio módulo, A, B, AUT, TT, nuevo 1 y nivel de invalidación.

### 2.5. Cierre y archivo

| Evento | Efecto | Estado |
|---|---|---|
| TT confirmado | La lectura puede finalizar o continuar según su ciclo. | CERRADO |
| CUT confirmado | Cierre de la rama C/CUT de esa lectura. | CERRADO |
| Final de A tocado antes de TT | TT cancelado; recorrido anterior pasa a módulo; retorno = A Grande. | CERRADO |
| Reclasificación | Cambia la función, no se borra el historial. | PROVISIONAL |
| Pérdida de coherencia | Lectura invalidada; se conserva en eventos. | CERRADO |
| Límite L3 | No se abre L4. | CERRADO |

---

## 3. ARQUITECTURA B — MÁQUINA DE ESTADOS POR LECTURA

### 3.1. Dos ejes que no deben confundirse

**Fase TM (qué función representa el recorrido):**

`1_ACTIVA`, `2_CANDIDATA`, `2_CONFIRMADA`, `3_CANDIDATA`, `3_CONFIRMADA`, `MODULO`, `A_GRANDE`, `B_CANDIDATA`, `B_GRANDE`, `AUT`, `TT_PENDIENTE`, `TT_CONFIRMADO`, `NUEVO_1`, `C_GRANDE`, `CUT`, `FT`, `TT_FALLIDO`.

**Estado de ciclo de vida (qué le ocurre a la lectura):**

`CANDIDATA`, `ACTIVA`, `CONFIRMADA`, `PENDIENTE`, `RECLASIFICADA`, `INTEGRADA`, `INVALIDADA`, `FINALIZADA`.

### 3.2. Estados funcionales permitidos

| Estado | Significado | Entrada | Salida |
|---|---|---|---|
| `1_ACTIVA` | Movimiento inicial del módulo. | N-001 | N-005 / N-008 / N-012 |
| `2_CANDIDATA` | Movimiento en misma dirección que 1, aún sin confirmar 2. | N-006 | N-007 / N-008 |
| `2_CONFIRMADA` | 2 confirmado por desplazamiento direccional. | N-007 | N-009 / N-011 |
| `3_CANDIDATA` | Retroceso 0–50 % y intención de superar extremo de 2. | N-009 | N-010 / N-011 |
| `3_CONFIRMADA` | 3 confirmado. | N-010 | Ciclo modular |
| `MODULO` | 1+2 (o conjunto validado) como referencia. | N-008 / N-011 / N-020 | N-012 / N-013 |
| `A_GRANDE` | Movimiento contrario al módulo. | N-011 / N-020 | N-014 |
| `B_CANDIDATA` | Movimiento contrario a A por debajo del 100 %. | N-014 | N-015 |
| `B_GRANDE` | B confirmada en 100 %–127 % + 0,25. | N-015 | N-017 / N-022 / N-023 |
| `AUT` | B superó 127 % + 0,25; TT pendiente. | N-017 | N-018 |
| `TT_PENDIENTE` | AUT activo; objetivo TT no alcanzado. | N-018 | N-019 / N-020 |
| `TT_CONFIRMADO` | Objetivo TT alcanzado. | N-019 | N-021 / N-026 |
| `NUEVO_1` | Movimiento que completa TT; nueva referencia. | N-019 / N-025 | Ciclo posterior |
| `C_GRANDE` | Movimiento contrario a B confirmada. | N-022 | N-023 / N-024 / N-025 |
| `CUT` | C Grande supera final de A. | N-024 | Cierre de rama |
| `FT` | Fin de tendencia tras TT. | N-026 | Cierre de patrón |
| `TT_FALLIDO` | TT no alcanzado y final de A tocado. | N-020 | N-011 / N-012 |

### 3.3. Transiciones de ciclo de vida

| Desde | Evento | Hasta |
|---|---|---|
| `CANDIDATA` | Evidencia insuficiente | `PENDIENTE` |
| `CANDIDATA` | Precondiciones cumplidas | `ACTIVA` |
| `ACTIVA` | Confirmación matemática | `CONFIRMADA` |
| `ACTIVA` | Corrección de referencia | `RECLASIFICADA` |
| `ACTIVA` | Absorción por lectura mayor | `INTEGRADA` |
| `ACTIVA` | Nivel de invalidación | `INVALIDADA` |
| `CONFIRMADA` | TT/CUT/FT o fin de ciclo | `FINALIZADA` |
| `RECLASIFICADA` | Nueva función estable | `ACTIVA` o `FINALIZADA` |
| `INVALIDADA` | Conservación histórica | `FINALIZADA` |

### 3.4. Invariantes

1. No hay 2 sin 1.
2. No hay 3 sin 2.
3. No hay módulo regular sin fallo de 2 o de 3, salvo módulo por descarte `PENDIENTE_JAVIER`.
4. No hay A Grande sin módulo.
5. No hay B Grande sin A Grande.
6. No hay C Grande sin B Grande confirmada en la misma lectura.
7. No hay CUT sin C Grande válida y sin superar el final de A.
8. No hay TT sin AUT y sin módulo.
9. No hay TT confirmado sin alcanzar el 100 % del objetivo.
10. No hay FT sin TT confirmado.
11. B Grande y AUT no coexisten en el mismo recorrido.
12. Cada lectura conserva sus propios niveles; no se mezclan.
13. Reclasificar no borra el evento anterior.

---

## 4. ARQUITECTURA C — ÁRBOL COMPLETO DE TRANSICIONES

> Formato obligatorio. `ESTADO_APROBACIÓN` usa `CERRADO`, `PROVISIONAL`, `PENDIENTE_JAVIER` o `NO_APLICA`.
> Los tests se despliegan en `TM_TESTS_REQUERIDOS_v1.md`.

### N-001 — Inicio de lectura y 1

- **ID:** N-001
- **ESTADO_ORIGEN:** `SIN_LECTURA`
- **EVENTO:** Primer movimiento direccional con referencia TM válida.
- **PRECONDICIONES:** Orden temporal reconstruido; no es ruido; no hay lectura previa en el slot.
- **FÓRMULA:** Dirección de 1 = dirección del movimiento; no exige rango mínimo teórico.
- **SI_TRUE:** Abre L1 como `1_ACTIVA/ACTIVA`.
- **SI_FALSE:** Permanece `SIN_LECTURA`.
- **ESTADO_DESTINO:** `1_ACTIVA/ACTIVA`
- **LECTURA_AFECTADA:** L1
- **¿ABRE_NUEVA_LECTURA?:** SÍ, L1.
- **PROHIBICIONES:** No clasificar 2, 3, A, B o C antes de 1; no usar color de vela.
- **DATOS_A_GUARDAR:** inicio, extremo, dirección, timestamps, fuente, serie de precio.
- **TEST_POSITIVO:** T-001
- **TEST_NEGATIVO:** T-040
- **TEST_FRONTERA:** T-001
- **ESTADO_APROBACIÓN:** `PROVISIONAL` (detección general del 1 inicial; el caso de la vela 1 está validado).

### N-002 — Apertura de vela: gap o plano

- **ID:** N-002
- **ESTADO_ORIGEN:** `1_ACTIVA`, `2_CONFIRMADA` o lectura activa.
- **EVENTO:** Apertura de vela nueva.
- **PRECONDICIONES:** Cierre de vela anterior y apertura nueva disponibles.
- **FÓRMULA:** `Δ = apertura_nueva − cierre_vela_anterior`. `|Δ| ≤ 0,25` = plano; `|Δ| > 0,25` = gap.
- **SI_TRUE:** Si plano → N-005; si gap → N-003 o N-004.
- **SI_FALSE:** Sin datos suficientes → `PENDIENTE_JAVIER`; no evaluar 2.
- **ESTADO_DESTINO:** `EVALUANDO_APERTURA` (control) → `2_CANDIDATA` o `A_GRANDE`.
- **LECTURA_AFECTADA:** L1/L2/L3 activa.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No aplicar la regla de 2 antes del gap; no usar el cierre del movimiento como referencia.
- **DATOS_A_GUARDAR:** `Δ`, cierre anterior, apertura nueva, timestamps, decisión plano/gap.
- **TEST_POSITIVO:** T-004
- **TEST_NEGATIVO:** T-037
- **TEST_FRONTERA:** T-038
- **ESTADO_APROBACIÓN:** `CERRADO` (H14 / H11).

### N-003 — Gap a favor de 1

- **ID:** N-003
- **ESTADO_ORIGEN:** `EVALUANDO_APERTURA` con gap.
- **EVENTO:** Gap en la misma dirección que 1.
- **PRECONDICIONES:** 1 activo; gap confirmado; dirección del gap = dirección de 1.
- **FÓRMULA:** `signo(Δ) = signo(1)`.
- **SI_TRUE:** A y B implícitas; posible TT; pasa a `TT_PENDIENTE`.
- **SI_FALSE:** N-004.
- **ESTADO_DESTINO:** `TT_PENDIENTE` (AUT por gap: `PENDIENTE_JAVIER`).
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No evaluar 2; no confirmar TT sin 100 %; no afirmar AUT por gap sin regla.
- **DATOS_A_GUARDAR:** tamaño del gap, A/B implícitas, módulo aplicable, objetivo TT.
- **TEST_POSITIVO:** T-002
- **TEST_NEGATIVO:** T-037
- **TEST_FRONTERA:** T-002
- **ESTADO_APROBACIÓN:** `CERRADO` para A/B implícitas y no 2; `PENDIENTE_JAVIER` para AUT por gap.

### N-004 — Gap contrario a 1

- **ID:** N-004
- **ESTADO_ORIGEN:** `EVALUANDO_APERTURA` con gap.
- **EVENTO:** Gap en dirección contraria a 1.
- **PRECONDICIONES:** 1 activo; gap confirmado; dirección contraria.
- **FÓRMULA:** `signo(Δ) = −signo(1)`.
- **SI_TRUE:** El movimiento es A Grande en dirección del gap; se sigue midiendo A con ticks.
- **SI_FALSE:** N-003.
- **ESTADO_DESTINO:** `A_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No evaluar 2; no llamar B antes de A.
- **DATOS_A_GUARDAR:** gap, inicio de A, extremo, timestamps.
- **TEST_POSITIVO:** T-003
- **TEST_NEGATIVO:** T-002
- **TEST_FRONTERA:** T-003
- **ESTADO_APROBACIÓN:** `CERRADO` (H11 / v3 §9.2).

### N-005 — Sin gap: salida en plano

- **ID:** N-005
- **ESTADO_ORIGEN:** `1_ACTIVA` tras apertura sin gap.
- **EVENTO:** Apertura nueva dentro de ±0,25 del cierre anterior.
- **PRECONDICIONES:** `|Δ| ≤ 0,25`; no hay gap.
- **FÓRMULA:** `|apertura_nueva − cierre_vela_anterior| ≤ 0,25`.
- **SI_TRUE:** Abre evaluación de posible 2 → N-006.
- **SI_FALSE:** Es gap → N-003/N-004.
- **ESTADO_DESTINO:** `2_CANDIDATA/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No llamar 2 solo por continuidad de dirección; no usar `Close(1)` del movimiento si la regla exige cierre de vela.
- **DATOS_A_GUARDAR:** `Δ`, cierre anterior, apertura, timestamps.
- **TEST_POSITIVO:** T-004
- **TEST_NEGATIVO:** T-037
- **TEST_FRONTERA:** T-038
- **ESTADO_APROBACIÓN:** `CERRADO` (H14).

### N-006 — Posible 2

- **ID:** N-006
- **ESTADO_ORIGEN:** `1_ACTIVA` / `EVALUANDO_2`.
- **EVENTO:** Movimiento en la misma dirección que 1 tras salida en plano.
- **PRECONDICIONES:** (a) misma dirección que 1; (b) rango de 2 ≥ rango de 1; (c) salida en plano; (d) cola observable ≤ 0,25.
- **FÓRMULA:** `rango_2 ≥ rango_1`; alcista `Low(2) = Open(2)`; bajista `High(2) = Open(2)`; tolerancia 0,25.
- **SI_TRUE:** `2_CANDIDATA`.
- **SI_FALSE:** N-008 (módulo + A Grande).
- **ESTADO_DESTINO:** `2_CANDIDATA/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No confirmar 2 por `High−Low`; no ignorar cola > 0,25.
- **DATOS_A_GUARDAR:** rango 1, rango 2, cola, apertura, cierre, timestamps.
- **TEST_POSITIVO:** T-001
- **TEST_NEGATIVO:** T-005
- **TEST_FRONTERA:** T-005
- **ESTADO_APROBACIÓN:** `CERRADO` (A1).

### N-007 — Confirmar 2

- **ID:** N-007
- **ESTADO_ORIGEN:** `2_CANDIDATA`.
- **EVENTO:** Desplazamiento direccional de 2 alcanza el tamaño de 1.
- **PRECONDICIONES:** N-006 cumplido; no hay gap.
- **FÓRMULA:** `desplazamiento_direccional(2) ≥ rango(1)`.
- **SI_TRUE:** `2_CONFIRMADA/ACTIVA`.
- **SI_FALSE:** Permanece candidata o N-008 si falla una condición.
- **ESTADO_DESTINO:** `2_CONFIRMADA/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No borrar 2 si después aparece el contrario; no llamar 3.
- **DATOS_A_GUARDAR:** tick de confirmación, desplazamiento, rango 1.
- **TEST_POSITIVO:** T-001
- **TEST_NEGATIVO:** T-005
- **TEST_FRONTERA:** T-001
- **ESTADO_APROBACIÓN:** `CERRADO` (A1).

### N-008 — Fallo de 2

- **ID:** N-008
- **ESTADO_ORIGEN:** Evaluación de 2.
- **EVENTO:** Falla dirección, rango, plano o cola.
- **PRECONDICIONES:** Alguna condición de N-006 no se cumple.
- **FÓRMULA:** Negación de N-006.
- **SI_TRUE:** 1 pasa a módulo por descarte; movimiento contrario = A Grande.
- **SI_FALSE:** N-007.
- **ESTADO_DESTINO:** `MODULO/ACTIVA` + `A_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No llamar 2; no llamar 3; conservar 1.
- **DATOS_A_GUARDAR:** causa del fallo, rango 1, extremos, timestamps.
- **TEST_POSITIVO:** T-005
- **TEST_NEGATIVO:** T-001
- **TEST_FRONTERA:** T-005
- **ESTADO_APROBACIÓN:** `CERRADO` (A1).

### N-009 — Posible 3

- **ID:** N-009
- **ESTADO_ORIGEN:** `2_CONFIRMADA`.
- **EVENTO:** Retroceso y nuevo extremo.
- **PRECONDICIONES:** Retroceso entre 0 % y 50 % del rango de 2; superación del extremo de 2.
- **FÓRMULA:** alcista `High(3) > High(2)`; bajista `Low(3) < Low(2)`; retroceso 0–50 %.
- **SI_TRUE:** `3_CANDIDATA/ACTIVA`.
- **SI_FALSE:** N-011.
- **ESTADO_DESTINO:** `3_CANDIDATA/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No llamar 3 si retrocede > 50 %; no borrar 2.
- **DATOS_A_GUARDAR:** retroceso, extremo 2, extremo 3, timestamps.
- **TEST_POSITIVO:** T-007 / T-009
- **TEST_NEGATIVO:** T-008
- **TEST_FRONTERA:** T-007
- **ESTADO_APROBACIÓN:** `CERRADO` (v3 §4.3).

### N-010 — Confirmar 3

- **ID:** N-010
- **ESTADO_ORIGEN:** `3_CANDIDATA`.
- **EVENTO:** Se cumplen simultáneamente las dos reglas de 3.
- **PRECONDICIONES:** Retroceso 0–50 % y superación del extremo de 2.
- **FÓRMULA:** N-009.
- **SI_TRUE:** `3_CONFIRMADA/ACTIVA`; ciclo modular regular.
- **SI_FALSE:** N-011.
- **ESTADO_DESTINO:** `3_CONFIRMADA/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No usar 3 como módulo sin confirmar; no mezclar con A.
- **DATOS_A_GUARDAR:** tick de confirmación, extremos, retroceso.
- **TEST_POSITIVO:** T-009
- **TEST_NEGATIVO:** T-008
- **TEST_FRONTERA:** T-007
- **ESTADO_APROBACIÓN:** `CERRADO` (v3 §4.3).

### N-011 — Fallo de 3: módulo 1+2 y A Grande

- **ID:** N-011
- **ESTADO_ORIGEN:** Evaluación de 3.
- **EVENTO:** Retroceso > 50 % o no supera extremo de 2.
- **PRECONDICIONES:** 2 confirmado; 3 no válido.
- **FÓRMULA:** Negación de N-009.
- **SI_TRUE:** `1+2 = MODULO`; movimiento contrario = `A_GRANDE`.
- **SI_FALSE:** N-010.
- **ESTADO_DESTINO:** `MODULO/ACTIVA` + `A_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No crear C antes de B; no llamar 3 fallido a un 2 no confirmado.
- **DATOS_A_GUARDAR:** rango del módulo, extremos, velas implicadas, timestamps.
- **TEST_POSITIVO:** T-010
- **TEST_NEGATIVO:** T-009
- **TEST_FRONTERA:** T-008
- **ESTADO_APROBACIÓN:** `CERRADO` para 1+2 regular; `PENDIENTE_JAVIER` para módulo general.

### N-012 — Medida del módulo

- **ID:** N-012
- **ESTADO_ORIGEN:** `MODULO`.
- **EVENTO:** Calcular rango de expansión.
- **PRECONDICIONES:** Composición del módulo conocida.
- **FÓRMULA:** `rango_modulo = max(highs) − min(lows)` del conjunto de velas del módulo.
- **SI_TRUE:** Guardar máximo, mínimo, rango, velas, timestamps y lectura de origen.
- **SI_FALSE:** Si la composición no está cerrada → `PENDIENTE_JAVIER`.
- **ESTADO_DESTINO:** `MODULO/ACTIVA` con rango calculado.
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No usar solo la última vela; no usar el rango de A como módulo; no inventar módulo de una vela.
- **DATOS_A_GUARDAR:** máximo, mínimo, rango, velas, timestamps.
- **TEST_POSITIVO:** T-011
- **TEST_NEGATIVO:** T-011
- **TEST_FRONTERA:** T-011
- **ESTADO_APROBACIÓN:** `CERRADO` para 1+2 regular; `PENDIENTE_JAVIER` para módulo por descarte / una vela (H17 / DUDA-009).

### N-013 — A Grande se extiende entre velas

- **ID:** N-013
- **ESTADO_ORIGEN:** `A_GRANDE`.
- **EVENTO:** La vela siguiente continúa la dirección de A sin volver.
- **PRECONDICIONES:** A activa; no hay referencia TM nueva.
- **FÓRMULA:** Actualizar extremo de A; `fin_A = extremo real`.
- **SI_TRUE:** A continúa; no se cierra en el primer extremo.
- **SI_FALSE:** N-014.
- **ESTADO_DESTINO:** `A_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No cerrar A en el primer máximo si la vela siguiente lo extiende.
- **DATOS_A_GUARDAR:** extremo actualizado, velas, timestamps.
- **TEST_POSITIVO:** T-012
- **TEST_NEGATIVO:** T-012
- **TEST_FRONTERA:** T-012
- **ESTADO_APROBACIÓN:** `CERRADO` para extensión (H4/H15); `PROVISIONAL` para tick exacto de fin (P3).

### N-014 — B candidata

- **ID:** N-014
- **ESTADO_ORIGEN:** `A_GRANDE` finalizada.
- **EVENTO:** Movimiento contrario a A.
- **PRECONDICIONES:** A Grande delimitada; B no alcanza el 100 % de A.
- **FÓRMULA:** `B_pct = desplazamiento_B / rango_A × 100`; si `< 100` → candidata.
- **SI_TRUE:** `B_CANDIDATA/ACTIVA`.
- **SI_FALSE:** N-015.
- **ESTADO_DESTINO:** `B_CANDIDATA/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No llamar B Grande antes del 100 %; no crear C.
- **DATOS_A_GUARDAR:** inicio B, porcentaje, rango A, timestamps.
- **TEST_POSITIVO:** T-013
- **TEST_NEGATIVO:** T-014
- **TEST_FRONTERA:** T-013
- **ESTADO_APROBACIÓN:** `CERRADO` (H12); tick exacto `PROVISIONAL` (P3).

### N-015 — B Grande 100–127 % + 0,25

- **ID:** N-015
- **ESTADO_ORIGEN:** `B_CANDIDATA`.
- **EVENTO:** B alcanza el 100 % sin superar `127 % + 0,25`.
- **PRECONDICIONES:** `100 % ≤ recorrido ≤ 127 % + 0,25`.
- **FÓRMULA:** `rango_A × 1,00 ≤ recorrido_B ≤ rango_A × 1,27 + 0,25`.
- **SI_TRUE:** `B_GRANDE/CONFIRMADA`.
- **SI_FALSE:** N-017.
- **ESTADO_DESTINO:** `B_GRANDE/CONFIRMADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No llamar AUT en el 100 %; no borrar B.
- **DATOS_A_GUARDAR:** porcentaje, nivel 100 %, nivel 127 % + 0,25, timestamps.
- **TEST_POSITIVO:** T-014
- **TEST_NEGATIVO:** T-015
- **TEST_FRONTERA:** T-015
- **ESTADO_APROBACIÓN:** `CERRADO` (H13a).

### N-016 — B toca 127 % + 0,25 y vuelve

- **ID:** N-016
- **ESTADO_ORIGEN:** `B_GRANDE`.
- **EVENTO:** Toque exacto del nivel `127 % + 0,25` y reversión.
- **PRECONDICIONES:** Toque sin superar; B confirmada.
- **FÓRMULA:** `recorrido = 1,27 × rango_A + 0,25`.
- **SI_TRUE:** No hay AUT; B Grande continúa; el movimiento contrario será C Grande (N-022).
- **SI_FALSE:** N-017.
- **ESTADO_DESTINO:** `B_GRANDE/CONFIRMADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No llamar AUT por tocar; no llamar CUT.
- **DATOS_A_GUARDAR:** nivel tocado, tick, reversión, timestamps.
- **TEST_POSITIVO:** T-015
- **TEST_NEGATIVO:** T-016
- **TEST_FRONTERA:** T-015
- **ESTADO_APROBACIÓN:** `CERRADO` (H9).

### N-017 — B supera 127 % + 0,25: AUT

- **ID:** N-017
- **ESTADO_ORIGEN:** `B_GRANDE`.
- **EVENTO:** B supera `127 % + 0,25`.
- **PRECONDICIONES:** B confirmada; superación estricta.
- **FÓRMULA:** `recorrido > 1,27 × rango_A + 0,25`.
- **SI_TRUE:** AUT inmediato; B deja de ser la clasificación vigente; nuevo 1 candidato.
- **SI_FALSE:** N-015/N-016.
- **ESTADO_DESTINO:** `AUT/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER` (posible L2 local).
- **PROHIBICIONES:** No `B_EXCESIVA`; B y AUT no coexisten; no confirmar TT.
- **DATOS_A_GUARDAR:** tick de superación, nivel, B previa, timestamps.
- **TEST_POSITIVO:** T-016
- **TEST_NEGATIVO:** T-015
- **TEST_FRONTERA:** T-016
- **ESTADO_APROBACIÓN:** `CERRADO` para AUT (B1/H13c); apertura L2 `PENDIENTE_JAVIER`.

### N-018 — AUT: TT pendiente

- **ID:** N-018
- **ESTADO_ORIGEN:** `AUT`.
- **EVENTO:** AUT confirmado con módulo disponible.
- **PRECONDICIONES:** Módulo calculado; TT no confirmado.
- **FÓRMULA:** `TT_alcista = fin_A + rango_modulo`; `TT_bajista = fin_A − rango_modulo`.
- **SI_TRUE:** `TT_PENDIENTE`.
- **SI_FALSE:** Sin módulo → `PENDIENTE_JAVIER`.
- **ESTADO_DESTINO:** `TT_PENDIENTE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No confirmar TT; no FT; no mezclar módulo de otra lectura.
- **DATOS_A_GUARDAR:** módulo, fin A, objetivo TT, tick AUT, timestamps.
- **TEST_POSITIVO:** T-017
- **TEST_NEGATIVO:** T-017
- **TEST_FRONTERA:** T-017
- **ESTADO_APROBACIÓN:** `CERRADO` con módulo (B2/B3/A3); sin módulo `PENDIENTE_JAVIER`.

### N-019 — TT confirmado

- **ID:** N-019
- **ESTADO_ORIGEN:** `TT_PENDIENTE`.
- **EVENTO:** El precio alcanza el objetivo TT.
- **PRECONDICIONES:** AUT activo; objetivo calculado; tick válido.
- **FÓRMULA:** alcista `precio ≥ TT_alcista`; bajista `precio ≤ TT_bajista`; mismo tick permitido.
- **SI_TRUE:** `TT_CONFIRMADO`; nace `NUEVO_1`.
- **SI_FALSE:** N-020.
- **ESTADO_DESTINO:** `TT_CONFIRMADO/ACTIVA` + `NUEVO_1`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No TT antes del 100 %; no FT antes de TT; no usar otro retroceso de A.
- **DATOS_A_GUARDAR:** tick, precio, objetivo, módulo, fin A, overshoot.
- **TEST_POSITIVO:** T-018 / T-019
- **TEST_NEGATIVO:** T-020
- **TEST_FRONTERA:** T-018
- **ESTADO_APROBACIÓN:** `CERRADO` (A3/B3/v3 §7.1).

### N-020 — TT fallido

- **ID:** N-020
- **ESTADO_ORIGEN:** `TT_PENDIENTE`.
- **EVENTO:** No alcanza el 100 % y el precio toca el final de A.
- **PRECONDICIONES:** TT pendiente; final de A definido.
- **FÓRMULA:** `precio = fin_A` sin haber alcanzado TT.
- **SI_TRUE:** TT cancelado; todo el recorrido anterior pasa a módulo; el retorno es A Grande.
- **SI_FALSE:** N-019.
- **ESTADO_DESTINO:** `TT_FALLIDO` → `MODULO/ACTIVA` + `A_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No llamar C al retorno; no llamar CUT; no borrar historial.
- **DATOS_A_GUARDAR:** tick de toque, final A, módulo nuevo, timestamps.
- **TEST_POSITIVO:** T-020
- **TEST_NEGATIVO:** T-018
- **TEST_FRONTERA:** T-020
- **ESTADO_APROBACIÓN:** `CERRADO` (v3 §7.3C / §10B).

### N-021 — Nuevo 1 después de TT

- **ID:** N-021
- **ESTADO_ORIGEN:** `TT_CONFIRMADO`.
- **EVENTO:** El movimiento que completa el objetivo TT.
- **PRECONDICIONES:** TT confirmado al 100 %.
- **FÓRMULA:** `nuevo_1` = recorrido desde fin de A hasta el extremo que alcanza/supera TT; rango real del recorrido.
- **SI_TRUE:** `NUEVO_1/CONFIRMADA`.
- **SI_FALSE:** No aplica.
- **ESTADO_DESTINO:** `NUEVO_1/CONFIRMADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No llamar 1 antes de TT; no mezclar su rango con el módulo anterior.
- **DATOS_A_GUARDAR:** inicio, extremo, rango real, tick TT, módulo de origen.
- **TEST_POSITIVO:** T-021
- **TEST_NEGATIVO:** T-018
- **TEST_FRONTERA:** T-021
- **ESTADO_APROBACIÓN:** `CERRADO` (v3 §7.4 / DEC-012).

### N-022 — C Grande

- **ID:** N-022
- **ESTADO_ORIGEN:** `B_GRANDE`.
- **EVENTO:** Movimiento contrario a B.
- **PRECONDICIONES:** B Grande confirmada en la misma lectura.
- **FÓRMULA:** dirección de C = dirección de A; C no es candidata tras B confirmada.
- **SI_TRUE:** `C_GRANDE/ACTIVA`.
- **SI_FALSE:** B continúa.
- **ESTADO_DESTINO:** `C_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No C antes de B; no CUT sin C; no llamar C a un micromovimiento.
- **DATOS_A_GUARDAR:** inicio C, dirección, B previa, timestamps.
- **TEST_POSITIVO:** T-022
- **TEST_NEGATIVO:** T-035
- **TEST_FRONTERA:** T-022
- **ESTADO_APROBACIÓN:** `CERRADO` (H13b / v3 §5.3).

### N-023 — B crea nuevo extremo: C cancelada

- **ID:** N-023
- **ESTADO_ORIGEN:** `C_GRANDE` / `B_GRANDE`.
- **EVENTO:** B Grande crea un nuevo extremo.
- **PRECONDICIONES:** C activa pero no CUT.
- **FÓRMULA:** nuevo extremo de B en su dirección.
- **SI_TRUE:** C Grande se cancela; B Grande continúa.
- **SI_FALSE:** N-024.
- **ESTADO_DESTINO:** `B_GRANDE/CONFIRMADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No confirmar CUT; no borrar C del historial.
- **DATOS_A_GUARDAR:** nuevo extremo, tick, C cancelada.
- **TEST_POSITIVO:** T-023
- **TEST_NEGATIVO:** T-024
- **TEST_FRONTERA:** T-023
- **ESTADO_APROBACIÓN:** `CERRADO` (H13d).

### N-024 — CUT

- **ID:** N-024
- **ESTADO_ORIGEN:** `C_GRANDE`.
- **EVENTO:** C Grande supera el final de A Grande.
- **PRECONDICIONES:** B Grande confirmada; C Grande válida; final de A definido.
- **FÓRMULA:** alcista/bajista según dirección; `C` supera `fin_A`.
- **SI_TRUE:** `CUT/CONFIRMADA`.
- **SI_FALSE:** N-025.
- **ESTADO_DESTINO:** `CUT/CONFIRMADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No CUT por base cualquiera; no CUT por color; no CUT sin C.
- **DATOS_A_GUARDAR:** fin A, extremo C, tick de superación, timestamps.
- **TEST_POSITIVO:** T-024
- **TEST_NEGATIVO:** T-025
- **TEST_FRONTERA:** T-024
- **ESTADO_APROBACIÓN:** `CERRADO` (v3 §6.2 / B4).

### N-025 — C = nuevo 1

- **ID:** N-025
- **ESTADO_ORIGEN:** `C_GRANDE` sin CUT.
- **EVENTO:** C cierra la referencia y pasa a nuevo 1 del ciclo siguiente.
- **PRECONDICIONES:** C Grande válida; no alcanza CUT; condición exacta `PENDIENTE_JAVIER`.
- **FÓRMULA:** `PENDIENTE_JAVIER`.
- **SI_TRUE:** `NUEVO_1`.
- **SI_FALSE:** C permanece en su rama.
- **ESTADO_DESTINO:** `NUEVO_1` (si Javier lo confirma)
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No declarar `C = nuevo 1` sin condición matemática cerrada.
- **DATOS_A_GUARDAR:** C, referencia cerrada, tick, lectura de origen.
- **TEST_POSITIVO:** T-026
- **TEST_NEGATIVO:** T-026
- **TEST_FRONTERA:** T-026
- **ESTADO_APROBACIÓN:** `PENDIENTE_JAVIER` (H1 / PR-e / DUDA-J04).

### N-026 — FT

- **ID:** N-026
- **ESTADO_ORIGEN:** `TT_CONFIRMADO`.
- **EVENTO:** Pérdida de velocidad y movimiento contrario claro.
- **PRECONDICIONES:** TT confirmado; referencia exacta y desplazamiento mínimo `PENDIENTE_JAVIER`.
- **FÓRMULA:** `PENDIENTE_JAVIER`.
- **SI_TRUE:** `FT`.
- **SI_FALSE:** No FT.
- **ESTADO_DESTINO:** `FT`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No FT sin TT; no FT por micromovimiento; no mezclar FT con lectura modular.
- **DATOS_A_GUARDAR:** TT previo, velocidad, movimiento contrario, tick.
- **TEST_POSITIVO:** T-028
- **TEST_NEGATIVO:** T-027
- **TEST_FRONTERA:** T-028
- **ESTADO_APROBACIÓN:** `PENDIENTE_JAVIER` (P6 / DUDA-J05).

### N-027 — Reclasificación live

- **ID:** N-027
- **ESTADO_ORIGEN:** Cualquier lectura activa.
- **EVENTO:** Corrección posterior que cambia la función de velas anteriores.
- **PRECONDICIONES:** Evidencia de corrección; criterios exactos `PENDIENTE_JAVIER`.
- **FÓRMULA:** `PENDIENTE_JAVIER`.
- **SI_TRUE:** `RECLASIFICADA` o `INTEGRADA`; se conserva el historial.
- **SI_FALSE:** La lectura continúa.
- **ESTADO_DESTINO:** `RECLASIFICADA/ACTIVA` o `INTEGRADA/FINALIZADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No borrar; no mezclar niveles; no reescribir el pasado.
- **DATOS_A_GUARDAR:** evento anterior, evento nuevo, motivo, tick, lectura.
- **TEST_POSITIVO:** T-034
- **TEST_NEGATIVO:** T-034
- **TEST_FRONTERA:** T-034
- **ESTADO_APROBACIÓN:** `PROVISIONAL` (P4).

### N-028 — Abrir L2

- **ID:** N-028
- **ESTADO_ORIGEN:** L1 activa.
- **EVENTO:** Candidato a segunda lectura coherente.
- **PRECONDICIONES:** Regla TM expresa; lectura matemáticamente válida; no ruido.
- **FÓRMULA:** No hay fórmula; la apertura es normativa.
- **SI_TRUE:** L2/`lectura 2` activa.
- **SI_FALSE:** El movimiento pertenece a L1 o se descarta.
- **ESTADO_DESTINO:** `LECTURA_2/ACTIVA`
- **LECTURA_AFECTADA:** L2
- **¿ABRE_NUEVA_LECTURA?:** SÍ, solo con regla expresa.
- **PROHIBICIONES:** No abrir por ver A/B/AUT dentro de una vela; no abrir por ruido; no mezclar con L1.
- **DATOS_A_GUARDAR:** regla que autoriza, referencia, módulo, niveles, tick.
- **TEST_POSITIVO:** T-029
- **TEST_NEGATIVO:** T-030
- **TEST_FRONTERA:** T-029
- **ESTADO_APROBACIÓN:** `PENDIENTE_JAVIER` (DUDA-J01).

### N-029 — Abrir L3

- **ID:** N-029
- **ESTADO_ORIGEN:** L1 y L2 activas.
- **EVENTO:** Candidato a tercera lectura coherente.
- **PRECONDICIONES:** Regla TM expresa; L1/L2 válidas; máximo 3.
- **FÓRMULA:** No hay fórmula; la apertura es normativa.
- **SI_TRUE:** L3/`lectura 3` activa.
- **SI_FALSE:** No se abre; nunca L4.
- **ESTADO_DESTINO:** `LECTURA_3/ACTIVA`
- **LECTURA_AFECTADA:** L3
- **¿ABRE_NUEVA_LECTURA?:** SÍ, solo con regla expresa.
- **PROHIBICIONES:** No L4; no abrir por ruido; no mezclar.
- **DATOS_A_GUARDAR:** regla que autoriza, referencia, niveles, tick.
- **TEST_POSITIVO:** T-039
- **TEST_NEGATIVO:** T-040
- **TEST_FRONTERA:** T-039
- **ESTADO_APROBACIÓN:** `PENDIENTE_JAVIER` (DUDA-J01).

### N-030 — Prioridad en el mismo tick

- **ID:** N-030
- **ESTADO_ORIGEN:** L1/L2/L3 activas.
- **EVENTO:** Dos o tres lecturas alcanzan nivel en el mismo tick.
- **PRECONDICIONES:** Niveles calculados; tick común.
- **FÓRMULA:** `PENDIENTE_JAVIER`.
- **SI_TRUE:** Aplicar la prioridad que fije Javier.
- **SI_FALSE:** Cada lectura se resuelve por separado.
- **ESTADO_DESTINO:** `PENDIENTE_JAVIER`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No resolver por orden de aparición, color, conveniencia ni resultado posterior.
- **DATOS_A_GUARDAR:** tick, niveles alcanzados, lecturas implicadas.
- **TEST_POSITIVO:** T-029
- **TEST_NEGATIVO:** T-029
- **TEST_FRONTERA:** T-029
- **ESTADO_APROBACIÓN:** `PENDIENTE_JAVIER` (P5 / DUDA-J03).

### N-031 — Cierre y archivo de lectura

- **ID:** N-031
- **ESTADO_ORIGEN:** Lectura activa.
- **EVENTO:** TT confirmado, CUT confirmado, invalidación, reclasificación o pérdida de coherencia.
- **PRECONDICIONES:** Resolución matemática documentada.
- **FÓRMULA:** Según evento.
- **SI_TRUE:** `FINALIZADA`, `INVALIDADA`, `RECLASIFICADA` o `INTEGRADA`.
- **SI_FALSE:** Continúa activa.
- **ESTADO_DESTINO:** `FINALIZADA/INVALIDADA/RECLASIFICADA/INTEGRADA`
- **LECTURA_AFECTADA:** La lectura resuelta.
- **¿ABRE_NUEVA_LECTURA?:** NO por sí solo.
- **PROHIBICIONES:** No borrar eventos; no reutilizar el slot sin conservar historial.
- **DATOS_A_GUARDAR:** causa, tick, estado final, historial.
- **TEST_POSITIVO:** T-034
- **TEST_NEGATIVO:** T-034
- **TEST_FRONTERA:** T-034
- **ESTADO_APROBACIÓN:** `CERRADO` para cierre; `PROVISIONAL` para reclasificación.

### N-032 — Ruido y micromovimiento

- **ID:** N-032
- **ESTADO_ORIGEN:** Cualquier lectura.
- **EVENTO:** Oscilación que no alcanza una referencia TM.
- **PRECONDICIONES:** No alcanza referencia; umbral numérico `PENDIENTE_JAVIER`.
- **FÓRMULA:** No se calcula; se descarta.
- **SI_TRUE:** No ocupa lectura; no se clasifica.
- **SI_FALSE:** N-001 u otra rama válida.
- **ESTADO_DESTINO:** `SIN_LECTURA` (descartado)
- **LECTURA_AFECTADA:** Ninguna.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No convertir en A/B/C/AUT/TT; no abrir lectura; no contar como nuevo 1.
- **DATOS_A_GUARDAR:** motivo de descarte, tick, referencia no alcanzada.
- **TEST_POSITIVO:** T-031
- **TEST_NEGATIVO:** T-031
- **TEST_FRONTERA:** T-031
- **ESTADO_APROBACIÓN:** `CERRADO` metodológico (H16 / DEC-015); umbral `PENDIENTE_JAVIER` (PR-g).

### N-033 — AUT y TT en el mismo tick

- **ID:** N-033
- **ESTADO_ORIGEN:** `B_GRANDE` / `AUT`.
- **EVENTO:** Un salto cruza AUT y TT en el mismo tick.
- **PRECONDICIONES:** Módulo; objetivo TT; tick único.
- **FÓRMULA:** `precio` supera AUT y alcanza TT en el mismo tick.
- **SI_TRUE:** AUT y TT confirmados en el mismo tick; nace nuevo 1.
- **SI_FALSE:** N-018 / N-019.
- **ESTADO_DESTINO:** `TT_CONFIRMADO/ACTIVA` + `NUEVO_1`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No saltar AUT; no confirmar TT antes del 100 %.
- **DATOS_A_GUARDAR:** tick, AUT, TT, overshoot.
- **TEST_POSITIVO:** T-033
- **TEST_NEGATIVO:** T-018
- **TEST_FRONTERA:** T-033
- **ESTADO_APROBACIÓN:** `CERRADO` (B3).

### N-034 — C Grande: tres funciones

- **ID:** N-034
- **ESTADO_ORIGEN:** `C_GRANDE`.
- **EVENTO:** Evaluar C tras B.
- **PRECONDICIONES:** B confirmada; C válida.
- **FÓRMULA:** Orden: (1) CUT; (2) C = nuevo 1; (3) C = A Grande de lectura mayor.
- **SI_TRUE:** Primera función aplicable.
- **SI_FALSE:** `PENDIENTE_JAVIER`.
- **ESTADO_DESTINO:** `CUT` / `NUEVO_1` / `A_GRANDE` (lectura mayor)
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** La tercera función puede abrir lectura mayor: `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No crear movimientos adicionales; no CUT sin C.
- **DATOS_A_GUARDAR:** C, final A, funciones comprobadas, tick.
- **TEST_POSITIVO:** T-024 / T-026
- **TEST_NEGATIVO:** T-025
- **TEST_FRONTERA:** T-034
- **ESTADO_APROBACIÓN:** `PROVISIONAL` (H3 cerrada en orden; C=new1 y lectura mayor pendientes).

### N-035 — Invalidación de lectura

- **ID:** N-035
- **ESTADO_ORIGEN:** Lectura activa.
- **EVENTO:** Toque del nivel de invalidación antes de TT o pérdida de coherencia.
- **PRECONDICIONES:** Nivel definido.
- **FÓRMULA:** `precio` alcanza el final de A o el nivel de invalidación.
- **SI_TRUE:** `INVALIDADA` o `RECLASIFICADA`.
- **SI_FALSE:** Continúa.
- **ESTADO_DESTINO:** `INVALIDADA` / `RECLASIFICADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No borrar; no mezclar.
- **DATOS_A_GUARDAR:** nivel, tick, causa.
- **TEST_POSITIVO:** T-020
- **TEST_NEGATIVO:** T-018
- **TEST_FRONTERA:** T-020
- **ESTADO_APROBACIÓN:** `CERRADO` para TT fallido; `PROVISIONAL` para otras invalidaciones.

### N-036 — 2 confirmado no se borra

- **ID:** N-036
- **ESTADO_ORIGEN:** `2_CONFIRMADA`.
- **EVENTO:** Aparece movimiento contrario después de 2.
- **PRECONDICIONES:** 2 confirmado.
- **FÓRMULA:** 2 se conserva; 1+2 = módulo; contrario = A Grande.
- **SI_TRUE:** `MODULO` + `A_GRANDE`.
- **SI_FALSE:** No aplica.
- **ESTADO_DESTINO:** `MODULO/ACTIVA` + `A_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No borrar 2; no llamar 3.
- **DATOS_A_GUARDAR:** 2 confirmado, módulo, A, tick.
- **TEST_POSITIVO:** T-006
- **TEST_NEGATIVO:** T-006
- **TEST_FRONTERA:** T-006
- **ESTADO_APROBACIÓN:** `CERRADO` (regla 4/5 del prompt).

### N-037 — B y AUT no coexisten

- **ID:** N-037
- **ESTADO_ORIGEN:** `B_GRANDE`.
- **EVENTO:** Superación de `127 % + 0,25`.
- **PRECONDICIONES:** B confirmada.
- **FÓRMULA:** N-017.
- **SI_TRUE:** B deja de ser B; AUT.
- **SI_FALSE:** B continúa.
- **ESTADO_DESTINO:** `AUT`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No `B_EXCESIVA`; no coexistencia.
- **DATOS_A_GUARDAR:** B previa, AUT, tick.
- **TEST_POSITIVO:** T-016
- **TEST_NEGATIVO:** T-015
- **TEST_FRONTERA:** T-016
- **ESTADO_APROBACIÓN:** `CERRADO` (B5).

### N-038 — A Grande multi-vela

- **ID:** N-038
- **ESTADO_ORIGEN:** `A_GRANDE`.
- **EVENTO:** A continúa en la vela siguiente.
- **PRECONDICIONES:** Sin referencia TM nueva.
- **FÓRMULA:** Actualizar extremo; no cerrar en el primer máximo.
- **SI_TRUE:** A continúa.
- **SI_FALSE:** N-014.
- **ESTADO_DESTINO:** `A_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No cerrar A por cambio de vela.
- **DATOS_A_GUARDAR:** extremos, velas, timestamps.
- **TEST_POSITIVO:** T-012
- **TEST_NEGATIVO:** T-012
- **TEST_FRONTERA:** T-012
- **ESTADO_APROBACIÓN:** `CERRADO` (H4/H15).

### N-039 — TT: alcanzar el 100 %

- **ID:** N-039
- **ESTADO_ORIGEN:** `TT_PENDIENTE`.
- **EVENTO:** El precio alcanza exactamente el objetivo o lo supera.
- **PRECONDICIONES:** Objetivo calculado.
- **FÓRMULA:** alcista `precio ≥ objetivo`; bajista `precio ≤ objetivo`.
- **SI_TRUE:** TT confirmado.
- **SI_FALSE:** TT pendiente.
- **ESTADO_DESTINO:** `TT_CONFIRMADO`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No exigir superación estricta salvo decisión expresa; no confundir con AUT.
- **DATOS_A_GUARDAR:** precio, objetivo, tick, exacto/overshoot.
- **TEST_POSITIVO:** T-018
- **TEST_NEGATIVO:** T-020
- **TEST_FRONTERA:** T-018
- **ESTADO_APROBACIÓN:** `CERRADO` por «alcanzar el 100 %»; igualdad exacta sujeta a confirmación si Javier la distingue.

### N-040 — Medida direccional de 1 y 2

- **ID:** N-040
- **ESTADO_ORIGEN:** `1_ACTIVA` / `2_CANDIDATA`.
- **EVENTO:** Medir 1 y 2.
- **PRECONDICIONES:** Movimientos delimitados.
- **FÓRMULA:** Desplazamiento direccional, no `High−Low` completo.
- **SI_TRUE:** Aplicar N-006/N-007.
- **SI_FALSE:** No medir.
- **ESTADO_DESTINO:** `2_CANDIDATA` / `2_CONFIRMADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No usar `High−Low` para confirmar 2.
- **DATOS_A_GUARDAR:** desplazamiento, rango, tick.
- **TEST_POSITIVO:** T-001
- **TEST_NEGATIVO:** T-005
- **TEST_FRONTERA:** T-001
- **ESTADO_APROBACIÓN:** `CERRADO` (A1).

---

## 5. ARQUITECTURA D — PRECONDICIONES Y PROHIBICIONES GLOBALES

### 5.1. Precondiciones

1. Ticks en orden temporal y serie de precio declarada.
2. Movimiento delimitado antes de medir.
3. 1 antes de 2; 2 antes de 3.
4. Módulo antes de A.
5. A antes de B.
6. B confirmada antes de C.
7. AUT antes de TT.
8. TT antes de FT.
9. C Grande antes de CUT.
10. Final de A definido antes de CUT.
11. Lectura identificada antes de asignar función.
12. Si falta una precondición: `PENDIENTE_JAVIER`, no etiqueta.

### 5.2. Prohibiciones

- No usar color de vela.
- No usar OHLC aislado si hay ticks.
- No usar datos futuros.
- No usar golden como regla.
- No llamar B Grande antes del 100 %.
- No llamar C antes de B confirmada.
- No llamar CUT sin C Grande.
- No llamar TT antes del 100 %.
- No llamar FT sin TT.
- No llamar nuevo 1 antes de TT.
- No llamar C al retorno del TT fallido.
- No borrar una lectura al reclasificar.
- No abrir L2/L3 sin regla expresa.
- No calcular ruido ni micromovimientos.
- No mezclar niveles entre lecturas.
- No inventar módulo, autocorte ni nivel.

---

## 6. ARQUITECTURA E — FÓRMULAS Y FRONTERAS EXACTAS

### 6.1. Medidas

- `rango_1 = max(1) − min(1)` según la medida direccional aplicable.
- `rango_2` = desplazamiento direccional del movimiento 2, no `High−Low` completo.
- `rango_modulo = max(highs del módulo) − min(lows del módulo)`.
- `A = rango_A` = desplazamiento direccional del movimiento contrario al módulo.
- `B_pct = desplazamiento_B / rango_A × 100`.
- `TT_alcista = fin_A + rango_modulo`.
- `TT_bajista = fin_A − rango_modulo`.
- `AUT = fin_A ± (1,27 × rango_A + 0,25)`.
- `CUT`: C supera `fin_A`.
- `plano`: `|apertura_nueva − cierre_vela_anterior| ≤ 0,25`.
- `gap`: `|apertura_nueva − cierre_vela_anterior| > 0,25`.
- `cola`: alcista `Low(2) = Open(2)`; bajista `High(2) = Open(2)`; tolerancia 0,25.

### 6.2. Fronteras

| Frontera | Regla | Estado |
|---|---|---|
| Plano/gap | `≤ 0,25` plano; `> 0,25` gap | CERRADO (H14) |
| Cola de 2 | `≤ 0,25` permite 2; `> 0,25` no 2 | CERRADO (A1) |
| B 100 % | `< 100 %` candidata; `≥ 100 %` B Grande | CERRADO (H12) |
| B 127 % + 0,25 | `≤` B Grande; `>` AUT | CERRADO (H9/H13) |
| TT 100 % | `≥` objetivo alcista; `≤` objetivo bajista | CERRADO por «alcanzar»; igualdad exacta a confirmar si Javier la distingue |
| CUT | C supera `fin_A` | CERRADO |
| Límite lecturas | 2 normal; 3 máximo; 4 prohibido | CERRADO (H16) |
| Ruido | no se calcula; umbral numérico pendiente | `PENDIENTE_JAVIER` (PR-g) |

### 6.3. Unidades

- En la muestra, `1 tick = 0,25 puntos` (DEC-002).
- El margen `0,25` es fijo y no se deriva del CSV.
- La serie de precio de la muestra es **Bid**; la ratificación experta sigue pendiente (P2).

---

## 7. ARQUITECTURA F — HISTORIAL SIN BORRADO

- **CSV de eventos:** conserva lo que se sabía en cada tick.
- **CSV de estados:** fotografía de la clasificación vigente.
- **Reclasificar no es borrar:** el evento anterior permanece.
- Estados de ciclo de vida: `CANDIDATA`, `ACTIVA`, `CONFIRMADA`, `PENDIENTE`, `RECLASIFICADA`, `INTEGRADA`, `INVALIDADA`, `FINALIZADA`.
- Cada transición guarda: tick, lectura, estado anterior, evento, estado nuevo, niveles, motivo y fuente.
- Una lectura invalidada no se elimina: se marca y se conserva para auditoría.
- Una lectura integrada conserva su historial y se referencia desde la lectura mayor.
- No se reescribe el pasado con datos posteriores.

---

## 8. ARQUITECTURA G — CASOS VALIDADOS

### 8.1. Caso obligatorio: velas 1–3 (23:39–23:41)

**L1 — lectura principal:**

- Vela 1, 23:39: `1` alcista; rango `29182,80 − 29173,00 = 9,80`.
- Vela 2, 23:40: `A`, `B`, `AUT`; final de A `29179,20`; TT posible `29179,20 + 9,80 = 29189,00`.
- Vela 3, 23:41: alcanza `29189,30`; TT confirmado; vela 3 = `nuevo 1`.
- Estado: `CERRADO` para L1.

**L2 — lectura candidata observada, NO abierta por regla expresa:**

- En la vela 3 se observa un segundo recorrido coherente: módulo de vela 2 con rango `5,40`; A hasta `29182,00`; TT pequeño `29187,40`; nuevo 1 hasta `29189,30` (rango `7,30`).
- No se declara L2 porque falta la regla expresa de apertura (DUDA-J01).
- Si Javier confirma la apertura, L2 se documentará con sus propios niveles y no se mezclará con L1.
- Estado: `PENDIENTE_JAVIER`.

**Prohibición expresa:** no afirmar que la vela 3 contiene A, B y AUT propios de L1. La vela 3 es el `nuevo 1` de L1. Cualquier segunda lectura debe demostrarse por regla expresa.

### 8.2. Caso de TT fallido (contrafáctico validado en la auditoría)

- TT no alcanza el 100 % y el precio toca el final de A.
- Resultado: TT cancelado; recorrido anterior = módulo; retorno = A Grande del nuevo módulo.
- No se llama C al retorno; no se confirma CUT.
- Estado: `CERRADO` (v3 §7.3C / §10B).

---

## 9. ARQUITECTURA H — TESTS

El catálogo completo está en `control/TM_TESTS_REQUERIDOS_v1.md`.

Resumen:

- Tests positivos: 15.
- Tests negativos: 12.
- Tests de frontera: 8.
- Tests de cronología: 5.
- Tests de concurrencia: 5.
- Total: 45 tests planificados, ninguno implementado en esta fase.

Cada nodo referencia sus tests en `TEST_POSITIVO`, `TEST_NEGATIVO` y `TEST_FRONTERA`.

---

## 10. ARQUITECTURA I — REGISTRO DE DUDAS

El registro completo está en `control/TM_DUDAS_PENDIENTES_JAVIER.md`.

### 10.1. Cinco dudas bloqueantes

1. `DUDA-J01` — ¿Qué regla expresa abre L2/L3?
2. `DUDA-J02` — ¿La composición general del módulo es siempre 1+2 o admite una vela / vela anterior por descarte?
3. `DUDA-J03` — ¿Qué prioridad rige cuando dos o tres lecturas alcanzan nivel en el mismo tick?
4. `DUDA-J04` — ¿Cuál es la condición exacta de `C = nuevo 1` cuando C no alcanza CUT?
5. `DUDA-J05` — ¿Cuál es la regla matemática completa de FT?

### 10.2. Dudas secundarias

- `DUDA-S01` — Umbral numérico entre ruido y movimiento TM.
- `DUDA-S02` — ¿Un gap a favor de 1 confirma AUT o solo deja TT pendiente?
- `DUDA-S03` — Tick exacto de confirmación de A/B/C Grande.
- `DUDA-S04` — Serie de precio definitiva (Bid/Ask/Last/medio).
- `DUDA-S05` — Igualdad exacta en TT: ¿alcanzar o superar?

---

## 11. TRAZABILIDAD Y ESTADO DE APROBACIÓN

| Bloque | Estado | Fuente principal |
|---|---|---|
| 1, 2, 3 y módulo regular | CERRADO | A1/A2/v3 §4 |
| Gap y salida en plano | CERRADO | A4/H11/H14 |
| A Grande y B Grande | CERRADO | H4/H12/H13/H15 |
| AUT | CERRADO | B1/B2/B3/H8/H9 |
| TT y nuevo 1 | CERRADO | A3/B3/v3 §7 |
| C Grande y CUT | CERRADO | H13b/B4/v3 §6.2 |
| C = nuevo 1 | PENDIENTE_JAVIER | H1/PR-e |
| FT | PENDIENTE_JAVIER | P6 |
| Reclasificación | PROVISIONAL | P4 |
| Concurrencia L1-L3 | PARCIAL | H16/P5 |
| Ruido | PARCIAL | H16/PR-g |
| Módulo general | PENDIENTE_JAVIER | DUDA-009 |

### 11.1. Confirmación de alcance

- Este documento es un **árbol de decisión y máquina de estados**, no una implementación.
- No se ha modificado código, golden ni tests.
- No se ha creado una regla nueva sin fuente o decisión expresa.
- Las ramas sin regla quedan `PENDIENTE_JAVIER`.

---

## 12. ÍNDICE

1. Control de fuentes y alcance.
2. Mapa de reglas confirmadas y pendientes.
3. Arquitectura A — controlador de concurrencia L1-L3.
4. Arquitectura B — máquina de estados por lectura.
5. Arquitectura C — árbol completo de transiciones (N-001 a N-040).
6. Arquitectura D — precondiciones y prohibiciones globales.
7. Arquitectura E — fórmulas y fronteras exactas.
8. Arquitectura F — historial sin borrado.
9. Arquitectura G — casos validados.
10. Arquitectura H — tests.
11. Arquitectura I — registro de dudas.
12. Trazabilidad y estado de aprobación.


---

# ANEXO 2 - FUENTE INTEGRA: `TM_ARBOL_MAESTRO_CANONICO_v0_9_SALIDA_MOVIMIENTOS_PATRONES_TT.md`

- **SHA-256:** `f7d7800e0538c3e956f043f518b91cedb693a7afa34c728faa7463d67ced09f0`
- **Integridad:** contenido incorporado sin recortes.

# TM · ÁRBOL MAESTRO CANÓNICO

Versión 0.5 MEGA BORRADOR. Cobertura global para prueba, preguntas y corrección. No apto todavía para ejecución automática ni para operar.

## 0. Regla constitucional

```text
CLASIFICACIÓN VÁLIDA = lectura + estado anterior + cronología + referencia + precondiciones + transición + resultado.
Si falta una pieza, el motor registra HECHO_SIN_REGLA y no inventa una función. En la versión final HECHO_SIN_REGLA deberá ser cero.
```

## 1. Leyenda de certeza

- CONFIRMADO_JAVIER: regla expresamente cerrada por Javier.

- DOCUMENTADO: aparece en fuentes, pendiente de prueba experta.

- PROPUESTA_CONTROLADA: cierre técnico provisional para poder probar el árbol completo.

- PENDIENTE_JAVIER: pregunta concreta, no programable.

- PROHIBIDO: transición incompatible con las precondiciones.

## 2. Ontología completa provisional

```text
FUNCIONES: 1 | 2 | 3 | A | B | AUT | C
PATRONES: TT | FT
ESTRUCTURAS: MÓDULO | LECTURA
EVENTOS: GAP | AUTOCORTE | CUT | OBJETIVO_TT | CONFIRMACIÓN_FT
CALIFICADORES INTERNOS: CANDIDATO | CONFIRMADO | CANCELADO | RECLASIFICADO | INTEGRADO
```

## 3. Datos mínimos por tick

- timestamp

- bid/ask o precio de referencia acordado

- OHLC de vela activa

- Open actual y Close anterior

- dirección y extremo de cada lectura

- niveles 0, 50, 100, 127 y 127+0,25

- objetivo TT

- referencia CUT

- referencia FT

- historial inmutable de eventos

## 4. Orden universal de evaluación

```text
1. Registrar tick.
2. Detectar nueva vela.
3. Si nueva vela, evaluar GAP antes de 2.
4. Actualizar extremos de cada lectura.
5. Detectar niveles cruzados en el tick.
6. Procesar todos los niveles cruzados en orden geométrico.
7. Aplicar transición por lectura, sin mezclar referencias.
8. Abrir lectura adicional solo por regla expresa.
9. Registrar reclasificación sin borrar historial.
10. Emitir etiqueta visible y trazabilidad.
```

## 5. Árbol raíz y nacimiento de lectura

### TM-ROOT-001 · Sin lectura activa

**Estado:** `PROPUESTA_CONTROLADA`

```text
ORIGEN: SIN_LECTURA
EVENTO: primer recorrido observable
PRECONDICIONES: datos suficientes y referencia inicial autorizada
SI SE CUMPLE: abrir L1 con 1 candidato
SI NO SE CUMPLE: seguir acumulando ticks
DESTINO: UNO_CANDIDATO
PROHIBICIONES: no inventar dirección por color de vela
PRUEBAS: inicio alcista; inicio bajista; vela incompleta
PREGUNTA: Q-001: regla matemática definitiva de nacimiento del primer 1
```

### TM-ROOT-002 · Nueva lectura adicional

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: L1/L2 activa
EVENTO: posible recorrido independiente
PRECONDICIONES: regla explícita de apertura
SI SE CUMPLE: abrir primer slot libre
SI NO SE CUMPLE: integrar en lecturas existentes
DESTINO: Ln activa
PROHIBICIONES: abrir por apariencia visual
PRUEBAS: caso abre L2; caso no abre L2
PREGUNTA: Q-002: catálogo completo de reglas que abren L2/L3
```

## 6. Estado 1

### TM-1-001 · 1 continúa

**Estado:** `PROPUESTA_CONTROLADA`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: extensión en dirección de 1
PRECONDICIONES: no nace función posterior
SI SE CUMPLE: actualizar extremo y rango de 1
SI NO SE CUMPLE: mantener extremo
DESTINO: UNO_CONFIRMADO
PROHIBICIONES: crear otro 1 por cada vela
PRUEBAS: extensión misma vela; varias velas
```

### TM-1-002 · Apertura siguiente con gap

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: Open actual != Close anterior
PRECONDICIONES: nueva vela
SI SE CUMPLE: prohibir 2 y saltar a árbol GAP
SI NO SE CUMPLE: n/a
DESTINO: GAP_EVALUADO
PROHIBICIONES: evaluar plano o 2
PRUEBAS: gap 1 tick; gap varios puntos
```

### TM-1-003 · Sin gap y salida en plano

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: Open actual = Close anterior
PRECONDICIONES: nueva vela y sin cola observable >0,25 antes de objetivo
SI SE CUMPLE: abrir DOS_CANDIDATO
SI NO SE CUMPLE: si hay cola, prohibir 2
DESTINO: DOS_CANDIDATO
PROHIBICIONES: confirmar 2 solo por color
PRUEBAS: plano exacto; cola 0,25; cola 0,50
```

### TM-1-004 · No 2 por cola

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: cola de base >0,25 antes de confirmar 2
PRECONDICIONES: sin gap
SI SE CUMPLE: cancelar 2 y evaluar ruta A
SI NO SE CUMPLE: si cola <=0,25 mantener candidato
DESTINO: A_CANDIDATA
PROHIBICIONES: recrear 2 después
PRUEBAS: cola antes/después del objetivo
```

### TM-1-005 · No 2 por gap

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: gap cualquiera
PRECONDICIONES: nueva vela
SI SE CUMPLE: 2 prohibido
SI NO SE CUMPLE: n/a
DESTINO: RUTA_GAP
PROHIBICIONES: llamar 2 al recorrido posterior
PRUEBAS: gap a favor; gap contrario
```

## 7. Estado 2

### TM-2-001 · 2 candidato progresa

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: avance en dirección de 1
PRECONDICIONES: sin invalidación previa
SI SE CUMPLE: actualizar recorrido 2
SI NO SE CUMPLE: mantener
DESTINO: DOS_CANDIDATO
PROHIBICIONES: confirmar antes de medida
PRUEBAS: <100; =100; >100
PREGUNTA: Q-003: medida exacta y anclajes de 2
```

### TM-2-002 · 2 confirmado

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: alcanza medida exigida
PRECONDICIONES: plano, sin gap, sin cola invalidante previa
SI SE CUMPLE: confirmar 2
SI NO SE CUMPLE: seguir candidato
DESTINO: DOS_CONFIRMADO
PROHIBICIONES: borrar 2 por hechos posteriores
PRUEBAS: frontera exacta y salto
```

### TM-2-003 · Retroceso después de confirmar 2

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: DOS_CONFIRMADO
EVENTO: movimiento contrario
PRECONDICIONES: 2 ya confirmado
SI SE CUMPLE: conservar 2 y abrir evaluación de 3
SI NO SE CUMPLE: n/a
DESTINO: TRES_CANDIDATO
PROHIBICIONES: borrar 2
PRUEBAS: retroceso pequeño; grande
```

### TM-2-004 · Cambio de vela con 2 candidato

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: cierra vela sin confirmar
PRECONDICIONES: no hubo invalidación
SI SE CUMPLE: conservar/cancelar según decisión
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir cancelación
PRUEBAS: varias velas
PREGUNTA: Q-004: 2 puede confirmarse en varias velas
```

## 8. Estado 3 y módulo

### TM-3-001 · Retroceso válido para 3

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CONFIRMADO
EVENTO: retroceso dentro de franja válida
PRECONDICIONES: 2 confirmado
SI SE CUMPLE: seguir TRES_CANDIDATO
SI NO SE CUMPLE: fallar 3
DESTINO: TRES_CANDIDATO
PROHIBICIONES: anticipar 3
PRUEBAS: 0; 50; >50
PREGUNTA: Q-005: límites exactos del retroceso de 3
```

### TM-3-002 · 3 confirmado

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_CANDIDATO
EVENTO: precio retoma dirección de 2 y supera/toca extremo
PRECONDICIONES: retroceso válido
SI SE CUMPLE: confirmar 3
SI NO SE CUMPLE: mantener candidato
DESTINO: TRES_CONFIRMADO
PROHIBICIONES: confirmar por color
PRUEBAS: toca; supera 1 tick
PREGUNTA: Q-006: tocar o superar extremo de 2
```

### TM-3-003 · 3 falla

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_CANDIDATO
EVENTO: incumple regla de 3
PRECONDICIONES: 1 y 2 confirmados
SI SE CUMPLE: consolidar 1+2 como módulo y opuesto como A Grande
SI NO SE CUMPLE: seguir 3
DESTINO: MODULO_CONFIRMADO + A
PROHIBICIONES: crear módulo si nunca hubo 2
PRUEBAS: fallo por profundidad; fallo temporal
```

### TM-3-004 · 3 confirmado y continuidad

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: TRES_CONFIRMADO
EVENTO: extensión posterior
PRECONDICIONES: 3 confirmado
SI SE CUMPLE: definir siguiente estructura
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir A automáticamente
PRUEBAS: extensión/giro
PREGUNTA: Q-007: consecuencia exacta después de 3
```

## 9. Módulo y A

### TM-MOD-001 · Módulo 1+2

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_FALLIDO
EVENTO: opuesto tras fallo de 3
PRECONDICIONES: 1 y 2 confirmados
SI SE CUMPLE: fijar rango del módulo y A Grande
SI NO SE CUMPLE: n/a
DESTINO: A_EN_CURSO
PROHIBICIONES: formar módulo sin 2
PRUEBAS: caso estándar
```

### TM-MOD-002 · Módulo reclasificado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: varios movimientos previos
EVENTO: retroceso posterior permite integración
PRECONDICIONES: regla de reclasificación satisfecha
SI SE CUMPLE: crear módulo conjunto conservando eventos
SI NO SE CUMPLE: mantener lecturas
DESTINO: MODULO_RECLASIFICADO
PROHIBICIONES: borrar eventos
PRUEBAS: varias velas
PREGUNTA: Q-008: catálogo completo de reclasificación
```

### TM-A-001 · A se extiende

**Estado:** `DOCUMENTADO`

```text
ORIGEN: A_EN_CURSO
EVENTO: nuevo extremo en dirección de A
PRECONDICIONES: sin B opuesta confirmable
SI SE CUMPLE: actualizar final y rango de A
SI NO SE CUMPLE: mantener
DESTINO: A_EN_CURSO
PROHIBICIONES: congelar A demasiado pronto
PRUEBAS: extensión 1 tick/multivela
```

### TM-A-002 · Nace B candidata

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: A_EN_CURSO
EVENTO: movimiento contrario a A
PRECONDICIONES: A posee inicio/final/rango
SI SE CUMPLE: abrir B candidata
SI NO SE CUMPLE: mantener A
DESTINO: B_CANDIDATA
PROHIBICIONES: llamar B confirmada antes del 100
PRUEBAS: retorno 10/99/100
```

## 10. B candidata, B confirmada y AUT

### TM-B-001 · B por debajo del 100 %

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: avance <100 % de A
PRECONDICIONES: B opuesta a A
SI SE CUMPLE: seguir B candidata
SI NO SE CUMPLE: n/a
DESTINO: B_CANDIDATA
PROHIBICIONES: llamar B Grande
PRUEBAS: 99,75 %
```

### TM-B-002 · B alcanza 100 %

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: alcanza 100 %
PRECONDICIONES: no supera 127 %+0,25
SI SE CUMPLE: confirmar B Grande
SI NO SE CUMPLE: seguir candidata
DESTINO: B_CONFIRMADA
PROHIBICIONES: exigir cierre
PRUEBAS: 100 exacto
```

### TM-B-003 · B entre 100 y límite AUT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CONFIRMADA
EVENTO: extensión sin superar 127 %+0,25
PRECONDICIONES: B confirmó 100
SI SE CUMPLE: mantener B confirmada
SI NO SE CUMPLE: n/a
DESTINO: B_CONFIRMADA
PROHIBICIONES: llamar AUT
PRUEBAS: 110;127; límite exacto
```

### TM-B-004 · B supera límite AUT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B candidata o confirmada
EVENTO: supera 127 %+0,25
PRECONDICIONES: A válida
SI SE CUMPLE: dejar B y confirmar AUT inmediato
SI NO SE CUMPLE: mantener B
DESTINO: AUT_CONFIRMADO
PROHIBICIONES: esperar otra vela
PRUEBAS: salto directo 90→130
```

### TM-B-005 · Giro de B candidata antes del 100

**Estado historico:** `SUPERADO_POR_PATCH_v2.2`

> La oscilacion interna ya no cancela ni divide B. Aplicar la seccion 0.2. El texto historico inferior se conserva solo por trazabilidad.

**Estado anterior:** `PENDIENTE_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: precio vuelve hacia A
PRECONDICIONES: B <100
SI SE CUMPLE: aplicar decisión experta
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: llamar C
PRUEBAS: giro 20/80/99
PREGUNTA: Q-009: absorción, nueva A o reclasificación
```

### TM-B-006 · B confirmada gira

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CONFIRMADA
EVENTO: movimiento contrario a B
PRECONDICIONES: B alcanzó 100 sin AUT
SI SE CUMPLE: clasificar C inmediatamente
SI NO SE CUMPLE: n/a
DESTINO: C_EN_CURSO
PROHIBICIONES: llamar C candidata
PRUEBAS: giro 1 tick
```

## 11. C y CUT

### TM-C-001 · C se extiende

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: C_EN_CURSO
EVENTO: avance en dirección contraria a B
PRECONDICIONES: B confirmada misma lectura
SI SE CUMPLE: actualizar C
SI NO SE CUMPLE: n/a
DESTINO: C_EN_CURSO
PROHIBICIONES: usar B de otra lectura
PRUEBAS: avance parcial
```

### TM-C-002 · CUT

**Estado:** `DOCUMENTADO`

```text
ORIGEN: C_EN_CURSO
EVENTO: C alcanza final de A
PRECONDICIONES: misma lectura
SI SE CUMPLE: confirmar CUT
SI NO SE CUMPLE: seguir C
DESTINO: CUT_CONFIRMADO
PROHIBICIONES: confirmar por color
PRUEBAS: toca/supera
PREGUNTA: Q-010: CUT evento o función; tocar o superar
```

### TM-C-003 · C no alcanza CUT y gira

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: C_EN_CURSO
EVENTO: movimiento vuelve hacia B
PRECONDICIONES: C < final A
SI SE CUMPLE: aplicar decisión experta
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: inventar función
PRUEBAS: múltiples profundidades
PREGUNTA: Q-011: tratamiento completo de C sin CUT
```

### TM-C-004 · Después de CUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: CUT_CONFIRMADO
EVENTO: continuidad o giro
PRECONDICIONES: CUT confirmado
SI SE CUMPLE: definir siguiente lectura
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: cerrar todo automáticamente
PRUEBAS: continúa/gira
PREGUNTA: Q-012: consecuencia posterior a CUT
```

## 12. AUT y TT

### TM-AUT-001 · AUT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B candidata o confirmada
EVENTO: supera 127 %+0,25
PRECONDICIONES: A válida
SI SE CUMPLE: activar TT posible
SI NO SE CUMPLE: n/a
DESTINO: TT_POSIBLE
PROHIBICIONES: mantener B vigente
PRUEBAS: salto multinivel
```

### TM-TT-001 · TT progresa

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: TT_POSIBLE
EVENTO: expansión desde final A hacia objetivo
PRECONDICIONES: AUT misma lectura
SI SE CUMPLE: actualizar porcentaje
SI NO SE CUMPLE: n/a
DESTINO: TT_POSIBLE
PROHIBICIONES: llamar TT confirmado
PRUEBAS: 1–99,75 %
```

### TM-TT-002 · TT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: TT_POSIBLE
EVENTO: alcanza 100 %
PRECONDICIONES: objetivo = final A ± rango módulo
SI SE CUMPLE: confirmar TT y convertir recorrido culminante en nuevo 1
SI NO SE CUMPLE: seguir posible
DESTINO: TT_CONFIRMADO + UNO_CONFIRMADO
PROHIBICIONES: crear A/B/AUT propios sin lectura
PRUEBAS: 100 exacto/salto
```

### TM-TT-003 · TT falla antes del 100

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TT_POSIBLE
EVENTO: precio toca/corta final A antes de objetivo
PRECONDICIONES: AUT activo
SI SE CUMPLE: cancelar TT y aplicar reclasificación
SI NO SE CUMPLE: mantener TT
DESTINO: TT_FALLIDO
PROHIBICIONES: borrar AUT
PRUEBAS: fallo temprano/tardío
PREGUNTA: Q-013: condición exacta de fallo TT
```

### TM-TT-004 · AUT, 1 y TT pequeño simultáneos

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: AUT_CONFIRMADO
EVENTO: recorrido cumple referencias concurrentes
PRECONDICIONES: lecturas explícitas
SI SE CUMPLE: registrar todos por lectura
SI NO SE CUMPLE: n/a
DESTINO: ESTADOS_CONCURRENTES
PROHIBICIONES: fusionar etiquetas
PRUEBAS: caso simultáneo
```

## 13. FT

### TM-FT-001 · FT prohibido sin TT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: cualquier
EVENTO: movimiento contrario
PRECONDICIONES: TT no confirmado
SI SE CUMPLE: no FT
SI NO SE CUMPLE: n/a
DESTINO: SIN_FT
PROHIBICIONES: anticipar FT
PRUEBAS: caso negativo
```

### TM-FT-002 · FT candidato

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TT_CONFIRMADO
EVENTO: movimiento contrario claro
PRECONDICIONES: TT confirmado y posible pérdida de velocidad
SI SE CUMPLE: abrir FT candidato
SI NO SE CUMPLE: integrar micromovimiento
DESTINO: FT_CANDIDATO
PROHIBICIONES: confirmar por color
PRUEBAS: mismo minuto/multivela
PREGUNTA: Q-014: umbral matemático de movimiento claro y pérdida de velocidad
```

### TM-FT-003 · FT confirmado

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: FT_CANDIDATO
EVENTO: alcanza referencia FT
PRECONDICIONES: precondiciones completas
SI SE CUMPLE: confirmar FT
SI NO SE CUMPLE: mantener candidato
DESTINO: FT_CONFIRMADO
PROHIBICIONES: usar referencia no definida
PRUEBAS: frontera
PREGUNTA: Q-015: objetivo, inicio, cancelación y confirmación FT
```

### TM-FT-004 · Después de FT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: FT_CONFIRMADO
EVENTO: continuidad/giro
PRECONDICIONES: FT confirmado
SI SE CUMPLE: definir nuevo ciclo
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir nuevo 1
PRUEBAS: dos direcciones
PREGUNTA: Q-016: consecuencia posterior a FT
```

## 14. Árbol completo de gap

### TM-GAP-001 · Gap a favor de 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: Open avanza en dirección de 1
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: RUTA_GAP_FAVOR
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-017: funciones implícitas exactas
```

### TM-GAP-002 · Gap contrario a 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: Open avanza contra 1
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: A_INICIADA_POR_GAP
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-018: anclajes exactos de A por gap
```

### TM-GAP-003 · Gap cruza 100 de B

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura atraviesa nivel 100
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: B_CONFIRMADA_O_AUT
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-019: orden de niveles implícitos
```

### TM-GAP-004 · Gap cruza AUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura supera 127 %+0,25
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: AUT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-020: AUT por gap y objetivo TT
```

### TM-GAP-005 · Gap cruza objetivo TT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura supera objetivo 100 TT
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: TT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-021: confirmación inmediata y precio de nuevo 1
```

### TM-GAP-006 · Gap cruza CUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura cruza final de A durante C
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: CUT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-022: CUT por gap
```

### TM-GAP-007 · Gap cruza nivel FT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura cruza referencia FT
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: FT_CONFIRMADO_O_PENDIENTE
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-023: FT por gap
```

## 15. Saltos multinivel en un tick

```text
REGLA PROPUESTA: si un tick salta varios umbrales, registrar todos los umbrales causales atravesados en orden, pero dejar como estado vigente el último estado válido. No exigir permanencia de un tick en estados intermedios.
```

- B candidata → AUT: cruza 100 y AUT.

- TT posible → más allá del objetivo: cruza 100 TT.

- C → más allá de CUT: cruza final A.

- 2 candidato → extremo y retroceso: orden intratick no observable.

La última combinación exige política de datos cuando dos precios extremos aparecen sin orden intratick fiable: `PENDIENTE_JAVIER` y no reconstrucción inventada.

## 16. Concurrencia L1/L2/L3

### TM-CON-001 · Actualizar lecturas

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: 1–3 lecturas activas
EVENTO: nuevo tick
PRECONDICIONES: cada lectura conserva referencias
SI SE CUMPLE: evaluar el tick en todas por separado
SI NO SE CUMPLE: n/a
DESTINO: lecturas actualizadas
PROHIBICIONES: mezclar niveles
PRUEBAS: dos eventos simultáneos
```

### TM-CON-002 · Abrir lectura

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lecturas activas
EVENTO: evento de apertura
PRECONDICIONES: regla expresa
SI SE CUMPLE: crear Ln con padre/regla/tick
SI NO SE CUMPLE: no abrir
DESTINO: Ln
PROHIBICIONES: abrir por apariencia
PRUEBAS: L2/L3
PREGUNTA: Q-024: lista exhaustiva de disparadores
```

### TM-CON-003 · Capacidad máxima

**Estado:** `DOCUMENTADO`

```text
ORIGEN: L1/L2 activas
EVENTO: tercera posibilidad
PRECONDICIONES: excepcional y justificada
SI SE CUMPLE: abrir L3
SI NO SE CUMPLE: integrar/invalidar
DESTINO: L3 o no
PROHIBICIONES: más de 3
PRUEBAS: tres lecturas
PREGUNTA: Q-025: máximo absoluto y prioridad
```

### TM-CON-004 · Mismo movimiento en dos lecturas

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: L1/L2
EVENTO: un recorrido cumple papeles distintos
PRECONDICIONES: referencias separadas
SI SE CUMPLE: registrar ambos papeles
SI NO SE CUMPLE: n/a
DESTINO: doble etiqueta por lectura
PROHIBICIONES: fusionar lecturas
PRUEBAS: TT L1 y 1 L2
```

### TM-CON-005 · Cerrar/integrar lectura

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: múltiples lecturas
EVENTO: convergencia o incompatibilidad
PRECONDICIONES: regla de integración
SI SE CUMPLE: marcar integrada/invalidada conservando historial
SI NO SE CUMPLE: mantener
DESTINO: LECTURA_CERRADA
PROHIBICIONES: borrar
PRUEBAS: casos variados
PREGUNTA: Q-026: criterios exhaustivos de cierre
```

## 17. Reclasificación

### TM-REC-001 · Velas previas pasan a módulo

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: retroceso revela 1+2 conjunto
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-027: condiciones exactas
```

### TM-REC-002 · Velas previas pasan a 1 conjunto

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: retroceso revela unidad mayor
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-028: condiciones exactas
```

### TM-REC-003 · Movimiento candidato absorbido

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: no alcanza confirmación y retorna
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-029: reglas por estado
```

### TM-REC-004 · AUT simultáneo con 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: AUT cumple nacimiento de 1
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-030: referencias
```

### TM-REC-005 · TT pequeño dentro de TT mayor

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: módulos anidados
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-031: anidamiento y prioridad
```

### TM-REC-006 · Lectura alternativa pasa a principal

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: evidencia posterior
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-032: criterio de prioridad
```

## 18. Cambio de vela

```text
La frontera temporal no crea por sí sola una función. Al abrir vela: registrar cierre, apertura, gap y lecturas. Las funciones pueden comenzar en una vela y terminar en otras. TT y FT pueden coexistir dentro de una misma vela si las referencias se alcanzan cronológicamente.
```

- Cambio de vela con `1`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `2 candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `2 confirmado`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `3 candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `A`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `B candidata`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `B confirmada`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `AUT/TT posible`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `C`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `FT candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

## 19. Transiciones prohibidas

- C sin B confirmada en la misma lectura.

- CUT sin C válida.

- TT sin AUT.

- TT confirmado antes del 100 %.

- FT sin TT confirmado.

- 2 con gap.

- 2 con cola >0,25 previa a confirmación.

- B confirmada antes del 100 %.

- Mantener B después de superar AUT.

- Abrir L2/L3 sin regla expresa.

- Mezclar el A de L1 con el B de L2.

- Borrar historia al reclasificar.

- Inferir orden intravela usando solo OHLC cuando el orden afecta la etiqueta.

- Usar color de vela como fundamento funcional.

- Llamar ruido a un movimiento no resuelto para ocultar una rama ausente.

## 20. Matriz de cobertura de eventos

### Cobertura SIN_LECTURA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 1

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 2_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 2_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 3_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 3_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura MÓDULO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura A

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura B_CANDIDATA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura B_CONFIRMADA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura AUT

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_POSIBLE

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_FALLIDO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura C

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura CUT

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura FT_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura FT_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

## 21. Casos mínimos de prueba obligatorios

- `SIN_LECTURA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `1`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `2_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `2_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `3_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `3_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `MÓDULO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `A`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `B_CANDIDATA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `B_CONFIRMADA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `AUT`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_POSIBLE`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_FALLIDO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `C`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `CUT`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `FT_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `FT_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

## 22. Registro maestro de preguntas

Preguntas explícitas detectadas: Q-001 a Q-032. Además, la matriz de cobertura puede generar preguntas adicionales durante los tests. Las preguntas se resolverán después del primer test global, una por una, y cada respuesta actualizará regla, nodo y pruebas.

## 23. Criterio de promoción a v1

```text
PENDIENTE_JAVIER = 0
PROPUESTA_CONTROLADA no aprobada = 0
CONTRADICCIONES = 0
CELDAS SIN SALIDA = 0
TESTS FALLIDOS = 0
TRANSICIONES SIN PRECONDICIÓN = 0
LECTURAS ABIERTAS SIN REGLA = 0
```

## 24. Correccion experta incorporada durante pruebas

### TEST-TM-INTRAVELA-001 - Vela 20-7-7

**Estado:** `CONFIRMADO_JAVIER`

```text
UNA UNICA VELA:
1. Sube 20 puntos -> 1.
2. Por descarte -> MODULO.
3. Retrocede 7 puntos -> A.
4. Recupera 7 puntos hasta el maximo -> B al 100 % de A.
5. B queda confirmada.
6. No hay AUT porque no supera 127 % + 0,25.

SECUENCIA CANONICA:
1 -> MODULO_POR_DESCARTE -> A -> B_CONFIRMADA_100
```

**Correccion del arbol:** queda prohibido omitir el modulo por descarte en esta secuencia y saltar directamente de 1 a A.

---

## 24. Protocolo obligatorio de escenarios completos

### TM-ESC-001 · Enumeración total antes de responder

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: cualquier lectura TM activa
EVENTO: solicitud de clasificación de una o varias velas
PRECONDICIONES: recorrer el árbol completo, incluidas concurrencia y reclasificación
SI SE CUMPLE: enumerar todos los escenarios TM válidos compatibles con los ticks
SI NO SE CUMPLE: respuesta inválida e incompleta
DESTINO: RESPUESTA_TM_COMPLETA
PROHIBICIONES: responder solo con el escenario principal; ocultar escenarios coexistentes; inventar escenarios
PRUEBAS: caso con 1 escenario; caso con 2 escenarios; caso excepcional con 3 escenarios
```

### TM-ESC-002 · Número máximo de escenarios

**Estado:** `CONFIRMADO_JAVIER`

```text
REGLA: una respuesta TM puede contener como máximo 3 escenarios válidos.
FRECUENCIA ESPERADA: normalmente habrá 1 o 2 escenarios.
ESCENARIO 3: solo se mostrará cuando el recorrido completo del árbol lo sostenga.
PROHIBICIÓN: forzar siempre 3 escenarios.
```

### TM-ESC-003 · Orden obligatorio de respuesta

**Estado:** `CONFIRMADO_JAVIER`

```text
1. Recorrer el árbol principal.
2. Recorrer concurrencia.
3. Recorrer reclasificación.
4. Detectar funciones simultáneas de una misma vela.
5. Detectar funciones conjuntas de varias velas.
6. Eliminar escenarios incompatibles con los ticks.
7. Mostrar todos los escenarios supervivientes, numerados del 1 al 3.
```

### TM-ESC-004 · Formato obligatorio

**Estado:** `CONFIRMADO_JAVIER`

```text
ESCENARIO 1:
- secuencia TM completa

ESCENARIO 2:
- secuencia TM completa

ESCENARIO 3:
- secuencia TM completa, solo si existe

LECTURA COMÚN:
- hechos TM compartidos por todos los escenarios
```

### TM-ESC-005 · Caso validado 23:39–23:41

**Estado:** `CONFIRMADO_JAVIER`

```text
LECTURA COMÚN:
23:39 = 1 alcista.
23:40 = A + B + AUT; abre TT posible alcista.
23:41 alcanza el objetivo del TT y es nuevo 1.

ESCENARIO 1:
23:40 abre el TT posible y 23:41 lo culmina.
23:41 = TT confirmado + nuevo 1.

ESCENARIO 2:
23:40 y 23:41 forman conjuntamente el TT del 1 de 23:39.
23:41 = culminación del TT conjunto + nuevo 1.

PROHIBICIÓN:
No responder únicamente con uno de los dos escenarios.
```

### TM-ESC-006 · Regla de validez de respuesta

**Estado:** `CONFIRMADO_JAVIER`

```text
Una respuesta es VÁLIDA solo si:
- ha recorrido el árbol completo;
- ha comprobado escenarios concurrentes;
- incluye todos los escenarios compatibles;
- no supera 3 escenarios;
- no confunde número de vela con función TM.

Si falta un escenario válido, la respuesta se considera INCORRECTA aunque el escenario mostrado sea verdadero.
```

---

## 25. Regla obligatoria FT inmediatamente posterior a TT

### TM-FT-005 · Giro claro desde el extremo de un TT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN:
TT confirmado.

EVENTO:
Desde el extremo que culmina el TT aparece una bajada o subida contraria clara y relevante.

PRECONDICIONES:
1. El TT anterior está confirmado.
2. El movimiento nace desde el extremo final del TT.
3. El movimiento va en sentido contrario al TT.
4. El desarrollo contrario es claro y tiene recorrido observable.

RESULTADO OBLIGATORIO:
El movimiento contrario se clasifica como FT del TT anterior.

CONCURRENCIA:
El mismo movimiento puede ser simultáneamente:
- FT del TT anterior; y
- A de un nuevo módulo por descarte nacido en el extremo.

PROHIBICIONES:
- Omitir FT por atender solo la nueva lectura modular.
- Responder únicamente A cuando también existe FT.
- Exigir otra vela para reconocer el FT si ya es claro en la vela actual.
- Borrar la referencia del TT al comenzar la nueva lectura.

CONTROL DE RESPUESTA:
Después de cada TT confirmado, el árbol debe preguntar obligatoriamente:
"¿Desde el extremo del TT aparece un movimiento contrario claro y relevante?"
Sí -> incluir FT en todos los escenarios compatibles.
No -> no inventar FT.
```

### TM-FT-006 · Caso de regresión, vela 5 desde 23:39

**Estado:** `CONFIRMADO_JAVIER`

```text
CONTEXTO:
Vela 5 = 23:43.
La vela 5 culmina el TT alcista anterior y marca un máximo aproximado de 29192,10.
Después baja hasta aproximadamente 29185,60.
Recorrido contrario aproximado: 6,50 puntos.

LECTURA OBLIGATORIA:
1. Culminación del TT alcista anterior.
2. Nuevo 1 en la vela 5.
3. En el máximo: módulo por descarte.
4. Bajada desde el máximo: A bajista de la nueva lectura.
5. Simultáneamente: FT bajista del TT alcista anterior.

ERROR DE REGRESIÓN:
La respuesta falla si menciona A bajista pero omite FT bajista.
```

### TM-FT-007 · Comprobación sistemática posterior a TT

**Estado:** `CONFIRMADO_JAVIER`

```text
Cada vez que se confirme un TT:
1. Conservar la referencia y el extremo del TT.
2. Analizar todos los ticks posteriores desde ese extremo.
3. Buscar movimiento contrario claro y relevante.
4. Si existe, activar FT.
5. En paralelo, recorrer módulo por descarte, A, B y demás lecturas nuevas.
6. Mostrar ambas lecturas si coexisten.

La detección del FT no puede quedar anulada por el nacimiento de un nuevo 1,
un módulo por descarte o una A concurrente.
```

---

## 26. B candidata que cruza de vela y funciona simultaneamente como modulo

### TM-CONC-008 · Persistencia de B candidata tras cambio de vela

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN:
Existe una A Grande confirmada y ha comenzado un movimiento contrario
clasificado como B candidata.

EVENTO:
Cambia la vela antes de que la B candidata alcance su frontera de confirmacion.

RESULTADO OBLIGATORIO:
El cambio de vela no cancela, reinicia ni confirma por si mismo la B candidata.
La lectura principal conserva:
A Grande -> B candidata pendiente.

CONTROL DE APERTURA:
Al abrir la nueva vela se evalua primero el gap.
El gap se registra dentro de la cronologia, pero no borra la B candidata heredada.
```

### TM-CONC-009 · La B candidata heredada puede ser modulo de una segunda lectura

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN LECTURA 1:
A Grande -> B candidata pendiente que continua en la vela siguiente.

CONDICION DE APERTURA DE LECTURA 2:
La subida o bajada que constituye la B candidata heredada puede tomarse,
simultaneamente y sin borrar la lectura 1, como modulo por descarte de una nueva lectura.

EVENTO:
En la nueva vela, despues del gap, el precio retrocede en sentido contrario
a ese modulo.

RESULTADO:
Se mantienen dos lecturas concurrentes:

LECTURA 1:
A Grande anterior -> B candidata pendiente.

LECTURA 2:
B candidata de lectura 1 = modulo por descarte.
Retroceso posterior = A de lectura 2.
Movimiento contrario posterior = B de lectura 2.
Si esa B supera 127 % + 0,25 puntos de A, deja de ser B y confirma AUT.

PROHIBICIONES:
- Cancelar la B candidata solo porque cambio la vela.
- Considerar que el gap crea por si solo la A de la lectura 2.
- Borrar la lectura 1 al abrir la lectura 2.
- Llamar B Grande a la B de lectura 2 despues de superar 127 % + 0,25.
- Omitir AUT cuando la frontera haya sido superada.
```

### TM-CONC-010 · Caso de regresion velas 5 y 6, 23:43-23:44

**Estado:** `CONFIRMADO_JAVIER`

```text
VELA 5 - 23:43:
Maximo inicial: 29192,10.
Minimo posterior: 29185,60.
Bajada: A Grande bajista y, simultaneamente, FT bajista del TT anterior.
Desde 29185,60 comienza una subida clasificada como B candidata alcista.

CAMBIO A VELA 6 - 23:44:
Cierre previo aproximado: 29189,30.
Apertura nueva: 29189,70.
Gap alcista aproximado: +0,40.
La B candidata de la lectura 1 continua pendiente.

LECTURA 2:
La subida que era B candidata en la lectura 1 funciona tambien como modulo.
En la vela 6 aparece un retroceso hasta 29188,80: A bajista de lectura 2.
Desde 29188,80 nace B alcista de lectura 2.
La subida posterior supera la frontera 127 % + 0,25 de esa A
y confirma AUT alcista.

SALIDA OBLIGATORIA:
LECTURA 1: A Grande bajista -> B candidata alcista pendiente/continua.
LECTURA 2: modulo -> A bajista -> B alcista -> AUT alcista.

ERROR DE REGRESION:
La respuesta falla si:
1. borra la B candidata al cambiar de vela;
2. no abre la lectura modular concurrente;
3. atribuye la A al gap en vez de al retroceso posterior;
4. omite la secuencia A -> B -> AUT de la segunda lectura.
```

---

## 27. Salida obligatoria separada: movimientos y patrones

### TM-SAL-001 · Separacion obligatoria de planos

**Estado:** `CONFIRMADO_JAVIER`

Toda lectura TM debe informar por separado:

```text
PLANO 1 - MOVIMIENTOS:
Modulo, 1, 2, 3, A, B, A Grande, B Grande, C Grande, AUT y CUT.

PLANO 2 - PATRONES:
TT, TT pendiente, TT fallido y FT.
```

Un elemento del plano de movimientos no sustituye ni oculta un patron. Si se confirma AUT y posteriormente se alcanza la expansion del 100 % del modulo, la salida no puede terminar en AUT: debe declarar tambien el TT confirmado en el plano de patrones.

### TM-SAL-002 · Comprobacion obligatoria de TT despues de AUT

**Estado:** `CONFIRMADO_JAVIER`

```text
SI se confirma AUT:
1. Mantener AUT en el plano de movimientos.
2. Proyectar el 100 % del rango del modulo desde el final de A.
3. Si el precio alcanza esa referencia, declarar TT confirmado.
4. Si todavia no la alcanza, declarar TT pendiente.
5. Si la estructura queda invalidada conforme a las reglas TM, declarar TT fallido.
```

**Prohibicion:** cerrar una lectura en AUT sin informar el estado del TT asociado.

### TM-SAL-003 · Formato minimo obligatorio de respuesta

**Estado:** `CONFIRMADO_JAVIER`

```text
MOVIMIENTOS:
[secuencia cronologica completa]

PATRONES:
[TT/TT pendiente/TT fallido/FT y su referencia]
```

### TM-SAL-004 · Regresion velas 5 y 6

**Estado:** `CONFIRMADO_JAVIER`

```text
MOVIMIENTOS:
Vela 5: modulo alcista.
Vela 6: A bajista -> B alcista -> AUT alcista.

PATRONES:
La vela 6 alcanza la expansion del 100 % del modulo alcista iniciado en la vela 5.
Resultado: TT alcista confirmado.
```

**Error de regresion:** la lectura falla si informa A -> B -> AUT, pero omite el TT alcista confirmado.


---

# ANEXO 3 - FUENTE INTEGRA: `TM_PATCH_CANONICO_v1_0_TT_FT_CONCURRENCIA_VELA7.md`

- **SHA-256:** `58628c161246097aff8f51efffe5f6342d55a6c721771e73574137c23f4e9435`
- **Integridad:** contenido incorporado sin recortes.

# TM PATCH CANONICO v1.0
## TT extendido, FT posterior y concurrencia interna en una misma vela

**Estado:** regla canonica obligatoria para integrar en el Arbol Maestro TM.

## 1. Regla del extremo real de un TT

1. El nivel del **100 %** es el minimo que confirma que un movimiento cumple como **TT**.
2. Alcanzar el 100 % **no cierra ni termina automaticamente el TT**.
3. Un TT confirmado puede continuar y extenderse por encima del 100 %.
4. El extremo final del TT se fija en el **maximo real alcanzado** si el TT es alcista, o en el **minimo real alcanzado** si el TT es bajista, antes de que comience el movimiento contrario que deba leerse como FT.
5. Por tanto, el FT nunca debe medirse desde el punto exacto del 100 % si el TT continuo extendiendose despues de alcanzarlo.

## 2. Regla del FT posterior al TT

1. Una vez terminado el recorrido efectivo del TT, el movimiento contrario que nace en su extremo real se clasifica como **FT**.
2. En nomenclatura TM se escribe solamente **FT**. No se anade al nombre "alcista" ni "bajista".
3. No obstante, el motor debe conservar internamente la direccion del recorrido:
   - TT alcista -> FT con recorrido descendente.
   - TT bajista -> FT con recorrido ascendente.
4. El FT puede comenzar dentro de la misma vela en la que el TT alcanza su extremo final y continuar en una o varias velas posteriores.
5. Una vela posterior puede completar el FT de un TT nacido en velas anteriores sin que el FT pertenezca exclusivamente a esa vela posterior.

## 3. Regla de concurrencia estructural

La lectura principal y las lecturas internas no son excluyentes.

Una misma vela puede simultaneamente:

- participar en el FT de un TT de escala superior;
- contener un modulo pequeno;
- iniciar una A Grande interna;
- desarrollar una B Grande interna;
- superar el limite de B Grande, dejar de ser B Grande y confirmar AUT;
- confirmar un TT pequeno interno al alcanzar como minimo el 100 % de su A Grande;
- extender ese TT pequeno mas alla del 100 % dentro de la misma vela.

El motor no debe borrar una lectura superior cuando detecta una estructura interna valida, ni debe borrar la estructura interna por existir un FT superior.

## 4. Secuencia canonica del caso velas 5, 6 y 7

### Estructura principal

1. El TT alcista comienza en la vela 5.
2. El TT continua durante la vela 6.
3. Aunque el TT ya haya alcanzado el 100 %, puede seguir extendiendose.
4. El extremo final del TT alcista queda fijado en el **maximo de la vela 6**.
5. Desde ese maximo comienza el movimiento contrario.
6. El recorrido desde el maximo de la vela 6 hasta el minimo de la vela 7 es el **FT del TT alcista de las velas 5 y 6**.
7. La vela 7 participa en ese FT. No debe etiquetarse como un FT alcista. En salida TM se informa simplemente `FT`, con direccion interna descendente.

### Estructura interna concurrente

1. La pequena bajada situada al final de la vela 6, desde su maximo hasta el inicio de la vela 7, puede ser **modulo**, si cumple todas las condiciones canonicas de modulo.
2. Esta clasificacion es condicional: si no se pueden verificar las condiciones del modulo, debe registrarse como `MODULO_CANDIDATO_NO_CONFIRMADO` y no inventarse la confirmacion.
3. Desde el inicio de la vela 7 aparece una pequena subida que se toma como **A Grande interna**.
4. El descenso posterior actua como **B Grande interna** mientras alcance al menos el 100 % de A Grande y no supere el limite canonico de B Grande.
5. Si el descenso supera el limite `127 % + 0,25 puntos`, deja inmediatamente de clasificarse como B Grande y se confirma **AUT**.
6. Cuando el movimiento descendente alcanza como minimo el 100 % de la A Grande interna, queda confirmado un **TT pequeno descendente**.
7. El TT pequeno puede seguir extendiendose hacia abajo hasta el minimo posterior de la vela 7.
8. El pequeno tamano o la falta de operabilidad no invalida la existencia estructural. Debe distinguirse entre `PATRON_DETECTADO` y `PATRON_OPERABLE`.

## 5. Prioridad de salida del motor

Para cada vela, el Arbol debe producir dos capas separadas:

### Capa A. Contexto principal

- patron superior activo;
- identificador del TT de origen;
- extremo real del TT;
- FT posterior activo;
- direccion geometrica del FT;
- velas que participan en el recorrido.

### Capa B. Estructuras internas concurrentes

- modulo confirmado o candidato;
- A Grande interna;
- B Grande interna;
- superacion del limite de B Grande;
- AUT;
- TT pequeno confirmado;
- extension real del TT pequeno;
- operable: si/no, evaluado aparte.

## 6. Prohibiciones expresas

El Arbol no puede:

1. cerrar un TT automaticamente al tocar el 100 %;
2. medir el FT desde el 100 % si el TT siguio extendiendose;
3. llamar "FT alcista" al descenso posterior a un TT alcista;
4. atribuir el FT solo a la vela 7 ignorando que nace en el maximo de la vela 6;
5. eliminar el FT principal porque dentro de la vela 7 exista otro TT pequeno;
6. eliminar el TT pequeno interno porque la vela 7 participe en un FT superior;
7. conservar la etiqueta B Grande despues de superar `127 % + 0,25 puntos`;
8. descartar un patron estructural solo por ser pequeno o no operable;
9. confirmar el modulo final de la vela 6 sin verificar sus condiciones propias.

## 7. Caso de validacion obligatorio

### Entrada conceptual

- vela 5 inicia TT alcista;
- vela 6 alcanza el 100 % y continua hasta un maximo superior;
- desde el maximo de vela 6 el precio baja;
- la bajada continua hasta el minimo de vela 7;
- al inicio de vela 7 existe una subida pequena;
- despues aparece una bajada que supera el limite de B Grande y alcanza el 100 % de la A interna;
- el movimiento continua descendiendo dentro de vela 7.

### Salida minima correcta

```text
TT_PRINCIPAL: confirmado
TT_DIRECCION: alcista
TT_INICIO: vela_5
TT_EXTREMO_FINAL: maximo_vela_6
TT_100_POR_CIENTO: umbral_minimo_no_extremo_final
FT_PRINCIPAL: confirmado
FT_ORIGEN: maximo_vela_6
FT_FIN_OBSERVADO: minimo_vela_7
FT_DIRECCION_GEOMETRICA: descendente
VELA_7_PARTICIPA_EN_FT: si

MODULO_FIN_VELA_6: condicionado_a_validacion
A_GRANDE_INTERNA_VELA_7: detectada
B_GRANDE_INTERNA_VELA_7: temporal
B_GRANDE_LIMITE_SUPERADO: si
AUT_INTERNO: confirmado
TT_INTERNO_VELA_7: confirmado_descendente
TT_INTERNO_EXTENDIDO_MAS_ALLA_100: si
OPERABILIDAD_TT_INTERNO: evaluar_aparte
CONCURRENCIA: permitida_y_obligatoria
```

## 8. Invariante final

> El 100 % confirma el minimo de un TT, pero no determina su final. El final del TT es su extremo real. Desde ese extremo nace el FT contrario. Simultaneamente, dentro del recorrido del FT pueden existir modulos y nuevos patrones A-B-AUT-TT de menor escala, sin que una lectura invalide la otra.


---

# ANEXO 4 - FUENTE INTEGRA: `TM_PATCH_CANONICO_v1_1_RESET_TT_VELAS8_9.md`

- **SHA-256:** `fba5f3964ab74b736974c4e4e58fb0e8ca77361b613d7a19823d2ee87defe0d5`
- **Integridad:** contenido incorporado sin recortes.

# TM PATCH CANONICO v1.1
## TT extendido, FT posterior y concurrencia interna en una misma vela

**Estado:** regla canonica obligatoria para integrar en el Arbol Maestro TM.

## 1. Regla del extremo real de un TT

1. El nivel del **100 %** es el minimo que confirma que un movimiento cumple como **TT**.
2. Alcanzar el 100 % **no cierra ni termina automaticamente el TT**.
3. Un TT confirmado puede continuar y extenderse por encima del 100 %.
4. El extremo final del TT se fija en el **maximo real alcanzado** si el TT es alcista, o en el **minimo real alcanzado** si el TT es bajista, antes de que comience el movimiento contrario que deba leerse como FT.
5. Por tanto, el FT nunca debe medirse desde el punto exacto del 100 % si el TT continuo extendiendose despues de alcanzarlo.

## 2. Regla del FT posterior al TT

1. Una vez terminado el recorrido efectivo del TT, el movimiento contrario que nace en su extremo real se clasifica como **FT**.
2. En nomenclatura TM se escribe solamente **FT**. No se anade al nombre "alcista" ni "bajista".
3. No obstante, el motor debe conservar internamente la direccion del recorrido:
   - TT alcista -> FT con recorrido descendente.
   - TT bajista -> FT con recorrido ascendente.
4. El FT puede comenzar dentro de la misma vela en la que el TT alcanza su extremo final y continuar en una o varias velas posteriores.
5. Una vela posterior puede completar el FT de un TT nacido en velas anteriores sin que el FT pertenezca exclusivamente a esa vela posterior.

## 3. Regla de concurrencia estructural

La lectura principal y las lecturas internas no son excluyentes.

Una misma vela puede simultaneamente:

- participar en el FT de un TT de escala superior;
- contener un modulo pequeno;
- iniciar una A Grande interna;
- desarrollar una B Grande interna;
- superar el limite de B Grande, dejar de ser B Grande y confirmar AUT;
- confirmar un TT pequeno interno al alcanzar como minimo el 100 % de su A Grande;
- extender ese TT pequeno mas alla del 100 % dentro de la misma vela.

El motor no debe borrar una lectura superior cuando detecta una estructura interna valida, ni debe borrar la estructura interna por existir un FT superior.

## 4. Secuencia canonica del caso velas 5, 6 y 7

### Estructura principal

1. El TT alcista comienza en la vela 5.
2. El TT continua durante la vela 6.
3. Aunque el TT ya haya alcanzado el 100 %, puede seguir extendiendose.
4. El extremo final del TT alcista queda fijado en el **maximo de la vela 6**.
5. Desde ese maximo comienza el movimiento contrario.
6. El recorrido desde el maximo de la vela 6 hasta el minimo de la vela 7 es el **FT del TT alcista de las velas 5 y 6**.
7. La vela 7 participa en ese FT. No debe etiquetarse como un FT alcista. En salida TM se informa simplemente `FT`, con direccion interna descendente.

### Estructura interna concurrente

1. La pequena bajada situada al final de la vela 6, desde su maximo hasta el inicio de la vela 7, puede ser **modulo**, si cumple todas las condiciones canonicas de modulo.
2. Esta clasificacion es condicional: si no se pueden verificar las condiciones del modulo, debe registrarse como `MODULO_CANDIDATO_NO_CONFIRMADO` y no inventarse la confirmacion.
3. Desde el inicio de la vela 7 aparece una pequena subida que se toma como **A Grande interna**.
4. El descenso posterior actua como **B Grande interna** mientras alcance al menos el 100 % de A Grande y no supere el limite canonico de B Grande.
5. Si el descenso supera el limite `127 % + 0,25 puntos`, deja inmediatamente de clasificarse como B Grande y se confirma **AUT**.
6. Cuando el movimiento descendente alcanza como minimo el 100 % de la A Grande interna, queda confirmado un **TT pequeno descendente**.
7. El TT pequeno puede seguir extendiendose hacia abajo hasta el minimo posterior de la vela 7.
8. El pequeno tamano o la falta de operabilidad no invalida la existencia estructural. Debe distinguirse entre `PATRON_DETECTADO` y `PATRON_OPERABLE`.

## 5. Prioridad de salida del motor

Para cada vela, el Arbol debe producir dos capas separadas:

### Capa A. Contexto principal

- patron superior activo;
- identificador del TT de origen;
- extremo real del TT;
- FT posterior activo;
- direccion geometrica del FT;
- velas que participan en el recorrido.

### Capa B. Estructuras internas concurrentes

- modulo confirmado o candidato;
- A Grande interna;
- B Grande interna;
- superacion del limite de B Grande;
- AUT;
- TT pequeno confirmado;
- extension real del TT pequeno;
- operable: si/no, evaluado aparte.

## 6. Prohibiciones expresas

El Arbol no puede:

1. cerrar un TT automaticamente al tocar el 100 %;
2. medir el FT desde el 100 % si el TT siguio extendiendose;
3. llamar "FT alcista" al descenso posterior a un TT alcista;
4. atribuir el FT solo a la vela 7 ignorando que nace en el maximo de la vela 6;
5. eliminar el FT principal porque dentro de la vela 7 exista otro TT pequeno;
6. eliminar el TT pequeno interno porque la vela 7 participe en un FT superior;
7. conservar la etiqueta B Grande despues de superar `127 % + 0,25 puntos`;
8. descartar un patron estructural solo por ser pequeno o no operable;
9. confirmar el modulo final de la vela 6 sin verificar sus condiciones propias.

## 7. Caso de validacion obligatorio

### Entrada conceptual

- vela 5 inicia TT alcista;
- vela 6 alcanza el 100 % y continua hasta un maximo superior;
- desde el maximo de vela 6 el precio baja;
- la bajada continua hasta el minimo de vela 7;
- al inicio de vela 7 existe una subida pequena;
- despues aparece una bajada que supera el limite de B Grande y alcanza el 100 % de la A interna;
- el movimiento continua descendiendo dentro de vela 7.

### Salida minima correcta

```text
TT_PRINCIPAL: confirmado
TT_DIRECCION: alcista
TT_INICIO: vela_5
TT_EXTREMO_FINAL: maximo_vela_6
TT_100_POR_CIENTO: umbral_minimo_no_extremo_final
FT_PRINCIPAL: confirmado
FT_ORIGEN: maximo_vela_6
FT_FIN_OBSERVADO: minimo_vela_7
FT_DIRECCION_GEOMETRICA: descendente
VELA_7_PARTICIPA_EN_FT: si

MODULO_FIN_VELA_6: condicionado_a_validacion
A_GRANDE_INTERNA_VELA_7: detectada
B_GRANDE_INTERNA_VELA_7: temporal
B_GRANDE_LIMITE_SUPERADO: si
AUT_INTERNO: confirmado
TT_INTERNO_VELA_7: confirmado_descendente
TT_INTERNO_EXTENDIDO_MAS_ALLA_100: si
OPERABILIDAD_TT_INTERNO: evaluar_aparte
CONCURRENCIA: permitida_y_obligatoria
```

## 8. Invariante final

> El 100 % confirma el minimo de un TT, pero no determina su final. El final del TT es su extremo real. Desde ese extremo nace el FT contrario. Simultaneamente, dentro del recorrido del FT pueden existir modulos y nuevos patrones A-B-AUT-TT de menor escala, sin que una lectura invalide la otra.

---

# 9. Regla canonica de cierre de ciclo y reset al confirmar TT

**Prioridad:** obligatoria. Esta regla prevalece sobre cualquier lectura que mantenga activo el ciclo anterior despues de confirmarse un TT.

1. Cuando el movimiento alcanza como minimo el 100 % exigido y confirma TT, el ciclo vigente queda cerrado.
2. La misma vela que confirma el TT pertenece simultaneamente a dos ciclos:
   - en el ciclo anterior, contiene o confirma el TT;
   - en el ciclo nuevo, pasa a ser el nuevo `1`.
3. El ciclo nuevo comienza en la propia vela TT, nunca en la vela posterior.
4. Tras el reset no se arrastran como referencias activas el `1`, el modulo X, A Grande, B Grande, AUT ni los niveles porcentuales del ciclo cerrado.
5. La informacion anterior se conserva unicamente como trazabilidad historica y concurrencia.

## 9.1 Orden obligatorio del Arbol

```text
1. Identificar el 1 vigente.
2. Medir el modulo completo X del 1.
3. Evaluar la apertura siguiente: gap, cola y salida.
4. Si hay gap, descartar 2.
5. Recorrer A, B y AUT.
6. Fijar el final real de A Grande.
7. Proyectar X desde el final de A Grande en la direccion del modulo.
8. Si el recorrido alcanza X, confirmar TT.
9. Cerrar inmediatamente el ciclo anterior.
10. Convertir la misma vela TT en el nuevo 1.
11. Recalcular el nuevo modulo con la vela TT.
12. Analizar la vela posterior exclusivamente desde el ciclo nuevo.
```

# 10. Caso canonico obligatorio: velas 8 y 9

## 10.1 Vela 8

La lectura comienza en la vela 8, sin arrastrar la vela 7:

```text
VELA_8 = 1
DIRECCION_GEOMETRICA = descendente
X = maximo_vela_8 - minimo_vela_8
```

`X` es la medida del modulo completo de la vela 8.

## 10.2 Vela 9 dentro del ciclo iniciado en vela 8

La vela 9 abre con gap de retroceso:

```text
GAP = si
DOS = imposible
```

La estructura interna obligatoria de vela 9 es:

```text
A -> B -> AUT
```

A Grande es el movimiento contrario al modulo de la vela 8:

```text
ORIGEN_A_GRANDE = final/minimo_vela_8
FINAL_A_GRANDE = maximo_vela_9
```

Desde el final de A Grande se mide el descenso:

```text
DESCENSO_VELA_9 = maximo_vela_9 - minimo_posterior_vela_9
NIVEL_100_TT = maximo_vela_9 - X
```

Confirmacion:

```text
SI DESCENSO_VELA_9 >= X
    VELA_9 = TT confirmado en el ciclo anterior
```

Equivalencia:

```text
SI minimo_posterior_vela_9 <= NIVEL_100_TT
    VELA_9 = TT confirmado
```

## 10.3 Reset en vela 9

En el mismo instante de confirmacion del TT:

```text
CICLO_ANTERIOR:
  VELA_8 = 1
  VELA_9 = A + B + AUT + TT
  ESTADO = cerrado

RESET = inmediato

CICLO_NUEVO:
  VELA_9 = 1
  NUEVO_MODULO_X9 = maximo_vela_9 - minimo_vela_9
```

La vela 9 tiene doble pertenencia obligatoria:

```text
VELA_9 respecto al ciclo anterior = TT
VELA_9 respecto al ciclo nuevo = 1
```

# 11. Errores prohibidos adicionales

1. Enlazar la vela 8 con la vela 7 cuando se ha ordenado comenzar el ciclo en la vela 8.
2. Clasificar la vela 9 como TT sin medir X desde el final de A Grande.
3. Tratar el gap de retroceso de vela 9 como `2`.
4. Mantener activo el ciclo de vela 8 despues de confirmar el TT.
5. Esperar a la vela 10 para crear el nuevo `1`.
6. Usar X de vela 8 para analizar el ciclo nuevo iniciado en vela 9.
7. Confundir la trazabilidad del TT anterior con el estado activo posterior al reset.

# 12. Invariante final actualizado

> Toda vela que confirma TT cierra el ciclo vigente y simultaneamente se convierte en el `1` del ciclo siguiente. El TT pertenece al ciclo anterior; el nuevo `1` pertenece al ciclo reiniciado. La vela posterior se analiza con las referencias recalculadas desde la vela TT convertida en nuevo `1`.


---

# ANEXO 5 - FUENTE INTEGRA: `TM_PATCH_CANONICO_v1_2_C_CUT_TERCERO_RESET.md`

- **SHA-256:** `b04b6629ffbd912f26ae2bedd0ae7cd366201db548749652d21bee3de4b108d6`
- **Integridad:** contenido incorporado sin recortes.

# TM PATCH CANONICO v1.2
## TT extendido, FT posterior y concurrencia interna en una misma vela

**Estado:** regla canonica obligatoria para integrar en el Arbol Maestro TM.

## 1. Regla del extremo real de un TT

1. El nivel del **100 %** es el minimo que confirma que un movimiento cumple como **TT**.
2. Alcanzar el 100 % **no cierra ni termina automaticamente el TT**.
3. Un TT confirmado puede continuar y extenderse por encima del 100 %.
4. El extremo final del TT se fija en el **maximo real alcanzado** si el TT es alcista, o en el **minimo real alcanzado** si el TT es bajista, antes de que comience el movimiento contrario que deba leerse como FT.
5. Por tanto, el FT nunca debe medirse desde el punto exacto del 100 % si el TT continuo extendiendose despues de alcanzarlo.

## 2. Regla del FT posterior al TT

1. Una vez terminado el recorrido efectivo del TT, el movimiento contrario que nace en su extremo real se clasifica como **FT**.
2. En nomenclatura TM se escribe solamente **FT**. No se anade al nombre "alcista" ni "bajista".
3. No obstante, el motor debe conservar internamente la direccion del recorrido:
   - TT alcista -> FT con recorrido descendente.
   - TT bajista -> FT con recorrido ascendente.
4. El FT puede comenzar dentro de la misma vela en la que el TT alcanza su extremo final y continuar en una o varias velas posteriores.
5. Una vela posterior puede completar el FT de un TT nacido en velas anteriores sin que el FT pertenezca exclusivamente a esa vela posterior.

## 3. Regla de concurrencia estructural

La lectura principal y las lecturas internas no son excluyentes.

Una misma vela puede simultaneamente:

- participar en el FT de un TT de escala superior;
- contener un modulo pequeno;
- iniciar una A Grande interna;
- desarrollar una B Grande interna;
- superar el limite de B Grande, dejar de ser B Grande y confirmar AUT;
- confirmar un TT pequeno interno al alcanzar como minimo el 100 % de su A Grande;
- extender ese TT pequeno mas alla del 100 % dentro de la misma vela.

El motor no debe borrar una lectura superior cuando detecta una estructura interna valida, ni debe borrar la estructura interna por existir un FT superior.

## 4. Secuencia canonica del caso velas 5, 6 y 7

### Estructura principal

1. El TT alcista comienza en la vela 5.
2. El TT continua durante la vela 6.
3. Aunque el TT ya haya alcanzado el 100 %, puede seguir extendiendose.
4. El extremo final del TT alcista queda fijado en el **maximo de la vela 6**.
5. Desde ese maximo comienza el movimiento contrario.
6. El recorrido desde el maximo de la vela 6 hasta el minimo de la vela 7 es el **FT del TT alcista de las velas 5 y 6**.
7. La vela 7 participa en ese FT. No debe etiquetarse como un FT alcista. En salida TM se informa simplemente `FT`, con direccion interna descendente.

### Estructura interna concurrente

1. La pequena bajada situada al final de la vela 6, desde su maximo hasta el inicio de la vela 7, puede ser **modulo**, si cumple todas las condiciones canonicas de modulo.
2. Esta clasificacion es condicional: si no se pueden verificar las condiciones del modulo, debe registrarse como `MODULO_CANDIDATO_NO_CONFIRMADO` y no inventarse la confirmacion.
3. Desde el inicio de la vela 7 aparece una pequena subida que se toma como **A Grande interna**.
4. El descenso posterior actua como **B Grande interna** mientras alcance al menos el 100 % de A Grande y no supere el limite canonico de B Grande.
5. Si el descenso supera el limite `127 % + 0,25 puntos`, deja inmediatamente de clasificarse como B Grande y se confirma **AUT**.
6. Cuando el movimiento descendente alcanza como minimo el 100 % de la A Grande interna, queda confirmado un **TT pequeno descendente**.
7. El TT pequeno puede seguir extendiendose hacia abajo hasta el minimo posterior de la vela 7.
8. El pequeno tamano o la falta de operabilidad no invalida la existencia estructural. Debe distinguirse entre `PATRON_DETECTADO` y `PATRON_OPERABLE`.

## 5. Prioridad de salida del motor

Para cada vela, el Arbol debe producir dos capas separadas:

### Capa A. Contexto principal

- patron superior activo;
- identificador del TT de origen;
- extremo real del TT;
- FT posterior activo;
- direccion geometrica del FT;
- velas que participan en el recorrido.

### Capa B. Estructuras internas concurrentes

- modulo confirmado o candidato;
- A Grande interna;
- B Grande interna;
- superacion del limite de B Grande;
- AUT;
- TT pequeno confirmado;
- extension real del TT pequeno;
- operable: si/no, evaluado aparte.

## 6. Prohibiciones expresas

El Arbol no puede:

1. cerrar un TT automaticamente al tocar el 100 %;
2. medir el FT desde el 100 % si el TT siguio extendiendose;
3. llamar "FT alcista" al descenso posterior a un TT alcista;
4. atribuir el FT solo a la vela 7 ignorando que nace en el maximo de la vela 6;
5. eliminar el FT principal porque dentro de la vela 7 exista otro TT pequeno;
6. eliminar el TT pequeno interno porque la vela 7 participe en un FT superior;
7. conservar la etiqueta B Grande despues de superar `127 % + 0,25 puntos`;
8. descartar un patron estructural solo por ser pequeno o no operable;
9. confirmar el modulo final de la vela 6 sin verificar sus condiciones propias.

## 7. Caso de validacion obligatorio

### Entrada conceptual

- vela 5 inicia TT alcista;
- vela 6 alcanza el 100 % y continua hasta un maximo superior;
- desde el maximo de vela 6 el precio baja;
- la bajada continua hasta el minimo de vela 7;
- al inicio de vela 7 existe una subida pequena;
- despues aparece una bajada que supera el limite de B Grande y alcanza el 100 % de la A interna;
- el movimiento continua descendiendo dentro de vela 7.

### Salida minima correcta

```text
TT_PRINCIPAL: confirmado
TT_DIRECCION: alcista
TT_INICIO: vela_5
TT_EXTREMO_FINAL: maximo_vela_6
TT_100_POR_CIENTO: umbral_minimo_no_extremo_final
FT_PRINCIPAL: confirmado
FT_ORIGEN: maximo_vela_6
FT_FIN_OBSERVADO: minimo_vela_7
FT_DIRECCION_GEOMETRICA: descendente
VELA_7_PARTICIPA_EN_FT: si

MODULO_FIN_VELA_6: condicionado_a_validacion
A_GRANDE_INTERNA_VELA_7: detectada
B_GRANDE_INTERNA_VELA_7: temporal
B_GRANDE_LIMITE_SUPERADO: si
AUT_INTERNO: confirmado
TT_INTERNO_VELA_7: confirmado_descendente
TT_INTERNO_EXTENDIDO_MAS_ALLA_100: si
OPERABILIDAD_TT_INTERNO: evaluar_aparte
CONCURRENCIA: permitida_y_obligatoria
```

## 8. Invariante final

> El 100 % confirma el minimo de un TT, pero no determina su final. El final del TT es su extremo real. Desde ese extremo nace el FT contrario. Simultaneamente, dentro del recorrido del FT pueden existir modulos y nuevos patrones A-B-AUT-TT de menor escala, sin que una lectura invalide la otra.

---

# 9. Regla canonica de cierre de ciclo y reset al confirmar TT

**Prioridad:** obligatoria. Esta regla prevalece sobre cualquier lectura que mantenga activo el ciclo anterior despues de confirmarse un TT.

1. Cuando el movimiento alcanza como minimo el 100 % exigido y confirma TT, el ciclo vigente queda cerrado.
2. La misma vela que confirma el TT pertenece simultaneamente a dos ciclos:
   - en el ciclo anterior, contiene o confirma el TT;
   - en el ciclo nuevo, pasa a ser el nuevo `1`.
3. El ciclo nuevo comienza en la propia vela TT, nunca en la vela posterior.
4. Tras el reset no se arrastran como referencias activas el `1`, el modulo X, A Grande, B Grande, AUT ni los niveles porcentuales del ciclo cerrado.
5. La informacion anterior se conserva unicamente como trazabilidad historica y concurrencia.

## 9.1 Orden obligatorio del Arbol

```text
1. Identificar el 1 vigente.
2. Medir el modulo completo X del 1.
3. Evaluar la apertura siguiente: gap, cola y salida.
4. Si hay gap, descartar 2.
5. Recorrer A, B y AUT.
6. Fijar el final real de A Grande.
7. Proyectar X desde el final de A Grande en la direccion del modulo.
8. Si el recorrido alcanza X, confirmar TT.
9. Cerrar inmediatamente el ciclo anterior.
10. Convertir la misma vela TT en el nuevo 1.
11. Recalcular el nuevo modulo con la vela TT.
12. Analizar la vela posterior exclusivamente desde el ciclo nuevo.
```

# 10. Caso canonico obligatorio: velas 8 y 9

## 10.1 Vela 8

La lectura comienza en la vela 8, sin arrastrar la vela 7:

```text
VELA_8 = 1
DIRECCION_GEOMETRICA = descendente
X = maximo_vela_8 - minimo_vela_8
```

`X` es la medida del modulo completo de la vela 8.

## 10.2 Vela 9 dentro del ciclo iniciado en vela 8

La vela 9 abre con gap de retroceso:

```text
GAP = si
DOS = imposible
```

La estructura interna obligatoria de vela 9 es:

```text
A -> B -> AUT
```

A Grande es el movimiento contrario al modulo de la vela 8:

```text
ORIGEN_A_GRANDE = final/minimo_vela_8
FINAL_A_GRANDE = maximo_vela_9
```

Desde el final de A Grande se mide el descenso:

```text
DESCENSO_VELA_9 = maximo_vela_9 - minimo_posterior_vela_9
NIVEL_100_TT = maximo_vela_9 - X
```

Confirmacion:

```text
SI DESCENSO_VELA_9 >= X
    VELA_9 = TT confirmado en el ciclo anterior
```

Equivalencia:

```text
SI minimo_posterior_vela_9 <= NIVEL_100_TT
    VELA_9 = TT confirmado
```

## 10.3 Reset en vela 9

En el mismo instante de confirmacion del TT:

```text
CICLO_ANTERIOR:
  VELA_8 = 1
  VELA_9 = A + B + AUT + TT
  ESTADO = cerrado

RESET = inmediato

CICLO_NUEVO:
  VELA_9 = 1
  NUEVO_MODULO_X9 = maximo_vela_9 - minimo_vela_9
```

La vela 9 tiene doble pertenencia obligatoria:

```text
VELA_9 respecto al ciclo anterior = TT
VELA_9 respecto al ciclo nuevo = 1
```

# 11. Errores prohibidos adicionales

1. Enlazar la vela 8 con la vela 7 cuando se ha ordenado comenzar el ciclo en la vela 8.
2. Clasificar la vela 9 como TT sin medir X desde el final de A Grande.
3. Tratar el gap de retroceso de vela 9 como `2`.
4. Mantener activo el ciclo de vela 8 despues de confirmar el TT.
5. Esperar a la vela 10 para crear el nuevo `1`.
6. Usar X de vela 8 para analizar el ciclo nuevo iniciado en vela 9.
7. Confundir la trazabilidad del TT anterior con el estado activo posterior al reset.

# 12. Invariante final actualizado

> Toda vela que confirma TT cierra el ciclo vigente y simultaneamente se convierte en el `1` del ciclo siguiente. El TT pertenece al ciclo anterior; el nuevo `1` pertenece al ciclo reiniciado. La vela posterior se analiza con las referencias recalculadas desde la vela TT convertida en nuevo `1`.

---

# 13. PATCH CANONICO v1.2 - C GRANDE, CUT, TERCERO, TT Y RESET

**Estado:** decision experta posterior y prevalente.

## 13.1 Principio general: A y C pueden superar la base del modulo

El Arbol debe comprobar no solo la medida de A, B o C respecto a la funcion anterior, sino tambien si el recorrido alcanza o supera la base o inicio del modulo activo.

```text
SI A supera la base/inicio del modulo:
    AUT

SI C supera la base/inicio del modulo:
    evaluar rama C -> CUT / TERCERO
```

La superacion de la base del modulo no puede omitirse por haber confirmado previamente A Grande, B Grande o C Grande.

## 13.2 Caso numerico canonico 1-A-B-C

Supuesto:

```text
Modulo = 20 puntos
1 descendente = 25 puntos
A = +4 puntos
B = -4,25 puntos
C = +25 puntos
```

Lectura obligatoria:

```text
1
-> A Grande
-> B Grande confirmada
-> C Grande
```

Como C recorre 25 puntos y supera la base o inicio del modulo de 20 puntos:

```text
C supera base del modulo
-> CUT
-> nuevo 1
-> reset inmediato del ciclo
```

El nuevo `1` nace en el movimiento que produce el CUT. Desde ese momento se recalculan modulo, extremos y referencias para el nuevo ciclo.

## 13.3 C Grande que no alcanza la base del modulo

Ejemplo:

```text
Modulo = 20 puntos
C Grande = 7 puntos
```

Resultado:

```text
C Grande confirmada
CUT = no
RESET = no
```

La lectura permanece abierta. C Grande no se convierte en CUT solo por existir o por cambiar posteriormente de direccion.

## 13.4 Cambio de direccion posterior a C Grande

Después de una C Grande que no ha alcanzado CUT, si el precio cambia de direccion y vuelve a superar la referencia de B Grande, el Arbol debe evaluar dos ramas excluyentes segun velocidad:

```text
C Grande
-> cambio de direccion
-> supera B Grande
-> evaluar VELOCIDAD
```

### Rama rapida

```text
SI movimiento = rapido:
    CUT
    posible TT
```

El TT solo se confirma si el nuevo recorrido alcanza como minimo el 100 % de la referencia Fibonacci activa.

```text
SI recorrido >= 100 %:
    TT confirmado
    nuevo 1
    reset inmediato
SINO:
    TT posible
    sin reset por TT
```

### Rama lenta

```text
SI movimiento = lento:
    TERCERO
    NO CUT
```

Despues de confirmar TERCERO, la secuencia modular continua obligatoriamente con:

```text
TERCERO
-> A
-> B
-> C
-> aplicar de nuevo todas las ramas AUT / CUT / TT / reset que correspondan
```

## 13.5 Alcance de la regla de velocidad

La bifurcacion `rapido = CUT` frente a `lento = TERCERO` se aplica especialmente cuando toda la secuencia ocurre dentro de una sola vela:

```text
A
-> B
-> C Grande
-> cambio de direccion
-> superacion de la referencia de B Grande
```

El color y el OHLC final de la vela no deciden la rama. La clasificacion depende del orden de ticks y de las variables de velocidad.

Las formulas matematicas definitivas de velocidad se incorporaran posteriormente. Hasta entonces el Arbol debe conservar dos escenarios si la velocidad no puede demostrarse:

```text
ESCENARIO 1: rapido -> CUT -> posible TT
ESCENARIO 2: lento -> TERCERO -> A -> B -> C
```

No se permite elegir una rama por intuicion visual.

## 13.6 Separacion obligatoria de movimientos y patrones

La salida siempre debe separar:

```text
MOVIMIENTOS:
1, 2, TERCERO, A, B, C, AUT, CUT

PATRONES:
TT, FT
```

Ejemplo rapido:

```text
MOVIMIENTOS:
1 -> A Grande -> B Grande -> C Grande -> CUT -> nuevo 1

PATRONES:
TT posible
TT confirmado solo al 100 %
```

Ejemplo lento:

```text
MOVIMIENTOS:
1 -> A Grande -> B Grande -> C Grande -> TERCERO -> A -> B -> C

PATRONES:
Sin TT mientras no exista la transicion correspondiente y no alcance el 100 %
```

## 13.7 Orden obligatorio del motor tras B Grande

```text
1. B Grande confirmada.
2. Movimiento contrario posterior = C Grande.
3. Medir C respecto a la base/inicio del modulo.
4. Si C supera la base del modulo:
      evaluar CUT y crear nuevo 1 con reset.
5. Si C no supera la base:
      mantener C Grande.
6. Si despues C cambia de direccion y el nuevo movimiento supera B Grande:
      evaluar velocidad.
7. Si rapido:
      CUT + posible TT.
8. Si lento:
      TERCERO, no CUT.
9. Si el posible TT alcanza 100 %:
      TT confirmado + nuevo 1 + reset.
10. Despues de TERCERO:
      recorrer A -> B -> C desde la nueva secuencia.
```

## 13.8 Prohibiciones nuevas

1. Detener la lectura en C Grande sin comprobar la base del modulo.
2. Omitir CUT cuando C supera la base o inicio del modulo.
3. Omitir el nuevo 1 y el reset posteriores al CUT estructural.
4. Llamar CUT a todo cambio de direccion posterior a C Grande.
5. Llamar TERCERO a un movimiento rapido.
6. Llamar CUT a un movimiento lento.
7. Confirmar TT sin alcanzar el 100 %.
8. Olvidar la secuencia A -> B -> C posterior a TERCERO.
9. Elegir rapidez o lentitud por apariencia, cuerpo o color de vela.
10. Mezclar la medida de B, la base del modulo y el 100 % del TT.

## 13.9 Variables de velocidad pendientes de matematizacion

La estructura cualitativa queda cerrada:

```text
rapido -> CUT -> posible TT
lento -> TERCERO -> A -> B -> C
```

Queda pendiente definir matematicamente las variables y umbrales de velocidad. Hasta su cierre, el motor debe:

1. calcular y conservar las variables disponibles;
2. no inventar el umbral;
3. mantener ambos escenarios cuando la velocidad no sea demostrable;
4. solicitar decision experta solo para la rama de velocidad, sin bloquear ramas independientes.

## 13.10 Casos minimos de regresion

### TEST-C-001: C supera modulo

```text
Modulo = 20
A = 4
B = 4,25
C = 25
Esperado:
1 -> A Grande -> B Grande -> C Grande -> CUT -> nuevo 1 -> reset
```

### TEST-C-002: C no supera modulo

```text
Modulo = 20
A = 4
B = 4,25
C = 7
Esperado:
1 -> A Grande -> B Grande -> C Grande
CUT = no
reset = no
```

### TEST-C-003: retorno rapido posterior a C

```text
C Grande no alcanza base del modulo
cambio de direccion
nuevo recorrido supera B Grande
velocidad = rapida
Esperado:
CUT + TT posible
TT confirmado solo si alcanza 100 %
```

### TEST-C-004: retorno lento posterior a C

```text
C Grande no alcanza base del modulo
cambio de direccion
nuevo recorrido supera B Grande
velocidad = lenta
Esperado:
TERCERO
CUT = no
Despues: A -> B -> C
```

## 13.11 Invariante v1.2

> Despues de B Grande, el movimiento contrario es C Grande. C debe compararse siempre con la base del modulo. Si C supera esa base, activa CUT, nuevo 1 y reset. Si C no la supera y posteriormente cambia de direccion superando B Grande, la velocidad decide: rapido produce CUT y posible TT; lento produce TERCERO, tras el cual comienza A-B-C. Ningun TT se confirma antes del 100 %.


---

# ANEXO 6 - FUENTE INTEGRA: `TM_DECISIONES_EXPERTO_v0_1.md`

- **SHA-256:** `10e79b4d5f85e1378c873f063e5134df7c2de46f3e50be5beb2ee57d9d7271e1`
- **Integridad:** contenido incorporado sin recortes.

# TM - DECISIONES EXPERTO

## Plantilla normativa

Cada decisión cerrada incluirá:

- ID
- fecha
- pregunta y contexto
- respuesta literal de Javier
- regla general extraída
- fronteras (<, =, >)
- estados afectados
- tests asociados
- estado: CERRADA

## Decisiones cerradas incorporadas inicialmente

### D-0001 B candidata / B confirmada / AUT

- Antes del 100 % de A Grande: B Grande candidata.
- Al alcanzar 100 % sin superar 127 % + 0,25: B Grande confirmada.
- Al superar 127 % + 0,25: deja de ser B Grande y se confirma AUT inmediatamente.

### D-0002 C tras B confirmada

Una vez B Grande está confirmada, cualquier movimiento posterior contrario a B Grande es C Grande, no C Grande candidata.

### D-0003 gap y 2

Al abrir vela se evalúa primero gap. Si hay gap, no hay 2. Sin gap, una cola observable superior a 0,25 antes de confirmar 2 impide 2.

### D-0004 caso vela 3

La vela 3 del caso validado es TT de la vela 2. Al alcanzar el 100 %, TT queda confirmado y vela 3 pasa a nuevo 1. No se añaden A/B/AUT propios sin otra lectura demostrada.


---

# ANEXO 7 - FUENTE INTEGRA: `TM_DUDAS_PENDIENTES_JAVIER.md`

- **SHA-256:** `261d68af1b30999280915262ab90828e0148056720659aa51053fc9d11cfabe2`
- **Integridad:** contenido incorporado sin recortes.

# TM — DUDAS PENDIENTES DE JAVIER

- **Documento:** `control/TM_DUDAS_PENDIENTES_JAVIER.md`
- **Versión:** 1.0
- **Fecha:** 2026-10-19
- **Autoridad:** Javier Armada López
- **Estado:** BLOQUE 1 — 5 preguntas bloqueantes.
- **Regla:** máximo 5 preguntas por bloque. No se avanza en las ramas dependientes hasta recibir respuesta.
- **Referencia:** `TM_ARBOL_CANONICO_COMPLETO_v1.md`.

---

## BLOQUE 1 — 5 PREGUNTAS BLOQUEANTES

### DUDA-J01 — Apertura de L2 y L3

**Nodo afectado:** N-028, N-029.  
**Pregunta:** ¿Qué regla TM expresa autoriza abrir una segunda o tercera lectura?

- **A)** Una vela que alcanza AUT puede abrir automáticamente L2 como nuevo 1 local / TT pequeño, aunque no haya corrección de módulo. L3 se abre solo si las tres lecturas siguen siendo matemáticamente válidas.
- **B)** L2/L3 solo se abren por reclasificación expresa de módulo o 1 conjunto; una vela con AUT no abre L2 por sí sola.
- **C)** Solo Javier identifica la segunda/tercera lectura escena por escena; no existe regla automática de apertura.

**Consecuencia de A:** la lectura pequeña de la vela 3 (TT `29187,40`) sería L2 y podría convivir con L1.  
**Consecuencia de B:** la lectura pequeña queda como movimiento interno de L1 hasta que exista reclasificación; no se declara L2.  
**Consecuencia de C:** el motor no abre L2/L3; toda segunda lectura queda `PENDIENTE_JAVIER`.

**Estado:** `PENDIENTE_JAVIER`.

---

### DUDA-J02 — Composición general del módulo

**Nodo afectado:** N-012.  
**Pregunta:** ¿La composición general del módulo es siempre 1+2 o admite otros casos?

- **A)** Siempre 1+2; el módulo por descarte de la vela anterior no es regla general.
- **B)** Puede ser de una sola vela o de la vela anterior por descarte, con su A Grande contraria, cuando no hay módulo claro.
- **C)** Depende de la escena; Javier debe indicar en cada caso qué velas forman el módulo.

**Consecuencia de A:** H17 queda como provisional y no se implementa módulo por descarte.  
**Consecuencia de B:** se cierra la regla general del módulo y se puede calcular TT en todos los casos.  
**Consecuencia de C:** todo módulo no regular queda `PENDIENTE_JAVIER`.

**Estado:** `PENDIENTE_JAVIER` (DUDA-009 / H17).

---

### DUDA-J03 — Prioridad cuando dos o tres lecturas alcanzan nivel en el mismo tick

**Nodo afectado:** N-030.  
**Pregunta:** Si L1, L2 y L3 alcanzan un nivel en el mismo tick, ¿qué lectura prevalece?

- **A)** Prevalece L1 por ser la lectura de referencia; L2/L3 se resuelven después.
- **B)** Prevalece la lectura con mayor coherencia matemática, aunque no sea L1; si hay empate, se conservan todas.
- **C)** No hay prioridad automática: las tres se registran y Javier resuelve la escena.

**Consecuencia de A:** L1 bloquea a L2/L3 en el mismo tick; puede perder una lectura válida.  
**Consecuencia de B:** se necesita una definición exacta de “mayor coherencia” y desempate.  
**Consecuencia de C:** el motor no decide; la escena queda `PENDIENTE_JAVIER`.

**Estado:** `PENDIENTE_JAVIER` (P5).

---

### DUDA-J04 — Condición exacta de `C = nuevo 1`

**Nodo afectado:** N-025, N-034.  
**Pregunta:** ¿Cuándo se confirma que C Grande, sin alcanzar CUT, pasa a ser nuevo 1?

- **A)** C se convierte en nuevo 1 cuando cierra la referencia de B/A sin superar el final de A y el precio continúa en la dirección de C.
- **B)** C se convierte en nuevo 1 solo cuando alcanza una referencia de expansión propia, no por el simple cierre de la referencia anterior.
- **C)** C = nuevo 1 solo se reconoce por escena, después de que Javier lo valide; no hay condición automática.

**Consecuencia de A:** se puede cerrar la rama C sin CUT con una regla de cierre.  
**Consecuencia de B:** hace falta fijar la referencia de expansión propia de C.  
**Consecuencia de C:** `C = nuevo 1` queda `PENDIENTE_JAVIER` y no se implementa.

**Estado:** `PENDIENTE_JAVIER` (H1 / PR-e).

---

### DUDA-J05 — Regla matemática completa de FT

**Nodo afectado:** N-026.  
**Pregunta:** ¿Qué condiciones exactas confirman FT después de un TT?

- **A)** FT se confirma cuando, tras TT, hay pérdida de velocidad y un movimiento contrario que supera el final de A o una referencia TM explícita.
- **B)** FT se confirma por un retroceso mínimo medido en puntos o porcentaje del último recorrido, además de la pérdida de velocidad.
- **C)** FT solo se reconoce por escena; no se fija una fórmula general todavía.

**Consecuencia de A:** se necesita definir “pérdida de velocidad” y la referencia exacta.  
**Consecuencia de B:** se necesitan umbrales numéricos y ventana de medición.  
**Consecuencia de C:** FT queda fuera del motor determinista y se marca `PENDIENTE_JAVIER`.

**Estado:** `PENDIENTE_JAVIER` (P6).

---

## COLA NO ENVIADA — DUDAS SECUNDARIAS

Estas dudas no forman parte del bloque de 5 y no deben enviarse hasta cerrar el bloque anterior.

- `DUDA-S01` — Umbral numérico entre ruido y movimiento TM (PR-g).
- `DUDA-S02` — ¿Un gap a favor de 1 confirma AUT o solo deja TT pendiente? (N-003).
- `DUDA-S03` — Tick exacto de confirmación de A/B/C Grande (P3).
- `DUDA-S04` — Serie de precio definitiva: Bid/Ask/Last/medio (P2).
- `DUDA-S05` — TT: ¿alcanzar exactamente el 100 % o exigir superación estricta? (N-039).

---

## CONTROL DE RESPUESTAS

| Duda | Respuesta de Javier | Fecha | Decisión | Nodos desbloqueados |
|---|---|---|---|---|
| DUDA-J01 |  |  |  | N-028, N-029 |
| DUDA-J02 |  |  |  | N-012 |
| DUDA-J03 |  |  |  | N-030 |
| DUDA-J04 |  |  |  | N-025, N-034 |
| DUDA-J05 |  |  |  | N-026 |


---

# ANEXO 8 - FUENTE INTEGRA: `TM_ARBOL_MAESTRO_CANONICO_v0_8_B_CANDIDATA_MODULO_ABAUT.md`

- **SHA-256:** `d97d91b3bde8a8cf0b8c22a3aaee0616e07724b6b3a2f60ddd98a298ac4f26ac`
- **Integridad:** contenido incorporado sin recortes.

# TM · ÁRBOL MAESTRO CANÓNICO

Versión 0.5 MEGA BORRADOR. Cobertura global para prueba, preguntas y corrección. No apto todavía para ejecución automática ni para operar.

## 0. Regla constitucional

```text
CLASIFICACIÓN VÁLIDA = lectura + estado anterior + cronología + referencia + precondiciones + transición + resultado.
Si falta una pieza, el motor registra HECHO_SIN_REGLA y no inventa una función. En la versión final HECHO_SIN_REGLA deberá ser cero.
```

## 1. Leyenda de certeza

- CONFIRMADO_JAVIER: regla expresamente cerrada por Javier.

- DOCUMENTADO: aparece en fuentes, pendiente de prueba experta.

- PROPUESTA_CONTROLADA: cierre técnico provisional para poder probar el árbol completo.

- PENDIENTE_JAVIER: pregunta concreta, no programable.

- PROHIBIDO: transición incompatible con las precondiciones.

## 2. Ontología completa provisional

```text
FUNCIONES: 1 | 2 | 3 | A | B | AUT | C
PATRONES: TT | FT
ESTRUCTURAS: MÓDULO | LECTURA
EVENTOS: GAP | AUTOCORTE | CUT | OBJETIVO_TT | CONFIRMACIÓN_FT
CALIFICADORES INTERNOS: CANDIDATO | CONFIRMADO | CANCELADO | RECLASIFICADO | INTEGRADO
```

## 3. Datos mínimos por tick

- timestamp

- bid/ask o precio de referencia acordado

- OHLC de vela activa

- Open actual y Close anterior

- dirección y extremo de cada lectura

- niveles 0, 50, 100, 127 y 127+0,25

- objetivo TT

- referencia CUT

- referencia FT

- historial inmutable de eventos

## 4. Orden universal de evaluación

```text
1. Registrar tick.
2. Detectar nueva vela.
3. Si nueva vela, evaluar GAP antes de 2.
4. Actualizar extremos de cada lectura.
5. Detectar niveles cruzados en el tick.
6. Procesar todos los niveles cruzados en orden geométrico.
7. Aplicar transición por lectura, sin mezclar referencias.
8. Abrir lectura adicional solo por regla expresa.
9. Registrar reclasificación sin borrar historial.
10. Emitir etiqueta visible y trazabilidad.
```

## 5. Árbol raíz y nacimiento de lectura

### TM-ROOT-001 · Sin lectura activa

**Estado:** `PROPUESTA_CONTROLADA`

```text
ORIGEN: SIN_LECTURA
EVENTO: primer recorrido observable
PRECONDICIONES: datos suficientes y referencia inicial autorizada
SI SE CUMPLE: abrir L1 con 1 candidato
SI NO SE CUMPLE: seguir acumulando ticks
DESTINO: UNO_CANDIDATO
PROHIBICIONES: no inventar dirección por color de vela
PRUEBAS: inicio alcista; inicio bajista; vela incompleta
PREGUNTA: Q-001: regla matemática definitiva de nacimiento del primer 1
```

### TM-ROOT-002 · Nueva lectura adicional

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: L1/L2 activa
EVENTO: posible recorrido independiente
PRECONDICIONES: regla explícita de apertura
SI SE CUMPLE: abrir primer slot libre
SI NO SE CUMPLE: integrar en lecturas existentes
DESTINO: Ln activa
PROHIBICIONES: abrir por apariencia visual
PRUEBAS: caso abre L2; caso no abre L2
PREGUNTA: Q-002: catálogo completo de reglas que abren L2/L3
```

## 6. Estado 1

### TM-1-001 · 1 continúa

**Estado:** `PROPUESTA_CONTROLADA`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: extensión en dirección de 1
PRECONDICIONES: no nace función posterior
SI SE CUMPLE: actualizar extremo y rango de 1
SI NO SE CUMPLE: mantener extremo
DESTINO: UNO_CONFIRMADO
PROHIBICIONES: crear otro 1 por cada vela
PRUEBAS: extensión misma vela; varias velas
```

### TM-1-002 · Apertura siguiente con gap

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: Open actual != Close anterior
PRECONDICIONES: nueva vela
SI SE CUMPLE: prohibir 2 y saltar a árbol GAP
SI NO SE CUMPLE: n/a
DESTINO: GAP_EVALUADO
PROHIBICIONES: evaluar plano o 2
PRUEBAS: gap 1 tick; gap varios puntos
```

### TM-1-003 · Sin gap y salida en plano

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: Open actual = Close anterior
PRECONDICIONES: nueva vela y sin cola observable >0,25 antes de objetivo
SI SE CUMPLE: abrir DOS_CANDIDATO
SI NO SE CUMPLE: si hay cola, prohibir 2
DESTINO: DOS_CANDIDATO
PROHIBICIONES: confirmar 2 solo por color
PRUEBAS: plano exacto; cola 0,25; cola 0,50
```

### TM-1-004 · No 2 por cola

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: cola de base >0,25 antes de confirmar 2
PRECONDICIONES: sin gap
SI SE CUMPLE: cancelar 2 y evaluar ruta A
SI NO SE CUMPLE: si cola <=0,25 mantener candidato
DESTINO: A_CANDIDATA
PROHIBICIONES: recrear 2 después
PRUEBAS: cola antes/después del objetivo
```

### TM-1-005 · No 2 por gap

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: gap cualquiera
PRECONDICIONES: nueva vela
SI SE CUMPLE: 2 prohibido
SI NO SE CUMPLE: n/a
DESTINO: RUTA_GAP
PROHIBICIONES: llamar 2 al recorrido posterior
PRUEBAS: gap a favor; gap contrario
```

## 7. Estado 2

### TM-2-001 · 2 candidato progresa

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: avance en dirección de 1
PRECONDICIONES: sin invalidación previa
SI SE CUMPLE: actualizar recorrido 2
SI NO SE CUMPLE: mantener
DESTINO: DOS_CANDIDATO
PROHIBICIONES: confirmar antes de medida
PRUEBAS: <100; =100; >100
PREGUNTA: Q-003: medida exacta y anclajes de 2
```

### TM-2-002 · 2 confirmado

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: alcanza medida exigida
PRECONDICIONES: plano, sin gap, sin cola invalidante previa
SI SE CUMPLE: confirmar 2
SI NO SE CUMPLE: seguir candidato
DESTINO: DOS_CONFIRMADO
PROHIBICIONES: borrar 2 por hechos posteriores
PRUEBAS: frontera exacta y salto
```

### TM-2-003 · Retroceso después de confirmar 2

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: DOS_CONFIRMADO
EVENTO: movimiento contrario
PRECONDICIONES: 2 ya confirmado
SI SE CUMPLE: conservar 2 y abrir evaluación de 3
SI NO SE CUMPLE: n/a
DESTINO: TRES_CANDIDATO
PROHIBICIONES: borrar 2
PRUEBAS: retroceso pequeño; grande
```

### TM-2-004 · Cambio de vela con 2 candidato

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: cierra vela sin confirmar
PRECONDICIONES: no hubo invalidación
SI SE CUMPLE: conservar/cancelar según decisión
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir cancelación
PRUEBAS: varias velas
PREGUNTA: Q-004: 2 puede confirmarse en varias velas
```

## 8. Estado 3 y módulo

### TM-3-001 · Retroceso válido para 3

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CONFIRMADO
EVENTO: retroceso dentro de franja válida
PRECONDICIONES: 2 confirmado
SI SE CUMPLE: seguir TRES_CANDIDATO
SI NO SE CUMPLE: fallar 3
DESTINO: TRES_CANDIDATO
PROHIBICIONES: anticipar 3
PRUEBAS: 0; 50; >50
PREGUNTA: Q-005: límites exactos del retroceso de 3
```

### TM-3-002 · 3 confirmado

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_CANDIDATO
EVENTO: precio retoma dirección de 2 y supera/toca extremo
PRECONDICIONES: retroceso válido
SI SE CUMPLE: confirmar 3
SI NO SE CUMPLE: mantener candidato
DESTINO: TRES_CONFIRMADO
PROHIBICIONES: confirmar por color
PRUEBAS: toca; supera 1 tick
PREGUNTA: Q-006: tocar o superar extremo de 2
```

### TM-3-003 · 3 falla

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_CANDIDATO
EVENTO: incumple regla de 3
PRECONDICIONES: 1 y 2 confirmados
SI SE CUMPLE: consolidar 1+2 como módulo y opuesto como A Grande
SI NO SE CUMPLE: seguir 3
DESTINO: MODULO_CONFIRMADO + A
PROHIBICIONES: crear módulo si nunca hubo 2
PRUEBAS: fallo por profundidad; fallo temporal
```

### TM-3-004 · 3 confirmado y continuidad

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: TRES_CONFIRMADO
EVENTO: extensión posterior
PRECONDICIONES: 3 confirmado
SI SE CUMPLE: definir siguiente estructura
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir A automáticamente
PRUEBAS: extensión/giro
PREGUNTA: Q-007: consecuencia exacta después de 3
```

## 9. Módulo y A

### TM-MOD-001 · Módulo 1+2

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_FALLIDO
EVENTO: opuesto tras fallo de 3
PRECONDICIONES: 1 y 2 confirmados
SI SE CUMPLE: fijar rango del módulo y A Grande
SI NO SE CUMPLE: n/a
DESTINO: A_EN_CURSO
PROHIBICIONES: formar módulo sin 2
PRUEBAS: caso estándar
```

### TM-MOD-002 · Módulo reclasificado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: varios movimientos previos
EVENTO: retroceso posterior permite integración
PRECONDICIONES: regla de reclasificación satisfecha
SI SE CUMPLE: crear módulo conjunto conservando eventos
SI NO SE CUMPLE: mantener lecturas
DESTINO: MODULO_RECLASIFICADO
PROHIBICIONES: borrar eventos
PRUEBAS: varias velas
PREGUNTA: Q-008: catálogo completo de reclasificación
```

### TM-A-001 · A se extiende

**Estado:** `DOCUMENTADO`

```text
ORIGEN: A_EN_CURSO
EVENTO: nuevo extremo en dirección de A
PRECONDICIONES: sin B opuesta confirmable
SI SE CUMPLE: actualizar final y rango de A
SI NO SE CUMPLE: mantener
DESTINO: A_EN_CURSO
PROHIBICIONES: congelar A demasiado pronto
PRUEBAS: extensión 1 tick/multivela
```

### TM-A-002 · Nace B candidata

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: A_EN_CURSO
EVENTO: movimiento contrario a A
PRECONDICIONES: A posee inicio/final/rango
SI SE CUMPLE: abrir B candidata
SI NO SE CUMPLE: mantener A
DESTINO: B_CANDIDATA
PROHIBICIONES: llamar B confirmada antes del 100
PRUEBAS: retorno 10/99/100
```

## 10. B candidata, B confirmada y AUT

### TM-B-001 · B por debajo del 100 %

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: avance <100 % de A
PRECONDICIONES: B opuesta a A
SI SE CUMPLE: seguir B candidata
SI NO SE CUMPLE: n/a
DESTINO: B_CANDIDATA
PROHIBICIONES: llamar B Grande
PRUEBAS: 99,75 %
```

### TM-B-002 · B alcanza 100 %

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: alcanza 100 %
PRECONDICIONES: no supera 127 %+0,25
SI SE CUMPLE: confirmar B Grande
SI NO SE CUMPLE: seguir candidata
DESTINO: B_CONFIRMADA
PROHIBICIONES: exigir cierre
PRUEBAS: 100 exacto
```

### TM-B-003 · B entre 100 y límite AUT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CONFIRMADA
EVENTO: extensión sin superar 127 %+0,25
PRECONDICIONES: B confirmó 100
SI SE CUMPLE: mantener B confirmada
SI NO SE CUMPLE: n/a
DESTINO: B_CONFIRMADA
PROHIBICIONES: llamar AUT
PRUEBAS: 110;127; límite exacto
```

### TM-B-004 · B supera límite AUT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B candidata o confirmada
EVENTO: supera 127 %+0,25
PRECONDICIONES: A válida
SI SE CUMPLE: dejar B y confirmar AUT inmediato
SI NO SE CUMPLE: mantener B
DESTINO: AUT_CONFIRMADO
PROHIBICIONES: esperar otra vela
PRUEBAS: salto directo 90→130
```

### TM-B-005 · Giro de B candidata antes del 100

**Estado historico:** `SUPERADO_POR_PATCH_v2.2`

> La oscilacion interna ya no cancela ni divide B. Aplicar la seccion 0.2. El texto historico inferior se conserva solo por trazabilidad.

**Estado anterior:** `PENDIENTE_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: precio vuelve hacia A
PRECONDICIONES: B <100
SI SE CUMPLE: aplicar decisión experta
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: llamar C
PRUEBAS: giro 20/80/99
PREGUNTA: Q-009: absorción, nueva A o reclasificación
```

### TM-B-006 · B confirmada gira

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CONFIRMADA
EVENTO: movimiento contrario a B
PRECONDICIONES: B alcanzó 100 sin AUT
SI SE CUMPLE: clasificar C inmediatamente
SI NO SE CUMPLE: n/a
DESTINO: C_EN_CURSO
PROHIBICIONES: llamar C candidata
PRUEBAS: giro 1 tick
```

## 11. C y CUT

### TM-C-001 · C se extiende

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: C_EN_CURSO
EVENTO: avance en dirección contraria a B
PRECONDICIONES: B confirmada misma lectura
SI SE CUMPLE: actualizar C
SI NO SE CUMPLE: n/a
DESTINO: C_EN_CURSO
PROHIBICIONES: usar B de otra lectura
PRUEBAS: avance parcial
```

### TM-C-002 · CUT

**Estado:** `DOCUMENTADO`

```text
ORIGEN: C_EN_CURSO
EVENTO: C alcanza final de A
PRECONDICIONES: misma lectura
SI SE CUMPLE: confirmar CUT
SI NO SE CUMPLE: seguir C
DESTINO: CUT_CONFIRMADO
PROHIBICIONES: confirmar por color
PRUEBAS: toca/supera
PREGUNTA: Q-010: CUT evento o función; tocar o superar
```

### TM-C-003 · C no alcanza CUT y gira

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: C_EN_CURSO
EVENTO: movimiento vuelve hacia B
PRECONDICIONES: C < final A
SI SE CUMPLE: aplicar decisión experta
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: inventar función
PRUEBAS: múltiples profundidades
PREGUNTA: Q-011: tratamiento completo de C sin CUT
```

### TM-C-004 · Después de CUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: CUT_CONFIRMADO
EVENTO: continuidad o giro
PRECONDICIONES: CUT confirmado
SI SE CUMPLE: definir siguiente lectura
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: cerrar todo automáticamente
PRUEBAS: continúa/gira
PREGUNTA: Q-012: consecuencia posterior a CUT
```

## 12. AUT y TT

### TM-AUT-001 · AUT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B candidata o confirmada
EVENTO: supera 127 %+0,25
PRECONDICIONES: A válida
SI SE CUMPLE: activar TT posible
SI NO SE CUMPLE: n/a
DESTINO: TT_POSIBLE
PROHIBICIONES: mantener B vigente
PRUEBAS: salto multinivel
```

### TM-TT-001 · TT progresa

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: TT_POSIBLE
EVENTO: expansión desde final A hacia objetivo
PRECONDICIONES: AUT misma lectura
SI SE CUMPLE: actualizar porcentaje
SI NO SE CUMPLE: n/a
DESTINO: TT_POSIBLE
PROHIBICIONES: llamar TT confirmado
PRUEBAS: 1–99,75 %
```

### TM-TT-002 · TT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: TT_POSIBLE
EVENTO: alcanza 100 %
PRECONDICIONES: objetivo = final A ± rango módulo
SI SE CUMPLE: confirmar TT y convertir recorrido culminante en nuevo 1
SI NO SE CUMPLE: seguir posible
DESTINO: TT_CONFIRMADO + UNO_CONFIRMADO
PROHIBICIONES: crear A/B/AUT propios sin lectura
PRUEBAS: 100 exacto/salto
```

### TM-TT-003 · TT falla antes del 100

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TT_POSIBLE
EVENTO: precio toca/corta final A antes de objetivo
PRECONDICIONES: AUT activo
SI SE CUMPLE: cancelar TT y aplicar reclasificación
SI NO SE CUMPLE: mantener TT
DESTINO: TT_FALLIDO
PROHIBICIONES: borrar AUT
PRUEBAS: fallo temprano/tardío
PREGUNTA: Q-013: condición exacta de fallo TT
```

### TM-TT-004 · AUT, 1 y TT pequeño simultáneos

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: AUT_CONFIRMADO
EVENTO: recorrido cumple referencias concurrentes
PRECONDICIONES: lecturas explícitas
SI SE CUMPLE: registrar todos por lectura
SI NO SE CUMPLE: n/a
DESTINO: ESTADOS_CONCURRENTES
PROHIBICIONES: fusionar etiquetas
PRUEBAS: caso simultáneo
```

## 13. FT

### TM-FT-001 · FT prohibido sin TT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: cualquier
EVENTO: movimiento contrario
PRECONDICIONES: TT no confirmado
SI SE CUMPLE: no FT
SI NO SE CUMPLE: n/a
DESTINO: SIN_FT
PROHIBICIONES: anticipar FT
PRUEBAS: caso negativo
```

### TM-FT-002 · FT candidato

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TT_CONFIRMADO
EVENTO: movimiento contrario claro
PRECONDICIONES: TT confirmado y posible pérdida de velocidad
SI SE CUMPLE: abrir FT candidato
SI NO SE CUMPLE: integrar micromovimiento
DESTINO: FT_CANDIDATO
PROHIBICIONES: confirmar por color
PRUEBAS: mismo minuto/multivela
PREGUNTA: Q-014: umbral matemático de movimiento claro y pérdida de velocidad
```

### TM-FT-003 · FT confirmado

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: FT_CANDIDATO
EVENTO: alcanza referencia FT
PRECONDICIONES: precondiciones completas
SI SE CUMPLE: confirmar FT
SI NO SE CUMPLE: mantener candidato
DESTINO: FT_CONFIRMADO
PROHIBICIONES: usar referencia no definida
PRUEBAS: frontera
PREGUNTA: Q-015: objetivo, inicio, cancelación y confirmación FT
```

### TM-FT-004 · Después de FT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: FT_CONFIRMADO
EVENTO: continuidad/giro
PRECONDICIONES: FT confirmado
SI SE CUMPLE: definir nuevo ciclo
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir nuevo 1
PRUEBAS: dos direcciones
PREGUNTA: Q-016: consecuencia posterior a FT
```

## 14. Árbol completo de gap

### TM-GAP-001 · Gap a favor de 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: Open avanza en dirección de 1
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: RUTA_GAP_FAVOR
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-017: funciones implícitas exactas
```

### TM-GAP-002 · Gap contrario a 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: Open avanza contra 1
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: A_INICIADA_POR_GAP
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-018: anclajes exactos de A por gap
```

### TM-GAP-003 · Gap cruza 100 de B

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura atraviesa nivel 100
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: B_CONFIRMADA_O_AUT
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-019: orden de niveles implícitos
```

### TM-GAP-004 · Gap cruza AUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura supera 127 %+0,25
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: AUT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-020: AUT por gap y objetivo TT
```

### TM-GAP-005 · Gap cruza objetivo TT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura supera objetivo 100 TT
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: TT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-021: confirmación inmediata y precio de nuevo 1
```

### TM-GAP-006 · Gap cruza CUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura cruza final de A durante C
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: CUT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-022: CUT por gap
```

### TM-GAP-007 · Gap cruza nivel FT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura cruza referencia FT
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: FT_CONFIRMADO_O_PENDIENTE
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-023: FT por gap
```

## 15. Saltos multinivel en un tick

```text
REGLA PROPUESTA: si un tick salta varios umbrales, registrar todos los umbrales causales atravesados en orden, pero dejar como estado vigente el último estado válido. No exigir permanencia de un tick en estados intermedios.
```

- B candidata → AUT: cruza 100 y AUT.

- TT posible → más allá del objetivo: cruza 100 TT.

- C → más allá de CUT: cruza final A.

- 2 candidato → extremo y retroceso: orden intratick no observable.

La última combinación exige política de datos cuando dos precios extremos aparecen sin orden intratick fiable: `PENDIENTE_JAVIER` y no reconstrucción inventada.

## 16. Concurrencia L1/L2/L3

### TM-CON-001 · Actualizar lecturas

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: 1–3 lecturas activas
EVENTO: nuevo tick
PRECONDICIONES: cada lectura conserva referencias
SI SE CUMPLE: evaluar el tick en todas por separado
SI NO SE CUMPLE: n/a
DESTINO: lecturas actualizadas
PROHIBICIONES: mezclar niveles
PRUEBAS: dos eventos simultáneos
```

### TM-CON-002 · Abrir lectura

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lecturas activas
EVENTO: evento de apertura
PRECONDICIONES: regla expresa
SI SE CUMPLE: crear Ln con padre/regla/tick
SI NO SE CUMPLE: no abrir
DESTINO: Ln
PROHIBICIONES: abrir por apariencia
PRUEBAS: L2/L3
PREGUNTA: Q-024: lista exhaustiva de disparadores
```

### TM-CON-003 · Capacidad máxima

**Estado:** `DOCUMENTADO`

```text
ORIGEN: L1/L2 activas
EVENTO: tercera posibilidad
PRECONDICIONES: excepcional y justificada
SI SE CUMPLE: abrir L3
SI NO SE CUMPLE: integrar/invalidar
DESTINO: L3 o no
PROHIBICIONES: más de 3
PRUEBAS: tres lecturas
PREGUNTA: Q-025: máximo absoluto y prioridad
```

### TM-CON-004 · Mismo movimiento en dos lecturas

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: L1/L2
EVENTO: un recorrido cumple papeles distintos
PRECONDICIONES: referencias separadas
SI SE CUMPLE: registrar ambos papeles
SI NO SE CUMPLE: n/a
DESTINO: doble etiqueta por lectura
PROHIBICIONES: fusionar lecturas
PRUEBAS: TT L1 y 1 L2
```

### TM-CON-005 · Cerrar/integrar lectura

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: múltiples lecturas
EVENTO: convergencia o incompatibilidad
PRECONDICIONES: regla de integración
SI SE CUMPLE: marcar integrada/invalidada conservando historial
SI NO SE CUMPLE: mantener
DESTINO: LECTURA_CERRADA
PROHIBICIONES: borrar
PRUEBAS: casos variados
PREGUNTA: Q-026: criterios exhaustivos de cierre
```

## 17. Reclasificación

### TM-REC-001 · Velas previas pasan a módulo

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: retroceso revela 1+2 conjunto
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-027: condiciones exactas
```

### TM-REC-002 · Velas previas pasan a 1 conjunto

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: retroceso revela unidad mayor
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-028: condiciones exactas
```

### TM-REC-003 · Movimiento candidato absorbido

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: no alcanza confirmación y retorna
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-029: reglas por estado
```

### TM-REC-004 · AUT simultáneo con 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: AUT cumple nacimiento de 1
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-030: referencias
```

### TM-REC-005 · TT pequeño dentro de TT mayor

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: módulos anidados
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-031: anidamiento y prioridad
```

### TM-REC-006 · Lectura alternativa pasa a principal

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: evidencia posterior
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-032: criterio de prioridad
```

## 18. Cambio de vela

```text
La frontera temporal no crea por sí sola una función. Al abrir vela: registrar cierre, apertura, gap y lecturas. Las funciones pueden comenzar en una vela y terminar en otras. TT y FT pueden coexistir dentro de una misma vela si las referencias se alcanzan cronológicamente.
```

- Cambio de vela con `1`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `2 candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `2 confirmado`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `3 candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `A`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `B candidata`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `B confirmada`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `AUT/TT posible`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `C`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `FT candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

## 19. Transiciones prohibidas

- C sin B confirmada en la misma lectura.

- CUT sin C válida.

- TT sin AUT.

- TT confirmado antes del 100 %.

- FT sin TT confirmado.

- 2 con gap.

- 2 con cola >0,25 previa a confirmación.

- B confirmada antes del 100 %.

- Mantener B después de superar AUT.

- Abrir L2/L3 sin regla expresa.

- Mezclar el A de L1 con el B de L2.

- Borrar historia al reclasificar.

- Inferir orden intravela usando solo OHLC cuando el orden afecta la etiqueta.

- Usar color de vela como fundamento funcional.

- Llamar ruido a un movimiento no resuelto para ocultar una rama ausente.

## 20. Matriz de cobertura de eventos

### Cobertura SIN_LECTURA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 1

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 2_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 2_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 3_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 3_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura MÓDULO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura A

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura B_CANDIDATA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura B_CONFIRMADA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura AUT

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_POSIBLE

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_FALLIDO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura C

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura CUT

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura FT_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura FT_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

## 21. Casos mínimos de prueba obligatorios

- `SIN_LECTURA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `1`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `2_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `2_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `3_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `3_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `MÓDULO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `A`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `B_CANDIDATA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `B_CONFIRMADA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `AUT`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_POSIBLE`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_FALLIDO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `C`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `CUT`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `FT_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `FT_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

## 22. Registro maestro de preguntas

Preguntas explícitas detectadas: Q-001 a Q-032. Además, la matriz de cobertura puede generar preguntas adicionales durante los tests. Las preguntas se resolverán después del primer test global, una por una, y cada respuesta actualizará regla, nodo y pruebas.

## 23. Criterio de promoción a v1

```text
PENDIENTE_JAVIER = 0
PROPUESTA_CONTROLADA no aprobada = 0
CONTRADICCIONES = 0
CELDAS SIN SALIDA = 0
TESTS FALLIDOS = 0
TRANSICIONES SIN PRECONDICIÓN = 0
LECTURAS ABIERTAS SIN REGLA = 0
```

## 24. Correccion experta incorporada durante pruebas

### TEST-TM-INTRAVELA-001 - Vela 20-7-7

**Estado:** `CONFIRMADO_JAVIER`

```text
UNA UNICA VELA:
1. Sube 20 puntos -> 1.
2. Por descarte -> MODULO.
3. Retrocede 7 puntos -> A.
4. Recupera 7 puntos hasta el maximo -> B al 100 % de A.
5. B queda confirmada.
6. No hay AUT porque no supera 127 % + 0,25.

SECUENCIA CANONICA:
1 -> MODULO_POR_DESCARTE -> A -> B_CONFIRMADA_100
```

**Correccion del arbol:** queda prohibido omitir el modulo por descarte en esta secuencia y saltar directamente de 1 a A.

---

## 24. Protocolo obligatorio de escenarios completos

### TM-ESC-001 · Enumeración total antes de responder

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: cualquier lectura TM activa
EVENTO: solicitud de clasificación de una o varias velas
PRECONDICIONES: recorrer el árbol completo, incluidas concurrencia y reclasificación
SI SE CUMPLE: enumerar todos los escenarios TM válidos compatibles con los ticks
SI NO SE CUMPLE: respuesta inválida e incompleta
DESTINO: RESPUESTA_TM_COMPLETA
PROHIBICIONES: responder solo con el escenario principal; ocultar escenarios coexistentes; inventar escenarios
PRUEBAS: caso con 1 escenario; caso con 2 escenarios; caso excepcional con 3 escenarios
```

### TM-ESC-002 · Número máximo de escenarios

**Estado:** `CONFIRMADO_JAVIER`

```text
REGLA: una respuesta TM puede contener como máximo 3 escenarios válidos.
FRECUENCIA ESPERADA: normalmente habrá 1 o 2 escenarios.
ESCENARIO 3: solo se mostrará cuando el recorrido completo del árbol lo sostenga.
PROHIBICIÓN: forzar siempre 3 escenarios.
```

### TM-ESC-003 · Orden obligatorio de respuesta

**Estado:** `CONFIRMADO_JAVIER`

```text
1. Recorrer el árbol principal.
2. Recorrer concurrencia.
3. Recorrer reclasificación.
4. Detectar funciones simultáneas de una misma vela.
5. Detectar funciones conjuntas de varias velas.
6. Eliminar escenarios incompatibles con los ticks.
7. Mostrar todos los escenarios supervivientes, numerados del 1 al 3.
```

### TM-ESC-004 · Formato obligatorio

**Estado:** `CONFIRMADO_JAVIER`

```text
ESCENARIO 1:
- secuencia TM completa

ESCENARIO 2:
- secuencia TM completa

ESCENARIO 3:
- secuencia TM completa, solo si existe

LECTURA COMÚN:
- hechos TM compartidos por todos los escenarios
```

### TM-ESC-005 · Caso validado 23:39–23:41

**Estado:** `CONFIRMADO_JAVIER`

```text
LECTURA COMÚN:
23:39 = 1 alcista.
23:40 = A + B + AUT; abre TT posible alcista.
23:41 alcanza el objetivo del TT y es nuevo 1.

ESCENARIO 1:
23:40 abre el TT posible y 23:41 lo culmina.
23:41 = TT confirmado + nuevo 1.

ESCENARIO 2:
23:40 y 23:41 forman conjuntamente el TT del 1 de 23:39.
23:41 = culminación del TT conjunto + nuevo 1.

PROHIBICIÓN:
No responder únicamente con uno de los dos escenarios.
```

### TM-ESC-006 · Regla de validez de respuesta

**Estado:** `CONFIRMADO_JAVIER`

```text
Una respuesta es VÁLIDA solo si:
- ha recorrido el árbol completo;
- ha comprobado escenarios concurrentes;
- incluye todos los escenarios compatibles;
- no supera 3 escenarios;
- no confunde número de vela con función TM.

Si falta un escenario válido, la respuesta se considera INCORRECTA aunque el escenario mostrado sea verdadero.
```

---

## 25. Regla obligatoria FT inmediatamente posterior a TT

### TM-FT-005 · Giro claro desde el extremo de un TT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN:
TT confirmado.

EVENTO:
Desde el extremo que culmina el TT aparece una bajada o subida contraria clara y relevante.

PRECONDICIONES:
1. El TT anterior está confirmado.
2. El movimiento nace desde el extremo final del TT.
3. El movimiento va en sentido contrario al TT.
4. El desarrollo contrario es claro y tiene recorrido observable.

RESULTADO OBLIGATORIO:
El movimiento contrario se clasifica como FT del TT anterior.

CONCURRENCIA:
El mismo movimiento puede ser simultáneamente:
- FT del TT anterior; y
- A de un nuevo módulo por descarte nacido en el extremo.

PROHIBICIONES:
- Omitir FT por atender solo la nueva lectura modular.
- Responder únicamente A cuando también existe FT.
- Exigir otra vela para reconocer el FT si ya es claro en la vela actual.
- Borrar la referencia del TT al comenzar la nueva lectura.

CONTROL DE RESPUESTA:
Después de cada TT confirmado, el árbol debe preguntar obligatoriamente:
"¿Desde el extremo del TT aparece un movimiento contrario claro y relevante?"
Sí -> incluir FT en todos los escenarios compatibles.
No -> no inventar FT.
```

### TM-FT-006 · Caso de regresión, vela 5 desde 23:39

**Estado:** `CONFIRMADO_JAVIER`

```text
CONTEXTO:
Vela 5 = 23:43.
La vela 5 culmina el TT alcista anterior y marca un máximo aproximado de 29192,10.
Después baja hasta aproximadamente 29185,60.
Recorrido contrario aproximado: 6,50 puntos.

LECTURA OBLIGATORIA:
1. Culminación del TT alcista anterior.
2. Nuevo 1 en la vela 5.
3. En el máximo: módulo por descarte.
4. Bajada desde el máximo: A bajista de la nueva lectura.
5. Simultáneamente: FT bajista del TT alcista anterior.

ERROR DE REGRESIÓN:
La respuesta falla si menciona A bajista pero omite FT bajista.
```

### TM-FT-007 · Comprobación sistemática posterior a TT

**Estado:** `CONFIRMADO_JAVIER`

```text
Cada vez que se confirme un TT:
1. Conservar la referencia y el extremo del TT.
2. Analizar todos los ticks posteriores desde ese extremo.
3. Buscar movimiento contrario claro y relevante.
4. Si existe, activar FT.
5. En paralelo, recorrer módulo por descarte, A, B y demás lecturas nuevas.
6. Mostrar ambas lecturas si coexisten.

La detección del FT no puede quedar anulada por el nacimiento de un nuevo 1,
un módulo por descarte o una A concurrente.
```

---

## 26. B candidata que cruza de vela y funciona simultaneamente como modulo

### TM-CONC-008 · Persistencia de B candidata tras cambio de vela

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN:
Existe una A Grande confirmada y ha comenzado un movimiento contrario
clasificado como B candidata.

EVENTO:
Cambia la vela antes de que la B candidata alcance su frontera de confirmacion.

RESULTADO OBLIGATORIO:
El cambio de vela no cancela, reinicia ni confirma por si mismo la B candidata.
La lectura principal conserva:
A Grande -> B candidata pendiente.

CONTROL DE APERTURA:
Al abrir la nueva vela se evalua primero el gap.
El gap se registra dentro de la cronologia, pero no borra la B candidata heredada.
```

### TM-CONC-009 · La B candidata heredada puede ser modulo de una segunda lectura

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN LECTURA 1:
A Grande -> B candidata pendiente que continua en la vela siguiente.

CONDICION DE APERTURA DE LECTURA 2:
La subida o bajada que constituye la B candidata heredada puede tomarse,
simultaneamente y sin borrar la lectura 1, como modulo por descarte de una nueva lectura.

EVENTO:
En la nueva vela, despues del gap, el precio retrocede en sentido contrario
a ese modulo.

RESULTADO:
Se mantienen dos lecturas concurrentes:

LECTURA 1:
A Grande anterior -> B candidata pendiente.

LECTURA 2:
B candidata de lectura 1 = modulo por descarte.
Retroceso posterior = A de lectura 2.
Movimiento contrario posterior = B de lectura 2.
Si esa B supera 127 % + 0,25 puntos de A, deja de ser B y confirma AUT.

PROHIBICIONES:
- Cancelar la B candidata solo porque cambio la vela.
- Considerar que el gap crea por si solo la A de la lectura 2.
- Borrar la lectura 1 al abrir la lectura 2.
- Llamar B Grande a la B de lectura 2 despues de superar 127 % + 0,25.
- Omitir AUT cuando la frontera haya sido superada.
```

### TM-CONC-010 · Caso de regresion velas 5 y 6, 23:43-23:44

**Estado:** `CONFIRMADO_JAVIER`

```text
VELA 5 - 23:43:
Maximo inicial: 29192,10.
Minimo posterior: 29185,60.
Bajada: A Grande bajista y, simultaneamente, FT bajista del TT anterior.
Desde 29185,60 comienza una subida clasificada como B candidata alcista.

CAMBIO A VELA 6 - 23:44:
Cierre previo aproximado: 29189,30.
Apertura nueva: 29189,70.
Gap alcista aproximado: +0,40.
La B candidata de la lectura 1 continua pendiente.

LECTURA 2:
La subida que era B candidata en la lectura 1 funciona tambien como modulo.
En la vela 6 aparece un retroceso hasta 29188,80: A bajista de lectura 2.
Desde 29188,80 nace B alcista de lectura 2.
La subida posterior supera la frontera 127 % + 0,25 de esa A
y confirma AUT alcista.

SALIDA OBLIGATORIA:
LECTURA 1: A Grande bajista -> B candidata alcista pendiente/continua.
LECTURA 2: modulo -> A bajista -> B alcista -> AUT alcista.

ERROR DE REGRESION:
La respuesta falla si:
1. borra la B candidata al cambiar de vela;
2. no abre la lectura modular concurrente;
3. atribuye la A al gap en vez de al retroceso posterior;
4. omite la secuencia A -> B -> AUT de la segunda lectura.
```


---

# ANEXO 9 - FUENTE INTEGRA: `TM_ARBOL_MAESTRO_CANONICO_v0_7_FT_POST_TT (1).md`

- **SHA-256:** `6e1d45824d8426feaca0d9c92a526e626e300f564b165587d04fe368a20d0246`
- **Integridad:** contenido incorporado sin recortes.

# TM · ÁRBOL MAESTRO CANÓNICO

Versión 0.5 MEGA BORRADOR. Cobertura global para prueba, preguntas y corrección. No apto todavía para ejecución automática ni para operar.

## 0. Regla constitucional

```text
CLASIFICACIÓN VÁLIDA = lectura + estado anterior + cronología + referencia + precondiciones + transición + resultado.
Si falta una pieza, el motor registra HECHO_SIN_REGLA y no inventa una función. En la versión final HECHO_SIN_REGLA deberá ser cero.
```

## 1. Leyenda de certeza

- CONFIRMADO_JAVIER: regla expresamente cerrada por Javier.

- DOCUMENTADO: aparece en fuentes, pendiente de prueba experta.

- PROPUESTA_CONTROLADA: cierre técnico provisional para poder probar el árbol completo.

- PENDIENTE_JAVIER: pregunta concreta, no programable.

- PROHIBIDO: transición incompatible con las precondiciones.

## 2. Ontología completa provisional

```text
FUNCIONES: 1 | 2 | 3 | A | B | AUT | C
PATRONES: TT | FT
ESTRUCTURAS: MÓDULO | LECTURA
EVENTOS: GAP | AUTOCORTE | CUT | OBJETIVO_TT | CONFIRMACIÓN_FT
CALIFICADORES INTERNOS: CANDIDATO | CONFIRMADO | CANCELADO | RECLASIFICADO | INTEGRADO
```

## 3. Datos mínimos por tick

- timestamp

- bid/ask o precio de referencia acordado

- OHLC de vela activa

- Open actual y Close anterior

- dirección y extremo de cada lectura

- niveles 0, 50, 100, 127 y 127+0,25

- objetivo TT

- referencia CUT

- referencia FT

- historial inmutable de eventos

## 4. Orden universal de evaluación

```text
1. Registrar tick.
2. Detectar nueva vela.
3. Si nueva vela, evaluar GAP antes de 2.
4. Actualizar extremos de cada lectura.
5. Detectar niveles cruzados en el tick.
6. Procesar todos los niveles cruzados en orden geométrico.
7. Aplicar transición por lectura, sin mezclar referencias.
8. Abrir lectura adicional solo por regla expresa.
9. Registrar reclasificación sin borrar historial.
10. Emitir etiqueta visible y trazabilidad.
```

## 5. Árbol raíz y nacimiento de lectura

### TM-ROOT-001 · Sin lectura activa

**Estado:** `PROPUESTA_CONTROLADA`

```text
ORIGEN: SIN_LECTURA
EVENTO: primer recorrido observable
PRECONDICIONES: datos suficientes y referencia inicial autorizada
SI SE CUMPLE: abrir L1 con 1 candidato
SI NO SE CUMPLE: seguir acumulando ticks
DESTINO: UNO_CANDIDATO
PROHIBICIONES: no inventar dirección por color de vela
PRUEBAS: inicio alcista; inicio bajista; vela incompleta
PREGUNTA: Q-001: regla matemática definitiva de nacimiento del primer 1
```

### TM-ROOT-002 · Nueva lectura adicional

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: L1/L2 activa
EVENTO: posible recorrido independiente
PRECONDICIONES: regla explícita de apertura
SI SE CUMPLE: abrir primer slot libre
SI NO SE CUMPLE: integrar en lecturas existentes
DESTINO: Ln activa
PROHIBICIONES: abrir por apariencia visual
PRUEBAS: caso abre L2; caso no abre L2
PREGUNTA: Q-002: catálogo completo de reglas que abren L2/L3
```

## 6. Estado 1

### TM-1-001 · 1 continúa

**Estado:** `PROPUESTA_CONTROLADA`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: extensión en dirección de 1
PRECONDICIONES: no nace función posterior
SI SE CUMPLE: actualizar extremo y rango de 1
SI NO SE CUMPLE: mantener extremo
DESTINO: UNO_CONFIRMADO
PROHIBICIONES: crear otro 1 por cada vela
PRUEBAS: extensión misma vela; varias velas
```

### TM-1-002 · Apertura siguiente con gap

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: Open actual != Close anterior
PRECONDICIONES: nueva vela
SI SE CUMPLE: prohibir 2 y saltar a árbol GAP
SI NO SE CUMPLE: n/a
DESTINO: GAP_EVALUADO
PROHIBICIONES: evaluar plano o 2
PRUEBAS: gap 1 tick; gap varios puntos
```

### TM-1-003 · Sin gap y salida en plano

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: Open actual = Close anterior
PRECONDICIONES: nueva vela y sin cola observable >0,25 antes de objetivo
SI SE CUMPLE: abrir DOS_CANDIDATO
SI NO SE CUMPLE: si hay cola, prohibir 2
DESTINO: DOS_CANDIDATO
PROHIBICIONES: confirmar 2 solo por color
PRUEBAS: plano exacto; cola 0,25; cola 0,50
```

### TM-1-004 · No 2 por cola

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: cola de base >0,25 antes de confirmar 2
PRECONDICIONES: sin gap
SI SE CUMPLE: cancelar 2 y evaluar ruta A
SI NO SE CUMPLE: si cola <=0,25 mantener candidato
DESTINO: A_CANDIDATA
PROHIBICIONES: recrear 2 después
PRUEBAS: cola antes/después del objetivo
```

### TM-1-005 · No 2 por gap

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: gap cualquiera
PRECONDICIONES: nueva vela
SI SE CUMPLE: 2 prohibido
SI NO SE CUMPLE: n/a
DESTINO: RUTA_GAP
PROHIBICIONES: llamar 2 al recorrido posterior
PRUEBAS: gap a favor; gap contrario
```

## 7. Estado 2

### TM-2-001 · 2 candidato progresa

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: avance en dirección de 1
PRECONDICIONES: sin invalidación previa
SI SE CUMPLE: actualizar recorrido 2
SI NO SE CUMPLE: mantener
DESTINO: DOS_CANDIDATO
PROHIBICIONES: confirmar antes de medida
PRUEBAS: <100; =100; >100
PREGUNTA: Q-003: medida exacta y anclajes de 2
```

### TM-2-002 · 2 confirmado

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: alcanza medida exigida
PRECONDICIONES: plano, sin gap, sin cola invalidante previa
SI SE CUMPLE: confirmar 2
SI NO SE CUMPLE: seguir candidato
DESTINO: DOS_CONFIRMADO
PROHIBICIONES: borrar 2 por hechos posteriores
PRUEBAS: frontera exacta y salto
```

### TM-2-003 · Retroceso después de confirmar 2

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: DOS_CONFIRMADO
EVENTO: movimiento contrario
PRECONDICIONES: 2 ya confirmado
SI SE CUMPLE: conservar 2 y abrir evaluación de 3
SI NO SE CUMPLE: n/a
DESTINO: TRES_CANDIDATO
PROHIBICIONES: borrar 2
PRUEBAS: retroceso pequeño; grande
```

### TM-2-004 · Cambio de vela con 2 candidato

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: cierra vela sin confirmar
PRECONDICIONES: no hubo invalidación
SI SE CUMPLE: conservar/cancelar según decisión
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir cancelación
PRUEBAS: varias velas
PREGUNTA: Q-004: 2 puede confirmarse en varias velas
```

## 8. Estado 3 y módulo

### TM-3-001 · Retroceso válido para 3

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CONFIRMADO
EVENTO: retroceso dentro de franja válida
PRECONDICIONES: 2 confirmado
SI SE CUMPLE: seguir TRES_CANDIDATO
SI NO SE CUMPLE: fallar 3
DESTINO: TRES_CANDIDATO
PROHIBICIONES: anticipar 3
PRUEBAS: 0; 50; >50
PREGUNTA: Q-005: límites exactos del retroceso de 3
```

### TM-3-002 · 3 confirmado

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_CANDIDATO
EVENTO: precio retoma dirección de 2 y supera/toca extremo
PRECONDICIONES: retroceso válido
SI SE CUMPLE: confirmar 3
SI NO SE CUMPLE: mantener candidato
DESTINO: TRES_CONFIRMADO
PROHIBICIONES: confirmar por color
PRUEBAS: toca; supera 1 tick
PREGUNTA: Q-006: tocar o superar extremo de 2
```

### TM-3-003 · 3 falla

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_CANDIDATO
EVENTO: incumple regla de 3
PRECONDICIONES: 1 y 2 confirmados
SI SE CUMPLE: consolidar 1+2 como módulo y opuesto como A Grande
SI NO SE CUMPLE: seguir 3
DESTINO: MODULO_CONFIRMADO + A
PROHIBICIONES: crear módulo si nunca hubo 2
PRUEBAS: fallo por profundidad; fallo temporal
```

### TM-3-004 · 3 confirmado y continuidad

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: TRES_CONFIRMADO
EVENTO: extensión posterior
PRECONDICIONES: 3 confirmado
SI SE CUMPLE: definir siguiente estructura
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir A automáticamente
PRUEBAS: extensión/giro
PREGUNTA: Q-007: consecuencia exacta después de 3
```

## 9. Módulo y A

### TM-MOD-001 · Módulo 1+2

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_FALLIDO
EVENTO: opuesto tras fallo de 3
PRECONDICIONES: 1 y 2 confirmados
SI SE CUMPLE: fijar rango del módulo y A Grande
SI NO SE CUMPLE: n/a
DESTINO: A_EN_CURSO
PROHIBICIONES: formar módulo sin 2
PRUEBAS: caso estándar
```

### TM-MOD-002 · Módulo reclasificado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: varios movimientos previos
EVENTO: retroceso posterior permite integración
PRECONDICIONES: regla de reclasificación satisfecha
SI SE CUMPLE: crear módulo conjunto conservando eventos
SI NO SE CUMPLE: mantener lecturas
DESTINO: MODULO_RECLASIFICADO
PROHIBICIONES: borrar eventos
PRUEBAS: varias velas
PREGUNTA: Q-008: catálogo completo de reclasificación
```

### TM-A-001 · A se extiende

**Estado:** `DOCUMENTADO`

```text
ORIGEN: A_EN_CURSO
EVENTO: nuevo extremo en dirección de A
PRECONDICIONES: sin B opuesta confirmable
SI SE CUMPLE: actualizar final y rango de A
SI NO SE CUMPLE: mantener
DESTINO: A_EN_CURSO
PROHIBICIONES: congelar A demasiado pronto
PRUEBAS: extensión 1 tick/multivela
```

### TM-A-002 · Nace B candidata

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: A_EN_CURSO
EVENTO: movimiento contrario a A
PRECONDICIONES: A posee inicio/final/rango
SI SE CUMPLE: abrir B candidata
SI NO SE CUMPLE: mantener A
DESTINO: B_CANDIDATA
PROHIBICIONES: llamar B confirmada antes del 100
PRUEBAS: retorno 10/99/100
```

## 10. B candidata, B confirmada y AUT

### TM-B-001 · B por debajo del 100 %

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: avance <100 % de A
PRECONDICIONES: B opuesta a A
SI SE CUMPLE: seguir B candidata
SI NO SE CUMPLE: n/a
DESTINO: B_CANDIDATA
PROHIBICIONES: llamar B Grande
PRUEBAS: 99,75 %
```

### TM-B-002 · B alcanza 100 %

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: alcanza 100 %
PRECONDICIONES: no supera 127 %+0,25
SI SE CUMPLE: confirmar B Grande
SI NO SE CUMPLE: seguir candidata
DESTINO: B_CONFIRMADA
PROHIBICIONES: exigir cierre
PRUEBAS: 100 exacto
```

### TM-B-003 · B entre 100 y límite AUT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CONFIRMADA
EVENTO: extensión sin superar 127 %+0,25
PRECONDICIONES: B confirmó 100
SI SE CUMPLE: mantener B confirmada
SI NO SE CUMPLE: n/a
DESTINO: B_CONFIRMADA
PROHIBICIONES: llamar AUT
PRUEBAS: 110;127; límite exacto
```

### TM-B-004 · B supera límite AUT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B candidata o confirmada
EVENTO: supera 127 %+0,25
PRECONDICIONES: A válida
SI SE CUMPLE: dejar B y confirmar AUT inmediato
SI NO SE CUMPLE: mantener B
DESTINO: AUT_CONFIRMADO
PROHIBICIONES: esperar otra vela
PRUEBAS: salto directo 90→130
```

### TM-B-005 · Giro de B candidata antes del 100

**Estado historico:** `SUPERADO_POR_PATCH_v2.2`

> La oscilacion interna ya no cancela ni divide B. Aplicar la seccion 0.2. El texto historico inferior se conserva solo por trazabilidad.

**Estado anterior:** `PENDIENTE_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: precio vuelve hacia A
PRECONDICIONES: B <100
SI SE CUMPLE: aplicar decisión experta
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: llamar C
PRUEBAS: giro 20/80/99
PREGUNTA: Q-009: absorción, nueva A o reclasificación
```

### TM-B-006 · B confirmada gira

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CONFIRMADA
EVENTO: movimiento contrario a B
PRECONDICIONES: B alcanzó 100 sin AUT
SI SE CUMPLE: clasificar C inmediatamente
SI NO SE CUMPLE: n/a
DESTINO: C_EN_CURSO
PROHIBICIONES: llamar C candidata
PRUEBAS: giro 1 tick
```

## 11. C y CUT

### TM-C-001 · C se extiende

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: C_EN_CURSO
EVENTO: avance en dirección contraria a B
PRECONDICIONES: B confirmada misma lectura
SI SE CUMPLE: actualizar C
SI NO SE CUMPLE: n/a
DESTINO: C_EN_CURSO
PROHIBICIONES: usar B de otra lectura
PRUEBAS: avance parcial
```

### TM-C-002 · CUT

**Estado:** `DOCUMENTADO`

```text
ORIGEN: C_EN_CURSO
EVENTO: C alcanza final de A
PRECONDICIONES: misma lectura
SI SE CUMPLE: confirmar CUT
SI NO SE CUMPLE: seguir C
DESTINO: CUT_CONFIRMADO
PROHIBICIONES: confirmar por color
PRUEBAS: toca/supera
PREGUNTA: Q-010: CUT evento o función; tocar o superar
```

### TM-C-003 · C no alcanza CUT y gira

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: C_EN_CURSO
EVENTO: movimiento vuelve hacia B
PRECONDICIONES: C < final A
SI SE CUMPLE: aplicar decisión experta
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: inventar función
PRUEBAS: múltiples profundidades
PREGUNTA: Q-011: tratamiento completo de C sin CUT
```

### TM-C-004 · Después de CUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: CUT_CONFIRMADO
EVENTO: continuidad o giro
PRECONDICIONES: CUT confirmado
SI SE CUMPLE: definir siguiente lectura
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: cerrar todo automáticamente
PRUEBAS: continúa/gira
PREGUNTA: Q-012: consecuencia posterior a CUT
```

## 12. AUT y TT

### TM-AUT-001 · AUT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B candidata o confirmada
EVENTO: supera 127 %+0,25
PRECONDICIONES: A válida
SI SE CUMPLE: activar TT posible
SI NO SE CUMPLE: n/a
DESTINO: TT_POSIBLE
PROHIBICIONES: mantener B vigente
PRUEBAS: salto multinivel
```

### TM-TT-001 · TT progresa

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: TT_POSIBLE
EVENTO: expansión desde final A hacia objetivo
PRECONDICIONES: AUT misma lectura
SI SE CUMPLE: actualizar porcentaje
SI NO SE CUMPLE: n/a
DESTINO: TT_POSIBLE
PROHIBICIONES: llamar TT confirmado
PRUEBAS: 1–99,75 %
```

### TM-TT-002 · TT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: TT_POSIBLE
EVENTO: alcanza 100 %
PRECONDICIONES: objetivo = final A ± rango módulo
SI SE CUMPLE: confirmar TT y convertir recorrido culminante en nuevo 1
SI NO SE CUMPLE: seguir posible
DESTINO: TT_CONFIRMADO + UNO_CONFIRMADO
PROHIBICIONES: crear A/B/AUT propios sin lectura
PRUEBAS: 100 exacto/salto
```

### TM-TT-003 · TT falla antes del 100

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TT_POSIBLE
EVENTO: precio toca/corta final A antes de objetivo
PRECONDICIONES: AUT activo
SI SE CUMPLE: cancelar TT y aplicar reclasificación
SI NO SE CUMPLE: mantener TT
DESTINO: TT_FALLIDO
PROHIBICIONES: borrar AUT
PRUEBAS: fallo temprano/tardío
PREGUNTA: Q-013: condición exacta de fallo TT
```

### TM-TT-004 · AUT, 1 y TT pequeño simultáneos

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: AUT_CONFIRMADO
EVENTO: recorrido cumple referencias concurrentes
PRECONDICIONES: lecturas explícitas
SI SE CUMPLE: registrar todos por lectura
SI NO SE CUMPLE: n/a
DESTINO: ESTADOS_CONCURRENTES
PROHIBICIONES: fusionar etiquetas
PRUEBAS: caso simultáneo
```

## 13. FT

### TM-FT-001 · FT prohibido sin TT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: cualquier
EVENTO: movimiento contrario
PRECONDICIONES: TT no confirmado
SI SE CUMPLE: no FT
SI NO SE CUMPLE: n/a
DESTINO: SIN_FT
PROHIBICIONES: anticipar FT
PRUEBAS: caso negativo
```

### TM-FT-002 · FT candidato

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TT_CONFIRMADO
EVENTO: movimiento contrario claro
PRECONDICIONES: TT confirmado y posible pérdida de velocidad
SI SE CUMPLE: abrir FT candidato
SI NO SE CUMPLE: integrar micromovimiento
DESTINO: FT_CANDIDATO
PROHIBICIONES: confirmar por color
PRUEBAS: mismo minuto/multivela
PREGUNTA: Q-014: umbral matemático de movimiento claro y pérdida de velocidad
```

### TM-FT-003 · FT confirmado

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: FT_CANDIDATO
EVENTO: alcanza referencia FT
PRECONDICIONES: precondiciones completas
SI SE CUMPLE: confirmar FT
SI NO SE CUMPLE: mantener candidato
DESTINO: FT_CONFIRMADO
PROHIBICIONES: usar referencia no definida
PRUEBAS: frontera
PREGUNTA: Q-015: objetivo, inicio, cancelación y confirmación FT
```

### TM-FT-004 · Después de FT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: FT_CONFIRMADO
EVENTO: continuidad/giro
PRECONDICIONES: FT confirmado
SI SE CUMPLE: definir nuevo ciclo
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir nuevo 1
PRUEBAS: dos direcciones
PREGUNTA: Q-016: consecuencia posterior a FT
```

## 14. Árbol completo de gap

### TM-GAP-001 · Gap a favor de 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: Open avanza en dirección de 1
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: RUTA_GAP_FAVOR
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-017: funciones implícitas exactas
```

### TM-GAP-002 · Gap contrario a 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: Open avanza contra 1
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: A_INICIADA_POR_GAP
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-018: anclajes exactos de A por gap
```

### TM-GAP-003 · Gap cruza 100 de B

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura atraviesa nivel 100
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: B_CONFIRMADA_O_AUT
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-019: orden de niveles implícitos
```

### TM-GAP-004 · Gap cruza AUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura supera 127 %+0,25
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: AUT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-020: AUT por gap y objetivo TT
```

### TM-GAP-005 · Gap cruza objetivo TT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura supera objetivo 100 TT
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: TT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-021: confirmación inmediata y precio de nuevo 1
```

### TM-GAP-006 · Gap cruza CUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura cruza final de A durante C
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: CUT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-022: CUT por gap
```

### TM-GAP-007 · Gap cruza nivel FT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura cruza referencia FT
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: FT_CONFIRMADO_O_PENDIENTE
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-023: FT por gap
```

## 15. Saltos multinivel en un tick

```text
REGLA PROPUESTA: si un tick salta varios umbrales, registrar todos los umbrales causales atravesados en orden, pero dejar como estado vigente el último estado válido. No exigir permanencia de un tick en estados intermedios.
```

- B candidata → AUT: cruza 100 y AUT.

- TT posible → más allá del objetivo: cruza 100 TT.

- C → más allá de CUT: cruza final A.

- 2 candidato → extremo y retroceso: orden intratick no observable.

La última combinación exige política de datos cuando dos precios extremos aparecen sin orden intratick fiable: `PENDIENTE_JAVIER` y no reconstrucción inventada.

## 16. Concurrencia L1/L2/L3

### TM-CON-001 · Actualizar lecturas

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: 1–3 lecturas activas
EVENTO: nuevo tick
PRECONDICIONES: cada lectura conserva referencias
SI SE CUMPLE: evaluar el tick en todas por separado
SI NO SE CUMPLE: n/a
DESTINO: lecturas actualizadas
PROHIBICIONES: mezclar niveles
PRUEBAS: dos eventos simultáneos
```

### TM-CON-002 · Abrir lectura

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lecturas activas
EVENTO: evento de apertura
PRECONDICIONES: regla expresa
SI SE CUMPLE: crear Ln con padre/regla/tick
SI NO SE CUMPLE: no abrir
DESTINO: Ln
PROHIBICIONES: abrir por apariencia
PRUEBAS: L2/L3
PREGUNTA: Q-024: lista exhaustiva de disparadores
```

### TM-CON-003 · Capacidad máxima

**Estado:** `DOCUMENTADO`

```text
ORIGEN: L1/L2 activas
EVENTO: tercera posibilidad
PRECONDICIONES: excepcional y justificada
SI SE CUMPLE: abrir L3
SI NO SE CUMPLE: integrar/invalidar
DESTINO: L3 o no
PROHIBICIONES: más de 3
PRUEBAS: tres lecturas
PREGUNTA: Q-025: máximo absoluto y prioridad
```

### TM-CON-004 · Mismo movimiento en dos lecturas

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: L1/L2
EVENTO: un recorrido cumple papeles distintos
PRECONDICIONES: referencias separadas
SI SE CUMPLE: registrar ambos papeles
SI NO SE CUMPLE: n/a
DESTINO: doble etiqueta por lectura
PROHIBICIONES: fusionar lecturas
PRUEBAS: TT L1 y 1 L2
```

### TM-CON-005 · Cerrar/integrar lectura

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: múltiples lecturas
EVENTO: convergencia o incompatibilidad
PRECONDICIONES: regla de integración
SI SE CUMPLE: marcar integrada/invalidada conservando historial
SI NO SE CUMPLE: mantener
DESTINO: LECTURA_CERRADA
PROHIBICIONES: borrar
PRUEBAS: casos variados
PREGUNTA: Q-026: criterios exhaustivos de cierre
```

## 17. Reclasificación

### TM-REC-001 · Velas previas pasan a módulo

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: retroceso revela 1+2 conjunto
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-027: condiciones exactas
```

### TM-REC-002 · Velas previas pasan a 1 conjunto

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: retroceso revela unidad mayor
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-028: condiciones exactas
```

### TM-REC-003 · Movimiento candidato absorbido

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: no alcanza confirmación y retorna
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-029: reglas por estado
```

### TM-REC-004 · AUT simultáneo con 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: AUT cumple nacimiento de 1
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-030: referencias
```

### TM-REC-005 · TT pequeño dentro de TT mayor

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: módulos anidados
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-031: anidamiento y prioridad
```

### TM-REC-006 · Lectura alternativa pasa a principal

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: evidencia posterior
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-032: criterio de prioridad
```

## 18. Cambio de vela

```text
La frontera temporal no crea por sí sola una función. Al abrir vela: registrar cierre, apertura, gap y lecturas. Las funciones pueden comenzar en una vela y terminar en otras. TT y FT pueden coexistir dentro de una misma vela si las referencias se alcanzan cronológicamente.
```

- Cambio de vela con `1`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `2 candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `2 confirmado`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `3 candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `A`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `B candidata`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `B confirmada`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `AUT/TT posible`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `C`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `FT candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

## 19. Transiciones prohibidas

- C sin B confirmada en la misma lectura.

- CUT sin C válida.

- TT sin AUT.

- TT confirmado antes del 100 %.

- FT sin TT confirmado.

- 2 con gap.

- 2 con cola >0,25 previa a confirmación.

- B confirmada antes del 100 %.

- Mantener B después de superar AUT.

- Abrir L2/L3 sin regla expresa.

- Mezclar el A de L1 con el B de L2.

- Borrar historia al reclasificar.

- Inferir orden intravela usando solo OHLC cuando el orden afecta la etiqueta.

- Usar color de vela como fundamento funcional.

- Llamar ruido a un movimiento no resuelto para ocultar una rama ausente.

## 20. Matriz de cobertura de eventos

### Cobertura SIN_LECTURA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 1

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 2_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 2_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 3_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 3_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura MÓDULO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura A

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura B_CANDIDATA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura B_CONFIRMADA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura AUT

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_POSIBLE

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_FALLIDO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura C

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura CUT

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura FT_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura FT_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

## 21. Casos mínimos de prueba obligatorios

- `SIN_LECTURA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `1`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `2_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `2_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `3_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `3_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `MÓDULO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `A`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `B_CANDIDATA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `B_CONFIRMADA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `AUT`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_POSIBLE`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_FALLIDO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `C`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `CUT`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `FT_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `FT_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

## 22. Registro maestro de preguntas

Preguntas explícitas detectadas: Q-001 a Q-032. Además, la matriz de cobertura puede generar preguntas adicionales durante los tests. Las preguntas se resolverán después del primer test global, una por una, y cada respuesta actualizará regla, nodo y pruebas.

## 23. Criterio de promoción a v1

```text
PENDIENTE_JAVIER = 0
PROPUESTA_CONTROLADA no aprobada = 0
CONTRADICCIONES = 0
CELDAS SIN SALIDA = 0
TESTS FALLIDOS = 0
TRANSICIONES SIN PRECONDICIÓN = 0
LECTURAS ABIERTAS SIN REGLA = 0
```

## 24. Correccion experta incorporada durante pruebas

### TEST-TM-INTRAVELA-001 - Vela 20-7-7

**Estado:** `CONFIRMADO_JAVIER`

```text
UNA UNICA VELA:
1. Sube 20 puntos -> 1.
2. Por descarte -> MODULO.
3. Retrocede 7 puntos -> A.
4. Recupera 7 puntos hasta el maximo -> B al 100 % de A.
5. B queda confirmada.
6. No hay AUT porque no supera 127 % + 0,25.

SECUENCIA CANONICA:
1 -> MODULO_POR_DESCARTE -> A -> B_CONFIRMADA_100
```

**Correccion del arbol:** queda prohibido omitir el modulo por descarte en esta secuencia y saltar directamente de 1 a A.

---

## 24. Protocolo obligatorio de escenarios completos

### TM-ESC-001 · Enumeración total antes de responder

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: cualquier lectura TM activa
EVENTO: solicitud de clasificación de una o varias velas
PRECONDICIONES: recorrer el árbol completo, incluidas concurrencia y reclasificación
SI SE CUMPLE: enumerar todos los escenarios TM válidos compatibles con los ticks
SI NO SE CUMPLE: respuesta inválida e incompleta
DESTINO: RESPUESTA_TM_COMPLETA
PROHIBICIONES: responder solo con el escenario principal; ocultar escenarios coexistentes; inventar escenarios
PRUEBAS: caso con 1 escenario; caso con 2 escenarios; caso excepcional con 3 escenarios
```

### TM-ESC-002 · Número máximo de escenarios

**Estado:** `CONFIRMADO_JAVIER`

```text
REGLA: una respuesta TM puede contener como máximo 3 escenarios válidos.
FRECUENCIA ESPERADA: normalmente habrá 1 o 2 escenarios.
ESCENARIO 3: solo se mostrará cuando el recorrido completo del árbol lo sostenga.
PROHIBICIÓN: forzar siempre 3 escenarios.
```

### TM-ESC-003 · Orden obligatorio de respuesta

**Estado:** `CONFIRMADO_JAVIER`

```text
1. Recorrer el árbol principal.
2. Recorrer concurrencia.
3. Recorrer reclasificación.
4. Detectar funciones simultáneas de una misma vela.
5. Detectar funciones conjuntas de varias velas.
6. Eliminar escenarios incompatibles con los ticks.
7. Mostrar todos los escenarios supervivientes, numerados del 1 al 3.
```

### TM-ESC-004 · Formato obligatorio

**Estado:** `CONFIRMADO_JAVIER`

```text
ESCENARIO 1:
- secuencia TM completa

ESCENARIO 2:
- secuencia TM completa

ESCENARIO 3:
- secuencia TM completa, solo si existe

LECTURA COMÚN:
- hechos TM compartidos por todos los escenarios
```

### TM-ESC-005 · Caso validado 23:39–23:41

**Estado:** `CONFIRMADO_JAVIER`

```text
LECTURA COMÚN:
23:39 = 1 alcista.
23:40 = A + B + AUT; abre TT posible alcista.
23:41 alcanza el objetivo del TT y es nuevo 1.

ESCENARIO 1:
23:40 abre el TT posible y 23:41 lo culmina.
23:41 = TT confirmado + nuevo 1.

ESCENARIO 2:
23:40 y 23:41 forman conjuntamente el TT del 1 de 23:39.
23:41 = culminación del TT conjunto + nuevo 1.

PROHIBICIÓN:
No responder únicamente con uno de los dos escenarios.
```

### TM-ESC-006 · Regla de validez de respuesta

**Estado:** `CONFIRMADO_JAVIER`

```text
Una respuesta es VÁLIDA solo si:
- ha recorrido el árbol completo;
- ha comprobado escenarios concurrentes;
- incluye todos los escenarios compatibles;
- no supera 3 escenarios;
- no confunde número de vela con función TM.

Si falta un escenario válido, la respuesta se considera INCORRECTA aunque el escenario mostrado sea verdadero.
```

---

## 25. Regla obligatoria FT inmediatamente posterior a TT

### TM-FT-005 · Giro claro desde el extremo de un TT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN:
TT confirmado.

EVENTO:
Desde el extremo que culmina el TT aparece una bajada o subida contraria clara y relevante.

PRECONDICIONES:
1. El TT anterior está confirmado.
2. El movimiento nace desde el extremo final del TT.
3. El movimiento va en sentido contrario al TT.
4. El desarrollo contrario es claro y tiene recorrido observable.

RESULTADO OBLIGATORIO:
El movimiento contrario se clasifica como FT del TT anterior.

CONCURRENCIA:
El mismo movimiento puede ser simultáneamente:
- FT del TT anterior; y
- A de un nuevo módulo por descarte nacido en el extremo.

PROHIBICIONES:
- Omitir FT por atender solo la nueva lectura modular.
- Responder únicamente A cuando también existe FT.
- Exigir otra vela para reconocer el FT si ya es claro en la vela actual.
- Borrar la referencia del TT al comenzar la nueva lectura.

CONTROL DE RESPUESTA:
Después de cada TT confirmado, el árbol debe preguntar obligatoriamente:
"¿Desde el extremo del TT aparece un movimiento contrario claro y relevante?"
Sí -> incluir FT en todos los escenarios compatibles.
No -> no inventar FT.
```

### TM-FT-006 · Caso de regresión, vela 5 desde 23:39

**Estado:** `CONFIRMADO_JAVIER`

```text
CONTEXTO:
Vela 5 = 23:43.
La vela 5 culmina el TT alcista anterior y marca un máximo aproximado de 29192,10.
Después baja hasta aproximadamente 29185,60.
Recorrido contrario aproximado: 6,50 puntos.

LECTURA OBLIGATORIA:
1. Culminación del TT alcista anterior.
2. Nuevo 1 en la vela 5.
3. En el máximo: módulo por descarte.
4. Bajada desde el máximo: A bajista de la nueva lectura.
5. Simultáneamente: FT bajista del TT alcista anterior.

ERROR DE REGRESIÓN:
La respuesta falla si menciona A bajista pero omite FT bajista.
```

### TM-FT-007 · Comprobación sistemática posterior a TT

**Estado:** `CONFIRMADO_JAVIER`

```text
Cada vez que se confirme un TT:
1. Conservar la referencia y el extremo del TT.
2. Analizar todos los ticks posteriores desde ese extremo.
3. Buscar movimiento contrario claro y relevante.
4. Si existe, activar FT.
5. En paralelo, recorrer módulo por descarte, A, B y demás lecturas nuevas.
6. Mostrar ambas lecturas si coexisten.

La detección del FT no puede quedar anulada por el nacimiento de un nuevo 1,
un módulo por descarte o una A concurrente.
```


---

# ANEXO 10 - FUENTE INTEGRA: `TM_ARBOL_MAESTRO_CANONICO_v0_6_ESCENARIOS_COMPLETOS.md`

- **SHA-256:** `6b269b6e90a0b9a01679ea32b98d0a1e191792109655cd84fada9dc16d4342bd`
- **Integridad:** contenido incorporado sin recortes.

# TM · ÁRBOL MAESTRO CANÓNICO

Versión 0.5 MEGA BORRADOR. Cobertura global para prueba, preguntas y corrección. No apto todavía para ejecución automática ni para operar.

## 0. Regla constitucional

```text
CLASIFICACIÓN VÁLIDA = lectura + estado anterior + cronología + referencia + precondiciones + transición + resultado.
Si falta una pieza, el motor registra HECHO_SIN_REGLA y no inventa una función. En la versión final HECHO_SIN_REGLA deberá ser cero.
```

## 1. Leyenda de certeza

- CONFIRMADO_JAVIER: regla expresamente cerrada por Javier.

- DOCUMENTADO: aparece en fuentes, pendiente de prueba experta.

- PROPUESTA_CONTROLADA: cierre técnico provisional para poder probar el árbol completo.

- PENDIENTE_JAVIER: pregunta concreta, no programable.

- PROHIBIDO: transición incompatible con las precondiciones.

## 2. Ontología completa provisional

```text
FUNCIONES: 1 | 2 | 3 | A | B | AUT | C
PATRONES: TT | FT
ESTRUCTURAS: MÓDULO | LECTURA
EVENTOS: GAP | AUTOCORTE | CUT | OBJETIVO_TT | CONFIRMACIÓN_FT
CALIFICADORES INTERNOS: CANDIDATO | CONFIRMADO | CANCELADO | RECLASIFICADO | INTEGRADO
```

## 3. Datos mínimos por tick

- timestamp

- bid/ask o precio de referencia acordado

- OHLC de vela activa

- Open actual y Close anterior

- dirección y extremo de cada lectura

- niveles 0, 50, 100, 127 y 127+0,25

- objetivo TT

- referencia CUT

- referencia FT

- historial inmutable de eventos

## 4. Orden universal de evaluación

```text
1. Registrar tick.
2. Detectar nueva vela.
3. Si nueva vela, evaluar GAP antes de 2.
4. Actualizar extremos de cada lectura.
5. Detectar niveles cruzados en el tick.
6. Procesar todos los niveles cruzados en orden geométrico.
7. Aplicar transición por lectura, sin mezclar referencias.
8. Abrir lectura adicional solo por regla expresa.
9. Registrar reclasificación sin borrar historial.
10. Emitir etiqueta visible y trazabilidad.
```

## 5. Árbol raíz y nacimiento de lectura

### TM-ROOT-001 · Sin lectura activa

**Estado:** `PROPUESTA_CONTROLADA`

```text
ORIGEN: SIN_LECTURA
EVENTO: primer recorrido observable
PRECONDICIONES: datos suficientes y referencia inicial autorizada
SI SE CUMPLE: abrir L1 con 1 candidato
SI NO SE CUMPLE: seguir acumulando ticks
DESTINO: UNO_CANDIDATO
PROHIBICIONES: no inventar dirección por color de vela
PRUEBAS: inicio alcista; inicio bajista; vela incompleta
PREGUNTA: Q-001: regla matemática definitiva de nacimiento del primer 1
```

### TM-ROOT-002 · Nueva lectura adicional

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: L1/L2 activa
EVENTO: posible recorrido independiente
PRECONDICIONES: regla explícita de apertura
SI SE CUMPLE: abrir primer slot libre
SI NO SE CUMPLE: integrar en lecturas existentes
DESTINO: Ln activa
PROHIBICIONES: abrir por apariencia visual
PRUEBAS: caso abre L2; caso no abre L2
PREGUNTA: Q-002: catálogo completo de reglas que abren L2/L3
```

## 6. Estado 1

### TM-1-001 · 1 continúa

**Estado:** `PROPUESTA_CONTROLADA`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: extensión en dirección de 1
PRECONDICIONES: no nace función posterior
SI SE CUMPLE: actualizar extremo y rango de 1
SI NO SE CUMPLE: mantener extremo
DESTINO: UNO_CONFIRMADO
PROHIBICIONES: crear otro 1 por cada vela
PRUEBAS: extensión misma vela; varias velas
```

### TM-1-002 · Apertura siguiente con gap

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: Open actual != Close anterior
PRECONDICIONES: nueva vela
SI SE CUMPLE: prohibir 2 y saltar a árbol GAP
SI NO SE CUMPLE: n/a
DESTINO: GAP_EVALUADO
PROHIBICIONES: evaluar plano o 2
PRUEBAS: gap 1 tick; gap varios puntos
```

### TM-1-003 · Sin gap y salida en plano

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: Open actual = Close anterior
PRECONDICIONES: nueva vela y sin cola observable >0,25 antes de objetivo
SI SE CUMPLE: abrir DOS_CANDIDATO
SI NO SE CUMPLE: si hay cola, prohibir 2
DESTINO: DOS_CANDIDATO
PROHIBICIONES: confirmar 2 solo por color
PRUEBAS: plano exacto; cola 0,25; cola 0,50
```

### TM-1-004 · No 2 por cola

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: cola de base >0,25 antes de confirmar 2
PRECONDICIONES: sin gap
SI SE CUMPLE: cancelar 2 y evaluar ruta A
SI NO SE CUMPLE: si cola <=0,25 mantener candidato
DESTINO: A_CANDIDATA
PROHIBICIONES: recrear 2 después
PRUEBAS: cola antes/después del objetivo
```

### TM-1-005 · No 2 por gap

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: gap cualquiera
PRECONDICIONES: nueva vela
SI SE CUMPLE: 2 prohibido
SI NO SE CUMPLE: n/a
DESTINO: RUTA_GAP
PROHIBICIONES: llamar 2 al recorrido posterior
PRUEBAS: gap a favor; gap contrario
```

## 7. Estado 2

### TM-2-001 · 2 candidato progresa

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: avance en dirección de 1
PRECONDICIONES: sin invalidación previa
SI SE CUMPLE: actualizar recorrido 2
SI NO SE CUMPLE: mantener
DESTINO: DOS_CANDIDATO
PROHIBICIONES: confirmar antes de medida
PRUEBAS: <100; =100; >100
PREGUNTA: Q-003: medida exacta y anclajes de 2
```

### TM-2-002 · 2 confirmado

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: alcanza medida exigida
PRECONDICIONES: plano, sin gap, sin cola invalidante previa
SI SE CUMPLE: confirmar 2
SI NO SE CUMPLE: seguir candidato
DESTINO: DOS_CONFIRMADO
PROHIBICIONES: borrar 2 por hechos posteriores
PRUEBAS: frontera exacta y salto
```

### TM-2-003 · Retroceso después de confirmar 2

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: DOS_CONFIRMADO
EVENTO: movimiento contrario
PRECONDICIONES: 2 ya confirmado
SI SE CUMPLE: conservar 2 y abrir evaluación de 3
SI NO SE CUMPLE: n/a
DESTINO: TRES_CANDIDATO
PROHIBICIONES: borrar 2
PRUEBAS: retroceso pequeño; grande
```

### TM-2-004 · Cambio de vela con 2 candidato

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: cierra vela sin confirmar
PRECONDICIONES: no hubo invalidación
SI SE CUMPLE: conservar/cancelar según decisión
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir cancelación
PRUEBAS: varias velas
PREGUNTA: Q-004: 2 puede confirmarse en varias velas
```

## 8. Estado 3 y módulo

### TM-3-001 · Retroceso válido para 3

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CONFIRMADO
EVENTO: retroceso dentro de franja válida
PRECONDICIONES: 2 confirmado
SI SE CUMPLE: seguir TRES_CANDIDATO
SI NO SE CUMPLE: fallar 3
DESTINO: TRES_CANDIDATO
PROHIBICIONES: anticipar 3
PRUEBAS: 0; 50; >50
PREGUNTA: Q-005: límites exactos del retroceso de 3
```

### TM-3-002 · 3 confirmado

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_CANDIDATO
EVENTO: precio retoma dirección de 2 y supera/toca extremo
PRECONDICIONES: retroceso válido
SI SE CUMPLE: confirmar 3
SI NO SE CUMPLE: mantener candidato
DESTINO: TRES_CONFIRMADO
PROHIBICIONES: confirmar por color
PRUEBAS: toca; supera 1 tick
PREGUNTA: Q-006: tocar o superar extremo de 2
```

### TM-3-003 · 3 falla

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_CANDIDATO
EVENTO: incumple regla de 3
PRECONDICIONES: 1 y 2 confirmados
SI SE CUMPLE: consolidar 1+2 como módulo y opuesto como A Grande
SI NO SE CUMPLE: seguir 3
DESTINO: MODULO_CONFIRMADO + A
PROHIBICIONES: crear módulo si nunca hubo 2
PRUEBAS: fallo por profundidad; fallo temporal
```

### TM-3-004 · 3 confirmado y continuidad

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: TRES_CONFIRMADO
EVENTO: extensión posterior
PRECONDICIONES: 3 confirmado
SI SE CUMPLE: definir siguiente estructura
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir A automáticamente
PRUEBAS: extensión/giro
PREGUNTA: Q-007: consecuencia exacta después de 3
```

## 9. Módulo y A

### TM-MOD-001 · Módulo 1+2

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_FALLIDO
EVENTO: opuesto tras fallo de 3
PRECONDICIONES: 1 y 2 confirmados
SI SE CUMPLE: fijar rango del módulo y A Grande
SI NO SE CUMPLE: n/a
DESTINO: A_EN_CURSO
PROHIBICIONES: formar módulo sin 2
PRUEBAS: caso estándar
```

### TM-MOD-002 · Módulo reclasificado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: varios movimientos previos
EVENTO: retroceso posterior permite integración
PRECONDICIONES: regla de reclasificación satisfecha
SI SE CUMPLE: crear módulo conjunto conservando eventos
SI NO SE CUMPLE: mantener lecturas
DESTINO: MODULO_RECLASIFICADO
PROHIBICIONES: borrar eventos
PRUEBAS: varias velas
PREGUNTA: Q-008: catálogo completo de reclasificación
```

### TM-A-001 · A se extiende

**Estado:** `DOCUMENTADO`

```text
ORIGEN: A_EN_CURSO
EVENTO: nuevo extremo en dirección de A
PRECONDICIONES: sin B opuesta confirmable
SI SE CUMPLE: actualizar final y rango de A
SI NO SE CUMPLE: mantener
DESTINO: A_EN_CURSO
PROHIBICIONES: congelar A demasiado pronto
PRUEBAS: extensión 1 tick/multivela
```

### TM-A-002 · Nace B candidata

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: A_EN_CURSO
EVENTO: movimiento contrario a A
PRECONDICIONES: A posee inicio/final/rango
SI SE CUMPLE: abrir B candidata
SI NO SE CUMPLE: mantener A
DESTINO: B_CANDIDATA
PROHIBICIONES: llamar B confirmada antes del 100
PRUEBAS: retorno 10/99/100
```

## 10. B candidata, B confirmada y AUT

### TM-B-001 · B por debajo del 100 %

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: avance <100 % de A
PRECONDICIONES: B opuesta a A
SI SE CUMPLE: seguir B candidata
SI NO SE CUMPLE: n/a
DESTINO: B_CANDIDATA
PROHIBICIONES: llamar B Grande
PRUEBAS: 99,75 %
```

### TM-B-002 · B alcanza 100 %

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: alcanza 100 %
PRECONDICIONES: no supera 127 %+0,25
SI SE CUMPLE: confirmar B Grande
SI NO SE CUMPLE: seguir candidata
DESTINO: B_CONFIRMADA
PROHIBICIONES: exigir cierre
PRUEBAS: 100 exacto
```

### TM-B-003 · B entre 100 y límite AUT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CONFIRMADA
EVENTO: extensión sin superar 127 %+0,25
PRECONDICIONES: B confirmó 100
SI SE CUMPLE: mantener B confirmada
SI NO SE CUMPLE: n/a
DESTINO: B_CONFIRMADA
PROHIBICIONES: llamar AUT
PRUEBAS: 110;127; límite exacto
```

### TM-B-004 · B supera límite AUT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B candidata o confirmada
EVENTO: supera 127 %+0,25
PRECONDICIONES: A válida
SI SE CUMPLE: dejar B y confirmar AUT inmediato
SI NO SE CUMPLE: mantener B
DESTINO: AUT_CONFIRMADO
PROHIBICIONES: esperar otra vela
PRUEBAS: salto directo 90→130
```

### TM-B-005 · Giro de B candidata antes del 100

**Estado historico:** `SUPERADO_POR_PATCH_v2.2`

> La oscilacion interna ya no cancela ni divide B. Aplicar la seccion 0.2. El texto historico inferior se conserva solo por trazabilidad.

**Estado anterior:** `PENDIENTE_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: precio vuelve hacia A
PRECONDICIONES: B <100
SI SE CUMPLE: aplicar decisión experta
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: llamar C
PRUEBAS: giro 20/80/99
PREGUNTA: Q-009: absorción, nueva A o reclasificación
```

### TM-B-006 · B confirmada gira

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CONFIRMADA
EVENTO: movimiento contrario a B
PRECONDICIONES: B alcanzó 100 sin AUT
SI SE CUMPLE: clasificar C inmediatamente
SI NO SE CUMPLE: n/a
DESTINO: C_EN_CURSO
PROHIBICIONES: llamar C candidata
PRUEBAS: giro 1 tick
```

## 11. C y CUT

### TM-C-001 · C se extiende

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: C_EN_CURSO
EVENTO: avance en dirección contraria a B
PRECONDICIONES: B confirmada misma lectura
SI SE CUMPLE: actualizar C
SI NO SE CUMPLE: n/a
DESTINO: C_EN_CURSO
PROHIBICIONES: usar B de otra lectura
PRUEBAS: avance parcial
```

### TM-C-002 · CUT

**Estado:** `DOCUMENTADO`

```text
ORIGEN: C_EN_CURSO
EVENTO: C alcanza final de A
PRECONDICIONES: misma lectura
SI SE CUMPLE: confirmar CUT
SI NO SE CUMPLE: seguir C
DESTINO: CUT_CONFIRMADO
PROHIBICIONES: confirmar por color
PRUEBAS: toca/supera
PREGUNTA: Q-010: CUT evento o función; tocar o superar
```

### TM-C-003 · C no alcanza CUT y gira

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: C_EN_CURSO
EVENTO: movimiento vuelve hacia B
PRECONDICIONES: C < final A
SI SE CUMPLE: aplicar decisión experta
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: inventar función
PRUEBAS: múltiples profundidades
PREGUNTA: Q-011: tratamiento completo de C sin CUT
```

### TM-C-004 · Después de CUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: CUT_CONFIRMADO
EVENTO: continuidad o giro
PRECONDICIONES: CUT confirmado
SI SE CUMPLE: definir siguiente lectura
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: cerrar todo automáticamente
PRUEBAS: continúa/gira
PREGUNTA: Q-012: consecuencia posterior a CUT
```

## 12. AUT y TT

### TM-AUT-001 · AUT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B candidata o confirmada
EVENTO: supera 127 %+0,25
PRECONDICIONES: A válida
SI SE CUMPLE: activar TT posible
SI NO SE CUMPLE: n/a
DESTINO: TT_POSIBLE
PROHIBICIONES: mantener B vigente
PRUEBAS: salto multinivel
```

### TM-TT-001 · TT progresa

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: TT_POSIBLE
EVENTO: expansión desde final A hacia objetivo
PRECONDICIONES: AUT misma lectura
SI SE CUMPLE: actualizar porcentaje
SI NO SE CUMPLE: n/a
DESTINO: TT_POSIBLE
PROHIBICIONES: llamar TT confirmado
PRUEBAS: 1–99,75 %
```

### TM-TT-002 · TT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: TT_POSIBLE
EVENTO: alcanza 100 %
PRECONDICIONES: objetivo = final A ± rango módulo
SI SE CUMPLE: confirmar TT y convertir recorrido culminante en nuevo 1
SI NO SE CUMPLE: seguir posible
DESTINO: TT_CONFIRMADO + UNO_CONFIRMADO
PROHIBICIONES: crear A/B/AUT propios sin lectura
PRUEBAS: 100 exacto/salto
```

### TM-TT-003 · TT falla antes del 100

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TT_POSIBLE
EVENTO: precio toca/corta final A antes de objetivo
PRECONDICIONES: AUT activo
SI SE CUMPLE: cancelar TT y aplicar reclasificación
SI NO SE CUMPLE: mantener TT
DESTINO: TT_FALLIDO
PROHIBICIONES: borrar AUT
PRUEBAS: fallo temprano/tardío
PREGUNTA: Q-013: condición exacta de fallo TT
```

### TM-TT-004 · AUT, 1 y TT pequeño simultáneos

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: AUT_CONFIRMADO
EVENTO: recorrido cumple referencias concurrentes
PRECONDICIONES: lecturas explícitas
SI SE CUMPLE: registrar todos por lectura
SI NO SE CUMPLE: n/a
DESTINO: ESTADOS_CONCURRENTES
PROHIBICIONES: fusionar etiquetas
PRUEBAS: caso simultáneo
```

## 13. FT

### TM-FT-001 · FT prohibido sin TT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: cualquier
EVENTO: movimiento contrario
PRECONDICIONES: TT no confirmado
SI SE CUMPLE: no FT
SI NO SE CUMPLE: n/a
DESTINO: SIN_FT
PROHIBICIONES: anticipar FT
PRUEBAS: caso negativo
```

### TM-FT-002 · FT candidato

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TT_CONFIRMADO
EVENTO: movimiento contrario claro
PRECONDICIONES: TT confirmado y posible pérdida de velocidad
SI SE CUMPLE: abrir FT candidato
SI NO SE CUMPLE: integrar micromovimiento
DESTINO: FT_CANDIDATO
PROHIBICIONES: confirmar por color
PRUEBAS: mismo minuto/multivela
PREGUNTA: Q-014: umbral matemático de movimiento claro y pérdida de velocidad
```

### TM-FT-003 · FT confirmado

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: FT_CANDIDATO
EVENTO: alcanza referencia FT
PRECONDICIONES: precondiciones completas
SI SE CUMPLE: confirmar FT
SI NO SE CUMPLE: mantener candidato
DESTINO: FT_CONFIRMADO
PROHIBICIONES: usar referencia no definida
PRUEBAS: frontera
PREGUNTA: Q-015: objetivo, inicio, cancelación y confirmación FT
```

### TM-FT-004 · Después de FT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: FT_CONFIRMADO
EVENTO: continuidad/giro
PRECONDICIONES: FT confirmado
SI SE CUMPLE: definir nuevo ciclo
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir nuevo 1
PRUEBAS: dos direcciones
PREGUNTA: Q-016: consecuencia posterior a FT
```

## 14. Árbol completo de gap

### TM-GAP-001 · Gap a favor de 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: Open avanza en dirección de 1
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: RUTA_GAP_FAVOR
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-017: funciones implícitas exactas
```

### TM-GAP-002 · Gap contrario a 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: Open avanza contra 1
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: A_INICIADA_POR_GAP
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-018: anclajes exactos de A por gap
```

### TM-GAP-003 · Gap cruza 100 de B

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura atraviesa nivel 100
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: B_CONFIRMADA_O_AUT
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-019: orden de niveles implícitos
```

### TM-GAP-004 · Gap cruza AUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura supera 127 %+0,25
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: AUT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-020: AUT por gap y objetivo TT
```

### TM-GAP-005 · Gap cruza objetivo TT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura supera objetivo 100 TT
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: TT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-021: confirmación inmediata y precio de nuevo 1
```

### TM-GAP-006 · Gap cruza CUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura cruza final de A durante C
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: CUT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-022: CUT por gap
```

### TM-GAP-007 · Gap cruza nivel FT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura cruza referencia FT
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: FT_CONFIRMADO_O_PENDIENTE
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-023: FT por gap
```

## 15. Saltos multinivel en un tick

```text
REGLA PROPUESTA: si un tick salta varios umbrales, registrar todos los umbrales causales atravesados en orden, pero dejar como estado vigente el último estado válido. No exigir permanencia de un tick en estados intermedios.
```

- B candidata → AUT: cruza 100 y AUT.

- TT posible → más allá del objetivo: cruza 100 TT.

- C → más allá de CUT: cruza final A.

- 2 candidato → extremo y retroceso: orden intratick no observable.

La última combinación exige política de datos cuando dos precios extremos aparecen sin orden intratick fiable: `PENDIENTE_JAVIER` y no reconstrucción inventada.

## 16. Concurrencia L1/L2/L3

### TM-CON-001 · Actualizar lecturas

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: 1–3 lecturas activas
EVENTO: nuevo tick
PRECONDICIONES: cada lectura conserva referencias
SI SE CUMPLE: evaluar el tick en todas por separado
SI NO SE CUMPLE: n/a
DESTINO: lecturas actualizadas
PROHIBICIONES: mezclar niveles
PRUEBAS: dos eventos simultáneos
```

### TM-CON-002 · Abrir lectura

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lecturas activas
EVENTO: evento de apertura
PRECONDICIONES: regla expresa
SI SE CUMPLE: crear Ln con padre/regla/tick
SI NO SE CUMPLE: no abrir
DESTINO: Ln
PROHIBICIONES: abrir por apariencia
PRUEBAS: L2/L3
PREGUNTA: Q-024: lista exhaustiva de disparadores
```

### TM-CON-003 · Capacidad máxima

**Estado:** `DOCUMENTADO`

```text
ORIGEN: L1/L2 activas
EVENTO: tercera posibilidad
PRECONDICIONES: excepcional y justificada
SI SE CUMPLE: abrir L3
SI NO SE CUMPLE: integrar/invalidar
DESTINO: L3 o no
PROHIBICIONES: más de 3
PRUEBAS: tres lecturas
PREGUNTA: Q-025: máximo absoluto y prioridad
```

### TM-CON-004 · Mismo movimiento en dos lecturas

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: L1/L2
EVENTO: un recorrido cumple papeles distintos
PRECONDICIONES: referencias separadas
SI SE CUMPLE: registrar ambos papeles
SI NO SE CUMPLE: n/a
DESTINO: doble etiqueta por lectura
PROHIBICIONES: fusionar lecturas
PRUEBAS: TT L1 y 1 L2
```

### TM-CON-005 · Cerrar/integrar lectura

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: múltiples lecturas
EVENTO: convergencia o incompatibilidad
PRECONDICIONES: regla de integración
SI SE CUMPLE: marcar integrada/invalidada conservando historial
SI NO SE CUMPLE: mantener
DESTINO: LECTURA_CERRADA
PROHIBICIONES: borrar
PRUEBAS: casos variados
PREGUNTA: Q-026: criterios exhaustivos de cierre
```

## 17. Reclasificación

### TM-REC-001 · Velas previas pasan a módulo

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: retroceso revela 1+2 conjunto
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-027: condiciones exactas
```

### TM-REC-002 · Velas previas pasan a 1 conjunto

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: retroceso revela unidad mayor
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-028: condiciones exactas
```

### TM-REC-003 · Movimiento candidato absorbido

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: no alcanza confirmación y retorna
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-029: reglas por estado
```

### TM-REC-004 · AUT simultáneo con 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: AUT cumple nacimiento de 1
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-030: referencias
```

### TM-REC-005 · TT pequeño dentro de TT mayor

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: módulos anidados
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-031: anidamiento y prioridad
```

### TM-REC-006 · Lectura alternativa pasa a principal

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: evidencia posterior
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-032: criterio de prioridad
```

## 18. Cambio de vela

```text
La frontera temporal no crea por sí sola una función. Al abrir vela: registrar cierre, apertura, gap y lecturas. Las funciones pueden comenzar en una vela y terminar en otras. TT y FT pueden coexistir dentro de una misma vela si las referencias se alcanzan cronológicamente.
```

- Cambio de vela con `1`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `2 candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `2 confirmado`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `3 candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `A`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `B candidata`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `B confirmada`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `AUT/TT posible`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `C`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `FT candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

## 19. Transiciones prohibidas

- C sin B confirmada en la misma lectura.

- CUT sin C válida.

- TT sin AUT.

- TT confirmado antes del 100 %.

- FT sin TT confirmado.

- 2 con gap.

- 2 con cola >0,25 previa a confirmación.

- B confirmada antes del 100 %.

- Mantener B después de superar AUT.

- Abrir L2/L3 sin regla expresa.

- Mezclar el A de L1 con el B de L2.

- Borrar historia al reclasificar.

- Inferir orden intravela usando solo OHLC cuando el orden afecta la etiqueta.

- Usar color de vela como fundamento funcional.

- Llamar ruido a un movimiento no resuelto para ocultar una rama ausente.

## 20. Matriz de cobertura de eventos

### Cobertura SIN_LECTURA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 1

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 2_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 2_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 3_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 3_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura MÓDULO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura A

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura B_CANDIDATA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura B_CONFIRMADA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura AUT

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_POSIBLE

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_FALLIDO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura C

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura CUT

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura FT_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura FT_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

## 21. Casos mínimos de prueba obligatorios

- `SIN_LECTURA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `1`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `2_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `2_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `3_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `3_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `MÓDULO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `A`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `B_CANDIDATA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `B_CONFIRMADA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `AUT`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_POSIBLE`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_FALLIDO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `C`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `CUT`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `FT_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `FT_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

## 22. Registro maestro de preguntas

Preguntas explícitas detectadas: Q-001 a Q-032. Además, la matriz de cobertura puede generar preguntas adicionales durante los tests. Las preguntas se resolverán después del primer test global, una por una, y cada respuesta actualizará regla, nodo y pruebas.

## 23. Criterio de promoción a v1

```text
PENDIENTE_JAVIER = 0
PROPUESTA_CONTROLADA no aprobada = 0
CONTRADICCIONES = 0
CELDAS SIN SALIDA = 0
TESTS FALLIDOS = 0
TRANSICIONES SIN PRECONDICIÓN = 0
LECTURAS ABIERTAS SIN REGLA = 0
```

## 24. Correccion experta incorporada durante pruebas

### TEST-TM-INTRAVELA-001 - Vela 20-7-7

**Estado:** `CONFIRMADO_JAVIER`

```text
UNA UNICA VELA:
1. Sube 20 puntos -> 1.
2. Por descarte -> MODULO.
3. Retrocede 7 puntos -> A.
4. Recupera 7 puntos hasta el maximo -> B al 100 % de A.
5. B queda confirmada.
6. No hay AUT porque no supera 127 % + 0,25.

SECUENCIA CANONICA:
1 -> MODULO_POR_DESCARTE -> A -> B_CONFIRMADA_100
```

**Correccion del arbol:** queda prohibido omitir el modulo por descarte en esta secuencia y saltar directamente de 1 a A.

---

## 24. Protocolo obligatorio de escenarios completos

### TM-ESC-001 · Enumeración total antes de responder

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: cualquier lectura TM activa
EVENTO: solicitud de clasificación de una o varias velas
PRECONDICIONES: recorrer el árbol completo, incluidas concurrencia y reclasificación
SI SE CUMPLE: enumerar todos los escenarios TM válidos compatibles con los ticks
SI NO SE CUMPLE: respuesta inválida e incompleta
DESTINO: RESPUESTA_TM_COMPLETA
PROHIBICIONES: responder solo con el escenario principal; ocultar escenarios coexistentes; inventar escenarios
PRUEBAS: caso con 1 escenario; caso con 2 escenarios; caso excepcional con 3 escenarios
```

### TM-ESC-002 · Número máximo de escenarios

**Estado:** `CONFIRMADO_JAVIER`

```text
REGLA: una respuesta TM puede contener como máximo 3 escenarios válidos.
FRECUENCIA ESPERADA: normalmente habrá 1 o 2 escenarios.
ESCENARIO 3: solo se mostrará cuando el recorrido completo del árbol lo sostenga.
PROHIBICIÓN: forzar siempre 3 escenarios.
```

### TM-ESC-003 · Orden obligatorio de respuesta

**Estado:** `CONFIRMADO_JAVIER`

```text
1. Recorrer el árbol principal.
2. Recorrer concurrencia.
3. Recorrer reclasificación.
4. Detectar funciones simultáneas de una misma vela.
5. Detectar funciones conjuntas de varias velas.
6. Eliminar escenarios incompatibles con los ticks.
7. Mostrar todos los escenarios supervivientes, numerados del 1 al 3.
```

### TM-ESC-004 · Formato obligatorio

**Estado:** `CONFIRMADO_JAVIER`

```text
ESCENARIO 1:
- secuencia TM completa

ESCENARIO 2:
- secuencia TM completa

ESCENARIO 3:
- secuencia TM completa, solo si existe

LECTURA COMÚN:
- hechos TM compartidos por todos los escenarios
```

### TM-ESC-005 · Caso validado 23:39–23:41

**Estado:** `CONFIRMADO_JAVIER`

```text
LECTURA COMÚN:
23:39 = 1 alcista.
23:40 = A + B + AUT; abre TT posible alcista.
23:41 alcanza el objetivo del TT y es nuevo 1.

ESCENARIO 1:
23:40 abre el TT posible y 23:41 lo culmina.
23:41 = TT confirmado + nuevo 1.

ESCENARIO 2:
23:40 y 23:41 forman conjuntamente el TT del 1 de 23:39.
23:41 = culminación del TT conjunto + nuevo 1.

PROHIBICIÓN:
No responder únicamente con uno de los dos escenarios.
```

### TM-ESC-006 · Regla de validez de respuesta

**Estado:** `CONFIRMADO_JAVIER`

```text
Una respuesta es VÁLIDA solo si:
- ha recorrido el árbol completo;
- ha comprobado escenarios concurrentes;
- incluye todos los escenarios compatibles;
- no supera 3 escenarios;
- no confunde número de vela con función TM.

Si falta un escenario válido, la respuesta se considera INCORRECTA aunque el escenario mostrado sea verdadero.
```


---

# ANEXO 11 - FUENTE INTEGRA: `TM_ARBOL_MAESTRO_CANONICO_v0_5_MEGA_BORRADOR.md`

- **SHA-256:** `b39e4dd9bd25916a51f96c1271ad9dd2950ab02d50319dfe2d473b7e6f7e9921`
- **Integridad:** contenido incorporado sin recortes.

# TM · ÁRBOL MAESTRO CANÓNICO

Versión 0.5 MEGA BORRADOR. Cobertura global para prueba, preguntas y corrección. No apto todavía para ejecución automática ni para operar.

## 0. Regla constitucional

```text
CLASIFICACIÓN VÁLIDA = lectura + estado anterior + cronología + referencia + precondiciones + transición + resultado.
Si falta una pieza, el motor registra HECHO_SIN_REGLA y no inventa una función. En la versión final HECHO_SIN_REGLA deberá ser cero.
```

## 1. Leyenda de certeza

- CONFIRMADO_JAVIER: regla expresamente cerrada por Javier.

- DOCUMENTADO: aparece en fuentes, pendiente de prueba experta.

- PROPUESTA_CONTROLADA: cierre técnico provisional para poder probar el árbol completo.

- PENDIENTE_JAVIER: pregunta concreta, no programable.

- PROHIBIDO: transición incompatible con las precondiciones.

## 2. Ontología completa provisional

```text
FUNCIONES: 1 | 2 | 3 | A | B | AUT | C
PATRONES: TT | FT
ESTRUCTURAS: MÓDULO | LECTURA
EVENTOS: GAP | AUTOCORTE | CUT | OBJETIVO_TT | CONFIRMACIÓN_FT
CALIFICADORES INTERNOS: CANDIDATO | CONFIRMADO | CANCELADO | RECLASIFICADO | INTEGRADO
```

## 3. Datos mínimos por tick

- timestamp

- bid/ask o precio de referencia acordado

- OHLC de vela activa

- Open actual y Close anterior

- dirección y extremo de cada lectura

- niveles 0, 50, 100, 127 y 127+0,25

- objetivo TT

- referencia CUT

- referencia FT

- historial inmutable de eventos

## 4. Orden universal de evaluación

```text
1. Registrar tick.
2. Detectar nueva vela.
3. Si nueva vela, evaluar GAP antes de 2.
4. Actualizar extremos de cada lectura.
5. Detectar niveles cruzados en el tick.
6. Procesar todos los niveles cruzados en orden geométrico.
7. Aplicar transición por lectura, sin mezclar referencias.
8. Abrir lectura adicional solo por regla expresa.
9. Registrar reclasificación sin borrar historial.
10. Emitir etiqueta visible y trazabilidad.
```

## 5. Árbol raíz y nacimiento de lectura

### TM-ROOT-001 · Sin lectura activa

**Estado:** `PROPUESTA_CONTROLADA`

```text
ORIGEN: SIN_LECTURA
EVENTO: primer recorrido observable
PRECONDICIONES: datos suficientes y referencia inicial autorizada
SI SE CUMPLE: abrir L1 con 1 candidato
SI NO SE CUMPLE: seguir acumulando ticks
DESTINO: UNO_CANDIDATO
PROHIBICIONES: no inventar dirección por color de vela
PRUEBAS: inicio alcista; inicio bajista; vela incompleta
PREGUNTA: Q-001: regla matemática definitiva de nacimiento del primer 1
```

### TM-ROOT-002 · Nueva lectura adicional

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: L1/L2 activa
EVENTO: posible recorrido independiente
PRECONDICIONES: regla explícita de apertura
SI SE CUMPLE: abrir primer slot libre
SI NO SE CUMPLE: integrar en lecturas existentes
DESTINO: Ln activa
PROHIBICIONES: abrir por apariencia visual
PRUEBAS: caso abre L2; caso no abre L2
PREGUNTA: Q-002: catálogo completo de reglas que abren L2/L3
```

## 6. Estado 1

### TM-1-001 · 1 continúa

**Estado:** `PROPUESTA_CONTROLADA`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: extensión en dirección de 1
PRECONDICIONES: no nace función posterior
SI SE CUMPLE: actualizar extremo y rango de 1
SI NO SE CUMPLE: mantener extremo
DESTINO: UNO_CONFIRMADO
PROHIBICIONES: crear otro 1 por cada vela
PRUEBAS: extensión misma vela; varias velas
```

### TM-1-002 · Apertura siguiente con gap

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: Open actual != Close anterior
PRECONDICIONES: nueva vela
SI SE CUMPLE: prohibir 2 y saltar a árbol GAP
SI NO SE CUMPLE: n/a
DESTINO: GAP_EVALUADO
PROHIBICIONES: evaluar plano o 2
PRUEBAS: gap 1 tick; gap varios puntos
```

### TM-1-003 · Sin gap y salida en plano

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: Open actual = Close anterior
PRECONDICIONES: nueva vela y sin cola observable >0,25 antes de objetivo
SI SE CUMPLE: abrir DOS_CANDIDATO
SI NO SE CUMPLE: si hay cola, prohibir 2
DESTINO: DOS_CANDIDATO
PROHIBICIONES: confirmar 2 solo por color
PRUEBAS: plano exacto; cola 0,25; cola 0,50
```

### TM-1-004 · No 2 por cola

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: cola de base >0,25 antes de confirmar 2
PRECONDICIONES: sin gap
SI SE CUMPLE: cancelar 2 y evaluar ruta A
SI NO SE CUMPLE: si cola <=0,25 mantener candidato
DESTINO: A_CANDIDATA
PROHIBICIONES: recrear 2 después
PRUEBAS: cola antes/después del objetivo
```

### TM-1-005 · No 2 por gap

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: gap cualquiera
PRECONDICIONES: nueva vela
SI SE CUMPLE: 2 prohibido
SI NO SE CUMPLE: n/a
DESTINO: RUTA_GAP
PROHIBICIONES: llamar 2 al recorrido posterior
PRUEBAS: gap a favor; gap contrario
```

## 7. Estado 2

### TM-2-001 · 2 candidato progresa

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: avance en dirección de 1
PRECONDICIONES: sin invalidación previa
SI SE CUMPLE: actualizar recorrido 2
SI NO SE CUMPLE: mantener
DESTINO: DOS_CANDIDATO
PROHIBICIONES: confirmar antes de medida
PRUEBAS: <100; =100; >100
PREGUNTA: Q-003: medida exacta y anclajes de 2
```

### TM-2-002 · 2 confirmado

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: alcanza medida exigida
PRECONDICIONES: plano, sin gap, sin cola invalidante previa
SI SE CUMPLE: confirmar 2
SI NO SE CUMPLE: seguir candidato
DESTINO: DOS_CONFIRMADO
PROHIBICIONES: borrar 2 por hechos posteriores
PRUEBAS: frontera exacta y salto
```

### TM-2-003 · Retroceso después de confirmar 2

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: DOS_CONFIRMADO
EVENTO: movimiento contrario
PRECONDICIONES: 2 ya confirmado
SI SE CUMPLE: conservar 2 y abrir evaluación de 3
SI NO SE CUMPLE: n/a
DESTINO: TRES_CANDIDATO
PROHIBICIONES: borrar 2
PRUEBAS: retroceso pequeño; grande
```

### TM-2-004 · Cambio de vela con 2 candidato

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: cierra vela sin confirmar
PRECONDICIONES: no hubo invalidación
SI SE CUMPLE: conservar/cancelar según decisión
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir cancelación
PRUEBAS: varias velas
PREGUNTA: Q-004: 2 puede confirmarse en varias velas
```

## 8. Estado 3 y módulo

### TM-3-001 · Retroceso válido para 3

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CONFIRMADO
EVENTO: retroceso dentro de franja válida
PRECONDICIONES: 2 confirmado
SI SE CUMPLE: seguir TRES_CANDIDATO
SI NO SE CUMPLE: fallar 3
DESTINO: TRES_CANDIDATO
PROHIBICIONES: anticipar 3
PRUEBAS: 0; 50; >50
PREGUNTA: Q-005: límites exactos del retroceso de 3
```

### TM-3-002 · 3 confirmado

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_CANDIDATO
EVENTO: precio retoma dirección de 2 y supera/toca extremo
PRECONDICIONES: retroceso válido
SI SE CUMPLE: confirmar 3
SI NO SE CUMPLE: mantener candidato
DESTINO: TRES_CONFIRMADO
PROHIBICIONES: confirmar por color
PRUEBAS: toca; supera 1 tick
PREGUNTA: Q-006: tocar o superar extremo de 2
```

### TM-3-003 · 3 falla

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_CANDIDATO
EVENTO: incumple regla de 3
PRECONDICIONES: 1 y 2 confirmados
SI SE CUMPLE: consolidar 1+2 como módulo y opuesto como A Grande
SI NO SE CUMPLE: seguir 3
DESTINO: MODULO_CONFIRMADO + A
PROHIBICIONES: crear módulo si nunca hubo 2
PRUEBAS: fallo por profundidad; fallo temporal
```

### TM-3-004 · 3 confirmado y continuidad

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: TRES_CONFIRMADO
EVENTO: extensión posterior
PRECONDICIONES: 3 confirmado
SI SE CUMPLE: definir siguiente estructura
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir A automáticamente
PRUEBAS: extensión/giro
PREGUNTA: Q-007: consecuencia exacta después de 3
```

## 9. Módulo y A

### TM-MOD-001 · Módulo 1+2

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_FALLIDO
EVENTO: opuesto tras fallo de 3
PRECONDICIONES: 1 y 2 confirmados
SI SE CUMPLE: fijar rango del módulo y A Grande
SI NO SE CUMPLE: n/a
DESTINO: A_EN_CURSO
PROHIBICIONES: formar módulo sin 2
PRUEBAS: caso estándar
```

### TM-MOD-002 · Módulo reclasificado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: varios movimientos previos
EVENTO: retroceso posterior permite integración
PRECONDICIONES: regla de reclasificación satisfecha
SI SE CUMPLE: crear módulo conjunto conservando eventos
SI NO SE CUMPLE: mantener lecturas
DESTINO: MODULO_RECLASIFICADO
PROHIBICIONES: borrar eventos
PRUEBAS: varias velas
PREGUNTA: Q-008: catálogo completo de reclasificación
```

### TM-A-001 · A se extiende

**Estado:** `DOCUMENTADO`

```text
ORIGEN: A_EN_CURSO
EVENTO: nuevo extremo en dirección de A
PRECONDICIONES: sin B opuesta confirmable
SI SE CUMPLE: actualizar final y rango de A
SI NO SE CUMPLE: mantener
DESTINO: A_EN_CURSO
PROHIBICIONES: congelar A demasiado pronto
PRUEBAS: extensión 1 tick/multivela
```

### TM-A-002 · Nace B candidata

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: A_EN_CURSO
EVENTO: movimiento contrario a A
PRECONDICIONES: A posee inicio/final/rango
SI SE CUMPLE: abrir B candidata
SI NO SE CUMPLE: mantener A
DESTINO: B_CANDIDATA
PROHIBICIONES: llamar B confirmada antes del 100
PRUEBAS: retorno 10/99/100
```

## 10. B candidata, B confirmada y AUT

### TM-B-001 · B por debajo del 100 %

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: avance <100 % de A
PRECONDICIONES: B opuesta a A
SI SE CUMPLE: seguir B candidata
SI NO SE CUMPLE: n/a
DESTINO: B_CANDIDATA
PROHIBICIONES: llamar B Grande
PRUEBAS: 99,75 %
```

### TM-B-002 · B alcanza 100 %

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: alcanza 100 %
PRECONDICIONES: no supera 127 %+0,25
SI SE CUMPLE: confirmar B Grande
SI NO SE CUMPLE: seguir candidata
DESTINO: B_CONFIRMADA
PROHIBICIONES: exigir cierre
PRUEBAS: 100 exacto
```

### TM-B-003 · B entre 100 y límite AUT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CONFIRMADA
EVENTO: extensión sin superar 127 %+0,25
PRECONDICIONES: B confirmó 100
SI SE CUMPLE: mantener B confirmada
SI NO SE CUMPLE: n/a
DESTINO: B_CONFIRMADA
PROHIBICIONES: llamar AUT
PRUEBAS: 110;127; límite exacto
```

### TM-B-004 · B supera límite AUT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B candidata o confirmada
EVENTO: supera 127 %+0,25
PRECONDICIONES: A válida
SI SE CUMPLE: dejar B y confirmar AUT inmediato
SI NO SE CUMPLE: mantener B
DESTINO: AUT_CONFIRMADO
PROHIBICIONES: esperar otra vela
PRUEBAS: salto directo 90→130
```

### TM-B-005 · Giro de B candidata antes del 100

**Estado historico:** `SUPERADO_POR_PATCH_v2.2`

> La oscilacion interna ya no cancela ni divide B. Aplicar la seccion 0.2. El texto historico inferior se conserva solo por trazabilidad.

**Estado anterior:** `PENDIENTE_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: precio vuelve hacia A
PRECONDICIONES: B <100
SI SE CUMPLE: aplicar decisión experta
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: llamar C
PRUEBAS: giro 20/80/99
PREGUNTA: Q-009: absorción, nueva A o reclasificación
```

### TM-B-006 · B confirmada gira

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CONFIRMADA
EVENTO: movimiento contrario a B
PRECONDICIONES: B alcanzó 100 sin AUT
SI SE CUMPLE: clasificar C inmediatamente
SI NO SE CUMPLE: n/a
DESTINO: C_EN_CURSO
PROHIBICIONES: llamar C candidata
PRUEBAS: giro 1 tick
```

## 11. C y CUT

### TM-C-001 · C se extiende

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: C_EN_CURSO
EVENTO: avance en dirección contraria a B
PRECONDICIONES: B confirmada misma lectura
SI SE CUMPLE: actualizar C
SI NO SE CUMPLE: n/a
DESTINO: C_EN_CURSO
PROHIBICIONES: usar B de otra lectura
PRUEBAS: avance parcial
```

### TM-C-002 · CUT

**Estado:** `DOCUMENTADO`

```text
ORIGEN: C_EN_CURSO
EVENTO: C alcanza final de A
PRECONDICIONES: misma lectura
SI SE CUMPLE: confirmar CUT
SI NO SE CUMPLE: seguir C
DESTINO: CUT_CONFIRMADO
PROHIBICIONES: confirmar por color
PRUEBAS: toca/supera
PREGUNTA: Q-010: CUT evento o función; tocar o superar
```

### TM-C-003 · C no alcanza CUT y gira

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: C_EN_CURSO
EVENTO: movimiento vuelve hacia B
PRECONDICIONES: C < final A
SI SE CUMPLE: aplicar decisión experta
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: inventar función
PRUEBAS: múltiples profundidades
PREGUNTA: Q-011: tratamiento completo de C sin CUT
```

### TM-C-004 · Después de CUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: CUT_CONFIRMADO
EVENTO: continuidad o giro
PRECONDICIONES: CUT confirmado
SI SE CUMPLE: definir siguiente lectura
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: cerrar todo automáticamente
PRUEBAS: continúa/gira
PREGUNTA: Q-012: consecuencia posterior a CUT
```

## 12. AUT y TT

### TM-AUT-001 · AUT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B candidata o confirmada
EVENTO: supera 127 %+0,25
PRECONDICIONES: A válida
SI SE CUMPLE: activar TT posible
SI NO SE CUMPLE: n/a
DESTINO: TT_POSIBLE
PROHIBICIONES: mantener B vigente
PRUEBAS: salto multinivel
```

### TM-TT-001 · TT progresa

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: TT_POSIBLE
EVENTO: expansión desde final A hacia objetivo
PRECONDICIONES: AUT misma lectura
SI SE CUMPLE: actualizar porcentaje
SI NO SE CUMPLE: n/a
DESTINO: TT_POSIBLE
PROHIBICIONES: llamar TT confirmado
PRUEBAS: 1–99,75 %
```

### TM-TT-002 · TT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: TT_POSIBLE
EVENTO: alcanza 100 %
PRECONDICIONES: objetivo = final A ± rango módulo
SI SE CUMPLE: confirmar TT y convertir recorrido culminante en nuevo 1
SI NO SE CUMPLE: seguir posible
DESTINO: TT_CONFIRMADO + UNO_CONFIRMADO
PROHIBICIONES: crear A/B/AUT propios sin lectura
PRUEBAS: 100 exacto/salto
```

### TM-TT-003 · TT falla antes del 100

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TT_POSIBLE
EVENTO: precio toca/corta final A antes de objetivo
PRECONDICIONES: AUT activo
SI SE CUMPLE: cancelar TT y aplicar reclasificación
SI NO SE CUMPLE: mantener TT
DESTINO: TT_FALLIDO
PROHIBICIONES: borrar AUT
PRUEBAS: fallo temprano/tardío
PREGUNTA: Q-013: condición exacta de fallo TT
```

### TM-TT-004 · AUT, 1 y TT pequeño simultáneos

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: AUT_CONFIRMADO
EVENTO: recorrido cumple referencias concurrentes
PRECONDICIONES: lecturas explícitas
SI SE CUMPLE: registrar todos por lectura
SI NO SE CUMPLE: n/a
DESTINO: ESTADOS_CONCURRENTES
PROHIBICIONES: fusionar etiquetas
PRUEBAS: caso simultáneo
```

## 13. FT

### TM-FT-001 · FT prohibido sin TT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: cualquier
EVENTO: movimiento contrario
PRECONDICIONES: TT no confirmado
SI SE CUMPLE: no FT
SI NO SE CUMPLE: n/a
DESTINO: SIN_FT
PROHIBICIONES: anticipar FT
PRUEBAS: caso negativo
```

### TM-FT-002 · FT candidato

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TT_CONFIRMADO
EVENTO: movimiento contrario claro
PRECONDICIONES: TT confirmado y posible pérdida de velocidad
SI SE CUMPLE: abrir FT candidato
SI NO SE CUMPLE: integrar micromovimiento
DESTINO: FT_CANDIDATO
PROHIBICIONES: confirmar por color
PRUEBAS: mismo minuto/multivela
PREGUNTA: Q-014: umbral matemático de movimiento claro y pérdida de velocidad
```

### TM-FT-003 · FT confirmado

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: FT_CANDIDATO
EVENTO: alcanza referencia FT
PRECONDICIONES: precondiciones completas
SI SE CUMPLE: confirmar FT
SI NO SE CUMPLE: mantener candidato
DESTINO: FT_CONFIRMADO
PROHIBICIONES: usar referencia no definida
PRUEBAS: frontera
PREGUNTA: Q-015: objetivo, inicio, cancelación y confirmación FT
```

### TM-FT-004 · Después de FT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: FT_CONFIRMADO
EVENTO: continuidad/giro
PRECONDICIONES: FT confirmado
SI SE CUMPLE: definir nuevo ciclo
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir nuevo 1
PRUEBAS: dos direcciones
PREGUNTA: Q-016: consecuencia posterior a FT
```

## 14. Árbol completo de gap

### TM-GAP-001 · Gap a favor de 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: Open avanza en dirección de 1
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: RUTA_GAP_FAVOR
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-017: funciones implícitas exactas
```

### TM-GAP-002 · Gap contrario a 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: Open avanza contra 1
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: A_INICIADA_POR_GAP
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-018: anclajes exactos de A por gap
```

### TM-GAP-003 · Gap cruza 100 de B

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura atraviesa nivel 100
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: B_CONFIRMADA_O_AUT
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-019: orden de niveles implícitos
```

### TM-GAP-004 · Gap cruza AUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura supera 127 %+0,25
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: AUT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-020: AUT por gap y objetivo TT
```

### TM-GAP-005 · Gap cruza objetivo TT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura supera objetivo 100 TT
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: TT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-021: confirmación inmediata y precio de nuevo 1
```

### TM-GAP-006 · Gap cruza CUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura cruza final de A durante C
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: CUT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-022: CUT por gap
```

### TM-GAP-007 · Gap cruza nivel FT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura cruza referencia FT
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: FT_CONFIRMADO_O_PENDIENTE
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-023: FT por gap
```

## 15. Saltos multinivel en un tick

```text
REGLA PROPUESTA: si un tick salta varios umbrales, registrar todos los umbrales causales atravesados en orden, pero dejar como estado vigente el último estado válido. No exigir permanencia de un tick en estados intermedios.
```

- B candidata → AUT: cruza 100 y AUT.

- TT posible → más allá del objetivo: cruza 100 TT.

- C → más allá de CUT: cruza final A.

- 2 candidato → extremo y retroceso: orden intratick no observable.

La última combinación exige política de datos cuando dos precios extremos aparecen sin orden intratick fiable: `PENDIENTE_JAVIER` y no reconstrucción inventada.

## 16. Concurrencia L1/L2/L3

### TM-CON-001 · Actualizar lecturas

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: 1–3 lecturas activas
EVENTO: nuevo tick
PRECONDICIONES: cada lectura conserva referencias
SI SE CUMPLE: evaluar el tick en todas por separado
SI NO SE CUMPLE: n/a
DESTINO: lecturas actualizadas
PROHIBICIONES: mezclar niveles
PRUEBAS: dos eventos simultáneos
```

### TM-CON-002 · Abrir lectura

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lecturas activas
EVENTO: evento de apertura
PRECONDICIONES: regla expresa
SI SE CUMPLE: crear Ln con padre/regla/tick
SI NO SE CUMPLE: no abrir
DESTINO: Ln
PROHIBICIONES: abrir por apariencia
PRUEBAS: L2/L3
PREGUNTA: Q-024: lista exhaustiva de disparadores
```

### TM-CON-003 · Capacidad máxima

**Estado:** `DOCUMENTADO`

```text
ORIGEN: L1/L2 activas
EVENTO: tercera posibilidad
PRECONDICIONES: excepcional y justificada
SI SE CUMPLE: abrir L3
SI NO SE CUMPLE: integrar/invalidar
DESTINO: L3 o no
PROHIBICIONES: más de 3
PRUEBAS: tres lecturas
PREGUNTA: Q-025: máximo absoluto y prioridad
```

### TM-CON-004 · Mismo movimiento en dos lecturas

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: L1/L2
EVENTO: un recorrido cumple papeles distintos
PRECONDICIONES: referencias separadas
SI SE CUMPLE: registrar ambos papeles
SI NO SE CUMPLE: n/a
DESTINO: doble etiqueta por lectura
PROHIBICIONES: fusionar lecturas
PRUEBAS: TT L1 y 1 L2
```

### TM-CON-005 · Cerrar/integrar lectura

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: múltiples lecturas
EVENTO: convergencia o incompatibilidad
PRECONDICIONES: regla de integración
SI SE CUMPLE: marcar integrada/invalidada conservando historial
SI NO SE CUMPLE: mantener
DESTINO: LECTURA_CERRADA
PROHIBICIONES: borrar
PRUEBAS: casos variados
PREGUNTA: Q-026: criterios exhaustivos de cierre
```

## 17. Reclasificación

### TM-REC-001 · Velas previas pasan a módulo

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: retroceso revela 1+2 conjunto
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-027: condiciones exactas
```

### TM-REC-002 · Velas previas pasan a 1 conjunto

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: retroceso revela unidad mayor
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-028: condiciones exactas
```

### TM-REC-003 · Movimiento candidato absorbido

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: no alcanza confirmación y retorna
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-029: reglas por estado
```

### TM-REC-004 · AUT simultáneo con 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: AUT cumple nacimiento de 1
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-030: referencias
```

### TM-REC-005 · TT pequeño dentro de TT mayor

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: módulos anidados
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-031: anidamiento y prioridad
```

### TM-REC-006 · Lectura alternativa pasa a principal

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: evidencia posterior
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-032: criterio de prioridad
```

## 18. Cambio de vela

```text
La frontera temporal no crea por sí sola una función. Al abrir vela: registrar cierre, apertura, gap y lecturas. Las funciones pueden comenzar en una vela y terminar en otras. TT y FT pueden coexistir dentro de una misma vela si las referencias se alcanzan cronológicamente.
```

- Cambio de vela con `1`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `2 candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `2 confirmado`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `3 candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `A`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `B candidata`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `B confirmada`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `AUT/TT posible`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `C`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `FT candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

## 19. Transiciones prohibidas

- C sin B confirmada en la misma lectura.

- CUT sin C válida.

- TT sin AUT.

- TT confirmado antes del 100 %.

- FT sin TT confirmado.

- 2 con gap.

- 2 con cola >0,25 previa a confirmación.

- B confirmada antes del 100 %.

- Mantener B después de superar AUT.

- Abrir L2/L3 sin regla expresa.

- Mezclar el A de L1 con el B de L2.

- Borrar historia al reclasificar.

- Inferir orden intravela usando solo OHLC cuando el orden afecta la etiqueta.

- Usar color de vela como fundamento funcional.

- Llamar ruido a un movimiento no resuelto para ocultar una rama ausente.

## 20. Matriz de cobertura de eventos

### Cobertura SIN_LECTURA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 1

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 2_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 2_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 3_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 3_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura MÓDULO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura A

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura B_CANDIDATA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura B_CONFIRMADA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura AUT

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_POSIBLE

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_FALLIDO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura C

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura CUT

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura FT_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura FT_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

## 21. Casos mínimos de prueba obligatorios

- `SIN_LECTURA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `1`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `2_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `2_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `3_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `3_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `MÓDULO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `A`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `B_CANDIDATA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `B_CONFIRMADA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `AUT`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_POSIBLE`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_FALLIDO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `C`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `CUT`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `FT_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `FT_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

## 22. Registro maestro de preguntas

Preguntas explícitas detectadas: Q-001 a Q-032. Además, la matriz de cobertura puede generar preguntas adicionales durante los tests. Las preguntas se resolverán después del primer test global, una por una, y cada respuesta actualizará regla, nodo y pruebas.

## 23. Criterio de promoción a v1

```text
PENDIENTE_JAVIER = 0
PROPUESTA_CONTROLADA no aprobada = 0
CONTRADICCIONES = 0
CELDAS SIN SALIDA = 0
TESTS FALLIDOS = 0
TRANSICIONES SIN PRECONDICIÓN = 0
LECTURAS ABIERTAS SIN REGLA = 0
```


---

# ANEXO 12 - FUENTE INTEGRA: `TM_ARBOL_MAESTRO_CANONICO_v0_1_TRABAJO.md`

- **SHA-256:** `db4a02401462c3a85ce4610cf1f5128611f85b1985df4606251f1d247db84769`
- **Integridad:** contenido incorporado sin recortes.

# TM - ARBOL MAESTRO CANONICO

## Versión 0.1 de trabajo supervisado

Estado: EN CONSTRUCCIÓN. No apto todavía para EA.
Autoridad experta: Javier.

## 0. Regla constitucional

Una clasificación TM solo es válida si identifica:

1. lectura;
2. estado anterior;
3. hecho cronológico;
4. referencia matemática;
5. precondiciones;
6. transición canónica;
7. estado resultante.

Si falta un elemento, la clasificación no se emite.

## 1. Unidad de análisis

La unidad primaria es el movimiento TM dentro de una lectura, no el color ni el cierre de una vela. Los ticks reconstruyen la cronología. Una vela puede contener varios movimientos y participar en más de una lectura si existe una regla expresa que abra dichas lecturas.

## 2. Capas propuestas para validación

### 2.1 Funciones / movimientos

- 1
- 2
- 3
- A
- B
- AUT
- C

### 2.2 Patrones

- TT
- FT

### 2.3 Estructuras

- módulo
- lectura L1/L2/L3

### 2.4 Evento cuya categoría debe confirmar Javier

- CUT

## 3. Estados temporales internos

Los estados internos no añaden vocabulario TM visible; sirven para impedir confirmaciones prematuras:

- CANDIDATO
- CONFIRMADO
- CANCELADO
- RECLASIFICADO
- INTEGRADO
- PENDIENTE_JAVIER, solo durante construcción

## 4. Reglas universales ya consolidadas

1. Procesar ticks en orden.
2. Evaluar gap antes de cualquier posible 2.
3. Con gap no hay 2.
4. Sin gap, cola observable superior a 0,25 antes de confirmar 2 impide 2.
5. Un 2 ya confirmado no se borra por una evolución posterior.
6. B es candidata antes del 100 % de A.
7. Si B alcanza 100 % sin superar 127 % + 0,25, B queda confirmada.
8. Si supera 127 % + 0,25, deja de clasificarse como B y se confirma AUT inmediatamente.
9. Tras B confirmada, cualquier movimiento posterior contrario a B es C.
10. AUT abre TT posible en la misma lectura.
11. TT solo se confirma al 100 %.
12. El movimiento que culmina TT confirmado pasa a nuevo 1.
13. Reclasificar no borra el historial.
14. Una función de una lectura no habilita funciones en otra lectura.

## 5. Caso de regresión 001

- Vela 1: 1, rango 9,80.
- Vela 2: A, B, AUT; final de A 29179,20.
- Objetivo TT: 29189,00.
- Vela 3 alcanza 29189,30.
- Resultado: vela 3 es TT de vela 2; TT confirmado; vela 3 es nuevo 1.
- Prohibido añadir A/B/AUT propios en vela 3 sin segunda lectura abierta por regla expresa.

## 6. Bloque actual

BLOQUE 0: ontología y fronteras universales.

No se redactarán ramas dependientes como definitivas hasta resolver Q-0001 a Q-0005.

## 7. Preguntas bloqueantes, ronda 1

### Q-0001 CUT

¿CUT es una función/movimiento independiente o el evento de confirmación de C al alcanzar el final de A?

### Q-0002 Movimiento absorbido

Cuando un movimiento contrario no alcanza la referencia necesaria para abrir la siguiente función, ¿queda integrado en el movimiento vigente o depende del estado de origen?

### Q-0003 Confirmación exacta de 1

¿Cuáles son todas las vías autorizadas para confirmar 1: inicial, TT confirmado, reclasificación, AUT simultáneo u otras?

### Q-0004 Medida exacta de 2

¿Qué distancia exacta debe alcanzar 2 y desde qué precio hasta qué precio se mide?

### Q-0005 Regla exacta de 3

¿Qué condiciones exactas confirman 3, incluyendo nivel de retroceso, superación del extremo de 2, mismo/múltiples minutos y cancelación?


---

# REGISTRO DE REVISION v2.5

- Prioridad obligatoria del modulo principal y del modulo conjunto grande.
- Todos los patrones se leen continuamente, incluidos los inferiores a 6 puntos.
- Filtro teórico: estructuras menores de 6 puntos no elegibles para entrada; 6 puntos exactos sí cumplen tamaño.
- Separacion estricta entre lectura TM y futura elegibilidad operativa.
- AUT registrado como zona conceptual futura de activacion, no como orden ejecutable en esta version.
- Plantilla obligatoria con tamaño, clase, B Grande, AUT y objetivo TT por escala.
- Archivo base v2.4 SHA-256: `a834914b97e9e07ed1e927a3c62c6bf28836b56c33ce95172c8bc81b4062ca8f`.
- La seccion 0.5 prevalece sobre cualquier redaccion historica incompatible.

---

# REGISTRO DE REVISION v2.4

- Maximo operativo de dos escalas: modulo principal y un mini modulo actual.
- Integracion M1 + M2 solo cuando A2 supera la base de M2.
- La misma A2 pasa a ser A Grande del modulo conjunto sin reiniciarse.
- Si A2 no supera M2 y gira, se mantienen solo TT principal y TT interno; no M3.
- Plantilla obligatoria para definir cada movimiento con lectura, origen, extremo, direccion, medida, referencia y estado.
- Prioridad de absorcion para evitar proliferacion y distorsion.
- Archivo base v2.3 SHA-256: `f39325564e3aa37671617eb6c8bb98018c39275a2a68d32544e9013351b04f97`.
- La seccion 0.4 prevalece sobre cualquier redaccion historica incompatible.

---

# REGISTRO DE REVISION v2.3

- Prioridad absoluta de preguntas despues de 1.
- Con gap, 2 imposible.
- Bifurcacion tick a tick: despues del gap sube primero o baja primero.
- Ramas completas A/B/AUT/TT y modulo por descarte.
- Regla de AUT y nuevo 1 cuando A supera la base del modulo.
- Caso de regresion completo de vela 16 incorporado.
- Archivo base v2.2 SHA-256: `0bb747c27b7bb724bc4f71e7c4c909233b4e4de59bfe6856a5c1d9f102614653`.
- La seccion 0.3 prevalece sobre cualquier redaccion historica incompatible.

---

# REGISTRO DE REVISION v2.2

- Regla incorporada: continuidad integral de B candidata y B Grande.
- Oscilaciones internas absorbidas dentro de una sola B, incluso si superan 2 puntos.
- Confirmacion de B Grande unicamente al alcanzar o superar el 100 % de A Grande.
- Conversion simultanea de A Grande en modulo por descarte para la lectura concurrente.
- Conservacion de la frontera AUT en `127 % + 0,25`, con superacion estricta.
- Caso de regresion de vela 14 corregido y fijado.
- Archivo base v2.1 SHA-256: `4f730f268dfb5468eb62f40c449af515abc673745302dca7f81b0d4807841f12`.
- La seccion 0.2 prevalece sobre ramas historicas incompatibles.

---

# REGISTRO DE REVISION v2.1

- Regla incorporada: concurrencia canonica de velas 5 y 6.
- Base preservada: v2.0 integra, salvo cambio de version y adicion prioritaria v2.1.
- Archivo base SHA-256: `d6bed6a42d62159dda733402665b6c0e2ce587b0c41e0d1e09090354af50dc0d`.
- Criterio de prevalencia: la seccion 0.1 v2.1 corrige cualquier lectura historica incompatible.

---

# MANIFIESTO FINAL DE INTEGRIDAD

- `TM_ARBOL_CANONICO_COMPLETO_v1.md` | 51786 bytes | SHA-256 `e9d4b419868233949b4459f9b97294b8b5487e84c7c4ee5a92aa3289113cfd3e`
- `TM_ARBOL_MAESTRO_CANONICO_v0_9_SALIDA_MOVIMIENTOS_PATRONES_TT.md` | 77939 bytes | SHA-256 `f7d7800e0538c3e956f043f518b91cedb693a7afa34c728faa7463d67ced09f0`
- `TM_PATCH_CANONICO_v1_0_TT_FT_CONCURRENCIA_VELA7.md` | 6654 bytes | SHA-256 `58628c161246097aff8f51efffe5f6342d55a6c721771e73574137c23f4e9435`
- `TM_PATCH_CANONICO_v1_1_RESET_TT_VELAS8_9.md` | 10260 bytes | SHA-256 `fba5f3964ab74b736974c4e4e58fb0e8ca77361b613d7a19823d2ee87defe0d5`
- `TM_PATCH_CANONICO_v1_2_C_CUT_TERCERO_RESET.md` | 16839 bytes | SHA-256 `b04b6629ffbd912f26ae2bedd0ae7cd366201db548749652d21bee3de4b108d6`
- `TM_DECISIONES_EXPERTO_v0_1.md` | 1063 bytes | SHA-256 `10e79b4d5f85e1378c873f063e5134df7c2de46f3e50be5beb2ee57d9d7271e1`
- `TM_DUDAS_PENDIENTES_JAVIER.md` | 5599 bytes | SHA-256 `261d68af1b30999280915262ab90828e0148056720659aa51053fc9d11cfabe2`
- `TM_ARBOL_MAESTRO_CANONICO_v0_8_B_CANDIDATA_MODULO_ABAUT.md` | 76197 bytes | SHA-256 `d97d91b3bde8a8cf0b8c22a3aaee0616e07724b6b3a2f60ddd98a298ac4f26ac`
- `TM_ARBOL_MAESTRO_CANONICO_v0_7_FT_POST_TT (1).md` | 73150 bytes | SHA-256 `6e1d45824d8426feaca0d9c92a526e626e300f564b165587d04fe368a20d0246`
- `TM_ARBOL_MAESTRO_CANONICO_v0_6_ESCENARIOS_COMPLETOS.md` | 70689 bytes | SHA-256 `6b269b6e90a0b9a01679ea32b98d0a1e191792109655cd84fada9dc16d4342bd`
- `TM_ARBOL_MAESTRO_CANONICO_v0_5_MEGA_BORRADOR.md` | 67445 bytes | SHA-256 `b39e4dd9bd25916a51f96c1271ad9dd2950ab02d50319dfe2d473b7e6f7e9921`
- `TM_ARBOL_MAESTRO_CANONICO_v0_1_TRABAJO.md` | 3329 bytes | SHA-256 `db4a02401462c3a85ce4610cf1f5128611f85b1985df4606251f1d247db84769`

**Copias duplicadas omitidas:** los archivos `(1)` y `(2)` de v1.2 son copias binarias/logicas del parche canonico v1.2 y no se repiten para evitar duplicacion literal.


# REGISTRO DE REVISION v2.10

- Se cierra teoricamente Variable 1 Patron.
- Se cierra conceptualmente Variable 2 Velocidad, pendiente de formula y validacion.
- Se fija observacion 9:15-9:30 NY y sesion 9:30-12:30 NY.
- Brokeraje pasa a fase dinamica, operable y separada del regimen estabilizado.
- Velocidad admite regimen sostenido o cambio hacia AUT.
- La ventana es adaptativa: B, A+B o parte final de 1+A+B.
- La primera implementacion MQL5 sera registrador, no filtro.
- Separacion absoluta: las variables nunca modifican la lectura TM.
- Archivo base v2.7 SHA-256: `4b3509d0dce73361097977320fa9f4f23156b36e8cd2eef061836d11ec8dc4fc`.


# REGISTRO DE REVISION v2.11

- Se define conceptualmente Variable 3 Solapamiento frente a verticalidad.
- Escala profesional: 0 solapamiento maximo, 10 verticalidad maxima.
- Se separan puntuacion de sesion y puntuacion reciente.
- Se documentan seis tipologias por tamaño y disposicion.
- Se incorpora USTECM1 como caso visual canonico 7/10 vertical, 3/10 solapado.
- Se proponen mediciones candidatas para futuro codigo sin aprobar formula final.
- Se mantiene separacion absoluta respecto de Velocidad y lectura TM.
- Archivo base v2.10 SHA-256: `abfff44c4789d948a1cfdbd0be18b16e96567bdd4c19c02497841707dd0f2013`.


# REGISTRO DE REVISION v2.12

- Se refuerza la separacion constitucional entre lectura, variables y decision.
- Se prohíbe que cualquier variable confirme, cancele o reclasifique la lectura TM.
- Las cinco variables se definen como organismo probabilistico conjunto, no filtros aislados.
- Se define Variable 4 Tiempo M1/M3 sin vetos temporales automaticos.
- Se define Variable 5 Estructura mediante SMA7 High/Low en M3.
- Se aprueba el Explorer historico con maximo tres CSV y todas las variables separadas.
- Se registra el principio `recoger ahora, definir despues, validar antes de decidir`.
- Archivo base v2.11 SHA-256: `ffd7309049b6ca31bcafb778e1684be35f6ded2a2935fc051ed6fc96ff480908`.
