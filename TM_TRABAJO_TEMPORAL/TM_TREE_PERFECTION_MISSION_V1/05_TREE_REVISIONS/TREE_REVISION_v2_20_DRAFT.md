# TM — REVISIÓN ACUMULADA v2.20 (BORRADOR, NO CONGELADA)

**Estado:** `DRAFT_NOT_FROZEN`
**Base:** `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md`
**SHA-256 base:** `94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17`
**Origen:** decisiones expertas del Checkpoint 1 (Q1, Q2, Q3) + auditoría de generaciones Fase 2.
**Regla:** este documento no sustituye v2.19. Es una revisión propuesta. No es autoridad ejecutable hasta que Javier la apruebe y se congele.

---

## 1. NODOS CORREGIDOS

### N-002 / N-005 — frontera de plano

```text
|Open - Close_previo| <  0,25  → plano
|Open - Close_previo| >= 0,25  → no plano
0,25 exactos NO es plano
```

Cerrado. Sin cambios posteriores.

### N-006 — condiciones de 2

2 solo se abre si:

- la vela abre en plano según N-002/N-005;
- no existe gap;
- no aparece cola inicial prohibitiva;
- el recorrido avanza en la dirección funcional de 1;
- 2 conserva una única candidatura durante su vela;
- las vibraciones internas no fragmentan 2 ni cancelan 2;
- no nace A Grande por una vibración interna;
- 2 conserva el origen de salida en plano y solo actualiza su extremo direccional.

Sin 2, el recorrido se resuelve como módulo por descarte y la pregunta siguiente es A Grande.

### N-012 — medida del módulo y propiedad de extremos

Sustituido por decisión Q2.

```text
knowledge_time_2 = primer tick en que 2 alcanza el 100 % de 1
extreme_2        = extremo final real de 2 antes del retroceso que abre 3
knowledge_time_3 = primer tick en que 3 supera estrictamente el extremo de 2
extreme_3        = extremo final real de 3 antes de comenzar A Grande
```

El módulo se mide con los **extremos estructurales finales** que pertenecen al módulo:

- origen estructural del módulo;
- extremo estructural más lejano con propiedad de módulo;
- un retroceso de 2 no encoje el módulo;
- un extremo que ya pertenece a A u otra función no se incorpora;
- no se usa `max(highs) − min(lows)` de las velas contenedoras;
- no se incluyen mechas anteriores al origen funcional sin regla expresa.

`knowledge_time` no se presenta como `structural_time`.

### N-021 — AUT y nuevo 1

Sustituido por decisión Q3 y por la regla 4.5.

```text
AUT → nuevo 1 inmediato en el mismo tick
```

- AUT por B: dirección del nuevo 1 = dirección de B; origen estructural = origen de B / final de A.
- AUT directo por A: dirección = A; origen = origen estructural de A.
- AUT por C usada como tendencia: dirección = C; origen = origen estructural de C.
- El tick de cruce es normalmente `knowledge_time`, no necesariamente `structural_time`.
- No se espera al 100 % del TT para reconocer el nuevo 1.
- El TT anterior puede quedar simultáneamente posible o pendiente.

### N-025 — TT

Cerrado por v2.17. TT se confirma en el primer tick que alcanza el objetivo completo; no espera al cierre de un movimiento físico. No se reabre.

---

## 2. Q1 — CONCURRENCIA L1 / L2

Decisión de Javier: el 1 local de 16:19 abre una **lectura secundaria L2**, no sustituye L1.

```text
L1 = lectura principal / módulo grande
L2 = única lectura local / mini módulo actual
```

Cada lectura conserva:

- referencias separadas;
- genealogía separada;
- módulo separado;
- objetivo TT separado;
- `structural_time` y `knowledge_time` propios.

Límites:

- máximo dos escalas activas;
- no se abre una tercera por encadenamiento;
- un AUT local no cambia automáticamente la dominancia;
- el cambio de dominancia exige una transición estructural posterior justificada;
- una secundaria válida no se elimina por la dominante;
- la dominante no se impone por producir AUT.

---

## 3. Q2 — VIDA DE 2 Y 3

Decisión de Javier: 2 y 3 se confirman en el primer tick válido, pero **continúan actualizando su extremo** mientras conserven la misma finalidad funcional.

Caso local verificado:

```text
L2 16:19–16:24
1 bajista: 29850,0 → 29842,5 = 7,5
2:         29844,8 → 29832,5 = 10,8  (CONFIRMED)
3 final:   29830,3                 (CONFIRMED)
módulo:    29850,0 → 29830,3 = 19,7
A:         29830,3 → 29850,8 = 20,5
nuevo 1:   29830,3 → 29850,8
```

El lector corregido reproduce 19,7 / 20,5; el lector anterior daba 16,7 / 17,5 por congelar 2 y 3 en el tick de confirmación.

---

## 4. Q3 — FRONTERA B / AUT

Decisión de Javier: la regla exclusiva de B es:

```text
B <  100 % de A                  → B candidata
100 % <= B <= 127 % de A + 0,25  → B Grande
B >  127 % de A + 0,25           → AUT inmediato
```

- Superar la base del módulo **no** confirma AUT por B.
- La superación de la base del módulo pertenece a A Grande usada como tendencia y a C Grande usada como tendencia.
- Si un tick cruza el 100 % y también el límite AUT: se registran ambos cruces; estado final = AUT; no se retrasa AUT; no se mantiene B Grande después de AUT.
- Caso 16:23: A = 8,0; B = 9,8 = 122,5 %; límite AUT = 10,41 → **B Grande, no AUT**.
- La lectura v005 de 16:23 que clasifica AUT queda `HUMAN_READING_SUPERSEDED_BY_LATER_UNIVERSAL_RULE`. No se modifica el árbol para reproducirla.

---

## 5. REGLA DE A — NO APROBADA EN SU FORMA RESTRICTIVA

No se adopta como canon:

```text
A se confirma solo si B alcanza el 100 %
A se confirma solo si A supera la base del módulo
```

Se conserva:

```text
CONTRARY_MOVE_PENDING
→ A_CONFIRMED
o
→ ABSORBED_IN_ACTIVE_FUNCTION
```

La autonomía de A se evalúa por:

- posición estructural;
- claridad;
- continuidad;
- independencia respecto de la función dominante;
- finalidad;
- conservación de origen y extremo;
- transición posterior;
- contexto entre velas.

Sin umbral fijo. Sin 2, 6, 12, 20 puntos ni 35 %.

Hechos que sí son confirmaciones fuertes, pero no las únicas:

- B alcanza el 100 % → confirmación retrospectiva adicional de A y de B Grande;
- A supera la base del módulo → A usada como tendencia → AUT directo → nuevo 1.

La condición mínima suficiente para confirmar A antes del 100 % de B queda **abierta** (ver pregunta Q-AUT).

---

## 6. REGLAS ABIERTAS QUE NO SE CIERRAN EN v2.20

| ID | Concepto | Estado |
|---|---|---|
| OPEN-INIT-01 | Ciclo inicial de 1 en el primer tick del feed | `PENDIENTE_JAVIER` |
| OPEN-3-50 | 50 % exacto de 2 para conservar o invalidar 3 | `PENDIENTE_JAVIER` |
| OPEN-CUT-01 | Significado funcional propio de CUT y su referencia exacta | `PENDIENTE_JAVIER` |
| OPEN-FT-01 | Condición de confirmación estructural de FT | `PENDIENTE_JAVIER` |
| OPEN-AUT-A | Condición mínima de autonomía de A antes del 100 % de B | `PENDIENTE_JAVIER` |

No se inventa respuesta. No se congela el árbol con estas reglas abiertas.

---

## 7. INVARIANTES DE LA REVISIÓN

1. El Python no prevalece sobre el árbol.
2. No se usan horas, precios, velas ni fixtures como reglas.
3. No se usa información futura.
4. `structural_time` y `knowledge_time` son campos distintos.
5. Máximo dos escalas activas.
6. No se añaden funciones ontológicas: solo 1, 2, 3, A, B, C, AUT, CUT.
7. TT y FT son patrones, no funciones.
8. A/C usadas como tendencia son razones de transición, no funciones nuevas.
9. Una política experimental no valida el árbol ni se congela.
10. Un gap no inventa ticks ni precios internos.

---

## 8. IMPACTO EN PRUEBAS

- Prueba de plano: 0,10 y 0,20 planos; 0,25 no plano.
- Prueba de 2: sin 100 % al cierre → IMPOSSIBLE; el módulo por descarte usa el extremo final de 3, no el tick de confirmación.
- Prueba de 3: `knowledge_time` en el primer tick que supera el extremo de 2; `extreme_3` puede ampliarse después.
- Prueba B/AUT: 100 % → B Grande; 127 % + 0,25 inclusive → B Grande; por encima → AUT en el mismo tick; base del módulo no da AUT por B.
- Prueba AUT: nuevo 1 en el mismo tick, con origen y dirección heredados.
- Prueba de concurrencia: L1 y L2 con referencias separadas; máximo dos escalas; AUT local no cambia dominancia.
- Prueba de gap: A/B/AUT implícitas, nuevo 1 desde la apertura, sin ticks inventados.

---

## 9. TRAZABILIDAD

Fuentes aplicadas, en orden:

1. Decisión expresa de Javier del Checkpoint 1 (Q1, Q2, Q3).
2. Parches v2.13–v2.19.
3. Canon activo v2.19.
4. Reglas cerradas.
5. Lecturas humanas v005 (solo como verificación; 16:23 sustituida).
6. Evidencia física del tickfeed.
7. Lector experimental v2 (no autoridad).

**Este documento no es el árbol congelado. Es la base de la revisión que Javier debe aprobar antes de la Fase C.**
