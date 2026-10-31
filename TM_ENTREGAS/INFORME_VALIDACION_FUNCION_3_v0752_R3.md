# VALIDACION CANONICA DE LA FUNCION 3 - INFORME

Agente: TM_READER_VALIDATOR
Fecha: 2026-10-29
Modo: solo lectura y ejecucion. Sin cambios en motor, arbol, goldens ni reglas.
Motor auditado: `TM_CORE_v0752_R3_B_AUT/python/TM_CORE_PYTHON_v0752_CANONICAL.py`
SHA-256: `71d9a97ac2c49848d152a790db0c70d20b30643782bfee0ac030d19110330b08` (coincide con `manifest.json`)
Artefactos de validacion: `t3_validation/` (harness, 12 pruebas, replay, JSON)

## A. Resumen ejecutivo

1. La definicion canonica de 3 existe y esta cerrada en lo esencial (Dossier v3/v4 §4.3,
   prompt §10.2, N-009/N-010/N-011). No hay que inventarla.
2. Se crearon 12 pruebas ejecutables independientes (T3-001 a T3-012). Resultado contra
   el motor actual: **3 pasan, 9 fallan**.
3. La desviacion principal: `WAIT_THREE` sustituye la regla funcional por
   `abs(precio - extremo_2) >= 2,00 puntos` y no registra el retroceso 0-50 %.
4. Consecuencias demostradas:
   - confirma 3 tarde: 16:21:51,869 en vez de 16:21:14,734 (37,135 s y 1,80 pts de retraso);
   - confirma 3 tras un retroceso del 52,85 % (deberia ser imposible);
   - convierte una extension pura de 2 en 3 (sin retroceso previo);
   - congela el extremo de la pata 3 en el precio de confirmacion (29830,5) mientras el
     modulo si se actualiza a 29830,3.
5. `_local_123` contiene tres reglas validas (superacion estricta, apertura plana, cola),
   pero mide 1 por High-Low y trabaja sobre velas cerradas, por lo que no es causal. No
   debe conectarse.
6. No se ha modificado ningun artefacto congelado. El SHA del motor coincide con el
   manifest.

## B. Fuentes canonicas verificadas

| Fuente | Ubicacion | Uso en esta validacion |
|---|---|---|
| Dossier TM v3 | `Dossier_TM_v3_Lectura_Obligatoria.txt` §4.3 (385-404) | Regla 0-50 % + superacion del extremo |
| Dossier TM v4 | `Dossier_TM_v4_Concurrencia_Reclasificacion.txt` §4.3 (260-287) | Copia consolidada |
| Prompt v2 | §10.2 (483-491) | Posible 3, 50 %, prohibicion intravela |
| Arbol v2.12 | N-009 (3023), N-010 (3040), N-011 (3055), §3.2 (2819), TM-3-001/002/003 (4087-4125) | Estados, formulas, prohibiciones, Q-005/Q-006 |
| Reglas cerradas | A1/A2 | Medida direccional de 1 y 2; modulo |
| Golden humano | v003 lineas 430-446 | 16:21 = 3; secuencia 16:19/16:20/16:21 |

## C. Definicion consolidada de 3 (operativa)

Precondicion: 2 confirmada.

1. `origin_2` = origen funcional de 2; `extreme_2` = extremo funcional de 2 en la
   direccion de 1, fijado antes del retroceso que puede dar origen a 3.
2. `size_2 = abs(extreme_2 - origin_2)` (desplazamiento funcional, no High-Low bruto).
3. Retroceso valido: `0 <= (retr_extreme - extreme_2)/size_2 <= 0,50` para bajista
   (simetrico para alcista). Exactamente 50 % es valido; mas de 50 % imposibilita 3.
4. Toque del extremo de 2: no confirma. Superacion estricta: confirma.
   Bajista `precio < extreme_2`; alcista `precio > extreme_2`. Sin `>=` ni `<=`.
5. Basta un tick de superacion (0,25 pts o el paso real del instrumento). No se exigen
   2,00 puntos.
6. La secuencia causal obligatoria es 2_CONFIRMADA -> retroceso valido -> 3_CANDIDATA ->
   superacion estricta -> 3_CONFIRMADA. Un nuevo extremo sin retroceso previo es
   2_EXTIENDE.
7. Intravela: la prohibicion es "no confirmar solo por nuevo extremo"; si la secuencia
   completa es demostrable, 3 puede confirmar dentro de la vela.
8. Tras confirmar: conservar tick y nivel de confirmacion, actualizar el extremo de 3 en
   cada extension. La finalizacion (TM-3-004) sigue pendiente.
9. Si 3 es imposible: 1+2 forman modulo y el contrario se sigue como A Grande.

## D. Ambiguedades todavia abiertas

| ID | Ambiguedad | Impacto |
|---|---|---|
| Q-005 | Limites exactos del retroceso y tamano minimo para considerarlo funcional | El replay usa el extremo de 2 confirmado por la lectura humana (29832,5); derivar automaticamente el final de 2 desde ticks no esta cerrado |
| Q-006 | Toque vs superacion | Resuelto para esta validacion por la decision C de Javier: superacion estricta |
| A1/F1 | High-Low vs desplazamiento direccional | Resuelto por la decision A: desplazamiento funcional |
| E | Alcance exacto de la prohibicion intravela | Se adopta la interpretacion de Javier: solo prohibe confirmar por nuevo extremo sin separacion |
| TM-3-004 | Fin de 3 | No se resuelve; no se inventa |
| N-002/N-005 | Plano: `|delta| <= 0,25` (canonico) vs `< 0,25` (motor) | Hallazgo colateral: el motor rechaza el caso frontera 0,25 |

Nota de honestidad: en el replay, el instante en que termina 2 se toma de la lectura
humana (minimo de 16:20 = 29832,5) y no de un algoritmo, porque el tamano minimo del
retroceso funcional no esta cerrado. Se verifico que toda la informacion usada para
confirmar 3 en 1446 es anterior o igual a 1446.

## E. Matriz teoria frente a implementacion

| Regla canonica | Implementacion actual | Veredicto | Gravedad | Prueba |
|---|---|---|---|---|
| 3 exige 2 confirmada | `WAIT_THREE` solo tras `TWO_CONFIRMED` | Coincide | - | T3-001 |
| Separacion funcional 2/3 | No existe; basta nuevo extremo | Desviacion | Critica | T3-005 |
| Retroceso 0-50 % | No se registra | Desviacion | Critica | T3-002/003 |
| >50 % imposibilita 3 | No existe guarda; confirma igual | Desviacion | Critica | T3-004/T3-008 |
| Toque no confirma | `<` estricto | Coincide | - | T3-001/T3-009 |
| Superacion estricta confirma | Exige estricto **y** >= 2,00 pts | Parcial | Alta | T3-002 |
| Basta 1 tick | Exige 2,00 pts | Desviacion | Critica | T3-006/T3-010 |
| Sin umbral de 2 puntos | `STRUCTURAL_MOVE = 200` | Desviacion | Critica | T3-006 |
| Extension de 2 no es 3 | Extension sin retroceso confirma 3 | Desviacion | Critica | T3-005/T3-012 |
| Extremo de 3 se actualiza | Pata congelada; solo `module_extreme` avanza | Desviacion | Alta | T3-007 |
| Sin informacion futura | Fase viva causal; `_local_123` no causal (muerta) | Parcial | Media | T3-010 |
| Fallo de 3 -> modulo + A | No existe transicion de imposibilidad | Desviacion | Critica | T3-008 |
| Plano `<= 0,25` | `local_two_gate` usa `< 0,25` | Desviacion | Media | hallazgo colateral |

## F. Pruebas ejecutables creadas

Ubicacion: `C:\Users\profesor\OpenBot\Agents\agent-47b92cd3-6213-468e-a63a-aeffa2d8a027\t3_validation\`

- `t3_model.py`: carga el motor congelado por ruta, inyecta el estado canonico previo
  (1 y 2 confirmados) y conduce la fase viva real `_process_local_sequence`.
- `test_t3_canonical.py`: 12 pruebas unittest/pytest (T3-001 a T3-012).
- `replay_1621.py`: replay causal del feed maestro y traza de 22 campos.
- `replay_1621.json`: traza completa y snapshots del motor.

Las pruebas T3-002..T3-009 y T3-011..T3-012 aíslan la compuerta de 3 con el estado
canonico inyectado; T3-010 es extremo a extremo sobre el feed real. No se modifica ni se
conecta `_local_123`.

## G. Resultado de cada prueba contra el motor actual

Comando: `python -m pytest test_t3_canonical.py -v` -> **3 passed, 9 failed**.

| Prueba | Escenario | Esperado | Motor | Resultado |
|---|---|---|---|---|
| T3-001 | retroceso <50 %, toque exacto | 3 no confirma | no confirma | PASA |
| T3-002 | retroceso <50 %, supera 0,25 | 3 confirma | no confirma | FALLA |
| T3-003 | retroceso 50,00 % + superacion | 3 confirma | no confirma | FALLA |
| T3-004 | retroceso 52,85 % + nuevo extremo | 3 imposible + A | confirma 3 | FALLA |
| T3-005 | extension de 2 sin retroceso | 2_EXTIENDE, no 3 | confirma 3 | FALLA |
| T3-006 | superacion 0,25, distancia <2 pts | 3 confirma sin umbral | no confirma | FALLA |
| T3-007 | extension posterior a la confirmacion | pata 3 = 29830,0 | pata 3 = 29830,4 | FALLA |
| T3-008 | fallo de 3 | modulo + A Grande | confirma 3, sin A | FALLA |
| T3-009 | toques repetidos sin superar | 3 no confirma | no confirma | PASA |
| T3-010 | feed real, causalidad | confirma en seq 1446 | confirma en seq 1590 | FALLA |
| T3-011 | intravela con separacion | 3 confirma | no confirma | FALLA |
| T3-012 | intravela sin separacion | 2_EXTIENDE, no 3 | 2 extiende, no 3 | PASA |

## H. Replay completo de 16:21

Precondiciones verificadas:

1. 2 confirmada: evento real, origen 29844,8, extremo de confirmacion 29837,3,
   16:20:14,218 (primer tick que alcanza 7,5 pts = 100 % del 1 de 16:19).
2. Extremo de 2: 29832,5, minimo de 16:20, seq 1314 (16:20:41,153). Coincide con el
   `two_extreme` del motor al cierre de 16:20 y con la lectura humana.
3. Retroceso: 29832,5 -> 29837,0 (seq 1342, 16:20:47,842); 4,5 pts = 36,59 % de 12,3.
4. 36,59 % <= 50 %: retroceso valido.
5. Primer tick inferior a 29832,5: seq 1446, 16:21:14,734, bid 29832,3. No existe ningun
   tick anterior por debajo de 29832,5 tras seq 1314.
6. Sin informacion futura: el ratio 36,59 % y el cruce estan disponibles en 1446.

Traza (extracto; 22 campos completos en `replay_1621.json`):

| seq | hora | bid | two_extreme | size_2 | retr | dist | ratio | rama | motor |
|---|---|---|---|---|---|---|---|---|---|
| 1314 | 16:20:41,153 | 29832,5 | 29832,5 | 1230 | - | 0 | 0,00 | 2_ACTIVA | TWO_CONFIRMED |
| 1316 | 16:20:41,959 | 29832,5 | 29832,5 | 1230 | 29832,8 | 30 | 0,024 | 3_CANDIDATA | TWO_CONFIRMED |
| 1342 | 16:20:47,842 | 29837,0 | 29832,5 | 1230 | 29837,0 | 450 | 0,366 | 3_CANDIDATA | TWO_CONFIRMED |
| 1390 | 16:21:00,048 | 29835,0 | 29832,5 | 1230 | 29837,0 | 450 | 0,366 | 3_CANDIDATA | WAIT_THREE |
| 1445 | 16:21:14,326 | 29832,5 | 29832,5 | 1230 | 29837,0 | 450 | 0,366 | 3_CANDIDATA | WAIT_THREE |
| 1446 | 16:21:14,734 | 29832,3 | 29832,5 | 1230 | 29837,0 | 450 | 0,366 | **3_CONFIRMADA** | **WAIT_THREE** |
| 1590 | 16:21:51,869 | 29830,5 | 29832,5 | 1230 | 29837,0 | 450 | 0,366 | 3_CONFIRMADA | **LOCAL_3_CONFIRMADO** |
| 1601 | 16:21:54,482 | 29830,3 | 29832,5 | 1230 | 29837,0 | 450 | 0,366 | 3_CONFIRMADA | WAIT_A_BAR |

## I. Primer tick canonico de confirmacion

seq 1446 - 16:21:14,734 - bid 29832,3 (superacion estricta por 0,2 pts).

## J. Tick utilizado actualmente por el motor

seq 1590 - 16:21:51,869 - bid 29830,5 (exactamente 2,00 pts por debajo de 29832,5).

## K. Diferencia temporal y matematica

- Tiempo: 37,135 s de retraso (16:21:14,734 -> 16:21:51,869).
- Precio: 1,80 pts de retraso (29832,3 -> 29830,5).
- Causa: `abs(p - ext) >= 200` sustituye a la superacion estricta.
- Fragilidad: si el minimo de la vela hubiera sido 29830,6 (1,9 pts), el motor no habria
  confirmado 3 en absoluto. El golden 16:21 pasa por coincidencia aritmetica exacta.

## L. Comprobacion de actualizacion posterior del extremo

| Momento | `leg3.extreme` | `module_extreme` | Minimo real |
|---|---|---|---|
| 1590 confirmacion | 29830,5 | 29830,5 | 29830,5 |
| 1601 nuevo minimo | **29830,5 (congelado)** | **29830,3 (actualizado)** | 29830,3 |

La pata 3 de `local_sequences[0].legs[2]` conserva 29830,5; el modulo avanza a 29830,3.
La confirmacion es correcta en nivel, pero la pata no representa el extremo funcional
final de 3.

## M. Auditoria de `_local_123` (R3 498-537, muerta)

Reglas contenidas:

1. 1: `span = b1.high - b1.low`; exige `span >= MOVE` (6,00 pts).
2. Direccion segun `b1.last` vs `b1.open`.
3. 2: cola inicial `<= 0,25`; apertura plana `abs(open_2 - close_1) < 0,25`.
4. 2: `abs(open_2 - extremo_2) >= span(1)` (el movimiento 2 cubre el tamano de 1).
5. 3: `b3.extremo` estrictamente mas alla de `b2.extremo` (`>=`/`<=` rechazan el toque).
6. Modulo: origen = extremo de 1; extremo = extremo de 3.

Correcto segun la definicion canonica:

- Superacion estricta del extremo de 2 (regla 5).
- Apertura plana y cola inicial (reglas 3).
- Exigir que 2 cubra el tamano de 1 (regla 4), con la salvedad de la medida.

Incorrecto o antiguo:

- Mide 1 por High-Low (`span`) en lugar de desplazamiento direccional (A1).
- Compara el tamano de 2 contra el High-Low de 1: si 1 tiene cola, exige de mas.
- No comprueba retroceso 0-50 %.
- No distingue 2_EXTIENDE de 3: cualquier vela siguiente con nuevo extremo es 3.
- Usa velas cerradas: el extremo de 3 es el minimo/maximo de la vela, no el primer tick
  de superacion; confirma con informacion posterior al cruce (retro-fit).
- Origen de 3 = `b3.open`, no el extremo del retroceso.
- Frontera plana: rechaza `abs(delta) == 0,25`, que el canonico considera plano.

Diferencias respecto a `WAIT_THREE`:

| Aspecto | `_local_123` | `WAIT_THREE` |
|---|---|---|
| Nivel | Vela cerrada | Tick |
| Confirmacion | Extremo de la vela 3 | `p - ext >= 2,00 pts` |
| Retroceso | No | No |
| Extension de 2 | La llama 3 | La llama 3 |
| Extremo de 3 | Extremo de vela (futuro) | Precio de confirmacion (congelado) |
| Uso | Muerta | Viva |

Por que no esta conectada: R3 sustituyo el reconocimiento por velas por una maquina de
estados tick a tick para preservar causalidad; `_local_123` no puede emitir el tick de
confirmacion y su origen/extremo no coinciden con la secuencia viva.

Riesgo de mantenerla: dos definiciones divergentes de 3 en el mismo archivo; si alguien
la reconecta, cambia resultados sin pruebas; induce a auditorias erroneas.

Recomendacion: reutilizar parcialmente (reglas 3 y 5) en la nueva compuerta, migrar la
medida a desplazamiento direccional, y eliminarla solo despues de que T3-001..T3-012
pasen y exista sustituto probado. No eliminarla ahora.

## N. Archivos que necesitarian modificacion posterior

1. `python/TM_CORE_PYTHON_v0752_CANONICAL.py`
   - `local_two_gate` (478-480): frontera `<= 0,25`.
   - `_local_123` (498-537): codigo muerto a retirar tras cobertura.
   - `_close_candidate_bar` (2425-2461): `span >= MOVE` para 1 local.
   - `_process_local_sequence` TWO_CONFIRMED (2557-2563), WAIT_THREE (2565-2574),
     WAIT_A_BAR (2576-2588).
   - Transicion al cierre de vela (2779-2788).
2. `05_TESTS`: incorporar la suite T3 como pruebas del paquete (no ahora).
3. Documentacion: estado de N-009/N-010 y de T-007..T-010 (no ahora).

## O. Propuesta minima de correccion (sin implementar)

1. Anadir al estado local: `two_origin`, `two_size`, `retr_extreme`, `retr_active`,
   `three_origin`, `three_confirmation_level`, `three_state`.
2. Al confirmar 2: fijar `two_origin = two_open`; actualizar `two_extreme` solo mientras
   no exista retroceso funcional.
3. En `WAIT_THREE`:
   - si el precio avanza en la direccion de 2 y no hay retroceso: `2_EXTIENDE`;
   - si retrocede: actualizar `retr_extreme` y `ratio`;
   - si `ratio > 0,50`: `THREE_IMPOSSIBLE` -> cerrar modulo 1+2 y abrir A Grande desde el
     extremo, sin crear 3;
   - si `retr_active` y el precio supera estrictamente `two_extreme`: confirmar 3 en ese
     tick, sin umbral de 2,00 pts.
4. Permitir la confirmacion dentro de la vela de 2 solo si la secuencia completa esta
   registrada; en caso contrario, mantener el paso a `WAIT_THREE` al cierre.
5. Al confirmar: guardar nivel y tick; en cada extension posterior actualizar tambien
   `leg3.extreme` (no solo `module_extreme`).
6. No fijar el fin de 3: TM-3-004 sigue abierto.

## P. Riesgos de regresion

- El cambio de umbral adelanta 3 de 1590 a 1446 en 16:21; cambia el extremo del modulo,
  el objetivo TT y la genealogia A/AUT posterior (16:22).
- Introducir la guarda del 50 % puede reclasificar casos hoy aceptados como 3.
- Permitir intravela aumenta el numero de secuencias locales y puede alterar la
  dominancia de lecturas.
- Cambiar la frontera `0,25` afecta a la compuerta de 2 y a T-004/T-037/T-038.
- `_local_123` no debe conectarse: duplicaria la maquina de estados.

## Q. Gates que deberan repetirse tras autorizar la correccion

Ejecutar siempre sobre una copia nueva, nunca sobre el ZIP congelado bajo auditoria:

1. `python -m pytest t3_validation/test_t3_canonical.py -q` -> 12/12.
2. `python -m pytest -q tests/legacy_v075/TM_CORE_PYTHON_v075_TESTS.py` -> 20/20.
3. `python tests/test_big_b_aut.py`.
4. `python tests/test_transformations.py`.
5. `python repro/run_transition_prefixes.py` -> `prefix_failures = 0`.
6. `python python/TM_CORE_PYTHON_v0752_CANONICAL.py --selftest`.
7. `python repro/run_all.py` -> salida 2 solo por la divergencia 16:23 documentada.
8. Replay 16:21 -> confirmacion canonica en seq 1446 y pata 3 con extremo 29830,3.
9. Verificar SHA-256 del motor y del ZIP; emitir version y ZIP nuevos.

## Estado final

VALIDACION COMPLETA. Motor no modificado (SHA coincide con manifest). Arbol, goldens y
reglas intactos. TM-3-004 no resuelto. No se implementa la correccion.

Se solicita autorizacion para pasar de VALIDACION a CORRECCION DEL MOTOR.
