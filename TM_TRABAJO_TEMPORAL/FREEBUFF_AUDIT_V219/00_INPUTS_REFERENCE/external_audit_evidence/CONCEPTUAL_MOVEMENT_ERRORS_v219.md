# CONCEPTUAL_MOVEMENT_ERRORS_v219

**Diagnóstico conceptual del motor R5 frente al árbol TM v2.19**
**Estado:** `WORKING / NO CONGELADO / SIN CORRECCIONES DE CÓDIGO`
**Fecha:** 2026-10-30
**Autoridad experta:** Javier (una sola).
**Documentos base:** `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md` (`94A1408A…`), motor `TM_CORE_PYTHON_v0752_CANONICAL_R5.py` (`9BD1BEDB…`, sin modificar), `CHECKPOINT_15_TRANSICIONES.md`, `DUDAS_ESTRUCTURALES_PENDIENTES_v219.md`.

Este documento no propone parches. Intenta responder, antes de tocar una línea: **qué movimiento está interpretando mal el motor, qué concepto TM no entiende, por qué ese concepto produce el fallo y qué principio universal lo gobierna.** Las correcciones técnicas aparecen solo al final y como propuesta posterior, subordinadas a las respuestas de Javier.

---

## 0. Método y alcance

- Se recorrieron las 15 transiciones constitucionales, los nodos N-001 a N-040 y las dos máquinas que hoy ejecutan el motor (`PRIMARY` por movimientos y `LOCAL` por ticks).
- Cada divergencia se separa en **síntoma**, **error local** y **error conceptual**. El error local se cita con línea; el conceptual se agrupa.
- Se añadió una **traza sintética de auditoría** (7 ticks, precios inventados a propósito, sin relación con el feed real) para observar el comportamiento sin depender de fixtures ni de la lectura humana. No es un golden y no debe convertirse en uno.
- Prohibido en este paso: modificar el motor, adaptar tests, convertir una vela en condición, o elegir rama por conveniencia.

Traza usada como evidencia (precios en centésimas):

```text
seq:      1       2       3       4       5       6       7
price: 100000  100800  100000  100800  101300  100600  101200
```

Salida real del motor (eventos filtrados):

```text
seq3  LECTURA_CREADA R0001  MODULE     FIRST
seq4  A_INICIO       R0001  A          MOVIMIENTO_CONTRARIO
seq5  B_GRANDE       R0001  TT_PENDING B100_TICK_EXACTO
seq5  AUT            R0001  AUT        SUPERA_127_MAS_025
seq6  B_INICIO       R0001  B          CONTRARIO_A_A
seq6  TT_100         R0001  TT_EXT     price=100800 (conocido en 100600)
seq6  LECTURA_CREADA R0002  MODULE     B_CONFIRMADA_NEW1
seq6  C              R0001  TT_EXT     CONTRARIO_POST_B_GRANDE_SIN_C_CANDIDAT
seq7  FT             R0001  DONE       CONTRARIO_DESPUES_DE_TT
seq7  A_INICIO       R0002  A          MOVIMIENTO_CONTRARIO
```

En siete ticks el motor: confirma B Grande y AUT en el mismo tick; confirma TT cuando el precio ya había caído 5,00 puntos desde el extremo; emite una `C` sobre una lectura cuyo estado sigue siendo `TT_EXT`; cierra el FT; y abre una segunda lectura `R0002` en el mismo tick. Ese encadenamiento es el síntoma de los errores conceptuales que siguen.

---

## 0.1 Mapa de conceptos

| ID | Concepto no comprendido | Fallos | Nodos | Gravedad |
|---|---|---|---|---|
| CE-1 | El tamaño sustituye a la finalidad | F-01..F-05 | N-001, N-006..N-015, N-022, N-026, N-040 | Crítica |
| CE-2 | Función, patrón y estado mezclados en un solo nivel | F-06 | N-017..N-021, N-024..N-026, N-031, N-034 | Crítica |
| CE-3 | No hay una autoridad única de "qué función viene ahora" | F-07, F-08 | N-006..N-011, N-018..N-021, N-036 | Crítica |
| CE-4 | Escalas y referencias concurrentes confundidas | F-09 | N-012, N-014, N-018, N-028..N-030, N-034 | Alta |
| CE-5 | Tiempo estructural y momento de conocimiento | F-10 | N-013, N-019, N-021, N-026, N-039 | Alta |
| CE-6 | El gap tratado como anomalía de datos | F-11 | N-002..N-004 | Alta |
| CE-7 | Transformación funcional no nombrada (A/C usadas como tendencia) | F-12 | N-017, N-024, N-025, v2.17, v2.19 | Media |

Siete conceptos explican las doce divergencias principales. No hay doce errores independientes.

---

## 1. CE-1 — El tamaño sustituye a la finalidad

**Concepto ausente.** El árbol pregunta *qué función cumple este movimiento dentro de la estructura activa*. El motor pregunta *cuántos puntos se movió*. Todo lo demás se deriva de ahí: `MovementBuilder(min_move=6,00, retrace=25 %)` convierte el flujo de ticks en "movimientos", y cada movimiento cerrado dispara una decisión funcional. La consecuencia es que una vibración grande adquiere autonomía y una función legítima pequeña no existe.

### F-01 — El 1 es una vela entera, no un movimiento

- **MOVIMIENTO OBSERVADO:** la primera vela del tramo (por ejemplo, una vela de 8,00 puntos con mecha superior e inferior) se convierte en el `1` del ciclo.
- **ESTADO ESTRUCTURAL RECIBIDO:** `SIN_LECTURA`.
- **LECTURA DEL ÁRBOL:** N-001: primer movimiento direccional con referencia válida, **sin rango mínimo teórico**; N-040: la medida es **desplazamiento direccional**, no `High−Low`; y v2.5 §D (rango 5, R5:1291-1303): «La lectura TM se realiza siempre, sin importar el tamaño»; 6,00 es solo filtro de la futura capa operativa.
- **LECTURA DEL PYTHON:** `_close_candidate_bar` fija `origin,extreme = (bar.low,bar.high)` y `one_size = span` (R5:2796-2800); exige `span ≥ 6,00` (R5:2797). El `1` nace solo después de un AUT previo (R5:2784-2790), al cerrar la vela siguiente.
- **PRIMERA DIVERGENCIA CAUSAL:** el tick de apertura de esa vela, que debería iniciar el `1` direccional, no hace nada; la decisión se toma al cierre, con el high-low completo.
- **SÍNTOMA:** `1` de tamaño inflado, dirección igual al neto de la vela, y ciclos que no empiezan hasta que hay un AUT anterior.
- **ERROR LOCAL:** `origin,extreme=(bar.low,bar.high)` + `span<MOVE: return` (R5:2797-2800).
- **ERROR CONCEPTUAL:** confunde **contenedor temporal** (la vela) con **contenido funcional** (el movimiento direccional). La vela es el marco donde se observa; no es la función.
- **POR QUÉ FALLA:** al usar el rango total de la vela, el `1` incluye recorridos que pertenecen a la ida y a la vuelta; su medida deja de ser comparable con `2` y contamina todas las proporciones posteriores (100 %, 127 %).
- **PRINCIPIO UNIVERSAL AFECTADO:** una función se mide por su **desplazamiento direccional** entre su origen y su extremo, no por el envolvente de la vela.
- **OTROS CASOS AFECTADOS:** 2 (hereda la medida), 3, A Grande, B Grande, TT (target), y cualquier comparación entre velas de distinta volatilidad.
- **PREGUNTA EXPERTA:** ver Q2 (sección 8).
- **PRUEBA CONCEPTUAL NECESARIA:** positivo: vela con mecha contraria grande que contiene un `1` direccional claro; negativo: vela grande sin dirección (no hay `1`); frontera: `1` de 5,99 puntos direccionales (el árbol lo admite, el motor no).
- **CORRECCIÓN TÉCNICA POSIBLE (posterior):** derivar `1` del primer tramo direccional con referencia, no del high-low; eliminar el mínimo absoluto.

### F-02 — Cualquier vibración de 2,00 o 6,00 puntos abre función

- **MOVIMIENTO OBSERVADO:** dentro de una `2` candidata, una oscilación contraria de 2,00 puntos (o un retroceso de 6,00) abre una `A` y luego una `B`.
- **ESTADO ESTRUCTURAL RECIBIDO:** `2_CANDIDATA` (o `LOCAL_2_CONFIRMADO`).
- **LECTURA DEL ÁRBOL:** mientras la vela de `2` siga cumpliendo N-006/N-007, las vibraciones internas no dividen `2`; N-032 prohíbe fragmentar por micromovimiento y el propio ejemplo de la aclaración lo exige.
- **LECTURA DEL PYTHON:** `_open_candidate` crea `A_SIGNIFICATIVA` con cualquier excursión contraria ≥ 2,00 cuando `A ≥ 75 %` (R5:1450-1470); `A_DESPROPORCIONADA_MODULO` con `A > 2 × módulo` (R5:1533); en LOCAL, `A_CANDIDATE` se abre con **cualquier** tick contrario (R5:3113-3115) y se eleva a `A` con ≥ 6,00 (R5:3142).
- **PRIMERA DIVERGENCIA CAUSAL:** el primer tick contrario dentro de `2`, que el árbol absorbe.
- **SÍNTOMA:** A Grande creada dentro de 2; módulo partido en dos; `2` desaparece de la lectura activa sin haber fallado.
- **ERROR LOCAL:** umbrales `A_SIGNIFICANT`/`A_MAX_MODULE_MULTIPLE` (R5:1450-1470, R5:1533) y `A_CANDIDATE` por tick (R5:3113).
- **ERROR CONCEPTUAL:** confunde **movimiento estructural físico** con **autonomía funcional**. Superar 2,00 prueba que hay recorrido, no que haya función nueva.
- **POR QUÉ FALLA:** el motor no tiene un estado "vibración absorbida"; toda excursión se convierte en candidata y la primera que supera un umbral gana.
- **PRINCIPIO UNIVERSAL AFECTADO:** la autonomía de un movimiento se decide por la **función que intenta completar y la referencia que rompe**, no por su tamaño.
- **OTROS CASOS AFECTADOS:** oscilaciones dentro de A, retrocesos internos de B, extensión de AUT, continuidad entre velas, y `C` que nace con 6,00 (R5:3207).
- **PREGUNTA EXPERTA:** Q2 y Q5.
- **PRUEBA CONCEPTUAL NECESARIA:** positivo: `2` con vibración de 3,00 que luego alcanza el 100 % de `1` → sigue siendo `2`; negativo: giro que rompe el origen de `1` → deja de ser `2`; frontera: vibración que alcanza exactamente 6,00 sin romper referencia.
- **CORRECCIÓN TÉCNICA POSIBLE (posterior):** una política única de absorción mientras la función esperada conserve su condición de confirmación.

### F-03 — El 3 se mide por magnitud, no por regularidad

- **MOVIMIENTO OBSERVADO:** tras `2` confirmado, cualquier nuevo extremo 2,00 puntos mayor se declara `3`.
- **ESTADO ESTRUCTURAL RECIBIDO:** `2_CONFIRMADA`.
- **LECTURA DEL ÁRBOL:** N-009/N-010: `3` exige **retroceso 0-50 % del rango de 2** *y* superación del extremo de 2.
- **LECTURA DEL PYTHON:** `WAIT_THREE` solo exige `new_extreme and abs(...) ≥ STRUCTURAL_MOVE` (R5:3082-3084); el propio motor escribe `provisional_rule = medida_de_3_no_definida` (R5:3094).
- **PRIMERA DIVERGENCIA CAUSAL:** el tick del nuevo extremo, sin haber evaluado antes el retroceso.
- **SÍNTOMA:** `3` confirmados con retrocesos del 80 %; módulos regulares que no lo son; `1+2` que nunca se cierra como módulo por descarte.
- **ERROR LOCAL:** `abs(p.price - ext.price) >= STRUCTURAL_MOVE` (R5:3083).
- **ERROR CONCEPTUAL:** sustituye una **condición de regularidad** (el retroceso relativo) por una **condición de tamaño** (2,00).
- **POR QUÉ FALLA:** el árbol mide el retroceso para saber si la secuencia sigue siendo modular; el motor solo mira si el extremo avanzó.
- **PRINCIPIO UNIVERSAL AFECTADO:** la regularidad del módulo se mide en proporción al movimiento previo, no en puntos absolutos.
- **OTROS CASOS AFECTADOS:** módulo 1+2 vs 1+2+3, `module_kind`, medida del módulo (F-04), y toda la cadena A/B/C que depende de él.
- **PREGUNTA EXPERTA:** Q5.
- **PRUEBA CONCEPTUAL NECESARIA:** positivo: retroceso 30 % + nuevo extremo → `3`; negativo: retroceso 70 % + nuevo extremo → módulo `1+2` + A Grande; frontera: retroceso exactamente 50 %.
- **CORRECCIÓN TÉCNICA POSIBLE (posterior):** añadir la condición de retroceso relativo, no un umbral nuevo.

### F-04 — El módulo es un tramo, no un rango de expansión

- **MOVIMIENTO OBSERVADO:** el módulo se guarda como `origen→extremo` del `1` (y luego del `2`).
- **ESTADO ESTRUCTURAL RECIBIDO:** `MODULE`/`LOCAL_MODULE`.
- **LECTURA DEL ÁRBOL:** N-012: `rango_modulo = max(highs) − min(lows)` de **todas las velas del conjunto**.
- **LECTURA DEL PYTHON:** `module_origin/module_extreme` son los extremos del tramo (`_make_local_reading` R5:2716-2723; `module_extreme=p.price` R5:3038) y `module_size = |extreme − origin|`.
- **PRIMERA DIVERGENCIA CAUSAL:** la construcción del módulo, antes de cualquier A.
- **SÍNTOMA:** módulos más pequeños que su expansión real; objetivos TT más cortos; porcentajes 100/127 calculados sobre una base menor.
- **ERROR LOCAL:** `module_size` derivado de dos puntos, no de max/min de velas.
- **ERROR CONCEPTUAL:** confunde **trayectoria** con **expansión**. El módulo es el espacio recorrido por el conjunto, no la recta entre dos extremos.
- **POR QUÉ FALLA:** con mechas o solapes, la expansión incluye precios que la recta no toca; el motor los ignora y subestima el módulo.
- **PRINCIPIO UNIVERSAL AFECTADO:** el módulo se mide por el **rango de expansión** del conjunto, no por su diagonal.
- **OTROS CASOS AFECTADOS:** target TT (F-09), B Grande 100/127 (F-05), CUT por base del módulo (Q1), A desproporcionada.
- **PREGUNTA EXPERTA:** Q4 (y Q1).
- **PRUEBA CONCEPTUAL NECESARIA:** positivo: tres velas solapadas cuya expansión supera la diagonal; negativo: tres velas monótonas (coinciden); frontera: mecha que amplía el rango sin cambiar extremos del tramo.
- **CORRECCIÓN TÉCNICA POSIBLE (posterior):** calcular el módulo como rango del conjunto de velas que lo componen.

### F-05 — El FT nace de un retroceso de 6,00, no de una pérdida de estructura

- **MOVIMIENTO OBSERVADO:** tras el TT, la primera pierna contraria de 6,00 puntos se etiqueta `FT`.
- **ESTADO ESTRUCTURAL RECIBIDO:** `TT_EXT`.
- **LECTURA DEL ÁRBOL:** N-026: FT exige pérdida de velocidad y movimiento contrario claro, con referencia y desplazamiento **PENDIENTE_JAVIER**.
- **LECTURA DEL PYTHON:** `TT_EXT` con `movement.direction != r.direction` → `FT` (R5:1327-1346); el umbral es el mismo `MOVE` del constructor.
- **PRIMERA DIVERGENCIA CAUSAL:** el tick en que el retroceso alcanza 6,00.
- **SÍNTOMA:** FT prematuros o tardíos según la volatilidad; el TT se cierra antes de que el árbol lo declare terminado.
- **ERROR LOCAL:** reutilizar `MOVE` como condición de FT (R5:1327).
- **ERROR CONCEPTUAL:** la finalización de un patrón se decide por tamaño, cuando el árbol la define por **pérdida de la estructura del TT**.
- **POR QUÉ FALLA:** el motor no distingue "retroceso interno del TT" de "FT"; ambos son movimientos contrarios y solo cambia el umbral.
- **PRINCIPIO UNIVERSAL AFECTADO:** un patrón termina cuando **deja de cumplirse su estructura**, no cuando el precio retrocede una cantidad fija.
- **OTROS CASOS AFECTADOS:** TT extendido (v1.2), FT multi-vela, cierre de lectura, y la genealogía del ciclo siguiente.
- **PREGUNTA EXPERTA:** Q4.
- **PRUEBA CONCEPTUAL NECESARIA:** positivo: TT extendido y retroceso que conserva estructura → sigue TT; negativo: retroceso que rompe el origen del tramo final → FT; frontera: retroceso de 6,00 sin pérdida de estructura.
- **CORRECCIÓN TÉCNICA POSIBLE (posterior):** definir FT por referencia estructural, no por `MOVE`; mantener la regla abierta hasta Q4.

---

## 2. CE-2 — Función, patrón y estado en el mismo nivel

**Concepto ausente.** El árbol separa **movimientos** (1, 2, 3, A, B, C, AUT, CUT) de **patrones** (TT, FT). El motor los guarda en el mismo campo `Reading.state` (`MODULE`, `A`, `B_CAND`, `TT_PENDING`, `C`, `TT_EXT`, `DONE`) y en `fail_reason`. Eso hace que un patrón "sea" la función y que un cierre sea un estado.

### F-06 — TT/FT/CUT como estados y no como patrones/eventos

- **MOVIMIENTO OBSERVADO:** la traza sintética emite `C` sobre `R0001` cuando su estado sigue siendo `TT_EXT`; después `FT` la pasa a `DONE`; `CUT` cierra con `fail_reason`.
- **ESTADO ESTRUCTURAL RECIBIDO:** `TT_PENDING`/`TT_EXT` (patrón) conviviendo con `A`/`B`/`C` (funciones).
- **LECTURA DEL ÁRBOL:** N-034 separa tres funciones de C (CUT, C = nuevo 1, C = A Grande de lectura mayor); v1.2 §13.6 exige separar movimientos de patrones; N-031 cierra por TT, CUT, invalidación o reclasificación, conservando historial.
- **LECTURA DEL PYTHON:** `state` mezcla ambos niveles; `C` se emite con `new_state=TT_EXT` (evidencia); `CUT` no es un estado propio sino `state=DONE` + `fail_reason="CUT_..."`; `FT` es `ft=True` + `DONE`; la tercera función de C (A Grande de lectura mayor) no existe.
- **PRIMERA DIVERGENCIA CAUSAL:** la primera vez que un patrón se escribe en `state`.
- **SÍNTOMA:** funciones que desaparecen al confirmarse un patrón; C que no puede seguir siendo C después del TT; CUT que no se puede consultar como función; lectura cerrada sin poder distinguir "cerró por FT" de "cerró por CUT" salvo por texto libre.
- **ERROR LOCAL:** `r.state="TT_PENDING"` / `"TT_EXT"` / `"DONE"` y `fail_reason` como sustituto de estado.
- **ERROR CONCEPTUAL:** no distingue **qué es** la estructura (función) de **qué patrón la recorre** (TT/FT) de **qué evento la cierra** (CUT/AUT/invalidación).
- **POR QUÉ FALLA:** al compartir un solo campo, confirmar un patrón sobrescribe la función; y cerrar la lectura impide seguir midiendo C como función de la lectura mayor.
- **PRINCIPIO UNIVERSAL AFECTADO:** función, patrón y evento son **capas distintas** y pueden coexistir; ninguna borra a la otra.
- **OTROS CASOS AFECTADOS:** N-017/N-018/N-021 (AUT/TT/nuevo 1), N-024/N-025 (CUT/nuevo 1), N-034 (tres funciones de C), N-031 (cierre), y las lecturas concurrentes (CE-4).
- **PREGUNTA EXPERTA:** Q1 y Q3 (la separación de capas decide qué puede convivir).
- **PRUEBA CONCEPTUAL NECESARIA:** positivo: C Grande que sigue siendo C mientras el TT de la lectura mayor está activo; negativo: CUT que cierra sin borrar el historial de C; frontera: TT y CUT en el mismo tick.
- **CORRECCIÓN TÉCNICA POSIBLE (posterior):** separar `function`, `pattern`, `lifecycle_event` en el modelo de lectura.

---

## 3. CE-3 — No hay una autoridad única de "qué función viene ahora"

**Concepto ausente.** El árbol define una función esperada por estado (después de 1 → 2; después de 2 → 3; después de 3 → A; después de A → B; después de B Grande → C). El motor tiene **dos** autoridades que responden distinto y se ejecutan ambas en el mismo tick: `_process_local_sequence` (fases) y `_legacy_tick_decision` (reglas heredadas), más `_update` de la máquina base. La consecuencia no es solo duplicación: es que "pendiente" e "imposible" se deciden con criterios distintos según quién responda.

### F-07 — Dos máquinas, dos expectativas, dos ciclos

- **MOVIMIENTO OBSERVADO:** el mismo tramo produce una lectura `R####` (PRIMARY) y una `LR####` (LOCAL), con `1`, `2`, `A`, `B`, `CUT` calculados por reglas distintas.
- **ESTADO ESTRUCTURAL RECIBIDO:** cualquier lectura activa.
- **LECTURA DEL ÁRBOL:** una sola lectura dominante por escala, con concurrencia regulada (N-028/N-029) y prioridad explícita (N-030, pendiente).
- **LECTURA DEL PYTHON:** `CanonicalEngine.feed_chunk` ejecuta `_process_movement` (R5:3436), `_advance_primary_question` (R5:3437), `_record_knowledge`, `_snapshot_state` y `_process_local_sequence` (R5:3455) sobre el mismo tick; cada una puede crear o cerrar lecturas.
- **PRIMERA DIVERGENCIA CAUSAL:** el primer tick en que ambas máquinas tienen una lectura activa.
- **SÍNTOMA:** dos nuevos 1 por un mismo CUT (traza: `R0002` creado en el tick del FT), dominancia que cambia dos veces, `C` emitida sobre una lectura que la otra máquina ya cerró.
- **ERROR LOCAL:** ejecución secuencial de dos motores completos sin árbitro (R5:3436-3455).
- **ERROR CONCEPTUAL:** no existe **una** autoridad que responda "qué función viene ahora" con la referencia de la lectura; hay dos que responden por su cuenta.
- **POR QUÉ FALLA:** cada máquina tiene su propia noción de módulo, de B Grande y de cierre; al convivir, una contradice a la otra y ambas escriben el estado.
- **PRINCIPIO UNIVERSAL AFECTADO:** para cada lectura hay **una sola** función esperada y **una sola** condición de confirmación en cada tick.
- **OTROS CASOS AFECTADOS:** todo el mapa; en especial N-017..N-021, N-022..N-025, N-030, N-034.
- **PREGUNTA EXPERTA:** no requiere teoría nueva; requiere decisión de arquitectura (sección 10). La teoría afectada es Q1/Q3.
- **PRUEBA CONCEPTUAL NECESARIA:** una sola lectura por tick con `next_function` único y trazable; la misma traza no puede producir dos ciclos.
- **CORRECCIÓN TÉCNICA POSIBLE (posterior):** retirar una de las dos máquinas del camino operativo (dejando la otra en legacy), no fusionarlas a ciegas.

### F-08 — "Pendiente" e "imposible" se confunden

- **MOVIMIENTO OBSERVADO:** un `2` que no se confirmó en su vela sigue pendiente indefinidamente; en cambio, una `A` que aún podía confirmarse se declara fallida por un retroceso de 6,00; y un TT que aún podía alcanzarse se declara `TT_FALLIDO` al cruzar `fin_A + 2,00`.
- **ESTADO ESTRUCTURAL RECIBIDO:** `POSSIBLE_TWO`, `A_CANDIDATE`, `TT_PENDING`.
- **LECTURA DEL ÁRBOL:** N-007 permite que `2` siga candidata mientras cumpla sus condiciones, pero N-006/N-007 la describen en su vela; N-008 solo la declara imposible cuando falla **una condición de N-006**; N-020 declara TT fallido al **tocar** `fin_A`; N-011 declara 3 fallido por retroceso > 50 % o no superar el extremo.
- **LECTURA DEL PYTHON:** `2` se prorroga entre velas (R5:3048-3071) y solo se declara imposible por gap/cola/ruptura 6,00; `A_CANDIDATE` se declara absorbida al volver al origen (R5:3155-3161) sin evaluar si aún podía confirmarse; `TT_FALLIDO` exige cruzar `a_end ± 2,00` (R5:1291-1293).
- **PRIMERA DIVERGENCIA CAUSAL:** el primer tick en que el motor decide "imposible" sin que se haya negado la condición canónica.
- **SÍNTOMA:** funciones que mueren antes de tiempo y funciones que sobreviven fuera de su marco; el estado deja de ser interpretable.
- **ERROR LOCAL:** tres criterios distintos de imposibilidad (prórroga, absorción, buffer).
- **ERROR CONCEPTUAL:** no distingue **"todavía no confirmado"** de **"ya no puede confirmarse"**. Son dos estados lógicos distintos; el motor usa uno solo.
- **POR QUÉ FALLA:** sin una condición de imposibilidad canónica por función, el motor la inventa con umbrales y con el paso del tiempo.
- **PRINCIPIO UNIVERSAL AFECTADO:** una función permanece pendiente mientras **exista al menos un camino** para cumplir su condición; se vuelve imposible solo cuando **la condición queda negada**, y entonces se activa la rama de fallo que el árbol fija.
- **OTROS CASOS AFECTADOS:** N-008 (módulo por descarte), N-011 (1+2), N-020 (TT fallido → módulo + A), N-035 (invalidación), N-036 (2 no se borra).
- **PREGUNTA EXPERTA:** Q5 (marco temporal de 2/3) y Q4 (tick de TT fallido).
- **PRUEBA CONCEPTUAL NECESARIA:** positivo: `2` que no confirma y luego rompe el origen → módulo por descarte + A; negativo: `2` que no confirma pero sigue dentro de condiciones → sigue pendiente; frontera: `2` que confirma justo al cierre de su vela.
- **CORRECCIÓN TÉCNICA POSIBLE (posterior):** una tabla de imposibilidad por función, derivada del árbol, sin umbrales nuevos.

---

## 4. CE-4 — Escalas y referencias concurrentes

**Concepto ausente.** El árbol admite lectura dominante, módulo principal, mini módulo y lecturas locales, cada una con su referencia, y prohíbe mezclarlas. El motor usa un único `module_size` para todo (target TT, ranking de propietario, límite 3) y una sola bandera `dominant`.

### F-09 — Una referencia para todas las escalas

- **MOVIMIENTO OBSERVADO:** el target del TT se calcula con el módulo del `1` de la lectura, no con el rango del módulo que corresponde; el propietario de un tick se elige por `module_size`; la tercera función de C (A Grande de lectura mayor) no existe.
- **ESTADO ESTRUCTURAL RECIBIDO:** varias lecturas activas (`R####`, `LR####`).
- **LECTURA DEL ÁRBOL:** N-018 (`fin_A ± rango_módulo`), N-029 (L3 solo con regla expresa), N-030 (prioridad pendiente), N-034 (C puede ser A Grande de una lectura mayor).
- **LECTURA DEL PYTHON:** `tt_target = a_end + direction*module_size` (R5:1008, 2910); `_owner` ordena por `module_size` (R5:1575-1581); `_make_local_reading` exige un único dominante (R5:2706-2707).
- **PRIMERA DIVERGENCIA CAUSAL:** el cálculo del target al confirmar B Grande.
- **SÍNTOMA:** TT demasiado cerca o demasiado lejos; un tick atribuido a la lectura equivocada; C que cierra la lectura mayor en vez de alimentarla.
- **ERROR LOCAL:** `module_size` sin cualificar y `_owner` por tamaño.
- **ERROR CONCEPTUAL:** trata **escala** y **referencia** como si fueran una sola cosa; no hay identidad de referencia por lectura.
- **POR QUÉ FALLA:** dos lecturas pueden tener módulos distintos; usar el mismo campo para ambas mezcla niveles y hace que la dominancia dependa del tamaño, no de la estructura.
- **PRINCIPIO UNIVERSAL AFECTADO:** cada lectura tiene su propia referencia y su propio módulo; la dominancia se decide por estructura, no por tamaño.
- **OTROS CASOS AFECTADOS:** N-012, N-014, N-028..N-030, N-034, TT/FT.
- **PREGUNTA EXPERTA:** Q4 (referencia del target) y Q3 (qué lectura posee el módulo tras AUT).
- **PRUEBA CONCEPTUAL NECESARIA:** positivo: dos lecturas con módulos distintos y TT calculado con el de cada una; negativo: lectura local que no altera el target de la principal; frontera: mismo tick reclamado por dos lecturas.
- **CORRECCIÓN TÉCNICA POSIBLE (posterior):** referencias explícitas por lectura y una política de dominancia no basada en tamaño.

---

## 5. CE-5 — Tiempo estructural y momento de conocimiento

**Concepto parcialmente comprendido.** El motor sí separa `structural_time`, `confirmation_time` y `knowledge_time` en los eventos y en `knowledge_audit`, y eso es correcto. El fallo está en **cuándo decide**: las decisiones se toman al cerrar un movimiento o una vela, y luego se les asigna la hora del tick encontrado. El estado intermedio no existe, y el objetivo `STATE_KNOWLEDGE_CORRECT_AT_EVERY_TICK` se rompe.

### F-10 — TT/FT y nuevos 1 decididos en el cierre, no en el tick

- **MOVIMIENTO OBSERVADO (traza):** el precio alcanza el objetivo TT en 100800 (seq4), cae a 100600 (seq6) y **entonces** el motor emite `TT_100` con `price=100800` y conocimiento seq6; en el mismo tick crea `R0002`. El FT se emite en seq7.
- **ESTADO ESTRUCTURAL RECIBIDO:** `TT_PENDING` desde seq5.
- **LECTURA DEL ÁRBOL:** N-019: el TT se confirma en el tick que alcanza el objetivo (mismo tick permitido); N-039: `precio ≥ objetivo`; N-021: el nuevo 1 nace en el movimiento que completa el TT; N-026: FT exige pérdida de estructura.
- **LECTURA DEL PYTHON:** `_check_tt` solo se invoca al procesar un movimiento y barre `origin_index..extreme_index` (R5:1030-1038); `_process_local_sequence` se evalúa por fases con `newbar`; el nuevo 1 se crea **en todo AUT** como dominante (R5:2854). Matiz de precedencia: si el AUT nace por cruce de la base del módulo, v2.3 §F exige el nuevo 1 en ese mismo movimiento; si nace por 127 %, N-017 solo autoriza un nuevo 1 **candidato** y v1.2 §13.7.9 sitúa el nuevo 1 + reset al confirmar el TT al 100 %. R5 no distingue ambos caminos.
- **PRIMERA DIVERGENCIA CAUSAL:** seq4, el tick que alcanza 100800; el motor no decide nada.
- **SÍNTOMA:** confirmaciones retroactivas; estados que "saltan" dos funciones en un tick; lecturas nuevas creadas por el cierre de un movimiento y no por el evento canónico.
- **ERROR LOCAL:** granularidad de decisión = movimiento/vela; `_check_tt` fuera de `feed_chunk`; nuevo 1 confirmado en todo AUT sin distinguir el camino.
- **ERROR CONCEPTUAL:** confunde **cuándo ocurrió el hecho estructural** con **cuándo el motor lo procesa**. Acepta conocer tarde y luego reescribe el pasado, en lugar de decidir en el tick.
- **POR QUÉ FALLA:** al depender del cierre, el motor necesita ticks futuros para una decisión que el árbol toma en el presente; y al rellenar la hora del tick encontrado, oculta el retraso.
- **PRINCIPIO UNIVERSAL AFECTADO:** el conocimiento debe actualizarse en el **primer tick válido**; ninguna decisión puede requerir información posterior a ese tick.
- **OTROS CASOS AFECTADOS:** 2 confirmado (vela), 3, B Grande, AUT, CUT, FT, y cualquier evento que hoy se emite con `knowledge_time` de cierre.
- **PREGUNTA EXPERTA:** Q4 (tick de TT/FT) y Q3 (tick del nuevo 1).
- **PRUEBA CONCEPTUAL NECESARIA:** positivo: TT confirmado en el tick exacto y visible en el `state_log` de ese tick; negativo: precio que toca el objetivo y vuelve en el mismo tick (sigue confirmado); frontera: TT y AUT en el mismo tick (N-033).
- **CORRECCIÓN TÉCNICA POSIBLE (posterior):** evaluar patrones y transiciones dentro de `feed_chunk`, con el estado por tick como única salida.

---

## 6. CE-6 — El gap como anomalía de datos

**Concepto ausente.** El árbol trata el gap como **evento estructural** con resolución implícita: a favor de 1 → A y B implícitas + TT pendiente (N-003); contrario → A Grande en la dirección del gap (N-004); nunca 2 (N-002/N-005). El motor lo trata como un dato raro: emite un evento informativo y bloquea ramas.

### F-11 — El gap no resuelve función

- **MOVIMIENTO OBSERVADO:** la vela abre con gap; el motor registra `GAP` y no crea A/B implícitas, no pasa a `TT_PENDIENTE`, no abre nuevo 1.
- **ESTADO ESTRUCTURAL RECIBIDO:** `1_ACTIVA` o lectura activa.
- **LECTURA DEL ÁRBOL:** v2.19 §A-C (rango 1, sustituye a N-003/N-004): en el tramo del gap se registran **A Grande implícita → B Grande implícita → A usada como tendencia implícita**, sin inventar precios, y la **apertura negociada de la segunda vela es el origen operativo del nuevo 1**; N-002: con gap no se evalúa 2.
- **LECTURA DEL PYTHON:** `_schedule_gap` emite `GAP` (R5:1545-1558); `_process_local_sequence` retorna sin decidir si `abs(bar.gap) ≥ 0,25` (R5:3009-3013); `local_two_gate` recibe `gap` pero solo para la vela 2 (R5:555).
- **PRIMERA DIVERGENCIA CAUSAL:** el primer tick de la vela con gap.
- **SÍNTOMA:** lecturas que ignoran el hueco y siguen midiendo como si hubiera continuidad; ni A/B/A-usada-como-tendencia implícitas ni nuevo 1 desde la apertura.
- **ERROR LOCAL:** el gap solo se usa como bloqueo o como dato del gate de 2.
- **ERROR CONCEPTUAL:** no comprende que un gap **es** un movimiento implícito: no hay ticks, pero sí resolución funcional.
- **POR QUÉ FALLA:** el motor modela precios, no estructura; sin ticks no hay movimiento y por tanto no hay función, cuando el árbol define la función aunque falten precios.
- **PRINCIPIO UNIVERSAL AFECTADO:** el gap se registra como **tramo no negociado con función implícita**; no se inventan precios y la lectura continúa desde la apertura.
- **OTROS CASOS AFECTADOS:** N-002..N-005, TT tras gap, nuevo 1 desde la apertura, cobertura funcional.
- **PREGUNTA EXPERTA:** ninguna: v2.19 §A-F (rango 1) cierra la resolución del gap. Queda fuera de Q1–Q5.
- **PRUEBA CONCEPTUAL NECESARIA:** positivo: gap tras `1` → A/B/A-usada-como-tendencia implícitas y nuevo 1 desde la apertura de la segunda vela; negativo: apertura dentro de ±0,25 (no hay gap, no hay implícitas); frontera: gap de 0,25 exactos (no es gap, DEC-009).
- **CORRECCIÓN TÉCNICA POSIBLE (posterior):** resolver el gap en la capa funcional, con precios prohibidos.

---

## 7. CE-7 — Transformación funcional no nombrada

**Concepto parcialmente comprendido.** v2.16/v2.17/v2.19 cierran que "A Grande usada como tendencia" y "C Grande usada como tendencia" **no son funciones nuevas**: son la función existente transformándose en nuevo 1 cuando supera la referencia, y deben expresarse como `transition_reason`. El motor sí transforma (crea un nuevo 1), pero no lo nombra así y lo hace como sustitución ontológica.

### F-12 — La transformación se implementa como función nueva

- **MOVIMIENTO OBSERVADO:** A que supera la base del módulo, o C que cruza `fin_A`: el motor crea un `1` dominante nuevo y cierra la lectura anterior.
- **ESTADO ESTRUCTURAL RECIBIDO:** `A`/`C`.
- **LECTURA DEL ÁRBOL:** v2.19: `A_USED_AS_TREND` y `C_USED_AS_TREND` como `transition_reason`; v2.17: nuevo 1 al superar la base del módulo; N-025 sigue `PENDIENTE_JAVIER` para C sin CUT.
- **LECTURA DEL PYTHON:** `_new_local_reading_after_aut` cierra y crea (`INTEGRADA_POR_AUT_NUEVO_1`, R5:2849-2857); `_reclassify_c_as_new_1` emite `C_RECLASSIFIED_AS_NEW_1` (R5:2955) y `A_LOCAL_SUPERA_BASE_MODULO` (R5:3183), no los nombres canónicos.
- **PRIMERA DIVERGENCIA CAUSAL:** el tick del cruce.
- **SÍNTOMA:** dos genealogías donde el árbol ve una transformación; motivos no auditables contra v2.19; nueva lectura que ya mide 2 mientras el árbol espera el TT.
- **ERROR LOCAL:** creación de lectura dominante en el evento de cruce, con razones de texto libre.
- **ERROR CONCEPTUAL:** confunde **transformación de una función** con **nacimiento de otra**; y no distingue el motivo canónico del motivo interno.
- **POR QUÉ FALLA:** el modelo de lectura no tiene "misma lectura, nueva función/razón de transición"; solo tiene crear o cerrar.
- **PRINCIPIO UNIVERSAL AFECTADO:** una función puede **transformarse** conservando su identidad y su genealogía; el nuevo 1 es el resultado de la transformación, no una lectura independiente.
- **OTROS CASOS AFECTADOS:** T09, T11, T12; cierre de lectura; concurrencia; y la trazabilidad exigida por v2.19.
- **PREGUNTA EXPERTA:** Q1 (qué transformación es cada cruce) y Q3 (cuándo nace el 1).
- **PRUEBA CONCEPTUAL NECESARIA:** positivo: A que cruza la base del módulo → `transition_reason=A_USED_AS_TREND`, misma genealogía; negativo: A que no cruza → sigue A; frontera: C que cruza `fin_A` y base del módulo en el mismo tick.
- **CORRECCIÓN TÉCNICA POSIBLE (posterior):** añadir `transition_reason` canónico y conservar identidad de lectura hasta que el árbol autorice el cierre.

---

## 8. Informe solicitado

### 8.1 Conceptos correctamente comprendidos por R5

| Concepto | Evidencia |
|---|---|
| Unidad entera de 0,25 y precios en centésimas | `PRICE_SCALE`, `PLANO_TICK`; sin floats en comparaciones |
| Plano vs gap con 0,25 exactos como **no** plano | `local_two_gate(gap<0.25)`; coherente con DEC-009, supera N-002 |
| AUT estricto `> 127 % + 0,25`; el toque exacto no dispara | `BigBTracker.limit` y `b_size > limit`; N-016 |
| B Grande exactamente al 100 % de A, por tick | `b_size >= a_size` en el mismo tick de confirmación |
| TT por `≥ objetivo` (igualdad admitida) | `_check_tt` usa `>=`/`<=`; N-039 |
| C solo después de B Grande confirmada | `begin_c` exige `confirmed`; N-022 |
| A se extiende entre velas sin cerrarse en el primer extremo | actualización de `a_end`; N-013/N-038 |
| No usa color de vela ni OHLC para clasificar | todo el motor trabaja sobre ticks |
| Conserva historial al cerrar/archivar | `_done` + `ARCHIVADA`; N-031 |
| Separa tiempos estructural/confirmación/conocimiento en los eventos | campos `*_time`, `knowledge_audit` |
| Máximo 3 lecturas como mecanismo | `MAX_ACTIVE` |

### 8.2 Conceptos implementados parcialmente

| Concepto | Qué falta |
|---|---|
| Medida de 2 (plano, cola, dirección, 100 %) | falta el guardián `rango_2 ≥ rango_1` (el detector que lo tenía es código muerto) y la medida direccional frente a high-low |
| 3 | falta el retroceso 0-50 %; sobra el umbral 2,00 |
| Módulo | falta `max−min` de las velas del conjunto |
| B Grande | falta la cota superior en el mismo tick (puede emitir B_GRANDE y AUT juntos) |
| TT | objetivo mal referenciado y descubrimiento tardío |
| FT | la parte v1.2 (extremo real del TT) está; la condición de fin es inventada |
| C | nace, se extiende y puede reasignarse; faltan N-023 y la tercera función de N-034 |
| Cierre/invalidación | cierra por FT/CUT; faltan las demás invalidaciones de N-035 |
| Reclasificación | existe la transferencia de dominio; criterios provisionales sin documentar |
| Gap | detectado y bloqueante; sin resolución funcional |

### 8.3 Conceptos interpretados incorrectamente

| Concepto | Interpretación del motor | Interpretación del árbol |
|---|---|---|
| `1` | high-low de una vela cerrada, mínimo 6,00 | desplazamiento direccional, sin mínimo |
| autonomía | todo giro ≥ 2,00/6,00 es función nueva | solo si rompe la referencia y completa una función |
| TT | se descubre al cerrar un movimiento | se confirma en el tick que alcanza el 100 % |
| TT fallido | cruzar `fin_A ± 2,00` y emitir CUT | tocar `fin_A`, sin CUT, → módulo + A Grande |
| CUT | `fin_A ± 2,00` (PRIMARY) o `fin_A` (LOCAL) | `fin_A` (N-024) **o** base del módulo (v1.2/v2.17): decisión de Javier |
| FT | primer movimiento contrario ≥ 6,00 | pérdida de estructura del TT (referencia pendiente) |
| prioridad mismo tick | orden de iteración | regla expresa (pendiente) |
| nueva lectura | se crea al confirmar AUT/CUT | se abre solo con regla expresa |

### 8.4 Conceptos ausentes

- Resolución funcional del gap (A/B implícitas, TT pendiente, A Grande por gap).
- Nuevo 1 en el TT (N-021) y mismo tick AUT+TT (N-033).
- Cancelación de C por nuevo extremo de B en la lectura local (N-023).
- Tercera función de C: A Grande de lectura mayor (N-034).
- `A_USED_AS_TREND` y `C_USED_AS_TREND` como `transition_reason` (v2.19).
- `TERCERO` y la bifurcación rápida/lenta de v1.2 §13.4 (ni siquiera existe en `FUNCTION_LABELS`).
- Vulnerabilidad/invalidación distinta del TT fallido (N-035).
- Reglas expresas de apertura L2/L3 (N-028/N-029) y de prioridad (N-030).

### 8.5 Conceptos duplicados entre motores

| Concepto | PRIMARY | LOCAL |
|---|---|---|
| CUT | `a_end ± 2,00` (R5:948, 1291, 1475) | `a_end` estricto (R5:503, 3265) |
| B Grande | `_legacy_tick_decision` (R5:3373) | `BigBTracker` + `_apply_local_b_transitions` (R5:2886) |
| AUT | `_maybe_aut` + `_legacy_tick_decision` | `_new_local_reading_after_aut` |
| C | primer tick contrario (R5:3403-3416) | excursión ≥ 6,00 (`begin_c`) |
| B candidata | cualquier tick (R5:3335) | retroceso ≥ 6,00 (R5:3187) |
| Módulo | movement origin→extreme | bar extreme→extreme o tramo |
| Dominancia | `dominant` en `_create_reading` | `_make_local_reading` limpia y reasigna |
| Autoridad de pregunta | `_legacy_tick_decision` | `_process_local_sequence` |

### 8.6 Conceptos abiertos que requieren a Javier

Solo cinco, agrupados por concepto (detalle en `DUDAS_ESTRUCTURALES_PENDIENTES_v219.md`): Q1 (CE-2/CE-7: qué cierra el ciclo y qué es cada cruce), Q2 (CE-1: tamaño absoluto o relativo), Q3 (CE-5/CE-7: cuándo nace el nuevo 1), Q4 (CE-4/CE-5: tick y referencia de TT/FT), Q5 (CE-1/CE-3: vida de 2 y regularidad de 3).

**Actualización tras el cierre del mapa (ver `MAPA_CIERRE_v219.md` §5):** Q1 queda respondida por v1.2 §13 (CUT = base del módulo; TERCERO solo por velocidad); Q5 queda respondida por N-007 (2 permanece candidata mientras cumpla N-006) y N-009/N-010 (3 exige retroceso 0–50 %); Q2 queda respondida en lo esencial por v2.5 §D (la lectura no tiene mínimo) y N-014 (B se mide sobre `rango_A`); Q3 queda acotada por v2.3 §F, N-017 y v1.2 §13.7.9 (dos caminos de AUT); Q4 queda resuelta para el TT (confirmación en el tick del 100 %) y abierta solo para el tick y las variables del FT. Las reglas realmente abiertas son R-01…R-07 del cierre del mapa.

### 8.7 Casos que parecían dudas y quedaron resueltos al recorrer el árbol

| Caso | Resolución |
|---|---|
| 0,25 exactos: plano o no | DEC-009/H14 prevalece sobre N-002: **no es plano**. El motor acierta |
| AUT al tocar 127 % + 0,25 | N-016 + DEC-003: no hay AUT; el motor acierta |
| TT con igualdad exacta | N-039: vale `≥`; el motor acierta |
| ¿C antes de B? | N-022: prohibido y el motor lo respeta |
| ¿B y AUT coexisten? | N-037: no; el motor los emite en el mismo tick (fallo de secuencia, no de teoría) |
| ¿1 exige tamaño mínimo? | N-001 + N-040: no; el motor se equivoca |
| ¿Módulo 1+2 es válido? | N-011: sí, para el caso regular; el motor lo deja por inacción (parcial) |
| ¿2 confirmado se borra? | N-036: no; el motor lo conserva |
| ¿TT sin 100 %? | N-039/N-019: no; el motor respeta el umbral, falla el tick |
| ¿CUT sin C? | N-024: prohibido; el motor lo respeta |

### 8.8 Preguntas expertas agrupadas

**Q1 (CE-2/CE-7).** Estábamos en `C Grande` de un ciclo con `B Grande` confirmada. El precio recorrió C y alcanzó el final de A; después siguió o giró. ¿Ese cruce es `CUT` y cierra el ciclo, o es `C Grande usada como tendencia` y transforma la misma lectura en nuevo 1? Si queda como CUT: ¿qué pasa cuando C supera la base del módulo pero no el final de A? Si se transforma: ¿qué condición exacta convierte C en nuevo 1, y qué ocurre cuando C no alcanza ninguna de las dos referencias?

**Q2 (CE-1).** Estábamos en `1` (o en `A Grande`) y el precio hizo un recorrido corto pero direccional; después continuó en la dirección esperada. ¿La función se define por un tamaño mínimo absoluto —y en ese caso cuál— o por su desplazamiento relativo al módulo/1? Si hay mínimo absoluto: ¿qué pasa con un `1` de 5,00 puntos? Si es relativo: ¿qué porcentaje define A Grande, B candidata y C?

**Q3 (CE-5/CE-7).** Estábamos en `B Grande` y el precio superó el 127 % + 0,25 (AUT). Después continuó hasta el objetivo TT. ¿El nuevo 1 nace en el tick del AUT —y entonces qué función mide el TT— o nace al alcanzar el TT —y entonces qué lectura posee el módulo mientras el TT está pendiente?

**Q4 (CE-4/CE-5).** Estábamos en `TT pendiente` con objetivo calculado. El precio alcanzó el objetivo y retrocedió; después siguió retrocediendo. ¿El TT se confirma en el tick que toca el objetivo y el FT nace en el extremo real del TT (v1.2), o el TT solo se considera terminado cuando se pierde su estructura? ¿El fallo del TT ocurre al tocar el final de A, sin margen, y convierte todo el recorrido en módulo + A Grande?

**Q5 (CE-1/CE-3).** Estábamos en `2 confirmada` (o en `2 candidata` al cerrar su vela). El precio no alcanzó el 100 % de 1 y apareció un movimiento contrario; después siguió. ¿Ese 2 sigue pendiente mientras conserve sus condiciones, o se cierra con su vela y el contrario abre A Grande? Y el `3`: ¿se confirma por superar el extremo de 2 en cualquier magnitud, o solo si antes retrocedió entre 0 % y 50 % del rango de 2?

### 8.9 Impacto de cada respuesta

| Respuesta | Nodos | Estados | Pruebas |
|---|---|---|---|
| Q1 | N-024, N-025, N-022, N-034, v1.2 §13, v2.17 | `C`, `CUT`, `NUEVO_1`, `A_GRANDE` (lectura mayor) | T-024, T-025, T-026, TEST-C-001..004 |
| Q2 | N-001, N-006, N-007, N-014, N-015, N-040 | `1`, `2`, `A`, `B_CAND`, `B_GRANDE`, `C` | T-001, T-005, T-013..T-016 |
| Q3 | N-017, N-018, N-021, N-031, N-033 | `AUT`, `TT_PENDIENTE`, `NUEVO_1` | T-016..T-021, T-033 |
| Q4 | N-018, N-019, N-020, N-026, N-035, N-039 | `TT_PENDIENTE`, `TT_EXT`, `FT`, `MODULO`, `A_GRANDE` | T-017..T-021, T-027, T-028 |
| Q5 | N-006..N-011, N-036 | `2_CANDIDATA`, `2_CONFIRMADA`, `3`, `MODULO`, `A_GRANDE` | T-004, T-005, T-007..T-010, T-037, T-038 |

### 8.10 Recomendación técnica posterior (no ejecutable todavía)

1. **Una sola autoridad funcional por tick.** Elegir una máquina (LOCAL, por ser la única con 1-2-3 y con confirmación por tick) y dejar la otra como legacy congelada. No fusionar reglas: trasladar solo las que el árbol cierra.
2. **Separar capas en el modelo de lectura:** `function` (1,2,3,A,B,C,AUT,CUT), `pattern` (TT, FT), `lifecycle` (activa, pendiente, confirmada, cerrada), `transition_reason` (incluidos `A_USED_AS_TREND`/`C_USED_AS_TREND`).
3. **Derivar la medida de la estructura, no del constructor de movimientos:** `1` direccional desde su origen; módulo como rango de expansión del conjunto; proporciones 100/127 calculadas sobre esa base.
4. **Evaluar patrones y transiciones en el tick**, con el `state_log` por tick como única fuente de verdad; eliminar el descubrimiento por cierre de movimiento.
5. **Tabla de imposibilidad por función** derivada de N-006..N-011, N-020, N-035, sin umbrales nuevos.
6. **Gap en la capa funcional**, con precios prohibidos y resolución implícita.
7. **Pruebas de concepto antes de tocar código:** por cada corrección, caso positivo, negativo y frontera, más una prueba de "misma traza no produce dos ciclos". Ninguna prueba puede depender de hora, precio o fixture; la traza sintética de este documento es evidencia de auditoría, no un golden.
8. **No implementar Q1..Q5** hasta que Javier responda; hasta entonces, marcar esos nodos como `BLOCKED_BY_OPEN_RULE` en el mapa y conservar el motor actual.

**Condición de validez de cualquier corrección futura:** debe explicar qué función cumple el movimiento, no solo qué etiqueta produce; debe resolver clases de movimientos equivalentes; y no puede ganar el caso perdiendo otro funcionalmente igual.

---

## 9. Restricción final

No se ha programado ninguna corrección semántica. El motor sigue en `9BD1BEDB…` y el árbol en `WORKING_CANON_NOT_FROZEN`. Este documento demuestra únicamente: qué movimientos fallan, qué finalidad tenían, qué concepto no comprende el motor y qué principio universal los gobierna. La corrección técnica queda supeditada a las cinco respuestas de Javier.


---

## 10. Adenda de precedencia (posterior al cierre del mapa)

Al indexar el árbol completo se aplicó §0 y aparecieron seis precisiones que **no cambian los conceptos**, pero sí su anclaje normativo:

1. **F-01** se refuerza: v2.5 §D (rango 5) prohíbe expresamente usar el tamaño como condición de lectura. El 6,00 de R5 no es un umbral canónico de estructura, sino un filtro operativo trasladado a la capa de lectura.
2. **F-10** se matiza: el nuevo 1 en el AUT es correcto cuando el AUT nace por cruce de la base del módulo (v2.3 §F); es incorrecto cuando nace por 127 %, porque N-017 solo autoriza un candidato y v1.2 §13.7.9 sitúa el nuevo 1 y el reset al confirmar el TT al 100 %. El defecto es no distinguir ambos caminos y crear un dominante.
3. **F-11** se reancla: la expectativa del gap no es la de N-003/N-004 (Anexo 1, rango 7), sino la de v2.19 §A-F (rango 1): A/B/A-usada-como-tendencia implícitas y nuevo 1 desde la apertura de la segunda vela. El motor no implementa ninguna de las dos.
4. **CE-7** se precisa: `A_USED_AS_TREND` es función implícita dentro de la resolución del gap (v2.19) y, a la vez, motivo de transición cuando una A existente se usa como tendencia (v2.17/v2.19). No es una etiqueta adicional del ciclo modular.
5. **CUT** se ancla a la base del módulo (v1.2 §13.2/13.7, rango 3), no a `fin_A ± 2,00`. El motor usa la referencia equivocada en las dos máquinas.
6. **FT** no puede llevar umbral inventado: v2.6 §F lo prohíbe y deja tick y variables pendientes (R-02).

Quedan **siete reglas realmente abiertas** (R-01…R-07) documentadas en `MAPA_CIERRE_v219.md` §6. Ninguna se implementa en esta fase.
