# TM — ÁRBOL MAESTRO CANÓNICO COMPLETO v2.13 R1 (PROPUESTA)

- **Estado:** `CANDIDATO_PENDIENTE_AUDITORIA_MIMO_Y_APROBACION_JAVIER`
- **Fecha:** 2026-10-28
- **Base documental:** `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_12.md` (histórica, preservada íntegra en `historical/`).
- **Golden humano vigente:** `TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v003.txt`.
- **Árbol activo aprobado antes de esta propuesta:** v2.12. Esta propuesta no lo sustituye.
- **Autoridad:** Javier. Las instrucciones expresas de Javier gobiernan las correcciones señaladas abajo. La decisión de autoridad sobre plano/gap está anexada en `DECISION_AUTORIDAD_PLANO_GAP_JAVIER.md`.

## 0. Estado y precedencia de esta propuesta

Este documento propone una normalización canónica v2.13. Hasta aprobación expresa de Javier, v2.12 sigue siendo la base autorizada y el archivo estable `TM_ARBOL_ACTIVO.md` conserva el SHA-256 de v2.12. Ningún motor, test, validador, salida de `GOLDEN.py` ni informe técnico eleva una lectura o establece una regla teórica.

Orden aplicado al preparar la propuesta:

1. Instrucción expresa actual de Javier para v2.13.
2. Decisiones expertas cerradas compatibles (`DECISIONES_EXPERTO.md`).
3. Reglas cerradas compatibles (`REGLAS_CERRADAS.md`).
4. Golden humano v003 para estados de velas, nunca para inferir reglas.
5. v2.12, dossiers y anexos como fuentes históricas; lo incompatible se etiqueta abajo.

### Estados editoriales

- **VIGENTE:** regla aceptada para esta propuesta por instrucción actual o decisión cerrada compatible.
- **SUPERADA:** formulación explícitamente sustituida; se conserva solo la cita histórica y su trazabilidad.
- **HISTÓRICA:** material preservado como antecedente, sin autoridad normativa actual.
- **PENDIENTE:** no se decide ni se amplía en esta fase.

## 1. Ontología formal — VIGENTE

**Funciones TM:** `1`, `2`, `3`, `A`, `B`, `C`, `AUT`, `CUT`.

**Patrones TM:** `TT`, `FT`.

**Módulo** es una estructura de referencia, no una función ni un patrón.

La palabra **«Tercero»** queda únicamente como término histórico superado. La función vigente se denomina `3`; no se crea una entidad TM adicional.

No se incorporan variables como capa normativa v2.13. Las secciones de variables del árbol v2.12 quedan fuera del cuerpo vigente de esta propuesta y se conservan como historia documental.

## 2. Lectura causal — VIGENTE

La TM describe movimientos y funciones a partir de ticks en orden físico. Una vela puede contener varios movimientos; un movimiento puede atravesar varias velas. OHLC, color, el resultado final o la salida de un motor no sustituyen el orden de ticks.

En cada lectura se distinguen, cuando están disponibles:

- `structural_time` y `structural_sequence_id`: inicio/extremo que pertenece a la estructura;
- `confirmation_time` y `confirmation_sequence_id`: tick en que se satisface la condición de confirmación;
- `knowledge_time` y `knowledge_sequence_id`: momento en que la lectura conoce y puede declarar esa confirmación.

La confirmación posterior no se retrotrae como conocimiento disponible en un prefijo anterior. Las reclasificaciones conservan genealogía, referencias y cronología; no borran eventos previos. Lecturas concurrentes mantienen sus propias referencias y ownership.

## 3. Plano, gap y regla de 2 — VIGENTE

La referencia es el **cierre de la vela anterior**, conforme a DEC-013. Sea `Δ = apertura_nueva − cierre_vela_anterior`:

```text
PLANO  ⇔ |Δ| < 0,25 puntos
GAP    ⇔ |Δ| ≥ 0,25 puntos
```

La igualdad exacta de 0,25 es **no plano** y corresponde a gap. Por tanto, 0,10, 0,20 y 0,24 son plano; 0,25 o más no son plano. Esta regla sustituye globalmente las antiguas fórmulas inclusivas `≤ 0,25` para plano. La decisión de autoridad reproducida en el anexo citado respalda esta frontera.

Si hay gap, no hay posible 2 ni 2. Si hay plano, se comprueban causalmente:

1. la cola inicial observable contraria; si supera 0,25, no hay 2;
2. la dirección, que debe coincidir con la función 1;
3. el desplazamiento direccional de 2, que debe ser igual o mayor que el de 1.

Solo si se satisfacen esas condiciones se confirma 2. El 3 se evalúa después del 2 confirmado. Si 2 no se confirma, 1 puede quedar como módulo por descarte, sujeto a las referencias de la lectura. La regla no crea una función por cada oscilación o cambio de direcci?n.

### Regla de 2 y golden

El golden v003 aporta ejemplos humanos confirmados: 16:16 abre con +0,1 y no es 2 por tamaño menor que 1; 16:20 abre con −0,2, cumple cola y dirección, y su recorrido supera el de 16:19. No aporta un ejemplo de frontera exacta ±0,25; esa igualdad se define por la regla experta de esta propuesta, no se infiere del golden.

## 4. Ruido y movimientos — VIGENTE/PENDIENTE, sin ampliar control

La instrucción de fase establece menos de 2 puntos como ruido y 2 puntos exactos como umbral de confirmación retroactiva de movimiento. El umbral no obliga por sí solo a abrir una función ni a fragmentar la función dominante. La decisión metodológica posterior DEC-015 prohíbe calcular ruido y micromovimientos como lecturas y deja abierto el umbral numérico general (PR-g). Se conserva esta diferencia documental: esta propuesta no modifica `REGLAS_PROVISIONALES.md` ni añade criterios de fragmentación. La aplicación general de un umbral de 2 puntos queda **PENDIENTE** de reconciliación expresa con DEC-015.

## 5. Módulo y funciones — VIGENTE dentro de decisiones cerradas

- El módulo es la estructura de referencia de la lectura; no es función.
- Se mantiene normalmente un módulo principal y un único mini módulo actual; no se encadenan mini módulos.
- Si A del mini módulo supera su base según la lectura que gobierna, se integran módulos conservando esa misma A. Los criterios generales de módulo por descarte permanecen sujetos a DUDA-009 cuando no estén fijados por una escena aprobada.
- 1 establece dirección. 2 requiere gap/plano, cola, dirección y tamaño conforme §3. 3 se considera únicamente después de 2 confirmado; su genealogía se conserva.
- A Grande es el movimiento contrario al módulo y puede prolongarse entre velas hasta su extremo real. El cambio de vela no la cierra automáticamente.
- Antes de alcanzar el 100 % de A, el movimiento contrario es B candidata. Al alcanzar 100 % queda confirmada B Grande si no supera el umbral de AUT. B Grande deja de ser la clasificación vigente del recorrido que supera estrictamente 127 % de A + 0,25 puntos.
- Una lectura grande puede permanecer secundaria. Una lectura pasa a dominante cuando causalmente sustituye a la anterior; la vela no se eleva por comparación retrospectiva con un precio golden.

### Disparadores AUT y límite de generalización

Se conservan los dos disparadores distinguibles de DEC-014: (1) B Grande supera 127 % de A + 0,25; (2) A Grande contra el módulo supera el inicio del módulo. La generalización del segundo disparador depende de la regla general de módulo pendiente en DUDA-009. La evidencia de un caso golden no cierra esa regla pendiente.

## 6. CUT — VIGENTE solo en su condición cerrada

C Grande solo se evalúa después de B Grande confirmada. CUT se confirma cuando C Grande supera el final real de A Grande. Esta propuesta no convierte en reglas cerradas secuencias históricas adicionales de reset, «Tercero» o tratamiento posterior a CUT si no están respaldadas por una decisión posterior compatible.

## 7. TT y FT — VIGENTE limitado a decisiones expresas

- TT solo se confirma cuando el precio alcanza el 100 % de su expansión. Aproximarse no basta.
- El objetivo se mide desde el extremo real de A usando el módulo de referencia de esa lectura.
- FT estructural solo se evalúa después de TT confirmado y desde el extremo real alcanzado por TT.
- La preparación operativa de FT ocurre durante la extensión de TT, antes del comienzo del movimiento contrario; iniciado FT no se persigue una entrada tardía.
- Si un TT operado cierra por detrás del 100 %, FT queda prohibido operativamente.
- No se incorporan aquí reglas históricas nuevas de TT fallido, expiración de FT, entrada tardía, ni gestión posterior. Esas semánticas siguen pendientes donde figuran en los documentos de control. No se amplía FT en esta propuesta.

## 8. Concurrencia y dominancia — VIGENTE/PENDIENTE

La concurrencia es habitual: normalmente coexisten dos lecturas y excepcionalmente tres si todas siguen siendo matemáticamente válidas y coherentes. Ruido y micromovimientos no abren lecturas. Cada lectura conserva referencias, genealogía y estado independientes. La lectura más grande puede seguir secundaria; la dominancia cambia cuando la lectura vigente es sustituida causalmente.

La prioridad total, el empate de referencias en el mismo tick y la sustitución general entre lecturas siguen **PENDIENTES** (DEC-015 / P5). No se promueven reglas de concurrencia de anexos antiguos que contradigan las decisiones posteriores.

## 9. Golden humano v003 — evidencia, no fuente de reglas

Se conserva cada estado A/B/C/D del documento humano. Solo las velas expresamente completas son `CONFIRMADA_COMPLETA`; B permanece parcial, C es referencia física y D queda pendiente. No se promueve ninguna vela usando el motor, `GOLDEN.py`, tests, cobertura, OHLC o reconstrucción retrospectiva.

El registro completo minuto a minuto está en `TM_v2_13_REGISTRO_GOLDEN_HUMANO.csv`; la relación regla-evidencia y sus límites está en `TM_v2_13_REGLA_A_GOLDEN.csv`.

**Confirmadas completas A:** 16:15–16:24, 16:30–16:32 y 16:37. Esto conserva el bloque 16:15–16:24 íntegro como golden completo conforme a v003.

**Parciales B:** 16:33–16:36 (estado del resumen; la sección 5 describe referencia física y deja abierta la función), 16:38–16:39 (etiqueta literal `[A/B]` conservada de v003; clasificación parcial según la instrucción expresa de Javier), y 16:42–16:48. 16:38–16:39 se mantienen parciales; no son golden completo.

**Pendientes D:** 16:25–16:29, 16:40–16:41 y 16:49–17:29. No hay filas C expresamente declaradas en el resumen v003.

### Evidencia canónica 16:15–16:24

- 16:16: diferencia +0,1, plano, sin cola inicial en contra y recorrido menor que 16:15; módulo por descarte.
- 16:19: 1 bajista; 16:20: 2 bajista confirmado; 16:21: 3 confirmado.
- 16:22: A Grande alcista; supera la referencia del módulo de la secuencia 1-2-3 de 16:19-16:21 en 0,8 puntos; confirma AUT alcista y nuevo 1 alcista dominante. 29850,0 es referencia física de esa lectura, no regla hardcodeable; no se exige 29877,0.
- 16:23: apertura +0,3 respecto del cierre anterior; según v003, `|Δ| >= 0,25`, por tanto NO PLANO y no abre en plano. Es un contraejemplo de la frontera, no un ejemplo de plano.
- 16:23–16:24: se conservan las lecturas completas y el orden causal descrito por v003.

## 10. Clasificación del contenido recibido de v2.12

El archivo v2.12 se preserva íntegro y separado en `historical/`. La siguiente clasificación gobierna su uso dentro de esta propuesta:

| Contenido de v2.12 | Estado en v2.13 | Tratamiento |
|---|---|---|
| Parches históricos 0.1–0.7 | HISTÓRICA; reglas expresamente compatibles se resumen en §§2–8 | No se copian como autoridad automática. |
| Ontología 0.8 | SUPERADA en la lista de funciones/patrones | Sustituida por §1; variables no entran en el cuerpo vigente y «Tercero» queda como término histórico superado. |
| Separación lectura/variables y variables 0.9–0.16 | HISTÓRICA / FUERA DE ALCANCE | No se implementan ni amplían variables. |
| Reglas de gap/plano en capítulos 1–4 y árbol de transiciones | SUPERADA donde usa `≤ 0,25` para plano; restante conforme §§3–5 | Se aplica globalmente `< 0,25`; la regla de cola de 2 es una condición distinta. |
| A/B/C/AUT y TT/CUT | VIGENTE solo en reglas cerradas compatibles de §§5–7 | Las variantes históricas de reset o desenlace no cerradas pasan a HISTÓRICA o PENDIENTE. |
| FT y operabilidad | PENDIENTE salvo los límites expresos de §7 | No se extienden criterios de umbral, expiración o entrada. |
| Concurrencia | VIGENTE en el alcance de §8; detalles en conflicto HISTÓRICOS/PENDIENTES | Se conserva normalmente 2, excepcionalmente 3; no se hereda prioridad no cerrada. |
| Casos, ejemplos, anexos v1 y versiones anteriores | HISTÓRICA | Evidencia de trazabilidad, no golden vigente ni nuevas reglas. |

## 11. Reglas superadas y contradicciones

El listado auditable de fórmulas anteriores y citas está en `REGLAS_SUPERADAS.csv`. Las discrepancias resueltas y pendientes están en `CONTRADICCIONES_RESUELTAS_Y_PENDIENTES.md`. No se modifica ningún documento original de reglas pendientes.

## 12. Control de aprobación

Esta propuesta se instala como `CANDIDATO_PENDIENTE_APROBACION`. La base activa y aprobada permanece v2.12 hasta que Javier apruebe expresamente `ARBOL_v2_13_APROBADO_POR_JAVIER`. La Fase 2 no está autorizada por este documento.
