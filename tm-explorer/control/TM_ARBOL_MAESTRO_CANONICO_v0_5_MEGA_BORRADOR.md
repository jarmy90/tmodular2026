# TM · ÁRBOL MAESTRO CANÓNICO

Versión 0.5 MEGA BORRADOR. Cobertura global para prueba, preguntas y corrección. No apto todavía para ejecución automática ni para operar.

## 0. Regla constitucional

```text
CLASIFICACIÓN VÁLIDA = lectura + estado anterior + cronología + referencia + precondiciones + transición + resultado.
Si falta una pieza, el motor registra HECHO_SIN_REGLA y no inventa una función. En la versión final HECHO_SIN_REGLA deberá ser cero.
```

## 1. Leyenda de certeza

- CONFIRMADO_JAVIER: regla expresamente cerrada por Javier.

- DOCUMENTADO: aparece en fuentes, pendiente de prueba experta.

- PROPUESTA_CONTROLADA: cierre técnico provisional para poder probar el árbol completo.

- PENDIENTE_JAVIER: pregunta concreta, no programable.

- PROHIBIDO: transición incompatible con las precondiciones.

## 2. Ontología completa provisional

```text
FUNCIONES: 1 | 2 | 3 | A | B | AUT | C
PATRONES: TT | FT
ESTRUCTURAS: MÓDULO | LECTURA
EVENTOS: GAP | AUTOCORTE | CUT | OBJETIVO_TT | CONFIRMACIÓN_FT
CALIFICADORES INTERNOS: CANDIDATO | CONFIRMADO | CANCELADO | RECLASIFICADO | INTEGRADO
```

## 3. Datos mínimos por tick

- timestamp

- bid/ask o precio de referencia acordado

- OHLC de vela activa

- Open actual y Close anterior

- dirección y extremo de cada lectura

- niveles 0, 50, 100, 127 y 127+0,25

- objetivo TT

- referencia CUT

- referencia FT

- historial inmutable de eventos

## 4. Orden universal de evaluación

```text
1. Registrar tick.
2. Detectar nueva vela.
3. Si nueva vela, evaluar GAP antes de 2.
4. Actualizar extremos de cada lectura.
5. Detectar niveles cruzados en el tick.
6. Procesar todos los niveles cruzados en orden geométrico.
7. Aplicar transición por lectura, sin mezclar referencias.
8. Abrir lectura adicional solo por regla expresa.
9. Registrar reclasificación sin borrar historial.
10. Emitir etiqueta visible y trazabilidad.
```

## 5. Árbol raíz y nacimiento de lectura

### TM-ROOT-001 · Sin lectura activa

**Estado:** `PROPUESTA_CONTROLADA`

```text
ORIGEN: SIN_LECTURA
EVENTO: primer recorrido observable
PRECONDICIONES: datos suficientes y referencia inicial autorizada
SI SE CUMPLE: abrir L1 con 1 candidato
SI NO SE CUMPLE: seguir acumulando ticks
DESTINO: UNO_CANDIDATO
PROHIBICIONES: no inventar dirección por color de vela
PRUEBAS: inicio alcista; inicio bajista; vela incompleta
PREGUNTA: Q-001: regla matemática definitiva de nacimiento del primer 1
```

### TM-ROOT-002 · Nueva lectura adicional

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: L1/L2 activa
EVENTO: posible recorrido independiente
PRECONDICIONES: regla explícita de apertura
SI SE CUMPLE: abrir primer slot libre
SI NO SE CUMPLE: integrar en lecturas existentes
DESTINO: Ln activa
PROHIBICIONES: abrir por apariencia visual
PRUEBAS: caso abre L2; caso no abre L2
PREGUNTA: Q-002: catálogo completo de reglas que abren L2/L3
```

## 6. Estado 1

### TM-1-001 · 1 continúa

**Estado:** `PROPUESTA_CONTROLADA`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: extensión en dirección de 1
PRECONDICIONES: no nace función posterior
SI SE CUMPLE: actualizar extremo y rango de 1
SI NO SE CUMPLE: mantener extremo
DESTINO: UNO_CONFIRMADO
PROHIBICIONES: crear otro 1 por cada vela
PRUEBAS: extensión misma vela; varias velas
```

### TM-1-002 · Apertura siguiente con gap

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: Open actual != Close anterior
PRECONDICIONES: nueva vela
SI SE CUMPLE: prohibir 2 y saltar a árbol GAP
SI NO SE CUMPLE: n/a
DESTINO: GAP_EVALUADO
PROHIBICIONES: evaluar plano o 2
PRUEBAS: gap 1 tick; gap varios puntos
```

### TM-1-003 · Sin gap y salida en plano

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: Open actual = Close anterior
PRECONDICIONES: nueva vela y sin cola observable >0,25 antes de objetivo
SI SE CUMPLE: abrir DOS_CANDIDATO
SI NO SE CUMPLE: si hay cola, prohibir 2
DESTINO: DOS_CANDIDATO
PROHIBICIONES: confirmar 2 solo por color
PRUEBAS: plano exacto; cola 0,25; cola 0,50
```

### TM-1-004 · No 2 por cola

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: cola de base >0,25 antes de confirmar 2
PRECONDICIONES: sin gap
SI SE CUMPLE: cancelar 2 y evaluar ruta A
SI NO SE CUMPLE: si cola <=0,25 mantener candidato
DESTINO: A_CANDIDATA
PROHIBICIONES: recrear 2 después
PRUEBAS: cola antes/después del objetivo
```

### TM-1-005 · No 2 por gap

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: UNO_CONFIRMADO
EVENTO: gap cualquiera
PRECONDICIONES: nueva vela
SI SE CUMPLE: 2 prohibido
SI NO SE CUMPLE: n/a
DESTINO: RUTA_GAP
PROHIBICIONES: llamar 2 al recorrido posterior
PRUEBAS: gap a favor; gap contrario
```

## 7. Estado 2

### TM-2-001 · 2 candidato progresa

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: avance en dirección de 1
PRECONDICIONES: sin invalidación previa
SI SE CUMPLE: actualizar recorrido 2
SI NO SE CUMPLE: mantener
DESTINO: DOS_CANDIDATO
PROHIBICIONES: confirmar antes de medida
PRUEBAS: <100; =100; >100
PREGUNTA: Q-003: medida exacta y anclajes de 2
```

### TM-2-002 · 2 confirmado

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: alcanza medida exigida
PRECONDICIONES: plano, sin gap, sin cola invalidante previa
SI SE CUMPLE: confirmar 2
SI NO SE CUMPLE: seguir candidato
DESTINO: DOS_CONFIRMADO
PROHIBICIONES: borrar 2 por hechos posteriores
PRUEBAS: frontera exacta y salto
```

### TM-2-003 · Retroceso después de confirmar 2

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: DOS_CONFIRMADO
EVENTO: movimiento contrario
PRECONDICIONES: 2 ya confirmado
SI SE CUMPLE: conservar 2 y abrir evaluación de 3
SI NO SE CUMPLE: n/a
DESTINO: TRES_CANDIDATO
PROHIBICIONES: borrar 2
PRUEBAS: retroceso pequeño; grande
```

### TM-2-004 · Cambio de vela con 2 candidato

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: DOS_CANDIDATO
EVENTO: cierra vela sin confirmar
PRECONDICIONES: no hubo invalidación
SI SE CUMPLE: conservar/cancelar según decisión
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir cancelación
PRUEBAS: varias velas
PREGUNTA: Q-004: 2 puede confirmarse en varias velas
```

## 8. Estado 3 y módulo

### TM-3-001 · Retroceso válido para 3

**Estado:** `DOCUMENTADO`

```text
ORIGEN: DOS_CONFIRMADO
EVENTO: retroceso dentro de franja válida
PRECONDICIONES: 2 confirmado
SI SE CUMPLE: seguir TRES_CANDIDATO
SI NO SE CUMPLE: fallar 3
DESTINO: TRES_CANDIDATO
PROHIBICIONES: anticipar 3
PRUEBAS: 0; 50; >50
PREGUNTA: Q-005: límites exactos del retroceso de 3
```

### TM-3-002 · 3 confirmado

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_CANDIDATO
EVENTO: precio retoma dirección de 2 y supera/toca extremo
PRECONDICIONES: retroceso válido
SI SE CUMPLE: confirmar 3
SI NO SE CUMPLE: mantener candidato
DESTINO: TRES_CONFIRMADO
PROHIBICIONES: confirmar por color
PRUEBAS: toca; supera 1 tick
PREGUNTA: Q-006: tocar o superar extremo de 2
```

### TM-3-003 · 3 falla

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_CANDIDATO
EVENTO: incumple regla de 3
PRECONDICIONES: 1 y 2 confirmados
SI SE CUMPLE: consolidar 1+2 como módulo y opuesto como A Grande
SI NO SE CUMPLE: seguir 3
DESTINO: MODULO_CONFIRMADO + A
PROHIBICIONES: crear módulo si nunca hubo 2
PRUEBAS: fallo por profundidad; fallo temporal
```

### TM-3-004 · 3 confirmado y continuidad

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: TRES_CONFIRMADO
EVENTO: extensión posterior
PRECONDICIONES: 3 confirmado
SI SE CUMPLE: definir siguiente estructura
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir A automáticamente
PRUEBAS: extensión/giro
PREGUNTA: Q-007: consecuencia exacta después de 3
```

## 9. Módulo y A

### TM-MOD-001 · Módulo 1+2

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TRES_FALLIDO
EVENTO: opuesto tras fallo de 3
PRECONDICIONES: 1 y 2 confirmados
SI SE CUMPLE: fijar rango del módulo y A Grande
SI NO SE CUMPLE: n/a
DESTINO: A_EN_CURSO
PROHIBICIONES: formar módulo sin 2
PRUEBAS: caso estándar
```

### TM-MOD-002 · Módulo reclasificado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: varios movimientos previos
EVENTO: retroceso posterior permite integración
PRECONDICIONES: regla de reclasificación satisfecha
SI SE CUMPLE: crear módulo conjunto conservando eventos
SI NO SE CUMPLE: mantener lecturas
DESTINO: MODULO_RECLASIFICADO
PROHIBICIONES: borrar eventos
PRUEBAS: varias velas
PREGUNTA: Q-008: catálogo completo de reclasificación
```

### TM-A-001 · A se extiende

**Estado:** `DOCUMENTADO`

```text
ORIGEN: A_EN_CURSO
EVENTO: nuevo extremo en dirección de A
PRECONDICIONES: sin B opuesta confirmable
SI SE CUMPLE: actualizar final y rango de A
SI NO SE CUMPLE: mantener
DESTINO: A_EN_CURSO
PROHIBICIONES: congelar A demasiado pronto
PRUEBAS: extensión 1 tick/multivela
```

### TM-A-002 · Nace B candidata

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: A_EN_CURSO
EVENTO: movimiento contrario a A
PRECONDICIONES: A posee inicio/final/rango
SI SE CUMPLE: abrir B candidata
SI NO SE CUMPLE: mantener A
DESTINO: B_CANDIDATA
PROHIBICIONES: llamar B confirmada antes del 100
PRUEBAS: retorno 10/99/100
```

## 10. B candidata, B confirmada y AUT

### TM-B-001 · B por debajo del 100 %

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: avance <100 % de A
PRECONDICIONES: B opuesta a A
SI SE CUMPLE: seguir B candidata
SI NO SE CUMPLE: n/a
DESTINO: B_CANDIDATA
PROHIBICIONES: llamar B Grande
PRUEBAS: 99,75 %
```

### TM-B-002 · B alcanza 100 %

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: alcanza 100 %
PRECONDICIONES: no supera 127 %+0,25
SI SE CUMPLE: confirmar B Grande
SI NO SE CUMPLE: seguir candidata
DESTINO: B_CONFIRMADA
PROHIBICIONES: exigir cierre
PRUEBAS: 100 exacto
```

### TM-B-003 · B entre 100 y límite AUT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CONFIRMADA
EVENTO: extensión sin superar 127 %+0,25
PRECONDICIONES: B confirmó 100
SI SE CUMPLE: mantener B confirmada
SI NO SE CUMPLE: n/a
DESTINO: B_CONFIRMADA
PROHIBICIONES: llamar AUT
PRUEBAS: 110;127; límite exacto
```

### TM-B-004 · B supera límite AUT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B candidata o confirmada
EVENTO: supera 127 %+0,25
PRECONDICIONES: A válida
SI SE CUMPLE: dejar B y confirmar AUT inmediato
SI NO SE CUMPLE: mantener B
DESTINO: AUT_CONFIRMADO
PROHIBICIONES: esperar otra vela
PRUEBAS: salto directo 90→130
```

### TM-B-005 · Giro de B candidata antes del 100

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: B_CANDIDATA
EVENTO: precio vuelve hacia A
PRECONDICIONES: B <100
SI SE CUMPLE: aplicar decisión experta
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: llamar C
PRUEBAS: giro 20/80/99
PREGUNTA: Q-009: absorción, nueva A o reclasificación
```

### TM-B-006 · B confirmada gira

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B_CONFIRMADA
EVENTO: movimiento contrario a B
PRECONDICIONES: B alcanzó 100 sin AUT
SI SE CUMPLE: clasificar C inmediatamente
SI NO SE CUMPLE: n/a
DESTINO: C_EN_CURSO
PROHIBICIONES: llamar C candidata
PRUEBAS: giro 1 tick
```

## 11. C y CUT

### TM-C-001 · C se extiende

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: C_EN_CURSO
EVENTO: avance en dirección contraria a B
PRECONDICIONES: B confirmada misma lectura
SI SE CUMPLE: actualizar C
SI NO SE CUMPLE: n/a
DESTINO: C_EN_CURSO
PROHIBICIONES: usar B de otra lectura
PRUEBAS: avance parcial
```

### TM-C-002 · CUT

**Estado:** `DOCUMENTADO`

```text
ORIGEN: C_EN_CURSO
EVENTO: C alcanza final de A
PRECONDICIONES: misma lectura
SI SE CUMPLE: confirmar CUT
SI NO SE CUMPLE: seguir C
DESTINO: CUT_CONFIRMADO
PROHIBICIONES: confirmar por color
PRUEBAS: toca/supera
PREGUNTA: Q-010: CUT evento o función; tocar o superar
```

### TM-C-003 · C no alcanza CUT y gira

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: C_EN_CURSO
EVENTO: movimiento vuelve hacia B
PRECONDICIONES: C < final A
SI SE CUMPLE: aplicar decisión experta
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: inventar función
PRUEBAS: múltiples profundidades
PREGUNTA: Q-011: tratamiento completo de C sin CUT
```

### TM-C-004 · Después de CUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: CUT_CONFIRMADO
EVENTO: continuidad o giro
PRECONDICIONES: CUT confirmado
SI SE CUMPLE: definir siguiente lectura
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: cerrar todo automáticamente
PRUEBAS: continúa/gira
PREGUNTA: Q-012: consecuencia posterior a CUT
```

## 12. AUT y TT

### TM-AUT-001 · AUT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: B candidata o confirmada
EVENTO: supera 127 %+0,25
PRECONDICIONES: A válida
SI SE CUMPLE: activar TT posible
SI NO SE CUMPLE: n/a
DESTINO: TT_POSIBLE
PROHIBICIONES: mantener B vigente
PRUEBAS: salto multinivel
```

### TM-TT-001 · TT progresa

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: TT_POSIBLE
EVENTO: expansión desde final A hacia objetivo
PRECONDICIONES: AUT misma lectura
SI SE CUMPLE: actualizar porcentaje
SI NO SE CUMPLE: n/a
DESTINO: TT_POSIBLE
PROHIBICIONES: llamar TT confirmado
PRUEBAS: 1–99,75 %
```

### TM-TT-002 · TT confirmado

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: TT_POSIBLE
EVENTO: alcanza 100 %
PRECONDICIONES: objetivo = final A ± rango módulo
SI SE CUMPLE: confirmar TT y convertir recorrido culminante en nuevo 1
SI NO SE CUMPLE: seguir posible
DESTINO: TT_CONFIRMADO + UNO_CONFIRMADO
PROHIBICIONES: crear A/B/AUT propios sin lectura
PRUEBAS: 100 exacto/salto
```

### TM-TT-003 · TT falla antes del 100

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TT_POSIBLE
EVENTO: precio toca/corta final A antes de objetivo
PRECONDICIONES: AUT activo
SI SE CUMPLE: cancelar TT y aplicar reclasificación
SI NO SE CUMPLE: mantener TT
DESTINO: TT_FALLIDO
PROHIBICIONES: borrar AUT
PRUEBAS: fallo temprano/tardío
PREGUNTA: Q-013: condición exacta de fallo TT
```

### TM-TT-004 · AUT, 1 y TT pequeño simultáneos

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: AUT_CONFIRMADO
EVENTO: recorrido cumple referencias concurrentes
PRECONDICIONES: lecturas explícitas
SI SE CUMPLE: registrar todos por lectura
SI NO SE CUMPLE: n/a
DESTINO: ESTADOS_CONCURRENTES
PROHIBICIONES: fusionar etiquetas
PRUEBAS: caso simultáneo
```

## 13. FT

### TM-FT-001 · FT prohibido sin TT

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: cualquier
EVENTO: movimiento contrario
PRECONDICIONES: TT no confirmado
SI SE CUMPLE: no FT
SI NO SE CUMPLE: n/a
DESTINO: SIN_FT
PROHIBICIONES: anticipar FT
PRUEBAS: caso negativo
```

### TM-FT-002 · FT candidato

**Estado:** `DOCUMENTADO`

```text
ORIGEN: TT_CONFIRMADO
EVENTO: movimiento contrario claro
PRECONDICIONES: TT confirmado y posible pérdida de velocidad
SI SE CUMPLE: abrir FT candidato
SI NO SE CUMPLE: integrar micromovimiento
DESTINO: FT_CANDIDATO
PROHIBICIONES: confirmar por color
PRUEBAS: mismo minuto/multivela
PREGUNTA: Q-014: umbral matemático de movimiento claro y pérdida de velocidad
```

### TM-FT-003 · FT confirmado

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: FT_CANDIDATO
EVENTO: alcanza referencia FT
PRECONDICIONES: precondiciones completas
SI SE CUMPLE: confirmar FT
SI NO SE CUMPLE: mantener candidato
DESTINO: FT_CONFIRMADO
PROHIBICIONES: usar referencia no definida
PRUEBAS: frontera
PREGUNTA: Q-015: objetivo, inicio, cancelación y confirmación FT
```

### TM-FT-004 · Después de FT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: FT_CONFIRMADO
EVENTO: continuidad/giro
PRECONDICIONES: FT confirmado
SI SE CUMPLE: definir nuevo ciclo
SI NO SE CUMPLE: n/a
DESTINO: PENDIENTE
PROHIBICIONES: asumir nuevo 1
PRUEBAS: dos direcciones
PREGUNTA: Q-016: consecuencia posterior a FT
```

## 14. Árbol completo de gap

### TM-GAP-001 · Gap a favor de 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: Open avanza en dirección de 1
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: RUTA_GAP_FAVOR
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-017: funciones implícitas exactas
```

### TM-GAP-002 · Gap contrario a 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: Open avanza contra 1
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: A_INICIADA_POR_GAP
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-018: anclajes exactos de A por gap
```

### TM-GAP-003 · Gap cruza 100 de B

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura atraviesa nivel 100
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: B_CONFIRMADA_O_AUT
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-019: orden de niveles implícitos
```

### TM-GAP-004 · Gap cruza AUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura supera 127 %+0,25
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: AUT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-020: AUT por gap y objetivo TT
```

### TM-GAP-005 · Gap cruza objetivo TT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura supera objetivo 100 TT
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: TT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-021: confirmación inmediata y precio de nuevo 1
```

### TM-GAP-006 · Gap cruza CUT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura cruza final de A durante C
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: CUT_CONFIRMADO
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-022: CUT por gap
```

### TM-GAP-007 · Gap cruza nivel FT

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lectura activa
EVENTO: apertura cruza referencia FT
PRECONDICIONES: nueva vela; evaluar gap primero
SI SE CUMPLE: procesar niveles cruzados en orden
SI NO SE CUMPLE: n/a
DESTINO: FT_CONFIRMADO_O_PENDIENTE
PROHIBICIONES: crear 2
PRUEBAS: gap mínimo; gap multinivel
PREGUNTA: Q-023: FT por gap
```

## 15. Saltos multinivel en un tick

```text
REGLA PROPUESTA: si un tick salta varios umbrales, registrar todos los umbrales causales atravesados en orden, pero dejar como estado vigente el último estado válido. No exigir permanencia de un tick en estados intermedios.
```

- B candidata → AUT: cruza 100 y AUT.

- TT posible → más allá del objetivo: cruza 100 TT.

- C → más allá de CUT: cruza final A.

- 2 candidato → extremo y retroceso: orden intratick no observable.

La última combinación exige política de datos cuando dos precios extremos aparecen sin orden intratick fiable: `PENDIENTE_JAVIER` y no reconstrucción inventada.

## 16. Concurrencia L1/L2/L3

### TM-CON-001 · Actualizar lecturas

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: 1–3 lecturas activas
EVENTO: nuevo tick
PRECONDICIONES: cada lectura conserva referencias
SI SE CUMPLE: evaluar el tick en todas por separado
SI NO SE CUMPLE: n/a
DESTINO: lecturas actualizadas
PROHIBICIONES: mezclar niveles
PRUEBAS: dos eventos simultáneos
```

### TM-CON-002 · Abrir lectura

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: lecturas activas
EVENTO: evento de apertura
PRECONDICIONES: regla expresa
SI SE CUMPLE: crear Ln con padre/regla/tick
SI NO SE CUMPLE: no abrir
DESTINO: Ln
PROHIBICIONES: abrir por apariencia
PRUEBAS: L2/L3
PREGUNTA: Q-024: lista exhaustiva de disparadores
```

### TM-CON-003 · Capacidad máxima

**Estado:** `DOCUMENTADO`

```text
ORIGEN: L1/L2 activas
EVENTO: tercera posibilidad
PRECONDICIONES: excepcional y justificada
SI SE CUMPLE: abrir L3
SI NO SE CUMPLE: integrar/invalidar
DESTINO: L3 o no
PROHIBICIONES: más de 3
PRUEBAS: tres lecturas
PREGUNTA: Q-025: máximo absoluto y prioridad
```

### TM-CON-004 · Mismo movimiento en dos lecturas

**Estado:** `CONFIRMADO_JAVIER`

```text
ORIGEN: L1/L2
EVENTO: un recorrido cumple papeles distintos
PRECONDICIONES: referencias separadas
SI SE CUMPLE: registrar ambos papeles
SI NO SE CUMPLE: n/a
DESTINO: doble etiqueta por lectura
PROHIBICIONES: fusionar lecturas
PRUEBAS: TT L1 y 1 L2
```

### TM-CON-005 · Cerrar/integrar lectura

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: múltiples lecturas
EVENTO: convergencia o incompatibilidad
PRECONDICIONES: regla de integración
SI SE CUMPLE: marcar integrada/invalidada conservando historial
SI NO SE CUMPLE: mantener
DESTINO: LECTURA_CERRADA
PROHIBICIONES: borrar
PRUEBAS: casos variados
PREGUNTA: Q-026: criterios exhaustivos de cierre
```

## 17. Reclasificación

### TM-REC-001 · Velas previas pasan a módulo

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: retroceso revela 1+2 conjunto
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-027: condiciones exactas
```

### TM-REC-002 · Velas previas pasan a 1 conjunto

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: retroceso revela unidad mayor
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-028: condiciones exactas
```

### TM-REC-003 · Movimiento candidato absorbido

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: no alcanza confirmación y retorna
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-029: reglas por estado
```

### TM-REC-004 · AUT simultáneo con 1

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: AUT cumple nacimiento de 1
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-030: referencias
```

### TM-REC-005 · TT pequeño dentro de TT mayor

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: módulos anidados
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-031: anidamiento y prioridad
```

### TM-REC-006 · Lectura alternativa pasa a principal

**Estado:** `PENDIENTE_JAVIER`

```text
ORIGEN: historial activo
EVENTO: evidencia posterior
PRECONDICIONES: cronología preservada
SI SE CUMPLE: crear evento RECLASIFICACIÓN y nuevas relaciones
SI NO SE CUMPLE: mantener
DESTINO: RECLASIFICADO
PROHIBICIONES: editar/borrar pasado
PRUEBAS: caso positivo/negativo
PREGUNTA: Q-032: criterio de prioridad
```

## 18. Cambio de vela

```text
La frontera temporal no crea por sí sola una función. Al abrir vela: registrar cierre, apertura, gap y lecturas. Las funciones pueden comenzar en una vela y terminar en otras. TT y FT pueden coexistir dentro de una misma vela si las referencias se alcanzan cronológicamente.
```

- Cambio de vela con `1`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `2 candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `2 confirmado`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `3 candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `A`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `B candidata`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `B confirmada`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `AUT/TT posible`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `C`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

- Cambio de vela con `FT candidato`: conservar estado salvo regla específica de gap, cancelación o reclasificación. Donde la regla específica no esté cerrada, queda asociada a prueba y pregunta.

## 19. Transiciones prohibidas

- C sin B confirmada en la misma lectura.

- CUT sin C válida.

- TT sin AUT.

- TT confirmado antes del 100 %.

- FT sin TT confirmado.

- 2 con gap.

- 2 con cola >0,25 previa a confirmación.

- B confirmada antes del 100 %.

- Mantener B después de superar AUT.

- Abrir L2/L3 sin regla expresa.

- Mezclar el A de L1 con el B de L2.

- Borrar historia al reclasificar.

- Inferir orden intravela usando solo OHLC cuando el orden afecta la etiqueta.

- Usar color de vela como fundamento funcional.

- Llamar ruido a un movimiento no resuelto para ocultar una rama ausente.

## 20. Matriz de cobertura de eventos

### Cobertura SIN_LECTURA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `SIN_LECTURA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 1

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `1::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 2_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 2_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `2_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 3_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura 3_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `3_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura MÓDULO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `MÓDULO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura A

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `A::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura B_CANDIDATA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CANDIDATA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura B_CONFIRMADA

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `B_CONFIRMADA::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura AUT

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `AUT::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_POSIBLE

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_POSIBLE::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura TT_FALLIDO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `TT_FALLIDO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura C

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `C::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura CUT

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `CUT::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura FT_CANDIDATO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CANDIDATO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

### Cobertura FT_CONFIRMADO

- `extensión misma dirección` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::extensión misma dirección`. La versión final no permitirá celda vacía.

- `giro contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::giro contrario`. La versión final no permitirá celda vacía.

- `toca nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::toca nivel`. La versión final no permitirá celda vacía.

- `supera nivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::supera nivel`. La versión final no permitirá celda vacía.

- `gap a favor` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::gap a favor`. La versión final no permitirá celda vacía.

- `gap contrario` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::gap contrario`. La versión final no permitirá celda vacía.

- `cambio de vela sin gap` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::cambio de vela sin gap`. La versión final no permitirá celda vacía.

- `salto multinivel` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::salto multinivel`. La versión final no permitirá celda vacía.

- `fin de datos` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::fin de datos`. La versión final no permitirá celda vacía.

- `evento simultáneo otra lectura` → aplicar nodo específico; si aún no existe decisión experta, registrar pregunta de cobertura `FT_CONFIRMADO::evento simultáneo otra lectura`. La versión final no permitirá celda vacía.

## 21. Casos mínimos de prueba obligatorios

- `SIN_LECTURA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `1`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `2_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `2_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `3_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `3_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `MÓDULO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `A`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `B_CANDIDATA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `B_CONFIRMADA`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `AUT`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_POSIBLE`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `TT_FALLIDO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `C`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `CUT`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `FT_CANDIDATO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

- `FT_CONFIRMADO`: frontera -1 tick, frontera exacta, frontera +1 tick, misma vela, varias velas, con gap, sin gap, salto multinivel, dos lecturas, tres lecturas, reclasificación sin borrado, OHLC insuficiente, caso validado 23:39–23:41.

## 22. Registro maestro de preguntas

Preguntas explícitas detectadas: Q-001 a Q-032. Además, la matriz de cobertura puede generar preguntas adicionales durante los tests. Las preguntas se resolverán después del primer test global, una por una, y cada respuesta actualizará regla, nodo y pruebas.

## 23. Criterio de promoción a v1

```text
PENDIENTE_JAVIER = 0
PROPUESTA_CONTROLADA no aprobada = 0
CONTRADICCIONES = 0
CELDAS SIN SALIDA = 0
TESTS FALLIDOS = 0
TRANSICIONES SIN PRECONDICIÓN = 0
LECTURAS ABIERTAS SIN REGLA = 0
```

## 24. Correccion experta incorporada durante pruebas

### TEST-TM-INTRAVELA-001 - Vela 20-7-7

**Estado:** `CONFIRMADO_JAVIER`

```text
UNA UNICA VELA:
1. Sube 20 puntos -> 1.
2. Por descarte -> MODULO.
3. Retrocede 7 puntos -> A.
4. Recupera 7 puntos hasta el maximo -> B al 100 % de A.
5. B queda confirmada.
6. No hay AUT porque no supera 127 % + 0,25.

SECUENCIA CANONICA:
1 -> MODULO_POR_DESCARTE -> A -> B_CONFIRMADA_100
```

**Correccion del arbol:** queda prohibido omitir el modulo por descarte en esta secuencia y saltar directamente de 1 a A.
