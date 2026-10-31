# AUDITORIA FUNCIONAL - DEFINICION CANONICA DE 3

Auditor: TM_READER_VALIDATOR
Fecha: 2026-10-29
Alcance: solo lectura. No se ha modificado motor, tests, arbol, golden ni reglas.
Artefacto de referencia: TM_CORE_v0752_R3_B_AUT (hash 450379BD...B7DB) y arbol/reglas activos en TM_CANON_ACTIVO.

## 1. Punto de partida

Javier pausa la decision sobre el 100 % de 1 y pide localizar la definicion canonica
existente de 3 antes de implementar la transicion 2 -> 3. Se descarta expresamente usar
el umbral de 2 puntos como definicion funcional de 3.

## 2. Donde esta definido 3

| Fuente | Ubicacion exacta | Contenido | Rango |
|---|---|---|---|
| Dossier TM v3 | `Dossier_TM_v3_Lectura_Obligatoria.txt` lineas 385-404 (§4.3 TERCERO) | Retroceso 0-50 % del rango de 2 + superacion del extremo de 2 | Normativo de referencia |
| Dossier TM v4 | `Dossier_TM_v4_Concurrencia_Reclasificacion.txt` lineas 260-287 (§4.3) | Texto identico al v3 | Copia consolidada |
| Prompt v2 | `Prompt_ECC_OpenCode_TM_..._v2 (1).txt` §10.2 lineas 483-491 | "Despues se abre posible 3"; "Si el movimiento contrario supera el 50 %, 3 falla"; "Posible 3 no se confirma automaticamente dentro de la misma vela solo por nuevo extremo" | Maximo rango |
| Arbol canonico | `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_12.md` N-009 (3023), N-010 (3040), N-011 (3055), tabla 3.2 (2819), TM-3-001/002/003 (4087-4125) | Estados `3_CANDIDATA` / `3_CONFIRMADA`, formulas, prohibiciones y Q-005/Q-006 | CERRADO (v3 §4.3) |
| Reglas cerradas | `REGLAS_CERRADAS.md` A1 y A2 | Solo referencia a 3: "cuando falla el 3, 1 y 2 forman modulo" | CERRADO por derivacion |
| Golden humano | `TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v003.txt` lineas 430-446 | 16:21 = 3 confirmado; secuencia 16:19=1, 16:20=2, 16:21=3 | [A] |

## 3. Definicion canonica literal

Dossier v3 §4.3:

    Para que exista 3 deben cumplirse simultaneamente las dos reglas:
    1. Retroceso entre el 0 % y el 50 % del rango de 2.
    2. Superacion del extremo de 2:
       Alcista: High(3) > High(2)
       Bajista: Low(3) < Low(2)
    Si retrocede mas del 50 % o no supera el extremo de 2:
       3 no existe.
       1 + 2 quedan como modulo.
       El movimiento contrario es A Grande del modulo 1-2.

Prompt v2 §10.2 anade tres limites que no estan en el dossier:

    - Despues se abre posible 3.
    - Si el movimiento contrario supera el 50 %, 3 falla.
    - Posible 3 no se confirma automaticamente dentro de la misma vela solo por nuevo extremo.

Arbol N-009/N-010:

    N-009 PRECONDICIONES: retroceso 0-50 % del rango de 2; superacion del extremo de 2.
    FOMULA: alcista High(3) > High(2); bajista Low(3) < Low(2); retroceso 0-50 %.
    N-010 SI_TRUE: 3_CONFIRMADA; ciclo modular regular.

## 4. Tabla de auditoria 1, 2 y 3

| Campo | 1 | 2 | 3 |
|---|---|---|---|
| funcion | Movimiento que inicia el modulo y define la direccion | Segundo movimiento del modulo, misma direccion que 1 | Tercer movimiento del ciclo modular regular |
| funcion anterior requerida | Ninguna (`SIN_LECTURA`); tambien puede nacer como nuevo 1 dominante tras AUT (B2/DEC-012) | `1_ACTIVA` + apertura de vela nueva | `2_CONFIRMADA` |
| condicion de nacimiento | Primer movimiento direccional con referencia TM valida, no ruido, orden temporal reconstruido (N-001) | `2_CANDIDATA` al abrir en plano sin gap; `2_CONFIRMADA` al alcanzar el desplazamiento de 1 (N-007) | `3_CANDIDATA` con retroceso 0-50 % y extremo de 2 superado; `3_CONFIRMADA` al cumplirse ambas a la vez (N-010) |
| origen de medicion | Extremo inicial del movimiento (low alcista / high bajista) | Apertura de 2, que debe ser su extremo de cola (Low(2)=Open(2) / High(2)=Open(2)) | Extremo de 2 (desde ahi se mide el retroceso) |
| extremo de medicion | Extremo final del movimiento (high alcista / low bajista) | Extremo de 2 en la direccion de 1 | Extremo de 2 (el que debe superarse) |
| medida minima de confirmacion | Ninguna teorica: "no exige rango minimo teorico" (N-001) | 100 % del desplazamiento direccional de 1 | Superar el extremo de 2; cuanto (toque o 1 tick) = Q-006 abierto |
| posibilidad de superar esa medida | Si; 1 se extiende hasta que aparece un contrario con referencia valida | Si; 2 puede extender su extremo y ampliar el modulo | Si; 3 puede extender (`3_EXTIENDE_MODULO`); hasta cuando = TM-3-004 `PENDIENTE_JAVIER` |
| condicion de imposibilidad | Ruido sin referencia TM (BASE-6); que el contrario sea A Grande | Gap `|delta| > 0,25`; cola inicial > 0,25; rango < 1; direccion distinta (N-008) | Retroceso > 50 % o no superar el extremo de 2 (N-011); ademas no confirmar intravela solo por nuevo extremo (prompt §10.2) |
| siguiente pregunta | Que es exactamente "referencia TM relevante" (BASE-6) y deteccion general de 1 (N-001 PROVISIONAL) | Q-004: puede 2 confirmarse en varias velas; yardstick H-L vs direccional | Q-005: limites exactos del retroceso; Q-006: tocar o superar el extremo de 2; prohibicion intravela |
| fuente canonica | A1; N-001; BASE-6; prompt §10.1-10.2; v003 16:19 | A1; N-005/N-006/N-007/N-008; H14; DEC-005/DEC-009; prompt §10.2; v003 16:20 | Dossier v3 §4.3; v4 §4.3; prompt §10.2; N-009/N-010/N-011; TM-3-001/002/003; v003 16:21 |
| implementacion actual | `_close_candidate_bar` (R3 2424-2453): exige `span >= MOVE` = 6,00 pts | `POSSIBLE_TWO` -> `TWO_CONFIRMED` (R3 2508-2532): `local_two_gate` con `dist >= one_size` y `tail <= 0,25` | `WAIT_THREE` (R3 2565-2573): exige nuevo extremo **y** `abs(p-ext) >= STRUCTURAL_MOVE` = 2,00 pts |
| pruebas existentes | T-001/T-040 solo "Diseno" (`TM_TESTS_REQUERIDOS_v1.md`); 0 ejecutables | T-001/T-004/T-005/T-037/T-038 solo "Diseno"; 0 ejecutables con nombre | T-007/T-008/T-009/T-010 solo "Diseno"; 0 ejecutables |

## 5. Hallazgos de auditoria

### H1. La definicion de 3 existe, pero esta dispersa y con dos huecos abiertos

No falta la definicion: esta en Dossier v3/v4 §4.3 y en N-009/N-010/N-011 como `CERRADO`.
Pero quedan abiertos:

- Q-005: limites exactos del retroceso (si 0 % y 50 % son inclusivos).
- Q-006: si 3 confirma al tocar o al superar el extremo de 2.
- Yardstick no fijado: el dossier dice "rango de 2", que sugiere High-Low; A1 fija
  "desplazamiento direccional, no High-Low" para 1 y 2. Es el mismo nudo que A1/F1.
- El bullet del prompt §10.2 ("no se confirma automaticamente dentro de la misma vela
  solo por nuevo extremo") no aparece en el dossier ni en el arbol.

Clasificacion: `REGLA_ABIERTA`.

### H2. La implementacion actual de 3 no es la canonica

`WAIT_THREE` (R3 2565-2573):

    ext = st["two_extreme"]
    new_extreme = (d<0 and p.price<ext.price) or (d>0 and p.price>ext.price)
    if new_extreme and abs(p.price-ext.price) >= STRUCTURAL_MOVE:
        ... LOCAL_3_CONFIRMADO

- Introduce un minimo de 2,00 pts (`STRUCTURAL_MOVE = 200` con `PRICE_SCALE = 100`).
  Ese umbral no existe en la definicion de 3 y es exactamente el que Javier prohibe.
- No comprueba el retroceso 0-50 % en ningun punto.
- La transicion a `WAIT_THREE` solo ocurre al cierre de la vela de 2 (R3 2787-2788),
  por lo que 3 nunca confirma en la vela de 2. Coincide con el prompt §10.2 por
  construccion de fases, no por regla implementada.
- `_local_123` (R3 498) no se usa en R3: queda como codigo muerto. En v0751 si se usa
  (linea 513) y tampoco comprueba el 50 %.

Prueba directa sobre la salida R3 (`out/CORE_RAW_OUTPUT.json`, `local_sequences[0].legs[2]`):

    3 -> direction -1, origin 2983250 (29832,50), extreme 2983050 (29830,50)
    confirmation_time 1792167711869 = 16:21:51.869

En el feed del paquete (`data/TM_TICKFEED_1615_1730.csv`):

    seq 1446  16:21:14  bid 29832,3   primer cruce del extremo de 2 (0,2 pts)
    seq 1590  16:21:51  bid 29830,5   exactamente 2,00 pts por debajo de 29832,5
    seq 1601  16:21:54  bid 29830,3   minimo real de la vela

Consecuencias verificables:

1. La regla canonica habria confirmado 3 en seq 1446 (16:21:14, 0,2 pts de superacion).
2. El motor no confirma hasta seq 1590 (16:21:51), 37 segundos y 1,8 pts despues,
   porque solo ahi se cumple `abs(p - ext) >= 2,00`.
3. La confirmacion depende de que el precio alcance exactamente 2,00 pts. Si el minimo
   de la vela hubiera sido 29830,6 (1,9 pts), el motor no habria confirmado 3.
4. El extremo registrado (29830,50) queda congelado en la confirmacion y no incorpora
   el minimo real de la vela (29830,30, seq 1601).

Clasificacion: `BUG_MOTOR` por el umbral anadido, por la regla ausente del 50 % y por
el extremo de 3 congelado antes del cierre.

### H3. No hay pruebas ejecutables de 3

T-007, T-008, T-009 y T-010 existen solo como especificacion de diseno
(`tm-explorer/control/TM_TESTS_REQUERIDOS_v1.md`, columna "Estado: Diseno").
En el paquete R3 solo hay `test_big_b_aut.py` y `test_transformations.py`; ninguno
ejercita un 3. La cobertura de 3 es indirecta via golden y via literatura del arbol.

Clasificacion: `SIN_EVIDENCIA` para comportamiento de 3 bajo prueba automatica.

## 6. Verificacion del caso humano 16:21 (control positivo)

- 1 = 16:19: maximo 29850,0, minimo 29842,5; medida direccional 7,5 pts.
- 2 = 16:20: apertura 29844,8 = maximo (cola 0), cierre anterior 29845,0, delta -0,2 < 0,25
  (plano); recorrido 12,3 >= 7,5; 2 confirmado.
- 3 = 16:21: tras 2, retroceso hasta 29836,3 (3,8 pts = 30,9 % de 12,3, dentro de 0-50 %)
  y nuevo minimo 29830,3 < 29832,5; 3 confirmado.
- El primer cruce canonico del extremo de 2 ocurre en seq 1446 (16:21:14, bid 29832,3):
  0,2 pts de superacion bastan segun la definicion.
- El motor no confirma 3 hasta seq 1590 (16:21:51, bid 29830,5), donde la distancia es
  exactamente 2,00 pts. Ese es el umbral `STRUCTURAL_MOVE`, no la regla de Javier.

Este caso es el control que invalida `STRUCTURAL_MOVE` como definicion de 3: el criterio
canonico se cumple 37 segundos antes de que el motor lo reconozca, y solo se cumple por
casualidad al tocar exactamente 2,00 pts. El golden pasa por coincidencia numerica, no
porque la regla implementada sea la canonica.

## 7. Respuesta a la pregunta de Javier

1. La definicion canonica de 3 **ya existe** y no hay que inventarla.
2. Esta **dispersa** en cuatro documentos y tiene **tres huecos**: Q-005, Q-006 y el
   yardstick del 50 %; mas un cuarto punto (prohibicion intravela) que solo esta en el
   prompt.
3. La implementacion **no** implementa esa definicion: usa un umbral de 2,00 pts y omite
   el 50 %. No debe tomarse como referencia de conducta.
4. No se ha tocado ninguna logica de 3. No se propone refactor hasta que Javier cierre
   Q-005, Q-006 y el yardstick del 50 %.

## 8. Recomendacion

Antes de la transicion 2 -> 3:

- fijar el yardstick del 50 % (High-Low de 2 vs desplazamiento direccional de 2);
- fijar si 0 % y 50 % son inclusivos;
- fijar si 3 confirma por toque o por 1 tick de superacion;
- resolver si la prohibicion intravela del prompt §10.2 se incorpora al arbol;
- solo despues, sustituir `STRUCTURAL_MOVE` por la regla de extremo de 2 y escribir
  T-007/T-008/T-009/T-010 ejecutables.

Sin aprobacion de Javier. Sin cambios en motor, tests, arbol, golden ni reglas.
