# Informe de fallos v0.7.3

Fecha: 2026-10-27
Alcance: ventana ciega `16:52–17:00` del feed `TM_TICKFEED_20261016_v010_USTEC_12345_USTEC_DAY16.csv`.
Referencia funcional: `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_14.md`, reglas Fase 1 y casos validados.

## 1. Evidencia del fallo

La salida ciega de v0.7.3 (`v073_blind_1652_1656_Eventos_SOLO_5_VELAS.csv`) contiene 21 eventos y ningún evento `LECTURA_CREADA`.

Hechos observados:

- Solo aparecen las lecturas heredadas `R0002` y `R0007`.
- `R0007` recibe actualizaciones `TT_REAL_EXTREME_UPDATED` hasta `29600.70` a las `16:56:39.164`.
- No se crea una lectura local para el movimiento `29667.30 -> 29602.10`.
- No se reconoce el módulo de `65.20` puntos.
- No se reconoce el TT de `29615.20` como TT de una lectura local.
- No se registra el FT posterior.
- Los GAP se emiten, pero no generan funciones ni lecturas.
- No existe narración por vela ni auditoría funcional tick a tick.

## 2. Fallos funcionales

### F1. Absorción del TT por la lectura dominante

El recorrido bajista se interpreta como extensión del TT de `R0007`. El extremo real se actualiza hasta `29600.70`, pero no se separa el submódulo `29667.30 -> 29602.10`.

Consecuencia: se pierde el módulo local de `65.20` y su TT `29615.20`.

### F2. Ausencia de nueva lectura local

La condición de nuevo `1` no se evalúa desde el origen local correcto. El motor no crea una lectura con:

- origen `29667.30`
- extremo `29602.10`
- módulo `65.20`
- A `29602.10 -> 29680.40` (`78.30`)
- B `29680.40 -> 29600.20` (`80.20`)
- TT `29615.20`

### F3. Confusión entre extensión de TT y nueva estructura

v0.7.3 conserva `R0007` como dueña del movimiento. No permite que el mismo recorrido sea FT de una lectura anterior y, a la vez, nueva `1` de una lectura local.

### F4. Cobertura no funcional

La salida no demuestra que cada movimiento tenga función, dirección, origen, extremo, lectura, padre y estado. La cobertura declarada no equivale a cobertura funcional.

### F5. Falta de auditoría y narrativa

No hay `FunctionalAudit.csv` ni `BarNarrative.csv`. No se puede reconstruir:

- qué funciones estaban activas antes y después de cada tick;
- qué lectura poseía cada movimiento;
- qué funciones se iniciaron o cerraron en cada vela;
- por qué se tomó cada decisión.

### F6. Causalidad no verificada

No se comprueba que un corte físico del feed produzca exactamente el mismo prefijo de eventos y lecturas que el feed completo truncado. Sin esa prueba no se puede afirmar que el lector sea causal.

## 3. Causas raíz

1. Un scheduler de lectura dominante decide qué estructura “merece” existir.
2. La extensión del TT se aplica sobre la misma lectura sin abrir el submódulo.
3. El origen local se toma desde el máximo/mínimo dominante, no desde el extremo del movimiento que confirma la lectura.
4. No existe una regla explícita de doble pertenencia entre FT y nuevo `1`.
5. La cobertura se calcula con contención geométrica, no con funciones y genealogía.
6. La salida no conserva el estado completo por tick ni por vela.

## 4. Correcciones aplicadas en v0.7.4

- Movement builder único con retracement del `25%` y mínimo `6.00` puntos.
- Lecturas causales creadas al confirmarse el movimiento, no al cerrar la ventana.
- Nueva lectura local por `B_CONFIRMADA_NEW1` y `A_SIGNIFICATIVA`.
- Módulo local `29667.30 -> 29602.10` con TT `29615.20`.
- A mayor que el módulo permitida; guardia provisional `A_MAX_MODULE_MULTIPLE=2.0`.
- `B_CAND` con oscilaciones internas y sin C antes de B confirmada.
- CUT con buffer de `2.00` puntos.
- Máximo de 3 lecturas activas, con archivo explícito por capacidad.
- Cobertura geométrica y funcional sobre módulo, A, B y C.
- `FunctionalAudit.csv` tick a tick y `BarNarrative.csv` por vela.
- Pruebas de prefijo causal y de la lectura clave.

## 5. Resultado de v0.7.4

- 11,120 ticks.
- 41 velas.
- 264 movimientos.
- 67 lecturas.
- 870 eventos.
- 183 patrones.
- 1,335 swings estructurales cubiertos geométrica y funcionalmente.
- 13 tests aprobados.
- Selftest interno aprobado con 8 comprobaciones.

Lectura clave del motor: `R0062` (equivalente a `R0063` del prototipo `proto10.py`):

| Campo | Valor |
|---|---:|
| Módulo | `29667.30 -> 29602.10` |
| x | `65.20` |
| A | `29602.10 -> 29680.40` |
| a | `78.30` |
| B | `29680.40 -> 29600.20` |
| b | `80.20` |
| TT | `29615.20` |
| TT 100 | `29614.20` |
| FT | `1` |
| FT time | `16:57:34.937` |
| Padre | `R0061` |
| Motivo | `B_CONFIRMADA_NEW1` |

## 6. Pendientes que no se declaran resueltos

- `post_tt_fallido`.
- Expiración exacta del FT.
- Entrada tardía después de FT.
- Límite definitivo de A respecto al módulo.
- Granularidad del módulo local de `16:45`.
- Confirmación experta sobre el buffer de CUT y el máximo de 3 activas.
- Contraste con los documentos ausentes y con `v2.13.3`.
