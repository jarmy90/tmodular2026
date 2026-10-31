# FREEBUFF_RC2_GAP_ANALYSIS_v219

**RC-2 — El gap se detecta pero no se resuelve**
**Motor:** R5 `9BD1BEDB…` (`0.7.5.2-R5`) · **Árbol:** `94A1408A…` · **Fecha:** 2026-10-30
**Versión documental:** 1.0
**tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

---

## 1. Las diez preguntas

### 1.1 ¿Qué detecta R5 al aparecer gap?

`_bar_for_tick` (2688-2700) crea la vela nueva con:

```text
gap = open.price - prior_bar.last.price
```

es decir, apertura menos **último tick** de la vela anterior. En cada primer tick de vela, `feed_chunk` llama a `_schedule_gap` (1540-1558). Si `abs(gap) >= 25` (0,25), programa un evento `GAP` con prioridad 0.

La detección es correcta en concepto y en aritmética entera: 10,00 se detecta como 10,00; 0,25 se detecta como 0,25; 0,10 no se detecta.

### 1.2 ¿Qué estado conserva?

**Ninguno.** `_schedule_gap` no escribe en `Reading`, no escribe en `self._local`, no crea referencias, no modifica `module_origin`, `a_end`, `b_extreme` ni `tt_target`. El evento se emite y se olvida.

### 1.3 ¿Qué evento emite?

```text
kind      = GAP
function  = GAP
new_state = GAP
detail    = gap=<valor>
price     = primer precio negociado de la vela nueva
structural_time = knowledge_time = confirmation_time = primer tick
```

Es un evento informativo, sin lectura asociada (`reading=None`).

### 1.4 ¿Qué referencias actualiza?

Ninguna. No actualiza el módulo, ni A, ni B, ni TT, ni el final de A. La lectura anterior sigue midiéndose desde referencias anteriores a la apertura, que es exactamente lo que v2.19 §F prohíbe.

### 1.5 ¿Por qué no registra la resolución funcional implícita?

Porque no existe código para ello. La única rama que menciona funciones en presencia de gap es el guardián de `_process_local_sequence`:

```text
if newbar and abs(bar.gap) >= 25 and phase in (AFTER_3, A_CANDIDATE, A_ACTIVE):
    return
```

Ese `return` **evita decidir**, no resuelve. No hay `A Grande` implícita, ni `B Grande` implícita, ni `A usada como tendencia`. El comentario del código lo dice: "the structural branch is resolved with the ticks that follow", pero los ticks que siguen no tienen ninguna rama que los recoja.

### 1.6 ¿Por qué no entrega un nuevo `1` desde la apertura?

Porque el nuevo `1` solo puede nacer de:

- `_open_candidate` → `FIRST`, que exige un `Movement` cerrado (≥ 6,00 y retroceso); o
- `_new_local_reading_after_aut`, que exige un `AUT` previo.

Un gap no es ninguna de las dos cosas. El motor no tiene un constructor de `1` desde una apertura.

### 1.7 ¿La omisión depende de RC-1?

**Parcialmente.**

| Aspecto | ¿Depende de RC-1? |
|---|---|
| Detección del gap | no |
| `NO_TWO` con gap | no (ya funciona en `WAIT_TWO`) |
| Registro de funciones implícitas | no (podrían emitirse como eventos sin precios) |
| Nuevo `1` desde la apertura | **sí**: necesita el ciclo de vida de `1` (RC-1.1) |
| Continuación tick a tick desde la apertura | **sí**: necesita una lectura viva con origen en la apertura |
| Rama local de gap | **sí**: LOCAL nunca se arma sin AUT (RC-1.2) |

Por tanto, RC-2 no es totalmente independiente, pero **su primer paso (registrar A/B/A-tendencia implícitas) podría hacerse sin resolver RC-1**. El segundo (nuevo `1`) no.

### 1.8 ¿Puede corregirse después de resolver el bootstrap?

Sí, y es el orden correcto:

1. Resolver el ciclo de vida de `1` (RC-1.1).
2. Definir un objeto funcional implícito (sin precios) para A, B Grande y A usada como tendencia.
3. Crear el nuevo `1` con `origen = OPEN` y `structural_time = knowledge_time = primer tick`.
4. Reanudar la lectura tick a tick desde esa apertura.
5. Verificar que no se evalúa `2` en esa vela.

Si se intenta antes del bootstrap, el nuevo `1` no tendría dónde alojarse y se crearía otra lectura `MODULE` tardía, reproduciendo el mismo error.

### 1.9 ¿Cómo representar funciones implícitas sin precios inventados?

Propiedad mínima:

```text
FUNCTION_RECORD
  function       = A_GRANDE | B_GRANDE | A_USADA_COMO_TENDENCIA
  implicit       = true
  origin_price   = null        # prohibido inventar
  extreme_price  = null
  origin_time    = null
  extreme_time   = null
  knowledge_time = tick de apertura
  structural_time= tick de apertura (solo para el nuevo 1)
  sequence       = A → B_GRANDE → A_TENDENCIA
  reading_id     = lectura en la que se registran
  origin_note    = "gap_no_negociado"
```

El nuevo `1` sí tiene precio:

```text
ORIGEN_NUEVO_1        = OPEN de la segunda vela
STRUCTURAL_TIME_NUEVO_1 = primer tick negociado
KNOWLEDGE_TIME_NUEVO_1  = primer tick negociado
```

Prohibiciones que la estructura debe hacer imposibles:

- rellenar `origin_price` o `extreme_price` de las funciones implícitas con el cierre previo o la apertura;
- simular ticks intermedios;
- medir todo el gap como una sola A Grande;
- fijar el nuevo `1` en el cierre anterior;
- abrir `2` en la vela del gap.

### 1.10 ¿Qué pruebas necesita?

| Prueba | Condición | Resultado exigido |
|---|---|---|
| GAP-1 | cierre 100,00, apertura 110,00 | 3 funciones implícitas + nuevo `1` en 110,00 |
| GAP-2 | apertura 100,10 | sin gap, sin implícitas |
| GAP-3 | apertura 100,25 | decisión experta Q2 antes de fijar expectativa |
| GAP-4 | gap y TT pendiente heredado | v2.7: resolver TT/final de A antes de la rama de gap |
| GAP-5 | gap tras `1` con `2` imposible | `NO_TWO` + resolución implícita |
| GAP-6 | gap contrario a la estructura | A Grande implícita en la dirección del gap |
| GAP-7 | gap y `3` confirmado | no se abre `2`; nuevo `1` desde apertura |
| GAP-8 | dos gaps consecutivos | cada uno con su propia resolución, sin mezclar referencias |
| GAP-9 | gap con precio que vuelve al cierre previo | el nuevo `1` sigue teniendo origen en la apertura |
| GAP-10 | ausencia de ticks intermedios | ninguna función implícita tiene precio interno |

## 2. Evidencia de ejecución

Eventos `GAP` observados en las 21 secuencias:

| Caso | Tick | Precio | Gap | Fase local | Lectura | Comentario |
|---|---:|---:|---:|---|---|---|
| CE3-NEG | 4 | 6,25 | +0,25 | IDLE | ninguna | 0,25 exactos: R5 lo trata como gap; H14 lo llamaría plano |
| CE5-POS | 12 | 15,75 | −0,25 | IDLE | ninguna | gap de 0,25 en una secuencia que no es de gap |
| CE6-POS | 5 | 110,00 | +10,00 | IDLE | ninguna | gap real, sin resolución |
| CE6-FRON | 5 | 100,25 | +0,25 | IDLE | ninguna | frontera 0,25, sin resolución |

**Observaciones:**

1. El gap se detecta **antes** de cualquier lectura: `phase=IDLE`, `armed=False`. No hay ninguna estructura a la que aplicar la resolución.
2. En los dos casos con gap real, el único evento funcional es `GAP`; no hay `A`, `B`, `A-tendencia` ni `LECTURA_CREADA`.
3. En CE3-NEG y CE5-POS el evento `GAP` aparece por una diferencia de exactamente 0,25, que el árbol H14 considera plano. Es una consecuencia directa de la contradicción documental (Q2), no de una decisión del motor.

## 3. Por qué el gap no puede resolverse con la arquitectura actual

```text
GAP detectado
→ no hay Reading viva
→ no hay ONE_CANDIDATE
→ no hay módulo
→ no hay A/B
→ no hay dónde registrar las implícitas
→ no hay nuevo 1
→ la lectura posterior (si nace) se ancla en referencias anteriores
```

La máquina local, que sí tiene fases y un `1`, no puede recibir el gap porque `armed=False`: el gap ocurre antes del primer AUT. Y aunque estuviera armada, el guardián solo hace `return`.

## 4. Relación con v2.7 (TT pendiente)

v2.7 exige que, al entrar en una vela con TT pendiente, se resuelva primero **qué frontera se alcanza antes**: objetivo TT o final de A. R5 no tiene ese árbitro. Si además hay gap, la rama de gap debe aplicarse **después** de resolver el TT pendiente, no antes. Hoy:

- no hay árbitro TT/final de A;
- no hay rama de gap funcional;
- por tanto, la combinación "TT pendiente + gap" es doblemente inalcanzable.

## 5. Conclusión

RC-2 es un fallo de **representación**, no de detección. El motor sabe *que* hay un hueco; no sabe *qué significa* el hueco. La corrección exige:

1. un objeto funcional implícito sin precios;
2. un constructor de `1` desde la apertura;
3. un orden de precedencia que coloque la resolución del TT pendiente antes de la rama de gap;
4. una prueba de frontera para 0,25 que dependa de la respuesta experta Q2.

Nada de esto se implementa en esta fase.
