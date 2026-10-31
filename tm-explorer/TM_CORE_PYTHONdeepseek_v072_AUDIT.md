# Auditoría v0.7.1 -> v0.7.2

## Causa raíz
v0.7.1 trataba el estado TT como una fase única que solo sabía esperar el cruce del objetivo (`TT_PENDING`) o cerrar (`TT_OK`). Al restaurar una semilla con TT ya confirmado:

- el estado se reconstruía como `TT_PENDING`;
- no se conservaba `tt_100` como hecho histórico inmutable;
- no existía un estado post-TT que siguiera el extremo real;
- no había FT posterior ni lectura local concurrente;
- el scheduler permitía que una lectura menor se convirtiera en un segundo TT pendiente.

En 16:42 eso produjo `R0006 TT_PENDING` espurio. En 16:45 produjo una única lectura, cero patrones y el estado inicial `TT_PENDING`.

## Comparación 16:42-16:44

| Métrica | v0.7.1 | v0.7.2 |
|---|---|---|
| Lecturas | 6 | 9 |
| Patrones | 4 | 8 |
| TT principal | `R0004 TT_OK`, target 29715.50 | `R0004 TT_EXTENDING`, target 29715.50, TT100 29716.30 |
| TT menor | `R0001` A=7.50 absorbido | `R0001` A=7.50 absorbido |
| FT interna | `P0004 CANDIDATA` | `P0002` absorbida por extensión TT |
| TT espurio | `R0006 TT_PENDING` | no existe |
| `pending` | no explicado | `[]` |
| `TM_COVERAGE_OK` | no implementado | `true` |

## Comparación 16:45-16:48

| Métrica | v0.7.1 | v0.7.2 |
|---|---|---|
| Lecturas | 1 | 6 |
| Patrones | 0 | 8 |
| Eventos | SEED + GAP | 116 |
| Estado inicial | `TT_PENDING` | `TT_CONFIRMED` -> `TT_EXTENDING` |
| Extremo real | 29736.70 | 29742.30 -> 29745.10 |
| FT | inexistente | `P0001..P0005` absorbidas, `P0007 FT_CONFIRMED` 29745.10 -> 29674.60 |
| Lectura local | inexistente | `R0006` módulo/A/B/AUT/TT local |
| Activas | 1 | 2 (`R0001` + `R0006`) |
| `pending` | `[]` artificial | `[]` con cobertura `true` |

Secuencia verificada en eventos:

```text
TT_100_RESTORED              16:45:00.015  TT100 29716.30
TT_REAL_EXTREME_RESTORED     16:45:00.015  extremo 29736.70
TT_REAL_EXTREME_UPDATED      16:45:31.684  29742.30
TT_REAL_EXTREME_UPDATED      16:46:36.462  29745.10
FT_CANDIDATE_OPENED          16:46:36.862  29745.10 -> 29740.80
LOCAL_READING_OPENED         16:46:36.862  R0006
FT_CONFIRMED                 16:46:37.063  29740.60
AUT / TT_PENDIENTE / TT_CONFIRMADO R0006  16:46:43.277 / 16:46:49.489
FT final                     16:48:54.201  R0001 ft_ext 29674.60
```

## Pruebas
- `SELFTEST OK v0.7.2: 15 comprobaciones`.
- `TESTS OK v0.7.2: 16 comprobaciones`.
- Metamórficos: traslación de precio +1000.00, tiempo +30 min, simetría UP/DOWN y mismo recorrido con distinto número de ticks.
- Determinismo: dos ejecuciones consecutivas de ambas ventanas generan hashes idénticos.

## Hashes SHA256 de la entrega

```text
897E8CDFDA087813BF50C098E903A69C9FDC3527340FF8D644DFF00774EBA3C5  v072_1642_Eventos.csv
B63A4978DD19C62EFF0355BDF4D18F348D8AF3BD4118AA16707DD274E682C4F6  v072_1642_Lecturas.csv
50F4C696FB6B245843BD38870347B68240B1206969E6735AD552EBD8F81ABF3A  v072_1642_Patrones.csv
9B59AC717A28A7BF551ADB1354FB4EB99E6CADCA78186FA7CD3FF108A5ADAC3D  v072_1645_Eventos.csv
8923A4868E4CEC4B0C0AED1F6FA886D2E64FE228A4A7FA6BF1032E4CA0B1DEB8  v072_1645_Lecturas.csv
227A7FDC896C389811FAB37A95F30659E187F3C58A34C203F8A09A241D594D8F  v072_1645_Patrones.csv
```

## Puntos abiertos
- La lectura local de 16:45 usa un módulo de 11.00 puntos; el experto esperaba 25.30. La lectura es causalmente válida y no mezcla niveles, pero la granularidad local requiere decisión.
- `FT_CONFIRMED` se dispara con el primer tick adverso posterior a la candidata; el prompt no fija una excursión mínima de confirmación.
- `TT_COMPLETED` y `FT_WINDOW_EXPIRED` no se usan todavía como cierre automático al final de feed.
- `post_tt_fallido` sigue sin definición cerrada.
- v2.13.3 no está disponible; se contrasta con v2.14.
