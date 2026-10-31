# TM — ÁRBOL MAESTRO CANÓNICO v1

- **Estado:** BORRADOR PREVIO. No es versión final ni base única.
- **Base de trabajo actual:** `TM_ARBOL_MAESTRO_CANONICO_v0_5_MEGA_BORRADOR.md`.
- **Fecha:** 2026-10-19.
- **Sustituye a:** `TM_ARBOL_CANONICO_COMPLETO_v1.md` solo después de la ratificación de Javier.
- **Autoridad:** Javier. Las conclusiones de OpenBot no son normativas.
- **Regla:** `PENDIENTE_JAVIER` solo puede existir durante la construcción. La versión final no puede contener ninguna.

---

## 0. CONTROL DE ALCANCE

Este documento es la especificación formal única del árbol. No es una explicación narrativa. Cada transición debe poder citarse por estado, evento, precondición y referencia matemática.

No se implementa código, EA, JSON ni tests en esta fase. No se modifica código, golden ni tests.

---

## 1. CRITERIO DE TERMINADO

El árbol no estará terminado hasta cumplir:

1. Todo movimiento TM está clasificado.
2. Todo tick pertenece a un movimiento vigente.
3. Toda función tiene precondiciones obligatorias.
4. Toda función tiene inicio, desarrollo, confirmación y final.
5. Toda función contempla continuidad y cambio de dirección.
6. Todo nivel exacto contempla `<`, `=` y `>`.
7. Todo salto que atraviese varios niveles en un tick está resuelto.
8. Todo gap tiene una rama definida.
9. Toda apertura de vela tiene una rama definida.
10. Toda combinación de una, dos o tres lecturas está resuelta.
11. Toda reclasificación conserva el historial.
12. Ninguna función utiliza referencias de otra lectura.
13. Ninguna rama termina en “ruido”, “sin clasificar” o “pérdida de coherencia”.
14. No queda ningún `PENDIENTE_JAVIER`.
15. Todos los casos de prueba de Javier producen la clasificación correcta.

---

## 2. DECISIONES YA RATIFICADAS

| ID | Decisión | Efecto en el árbol |
|---|---|---|
| R-01 | B candidata que gira antes del 100 %: la A original continúa y absorbe la B candidata. | `B_CANDIDATA` + giro antes de 100 % → `A_ACTIVA`; no nace C; no se crea módulo. |
| R-02 | Gap a favor de 1: produce A, B y AUT implícitos; puede abrir TT si hay módulo. | `1_ACTIVA` + `GAP_FAVOR` → `AUT` implícito; TT solo después de AUT; no se salta a TT sin AUT. |

> R-02 no elimina la exigencia de AUT: lo implícito es el AUT, no el TT.

---

## 3. DECISIONES ABIERTAS DEL NÚCLEO

### D-01 — Universo y CUT

¿Se confirma este universo?

- Movimientos o funciones: `1`, `2`, `3`, `A`, `B`, `C`, `AUT`.
- Patrones: `TT`, `FT`.
- Estructura: `módulo`.
- Evento de confirmación: `CUT`.

Pregunta exacta: ¿`CUT` es un evento producido por `C` al alcanzar el final de A, o es un movimiento/función propio?

**Estado:** `PENDIENTE_JAVIER`.

### D-02 — Definición universal de 1

Falta la regla matemática de confirmación de `1` para:

- `1` inicial de una lectura;
- `1` producido por TT confirmado;
- `1` producido por reclasificación;
- `1` pequeño simultáneo con AUT;
- `1` formado por varias velas.

Pregunta exacta: ¿Todos usan la misma definición de rango y extremos o existen varios tipos de origen?

**Estado:** `PENDIENTE_JAVIER`.

### D-03 — Movimiento menor que no abre otra función

Existe una función vigente y aparece un movimiento contrario que no alcanza la referencia necesaria para crear la siguiente función.

Opciones:

- **A)** Se integra en la función vigente y no nace otro movimiento TM.
- **B)** Siempre abre A, B u otra función provisional.
- **C)** Depende del estado de origen.

**Estado:** `PENDIENTE_JAVIER`.

### D-04 — Definición completa de 2

Propuesta provisional:

1. Existe `1` confirmado.
2. Se comprueba primero el gap.
3. Si hay gap, no existe `2`.
4. Si no hay gap, se comprueba la salida en plano.
5. Si aparece cola observable superior a `0,25` antes de alcanzar la medida exigida, no existe `2`.
6. Si alcanza primero la medida exigida, `2` queda confirmado.
7. Un movimiento posterior no borra el `2` confirmado.

Falta precisar:

- ¿La medida de `2` es al menos el rango completo de `1`?
- ¿Qué extremos definen esa medida?
- ¿La medida usa desplazamiento direccional o `High-Low`?
- ¿Cambia según el tipo de `1`?

**Estado:** `PENDIENTE_JAVIER`.

### D-05 — Definición completa de 3

Secuencia propuesta:

1. Existe `2` confirmado.
2. Retroceso entre el `0 %` y el `50 %` del rango de `2`.
3. Superación del extremo de `2`:
   - alcista: `High(3) > High(2)`;
   - bajista: `Low(3) < Low(2)`.
4. Si retrocede más del `50 %` o no supera el extremo de `2`, `3` no existe.
5. `1 + 2` quedan como módulo y el contrario es `A Grande`.

Falta confirmar:

- ¿Puede ocurrir todo dentro de la misma vela?
- ¿Puede estar formado por varias velas?
- ¿Qué sucede si antes aparece el movimiento contrario?
- ¿El retroceso se mide sobre el rango de `2` o sobre el desplazamiento direccional?

**Estado:** `PENDIENTE_JAVIER`.

### D-06 — Regla de FT (secundaria)

Falta la condición exacta de FT después de TT: referencia, desplazamiento mínimo y pérdida de velocidad.

**Estado:** `PENDIENTE_JAVIER`.

---

## 4. UNIVERSO PROPUESTO

> Pendiente de D-01. Se usa como estructura de trabajo, no como decisión final.

| Categoría | Elementos |
|---|---|
| Movimientos o funciones | `1`, `2`, `3`, `A`, `B`, `C`, `AUT` |
| Patrones | `TT`, `FT` |
| Estructura | `módulo` |
| Evento de nivel | `CUT` |
| Tipos de `1` | inicial, por TT, por reclasificación, pequeño simultáneo con AUT, multi-vela |

`nuevo 1` no es una función distinta: es un `1` con origen `TT`.

`CUT` no se trata como movimiento: se trata como evento de `C` si D-01 se confirma.

---

## 5. UNIDAD DE PROCESAMIENTO

La unidad no es la vela. Es:

```
movimiento TM dentro de una lectura
```

Una vela puede contener varios movimientos y puede participar en varias lecturas. El motor procesa eventos de precio en orden temporal:

1. tick anterior;
2. tick actual;
3. dirección vigente;
4. extremo vigente;
5. cambio de dirección;
6. gap;
7. apertura de vela;
8. nivel estructural alcanzado;
9. referencia TM alcanzada o no alcanzada.

---

## 6. ARQUITECTURA POR NIVELES

### Nivel 1 — Segmentación objetiva

Reconstruir movimientos con ticks, no con OHLC ni color:

- dirección;
- extremo;
- cambio de dirección;
- gap;
- apertura de vela;
- nivel estructural.

### Nivel 2 — Función TM

Cada movimiento reconocido debe pertenecer a:

`1`, `2`, `3`, `A`, `B`, `C`, `AUT`.

### Nivel 3 — Patrones

Las funciones pueden activar:

`TT`, `FT`.

### Nivel 4 — Estructuras y eventos

El motor conserva:

- `módulo`;
- `AUT`;
- `CUT`, según D-01;
- reclasificaciones;
- lecturas concurrentes.

---

## 7. ESTADOS DEL ÁRBOL

| Estado | Significado | Terminal |
|---|---|---|
| `INICIO` | No hay lectura activa. | No |
| `1_ACTIVA` | `1` confirmado; incluye `nuevo 1` con origen TT. | No |
| `2_CANDIDATA` | Movimiento en dirección de `1`; `2` aún no confirmado. | No |
| `2_CONFIRMADA` | `2` confirmado. | No |
| `3_CANDIDATA` | Retroceso válido en curso; `3` aún no confirmado. | No |
| `3_CONFIRMADA` | `3` confirmado; secuencia modular regular. | No |
| `MODULO` | `1+2` o conjunto validado como referencia. | No |
| `A_ACTIVA` | A Grande activa. | No |
| `B_CANDIDATA` | B candidata por debajo del 100 %. | No |
| `B_CONFIRMADA` | B Grande confirmada entre 100 % y 127 % + 0,25. | No |
| `AUT` | AUT confirmado; TT pendiente si hay módulo. | No |
| `TT_CONFIRMADO` | TT confirmado; nace `nuevo 1`. | No |
| `FT_PENDIENTE` | TT confirmado; FT en evaluación. | No |
| `FT_CONFIRMADO` | FT confirmado. | Sí |
| `C_ACTIVA` | C Grande activa después de B confirmada. | No |
| `CUT_CONFIRMADO` | CUT confirmado como evento de C. | Sí |
| `LECTURA_CERRADA` | Lectura cerrada; historial conservado. | Sí |

Estados transitorios de error de entrada, no funciones TM:

- `RECHAZO_POR_DATO_INVALIDO`: tick fuera de orden, dato faltante o referencia imposible. No crea función.
- `RECLASIFICADA`: metaestado; conserva historial y vuelve al estado funcional que corresponda.

---

## 8. EVENTOS DEL MOTOR

| Evento | Definición |
|---|---|
| `EXTIENDE` | Nuevo extremo en la dirección vigente. |
| `RETROCESO_SIN_REF` | Cambio de dirección que no alcanza la referencia de la función siguiente. |
| `RETROCESO_CON_REF` | Cambio de dirección que alcanza la referencia de la función siguiente. |
| `ALCANZA_100` | B alcanza exactamente el 100 % de A. |
| `CRUCE_AUT` | B supera `127 % + 0,25`. |
| `TOCA_AUT` | B toca exactamente `127 % + 0,25` y no supera. |
| `ALCANZA_TT` | Precio alcanza el objetivo TT. |
| `FALLA_TT` | Precio toca el final de A sin alcanzar TT. |
| `GAP_FAVOR` | Gap en dirección de la función vigente o de `1`. |
| `GAP_CONTRA` | Gap en dirección contraria. |
| `APERTURA_PLANO` | Apertura dentro de `±0,25` del cierre anterior. |
| `SALTO_MULTINIVEL` | Un tick cruza dos o más niveles relevantes. |
| `NUEVO_EXTREMO_B` | B confirmada crea un nuevo extremo. |
| `CAMBIO_VELA` | Cambia la vela sin cambiar el movimiento. |
| `RECLASIFICACION` | Corrección posterior que cambia la función sin borrar historial. |
| `CIERRE` | Se cierra la lectura por TT, CUT, FT o invalidación. |

---

## 9. GRAMÁTICA CERRADA PROPUESTA

```
INICIO
└── 1
    ├── 2
    │   ├── 3
    │   │   └── fin de secuencia modular regular
    │   └── si 3 no existe:
    │       1 + 2 = MÓDULO
    │       └── A
    │           └── B
    │               ├── B confirmada
    │               │   └── C
    │               │       └── CUT
    │               └── AUT
    │                   └── TT
    │                       └── nuevo 1
    │                           └── FT
    └── si 2 no existe:
        └── A
            └── B
                ├── B confirmada
                │   └── C
                │       └── CUT
                └── AUT
                    └── TT
                        └── nuevo 1
                            └── FT
```

Reglas de la gramática:

- `C` solo existe después de `B` confirmada.
- Sin `B` confirmada no hay `C` ni `CUT` derivado de esa `C`.
- `TT` no existe sin `AUT` confirmado; el AUT puede ser explícito o implícito por gap ratificado.
- `FT` solo se evalúa después de `TT`.
- `3` no se puede confirmar sin `2` confirmado.
- Si `2` nunca existió, no se fabrica un módulo `1+2`.
- Si `2` existió y `3` falló, `1+2` es módulo y el contrario es `A`.
- Una vela puede contener varios de estos eventos; el orden es por tick.

---

## 10. MATRIZ TOTAL ESTADO × EVENTO

> Esta matriz es la parte que debe quedar sin celdas vacías. Las celdas `PENDIENTE_JAVIER` son las únicas abiertas y desaparecerán en la versión final. `SIN_CAMBIO` significa “el evento se integra en el movimiento vigente y no crea función”; no es una categoría de ruido.

### 10.1. `INICIO`

| Evento | Condición | Salida | Nota |
|---|---|---|---|
| Primer movimiento válido | D-02 | `1_ACTIVA` | Único nacimiento de lectura. |
| Evento no válido | No cumple D-02 | `SIN_CAMBIO` | No hay función TM todavía. |
| `CIERRE` | — | `LECTURA_CERRADA` | — |

### 10.2. `1_ACTIVA`

| Evento | Condición | Salida | Nota |
|---|---|---|---|
| `EXTIENDE` | Igual dirección | `1_ACTIVA` | Actualiza extremo. |
| `RETROCESO_SIN_REF` | No alcanza referencia de `2` | `1_ACTIVA` | Se integra en `1`. |
| `RETROCESO_CON_REF` | Cumple D-04 | `2_CANDIDATA` | `2` posible. |
| `GAP_FAVOR` | R-02 | `AUT` | A/B/AUT implícitos; TT solo con módulo. |
| `GAP_CONTRA` | — | `A_ACTIVA` | A Grande. |
| `APERTURA_PLANO` | — | `2_CANDIDATA` o `1_ACTIVA` | Según D-04. |
| `SALTO_MULTINIVEL` | Cruza `2` y `AUT` | `PENDIENTE_JAVIER` | Falta prioridad y secuencia exacta. |
| `CAMBIO_VELA` | — | `1_ACTIVA` | No cierra `1`. |
| `RECLASIFICACION` | Evidencia | `1_ACTIVA` | Conserva historial. |
| `CIERRE` | — | `LECTURA_CERRADA` | — |
| Cualquier otro | — | `SIN_CAMBIO` | Integrado. |

### 10.3. `2_CANDIDATA`

| Evento | Condición | Salida | Nota |
|---|---|---|---|
| `EXTIENDE` | Igual dirección y `< 100 %` | `2_CANDIDATA` | Continúa. |
| `ALCANZA_100` | Sin AUT | `2_CONFIRMADA` | Frontera exacta. |
| `CRUCE_AUT` | Supera `127 % + 0,25` | `AUT` | Aunque no existiera `B_CONFIRMADA` persistente. |
| `TOCA_AUT` | Toca y no supera | `2_CONFIRMADA` | Si ya alcanzó 100 %. |
| Giro antes del 100 % | R-01 | `A_ACTIVA` | `2` no existió; no hay módulo. |
| `GAP_FAVOR` / `GAP_CONTRA` | — | `PENDIENTE_JAVIER` | Falta rama de gap en `2`. |
| `SALTO_MULTINIVEL` | Cruza 100 % y AUT | `AUT` | Clasificación vigente AUT. |
| `CAMBIO_VELA` | — | `2_CANDIDATA` | No cierra. |
| `CIERRE` | — | `LECTURA_CERRADA` | — |
| Cualquier otro | — | `SIN_CAMBIO` | Integrado. |

### 10.4. `2_CONFIRMADA`

| Evento | Condición | Salida | Nota |
|---|---|---|---|
| `EXTIENDE` | Igual dirección | `2_CONFIRMADA` | `2` no se borra. |
| Inicio de retroceso | D-05 | `3_CANDIDATA` | Comienza evaluación de `3`. |
| Retroceso `> 50 %` | D-05 | `MODULO` + `A_ACTIVA` | `3` no existe. |
| No supera extremo de `2` | D-05 | `MODULO` + `A_ACTIVA` | `3` no existe. |
| `GAP_*` | — | `PENDIENTE_JAVIER` | Falta rama. |
| `SALTO_MULTINIVEL` | Cruza extremo de `2` | `PENDIENTE_JAVIER` | Falta secuencia. |
| `CAMBIO_VELA` | — | `2_CONFIRMADA` | No cierra. |
| `CIERRE` | — | `LECTURA_CERRADA` | — |
| Cualquier otro | — | `SIN_CAMBIO` | Integrado. |

### 10.5. `3_CANDIDATA`

| Evento | Condición | Salida | Nota |
|---|---|---|---|
| Nuevo extremo de `2` | D-05 | `3_CONFIRMADA` | `3` confirmado. |
| Retroceso `> 50 %` | D-05 | `MODULO` + `A_ACTIVA` | `3` no existe. |
| No nuevo extremo | D-05 | `MODULO` + `A_ACTIVA` | `3` no existe. |
| `GAP_*` | — | `PENDIENTE_JAVIER` | Falta rama. |
| `CAMBIO_VELA` | — | `3_CANDIDATA` | No cierra. |
| `CIERRE` | — | `LECTURA_CERRADA` | — |
| Cualquier otro | — | `SIN_CAMBIO` | Integrado. |

### 10.6. `3_CONFIRMADA`

| Evento | Condición | Salida | Nota |
|---|---|---|---|
| Fin de secuencia | — | `LECTURA_CERRADA` | No se inventa un movimiento posterior. |
| `CAMBIO_VELA` | — | `3_CONFIRMADA` | Sin efecto. |
| `CIERRE` | — | `LECTURA_CERRADA` | — |
| Cualquier otro | — | `SIN_CAMBIO` | Integrado. |

### 10.7. `MODULO`

| Evento | Condición | Salida | Nota |
|---|---|---|---|
| `RETROCESO_CON_REF` | Contrario al módulo | `A_ACTIVA` | A Grande. |
| `RETROCESO_SIN_REF` | No alcanza A | `MODULO` | Integrado. |
| `GAP_CONTRA` | — | `A_ACTIVA` | A Grande. |
| `GAP_FAVOR` | — | `PENDIENTE_JAVIER` | Falta rama. |
| `CAMBIO_VELA` | — | `MODULO` | Sin efecto. |
| `CIERRE` | — | `LECTURA_CERRADA` | — |
| Cualquier otro | — | `SIN_CAMBIO` | Integrado. |

### 10.8. `A_ACTIVA`

| Evento | Condición | Salida | Nota |
|---|---|---|---|
| `EXTIENDE` | Igual dirección | `A_ACTIVA` | A continúa. |
| `RETROCESO_CON_REF` | Contrario a A | `B_CANDIDATA` | B candidata. |
| `RETROCESO_SIN_REF` | No alcanza B | `A_ACTIVA` | Se integra en A. |
| `GAP_FAVOR` | — | `A_ACTIVA` | A continúa. |
| `GAP_CONTRA` | — | `PENDIENTE_JAVIER` | Falta rama B por gap. |
| `CAMBIO_VELA` | — | `A_ACTIVA` | A multi-vela. |
| `CIERRE` | — | `LECTURA_CERRADA` | — |
| Cualquier otro | — | `SIN_CAMBIO` | Integrado. |

### 10.9. `B_CANDIDATA`

| Evento | Condición | Salida | Nota |
|---|---|---|---|
| `EXTIENDE` | Igual dirección y `< 100 %` | `B_CANDIDATA` | Continúa. |
| `ALCANZA_100` | Sin AUT | `B_CONFIRMADA` | Frontera exacta. |
| `CRUCE_AUT` | Supera `127 % + 0,25` | `AUT` | Aunque venga de candidata. |
| `TOCA_AUT` | Toca y no supera | `B_CONFIRMADA` | Si ya alcanzó 100 %. |
| Giro antes del 100 % | R-01 | `A_ACTIVA` | A original absorbe B candidata. |
| `GAP_*` | — | `PENDIENTE_JAVIER` | Falta rama. |
| `SALTO_MULTINIVEL` | Cruza 100 % y AUT | `AUT` | Prioridad AUT. |
| `CAMBIO_VELA` | — | `B_CANDIDATA` | No cierra. |
| `CIERRE` | — | `LECTURA_CERRADA` | — |
| Cualquier otro | — | `SIN_CAMBIO` | Integrado. |

### 10.10. `B_CONFIRMADA`

| Evento | Condición | Salida | Nota |
|---|---|---|---|
| `EXTIENDE` | Igual dirección | `B_CONFIRMADA` | B continúa. |
| `RETROCESO_CON_REF` | Contrario a B | `C_ACTIVA` | Nace C. |
| `RETROCESO_SIN_REF` | No alcanza C | `B_CONFIRMADA` | Integrado. |
| `CRUCE_AUT` | Supera AUT | `AUT` | B y AUT no coexisten. |
| `TOCA_AUT` | Toca y no supera | `B_CONFIRMADA` | Sin AUT. |
| `NUEVO_EXTREMO_B` | — | `B_CONFIRMADA` | Si C activa, C se cancela. |
| `GAP_*` | — | `PENDIENTE_JAVIER` | Falta rama. |
| `CAMBIO_VELA` | — | `B_CONFIRMADA` | No cierra. |
| `CIERRE` | — | `LECTURA_CERRADA` | — |
| Cualquier otro | — | `SIN_CAMBIO` | Integrado. |

### 10.11. `AUT`

| Evento | Condición | Salida | Nota |
|---|---|---|---|
| `EXTIENDE` | Igual dirección | `AUT` | TT sigue pendiente. |
| `ALCANZA_TT` | Objetivo | `TT_CONFIRMADO` | Nace nuevo 1. |
| `FALLA_TT` | Toca fin de A sin TT | `MODULO` + `A_ACTIVA` | TT fallido. |
| `RETROCESO_SIN_REF` | No toca fin de A | `AUT` | Integrado. |
| `RETROCESO_CON_REF` | Toca fin de A | `FALLA_TT` | Se evalúa TT fallido. |
| `GAP_*` | — | `PENDIENTE_JAVIER` | Falta rama. |
| `SALTO_MULTINIVEL` | Cruza AUT y TT | `TT_CONFIRMADO` | Mismo tick. |
| `CAMBIO_VELA` | — | `AUT` | No cierra. |
| `CIERRE` | — | `LECTURA_CERRADA` | — |
| Cualquier otro | — | `SIN_CAMBIO` | Integrado. |

### 10.12. `TT_CONFIRMADO`

| Evento | Condición | Salida | Nota |
|---|---|---|---|
| Nacimiento de nuevo 1 | — | `1_ACTIVA` con origen TT | Misma definición de D-02. |
| `CAMBIO_VELA` | — | `TT_CONFIRMADO` | Sin efecto. |
| `CIERRE` | — | `LECTURA_CERRADA` | — |
| Cualquier otro | — | `SIN_CAMBIO` | Integrado. |

### 10.13. `FT_PENDIENTE`

| Evento | Condición | Salida | Nota |
|---|---|---|---|
| `RETROCESO_CON_REF` | Regla FT | `FT_CONFIRMADO` | D-06 pendiente. |
| `RETROCESO_SIN_REF` | No alcanza FT | `1_ACTIVA` | Nuevo 1 continúa. |
| `CAMBIO_VELA` | — | `FT_PENDIENTE` | Sin efecto. |
| `CIERRE` | — | `LECTURA_CERRADA` | — |
| Cualquier otro | — | `SIN_CAMBIO` | Integrado. |

### 10.14. `C_ACTIVA`

| Evento | Condición | Salida | Nota |
|---|---|---|---|
| `EXTIENDE` | Igual dirección | `C_ACTIVA` | C continúa. |
| CUT | C alcanza final de A | `CUT_CONFIRMADO` | Evento, no función. |
| `RETROCESO_SIN_REF` | No alcanza nueva referencia | `C_ACTIVA` | Integrado. |
| `RETROCESO_CON_REF` | Nueva referencia | `PENDIENTE_JAVIER` | Falta rama C sin CUT. |
| `NUEVO_EXTREMO_B` | B recupera extremo | `B_CONFIRMADA` | C se cancela. |
| `GAP_*` | — | `PENDIENTE_JAVIER` | Falta rama. |
| `CAMBIO_VELA` | — | `C_ACTIVA` | No cierra. |
| `CIERRE` | — | `LECTURA_CERRADA` | — |
| Cualquier otro | — | `SIN_CAMBIO` | Integrado. |

### 10.15. `CUT_CONFIRMADO` y `FT_CONFIRMADO`

| Estado | Evento | Salida | Nota |
|---|---|---|---|
| `CUT_CONFIRMADO` | `CIERRE` | `LECTURA_CERRADA` | Cierra rama C. |
| `CUT_CONFIRMADO` | Cualquier otro | `SIN_CAMBIO` | Historial conservado. |
| `FT_CONFIRMADO` | `CIERRE` | `LECTURA_CERRADA` | Cierra patrón FT. |
| `FT_CONFIRMADO` | Cualquier otro | `SIN_CAMBIO` | Historial conservado. |

### 10.16. `LECTURA_CERRADA`

| Evento | Salida | Nota |
|---|---|---|
| Cualquier evento | `SIN_CAMBIO` | No se reabre; el historial queda archivado. |
| Nueva lectura | `INICIO` | Solo si una regla independiente la autoriza. |

---

## 11. CONCURRENCIA

- `L1`, `L2` y `L3` no son funciones ni estados distintos.
- Son instancias independientes del mismo árbol.
- Cada lectura conserva: función vigente, función anterior, dirección, módulo, A, B, nivel AUT, objetivo TT, nivel C, evento CUT, referencia FT e historial.
- Ninguna función puede usar la referencia de otra lectura.
- La apertura de `L2` o `L3` exige una regla TM independiente. No se abre por parecido visual.
- El máximo operativo es 3 lecturas; nunca 4.
- La prioridad cuando dos o tres lecturas alcanzan un nivel en el mismo tick sigue `PENDIENTE_JAVIER`.

---

## 12. CORRECCIONES OBLIGATORIAS A LA V1

| ID | Error v1 | Corrección v2 |
|---|---|---|
| C-01 | `rango_2 >= rango_1` en narrativa y `rango_2 <= rango_1` en matriz. | Se elimina la contradicción. La medida de `2` queda en D-04; no se usa `rango_2 <= rango_1`. |
| C-02 | T-001 declara que vela 2 es `2`; el caso real dice que vela 2 es A/B/AUT. | T-001 se elimina. El caso real se convierte en prueba negativa de `2`: vela 1 = 1; vela 2 = A/B/AUT; vela 3 = TT y nuevo 1. |
| C-03 | Gap a favor salta a TT pendiente sin AUT. | Gap a favor produce A/B/AUT implícitos (R-02); TT solo después de AUT. |
| C-04 | Todo fallo de `2` produce módulo + A. | Si `2` existió y `3` falló: módulo + A. Si `2` nunca existió: A, sin módulo `1+2`. |
| C-05 | `B_CANDIDATA` no puede pasar a AUT sin `B_CONFIRMADA` persistente. | Un tick que cruza 100 % y AUT desde `B_CANDIDATA` produce `AUT` directo. |
| C-06 | `ruido` y `SIN_LECTURA` se usan como salida. | No hay estado “ruido”. El evento sin referencia se integra en el movimiento vigente (`SIN_CAMBIO`) o se rechaza por dato inválido. |
| C-07 | `CUT` se trata como estado funcional. | `CUT` es evento de `C` (pendiente D-01). |
| C-08 | L1/L2/L3 se modelan como árboles distintos. | Son instancias del mismo árbol. |

---

## 13. TESTS QUE CAMBIAN

No se ejecutan todavía.

| Test v1 | Problema | Acción |
|---|---|---|
| T-001 | Declara `2` donde el caso real tiene A/B/AUT. | Eliminar y sustituir por `T-001N` negativo de `2`. |
| T-005 | Usa `rango_2 > rango_1` como inválido. | Reescribir según D-04 y la medida exacta. |
| T-002 | Gap a favor sin AUT. | Reescribir: gap → A/B/AUT implícitos → TT solo después de AUT. |
| T-015 | Frontera de AUT. | Mantener, pero separar toque exacto y superación. |
| T-029/T-030 | Concurrencia sin regla de apertura. | Bloquear hasta definir la regla de L2/L3. |
| T-040 | Mezcla L4 con `1` sin regla. | Separar “no L4” de “confirmación de 1”. |

Tests nuevos obligatorios:

1. `T-001N`: vela 1 = `1`; vela 2 = `A`, `B`, `AUT`; vela 2 no es `2`.
2. `T-002N`: gap a favor; no hay TT sin AUT.
3. `T-003N`: `2` nunca existió; el contrario es `A`, no módulo `1+2`.
4. `T-004N`: `B_CANDIDATA` + salto de un tick por encima de AUT → `AUT`.
5. `T-005N`: movimiento contrario sin referencia → integrado, no “ruido”.
6. `T-006N`: `3` confirmado cierra la secuencia modular regular.

---

## 14. TRAZABILIDAD

| Fuente | Uso |
|---|---|
| `00_LEEME_PRIMERO_PRIORIDAD_DOCUMENTOS_TM.txt` | Orden y prioridad documental. |
| `Dossier_TM_v3_Lectura_Obligatoria.txt` | Reglas base de 1, 2, 3, A, B, C, TT. |
| `Dossier_TM_v4_Concurrencia_Reclasificacion.txt` | Concurrencia y reclasificación. |
| `DECISIONES_EXPERTO.md` | `DEC-015` y decisiones de Javier. |
| `REGLAS_CERRADAS.md` | Reglas cerradas y fronteras. |
| `REGLAS_PROVISIONALES.md` | Reglas aún no cerradas. |
| `CONTRADICCIONES.md` | Contradicciones pendientes. |
| `TM_ARBOL_CANONICO_COMPLETO_v1.md` | Inventario de casos; no es autoridad. |

---

## 15. PRÓXIMO PASO

Cerrar D-01 a D-05 con Javier. Después:

1. Corregir la matriz total.
2. Enumerar todos los estados y eventos.
3. Asignar salida a cada celda.
4. Añadir concurrencia y reclasificación.
5. Añadir gaps y saltos multinivel.
6. Crear tests positivos, negativos y de frontera.
7. Solo entonces derivar JSON, CSV, casos y motor.
