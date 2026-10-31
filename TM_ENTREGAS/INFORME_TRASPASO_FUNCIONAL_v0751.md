# Informe de traspaso funcional — v0.7.5.1 vs golden humano v0.03

- Emisor: TM_READER_VALIDATOR (auditor funcional; sin permisos de edición sobre motor, tests, árbol, golden ni reglas).
- Fecha: 2026-10-28.
- Destinatario siguiente en la cadena: TM SUPERVISOR MIMO (auditoría técnica). Copia a DS TM BOSS y a Copilot/Javier.
- Protocolo aplicado: el mensaje de coordinación del coordinador. `AGENT_COORDINATION.md` **no existe** en `C:\Users\profesor\tm\Teoria Modular`, `C:\Users\profesor\OpenBot\Shared` ni en los directorios de agente consultados (búsqueda recursiva por nombre). Se aplica la secuencia indicada en el mensaje.

## 1. Artefactos congelados y verificación

| Artefacto | SHA-256 | Comprobación |
|---|---|---|
| `deliverables_v0751_corrected_COMPLETE.zip` (motor + salidas) | `9ECF30117FF878EEE970F95096DA0337E0E026BA74EC1529A9B0D3FBC4473418` | ZIP íntegro; `SHA256SUMS.txt` interno: 47/47 OK, 0 ausentes |
| `TM_CANON_v2_13_PROPUESTA.zip` (árbol/golden) | `A42274932680493CFEA99F0D8587258B11C61E7B7EC8C9FDB49322403FC01E3F` | ZIP íntegro; `SHA256SUMS.txt` interno: 22/22 OK, 0 ausentes |

Identidad entre lo auditado y lo congelado (para descartar auditoría sobre copia distinta):

| Archivo | SHA-256 | Repo vs ZIP |
|---|---|---|
| `out_v0751/v0751_Eventos.csv` | `F171E99E9068256E4154CDDEA9CC7242CC699400EAAF93BD26A8746EA6F9699E` | idéntico |
| `out_v0751/v0751_LocalEventos.csv` | `878967F0C767572D0AD185250BD3C7F122DCC57C91EEBC108114D2920D263447` | idéntico |
| `out_v0751/v0751_Lecturas.csv` | `80B22427795C539E5941F6389D3F97F74D755E5262A5A734B8B7EF4BB570101A` | idéntico |
| `data/TM_TICKFEED_1615_1730.csv` | `5F701BE2307352CB559ABBD7BB856A6FD2A1F91E5D269A93DCC9AE2992E2C9FF` | idéntico al feed maestro |

No se modificó ningún archivo del paquete. Sólo lectura y ejecución de comprobaciones.

## 2. Método

1. Se parte de la salida bruta del núcleo (`v0751_Eventos.csv`, `v0751_LocalEventos.csv`, `v0751_Lecturas.csv`), no de los informes del implementador.
2. Se cruza cada hito con el tickfeed maestro por `sequence_id`, `time_msc` y precio bid.
3. Se separan siempre `structural_time` / `confirmation_time` / `knowledge_time` / `sequence_id`.
4. No se generan etiquetas desde horas, precios ni velas; la única autoridad es `lecturas_confirmadas_v003.txt`.

## 3. Resultados

| Bloque golden | Estado | Resultado funcional |
|---|---|---|
| 16:15–16:22 | [A] | Reproducido. Módulo 29877,00→29848,50 X=28,50; A 29848,50→29857,60; AUT bajista 29843,00; local 1-2-3 con 29830,30. |
| 16:23–16:24 | [A] tick a tick | **Reproducido exacto.** `extreme_time` coincide al milisegundo con los `sequence_id` del golden: 1846, 1879, 1951, 2062, 2078, 2107, 2162, 2165, 2240, 2259, 2290, 2303. |
| 16:30 | [A] | Parcial: módulo 53,60 y TT pendiente correctos; **final de A divergente**. |
| 16:31 | [A] | Parcial: TT pendiente correcto; arrastra 2,10 puntos del final de A; confirma AUT no registrada en el golden. |
| 16:32 | [A] | Desenlace equivalente, mecanismo distinto (reset 14 ticks más tarde). |
| 16:37 | [A] | **No reproducido**: falta el módulo 61,20. |
| 16:38–16:39 | [A/B] | Parcial por arrastre del error de 16:37. |

**Lecturas [A] completamente reproducidas: 10/14 (71,4 %).** El 100 % del tramo con orden causal certificado (16:23–16:24) se reproduce exacto.

### Primera divergencia funcional

`16:30:59.568`, `sequence_id 3827`, `bid 29812,90`.

- Motor (R0011): `a_end = 29812,90`, `a = 28,30`, `tt_target = 29759,30`.
- Golden (16:31): `FINAL_A = 29810,80`, `TT = 29757,20`, distancia 3,10.
- El tape da 29812,90 antes de la apertura de 16:31 (29810,80).

Clasificación: **`GOLDEN_INCOMPLETO`**. No es error de regla del motor. Efecto: distancia real al TT = 1,00, no 3,10; la conclusión cualitativa (TT pendiente) no cambia.

### Fallos priorizados

| ID | Clasificación | Vela | Descripción |
|---|---|---|---|
| F1 | `BUG_MOTOR` | 16:37 | Golden exige 1 bajista con módulo 29744,40→29683,20 = 61,20. El motor fragmenta en X=26,80 (R0030) y X=20,80 (R0031); el mínimo 29683,20 (seq 5827) no cierra módulo y el B de R0031 se prolonga a 29674,60 ya en 16:38. Arrastra 16:38–16:39, que comparan contra 8,80/20,80. |
| F2 | `REGLA_ABIERTA` | 16:31 | El 127 %+0,25 se cruza en 16:31:18.407 (seq 3920). El golden mantiene "B activa / TT pendiente" sin AUT; el motor confirma AUT en 16:31:37.857 (structural 16:31:33.648, precio 29760,30). Requiere fallo de Javier sobre el orden AUT ↔ TT. |
| F3 | `ALTERNATIVA_VALIDA` | 16:32 | El golden invalida el TT al superar 29810,80 (tick 29811,80 en 16:32:23,358, seq 4227) y reclasifica 16:30+16:31 como módulo conjunto. El motor detecta ese tick pero lo etiqueta `C`; resetea con `CUT_CRUZA_A_END_MAS_2` en 29820,80 (+14 ticks). |
| F4 | `REGLA_ABIERTA` | 16:32–16:40 | Tope de 3 lecturas activas (`ARCHIVADA_POR_CAPACIDAD` en R0012, R0013, R0015, R0019, R0023, R0028, R0032, R0033). El golden no contempla ese límite y conserva escenarios secundarios. |
| F5 | `FALLO_AUDITOR` | paquete | El auto-check declara "golden_v003 22/22" y "prefijos 11/11", pero compara barra/precio/función: no valida `structural_time`, `confirmation_time`, `knowledge_time` ni `sequence_id`. No es evidencia de fidelidad tick a tick. |

### Casos mínimos reproducibles (para corrección y para tests)

1. **F1:** alimentar 16:36:50–16:38:10 → esperado módulo 61,20; obtenido 26,80/20,80.
2. **F2:** alimentar hasta seq 3920 → esperado B activa + TT pendiente; obtenido AUT en seq 3990.
3. **F3:** alimentar hasta seq 4227 → esperado TT invalidado + reclasificación; obtenido `C` y reset en seq 4300.
4. **Control:** alimentar hasta seq 1846 → esperado y obtenido extremo A 29842,80 con `structural_time` 16:23:02.021.

## 4. Limitaciones

- No ejecuté el motor: audité la salida congelada. La reproducción ejecutable corresponde a MiMo.
- El ZIP `TM_CANON_v2_13_PROPUESTA` no contiene motor ni salida bruta; sólo árbol/golden documental. Su validación funcional queda cubierta por el ZIP de motor.
- El tramo 16:25–16:29 y 16:40–17:29 no tiene golden completo; no se pronunció veredicto sobre ellos.
- El golden usa un criterio por vela; 16:37 y 16:30 muestran que "máximo−mínimo de vela" no siempre coincide con el módulo funcional del tape.
- No hay `AGENT_COORDINATION.md`; el traspaso se rige por el mensaje del coordinador.

## 5. Veredicto y traspaso

**CON RESERVAS** — `ENTREGADO_A_AUDITORIA_TECNICA`.

- No autoriza replay ciego, AFS2 ni producción.
- No equivale a aprobación técnica ni a aprobación de Javier.
- DS TM BOSS no debe modificar v0.7.5.1 mientras siga en auditoría: toda corrección exige versión y ZIP nuevos.
- Siguiente paso en la cadena: MiMo audita el mismo ZIP `9ECF3011…3418` (manifiesto, tests, prefijos, generalidad, hardcodes, regresión, causalidad).
- Decisión pendiente de Javier: F2 (orden AUT ↔ TT) y criterio de módulo de F1 cuando el extremo cae en el último segundo de vela.

## 6. Anexo — separación de tiempos (verificada)

El motor separa correctamente los tres tiempos; el desfase inicialmente sospechado era de lectura, no de sellado:

- L00007 A: extremo 16:23:02.021 (seq 1846), confirmación 16:23:08.304 (seq 1867).
- L00008 B: extremo 16:23:12.154 (seq 1879), confirmación 16:23:28.868.
- L00014 B: extremo 16:24:49.819 (seq 2259), confirmación 16:24:58.066.
- TT_100: estructural 16:24:44.990 (seq 2240, 29829,00), confirmación 16:24:58.066.
