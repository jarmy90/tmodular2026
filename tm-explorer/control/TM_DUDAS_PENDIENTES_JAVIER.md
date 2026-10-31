# TM — DUDAS PENDIENTES DE JAVIER

- **Documento:** `control/TM_DUDAS_PENDIENTES_JAVIER.md`
- **Versión:** 1.0
- **Fecha:** 2026-10-19
- **Autoridad:** Javier Armada López
- **Estado:** BLOQUE 1 — 5 preguntas bloqueantes.
- **Regla:** máximo 5 preguntas por bloque. No se avanza en las ramas dependientes hasta recibir respuesta.
- **Referencia:** `TM_ARBOL_CANONICO_COMPLETO_v1.md`.

---

## BLOQUE 1 — 5 PREGUNTAS BLOQUEANTES

### DUDA-J01 — Apertura de L2 y L3

**Nodo afectado:** N-028, N-029.  
**Pregunta:** ¿Qué regla TM expresa autoriza abrir una segunda o tercera lectura?

- **A)** Una vela que alcanza AUT puede abrir automáticamente L2 como nuevo 1 local / TT pequeño, aunque no haya corrección de módulo. L3 se abre solo si las tres lecturas siguen siendo matemáticamente válidas.
- **B)** L2/L3 solo se abren por reclasificación expresa de módulo o 1 conjunto; una vela con AUT no abre L2 por sí sola.
- **C)** Solo Javier identifica la segunda/tercera lectura escena por escena; no existe regla automática de apertura.

**Consecuencia de A:** la lectura pequeña de la vela 3 (TT `29187,40`) sería L2 y podría convivir con L1.  
**Consecuencia de B:** la lectura pequeña queda como movimiento interno de L1 hasta que exista reclasificación; no se declara L2.  
**Consecuencia de C:** el motor no abre L2/L3; toda segunda lectura queda `PENDIENTE_JAVIER`.

**Estado:** `PENDIENTE_JAVIER`.

---

### DUDA-J02 — Composición general del módulo

**Nodo afectado:** N-012.  
**Pregunta:** ¿La composición general del módulo es siempre 1+2 o admite otros casos?

- **A)** Siempre 1+2; el módulo por descarte de la vela anterior no es regla general.
- **B)** Puede ser de una sola vela o de la vela anterior por descarte, con su A Grande contraria, cuando no hay módulo claro.
- **C)** Depende de la escena; Javier debe indicar en cada caso qué velas forman el módulo.

**Consecuencia de A:** H17 queda como provisional y no se implementa módulo por descarte.  
**Consecuencia de B:** se cierra la regla general del módulo y se puede calcular TT en todos los casos.  
**Consecuencia de C:** todo módulo no regular queda `PENDIENTE_JAVIER`.

**Estado:** `PENDIENTE_JAVIER` (DUDA-009 / H17).

---

### DUDA-J03 — Prioridad cuando dos o tres lecturas alcanzan nivel en el mismo tick

**Nodo afectado:** N-030.  
**Pregunta:** Si L1, L2 y L3 alcanzan un nivel en el mismo tick, ¿qué lectura prevalece?

- **A)** Prevalece L1 por ser la lectura de referencia; L2/L3 se resuelven después.
- **B)** Prevalece la lectura con mayor coherencia matemática, aunque no sea L1; si hay empate, se conservan todas.
- **C)** No hay prioridad automática: las tres se registran y Javier resuelve la escena.

**Consecuencia de A:** L1 bloquea a L2/L3 en el mismo tick; puede perder una lectura válida.  
**Consecuencia de B:** se necesita una definición exacta de “mayor coherencia” y desempate.  
**Consecuencia de C:** el motor no decide; la escena queda `PENDIENTE_JAVIER`.

**Estado:** `PENDIENTE_JAVIER` (P5).

---

### DUDA-J04 — Condición exacta de `C = nuevo 1`

**Nodo afectado:** N-025, N-034.  
**Pregunta:** ¿Cuándo se confirma que C Grande, sin alcanzar CUT, pasa a ser nuevo 1?

- **A)** C se convierte en nuevo 1 cuando cierra la referencia de B/A sin superar el final de A y el precio continúa en la dirección de C.
- **B)** C se convierte en nuevo 1 solo cuando alcanza una referencia de expansión propia, no por el simple cierre de la referencia anterior.
- **C)** C = nuevo 1 solo se reconoce por escena, después de que Javier lo valide; no hay condición automática.

**Consecuencia de A:** se puede cerrar la rama C sin CUT con una regla de cierre.  
**Consecuencia de B:** hace falta fijar la referencia de expansión propia de C.  
**Consecuencia de C:** `C = nuevo 1` queda `PENDIENTE_JAVIER` y no se implementa.

**Estado:** `PENDIENTE_JAVIER` (H1 / PR-e).

---

### DUDA-J05 — Regla matemática completa de FT

**Nodo afectado:** N-026.  
**Pregunta:** ¿Qué condiciones exactas confirman FT después de un TT?

- **A)** FT se confirma cuando, tras TT, hay pérdida de velocidad y un movimiento contrario que supera el final de A o una referencia TM explícita.
- **B)** FT se confirma por un retroceso mínimo medido en puntos o porcentaje del último recorrido, además de la pérdida de velocidad.
- **C)** FT solo se reconoce por escena; no se fija una fórmula general todavía.

**Consecuencia de A:** se necesita definir “pérdida de velocidad” y la referencia exacta.  
**Consecuencia de B:** se necesitan umbrales numéricos y ventana de medición.  
**Consecuencia de C:** FT queda fuera del motor determinista y se marca `PENDIENTE_JAVIER`.

**Estado:** `PENDIENTE_JAVIER` (P6).

---

## COLA NO ENVIADA — DUDAS SECUNDARIAS

Estas dudas no forman parte del bloque de 5 y no deben enviarse hasta cerrar el bloque anterior.

- `DUDA-S01` — Umbral numérico entre ruido y movimiento TM (PR-g).
- `DUDA-S02` — ¿Un gap a favor de 1 confirma AUT o solo deja TT pendiente? (N-003).
- `DUDA-S03` — Tick exacto de confirmación de A/B/C Grande (P3).
- `DUDA-S04` — Serie de precio definitiva: Bid/Ask/Last/medio (P2).
- `DUDA-S05` — TT: ¿alcanzar exactamente el 100 % o exigir superación estricta? (N-039).

---

## CONTROL DE RESPUESTAS

| Duda | Respuesta de Javier | Fecha | Decisión | Nodos desbloqueados |
|---|---|---|---|---|
| DUDA-J01 |  |  |  | N-028, N-029 |
| DUDA-J02 |  |  |  | N-012 |
| DUDA-J03 |  |  |  | N-030 |
| DUDA-J04 |  |  |  | N-025, N-034 |
| DUDA-J05 |  |  |  | N-026 |
