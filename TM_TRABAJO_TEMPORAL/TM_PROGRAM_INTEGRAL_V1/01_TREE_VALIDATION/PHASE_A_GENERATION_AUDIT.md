# TM — FASE A — AUDITORÍA FUNCIONAL DE LAS 16 GENERACIONES

- **Fecha:** 2026-10-30
- **Bloque:** 16:49:00.012 → 17:29:59.897 (11.414 ticks, secuencias 8922–20335)
- **Árbol:** v2.19 `94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17`
- **Estado del árbol:** `WORKING_CANON_NOT_FROZEN`
- **Tickfeed:** `5F701BE2307352CB559ABBD7BB856A6FD2A1F91E5D269A93DCC9AE2992E2C9FF`
- **Lecturas humanas:** v005 `F5D7550C42C90897D833E6C2A3FAF772753A129640FD4411DE4190CB2CF94226` (bloque **[D]**, sin golden)
- **Instrumento:** `blind_reader.py` SHA-256 `5453936409204D742D74E6F51D73B09DC3E1185E23F633261B5179C7E392F458`
- **Salida bloqueada:** `BLIND_TREE_GENERATIONS_1649_1729.csv` SHA-256 `63768588AA7C0770BFFE7569511B0B52ABD2AEF06FC26E28348D4CED792FB62B`
- **Eventos:** `BLIND_TREE_EVENTS_1649_1729.csv` SHA-256 `369E823C9540073D071CE10B8BF073A69194B46AF3A90FDE6367E513AAAD2111`
- **Traza:** `BLIND_TREE_TRACE_1649_1729.jsonl` SHA-256 `8150F4023523F37A7717101C8035BBD41DA85ECF96CA0C006251BD338814AB03`
- **Determinismo:** `b219049b26d1221905b7451a92ba4710ea6b7103e54f7088fa74ca230656eede` (doble ejecución idéntica, `verify_phase_a.json`)
- **tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

> Esta auditoría **no re-ejecuta** el lector, no corrige el árbol, no cambia
> expectativas y no usa información futura. Trabaja sobre la salida ya
> bloqueada y compara la dirección y la propiedad de cada extremo con la
> transición que abrió la generación. No aprueba las 16 generaciones.

---

## 0. RESUMEN EJECUTIVO

| Hecho | Resultado |
|---|---|
| Generaciones auditadas | 16 (12–27) |
| Inversiones de dirección | **10 de 16** |
| — violación explícita de v2.17 (C_TREND) | **2** (12, 19) |
| — inferencia fuerte de v2.18 (A_TREND) | **2** (18, 23) |
| — regla AUT abierta (4.5) | **6** (14, 15, 16, 20, 24, 25) |
| Dirección válida | **6** (13, 17, 21, 22, 26, 27) |
| Candidatas principales (dirección válida) | **5** (13, 17, 22, 26, 27) |
| Secundaria (dirección válida, retest) | **1** (21) |
| Integradas en el módulo padre | **4** (12, 18, 19, 23) |
| Pendientes de decisión experta | **6** (14, 15, 16, 20, 24, 25) |
| Origen de 1 en el extremo de la transición | **0 de 16** |
| Tiempo del bloque fuera de toda 1 generacional | **551,5 s = 9,19 min = 22,4 %** |
| Primera divergencia | **gen 12**, `structural_time` 16:49:59.949, `knowledge_time` 16:50:00.152 |
| Golden humano | **no existe**; v005 marca el bloque [D] |

**Conclusión corta:** la lectura de 16 generaciones no es una escalera de
nuevos 1. Es una cadena de **movimientos locales posteriores a la transición**
(la vela siguiente), no del movimiento que la transición convirtió en nuevo 1.
En 10 casos ese movimiento local va en dirección contraria a la transición; en
los 6 restantes coincide, pero su origen sigue siendo el extremo de la vela, no
el extremo de la transición. La primera divergencia está ya en la generación 12
y se propaga a toda la cadena.

---

## 1. MÉTODO

1. Se leyó la salida bloqueada: 16 generaciones, 454 eventos, 41 velas.
2. Para cada generación se reconstruyó la transición de entrada a partir del
   `ended_by` de la generación anterior y de sus extremos A/B/C:
   - `AUT` → dirección de B (opuesta a A);
   - `A_USED_AS_TREND` → dirección de A;
   - `C_USED_AS_TREND` → dirección de C.
3. Se comparó esa dirección con la dirección del 1 del lector,
   `sign(one_extreme − one_origin)`.
4. Se separó la fuerza de la regla:
   - **EXPLICIT**: v2.17 dice “nuevo 1 en su propia dirección” para C.
   - **STRONG_INFERENCE**: v2.18 no repite la frase para A, pero “A usada como
     tendencia” implica continuidad; se marca como inferencia fuerte, no como
     texto literal.
   - **OPEN**: 4.5 dice “AUT confirma inmediatamente el nuevo 1” sin fijar la
     dirección.
5. Se auditó la propiedad de cada extremo: quién lo alcanzó y si pertenece a 1,
   2, A, B o C.
6. Se buscó el primer punto en que la fragmentación deja de estar respaldada
   por una transición. No se usaron los tres tramos macro como respuesta.

**Límites:**

- No se releyó el bloque tick a tick con una semántica corregida; eso es Fase B.
- No se declara que las 5 candidatas principales sean canónicas: sólo que su
  dirección coincide con la transición.
- La regla de dirección de AUT es una cuestión abierta, no una violación
  demostrada.
- El bloque no tiene golden humano; no se puede comparar contra v005.

---

## 2. LA REGLA DE DIRECCIÓN

### 2.1 Lo que dice el árbol

```text
v2.17  C Grande supera la base del módulo
       → C usada como tendencia
       → nuevo 1 EN SU PROPIA DIRECCIÓN

v2.18  A Grande usada como tendencia
       → nuevo 1
       (la frase “en su propia dirección” no se repite, pero la transición
        significa que A pasa a ser la tendencia)

4.5    AUT confirma inmediatamente el nuevo 1
       (no dice si el nuevo 1 es la extensión de B o la vela siguiente)
```

### 2.2 Lo que hace el lector

En `blind_reader.py`:

```python
def confirm_one(self, r, t):
    d = 1 if c > o else (-1 if c < o else 0)
    r.direction = d
    r.one_origin = h if d < 0 else l
    r.one_extreme = l if d < 0 else h
```

La dirección se decide por **el cierre contra la apertura de la vela**, no por
la transición que abrió la generación. El `origin_reason` se guarda, pero no se
usa para orientar el 1. Además, `reset_generation` deja la fase en `WAIT_ONE` y
`start_one_candle` arranca el 1 en la **vela siguiente**, no en el tick de la
transición.

Esto produce dos errores independientes:

| Error | Qué hace | Efecto |
|---|---|---|
| **E-DIR** | orienta el 1 por la vela, no por la transición | 10/16 inversiones |
| **E-ORIG** | hace nacer el 1 en la vela siguiente, no en el extremo de la transición | 16/16 orígenes desplazados |

Los dos errores se refuerzan: al esperar la vela siguiente, el lector pierde el
movimiento de la transición y toma el primer movimiento contrario como 1.

---

## 3. PRIMERA DIVERGENCIA — GEN 12, 16:49–16:50

### 3.1 Movimiento

```text
16:48:15.900   C_USED_AS_TREND heredado
               C = 29666,1   base del módulo = 29666,4   dirección C = −1

16:49          OHLC 29680,8 / 29699,9 / 29666,4 / 29689,9
               primer tramo: 29680,8 → 29666,4 = 14,4 bajista
               segundo tramo: 29666,4 → 29699,9 = 33,5 alcista
```

### 3.2 Lo que hace el lector

```text
16:50:00.152   ONE_CONFIRMED
               dir = +1
               origen = 29666,4   extremo = 29699,9   tamaño = 33,5
```

La vela cerró por encima de su apertura, así que el lector la leyó alcista. El
1 es el **segundo tramo**, el rebote.

### 3.3 Lo que dice el árbol

La transición de 16:48 fue `C_USED_AS_TREND` bajista. El nuevo 1 es el
movimiento de C, en su propia dirección: **bajista**. El primer tramo de 16:49,
29680,8 → 29666,4 = **14,4 bajista**, es la continuación del nuevo 1. El rebote
29666,4 → 29699,9 = **33,5** es el primer movimiento contrario, es decir **A**,
no 1.

```text
LECTOR:  1 alcista 33,5   A bajista 16,2   B alcista 17,1   C bajista 34,7
ÁRBOL:   1 bajista 14,4   A alcista 33,5   B bajista …       C …
```

La escalera del lector está **desplazada una función**: su 1 es la A del árbol;
su A es parte de la B; su B es parte de la C; su C es la extensión de la B.

### 3.4 Tiempos

| Tiempo | Valor | Qué es |
|---|---|---|
| 16:49:00.012 | 29680,8 | primer tick del bloque; apertura de la vela |
| 16:49:59.949 | 29689,9 | cierre de la vela; el rango ya es conocido |
| **16:50:00.152** | **29699,9 / 29666,4** | **`knowledge_time` de la divergencia: `ONE_CONFIRMED`** |

`structural_time` del 1 del lector = 16:49:59.949 (cierre de la vela).
`knowledge_time` = 16:50:00.152 (confirmación). La divergencia no es de
`knowledge_time`: es de **qué movimiento es 1**.

### 3.5 Propagación

- El módulo de 33,5 no es un módulo: es una A.
- La A de 16,2 no es A: es parte de la B.
- El AUT de 16:50 no es AUT de un módulo de 33,5; es la extensión de una B
  dentro de un módulo de 14,4.
- El C_TREND de 16:50:32 nace de esa B, no de un C de 34,7 sobre un módulo de
  33,5.
- La generación 13 hereda la transición, pero su 1 (64,6) es la B/AUT del
  padre, no un nuevo 1.

**La primera fragmentación no respaldada es la primera generación.** No hay un
punto posterior donde la cadena “empiece” a fallar: falla en su primer 1.

---

## 4. LAS 10 INVERSIONES

| Gen | Transición | Hora | Dir. trans. | Dir. 1 | 1 (pts) | Regla | Clasificación |
|---:|---|---|---:|---:|---:|---|---|
| **12** | C_TREND | 16:48:15.900 | −1 | **+1** | 33,5 | v2.17 explícita | **INTEGRADA** |
| **14** | AUT | 16:52:17.291 | −1 | **+1** | 19,2 | 4.5 abierta | PENDIENTE |
| **15** | AUT | 16:54:27.442 | +1 | **−1** | 33,3 | 4.5 abierta | PENDIENTE |
| **16** | AUT | 16:56:05.283 | −1 | **+1** | 24,9 | 4.5 abierta | PENDIENTE |
| **18** | A_TREND | 17:00:08.407 | −1 | **+1** | 54,2 | v2.18 inferencia fuerte | **INTEGRADA** |
| **19** | C_TREND | 17:07:02.847 | −1 | **+1** | 36,7 | v2.17 explícita | **INTEGRADA** |
| **20** | AUT | 17:09:23.432 | +1 | **−1** | 44,6 | 4.5 abierta | PENDIENTE |
| **23** | A_TREND | 17:15:37.388 | −1 | **+1** | 24,7 | v2.18 inferencia fuerte | **INTEGRADA** |
| **24** | AUT | 17:18:09.401 | +1 | **−1** | 28,2 | 4.5 abierta | PENDIENTE |
| **25** | AUT | 17:21:21.925 | −1 | **+1** | 44,7 | 4.5 abierta | PENDIENTE |

### 4.1 Las dos violaciones explícitas de C_TREND

**Gen 12.** C bajista 29700,8 → 29666,1 (34,7) sobre la base 29666,4. El nuevo 1
debe ser bajista. El lector hace 1 alcista de 33,5. Es el rebote, no la
continuación.

**Gen 19.** C bajista 29677,1 → 29615,6 (61,5) sobre la base 29617,6. El nuevo 1
debe ser bajista. El lector hace 1 alcista de 36,7. Otra vez el rebote.

En los dos casos el movimiento del lector es **A**, no 1. No son ambigüedades:
v2.17 dice “en su propia dirección”.

### 4.2 Las dos inferencias fuertes de A_TREND

**Gen 18.** A bajista 29641,1 → 29623,2 (17,9) sobre la base 29623,6. El nuevo 1
debe continuar bajista. El lector hace 1 alcista de 54,2 (29617,6 → 29671,8).
El movimiento bajista que continúa es sólo 5,6 puntos (29623,2 → 29617,6); el
resto, 54,2, es la A del nuevo 1.

**Gen 23.** A bajista 29679,3 → 29653,3 (26,0) sobre la base 29653,8. El nuevo 1
debe continuar bajista. El lector hace 1 alcista de 24,7 (29656,1 → 29680,8).
Otra vez el rebote.

La frase “en su propia dirección” no se repite en v2.18, pero “A usada como
tendencia” significa que A pasa a ser la tendencia. Se marca como **inferencia
fuerte**, no como texto literal. Si Javier no confirma la inferencia, estas dos
generaciones pasan a `PENDING`, no a `INTEGRADA`.

### 4.3 Las seis AUT abiertas

| Gen | AUT | Precio AUT | 1 del lector | Extremo real de la extensión AUT | Origen 1 − extremo AUT |
|---:|---|---:|---|---:|---:|
| 14 | 16:52:17.291 | 29607,1 | alcista 29622,9 → 29642,1 = 19,2 | 29602,8 (16:52:32) | **+20,1** |
| 15 | 16:54:27.442 | 29646,6 | bajista 29680,4 → 29647,1 = 33,3 | 29680,4 (16:55:12) | **0,0** |
| 16 | 16:56:05.283 | 29641,6 | alcista 29600,2 → 29625,1 = 24,9 | 29600,7 (16:56:39) | **−0,5** |
| 20 | 17:09:23.432 | 29656,1 | bajista 29634,8 → 29590,2 = 44,6 | 29661,0 aprox. | **−26,2** |
| 24 | 17:18:09.401 | 29685,9 | bajista 29669,8 → 29641,6 = 28,2 | 29685,9 (sin extensión) | **−16,1** |
| 25 | 17:21:21.925 | 29631,3 | alcista 29633,6 → 29678,3 = 44,7 | 29626,2 (17:21:24) | **+7,4** |

En los seis casos la **dirección es contraria** a la extensión AUT. En cuatro
(14, 20, 24, 25) el origen además está desplazado; en 15 y 16 el origen
coincide con el extremo, pero el 1 toma la dirección opuesta. Si 4.5 exige que
el nuevo 1 sea la extensión de B, las seis son A, no 1.

**Por eso no se clasifican como integradas todavía:** 4.5 no fija la dirección.
La respuesta a Q_AUT decide si se integran o si son ciclos locales válidos.

---

## 5. CLASIFICACIÓN DE LAS 16

| Gen | Transición | 1 (pts) | Módulo (pts) | A (pts) | B (pts) | Fin | Clasificación | Nota |
|---:|---|---:|---:|---:|---:|---|---|---|
| 12 | C_TREND 16:48 | 33,5 | 33,5 | 16,2 | 17,1 | C_TREND | **INTEGRADA** | C explícita; 1 = A del padre |
| 13 | C_TREND 16:50 | 64,6 | 64,6 | 13,6 | 17,7 | AUT | **PRIMARIA LOCAL** | C 0,30; 1 = B/AUT del padre |
| 14 | AUT 16:52 | 19,2 | 19,4 | 13,0 | 17,3 | AUT | PENDIENTE | AUT abierta |
| 15 | AUT 16:54 | 33,3 | 36,6 | 6,3 | 8,5 | AUT | PENDIENTE | AUT abierta |
| 16 | AUT 16:56 | 24,9 | 24,9 | 7,7 | 12,7 | AUT | PENDIENTE | AUT abierta |
| 17 | AUT 16:58 | 17,5 | 17,5 | 17,9 | 0,0 | A_TREND | **PRIMARIA LOCAL** | salida A 0,40 |
| 18 | A_TREND 17:00 | 54,2 | 54,2 | 33,4 | 38,7 | C_TREND | **INTEGRADA** | A inferencia fuerte; 1 = A del padre |
| 19 | C_TREND 17:07 | 36,7 | 36,7 | 8,2 | 10,7 | AUT | **INTEGRADA** | C explícita; 1 = A del padre |
| 20 | AUT 17:09 | 44,6 | 49,7 | 51,0 | 2,0 | A_TREND | PENDIENTE | AUT abierta |
| 21 | A_TREND 17:11 | 20,5 | 22,4 | 9,9 | 13,5 | AUT | **SECUNDARIA** | retest: 29635,8 < 29636,1 |
| 22 | AUT 17:13 | 25,5 | 25,5 | 26,0 | 3,9 | A_TREND | **PRIMARIA LOCAL** | salida A 0,50 |
| 23 | A_TREND 17:15 | 24,7 | 24,7 | 8,5 | 13,6 | AUT | **INTEGRADA** | A inferencia fuerte; 1 = A del padre |
| 24 | AUT 17:18 | 28,2 | 28,2 | 27,6 | 37,9 | AUT | PENDIENTE | AUT abierta |
| 25 | AUT 17:21 | 44,7 | 44,7 | 46,2 | 0,0 | A_TREND | PENDIENTE | AUT abierta |
| 26 | A_TREND 17:25 | 23,4 | 28,2 | 12,3 | 17,1 | AUT | **PRIMARIA LOCAL** | salida A 1,50; 1 puede ser extensión de A |
| 27 | AUT 17:27 | 23,7 | 23,7 | 21,7 | 3,7 | ABIERTA | **PRIMARIA LOCAL ABIERTA** | feed termina |

**“PRIMARIA LOCAL” no significa aprobada.** Significa que la dirección del 1
coincide con la transición; su origen sigue siendo el extremo de la vela
siguiente, no el extremo de la transición (ver §6).

### 5.1 Recuento

```text
PRIMARIAS LOCALES (dirección válida) ....... 5   13, 17, 22, 26, 27
SECUNDARIA (dirección válida, retest) ...... 1   21
INTEGRADAS EN EL MÓDULO PADRE .............. 4   12, 18, 19, 23
PENDIENTES DE DECISIÓN EXPERTA ............. 6   14, 15, 16, 20, 24, 25
```

**Corrección al acta de Fase A:** el acta dice `AUT 8`; son **9** (13, 14, 15,
16, 19, 21, 23, 24, 26). La tabla de 16 filas y el CSV coinciden en 9; el
recuento del acta omitió una. También la fila de la gen 23 del acta dice módulo
23,0 / extremo 29679,1 y AUT 17:18:07.395; el CSV dice módulo **24,7** /
extremo **29680,8** y AUT **17:18:09.401**. El evento de 17:18:07.395 es un
`TT_EXTENDED`, no el AUT. Se corrige en §10.

---

## 6. EL SEGUNDO ERROR: EL ORIGEN DE 1

La dirección es sólo la mitad. Aunque el 1 tenga la dirección correcta, su
**origen** no es el extremo de la transición: es el extremo de la vela
siguiente. En las 5 candidatas principales:

| Gen | Transición | Precio/extremo de la transición | Origen del 1 del lector | Diferencia |
|---:|---|---:|---:|---:|
| 13 | C_TREND 16:50:32 | 29666,1 | 29675,8 | +9,7 |
| 17 | AUT 16:58:04 | 29630,1 | 29623,6 | −6,5 |
| 22 | AUT 17:13:17 | 29641,3 | 29653,8 | +12,5 |
| 26 | A_TREND 17:25:41 | 29632,1 | 29640,1 | +8,0 |
| 27 | AUT 17:27:51 | 29607,1 | 29618,1 | +11,0 |

En los cinco casos el 1 del lector empieza en un extremo de la vela siguiente,
no en el extremo que produjo la transición. El 1 contiene un tramo de la
extensión del padre o un retroceso previo. **Ninguna de las 16 generaciones
nace en el extremo de su transición.**

Esto tiene una consecuencia fuerte: el lector no está leyendo el nuevo 1 que la
transición confirma; está leyendo el **primer movimiento local posterior**. La
cadena de 16 es una cadena de 1 locales, no la escalera primaria de nuevos 1.

La diferencia entre ambas capas es la materia de Q_LOCAL_VS_PRIMARY.

---

## 7. PROPIEDAD DE EXTREMOS — EL CASO 17:22

### 7.1 Datos físicos

```text
17:22  O 29638,1   H 29678,3 (17:22:40, seq 18304)
                   L 29633,6 (17:22:01, seq 18125)
                   C 29664,1

17:23  O 29664,3   H 29664,4 (17:23:00, seq 18394)
                   L 29647,9 (17:23:33, seq 18551)
                   C 29656,8
```

### 7.2 Lectura del lector

```text
1 alcista  29633,6 → 29678,3 = 44,7
2 alcista  29664,3 → 29664,4 = 0,1   (falla al cierre)
módulo     29633,6 → 29678,3 = 44,7
```

### 7.3 Por qué 44,7 y no 30,8

- El origen del módulo, 29633,6, es el mínimo de la vela 17:22 (seq 18125). Es
  el origen de 1: desde ahí sube hasta 29678,3.
- El extremo del módulo, 29678,3, es el máximo de la vela 17:22 (seq 18304). Es
  el extremo de 1.
- El extremo de 2, 29664,4, es el máximo de la vela 17:23 (seq 18394). Está
  **13,9 puntos por debajo** del extremo de 1 y **dentro** de su rango.
- La medida 30,8 = 29664,4 − 29633,6 es la distancia al extremo de un 2 que
  falló con 0,1 puntos. No es la medida del módulo: es un sub-extremo interno.
- El módulo por descarte se mide con el extremo estructural más lejano que
  pertenece al módulo. Ese extremo es 29678,3, de 1. Por tanto **44,7**.

### 7.4 Otros casos de propiedad

| Gen | Extremo del módulo | Propietario | Evidencia |
|---:|---:|---|---|
| 12 | 29699,9 | 1 | 1 = 33,5; 2 = 0,0 |
| 13 | 29611,2 | 1 | 1 = 64,6; 2 = 0,0 |
| 14 | 29642,3 | módulo (extensión posterior) | 0,2 más allá de 1; 2 = 0,0; A se reinicia |
| 15 | 29643,8 | 2 (apertura) | la apertura de 2 extiende 3,3 más que 1; 2 = 0,0 |
| 16 | 29625,1 | 1 | 1 = 24,9; 2 = 0,0 |
| 17 | 29641,1 | 1 | 1 = 17,5; 2 = 0,0 |
| 18 | 29671,8 | 1 | 1 = 54,2; 2 = 0,0 |
| 19 | 29653,6 | 1 | 1 = 36,7; 2 = 0,0 |
| 20 | 29585,1 | módulo (extensión posterior) | 5,1 más allá de 1; 2 = 0,0; A se reinicia |
| 21 | 29637,7 | 2 (apertura) | la apertura de 2 extiende 1,9 más que 1; 2 = 0,0 |
| 22 | 29679,3 | 1 | 1 = 25,5; 2 = 0,0 |
| 23 | 29680,8 | 1 | 1 = 24,7; 2 = 11,2, dentro de 1 |
| 24 | 29641,6 | 1 | 1 = 28,2; 2 = 0,0 |
| 25 | 29678,3 | 1 | 1 = 44,7; 2 = 0,1 |
| 26 | 29611,9 | módulo (extensión posterior) | 4,8 más allá de 1; 2 = 0,0; A se reinicia |
| 27 | 29594,4 | 1 | 1 = 23,7; 2 = 0,0 |

La tabla completa, con origen y propietario de cada extremo, está en
`PHASE_A_EXTREME_OWNERSHIP.csv`.

---

## 8. QUÉ DESAPARECE Y QUÉ PERMANECE

### 8.1 Integración definitiva (4)

Las 4 inversiones con regla explícita o inferencia fuerte se integran en el
módulo padre; su 1 es la A del nuevo 1 del padre:

| Gen | Padre | 1 del lector | Función real | 1 del padre |
|---:|---|---|---|---|
| 12 | C_TREND 16:48 bajista | 33,5 alcista | A del 1 bajista 14,4 | 14,4 |
| 18 | A_TREND 17:00 bajista | 54,2 alcista | A del 1 bajista 5,6 | 5,6 |
| 19 | C_TREND 17:07 bajista | 36,7 alcista | A del 1 bajista 61,5 | 61,5 |
| 23 | A_TREND 17:15 bajista | 24,7 alcista | A del 1 bajista 26,0 | 26,0 |

### 8.2 Integración condicional (6)

Las 6 AUT se integran si 4.5 exige que el nuevo 1 sea la extensión de B:

```text
14, 15, 16, 20, 24, 25
→ 1 del lector = A de la extensión AUT
→ el módulo padre es la extensión de B
```

Si 4.5 no exige dirección, estas 6 pueden ser ciclos locales válidos. No se
deciden aquí.

### 8.3 Lo que permanece

```text
5 primarias locales:  13, 17, 22, 26, 27
1 secundaria:         21
4 integradas:         12, 18, 19, 23
6 pendientes:         14, 15, 16, 20, 24, 25
```

Ninguna de las 5 primarias está aprobada: su dirección es válida, su origen no
nace en la transición. Son candidatas para la Fase B, no goldens.

### 8.4 Tiempo no asignado

Entre cada transición y el `ONE_CANDIDATE` de la generación siguiente queda un
tramo de vela que no pertenece a ninguna 1 generacional:

```text
16:50:32.234 → 16:51:00.099   27,865 s
16:52:17.291 → 16:53:00.189   42,898 s
16:54:27.442 → 16:55:00.130   32,688 s
16:56:05.283 → 16:57:00.027   54,744 s
16:58:04.242 → 16:59:00.016   55,774 s
17:00:08.407 → 17:01:00.132   51,725 s
17:07:02.847 → 17:08:00.199   57,352 s
17:09:23.432 → 17:10:00.149   36,717 s
17:11:49.457 → 17:12:00.085   10,628 s
17:13:17.706 → 17:14:00.011   42,305 s
17:15:37.388 → 17:16:00.046   22,658 s
17:18:09.401 → 17:19:00.146   50,745 s
17:21:21.925 → 17:22:00.060   38,135 s
17:25:41.128 → 17:26:00.186   19,058 s
17:27:51.920 → 17:28:00.143    8,223 s
────────────────────────────────────────
TOTAL                         551,515 s = 9,19 min = 22,4 % del bloque
```

El lector procesa esos ticks, pero no los asigna a ninguna 1: quedan en
`WAIT_ONE`/`CLOSED`. Para un lector tick a tick, el 22,4 % del tiempo sin
función activa es un hueco de trazabilidad, no un detalle.

---

## 9. COMPARACIÓN CON LOS TRES TRAMOS MACRO

Los tres tramos no se usaron para clasificar. Se comparan después:

| Tramo | Recorrido | Generaciones primarias | Generaciones integradas | Generaciones pendientes |
|---|---|---:|---:|---:|
| 16:49–17:10 | −109,7 | 13 (64,6 bajista), 17 (17,5 alcista) | 12, 18, 19 | 14, 15, 16, 20 |
| 17:10–17:18 | +95,7 | 21 (20,5 alcista), 22 (25,5 alcista) | 23 | — |
| 17:18–17:29 | −91,5 | 26 (23,4 bajista), 27 (23,7 bajista) | — | 24, 25 |

La comparación no valida las 16: los impulsos macro están contenidos en las
primarias, pero las integradas y pendientes también son movimientos reales del
mismo tramo. La lectura macro sigue siendo una reconstrucción humana, no una
salida del instrumento.

---

## 10. ERRATA DEL ACTA DE FASE A

| Dato del acta | Valor correcto | Fuente |
|---|---|---|
| `AUT 8` | **9** (13, 14, 15, 16, 19, 21, 23, 24, 26) | `BLIND_TREE_GENERATIONS_1649_1729.csv` |
| Gen 23 módulo 23,0 / 29679,1 | **24,7 / 29680,8** | CSV, columna `module_size` / `module_extreme` |
| Gen 23 AUT 17:18:07.395 | **17:18:09.401** | CSV `aut_kt`; 17:18:07.395 es `TT_EXTENDED` |
| “la dirección y la medida de 1 no coinciden” (D003) | Correcto, pero el acta no lo clasifica como violación de v2.17 | Este documento, §3–4 |
| “16 generaciones” | Correcto como cadena local; no como escalera primaria | Este documento, §6 |

No se reescribe el acta; se deja constancia de la errata y se corrigen los
derivados en este documento. El CSV es la fuente de verdad de la tabla.

---

## 11. PREGUNTAS EXPERTAS (3)

### Q_AUT_DIRECTION — ¿el nuevo 1 del AUT es la extensión de B o la vela siguiente?

**MOVIMIENTO**

```text
Estábamos en el AUT bajista de 16:52:17 (gen 13, B = 17,7, precio 29607,1).
La extensión bajista siguió hasta 29602,8 a las 16:52:32.
Después la vela 16:53 abrió en 29633,6, bajó a 29622,9 y subió a 29642,1.
El lector llamó 1 a ese tramo alcista de 19,2.
```

**DUDA**

¿El nuevo 1 que confirma el AUT es la extensión bajista 29607,1 → 29602,8 (y
el tramo 29622,9 → 29642,1 es su A), o es la vela siguiente en la dirección que
resulte (y el tramo alcista es el nuevo 1)?

**CONSECUENCIA A — el nuevo 1 es la extensión de B**

```text
14, 15, 16, 20, 24, 25 se integran como A de la extensión AUT.
Quedan 5 primarias locales + 1 secundaria.
La cadena de 16 pasa a 6 ciclos, no a 16.
```

**CONSECUENCIA B — el nuevo 1 es la vela siguiente**

```text
14, 15, 16, 20, 24, 25 son ciclos locales válidos.
Quedan 12 ciclos: 5 primarias + 6 AUT + 1 secundaria.
La dirección del AUT no se hereda; cada vela decide.
```

**NODOS DESBLOQUEADOS:** dirección del nuevo 1, origen del 1, medida del módulo,
TT, dominancia, lectura local vs primaria.

---

### Q_C_GRANDE — ¿C tiene estado Grande antes de convertirse en tendencia?

**MOVIMIENTO**

```text
Estábamos en B Grande de 16:50:07 (gen 12, A = 16,2).
El precio bajó de 29700,8 a 29666,1: C = 34,7, más del 100 % de A.
Después cruzó la base 29666,4 y se convirtió en C usada como tendencia.
El lector nunca emitió C_GRANDE: sólo C candidata, CUT y C_TREND.
```

**DUDA**

¿C se confirma como **C Grande** al alcanzar el 100 % de A, y después se
registra la transición a C usada como tendencia, o C sólo existe como candidata
hasta cruzar la base del módulo?

**CONSECUENCIA A — C Grande es un estado**

```text
C se confirma al 100 % de A; CUT y C_TREND son transiciones posteriores.
Cambia el estado de C en 12 y 18; se abre la puerta a C Grande como función.
```

**CONSECUENCIA B — C sólo es candidata**

```text
C no tiene estado Grande; sólo C candidata y C_TREND.
El estado actual del lector es correcto y el hueco es ontológico del árbol.
```

**NODOS DESBLOQUEADOS:** C, CUT, C_TREND, TT, ontología de C, estados de la
generación.

---

### Q_A_MARGIN — ¿A usada como tendencia necesita autonomía estructural?

**MOVIMIENTO**

```text
Estábamos en el 1 alcista de 16:59 (gen 17, módulo 17,5).
A bajó a 29623,2: A = 17,9, sólo 0,4 puntos por debajo de la base 29623,6.
Después el precio siguió bajando hasta 29617,6 antes de girar.
El lector disparó A_USED_AS_TREND en 29623,2 y abrió la gen 18 en 17:01.
```

**DUDA**

¿A se convierte en A usada como tendencia en el **primer tick** que supera la
base, o necesita una autonomía estructural que excluya una extensión marginal
de 0,4–0,5 puntos?

**CONSECUENCIA A — primer tick**

```text
La transición se dispara en 29623,2; el nuevo 1 nace antes del extremo real
29617,6. Se mantienen las integraciones 18 y 23 y la medida actual del módulo.
```

**CONSECUENCIA B — autonomía estructural**

```text
A sigue siendo A hasta 29617,6; el nuevo 1 nace allí. Cambian el origen y la
medida de 18 y 23; la frontera de 0,4–0,5 deja de ser transición.
```

**NODOS DESBLOQUEADOS:** A, A_TREND, origen del nuevo 1, módulo, B/AUT
posteriores, umbral de autonomía.

---

## 12. RECOMENDACIÓN

```text
NEEDS_EXPERT_DECISION
```

No se recomienda `READY_TO_CONTINUE_PHASE_B` todavía:

1. **Q_AUT_DIRECTION** decide 6 de las 16 generaciones y la diferencia entre
   lectura local y lectura primaria.
2. **Q_C_GRANDE** decide si falta un estado ontológico de C; afecta a 12 y 18.
3. **Q_A_MARGIN** decide dos transiciones A_TREND (18 y 23) y la medida del
   módulo en 17:00 y 17:15.

Además, hay dos errores de instrumento que no requieren decisión experta y
deben corregirse antes de cualquier relectura:

- **E-DIR:** el 1 debe orientarse por la transición, no por `close − open`.
  Las 2 inversiones C_TREND son violaciones explícitas de v2.17; las 2 A_TREND
  son inferencia fuerte de v2.18.
- **E-ORIG:** el 1 debe nacer en el extremo de la transición, no en el extremo
  de la vela siguiente. Afecta a las 16 y deja 22,4 % del tiempo sin 1.

Mientras esas dos correcciones no se apliquen, la cadena de 16 no puede usarse
como evidencia de la escalera TM ni como base para congelar el árbol.

**Prioridad de las preguntas:** Q_AUT_DIRECTION → Q_C_GRANDE → Q_A_MARGIN.
La primera es la que cambia el número de ciclos; las otras dos cambian estados
y fronteras.

---

## 13. INTEGRIDAD

| Comprobación | Resultado |
|---|---|
| Árbol modificado | no |
| R3 / R5 modificados | no |
| Lecturas v005 modificadas | no |
| Tickfeed modificado | no |
| Goldens modificados | no |
| Lector re-ejecutado en esta auditoría | no |
| Información futura | no usada |
| Hardcoding en el motor | no: la única referencia externa es la transición heredada de 16:48, documentada como estado inicial; el script de auditoría la contiene como evidencia, no como fixture del motor |
| Determinismo de la salida auditada | `b219049b…` idéntico en doble ejecución (según `verify_phase_a.json`) |
| Prefijos | 41/41 (según `verify_phase_a.json`) |
| Ticks | 11.414, sin huecos |

**Archivos de esta auditoría:**

- `PHASE_A_GENERATION_CLASSIFICATION.csv`
- `PHASE_A_EXTREME_OWNERSHIP.csv`
- `PHASE_A_EXPERIMENTAL_POLICIES.md`
- `PHASE_A_PRIMARY_SECONDARY_MAP.md`
- `PHASE_A_GENERATION_AUDIT.json`
- `audit_generations.py` (script de auditoría, no motor)
- `verify_generation_audit.py` y `PHASE_A_AUDIT_VERIFICATION.json` (verificación con aserciones)

---

## 14. RESPUESTA A LAS PREGUNTAS DEL MANDATO

**¿Cuántas generaciones principales permanecen?**
5 candidatas locales con dirección válida: 13, 17, 22, 26, 27. Ninguna está
aprobada; las cinco fallan el origen en la transición.

**¿Cuántas secundarias permanecen?**
1: la 21, dirección válida pero retest por debajo del extremo de A.

**¿Cuántas fueron fragmentación artificial?**
4 confirmadas (12, 18, 19, 23) por inversión de dirección; 6 condicionales
(14, 15, 16, 20, 24, 25) si el AUT exige continuidad. En total, 10 ciclos
artificiales posibles, 4 ya resueltos.

**¿Qué preguntas expertas siguen abiertas?**
Q_AUT_DIRECTION, Q_C_GRANDE, Q_A_MARGIN.

**¿Recomendación?**
`NEEDS_EXPERT_DECISION`, no `READY_TO_CONTINUE_PHASE_B`.
