# TM — PROGRAMA INTEGRAL — CHECKPOINT FASE A

- **Fase:** A — Lectura ciega de velas pendientes
- **Bloque:** 16:49:00.012 → 17:29:59.897
- **Árbol:** v2.19 `94A1408A…` · `WORKING_CANON_NOT_FROZEN`
- **Instrumento:** `blind_reader.py` (Fase A; no es el motor oficial)
- **tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

> **ERRATA 2026-10-30.** Tras la auditoría funcional de las 16 generaciones
> (`01_TREE_VALIDATION/PHASE_A_GENERATION_AUDIT.md`): el recuento de AUT es
> **9**, no 8; la gen 23 tiene módulo **24,7** y AUT **17:18:09.401**. Las
> preguntas Q1/Q2/Q4 de este checkpoint quedan reformuladas como
> Q_AUT_DIRECTION, Q_C_GRANDE y Q_A_MARGIN. Las 16 generaciones **no están
> aprobadas** como lectura TM definitiva.

---

## 1. TRABAJO COMPLETADO

1. Registro de la continuación oficial del mandato (§4–§15) con hash verificado.
2. Construcción de un lector causal tick a tick que aplica las reglas cerradas
   4.1–4.10 y declara explícitamente sus políticas H1–H7.
3. Recorrido completo del bloque 16:49–17:29: **11.414 ticks**, 41 velas,
   secuencias 8922–20335 sin huecos.
4. Lectura funcional del bloque: **16 generaciones**, con origen, extremo,
   módulo, A, B, C, AUT/CUT, TT, `structural_time` y `knowledge_time`.
5. Lectura secundaria: 6 TT confirmados, 9 fallidos, 1 posible; 9 esbozos de
   gap; 6 transiciones A/C usadas como tendencia.
6. Ejecución de R5 sobre el mismo bloque real como evidencia observacional:
   29 lecturas, 702 eventos.
7. Verificación: doble ejecución idéntica y **41/41 prefijos** consistentes.
8. Registro de cuatro preguntas universales y nueve huecos menores.

## 2. RESULTADO

```text
TICKS DEL BLOQUE ............. 11.414
VELAS ........................ 41
GENERACIONES ................. 16
MÓDULOS REGULARES 1-2-3 ...... 0
MÓDULOS POR DESCARTE ......... 16
AUT .......................... 9
A_USED_AS_TREND .............. 4
C_USED_AS_TREND .............. 2
ABIERTA AL FINAL ............. 1
TT CONFIRMADOS ............... 6
TT FALLIDOS .................. 9
```

La lectura principal está en
`01_TREE_VALIDATION/BLIND_TREE_READINGS_1649_1729.md`.

El hallazgo estructural: **en 41 velas no se completó ni un solo módulo
regular 1-2-3**. La regla 4.2 (2 exige apertura plana y 100 % de 1) hizo que
14 de 16 velas no pudieran abrir 2. El bloque entero se leyó como módulos por
descarte. Esto no es un fallo del lector: es la consecuencia literal de la
regla.

## 3. DIVERGENCIAS

| Referencia | Divergencia | Clasificación |
|---|---|---|
| R5 real | R5 abre su primera lectura en 16:49:06 con módulo 14,4 (primer tramo de la vela); el lector abre 1 con la vela completa de 33,5 | `ONE_UNIT` |
| R5 real | R5 produce 29 lecturas; el lector, 16 generaciones | `GRANULARITY` |
| R5 real | R5 sí emite A, B, C, AUT, CUT y TT_100 en el feed real; la ausencia de las 21 secuencias CE era un artefacto del banco sintético | corrección de la auditoría CE |
| v005 16:15–16:24 | coincidencia en módulo 28,5, TT 29829,1, A 9,1, AUT 29845,3, A 7,3 y AUT 29831,0 | sin divergencia semántica |
| v005 16:18 | AUT reportado en 29843,0; primer tick del lector en 29845,3 | `KNOWLEDGE_TIME` |
| v005 16:49–17:29 | **[D] pendiente**, sin golden | no comparable |

El detalle está en
`01_TREE_VALIDATION/BLIND_TREE_FIRST_DIVERGENCES.csv` y
`01_TREE_VALIDATION/BLIND_TREE_SECONDARY_READINGS.md`.

## 4. REGLAS ABIERTAS

> **Q1/Q2/Q4 reformuladas.** La auditoría de generaciones sustituye estas
> preguntas binarias por tres preguntas estructurales: Q_AUT_DIRECTION,
> Q_C_GRANDE y Q_A_MARGIN. Se conservan aquí como registro de la Pasada A.

### Q1 — Unidad de 1 en vela no monótona (reformulada)

16:49: ¿1 es el primer tramo bajista de 14,4 o la vela completa de 33,5?
Decide la granularidad de toda la salida (16 vs 29 lecturas). La auditoría
muestra que **ninguna de las dos opciones basta**: el 1 del árbol es el
movimiento de la transición, no la vela ni el tramo.

### Q2 — Autonomía de A y propiedad del extremo del módulo

17:22: ¿el módulo mide 44,7 (extremo de 1) o 30,8 (extremo de 2)? ¿Cuánta
autonomía necesita A? La sensibilidad del bloque es 16 / 16 / 9 / 11
generaciones para mínimos de A de 2 / 6 / 12 / 20 puntos.

### Q3 — Gap significativo y referencia de C

¿Un hueco de 3,1 exige la resolución implícita A/B/A de v2.19 o sólo impide 2?
¿C se convierte en tendencia en el final de A o en la base del módulo?

### Q4 — Dominancia y concurrencia

¿La lectura dominante es la cadena de 16 generaciones o los tres tramos
humanos? Cuando AUT abre un nuevo 1, ¿es el movimiento de B o la vela
siguiente? ¿La lectura anterior sigue siendo dominante?

Formulación completa en
`01_TREE_VALIDATION/BLIND_TREE_CONCEPTUAL_GAPS.md`.

## 5. ARCHIVOS

| Archivo | Contenido |
|---|---|
| `01_TREE_VALIDATION/BLIND_TREE_READINGS_1649_1729.md` | acta de la lectura y 16 generaciones |
| `01_TREE_VALIDATION/BLIND_TREE_SECONDARY_READINGS.md` | TT, gaps, transiciones y R5 real |
| `01_TREE_VALIDATION/BLIND_TREE_CONCEPTUAL_GAPS.md` | Q1–Q4 y huecos menores |
| `01_TREE_VALIDATION/BLIND_TREE_FIRST_DIVERGENCES.csv` | 12 primeras divergencias |
| `01_TREE_VALIDATION/BLIND_TREE_TRACE_1649_1729.jsonl` | estado por tick (11.414 filas) |
| `01_TREE_VALIDATION/BLIND_TREE_EVENTS_1649_1729.csv` | 454 eventos |
| `01_TREE_VALIDATION/BLIND_TREE_STATE_AT_BAR_CLOSE.csv` | estado al cierre de 41 velas |
| `01_TREE_VALIDATION/BLIND_TREE_GENERATIONS_1649_1729.csv` | tabla de 16 generaciones |
| `01_TREE_VALIDATION/PHASE_A_MANIFEST.json` | manifiesto, hashes y gate |
| `01_TREE_VALIDATION/SHA256SUMS.txt` | hashes de los entregables |
| `01_TREE_VALIDATION/blind_reader.py` | lector causal |
| `01_TREE_VALIDATION/verify_phase_a.py` | determinismo y prefijos |
| `01_TREE_VALIDATION/run_r5_block.py` | evidencia R5 sobre el bloque |

## 6. HASHES

```text
árbol v2.19 ........ 94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17
lecturas v005 ...... F5D7550C42C90897D833E6C2A3FAF772753A129640FD4411DE4190CB2CF94226
tickfeed maestro ... 5F701BE2307352CB559ABBD7BB856A6FD2A1F91E5D269A93DCC9AE2992E2C9FF
R5 auditado ........ 9BD1BEDB5DEC8C5A1C3A831338503E90CC04EE3CD776CF4E01D27CF8AA0EBEAE
mandato continuación f9050901565c334e1daf6ba48df42dc0ab5d0f081798b27598318e48b0ad3657
```

Los hashes de los cinco originales coinciden con los esperados. No se
modificó ningún original.

## 7. GATE A

```text
GATE A = PASS_WITH_OPEN_QUESTIONS

todos los ticks recorridos ........ SÍ
toda función trazable ............. SÍ
ambigüedades explícitas ........... SÍ
sin spoilers ...................... SÍ
determinista ...................... SÍ
prefijos consistentes ............. 41/41
sin hardcoding .................... SÍ
```

El gate se cumple porque la lectura es trazable, determinista y por prefijos.
Las cuatro preguntas abiertas no impiden avanzar: son la materia de la Fase B.

## 8. SIGUIENTE FASE

```text
FASE B — PERFECCIONAMIENTO CONCEPTUAL DEL ÁRBOL
```

La Fase B debe:

1. agrupar Q1–Q4 con los casos equivalentes del warm-up 16:15–16:48;
2. decidir si alguna queda bloqueada por falta de evidencia;
3. formular como máximo 4 preguntas expertas, con consecuencia y nodos
   desbloqueados;
4. no congelar el árbol hasta que Q1 y Q2 estén resueltas.

## 9. DECISIÓN NECESARIA

Antes de la Fase B:

- **¿Se acepta Q1 como la primera pregunta experta?** Sin ella, la unidad de 1
  y la granularidad de toda la salida quedan indefinidas.
- **¿Se acepta H2 (A = 6,00) como política provisional** mientras Javier no
  fije la autonomía de A?
- **¿Se acepta que el bloque 16:49–17:29 se lea como 16 generaciones**, con la
  lectura macro de tres tramos sólo como reconstrucción humana?

No se inicia la Fase B ni se congela nada hasta recibir la respuesta.
