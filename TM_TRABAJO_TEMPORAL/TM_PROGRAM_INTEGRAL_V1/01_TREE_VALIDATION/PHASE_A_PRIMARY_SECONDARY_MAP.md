# TM — FASE A — MAPA DE LECTURA PRIMARIA Y SECUNDARIA

- **Fuente:** `PHASE_A_GENERATION_AUDIT.md`, `PHASE_A_GENERATION_CLASSIFICATION.csv`, `BLIND_TREE_EVENTS_1649_1729.csv`
- **Árbol:** v2.19 `94A1408A…`, `WORKING_CANON_NOT_FROZEN`
- **Instrumento:** `blind_reader.py` `54539364…`
- **tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

> Este mapa separa **dos capas** que el lector mezcla:
>
> 1. **Capa primaria (árbol):** el movimiento que la transición convierte en
>    nuevo 1 (C usada como tendencia, A usada como tendencia, extensión de B
>    tras AUT). Es la escalera funcional.
> 2. **Capa local (lector):** el 1 de la vela siguiente, que el lector trata
>    como si fuera la capa primaria.
>
> Las 16 generaciones pertenecen a la **capa local**. La capa primaria tiene 15
> nuevos 1 observables (16 con el heredado de 16:48), pero el lector no los
> desarrolla: sólo los registra como `C_USED_AS_TREND`, `A_USED_AS_TREND` o
> `AUT`, y después abre una generación nueva en la vela siguiente.

---

## 0. LAS DOS CAPAS

```text
CAPA PRIMARIA (árbol)
  transición → el movimiento de la transición es el nuevo 1
  structural_time = tick de la transición
  knowledge_time = tick en que la transición se confirma
  dueño del origen = extremo previo que disparó la transición
  dueño del extremo = el nuevo 1

CAPA LOCAL (lector)
  transición → WAIT_ONE → vela siguiente → 1 = rango direccional de la vela
  structural_time = último tick de la vela local
  knowledge_time = apertura de la vela siguiente
  dueño del origen = extremo de la vela local
  dueño del extremo = extremo de la vela local
```

La capa local no es falsa: es una lectura válida de la vela. El error es
**promoverla** a capa primaria y perder el movimiento de la transición.

---

## 1. CAPA PRIMARIA — LOS 15 NUEVOS 1

| # | Transición | Hora | Nuevo 1 primario | Dirección | Tamaño | Extensión posterior |
|---:|---|---|---|---|---:|---:|
| 1 | C_TREND 16:48 | 16:48:15.900 | C: 29699,9 → 29666,1 | bajista | 33,8 | 29666,1 |
| 2 | C_TREND 16:50 | 16:50:32.234 | C: 29700,8 → 29666,1 | bajista | 34,7 | 29666,1 |
| 3 | AUT 16:52 | 16:52:17.291 | B: 29624,8 → 29607,1 | bajista | 17,7 | 29602,8 |
| 4 | AUT 16:54 | 16:54:27.442 | B: 29629,3 → 29646,6 | alcista | 17,3 | 29680,4 |
| 5 | AUT 16:56 | 16:56:05.283 | B: 29650,1 → 29641,6 | bajista | 8,5 | 29600,7 |
| 6 | AUT 16:58 | 16:58:04.242 | B: 29618,8 → 29630,1 | alcista | 11,3 | 29641,1 |
| 7 | A_TREND 17:00 | 17:00:08.407 | A: 29641,1 → 29623,2 | bajista | 17,9 | 29617,6 |
| 8 | C_TREND 17:07 | 17:07:02.847 | C: 29677,1 → 29615,6 | bajista | 61,5 | 29615,6 |
| 9 | AUT 17:09 | 17:09:23.432 | B: 29645,4 → 29656,1 | alcista | 10,7 | 29661,0 aprox. |
| 10 | A_TREND 17:11 | 17:11:49.457 | A: 29585,1 → 29636,1 | alcista | 51,0 | 29636,1 |
| 11 | AUT 17:13 | 17:13:17.706 | B: 29627,8 → 29641,3 | alcista | 13,5 | 29653,8 / 29679,3 |
| 12 | A_TREND 17:15 | 17:15:37.388 | A: 29679,3 → 29653,3 | bajista | 26,0 | 29653,3 |
| 13 | AUT 17:18 | 17:18:09.401 | B: 29648,0 → 29685,9 | alcista | 37,9 | 29685,9 |
| 14 | AUT 17:21 | 17:21:21.925 | B: 29669,2 → 29631,3 | bajista | 37,9 | 29626,2 |
| 15 | A_TREND 17:25 | 17:25:41.128 | A: 29678,3 → 29632,1 | bajista | 46,2 | 29611,9 |
| 16 | AUT 17:27 | 17:27:51.920 | B: 29624,2 → 29607,1 | bajista | 17,1 | 29594,4 |

> La tabla tiene 16 filas porque incluye la transición heredada de 16:48. El
> bloque observable 16:49–17:29 contiene 15 transiciones; la primera (16:48)
> viene del bloque anterior. Los tamaños son los del movimiento que disparó la
> transición; las extensiones son los extremos posteriores conocidos.

**Lectura:** la capa primaria es una alternancia de nuevos 1 bajistas y
alcistas. Los tamaños 33,8 / 34,7 / 17,7 / 17,3 / 8,5 / 11,3 / 17,9 / 61,5 /
10,7 / 51,0 / 13,5 / 26,0 / 37,9 / 37,9 / 46,2 / 17,1. No es una escalera
monótona: es una secuencia de transiciones, cada una con su propio 1.

---

## 2. CAPA LOCAL — LAS 16 GENERACIONES

### 2.1 Primarias locales (5)

| Gen | 1 local | Dirección | Origen | Extremo | Padre primario | Diferencia de origen | TT | Salida | Estado |
|---:|---|---|---:|---:|---|---:|---|---|---|
| **13** | 64,6 | bajista | 29675,8 | 29611,2 | C_TREND 16:50 (34,7) | +9,7 | 29560,2 FAILED | AUT | Candidata |
| **17** | 17,5 | alcista | 29623,6 | 29641,1 | AUT 16:58 (11,3) | −6,5 | 29643,1 FAILED | A_TREND 0,40 | Candidata |
| **22** | 25,5 | alcista | 29653,8 | 29679,3 | AUT 17:13 (13,5) | +12,5 | 29679,3 FAILED | A_TREND 0,50 | Candidata |
| **26** | 23,4 | bajista | 29640,1 | 29616,7 | A_TREND 17:25 (46,2) | +8,0 | 29596,0 CONFIRMED | AUT | Candidata |
| **27** | 23,7 | bajista | 29618,1 | 29594,4 | AUT 17:27 (17,1) | +11,0 | 29592,4 POSSIBLE | ABIERTA | Candidata abierta |

**Ninguna nace en el extremo de la transición.** Las cinco son movimientos
locales que continúan o retoman la dirección del padre, pero su origen es el
extremo de la vela siguiente. La diferencia de origen va de 6,5 a 12,5 puntos.
Por eso son “primarias locales”, no “primarias funcionales”.

### 2.2 Secundaria (1)

| Gen | 1 local | Dirección | Origen | Extremo | Padre primario | Por qué es secundaria |
|---:|---|---|---:|---:|---|---|
| **21** | 20,5 | alcista | 29615,3 | 29635,8 | A_TREND 17:11 (51,0) | El máximo 29635,8 no supera el extremo de A 29636,1: es un retest, no una extensión. |

Produce AUT (17:13:17.706) y TT confirmado (29650,2), pero **no se convierte en
dominante por producir AUT**. La dominancia no se hereda de un evento; se
decide por la posición estructural.

### 2.3 Integradas (4)

| Gen | 1 local | Dirección | Padre primario | Función real | Evidencia |
|---:|---|---|---|---|---|
| **12** | 33,5 | alcista | C_TREND 16:48 bajista (33,8) | A del 1 bajista | 16:49: 29680,8 → 29666,4 es el 1; 29666,4 → 29699,9 es A |
| **18** | 54,2 | alcista | A_TREND 17:00 bajista (17,9) | A del 1 bajista | 17:00: 29623,2 → 29617,6 es el 1; 29617,6 → 29671,8 es A |
| **19** | 36,7 | alcista | C_TREND 17:07 bajista (61,5) | A del 1 bajista | 17:07: C baja a 29615,6; 29615,6 → 29653,6 es A |
| **23** | 24,7 | alcista | A_TREND 17:15 bajista (26,0) | A del 1 bajista | 17:15: A baja a 29653,3; 29653,3 → 29680,8 es A |

Las cuatro son movimientos reales, no ruido. Se integran porque pertenecen al
padre como A, no porque sean pequeños.

### 2.4 Pendientes (6)

| Gen | 1 local | Dirección | Padre primario | Extensión AUT | Si Q_AUT = extensión | Si Q_AUT = vela |
|---:|---|---|---|---:|---|---|
| **14** | 19,2 | alcista | AUT 16:52 bajista (17,7) | 29602,8 | A del padre | ciclo local |
| **15** | 33,3 | bajista | AUT 16:54 alcista (17,3) | 29680,4 | A del padre | ciclo local |
| **16** | 24,9 | alcista | AUT 16:56 bajista (8,5) | 29600,7 | A del padre | ciclo local |
| **20** | 44,6 | bajista | AUT 17:09 alcista (10,7) | 29661,0 aprox. | A del padre | ciclo local |
| **24** | 28,2 | bajista | AUT 17:18 alcista (37,9) | 29685,9 | A del padre | ciclo local |
| **25** | 44,7 | alcista | AUT 17:21 bajista (37,9) | 29626,2 | A del padre | ciclo local |

Las seis dependen de Q_AUT_DIRECTION. No se clasifican como integradas ni como
válidas hasta que la regla se decida.

---

## 3. DOMINANCIA

### 3.1 Lo que no se hace

- No se elige la capa local como dominante sólo porque tiene 16 ciclos.
- No se elige la capa primaria como dominante sólo porque tiene 16 transiciones.
- No se convierte una secundaria en dominante porque produzca AUT (gen 21).
- No se usa el tramo macro de tres segmentos como respuesta anticipada.

### 3.2 Lo que se conserva

```text
CAPA PRIMARIA .... 16 nuevos 1 (15 observables + 1 heredado)
CAPA LOCAL ....... 16 generaciones: 5 primarias locales, 1 secundaria,
                   4 integradas, 6 pendientes
CAPA MACRO ....... 3 tramos humanos (16:49–17:10, 17:10–17:18, 17:18–17:29)
```

Las tres capas se conservan. La capa primaria es la que el árbol autoriza; la
local es la que el lector produce; la macro es una reconstrucción humana.

### 3.3 Comparación con los tres tramos

| Tramo | Capa primaria | Capa local | Comentario |
|---|---|---|---|
| 16:49–17:10 (−109,7) | C 16:48, C 16:50, AUT 16:52, AUT 16:54, AUT 16:56, AUT 16:58, A_TREND 17:00, C_TREND 17:07, AUT 17:09 | 12, 13, 14, 15, 16, 17, 18, 19, 20 | Las primarias locales 13/17 y las integradas 12/18/19 cubren el tramo; las pendientes 14/15/16/20 son AUT. |
| 17:10–17:18 (+95,7) | A_TREND 17:11, AUT 17:13, A_TREND 17:15, AUT 17:18 | 21, 22, 23, 24 | 21/22 son las primarias locales; 23 integrada; 24 pendiente. |
| 17:18–17:29 (−91,5) | AUT 17:21, A_TREND 17:25, AUT 17:27 | 24, 25, 26, 27 | 26/27 primarias locales; 24/25 pendientes. |

La macro no decide la clasificación; sólo muestra que las tres capas son
compatibles. El tramo 17:10–17:18 es el más claro: la capa primaria tiene dos
A_TREND y dos AUT, y la capa local tiene dos primarias (21, 22), una integrada
(23) y una pendiente (24).

---

## 4. QUÉ SIGNIFICA “PRIMARIA LOCAL”

```text
PRIMARIA LOCAL
  = dirección válida respecto de la transición
  + origen en la vela siguiente, no en la transición
  + módulo/A/B/AUT propios
  + TT propio
  = candidata para la Fase B, no golden
```

No es una función ontológica nueva. No se añade al árbol. Es una etiqueta de
auditoría para separar “dirección correcta” de “origen correcto”.

---

## 5. PREGUNTAS QUE EL MAPA DEJA ABIERTAS

1. **Q_AUT_DIRECTION:** ¿la capa primaria del AUT es la extensión de B o la vela
   siguiente? Decide las 6 pendientes.
2. **Q_LOCAL_VS_PRIMARY:** ¿la capa local tiene estatus ontológico propio o es
   una lectura secundaria de la capa primaria? Decide si las 16 generaciones
   son una lectura válida o sólo una descomposición local.
3. **Q_C_GRANDE:** ¿C Grande es un estado de la capa primaria? Decide si la
   transición C_TREND tiene un estado previo.
4. **Q_A_MARGIN:** ¿A usada como tendencia se dispara en el primer tick o
   necesita autonomía? Decide los orígenes de 18 y 23.

Las preguntas 1 y 2 son las que cambian el número de ciclos. Las preguntas 3 y
4 cambian estados y fronteras.

---

## 6. RESUMEN

| Capa | Qué es | Cuántos | Estado |
|---|---|---:|---|
| Primaria | nuevo 1 de la transición | 16 (15 observables + 1 heredado) | No desarrollada por el lector |
| Local primaria | 1 de la vela siguiente, dirección válida | 5 | Candidatas, no aprobadas |
| Local secundaria | 1 de la vela siguiente, retest | 1 | Conservada, no dominante |
| Local integrada | 1 de la vela siguiente, A del padre | 4 | Integradas |
| Local pendiente | 1 de la vela siguiente, AUT abierta | 6 | Pendientes de Q_AUT |
| Macro | reconstrucción humana | 3 tramos | No es salida del instrumento |

La lectura dominante no se declara. La única conclusión estable es que **la
capa local no puede sustituir a la capa primaria**: 10 de sus 16 generaciones
van en dirección contraria a la transición, y las 6 restantes no nacen en el
extremo de la transición.
