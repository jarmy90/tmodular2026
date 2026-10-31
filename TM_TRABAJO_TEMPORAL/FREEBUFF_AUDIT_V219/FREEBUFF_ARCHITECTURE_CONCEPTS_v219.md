# FREEBUFF_ARCHITECTURE_CONCEPTS_v219

**Arquitectura conceptual mínima para ejecutar el árbol v2.19**
**Fecha:** 2026-10-30
**Árbol:** `94A1408A…` (WORKING_CANON_NOT_FROZEN) · **Motor de referencia:** R5 `9BD1BEDB…` (`0.7.5.2-R5`)
**Versión documental:** 1.0
**Sin código. Sin implementación. Sin declarar el árbol congelado.**
**tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

---

## 0. Principio rector

> **Una lectura, un tick, una pregunta.**

En cada tick, para cada lectura activa, debe existir exactamente:

```text
1 función vigente
1 pregunta activa
1 condición de confirmación
1 condición de imposibilidad
1 dueño del origen
1 dueño del extremo
```

Todo lo demás (patrón, evento, genealogía) es una capa distinta que **no sustituye** a la función.

La decisión no puede depender del cierre de un movimiento ni de una vela. El movimiento es el **contenido**; la vela es solo el **contenedor temporal**.

## 1. Diagrama de la escalera regular

```text
NO_READING
  │ primer desplazamiento con referencia
  ▼
ONE_CANDIDATE ──(nuevo extremo)──► ONE_CANDIDATE
  │ condición de confirmación de 1 (Q1)
  ▼
ONE_CONFIRMED (medida congelada)
  │ apertura de la vela siguiente
  ▼
EVALUATE_OPENING ──gap / cola / dirección──► TWO_IMPOSSIBLE
  │ plano + sin gap + sin cola + misma dirección
  ▼
TWO_CANDIDATE ──(100 % de 1)──► TWO_CONFIRMED
  │ retroceso funcional requerido
  ▼
THREE_CANDIDATE ──(supera extremo de 2)──► THREE_CONFIRMED
  │ módulo regular 1-2-3
  ▼
A_CANDIDATE ──(contrario estructural)──► A_GRANDE
  │ giro contrario a A
  ▼
B_CANDIDATE ──(100 % de A)──► B_GRANDE
  │ 100 % ≤ B ≤ 127 % + 0,25 inclusive
  ▼
AUT (superación estricta)
  │
  ├──► TT_POSSIBLE ──(100 % del objetivo)──► TT_CONFIRMED ──► TT_EXTREME ──► FT_POSSIBLE
  │
  └──► C_CANDIDATE ──► C_GRANDE ──► CUT / C_USED_AS_TREND
```

Ramas laterales:

```text
TWO_IMPOSSIBLE  → MÓDULO_POR_DESCARTE (1) → A_CANDIDATE
THREE_IMPOSSIBLE → MÓDULO 1+2 → A_CANDIDATE
GAP             → funciones implícitas → NUEVO_1_EN_APERTURA
AUT por base    → A_USED_AS_TREND → NUEVO_1
CUT             → C_USED_AS_TREND → NUEVO_1
```

## 2. Fichas de concepto

### C-01 — Reading (lectura)

- **Finalidad:** unidad de referencia independiente. Todo pertenece a una lectura.
- **Datos:** `reading_id`, dirección, padre, genealogía, referencias congeladas, función vigente, patrón vigente, evento de cierre, dueño del tick.
- **Entrada:** primer desplazamiento con referencia válida, o resolución de gap, o transformación de A/C.
- **Pendiente:** pregunta activa sin resolver.
- **Confirmación:** no aplica a la lectura; aplica a sus funciones.
- **Imposibilidad:** pérdida de coherencia o cierre por evento canónico.
- **Origen:** el de la función que la abre.
- **Extremo:** el de la función vigente.
- **`structural_time`:** tick del origen funcional.
- **`knowledge_time`:** primer tick con evidencia suficiente.
- **Siguiente pregunta:** la que fije la función vigente.
- **Pruebas:** una lectura no se abre sin regla expresa; máximo 3 activas; cada una conserva sus referencias.

### C-02 — ONE_CANDIDATE / ONE_CONFIRMED

- **Finalidad:** que `1` exista desde el primer desplazamiento y que su medida se congele una sola vez.
- **Datos:** `direction`, `origin` (inmutable), `current_extreme`, `current_measure`, `structural_time`, `owning_bar`, `candidate_status`.
- **Entrada:** primer desplazamiento direccional con referencia; **sin mínimo de tamaño**.
- **Pendiente:** mientras el extremo se amplía y no se cumple la condición de confirmación (Q1).
- **Confirmación:** la que fije Javier (cierre de vela, primer no-extremo o primer contrario estructural). **No se inventa.**
- **Imposibilidad:** retorno completo al origen antes de confirmar (si Javier lo aprueba).
- **Origen:** dueño = `1`.
- **Extremo:** dueño = `1` mientras esté en candidatura; se congela al confirmar.
- **`structural_time`:** tick del origen.
- **`knowledge_time`:** tick de confirmación.
- **Siguiente pregunta:** `¿puede existir 2?`.
- **Pruebas:** `1` de 2,00; `1` de 5,99; `1` que cruza vela; `1` que nunca confirma.

### C-03 — EVALUATE_OPENING / TWO_CANDIDATE / TWO_CONFIRMED / TWO_IMPOSSIBLE

- **Finalidad:** decidir si `2` puede existir y confirmarlo al 100 % de `1`.
- **Datos:** apertura, gap, cola inicial, dirección, `one_size`, `two_open`, `two_extreme`, `measure`.
- **Entrada:** `ONE_CONFIRMED` + primera apertura evaluable.
- **Pendiente:** `2` sigue candidata mientras se cumplan las condiciones de N-006/N-007, aunque cruce velas.
- **Confirmación:** recorrido direccional `>= one_size` (100 % de `1`), en el primer tick que lo alcanza.
- **Imposibilidad:** gap, cola > 0,25, dirección contraria, o ruptura que el árbol fije. La imposibilidad es un estado lógico, no un silencio.
- **Origen:** `open` de la vela de `2`.
- **Extremo:** el más lejano en dirección de `2`; las vibraciones internas no lo fragmentan.
- **`structural_time`:** tick de apertura.
- **`knowledge_time`:** tick de confirmación (o de imposibilidad).
- **Siguiente pregunta:** `¿confirma 3?`.
- **Pruebas:** vibración interna de 3,00 sin romper `2`; `2` que cruza vela; `2` exactamente al 100 %; `2` imposible por gap.

### C-04 — THREE_CANDIDATE / THREE_CONFIRMED / THREE_IMPOSSIBLE

- **Finalidad:** completar el módulo regular o degradarlo a `1+2`.
- **Datos:** `two_extreme`, retroceso medido, `three_extreme`, `module_kind`.
- **Entrada:** `TWO_CONFIRMED`.
- **Pendiente:** mientras el retroceso esté entre 0 % y 50 % del rango de `2` y no se supere el extremo.
- **Confirmación:** retroceso válido + superación estricta del extremo de `2`.
- **Imposibilidad:** retroceso > 50 % o ausencia de superación cuando el árbol lo determine; entonces `1+2` = módulo.
- **Origen:** extremo de `2`.
- **Extremo:** nuevo extremo de `3`.
- **`structural_time`:** extremo de `2`.
- **`knowledge_time`:** tick de superación.
- **Siguiente pregunta:** `¿dónde nace A?`.
- **Pruebas:** retroceso 30 % → `3`; retroceso 70 % → `1+2` + A; retroceso exactamente 50 % (decisión experta).

### C-05 — MÓDULO (derivado, no estado)

- **Finalidad:** dar a TT y CUT la referencia de expansión correcta.
- **Datos:** `module_origin`, `module_extreme`, `module_size`, `module_kind` (`REGULAR` / `POR_DESCARTE`), dueño.
- **Entrada:** `THREE_CONFIRMED` o `TWO_IMPOSSIBLE` o `THREE_IMPOSSIBLE`.
- **Pendiente:** no aplica; el módulo se congela al nacer.
- **Confirmación:** queda definido por la función que lo origina.
- **Imposibilidad:** no aplica.
- **Origen:** dueño = función que lo origina (`1`, o `1+2`, o `1+2+3`).
- **Extremo:** dueño = la misma función; **no se amplía** con funciones posteriores.
- **`structural_time`:** origen de la función que lo define.
- **`knowledge_time`:** tick en que se cierra la función.
- **Siguiente pregunta:** `¿A Grande?`.
- **Pruebas:** módulo monótono; módulo con mechas; módulo con oscilaciones internas; módulo por descarte; módulo que no debe crecer con `2` ni con `3`.

> **Decisión experta pendiente (Q5):** si el módulo se mide por desplazamiento direccional o por expansión `high-low` del conjunto. La ficha admite ambas; el árbol contiene las dos formulaciones.

### C-06 — A_CANDIDATE / A_GRANDE / A_USED_AS_TREND

- **Finalidad:** representar el primer contrario estructural y su posible transformación en tendencia.
- **Datos:** `origin` (extremo del módulo o de `3`), `current_extreme`, `size`, `direction`, `base` del módulo, `transition_reason`.
- **Entrada:** primer tick contrario al módulo, tras `3` confirmado.
- **Pendiente:** mientras el contrario no alcance la referencia de A (filtro de ruido 2,00).
- **Confirmación:** contrario estructural `>= 2,00` (nunca 6,00).
- **Imposibilidad:** el precio vuelve a extender el módulo antes de confirmar A; entonces el contrario se absorbe.
- **Origen:** extremo real del módulo / de `3`.
- **Extremo:** el más lejano del contrario.
- **`structural_time`:** extremo del módulo.
- **`knowledge_time`:** primer tick con contrario `>= 2,00`.
- **Siguiente pregunta:** `¿B candidata?` o `¿AUT por base?`.
- **Pruebas:** A de 2,00; A que cruza la base; A que no la cruza; transformación `A_USED_AS_TREND` con genealogía conservada.

### C-07 — B_CANDIDATE / B_GRANDE

- **Finalidad:** medir el retroceso contrario a A y decidir si alcanza el 100 %.
- **Datos:** `origin = a_extreme`, `current_extreme`, `b_size`, `a_size`, `aut_limit`.
- **Entrada:** primer recorrido contrario a A `>= 2,00` (ruido).
- **Pendiente:** mientras `b_size < a_size`; las oscilaciones internas se absorben.
- **Confirmación:** `b_size >= a_size` en el primer tick.
- **Imposibilidad:** el precio vuelve a superar el extremo de A antes del 100 %; B falla y A se extiende.
- **Origen:** extremo real de A.
- **Extremo:** extremo direccional más lejano de B.
- **`structural_time`:** extremo de A.
- **`knowledge_time`:** tick del 100 %.
- **Siguiente pregunta:** `¿AUT?`.
- **Pruebas:** B de 99,99 %; B de 100 %; B de 127 % + 0,25 exactos; B que supera; vibraciones internas.

### C-08 — AUT

- **Finalidad:** marcar el punto decisivo exacto y abrir TT posible.
- **Datos:** `aut_price`, `aut_time`, `aut_source` (`B` o `A_BASE`), `level_100`, `level_127`, `module`, `fin_A`, `tt_target`, `class_size`.
- **Entrada:** `B_GRANDE` vigente.
- **Pendiente:** mientras `b_size <= 127 % + 0,25`.
- **Confirmación:** `b_size > 127 % + 0,25`, estricto, en ese tick.
- **Imposibilidad:** no aplica; si B se detiene, no hay AUT y B sigue vigente.
- **Origen:** extremo de A.
- **Extremo:** extremo de B en el tick de AUT.
- **`structural_time`:** tick del 127 %.
- **`knowledge_time`:** tick de la superación estricta.
- **Siguiente pregunta:** `¿TT posible?` (y, si corresponde, `¿C?`).
- **Pruebas:** 127 % exactos → no AUT; 127 % + 0,01 → AUT; B Grande y AUT nunca en el mismo tick (N-037).

### C-09 — C_CANDIDATE / C_GRANDE / C_USED_AS_TREND

- **Finalidad:** representar el contrario posterior a B Grande y sus tres salidas (CUT, nuevo `1`, A de lectura mayor).
- **Datos:** `origin = b_extreme`, `current_extreme`, `size`, `base` del módulo, `a_end` congelado.
- **Entrada:** `B_GRANDE` confirmada + primer contrario estructural.
- **Pendiente:** mientras no cruce la referencia de CUT ni se transforme.
- **Confirmación:** contrario `>= 2,00`.
- **Imposibilidad:** nuevo extremo de B; entonces C se cancela (historial conservado).
- **Origen:** extremo de B.
- **Extremo:** extremo direccional de C.
- **`structural_time`:** extremo de B.
- **`knowledge_time`:** tick en que se confirma C.
- **Siguiente pregunta:** `¿CUT?` / `¿C como nuevo 1?` / `¿C como A de lectura mayor?`.
- **Pruebas:** C sin CUT; CUT exacto; C que supera la base; C que no la supera; las tres funciones de C (N-034).

### C-10 — CUT / reset

- **Finalidad:** cerrar el ciclo y abrir el nuevo `1` sin borrar genealogía.
- **Datos:** referencia de CUT (Q3), tick, precio, `cut_confirmed`, `transition_reason`, `parent_reading_id`.
- **Entrada:** C Grande vigente.
- **Pendiente:** mientras C no cruce la referencia.
- **Confirmación:** cruce estricto o alcance, según la respuesta experta Q3.
- **Imposibilidad:** C cancelada por nuevo extremo de B.
- **Origen:** extremo de B.
- **Extremo:** extremo de C en el CUT.
- **`structural_time`:** extremo de B.
- **`knowledge_time`:** tick del cruce.
- **Siguiente pregunta:** `¿nuevo 1 desde la apertura/cierre?`.
- **Pruebas:** CUT exacto; CUT por base; CUT por `a_end`; CUT y TT en el mismo tick; historial conservado.

### C-11 — TT_POSSIBLE / TT_CONFIRMED / TT_EXTREME / FT

- **Finalidad:** confirmar el patrón en el tick exacto y separar patrón de función.
- **Datos:** `tt_target`, `tt_hit`, `tt_time`, `tt_price`, `tt_knowledge_time`, `tt_extreme`, `ft`.
- **Entrada:** `AUT`.
- **Pendiente:** `TT_POSSIBLE` mientras el precio no alcance el objetivo.
- **Confirmación:** primer tick con `precio >= objetivo` (alcista) o `<= objetivo` (bajista).
- **Imposibilidad:** tocar el final de A antes del 100 % → TT fallido, módulo por descarte, A Grande.
- **Origen:** `fin_A`.
- **Extremo:** máximo/mínimo real del TT.
- **`structural_time`:** `fin_A`.
- **`knowledge_time`:** tick del 100 %.
- **Siguiente pregunta:** `¿extremo real?` y, después, `¿FT?`.
- **Pruebas:** TT en el tick; TT y retroceso en el mismo tick; TT extendido; TT fallido por final de A; TT nunca confirmado aunque el precio lo supere (regresión del hallazgo §8 de CE).

### C-12 — GAP_IMPLICIT

- **Finalidad:** resolver el tramo no negociado sin inventar precios.
- **Datos:** `gap`, `open`, `implicit_functions = [A, B_GRANDE, A_TREND]`, `new_1_origin = open`, tiempos.
- **Entrada:** apertura con `|gap| >= 0,25` (Q2).
- **Pendiente:** no aplica; la resolución es inmediata en el primer tick.
- **Confirmación:** registro de las tres funciones implícitas + nuevo `1`.
- **Imposibilidad:** no aplica.
- **Origen:** dueño = nuevo `1` (solo él tiene precio).
- **Extremo:** null para las implícitas; el nuevo `1` actualiza su extremo desde la apertura.
- **`structural_time`:** primer tick negociado.
- **`knowledge_time`:** primer tick negociado.
- **Siguiente pregunta:** `¿2?` (prohibida en la vela del gap) → `¿A?`.
- **Pruebas:** GAP-1..GAP-10 de `FREEBUFF_RC2_GAP_ANALYSIS_v219.md`.

## 3. Fichas transversales

### C-13 — Autoridad de pregunta

- **Finalidad:** una sola respuesta por lectura y tick.
- **Datos:** `machine`, `current_function`, `expected_function`, `active_question`, `candidate_status`, `pending_condition`, `confirmation_condition`, `impossibility_condition`, `transition_reason`, `source_tick`.
- **Regla:** ninguna otra rutina puede escribir la pregunta de una lectura en ese tick.
- **Pruebas:** un único `next_function` por tick; ninguna transición duplicada; ninguna lectura creada por dos rutas.

### C-14 — Genealogía y transformación

- **Finalidad:** conservar identidad cuando una función se convierte en tendencia.
- **Datos:** `parent_reading_id`, `transition_reason`, `replaced_ids`, `origin_function`, `target_function`.
- **Regla:** `A_USED_AS_TREND` y `C_USED_AS_TREND` son transformaciones de la misma lectura, no lecturas nuevas.
- **Pruebas:** mismo `reading_id` antes y después; historial consultable; sin duplicar genealogía.

### C-15 — Capas separadas

- **Finalidad:** que función, patrón y evento coexistan.
- **Datos:** `function_state`, `pattern_state`, `lifecycle_event`.
- **Regla:** confirmar TT no borra C; CUT no borra TT; FT no sustituye A.
- **Pruebas:** C sobre TT activo; TT y CUT en el mismo tick; FT con A concurrente.

## 4. Lo que la arquitectura NO debe incluir todavía

- Velocidad, solapamiento, tiempo M1/M3 y estructura: son capa 2 y no pueden modificar la lectura.
- Umbrales de 6,00 para funciones.
- Confirmaciones al cierre de movimiento o de vela.
- Lecturas nuevas por tamaño o proporción.
- Reglas de FT sin decisión experta.
- Ejecución de órdenes.

## 5. Criterio de aceptación conceptual

La arquitectura será suficiente si puede reproducir, sin mirar el futuro y tick a tick, estas cinco cadenas:

```text
1. 1(2,00) → 2 confirmada → 3 → A → B → B Grande → AUT → TT
2. 1 → 2 imposible → módulo por descarte → A
3. gap → A/B/A-tendencia implícitas → nuevo 1 en apertura
4. AUT → TT 100 % en el tick exacto → TT extendido → FT
5. lectura principal + lectura local con TT independientes
```

Si alguna cadena exige un umbral no escrito en el árbol, la arquitectura no está cerrada y hay que preguntar a Javier.
