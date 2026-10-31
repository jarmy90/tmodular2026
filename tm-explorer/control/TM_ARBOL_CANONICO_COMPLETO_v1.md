# TM — ÁRBOL CANÓNICO COMPLETO v1

- **Documento:** `control/TM_ARBOL_CANONICO_COMPLETO_v1.md`
- **Versión:** 1.0
- **Fecha:** 2026-10-19
- **Autoridad experta:** Javier Armada López
- **Estado:** BORRADOR CANÓNICO PARA REVISIÓN DE JAVIER
- **Uso:** documento maestro de ramas, estados y transiciones. No es código, no es golden y no sustituye a las fuentes.
- **Regla de control:** si una rama no está cerrada por una fuente o por una decisión expresa de Javier, se escribe `PENDIENTE_JAVIER`. No se completa por intuición.

## 0. CONTROL DE FUENTES Y ALCANCE

### 0.1. Fuentes leídas

1. `00_LEEME_PRIMERO_PRIORIDAD_DOCUMENTOS_TM.txt`
2. `AGENTS.md`
3. `control/DECISIONES_EXPERTO.md`
4. `control/REGLAS_CERRADAS.md`
5. `Dossier_TM_v3_Lectura_Obligatoria.txt`
6. `Dossier_TM_v4_Concurrencia_Reclasificacion.txt`
7. `control/CONTRADICCIONES.md`
8. `control/REGLAS_PROVISIONALES.md`
9. `control/DICCIONARIO_TM.md`
10. `PROMPT_OPENBOT_TM_ARBOL_CANONICO.txt` (instrucción de esta fase)

No existe `control/CASOS_VALIDADOS.md` en la fecha de creación.

### 0.2. Precedencia aplicada

1. Corrección expresa de Javier.
2. `DECISIONES_EXPERTO.md`.
3. `REGLAS_CERRADAS.md`.
4. Dossier v3.
5. Adenda v4.
6. Resto de documentación, solo como apoyo.

Si dos fuentes discrepan y no hay corrección expresa, la rama queda `PENDIENTE_JAVIER` y se registra en `TM_DUDAS_PENDIENTES_JAVIER.md`.

### 0.3. Prohibiciones de esta fase

- No programar.
- No generar MQL5.
- No modificar golden.
- No modificar tests.
- No modificar documentos vigentes.
- No abrir una lectura nueva sin regla TM expresa.
- No etiquetar una función si falta su precondición.
- No usar análisis técnico externo.
- No tratar conversaciones de asistentes como normativa.

---

## 1. MAPA DE REGLAS CONFIRMADAS Y PENDIENTES

### 1.1. Reglas cerradas que gobiernan el árbol

| ID | Regla | Fuente | Nodo |
|---|---|---|---|
| BASE-1 | La TM estudia movimientos, no colores de velas. | `REGLAS_CERRADAS` BASE-1 | N-001, N-032 |
| BASE-2 | Un cambio de vela no termina automáticamente un movimiento. | BASE-2 | N-013, N-038 |
| BASE-3 | El orden intravela es obligatorio. | BASE-3 | N-001, N-038 |
| BASE-4 | Una vela puede contener varios movimientos. | BASE-4 | N-001, N-028 |
| BASE-5 | Un movimiento puede atravesar varias velas. | BASE-5 | N-013, N-038 |
| BASE-6 | Un cambio de dirección solo crea movimiento TM nuevo si alcanza referencia TM; si no, queda integrado. | BASE-6 | N-032 |
| A1 | `2` exige misma dirección, rango ≥ rango de 1, salida en plano y cola ≤ 0,25; confirmación por desplazamiento direccional. | A1 | N-005, N-006, N-007, N-008 |
| A2 | Módulo regular 1+2: rango de expansión = `High−Low` completo del conjunto. | A2 | N-012 |
| A3 | TT = final de A ± rango del módulo. | A3 | N-018, N-019 |
| A4 | Primero gap; con gap no se aplica la regla de 2. | A4 / H11 | N-002, N-003, N-004 |
| B1 | AUT = B Grande supera `127 % + 0,25` (1 tick). | B1 / H8 | N-017 |
| B2 | AUT no confirma por sí solo nuevo 1 ni TT; deja TT pendiente si hay módulo. | B2 | N-018 |
| B3 | Orden causal B Grande confirmada → AUT → TT; TT puede confirmarse en el mismo tick. | B3 | N-017, N-018, N-019, N-033 |
| B4 | AUT y CUT pueden coexistir en momentos distintos de la misma lectura. | B4 | N-024 |
| B5 | B Grande y AUT no coexisten como clasificación vigente del mismo recorrido. | B5 | N-017, N-037 |
| H1 | C Grande puede desembocar en CUT o en nuevo 1; la condición exacta de `C = nuevo 1` sigue pendiente. | H1 | N-025 |
| H2 | `C = nuevo 1` pertenece a la lectura modular; FT pertenece a la lectura de patrones. | H2 | N-025, N-026 |
| H3 | Ante C Grande se comprueban, en orden: CUT; C como nuevo 1; C como A Grande de una lectura mayor. | H3 | N-034 |
| H4 | A Grande puede ocupar dos velas; B puede comenzar dentro de la segunda. | H4 | N-013, N-038 |
| H5 | Doble medición Fibonacci independiente: retroceso de A solo confirma B; expansión del módulo solo confirma TT. | H5 | N-014, N-019 |
| H6 | Cada lectura concurrente puede tener su propio autocorte. | H6 | N-028, N-029 |
| H9 | AUT exige superar, no solo tocar, `127 % + 0,25`. | H9 | N-016, N-017 |
| H10 | Lecturas concurrentes se nombran lectura 1 / 2 / 3. | H10 | N-028, N-029 |
| H11 | Gap primero; con gap no hay salida en plano, ni posible 2, ni 2. | H11 | N-002, N-003, N-004 |
| H12 | B candidata antes del 100 %; el 100 % confirma B Grande. | H12 | N-014, N-015 |
| H13 | Desde B Grande: 100–127 % + 0,25 → B Grande; cambio de sentido → C Grande; superar → AUT; nuevo extremo de B cancela C. | H13 | N-015, N-016, N-017, N-022, N-023 |
| H14 | Plano si `|cierre vela anterior − apertura siguiente| ≤ 0,25`; si > 0,25 es gap. | H14 | N-002, N-005 |
| H15 | A Grande no se cierra en el primer extremo si la vela siguiente lo extiende; el fin es el extremo real. | H15 | N-013, N-038 |
| H16 | Concurrencia habitual: normalmente 2 lecturas, excepcionalmente 3; no se calculan ruido ni micromovimientos. | H16 / DEC-015 | N-028, N-029, N-032 |
| H17 | Módulo por descarte (vela anterior) es PROVISIONAL, no regla general. | H17 | N-012 |
| DEC-004 | Vocabulario de concurrencia: lectura 1 / 2 / 3. | DEC-004 | N-028, N-029 |
| DEC-015 | Concurrencia habitual y filtro metodológico de ruido/micromovimientos. | DEC-015 | N-032 |

### 1.2. Ramas pendientes que condicionan el árbol

| ID | Pendiente | Fuente | Nodo |
|---|---|---|---|
| P2 | Serie de precio definitiva (Bid/Ask/Last/medio). En la muestra se usa Bid, sin ratificación experta. | `REGLAS_PROVISIONALES` P2 | N-001, N-019 |
| P3 | Tick exacto de confirmación de A/B/C Grande más allá del umbral numérico. | P3 | N-013, N-014, N-022 |
| P4 | Criterios exactos de reclasificación como módulo o 1 conjunto. | P4 | N-027 |
| P5 | Prioridad y permanencia cuando dos o tres lecturas alcanzan nivel en el mismo tick. | P5 | N-030 |
| P6 | Regla matemática completa de FT. | P6 | N-026 |
| PR-e | Condición exacta de `C = nuevo 1` cuando C no alcanza CUT. | PR-e | N-025 |
| PR-g | Umbral numérico entre ruido y movimiento TM. | PR-g | N-032 |
| DUDA-009 | Regla general del módulo: ¿siempre 2 velas o una sola / vela anterior por descarte? | DUDA-009 | N-012 |
| DUDA-J01 | Regla expresa para abrir L2/L3. | Esta auditoría | N-028, N-029 |
| DUDA-J02 | Módulo general. | Esta auditoría | N-012 |
| DUDA-J03 | Prioridad mismo tick. | Esta auditoría | N-030 |
| DUDA-J04 | `C = nuevo 1`. | Esta auditoría | N-025 |
| DUDA-J05 | FT. | Esta auditoría | N-026 |

---

## 2. ARQUITECTURA A — CONTROLADOR DE CONCURRENCIA L1-L3

### 2.1. Slots

| Slot | Nombre funcional | Función |
|---|---|---|
| L1 | `lectura 1` | Lectura de referencia principal. |
| L2 | `lectura 2` | Segunda lectura coherente, solo con regla expresa. |
| L3 | `lectura 3` | Tercera lectura coherente, solo con regla expresa. |

`L1`, `L2` y `L3` son identificadores de slot; la capa funcional usa `lectura 1`, `lectura 2` y `lectura 3` (DEC-004 / H10).

### 2.2. Regla central

- No se abre L2 o L3 por observar varios movimientos dentro de una vela.
- Una lectura nueva solo se abre si existe una **regla TM expresa**.
- Cada función pertenece a una lectura concreta.
- No se mezclan referencias entre lecturas.
- La concurrencia es habitual: normalmente 2 lecturas; excepcionalmente 3; nunca 4.
- El ruido y los micromovimientos no se calculan, no se clasifican y no ocupan lectura.

### 2.3. Condiciones de apertura

| ID | Condición | Estado | Consecuencia |
|---|---|---|---|
| OPEN-L2-01 | AUT local que puede ser nuevo 1 y TT pequeño. | `PENDIENTE_JAVIER` | Si se confirma, abre L2; si no, el movimiento pertenece a L1. |
| OPEN-L2-02 | Reclasificación de velas anteriores como módulo o 1 conjunto. | `PENDIENTE_JAVIER` | Si se confirma, puede abrir o transformar L2. |
| OPEN-L2-03 | Segunda lectura ya contenida en una referencia mayor. | `PENDIENTE_JAVIER` | No se abre hasta que Javier fije la regla. |
| OPEN-L3-01 | Tercera lectura matemáticamente válida y coherente. | `PENDIENTE_JAVIER` | Solo puede existir si L1 y L2 siguen válidas y hay regla expresa. |

### 2.4. Prioridad y permanencia

- Una lectura permanece activa hasta una resolución matemática: TT confirmado, CUT confirmado, invalidación por final de A, reclasificación/integración o pérdida de coherencia.
- La prioridad cuando dos o tres lecturas alcanzan nivel en el mismo tick es `PENDIENTE_JAVIER` (P5 / DUDA-J03).
- No se resuelve por preferencia del agente, por color de vela ni por resultado posterior.
- Cada lectura conserva su propio módulo, A, B, AUT, TT, nuevo 1 y nivel de invalidación.

### 2.5. Cierre y archivo

| Evento | Efecto | Estado |
|---|---|---|
| TT confirmado | La lectura puede finalizar o continuar según su ciclo. | CERRADO |
| CUT confirmado | Cierre de la rama C/CUT de esa lectura. | CERRADO |
| Final de A tocado antes de TT | TT cancelado; recorrido anterior pasa a módulo; retorno = A Grande. | CERRADO |
| Reclasificación | Cambia la función, no se borra el historial. | PROVISIONAL |
| Pérdida de coherencia | Lectura invalidada; se conserva en eventos. | CERRADO |
| Límite L3 | No se abre L4. | CERRADO |

---

## 3. ARQUITECTURA B — MÁQUINA DE ESTADOS POR LECTURA

### 3.1. Dos ejes que no deben confundirse

**Fase TM (qué función representa el recorrido):**

`1_ACTIVA`, `2_CANDIDATA`, `2_CONFIRMADA`, `3_CANDIDATA`, `3_CONFIRMADA`, `MODULO`, `A_GRANDE`, `B_CANDIDATA`, `B_GRANDE`, `AUT`, `TT_PENDIENTE`, `TT_CONFIRMADO`, `NUEVO_1`, `C_GRANDE`, `CUT`, `FT`, `TT_FALLIDO`.

**Estado de ciclo de vida (qué le ocurre a la lectura):**

`CANDIDATA`, `ACTIVA`, `CONFIRMADA`, `PENDIENTE`, `RECLASIFICADA`, `INTEGRADA`, `INVALIDADA`, `FINALIZADA`.

### 3.2. Estados funcionales permitidos

| Estado | Significado | Entrada | Salida |
|---|---|---|---|
| `1_ACTIVA` | Movimiento inicial del módulo. | N-001 | N-005 / N-008 / N-012 |
| `2_CANDIDATA` | Movimiento en misma dirección que 1, aún sin confirmar 2. | N-006 | N-007 / N-008 |
| `2_CONFIRMADA` | 2 confirmado por desplazamiento direccional. | N-007 | N-009 / N-011 |
| `3_CANDIDATA` | Retroceso 0–50 % y intención de superar extremo de 2. | N-009 | N-010 / N-011 |
| `3_CONFIRMADA` | 3 confirmado. | N-010 | Ciclo modular |
| `MODULO` | 1+2 (o conjunto validado) como referencia. | N-008 / N-011 / N-020 | N-012 / N-013 |
| `A_GRANDE` | Movimiento contrario al módulo. | N-011 / N-020 | N-014 |
| `B_CANDIDATA` | Movimiento contrario a A por debajo del 100 %. | N-014 | N-015 |
| `B_GRANDE` | B confirmada en 100 %–127 % + 0,25. | N-015 | N-017 / N-022 / N-023 |
| `AUT` | B superó 127 % + 0,25; TT pendiente. | N-017 | N-018 |
| `TT_PENDIENTE` | AUT activo; objetivo TT no alcanzado. | N-018 | N-019 / N-020 |
| `TT_CONFIRMADO` | Objetivo TT alcanzado. | N-019 | N-021 / N-026 |
| `NUEVO_1` | Movimiento que completa TT; nueva referencia. | N-019 / N-025 | Ciclo posterior |
| `C_GRANDE` | Movimiento contrario a B confirmada. | N-022 | N-023 / N-024 / N-025 |
| `CUT` | C Grande supera final de A. | N-024 | Cierre de rama |
| `FT` | Fin de tendencia tras TT. | N-026 | Cierre de patrón |
| `TT_FALLIDO` | TT no alcanzado y final de A tocado. | N-020 | N-011 / N-012 |

### 3.3. Transiciones de ciclo de vida

| Desde | Evento | Hasta |
|---|---|---|
| `CANDIDATA` | Evidencia insuficiente | `PENDIENTE` |
| `CANDIDATA` | Precondiciones cumplidas | `ACTIVA` |
| `ACTIVA` | Confirmación matemática | `CONFIRMADA` |
| `ACTIVA` | Corrección de referencia | `RECLASIFICADA` |
| `ACTIVA` | Absorción por lectura mayor | `INTEGRADA` |
| `ACTIVA` | Nivel de invalidación | `INVALIDADA` |
| `CONFIRMADA` | TT/CUT/FT o fin de ciclo | `FINALIZADA` |
| `RECLASIFICADA` | Nueva función estable | `ACTIVA` o `FINALIZADA` |
| `INVALIDADA` | Conservación histórica | `FINALIZADA` |

### 3.4. Invariantes

1. No hay 2 sin 1.
2. No hay 3 sin 2.
3. No hay módulo regular sin fallo de 2 o de 3, salvo módulo por descarte `PENDIENTE_JAVIER`.
4. No hay A Grande sin módulo.
5. No hay B Grande sin A Grande.
6. No hay C Grande sin B Grande confirmada en la misma lectura.
7. No hay CUT sin C Grande válida y sin superar el final de A.
8. No hay TT sin AUT y sin módulo.
9. No hay TT confirmado sin alcanzar el 100 % del objetivo.
10. No hay FT sin TT confirmado.
11. B Grande y AUT no coexisten en el mismo recorrido.
12. Cada lectura conserva sus propios niveles; no se mezclan.
13. Reclasificar no borra el evento anterior.

---

## 4. ARQUITECTURA C — ÁRBOL COMPLETO DE TRANSICIONES

> Formato obligatorio. `ESTADO_APROBACIÓN` usa `CERRADO`, `PROVISIONAL`, `PENDIENTE_JAVIER` o `NO_APLICA`.
> Los tests se despliegan en `TM_TESTS_REQUERIDOS_v1.md`.

### N-001 — Inicio de lectura y 1

- **ID:** N-001
- **ESTADO_ORIGEN:** `SIN_LECTURA`
- **EVENTO:** Primer movimiento direccional con referencia TM válida.
- **PRECONDICIONES:** Orden temporal reconstruido; no es ruido; no hay lectura previa en el slot.
- **FÓRMULA:** Dirección de 1 = dirección del movimiento; no exige rango mínimo teórico.
- **SI_TRUE:** Abre L1 como `1_ACTIVA/ACTIVA`.
- **SI_FALSE:** Permanece `SIN_LECTURA`.
- **ESTADO_DESTINO:** `1_ACTIVA/ACTIVA`
- **LECTURA_AFECTADA:** L1
- **¿ABRE_NUEVA_LECTURA?:** SÍ, L1.
- **PROHIBICIONES:** No clasificar 2, 3, A, B o C antes de 1; no usar color de vela.
- **DATOS_A_GUARDAR:** inicio, extremo, dirección, timestamps, fuente, serie de precio.
- **TEST_POSITIVO:** T-001
- **TEST_NEGATIVO:** T-040
- **TEST_FRONTERA:** T-001
- **ESTADO_APROBACIÓN:** `PROVISIONAL` (detección general del 1 inicial; el caso de la vela 1 está validado).

### N-002 — Apertura de vela: gap o plano

- **ID:** N-002
- **ESTADO_ORIGEN:** `1_ACTIVA`, `2_CONFIRMADA` o lectura activa.
- **EVENTO:** Apertura de vela nueva.
- **PRECONDICIONES:** Cierre de vela anterior y apertura nueva disponibles.
- **FÓRMULA:** `Δ = apertura_nueva − cierre_vela_anterior`. `|Δ| ≤ 0,25` = plano; `|Δ| > 0,25` = gap.
- **SI_TRUE:** Si plano → N-005; si gap → N-003 o N-004.
- **SI_FALSE:** Sin datos suficientes → `PENDIENTE_JAVIER`; no evaluar 2.
- **ESTADO_DESTINO:** `EVALUANDO_APERTURA` (control) → `2_CANDIDATA` o `A_GRANDE`.
- **LECTURA_AFECTADA:** L1/L2/L3 activa.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No aplicar la regla de 2 antes del gap; no usar el cierre del movimiento como referencia.
- **DATOS_A_GUARDAR:** `Δ`, cierre anterior, apertura nueva, timestamps, decisión plano/gap.
- **TEST_POSITIVO:** T-004
- **TEST_NEGATIVO:** T-037
- **TEST_FRONTERA:** T-038
- **ESTADO_APROBACIÓN:** `CERRADO` (H14 / H11).

### N-003 — Gap a favor de 1

- **ID:** N-003
- **ESTADO_ORIGEN:** `EVALUANDO_APERTURA` con gap.
- **EVENTO:** Gap en la misma dirección que 1.
- **PRECONDICIONES:** 1 activo; gap confirmado; dirección del gap = dirección de 1.
- **FÓRMULA:** `signo(Δ) = signo(1)`.
- **SI_TRUE:** A y B implícitas; posible TT; pasa a `TT_PENDIENTE`.
- **SI_FALSE:** N-004.
- **ESTADO_DESTINO:** `TT_PENDIENTE` (AUT por gap: `PENDIENTE_JAVIER`).
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No evaluar 2; no confirmar TT sin 100 %; no afirmar AUT por gap sin regla.
- **DATOS_A_GUARDAR:** tamaño del gap, A/B implícitas, módulo aplicable, objetivo TT.
- **TEST_POSITIVO:** T-002
- **TEST_NEGATIVO:** T-037
- **TEST_FRONTERA:** T-002
- **ESTADO_APROBACIÓN:** `CERRADO` para A/B implícitas y no 2; `PENDIENTE_JAVIER` para AUT por gap.

### N-004 — Gap contrario a 1

- **ID:** N-004
- **ESTADO_ORIGEN:** `EVALUANDO_APERTURA` con gap.
- **EVENTO:** Gap en dirección contraria a 1.
- **PRECONDICIONES:** 1 activo; gap confirmado; dirección contraria.
- **FÓRMULA:** `signo(Δ) = −signo(1)`.
- **SI_TRUE:** El movimiento es A Grande en dirección del gap; se sigue midiendo A con ticks.
- **SI_FALSE:** N-003.
- **ESTADO_DESTINO:** `A_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No evaluar 2; no llamar B antes de A.
- **DATOS_A_GUARDAR:** gap, inicio de A, extremo, timestamps.
- **TEST_POSITIVO:** T-003
- **TEST_NEGATIVO:** T-002
- **TEST_FRONTERA:** T-003
- **ESTADO_APROBACIÓN:** `CERRADO` (H11 / v3 §9.2).

### N-005 — Sin gap: salida en plano

- **ID:** N-005
- **ESTADO_ORIGEN:** `1_ACTIVA` tras apertura sin gap.
- **EVENTO:** Apertura nueva dentro de ±0,25 del cierre anterior.
- **PRECONDICIONES:** `|Δ| ≤ 0,25`; no hay gap.
- **FÓRMULA:** `|apertura_nueva − cierre_vela_anterior| ≤ 0,25`.
- **SI_TRUE:** Abre evaluación de posible 2 → N-006.
- **SI_FALSE:** Es gap → N-003/N-004.
- **ESTADO_DESTINO:** `2_CANDIDATA/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No llamar 2 solo por continuidad de dirección; no usar `Close(1)` del movimiento si la regla exige cierre de vela.
- **DATOS_A_GUARDAR:** `Δ`, cierre anterior, apertura, timestamps.
- **TEST_POSITIVO:** T-004
- **TEST_NEGATIVO:** T-037
- **TEST_FRONTERA:** T-038
- **ESTADO_APROBACIÓN:** `CERRADO` (H14).

### N-006 — Posible 2

- **ID:** N-006
- **ESTADO_ORIGEN:** `1_ACTIVA` / `EVALUANDO_2`.
- **EVENTO:** Movimiento en la misma dirección que 1 tras salida en plano.
- **PRECONDICIONES:** (a) misma dirección que 1; (b) rango de 2 ≥ rango de 1; (c) salida en plano; (d) cola observable ≤ 0,25.
- **FÓRMULA:** `rango_2 ≥ rango_1`; alcista `Low(2) = Open(2)`; bajista `High(2) = Open(2)`; tolerancia 0,25.
- **SI_TRUE:** `2_CANDIDATA`.
- **SI_FALSE:** N-008 (módulo + A Grande).
- **ESTADO_DESTINO:** `2_CANDIDATA/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No confirmar 2 por `High−Low`; no ignorar cola > 0,25.
- **DATOS_A_GUARDAR:** rango 1, rango 2, cola, apertura, cierre, timestamps.
- **TEST_POSITIVO:** T-001
- **TEST_NEGATIVO:** T-005
- **TEST_FRONTERA:** T-005
- **ESTADO_APROBACIÓN:** `CERRADO` (A1).

### N-007 — Confirmar 2

- **ID:** N-007
- **ESTADO_ORIGEN:** `2_CANDIDATA`.
- **EVENTO:** Desplazamiento direccional de 2 alcanza el tamaño de 1.
- **PRECONDICIONES:** N-006 cumplido; no hay gap.
- **FÓRMULA:** `desplazamiento_direccional(2) ≥ rango(1)`.
- **SI_TRUE:** `2_CONFIRMADA/ACTIVA`.
- **SI_FALSE:** Permanece candidata o N-008 si falla una condición.
- **ESTADO_DESTINO:** `2_CONFIRMADA/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No borrar 2 si después aparece el contrario; no llamar 3.
- **DATOS_A_GUARDAR:** tick de confirmación, desplazamiento, rango 1.
- **TEST_POSITIVO:** T-001
- **TEST_NEGATIVO:** T-005
- **TEST_FRONTERA:** T-001
- **ESTADO_APROBACIÓN:** `CERRADO` (A1).

### N-008 — Fallo de 2

- **ID:** N-008
- **ESTADO_ORIGEN:** Evaluación de 2.
- **EVENTO:** Falla dirección, rango, plano o cola.
- **PRECONDICIONES:** Alguna condición de N-006 no se cumple.
- **FÓRMULA:** Negación de N-006.
- **SI_TRUE:** 1 pasa a módulo por descarte; movimiento contrario = A Grande.
- **SI_FALSE:** N-007.
- **ESTADO_DESTINO:** `MODULO/ACTIVA` + `A_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No llamar 2; no llamar 3; conservar 1.
- **DATOS_A_GUARDAR:** causa del fallo, rango 1, extremos, timestamps.
- **TEST_POSITIVO:** T-005
- **TEST_NEGATIVO:** T-001
- **TEST_FRONTERA:** T-005
- **ESTADO_APROBACIÓN:** `CERRADO` (A1).

### N-009 — Posible 3

- **ID:** N-009
- **ESTADO_ORIGEN:** `2_CONFIRMADA`.
- **EVENTO:** Retroceso y nuevo extremo.
- **PRECONDICIONES:** Retroceso entre 0 % y 50 % del rango de 2; superación del extremo de 2.
- **FÓRMULA:** alcista `High(3) > High(2)`; bajista `Low(3) < Low(2)`; retroceso 0–50 %.
- **SI_TRUE:** `3_CANDIDATA/ACTIVA`.
- **SI_FALSE:** N-011.
- **ESTADO_DESTINO:** `3_CANDIDATA/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No llamar 3 si retrocede > 50 %; no borrar 2.
- **DATOS_A_GUARDAR:** retroceso, extremo 2, extremo 3, timestamps.
- **TEST_POSITIVO:** T-007 / T-009
- **TEST_NEGATIVO:** T-008
- **TEST_FRONTERA:** T-007
- **ESTADO_APROBACIÓN:** `CERRADO` (v3 §4.3).

### N-010 — Confirmar 3

- **ID:** N-010
- **ESTADO_ORIGEN:** `3_CANDIDATA`.
- **EVENTO:** Se cumplen simultáneamente las dos reglas de 3.
- **PRECONDICIONES:** Retroceso 0–50 % y superación del extremo de 2.
- **FÓRMULA:** N-009.
- **SI_TRUE:** `3_CONFIRMADA/ACTIVA`; ciclo modular regular.
- **SI_FALSE:** N-011.
- **ESTADO_DESTINO:** `3_CONFIRMADA/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No usar 3 como módulo sin confirmar; no mezclar con A.
- **DATOS_A_GUARDAR:** tick de confirmación, extremos, retroceso.
- **TEST_POSITIVO:** T-009
- **TEST_NEGATIVO:** T-008
- **TEST_FRONTERA:** T-007
- **ESTADO_APROBACIÓN:** `CERRADO` (v3 §4.3).

### N-011 — Fallo de 3: módulo 1+2 y A Grande

- **ID:** N-011
- **ESTADO_ORIGEN:** Evaluación de 3.
- **EVENTO:** Retroceso > 50 % o no supera extremo de 2.
- **PRECONDICIONES:** 2 confirmado; 3 no válido.
- **FÓRMULA:** Negación de N-009.
- **SI_TRUE:** `1+2 = MODULO`; movimiento contrario = `A_GRANDE`.
- **SI_FALSE:** N-010.
- **ESTADO_DESTINO:** `MODULO/ACTIVA` + `A_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No crear C antes de B; no llamar 3 fallido a un 2 no confirmado.
- **DATOS_A_GUARDAR:** rango del módulo, extremos, velas implicadas, timestamps.
- **TEST_POSITIVO:** T-010
- **TEST_NEGATIVO:** T-009
- **TEST_FRONTERA:** T-008
- **ESTADO_APROBACIÓN:** `CERRADO` para 1+2 regular; `PENDIENTE_JAVIER` para módulo general.

### N-012 — Medida del módulo

- **ID:** N-012
- **ESTADO_ORIGEN:** `MODULO`.
- **EVENTO:** Calcular rango de expansión.
- **PRECONDICIONES:** Composición del módulo conocida.
- **FÓRMULA:** `rango_modulo = max(highs) − min(lows)` del conjunto de velas del módulo.
- **SI_TRUE:** Guardar máximo, mínimo, rango, velas, timestamps y lectura de origen.
- **SI_FALSE:** Si la composición no está cerrada → `PENDIENTE_JAVIER`.
- **ESTADO_DESTINO:** `MODULO/ACTIVA` con rango calculado.
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No usar solo la última vela; no usar el rango de A como módulo; no inventar módulo de una vela.
- **DATOS_A_GUARDAR:** máximo, mínimo, rango, velas, timestamps.
- **TEST_POSITIVO:** T-011
- **TEST_NEGATIVO:** T-011
- **TEST_FRONTERA:** T-011
- **ESTADO_APROBACIÓN:** `CERRADO` para 1+2 regular; `PENDIENTE_JAVIER` para módulo por descarte / una vela (H17 / DUDA-009).

### N-013 — A Grande se extiende entre velas

- **ID:** N-013
- **ESTADO_ORIGEN:** `A_GRANDE`.
- **EVENTO:** La vela siguiente continúa la dirección de A sin volver.
- **PRECONDICIONES:** A activa; no hay referencia TM nueva.
- **FÓRMULA:** Actualizar extremo de A; `fin_A = extremo real`.
- **SI_TRUE:** A continúa; no se cierra en el primer extremo.
- **SI_FALSE:** N-014.
- **ESTADO_DESTINO:** `A_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No cerrar A en el primer máximo si la vela siguiente lo extiende.
- **DATOS_A_GUARDAR:** extremo actualizado, velas, timestamps.
- **TEST_POSITIVO:** T-012
- **TEST_NEGATIVO:** T-012
- **TEST_FRONTERA:** T-012
- **ESTADO_APROBACIÓN:** `CERRADO` para extensión (H4/H15); `PROVISIONAL` para tick exacto de fin (P3).

### N-014 — B candidata

- **ID:** N-014
- **ESTADO_ORIGEN:** `A_GRANDE` finalizada.
- **EVENTO:** Movimiento contrario a A.
- **PRECONDICIONES:** A Grande delimitada; B no alcanza el 100 % de A.
- **FÓRMULA:** `B_pct = desplazamiento_B / rango_A × 100`; si `< 100` → candidata.
- **SI_TRUE:** `B_CANDIDATA/ACTIVA`.
- **SI_FALSE:** N-015.
- **ESTADO_DESTINO:** `B_CANDIDATA/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No llamar B Grande antes del 100 %; no crear C.
- **DATOS_A_GUARDAR:** inicio B, porcentaje, rango A, timestamps.
- **TEST_POSITIVO:** T-013
- **TEST_NEGATIVO:** T-014
- **TEST_FRONTERA:** T-013
- **ESTADO_APROBACIÓN:** `CERRADO` (H12); tick exacto `PROVISIONAL` (P3).

### N-015 — B Grande 100–127 % + 0,25

- **ID:** N-015
- **ESTADO_ORIGEN:** `B_CANDIDATA`.
- **EVENTO:** B alcanza el 100 % sin superar `127 % + 0,25`.
- **PRECONDICIONES:** `100 % ≤ recorrido ≤ 127 % + 0,25`.
- **FÓRMULA:** `rango_A × 1,00 ≤ recorrido_B ≤ rango_A × 1,27 + 0,25`.
- **SI_TRUE:** `B_GRANDE/CONFIRMADA`.
- **SI_FALSE:** N-017.
- **ESTADO_DESTINO:** `B_GRANDE/CONFIRMADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No llamar AUT en el 100 %; no borrar B.
- **DATOS_A_GUARDAR:** porcentaje, nivel 100 %, nivel 127 % + 0,25, timestamps.
- **TEST_POSITIVO:** T-014
- **TEST_NEGATIVO:** T-015
- **TEST_FRONTERA:** T-015
- **ESTADO_APROBACIÓN:** `CERRADO` (H13a).

### N-016 — B toca 127 % + 0,25 y vuelve

- **ID:** N-016
- **ESTADO_ORIGEN:** `B_GRANDE`.
- **EVENTO:** Toque exacto del nivel `127 % + 0,25` y reversión.
- **PRECONDICIONES:** Toque sin superar; B confirmada.
- **FÓRMULA:** `recorrido = 1,27 × rango_A + 0,25`.
- **SI_TRUE:** No hay AUT; B Grande continúa; el movimiento contrario será C Grande (N-022).
- **SI_FALSE:** N-017.
- **ESTADO_DESTINO:** `B_GRANDE/CONFIRMADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No llamar AUT por tocar; no llamar CUT.
- **DATOS_A_GUARDAR:** nivel tocado, tick, reversión, timestamps.
- **TEST_POSITIVO:** T-015
- **TEST_NEGATIVO:** T-016
- **TEST_FRONTERA:** T-015
- **ESTADO_APROBACIÓN:** `CERRADO` (H9).

### N-017 — B supera 127 % + 0,25: AUT

- **ID:** N-017
- **ESTADO_ORIGEN:** `B_GRANDE`.
- **EVENTO:** B supera `127 % + 0,25`.
- **PRECONDICIONES:** B confirmada; superación estricta.
- **FÓRMULA:** `recorrido > 1,27 × rango_A + 0,25`.
- **SI_TRUE:** AUT inmediato; B deja de ser la clasificación vigente; nuevo 1 candidato.
- **SI_FALSE:** N-015/N-016.
- **ESTADO_DESTINO:** `AUT/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER` (posible L2 local).
- **PROHIBICIONES:** No `B_EXCESIVA`; B y AUT no coexisten; no confirmar TT.
- **DATOS_A_GUARDAR:** tick de superación, nivel, B previa, timestamps.
- **TEST_POSITIVO:** T-016
- **TEST_NEGATIVO:** T-015
- **TEST_FRONTERA:** T-016
- **ESTADO_APROBACIÓN:** `CERRADO` para AUT (B1/H13c); apertura L2 `PENDIENTE_JAVIER`.

### N-018 — AUT: TT pendiente

- **ID:** N-018
- **ESTADO_ORIGEN:** `AUT`.
- **EVENTO:** AUT confirmado con módulo disponible.
- **PRECONDICIONES:** Módulo calculado; TT no confirmado.
- **FÓRMULA:** `TT_alcista = fin_A + rango_modulo`; `TT_bajista = fin_A − rango_modulo`.
- **SI_TRUE:** `TT_PENDIENTE`.
- **SI_FALSE:** Sin módulo → `PENDIENTE_JAVIER`.
- **ESTADO_DESTINO:** `TT_PENDIENTE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No confirmar TT; no FT; no mezclar módulo de otra lectura.
- **DATOS_A_GUARDAR:** módulo, fin A, objetivo TT, tick AUT, timestamps.
- **TEST_POSITIVO:** T-017
- **TEST_NEGATIVO:** T-017
- **TEST_FRONTERA:** T-017
- **ESTADO_APROBACIÓN:** `CERRADO` con módulo (B2/B3/A3); sin módulo `PENDIENTE_JAVIER`.

### N-019 — TT confirmado

- **ID:** N-019
- **ESTADO_ORIGEN:** `TT_PENDIENTE`.
- **EVENTO:** El precio alcanza el objetivo TT.
- **PRECONDICIONES:** AUT activo; objetivo calculado; tick válido.
- **FÓRMULA:** alcista `precio ≥ TT_alcista`; bajista `precio ≤ TT_bajista`; mismo tick permitido.
- **SI_TRUE:** `TT_CONFIRMADO`; nace `NUEVO_1`.
- **SI_FALSE:** N-020.
- **ESTADO_DESTINO:** `TT_CONFIRMADO/ACTIVA` + `NUEVO_1`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No TT antes del 100 %; no FT antes de TT; no usar otro retroceso de A.
- **DATOS_A_GUARDAR:** tick, precio, objetivo, módulo, fin A, overshoot.
- **TEST_POSITIVO:** T-018 / T-019
- **TEST_NEGATIVO:** T-020
- **TEST_FRONTERA:** T-018
- **ESTADO_APROBACIÓN:** `CERRADO` (A3/B3/v3 §7.1).

### N-020 — TT fallido

- **ID:** N-020
- **ESTADO_ORIGEN:** `TT_PENDIENTE`.
- **EVENTO:** No alcanza el 100 % y el precio toca el final de A.
- **PRECONDICIONES:** TT pendiente; final de A definido.
- **FÓRMULA:** `precio = fin_A` sin haber alcanzado TT.
- **SI_TRUE:** TT cancelado; todo el recorrido anterior pasa a módulo; el retorno es A Grande.
- **SI_FALSE:** N-019.
- **ESTADO_DESTINO:** `TT_FALLIDO` → `MODULO/ACTIVA` + `A_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No llamar C al retorno; no llamar CUT; no borrar historial.
- **DATOS_A_GUARDAR:** tick de toque, final A, módulo nuevo, timestamps.
- **TEST_POSITIVO:** T-020
- **TEST_NEGATIVO:** T-018
- **TEST_FRONTERA:** T-020
- **ESTADO_APROBACIÓN:** `CERRADO` (v3 §7.3C / §10B).

### N-021 — Nuevo 1 después de TT

- **ID:** N-021
- **ESTADO_ORIGEN:** `TT_CONFIRMADO`.
- **EVENTO:** El movimiento que completa el objetivo TT.
- **PRECONDICIONES:** TT confirmado al 100 %.
- **FÓRMULA:** `nuevo_1` = recorrido desde fin de A hasta el extremo que alcanza/supera TT; rango real del recorrido.
- **SI_TRUE:** `NUEVO_1/CONFIRMADA`.
- **SI_FALSE:** No aplica.
- **ESTADO_DESTINO:** `NUEVO_1/CONFIRMADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No llamar 1 antes de TT; no mezclar su rango con el módulo anterior.
- **DATOS_A_GUARDAR:** inicio, extremo, rango real, tick TT, módulo de origen.
- **TEST_POSITIVO:** T-021
- **TEST_NEGATIVO:** T-018
- **TEST_FRONTERA:** T-021
- **ESTADO_APROBACIÓN:** `CERRADO` (v3 §7.4 / DEC-012).

### N-022 — C Grande

- **ID:** N-022
- **ESTADO_ORIGEN:** `B_GRANDE`.
- **EVENTO:** Movimiento contrario a B.
- **PRECONDICIONES:** B Grande confirmada en la misma lectura.
- **FÓRMULA:** dirección de C = dirección de A; C no es candidata tras B confirmada.
- **SI_TRUE:** `C_GRANDE/ACTIVA`.
- **SI_FALSE:** B continúa.
- **ESTADO_DESTINO:** `C_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No C antes de B; no CUT sin C; no llamar C a un micromovimiento.
- **DATOS_A_GUARDAR:** inicio C, dirección, B previa, timestamps.
- **TEST_POSITIVO:** T-022
- **TEST_NEGATIVO:** T-035
- **TEST_FRONTERA:** T-022
- **ESTADO_APROBACIÓN:** `CERRADO` (H13b / v3 §5.3).

### N-023 — B crea nuevo extremo: C cancelada

- **ID:** N-023
- **ESTADO_ORIGEN:** `C_GRANDE` / `B_GRANDE`.
- **EVENTO:** B Grande crea un nuevo extremo.
- **PRECONDICIONES:** C activa pero no CUT.
- **FÓRMULA:** nuevo extremo de B en su dirección.
- **SI_TRUE:** C Grande se cancela; B Grande continúa.
- **SI_FALSE:** N-024.
- **ESTADO_DESTINO:** `B_GRANDE/CONFIRMADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No confirmar CUT; no borrar C del historial.
- **DATOS_A_GUARDAR:** nuevo extremo, tick, C cancelada.
- **TEST_POSITIVO:** T-023
- **TEST_NEGATIVO:** T-024
- **TEST_FRONTERA:** T-023
- **ESTADO_APROBACIÓN:** `CERRADO` (H13d).

### N-024 — CUT

- **ID:** N-024
- **ESTADO_ORIGEN:** `C_GRANDE`.
- **EVENTO:** C Grande supera el final de A Grande.
- **PRECONDICIONES:** B Grande confirmada; C Grande válida; final de A definido.
- **FÓRMULA:** alcista/bajista según dirección; `C` supera `fin_A`.
- **SI_TRUE:** `CUT/CONFIRMADA`.
- **SI_FALSE:** N-025.
- **ESTADO_DESTINO:** `CUT/CONFIRMADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No CUT por base cualquiera; no CUT por color; no CUT sin C.
- **DATOS_A_GUARDAR:** fin A, extremo C, tick de superación, timestamps.
- **TEST_POSITIVO:** T-024
- **TEST_NEGATIVO:** T-025
- **TEST_FRONTERA:** T-024
- **ESTADO_APROBACIÓN:** `CERRADO` (v3 §6.2 / B4).

### N-025 — C = nuevo 1

- **ID:** N-025
- **ESTADO_ORIGEN:** `C_GRANDE` sin CUT.
- **EVENTO:** C cierra la referencia y pasa a nuevo 1 del ciclo siguiente.
- **PRECONDICIONES:** C Grande válida; no alcanza CUT; condición exacta `PENDIENTE_JAVIER`.
- **FÓRMULA:** `PENDIENTE_JAVIER`.
- **SI_TRUE:** `NUEVO_1`.
- **SI_FALSE:** C permanece en su rama.
- **ESTADO_DESTINO:** `NUEVO_1` (si Javier lo confirma)
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No declarar `C = nuevo 1` sin condición matemática cerrada.
- **DATOS_A_GUARDAR:** C, referencia cerrada, tick, lectura de origen.
- **TEST_POSITIVO:** T-026
- **TEST_NEGATIVO:** T-026
- **TEST_FRONTERA:** T-026
- **ESTADO_APROBACIÓN:** `PENDIENTE_JAVIER` (H1 / PR-e / DUDA-J04).

### N-026 — FT

- **ID:** N-026
- **ESTADO_ORIGEN:** `TT_CONFIRMADO`.
- **EVENTO:** Pérdida de velocidad y movimiento contrario claro.
- **PRECONDICIONES:** TT confirmado; referencia exacta y desplazamiento mínimo `PENDIENTE_JAVIER`.
- **FÓRMULA:** `PENDIENTE_JAVIER`.
- **SI_TRUE:** `FT`.
- **SI_FALSE:** No FT.
- **ESTADO_DESTINO:** `FT`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No FT sin TT; no FT por micromovimiento; no mezclar FT con lectura modular.
- **DATOS_A_GUARDAR:** TT previo, velocidad, movimiento contrario, tick.
- **TEST_POSITIVO:** T-028
- **TEST_NEGATIVO:** T-027
- **TEST_FRONTERA:** T-028
- **ESTADO_APROBACIÓN:** `PENDIENTE_JAVIER` (P6 / DUDA-J05).

### N-027 — Reclasificación live

- **ID:** N-027
- **ESTADO_ORIGEN:** Cualquier lectura activa.
- **EVENTO:** Corrección posterior que cambia la función de velas anteriores.
- **PRECONDICIONES:** Evidencia de corrección; criterios exactos `PENDIENTE_JAVIER`.
- **FÓRMULA:** `PENDIENTE_JAVIER`.
- **SI_TRUE:** `RECLASIFICADA` o `INTEGRADA`; se conserva el historial.
- **SI_FALSE:** La lectura continúa.
- **ESTADO_DESTINO:** `RECLASIFICADA/ACTIVA` o `INTEGRADA/FINALIZADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No borrar; no mezclar niveles; no reescribir el pasado.
- **DATOS_A_GUARDAR:** evento anterior, evento nuevo, motivo, tick, lectura.
- **TEST_POSITIVO:** T-034
- **TEST_NEGATIVO:** T-034
- **TEST_FRONTERA:** T-034
- **ESTADO_APROBACIÓN:** `PROVISIONAL` (P4).

### N-028 — Abrir L2

- **ID:** N-028
- **ESTADO_ORIGEN:** L1 activa.
- **EVENTO:** Candidato a segunda lectura coherente.
- **PRECONDICIONES:** Regla TM expresa; lectura matemáticamente válida; no ruido.
- **FÓRMULA:** No hay fórmula; la apertura es normativa.
- **SI_TRUE:** L2/`lectura 2` activa.
- **SI_FALSE:** El movimiento pertenece a L1 o se descarta.
- **ESTADO_DESTINO:** `LECTURA_2/ACTIVA`
- **LECTURA_AFECTADA:** L2
- **¿ABRE_NUEVA_LECTURA?:** SÍ, solo con regla expresa.
- **PROHIBICIONES:** No abrir por ver A/B/AUT dentro de una vela; no abrir por ruido; no mezclar con L1.
- **DATOS_A_GUARDAR:** regla que autoriza, referencia, módulo, niveles, tick.
- **TEST_POSITIVO:** T-029
- **TEST_NEGATIVO:** T-030
- **TEST_FRONTERA:** T-029
- **ESTADO_APROBACIÓN:** `PENDIENTE_JAVIER` (DUDA-J01).

### N-029 — Abrir L3

- **ID:** N-029
- **ESTADO_ORIGEN:** L1 y L2 activas.
- **EVENTO:** Candidato a tercera lectura coherente.
- **PRECONDICIONES:** Regla TM expresa; L1/L2 válidas; máximo 3.
- **FÓRMULA:** No hay fórmula; la apertura es normativa.
- **SI_TRUE:** L3/`lectura 3` activa.
- **SI_FALSE:** No se abre; nunca L4.
- **ESTADO_DESTINO:** `LECTURA_3/ACTIVA`
- **LECTURA_AFECTADA:** L3
- **¿ABRE_NUEVA_LECTURA?:** SÍ, solo con regla expresa.
- **PROHIBICIONES:** No L4; no abrir por ruido; no mezclar.
- **DATOS_A_GUARDAR:** regla que autoriza, referencia, niveles, tick.
- **TEST_POSITIVO:** T-039
- **TEST_NEGATIVO:** T-040
- **TEST_FRONTERA:** T-039
- **ESTADO_APROBACIÓN:** `PENDIENTE_JAVIER` (DUDA-J01).

### N-030 — Prioridad en el mismo tick

- **ID:** N-030
- **ESTADO_ORIGEN:** L1/L2/L3 activas.
- **EVENTO:** Dos o tres lecturas alcanzan nivel en el mismo tick.
- **PRECONDICIONES:** Niveles calculados; tick común.
- **FÓRMULA:** `PENDIENTE_JAVIER`.
- **SI_TRUE:** Aplicar la prioridad que fije Javier.
- **SI_FALSE:** Cada lectura se resuelve por separado.
- **ESTADO_DESTINO:** `PENDIENTE_JAVIER`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No resolver por orden de aparición, color, conveniencia ni resultado posterior.
- **DATOS_A_GUARDAR:** tick, niveles alcanzados, lecturas implicadas.
- **TEST_POSITIVO:** T-029
- **TEST_NEGATIVO:** T-029
- **TEST_FRONTERA:** T-029
- **ESTADO_APROBACIÓN:** `PENDIENTE_JAVIER` (P5 / DUDA-J03).

### N-031 — Cierre y archivo de lectura

- **ID:** N-031
- **ESTADO_ORIGEN:** Lectura activa.
- **EVENTO:** TT confirmado, CUT confirmado, invalidación, reclasificación o pérdida de coherencia.
- **PRECONDICIONES:** Resolución matemática documentada.
- **FÓRMULA:** Según evento.
- **SI_TRUE:** `FINALIZADA`, `INVALIDADA`, `RECLASIFICADA` o `INTEGRADA`.
- **SI_FALSE:** Continúa activa.
- **ESTADO_DESTINO:** `FINALIZADA/INVALIDADA/RECLASIFICADA/INTEGRADA`
- **LECTURA_AFECTADA:** La lectura resuelta.
- **¿ABRE_NUEVA_LECTURA?:** NO por sí solo.
- **PROHIBICIONES:** No borrar eventos; no reutilizar el slot sin conservar historial.
- **DATOS_A_GUARDAR:** causa, tick, estado final, historial.
- **TEST_POSITIVO:** T-034
- **TEST_NEGATIVO:** T-034
- **TEST_FRONTERA:** T-034
- **ESTADO_APROBACIÓN:** `CERRADO` para cierre; `PROVISIONAL` para reclasificación.

### N-032 — Ruido y micromovimiento

- **ID:** N-032
- **ESTADO_ORIGEN:** Cualquier lectura.
- **EVENTO:** Oscilación que no alcanza una referencia TM.
- **PRECONDICIONES:** No alcanza referencia; umbral numérico `PENDIENTE_JAVIER`.
- **FÓRMULA:** No se calcula; se descarta.
- **SI_TRUE:** No ocupa lectura; no se clasifica.
- **SI_FALSE:** N-001 u otra rama válida.
- **ESTADO_DESTINO:** `SIN_LECTURA` (descartado)
- **LECTURA_AFECTADA:** Ninguna.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No convertir en A/B/C/AUT/TT; no abrir lectura; no contar como nuevo 1.
- **DATOS_A_GUARDAR:** motivo de descarte, tick, referencia no alcanzada.
- **TEST_POSITIVO:** T-031
- **TEST_NEGATIVO:** T-031
- **TEST_FRONTERA:** T-031
- **ESTADO_APROBACIÓN:** `CERRADO` metodológico (H16 / DEC-015); umbral `PENDIENTE_JAVIER` (PR-g).

### N-033 — AUT y TT en el mismo tick

- **ID:** N-033
- **ESTADO_ORIGEN:** `B_GRANDE` / `AUT`.
- **EVENTO:** Un salto cruza AUT y TT en el mismo tick.
- **PRECONDICIONES:** Módulo; objetivo TT; tick único.
- **FÓRMULA:** `precio` supera AUT y alcanza TT en el mismo tick.
- **SI_TRUE:** AUT y TT confirmados en el mismo tick; nace nuevo 1.
- **SI_FALSE:** N-018 / N-019.
- **ESTADO_DESTINO:** `TT_CONFIRMADO/ACTIVA` + `NUEVO_1`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No saltar AUT; no confirmar TT antes del 100 %.
- **DATOS_A_GUARDAR:** tick, AUT, TT, overshoot.
- **TEST_POSITIVO:** T-033
- **TEST_NEGATIVO:** T-018
- **TEST_FRONTERA:** T-033
- **ESTADO_APROBACIÓN:** `CERRADO` (B3).

### N-034 — C Grande: tres funciones

- **ID:** N-034
- **ESTADO_ORIGEN:** `C_GRANDE`.
- **EVENTO:** Evaluar C tras B.
- **PRECONDICIONES:** B confirmada; C válida.
- **FÓRMULA:** Orden: (1) CUT; (2) C = nuevo 1; (3) C = A Grande de lectura mayor.
- **SI_TRUE:** Primera función aplicable.
- **SI_FALSE:** `PENDIENTE_JAVIER`.
- **ESTADO_DESTINO:** `CUT` / `NUEVO_1` / `A_GRANDE` (lectura mayor)
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** La tercera función puede abrir lectura mayor: `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No crear movimientos adicionales; no CUT sin C.
- **DATOS_A_GUARDAR:** C, final A, funciones comprobadas, tick.
- **TEST_POSITIVO:** T-024 / T-026
- **TEST_NEGATIVO:** T-025
- **TEST_FRONTERA:** T-034
- **ESTADO_APROBACIÓN:** `PROVISIONAL` (H3 cerrada en orden; C=new1 y lectura mayor pendientes).

### N-035 — Invalidación de lectura

- **ID:** N-035
- **ESTADO_ORIGEN:** Lectura activa.
- **EVENTO:** Toque del nivel de invalidación antes de TT o pérdida de coherencia.
- **PRECONDICIONES:** Nivel definido.
- **FÓRMULA:** `precio` alcanza el final de A o el nivel de invalidación.
- **SI_TRUE:** `INVALIDADA` o `RECLASIFICADA`.
- **SI_FALSE:** Continúa.
- **ESTADO_DESTINO:** `INVALIDADA` / `RECLASIFICADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No borrar; no mezclar.
- **DATOS_A_GUARDAR:** nivel, tick, causa.
- **TEST_POSITIVO:** T-020
- **TEST_NEGATIVO:** T-018
- **TEST_FRONTERA:** T-020
- **ESTADO_APROBACIÓN:** `CERRADO` para TT fallido; `PROVISIONAL` para otras invalidaciones.

### N-036 — 2 confirmado no se borra

- **ID:** N-036
- **ESTADO_ORIGEN:** `2_CONFIRMADA`.
- **EVENTO:** Aparece movimiento contrario después de 2.
- **PRECONDICIONES:** 2 confirmado.
- **FÓRMULA:** 2 se conserva; 1+2 = módulo; contrario = A Grande.
- **SI_TRUE:** `MODULO` + `A_GRANDE`.
- **SI_FALSE:** No aplica.
- **ESTADO_DESTINO:** `MODULO/ACTIVA` + `A_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No borrar 2; no llamar 3.
- **DATOS_A_GUARDAR:** 2 confirmado, módulo, A, tick.
- **TEST_POSITIVO:** T-006
- **TEST_NEGATIVO:** T-006
- **TEST_FRONTERA:** T-006
- **ESTADO_APROBACIÓN:** `CERRADO` (regla 4/5 del prompt).

### N-037 — B y AUT no coexisten

- **ID:** N-037
- **ESTADO_ORIGEN:** `B_GRANDE`.
- **EVENTO:** Superación de `127 % + 0,25`.
- **PRECONDICIONES:** B confirmada.
- **FÓRMULA:** N-017.
- **SI_TRUE:** B deja de ser B; AUT.
- **SI_FALSE:** B continúa.
- **ESTADO_DESTINO:** `AUT`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No `B_EXCESIVA`; no coexistencia.
- **DATOS_A_GUARDAR:** B previa, AUT, tick.
- **TEST_POSITIVO:** T-016
- **TEST_NEGATIVO:** T-015
- **TEST_FRONTERA:** T-016
- **ESTADO_APROBACIÓN:** `CERRADO` (B5).

### N-038 — A Grande multi-vela

- **ID:** N-038
- **ESTADO_ORIGEN:** `A_GRANDE`.
- **EVENTO:** A continúa en la vela siguiente.
- **PRECONDICIONES:** Sin referencia TM nueva.
- **FÓRMULA:** Actualizar extremo; no cerrar en el primer máximo.
- **SI_TRUE:** A continúa.
- **SI_FALSE:** N-014.
- **ESTADO_DESTINO:** `A_GRANDE/ACTIVA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No cerrar A por cambio de vela.
- **DATOS_A_GUARDAR:** extremos, velas, timestamps.
- **TEST_POSITIVO:** T-012
- **TEST_NEGATIVO:** T-012
- **TEST_FRONTERA:** T-012
- **ESTADO_APROBACIÓN:** `CERRADO` (H4/H15).

### N-039 — TT: alcanzar el 100 %

- **ID:** N-039
- **ESTADO_ORIGEN:** `TT_PENDIENTE`.
- **EVENTO:** El precio alcanza exactamente el objetivo o lo supera.
- **PRECONDICIONES:** Objetivo calculado.
- **FÓRMULA:** alcista `precio ≥ objetivo`; bajista `precio ≤ objetivo`.
- **SI_TRUE:** TT confirmado.
- **SI_FALSE:** TT pendiente.
- **ESTADO_DESTINO:** `TT_CONFIRMADO`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** `PENDIENTE_JAVIER`.
- **PROHIBICIONES:** No exigir superación estricta salvo decisión expresa; no confundir con AUT.
- **DATOS_A_GUARDAR:** precio, objetivo, tick, exacto/overshoot.
- **TEST_POSITIVO:** T-018
- **TEST_NEGATIVO:** T-020
- **TEST_FRONTERA:** T-018
- **ESTADO_APROBACIÓN:** `CERRADO` por «alcanzar el 100 %»; igualdad exacta sujeta a confirmación si Javier la distingue.

### N-040 — Medida direccional de 1 y 2

- **ID:** N-040
- **ESTADO_ORIGEN:** `1_ACTIVA` / `2_CANDIDATA`.
- **EVENTO:** Medir 1 y 2.
- **PRECONDICIONES:** Movimientos delimitados.
- **FÓRMULA:** Desplazamiento direccional, no `High−Low` completo.
- **SI_TRUE:** Aplicar N-006/N-007.
- **SI_FALSE:** No medir.
- **ESTADO_DESTINO:** `2_CANDIDATA` / `2_CONFIRMADA`
- **LECTURA_AFECTADA:** L1/L2/L3.
- **¿ABRE_NUEVA_LECTURA?:** NO.
- **PROHIBICIONES:** No usar `High−Low` para confirmar 2.
- **DATOS_A_GUARDAR:** desplazamiento, rango, tick.
- **TEST_POSITIVO:** T-001
- **TEST_NEGATIVO:** T-005
- **TEST_FRONTERA:** T-001
- **ESTADO_APROBACIÓN:** `CERRADO` (A1).

---

## 5. ARQUITECTURA D — PRECONDICIONES Y PROHIBICIONES GLOBALES

### 5.1. Precondiciones

1. Ticks en orden temporal y serie de precio declarada.
2. Movimiento delimitado antes de medir.
3. 1 antes de 2; 2 antes de 3.
4. Módulo antes de A.
5. A antes de B.
6. B confirmada antes de C.
7. AUT antes de TT.
8. TT antes de FT.
9. C Grande antes de CUT.
10. Final de A definido antes de CUT.
11. Lectura identificada antes de asignar función.
12. Si falta una precondición: `PENDIENTE_JAVIER`, no etiqueta.

### 5.2. Prohibiciones

- No usar color de vela.
- No usar OHLC aislado si hay ticks.
- No usar datos futuros.
- No usar golden como regla.
- No llamar B Grande antes del 100 %.
- No llamar C antes de B confirmada.
- No llamar CUT sin C Grande.
- No llamar TT antes del 100 %.
- No llamar FT sin TT.
- No llamar nuevo 1 antes de TT.
- No llamar C al retorno del TT fallido.
- No borrar una lectura al reclasificar.
- No abrir L2/L3 sin regla expresa.
- No calcular ruido ni micromovimientos.
- No mezclar niveles entre lecturas.
- No inventar módulo, autocorte ni nivel.

---

## 6. ARQUITECTURA E — FÓRMULAS Y FRONTERAS EXACTAS

### 6.1. Medidas

- `rango_1 = max(1) − min(1)` según la medida direccional aplicable.
- `rango_2` = desplazamiento direccional del movimiento 2, no `High−Low` completo.
- `rango_modulo = max(highs del módulo) − min(lows del módulo)`.
- `A = rango_A` = desplazamiento direccional del movimiento contrario al módulo.
- `B_pct = desplazamiento_B / rango_A × 100`.
- `TT_alcista = fin_A + rango_modulo`.
- `TT_bajista = fin_A − rango_modulo`.
- `AUT = fin_A ± (1,27 × rango_A + 0,25)`.
- `CUT`: C supera `fin_A`.
- `plano`: `|apertura_nueva − cierre_vela_anterior| ≤ 0,25`.
- `gap`: `|apertura_nueva − cierre_vela_anterior| > 0,25`.
- `cola`: alcista `Low(2) = Open(2)`; bajista `High(2) = Open(2)`; tolerancia 0,25.

### 6.2. Fronteras

| Frontera | Regla | Estado |
|---|---|---|
| Plano/gap | `≤ 0,25` plano; `> 0,25` gap | CERRADO (H14) |
| Cola de 2 | `≤ 0,25` permite 2; `> 0,25` no 2 | CERRADO (A1) |
| B 100 % | `< 100 %` candidata; `≥ 100 %` B Grande | CERRADO (H12) |
| B 127 % + 0,25 | `≤` B Grande; `>` AUT | CERRADO (H9/H13) |
| TT 100 % | `≥` objetivo alcista; `≤` objetivo bajista | CERRADO por «alcanzar»; igualdad exacta a confirmar si Javier la distingue |
| CUT | C supera `fin_A` | CERRADO |
| Límite lecturas | 2 normal; 3 máximo; 4 prohibido | CERRADO (H16) |
| Ruido | no se calcula; umbral numérico pendiente | `PENDIENTE_JAVIER` (PR-g) |

### 6.3. Unidades

- En la muestra, `1 tick = 0,25 puntos` (DEC-002).
- El margen `0,25` es fijo y no se deriva del CSV.
- La serie de precio de la muestra es **Bid**; la ratificación experta sigue pendiente (P2).

---

## 7. ARQUITECTURA F — HISTORIAL SIN BORRADO

- **CSV de eventos:** conserva lo que se sabía en cada tick.
- **CSV de estados:** fotografía de la clasificación vigente.
- **Reclasificar no es borrar:** el evento anterior permanece.
- Estados de ciclo de vida: `CANDIDATA`, `ACTIVA`, `CONFIRMADA`, `PENDIENTE`, `RECLASIFICADA`, `INTEGRADA`, `INVALIDADA`, `FINALIZADA`.
- Cada transición guarda: tick, lectura, estado anterior, evento, estado nuevo, niveles, motivo y fuente.
- Una lectura invalidada no se elimina: se marca y se conserva para auditoría.
- Una lectura integrada conserva su historial y se referencia desde la lectura mayor.
- No se reescribe el pasado con datos posteriores.

---

## 8. ARQUITECTURA G — CASOS VALIDADOS

### 8.1. Caso obligatorio: velas 1–3 (23:39–23:41)

**L1 — lectura principal:**

- Vela 1, 23:39: `1` alcista; rango `29182,80 − 29173,00 = 9,80`.
- Vela 2, 23:40: `A`, `B`, `AUT`; final de A `29179,20`; TT posible `29179,20 + 9,80 = 29189,00`.
- Vela 3, 23:41: alcanza `29189,30`; TT confirmado; vela 3 = `nuevo 1`.
- Estado: `CERRADO` para L1.

**L2 — lectura candidata observada, NO abierta por regla expresa:**

- En la vela 3 se observa un segundo recorrido coherente: módulo de vela 2 con rango `5,40`; A hasta `29182,00`; TT pequeño `29187,40`; nuevo 1 hasta `29189,30` (rango `7,30`).
- No se declara L2 porque falta la regla expresa de apertura (DUDA-J01).
- Si Javier confirma la apertura, L2 se documentará con sus propios niveles y no se mezclará con L1.
- Estado: `PENDIENTE_JAVIER`.

**Prohibición expresa:** no afirmar que la vela 3 contiene A, B y AUT propios de L1. La vela 3 es el `nuevo 1` de L1. Cualquier segunda lectura debe demostrarse por regla expresa.

### 8.2. Caso de TT fallido (contrafáctico validado en la auditoría)

- TT no alcanza el 100 % y el precio toca el final de A.
- Resultado: TT cancelado; recorrido anterior = módulo; retorno = A Grande del nuevo módulo.
- No se llama C al retorno; no se confirma CUT.
- Estado: `CERRADO` (v3 §7.3C / §10B).

---

## 9. ARQUITECTURA H — TESTS

El catálogo completo está en `control/TM_TESTS_REQUERIDOS_v1.md`.

Resumen:

- Tests positivos: 15.
- Tests negativos: 12.
- Tests de frontera: 8.
- Tests de cronología: 5.
- Tests de concurrencia: 5.
- Total: 45 tests planificados, ninguno implementado en esta fase.

Cada nodo referencia sus tests en `TEST_POSITIVO`, `TEST_NEGATIVO` y `TEST_FRONTERA`.

---

## 10. ARQUITECTURA I — REGISTRO DE DUDAS

El registro completo está en `control/TM_DUDAS_PENDIENTES_JAVIER.md`.

### 10.1. Cinco dudas bloqueantes

1. `DUDA-J01` — ¿Qué regla expresa abre L2/L3?
2. `DUDA-J02` — ¿La composición general del módulo es siempre 1+2 o admite una vela / vela anterior por descarte?
3. `DUDA-J03` — ¿Qué prioridad rige cuando dos o tres lecturas alcanzan nivel en el mismo tick?
4. `DUDA-J04` — ¿Cuál es la condición exacta de `C = nuevo 1` cuando C no alcanza CUT?
5. `DUDA-J05` — ¿Cuál es la regla matemática completa de FT?

### 10.2. Dudas secundarias

- `DUDA-S01` — Umbral numérico entre ruido y movimiento TM.
- `DUDA-S02` — ¿Un gap a favor de 1 confirma AUT o solo deja TT pendiente?
- `DUDA-S03` — Tick exacto de confirmación de A/B/C Grande.
- `DUDA-S04` — Serie de precio definitiva (Bid/Ask/Last/medio).
- `DUDA-S05` — Igualdad exacta en TT: ¿alcanzar o superar?

---

## 11. TRAZABILIDAD Y ESTADO DE APROBACIÓN

| Bloque | Estado | Fuente principal |
|---|---|---|
| 1, 2, 3 y módulo regular | CERRADO | A1/A2/v3 §4 |
| Gap y salida en plano | CERRADO | A4/H11/H14 |
| A Grande y B Grande | CERRADO | H4/H12/H13/H15 |
| AUT | CERRADO | B1/B2/B3/H8/H9 |
| TT y nuevo 1 | CERRADO | A3/B3/v3 §7 |
| C Grande y CUT | CERRADO | H13b/B4/v3 §6.2 |
| C = nuevo 1 | PENDIENTE_JAVIER | H1/PR-e |
| FT | PENDIENTE_JAVIER | P6 |
| Reclasificación | PROVISIONAL | P4 |
| Concurrencia L1-L3 | PARCIAL | H16/P5 |
| Ruido | PARCIAL | H16/PR-g |
| Módulo general | PENDIENTE_JAVIER | DUDA-009 |

### 11.1. Confirmación de alcance

- Este documento es un **árbol de decisión y máquina de estados**, no una implementación.
- No se ha modificado código, golden ni tests.
- No se ha creado una regla nueva sin fuente o decisión expresa.
- Las ramas sin regla quedan `PENDIENTE_JAVIER`.

---

## 12. ÍNDICE

1. Control de fuentes y alcance.
2. Mapa de reglas confirmadas y pendientes.
3. Arquitectura A — controlador de concurrencia L1-L3.
4. Arquitectura B — máquina de estados por lectura.
5. Arquitectura C — árbol completo de transiciones (N-001 a N-040).
6. Arquitectura D — precondiciones y prohibiciones globales.
7. Arquitectura E — fórmulas y fronteras exactas.
8. Arquitectura F — historial sin borrado.
9. Arquitectura G — casos validados.
10. Arquitectura H — tests.
11. Arquitectura I — registro de dudas.
12. Trazabilidad y estado de aprobación.
