# FREEBUFF_RC1_MOVEMENT_ANALYSIS_v219

**RC-1 — Qué movimiento representa R5 y qué movimiento debería representar**
**Motor:** R5 `9BD1BEDB…` (`0.7.5.2-R5`) · **Árbol:** `94A1408A…` · **Fecha:** 2026-10-30
**Versión documental:** 1.0
**tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

---

## 1. Respuesta corta

R5 no representa un movimiento: representa **movimientos ya cerrados**. Un movimiento solo existe cuando `MovementBuilder` detecta un retroceso de `max(6,00; 25 %)` desde el extremo. Hasta ese tick, el motor no tiene dirección, no tiene origen funcional y no tiene ninguna pregunta que hacer. Cuando por fin cierra, crea una lectura `MODULE` etiquetada `1` con el recorrido **completo** del movimiento, que ya contiene lo que el árbol llamaría `1`, `2` y `3`.

El árbol, en cambio, representa **funciones en curso**: `1` nace con el primer desplazamiento, conserva su origen y actualiza su extremo; `2` se pregunta en cuanto `1` existe; `3` se pregunta tras `2`; `A` nace del primer contrario estructural. La función no espera a que el movimiento se cierre: lo habita.

## 2. Las 20 preguntas de la investigación RC-1

### 2.1 ¿Qué estado representa `1:FIRST`?

No es un estado. Es el evento `LECTURA_CREADA` emitido por `_create_reading` (857-897) con:

```text
function      = "1"
new_state     = "MODULE"
origin_reason = "FIRST"
```

El estado interno de la lectura es `MODULE`. El texto `1:FIRST` que aparece en los informes es la concatenación de `function=1` y `origin_reason=FIRST`.

### 2.2 ¿Es función TM, marcador técnico o evento provisional?

**Marcador técnico de un movimiento ya consolidado.** No es la función `1` del árbol porque:

- se crea en el tick de **confirmación** del movimiento (`cp = points[movement.confirm_index]`), no en su origen;
- su `module_origin`/`module_extreme` son los del movimiento completo;
- no tiene estado de candidatura ni condición de confirmación propia.

### 2.3 ¿Qué campos se inicializan?

`reading_id`, `direction` (= dirección del movimiento), `state="MODULE"`, `created_time/seq/bar`, `origin_reason`, `module_origin`, `module_extreme`, tiempos y secuencias de ambos, `parent_reading_id`, `owner_reading_id`, `dominant` (si es la primera activa), `labels=[(leg_index,"1")]`, `leg_indices`.

No se inicializan: `confirmation_condition`, `confirmation_time`, `knowledge_time`, `candidate_status`, `origin_owner`, `extreme_owner`, `tt_target` (hasta B Grande).

### 2.4 ¿Qué extremo se actualiza?

`module_extreme`. En estado `MODULE`, cada movimiento de la misma dirección lo reemplaza por `movement.extreme` (1074-1093). No hay un extremo de `1` separado: el extremo del módulo **es** el extremo de la pata.

### 2.5 ¿Qué condición espera el motor?

Dos condiciones consecutivas:

1. `MovementBuilder.feed` (351-362): que el precio se aleje `>= 600` de `origin`.
2. `feed` (363-382): que el precio retroceda `>= max(600, 25 % del recorrido)` desde `ext`.

Solo entonces devuelve un `Movement` y `_process_movement` puede crear la lectura.

### 2.6 ¿Por qué exige una reacción adversa de 6 puntos?

Porque reutiliza `MOVE = 600` como `min_move` del constructor (334) y como mínimo del umbral de cierre (363). El 6,00 no proviene del árbol: es el filtro de elegibilidad operativa de v2.5 §D.

### 2.7 ¿Qué semántica atribuye a ese umbral?

La de **movimiento estructural**. El código lo aplica como si por debajo de 6,00 no hubiera estructura. Eso contradice v2.5 §H, que prohíbe usar el filtro de 6 puntos para alterar funciones y patrones.

### 2.8 ¿En qué momento crea `MODULE`?

En `_open_candidate` (1383-1415), cuando no hay ninguna lectura primaria viva. Devuelve `"FIRST"` con `movement.origin/extreme`; `_process_movement` (1494-1539) llama a `_create_reading` con `cp` (tick de confirmación del movimiento).

### 2.9 ¿Qué recorrido incluye en la medida?

`movement.origin → movement.extreme`, es decir, **todo** el tramo recorrido desde el origen del constructor hasta el extremo más lejano, incluyendo cualquier oscilación intermedia que no haya alcanzado el retroceso de 6,00.

### 2.10 ¿Por qué CE-2 termina midiendo 0→16?

Porque la pata 0→16 nunca retrocede 6,00 antes del tick 19:

| Tick | Precio | Retroceso desde 16 | ¿Cierra movimiento? |
|---:|---:|---:|---|
| 4 | 10,00 | — | no (aún sube) |
| 7 | 6,00 | 4,00 desde 10 | no (< 6,00) |
| 14 | 7,00 | 4,00 desde 11 | no (< 6,00) |
| 17 | 16,00 | — | no (nuevo extremo) |
| 19 | 10,00 | 6,00 desde 16 | **sí** |

En el tick 19 se cierra un único movimiento 0→16. El motor crea la lectura con módulo 16,00. Canónicamente, el `1` es 0→10 y el resto son funciones distintas.

### 2.11 ¿Qué parte pertenecía canónicamente al primer movimiento?

`0,00 → 10,00`, medida 10,00 (CE-2). Ese es el `1`.

### 2.12 ¿Qué parte pertenecía a la función siguiente?

- `10,00 → 6,00`: `A Grande` bajista de 4,00 (el `2` es imposible porque la vela abre en plano pero va en dirección contraria).
- `6,00 → 11,00`: `B` de 5,00 (125 % de A) → `B Grande` en 10,00, sin AUT (límite 5,33).
- `11,00 → 7,00`: `C Grande` de 4,00.
- `7,00 → 16,00`: TT al 100 % (fin de A 6,00 + módulo 10,00 = 16,00).
- `16,00 → 3,90`: C continúa; base 0,00 no alcanzada → sin CUT.

Ninguna de esas funciones existe en R5.

### 2.13 ¿Dónde se pierde la frontera entre funciones?

En `MovementBuilder`. No hay ninguna referencia funcional en el constructor: solo un umbral de retroceso. Dos funciones separadas por un giro de 4,00 pertenecen al mismo movimiento; un giro de 6,00 las separa. La frontera es **de tamaño**, no **de función**.

### 2.14 ¿Por qué no se abre la pregunta por `2`?

Porque la pregunta primaria de `MODULE` es `A`:

```text
_advance_primary_question (3282-3313)
  if r.state == "MODULE":
      expected_function = "A"
      active_question   = "DONDE_NACE_A"
```

`2` solo existe en `_process_local_sequence` (3005-3281), y esa máquina exige `armed=True`, que solo se activa con un evento `AUT` primario (`_observe_core_aut`, 2784-2790). Sin AUT no hay LOCAL; sin LOCAL no hay `2`.

### 2.15 ¿Por qué el estado termina en `DONDE_NACE_A`?

Porque `A` solo nace cuando se cierra un movimiento contrario (1072-1112). Si el tramo contrario no retrocede 6,00 antes del final del feed, `A` no se emite y la lectura queda en `MODULE` con la pregunta `DONDE_NACE_A` indefinidamente. Es lo que ocurre en CE-7-AUT: el descenso 20→−3 no se cierra y el motor nunca ve la A que cruza la base.

### 2.16 ¿Qué eventos posteriores nunca pueden alcanzarse?

Sin `1`: `2`, `3`, `A`, `B`, `B Grande`, `AUT`, `C`, `CUT`, `TT`, `FT`. Sin `AUT`: toda la máquina `LOCAL` (que es la única que contiene `2/3`). Sin movimiento contrario cerrado: `A`. Sin `A`: `B`. Sin `B Grande`: `C`. Sin `C`: `CUT`.

### 2.17 ¿Qué parte del problema es de arquitectura?

La unidad de decisión. Mientras `feed_chunk` decida en `_process_movement`, toda función llegará tarde. La arquitectura necesita un estado funcional por tick, no por movimiento cerrado.

### 2.18 ¿Qué parte es una condición local?

`min_move=600` (334) y `span<MOVE` (2797). Son dos líneas concretas; cambiarlas no basta, pero sin cambiarlas nada arranca.

### 2.19 ¿Qué parte es falta de estado?

Faltan, como mínimo:

```text
ONE_CANDIDATE      (origen inmutable, extremo móvil, medida provisional)
ONE_CONFIRMED      (medida congelada, knowledge_time)
TWO_CANDIDATE      (pregunta activa tras 1, con su condición e imposibilidad)
THREE_CANDIDATE    (retroceso 0-50 % + superación del extremo de 2)
A_CANDIDATE        (primer contrario estructural, antes de ser A Grande)
B_CANDIDATE        (con oscilaciones internas absorbidas)
```

Hoy solo existen `MODULE`, `A`, `B_CAND`, `TT_PENDING`, `TT_EXT`, `C`, `DONE`. No hay ningún estado de candidatura para `1`, `2` ni `3`.

### 2.20 ¿Qué parte es falta de precedencia?

No hay árbitro entre:

- `TT pendiente` y `final de A` (v2.7 §B);
- `B Grande` y `AUT` en el mismo tick (N-037);
- lectura primaria y lectura local (N-028/N-029/N-030);
- función y patrón (v1.2 §13.6).

`_advance_primary_question` y `_process_local_sequence` se ejecutan ambos cada tick sin orden de precedencia funcional.

## 3. Movimiento completo — CE-2

### 3.1 Estado canónico en el tick 2 (precio 4,00)

| Campo | Valor canónico | Valor R5 |
|---|---|---|
| Estado recibido | `SIN_LECTURA` | `SIN_LECTURA` |
| Función dominante | `1` (candidata) | ninguna |
| Lectura secundaria | no | no |
| Origen activo | 0,00 | — |
| Extremo activo | 4,00 | — |
| Función esperada | `1` en curso | ninguna |
| Pregunta que debía formularse | ¿se confirma `1`? | ninguna |
| Movimiento físico | 0,00→4,00 | 0,00→4,00 |
| Función que cumple | `1` | ninguna |
| Candidatura | sí | no |
| Confirmación | al congelarse la medida | no |
| Imposibilidad | volver al origen | no evaluada |
| Transición posterior | pregunta por `2` | ninguna |
| `structural_time` | tick 1 | — |
| `knowledge_time` | tick 2 | — |
| Estado transmitido | `ONE_CANDIDATE` | vacío |

### 3.2 Estado R5 en el tick 19 (precio 10,00)

| Campo | Valor R5 | Valor canónico |
|---|---|---|
| Estado | `MODULE` | `C` / `TT` |
| Función | `1` | `C Grande` + `TT posible` |
| Origen del módulo | 0,00 | 0,00 (módulo de `1`) |
| Extremo del módulo | 16,00 | 10,00 |
| Medida | 16,00 | 10,00 |
| Pregunta | `DONDE_NACE_A` | `TT 100 %` / `CUT` |
| `structural_time` | tick 1 | tick 1 |
| `knowledge_time` | tick 19 | tick 4 para `1`, tick 10 para B Grande |

La lectura nace **15 ticks tarde** y con una medida **60 % mayor** que la canónica.

### 3.3 CE-2 en una línea

```text
canónico: 1(0→10) → 2 imposible → A(10→6) → B(6→11) → C(11→7) → TT(16)
R5:       .............................................. 1(0→16) → DONDE_NACE_A
```

## 4. Movimiento completo — CE-7-AUT

| Tick | Precio | Canónico | R5 |
|---:|---:|---|---|
| 1 | 0,00 | origen de `1` | sin lectura |
| 5 | 20,00 | `1` = 0→20 (medida 20) | sin lectura (aún no hay retroceso 6) |
| 6 | 20,00 | A candidata desde 20,00 | sin lectura |
| 8 | 10,00 | A = 20→10 (10) | **nace** `MODULE` 0→20, pregunta `DONDE_NACE_A` |
| 9 | 5,00 | A se extiende a 5,00 | sin A |
| 10 | −1,00 | A cruza base 0,00 → AUT + nuevo `1` bajista | sin A, sin AUT |
| 11 | −3,00 | nuevo `1` bajista en curso | sigue `MODULE`, `DONDE_NACE_A` |

R5 crea la lectura cuando el precio retrocede de 20 a 10 (10 puntos ≥ 6). En ese momento el movimiento 0→20 ya terminó; la A que empieza en 20 no se reconocerá hasta que el descenso 20→−3 retroceda 6,00, cosa que no ocurre en el feed. Por eso no hay AUT.

## 5. Movimiento completo — CE-7-C

| Aspecto | Canónico | R5 |
|---|---|---|
| `1` | 25,00→0,00 (25,00) | 25,00→−0,25 (25,25) |
| A | 0,00→4,00 (4,00) | no existe |
| B | 4,00→0,00 (100 %) → B Grande; −0,25 dentro de 127 %+0,25 | no existe |
| C | −0,25→7,00 o 26,00 | no existe |
| CUT | contra `a_end` 4,00 o base 0,00 (ambigüedad de la prueba) | no existe |
| Tick de lectura | 1 | 15 (NEG) / 14 (FRON) |

## 6. Por qué el módulo no siempre está mal

| Caso | Pata | Retrocesos internos | Módulo R5 | Módulo canónico | ¿Error? |
|---|---|---|---:|---:|---|
| CE-2 | 0→16 | 10→6 (4), 11→7 (4) | 16,00 | 10,00 | sí |
| CE-4-NEG | 0→20 | 20→16 (4), 16→14 (2) | 20,00 | 20,00 | no |
| CE-7-C | 25→−0,25 | 0→4 (4), 4→−0,25 (4,25) | 25,25 | 25,00 | sí (0,25) |

**Regla observada:** el módulo es correcto cuando la pata es monótona o cuando sus retrocesos internos alcanzan el umbral de cierre; se infla cuando la pata absorbe oscilaciones menores de 6,00. El error no es "la fórmula del módulo", sino **qué ticks pertenecen al movimiento**.

## 7. Consecuencias para la implementación (sin código)

1. La decisión funcional no puede depender de `Movement` cerrado.
2. `1` necesita candidatura y congelación explícitas; sin ellas, ni el módulo ni `2` tienen referencia.
3. `MOVE=600` debe salir de la capa de lectura. Solo quedan `25` (tick/plano) y `200` (ruido).
4. La escalera `2/3` no puede vivir en una máquina que solo se arma con un AUT.
5. El módulo debe derivarse de la función `1` (y de `2/3` cuando existan), no del recorrido de la pata.
6. TT debe comprobarse en cada tick contra su objetivo, no al cerrar un movimiento.

Ninguna de estas conclusiones se implementa en esta fase.
