# Informe de traspaso — validación funcional Fase 1 (v2.13 propuesta)

- Emisor: TM_READER_VALIDATOR (auditor funcional). Sin edición de ningún archivo.
- Fecha: 2026-10-28.
- Destino: DS TM BOSS. Copia para MiMo y coordinación.
- Versión: `TM_CANON_v2_13_PROPUESTA` — `CANDIDATO_PENDIENTE_APROBACION`.

## 1. Hash verificado antes de abrir

| Comprobación | Valor |
|---|---|
| SHA-256 del ZIP | `A42274932680493CFEA99F0D8587258B11C61E7B7EC8C9FDB49322403FC01E3F` |
| Tamaño | 306.875 bytes |
| Entradas físicas | 23 (21 payload + `manifest.json` + `SHA256SUMS.txt`) |
| `SHA256SUMS.txt` interno | 22/22 OK, 0 ausentes |
| Coincidencia con el hash entregado | SÍ |

## 2. Archivos revisados

`TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA.md`; `TM_v2_13_REGISTRO_GOLDEN_HUMANO.csv`;
`TM_v2_13_REGLA_A_GOLDEN.csv`; `REGLAS_SUPERADAS.csv`;
`CONTRADICCIONES_RESUELTAS_Y_PENDIENTES.md`; `CLASIFICACION_CONTENIDO_v2_12.csv.md`;
`README_REPRODUCCION.md`; `manifest.json`; `SHA256SUMS.txt`; `DIFF_v2_12_a_v2_13_PROPUESTA.diff`;
`historical/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_12.md`;
`source/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v003.txt` y demás `source/`.

## 3. Resultado y evidencia

| Verificación | Resultado |
|---|---|
| Integridad del paquete | 23/23 entradas con hash correcto (`SHA256SUMS.txt` 22/22). |
| `historical/` contiene el v2.12 exacto | SÍ: `07880B12…F997A8`, idéntico al `TM_ARBOL_ACTIVO.md` de `TM_CANON_ACTIVO/01_ARBOL`. |
| Golden incluido = golden vigente | SÍ: `1E634EBB…104E5B`, idéntico al del ZIP de motor v0.7.5.1. |
| Registro golden completo | 75/75 minutos consecutivos, 16:15–17:29, sin huecos ni duplicados. |
| Estados A/B/C/D | A=14, B=13, C=0, D=48 (total 75). Coincide con v003 §3. |
| Confirmadas A | 16:15–16:24 (10), 16:30–16:32 (3), 16:37 (1). Coincide con v003. |
| Parciales B | 16:33–16:36 (4), 16:38–16:39 (2), 16:42–16:48 (7). Coincide con v003. |
| Pendientes D | 16:25–16:29 (5), 16:40–16:41 (2), 16:49–17:29 (41). Coincide con v003. |
| `REGLAS_SUPERADAS.csv` | 17/17 citas verificadas literalmente en la línea indicada de la fuente. |
| Contradicción C-PLANO-01 | Confirmada: AGENTS.md:36 usa `<= 0,25`; DEC-009 usa ±1 tick inclusivo; v2.12 H14 y §2896 usan `= 0,25` como plano. |
| Contradicción C-TERCERO-01 | Confirmada: v2.12 usa «Tercero» 23 veces como función/clasificación; v2.13 sólo lo mantiene como término histórico superado. |
| Contradicción C-ZIP-01 | Confirmada: ZIP de motor con 48 entradas físicas y `file_count=46` + 2 controles (`manifest.json`, `SHA256SUMS.txt`). |
| Diff v2.12→v2.13 | Reproduce las 153 líneas del documento v2.13 (hunk único `-1,13727 +1,153`, 13680 eliminadas + 47 contexto / 106 añadidas + 47 contexto). |
| Lectura humana 16:15–16:24 resumida en §9 | Coincide con v003: 16:16 (+0,1, plano, 12,6 < 16,2); 16:19/20/21 = 1/2/3; 16:22 AUT 29850,8 > 29850,0 en 0,8; 16:23–16:24 bloque causal. |

### Primera divergencia funcional

**16:23 — `TM_v2_13_REGLA_A_GOLDEN.csv`, fila `PLANO-01`, columna `golden_minutes`.**

- La matriz cita `16:23 (+0,3)` como ejemplo de la regla «plano si |Δ| < 0,25».
- v003, VELA 16:23, dice literalmente: «Diferencia: +0,3 puntos. Como 0,3 >= 0,25, no abre en plano».
- Es decir, 16:23 es un **ejemplo de gap**, no de plano. Con la regla que la propia fila documenta, +0,3 queda fuera del plano.
- Clasificación: `FALLO_AUDITOR` en la taxonomía disponible = defecto de transcripción del entregable. **El golden no falla; la regla tampoco.**

### Observaciones menores

1. El paquete **no cita la corroboración más fuerte** de la regla estricta: v003 ya aplica `< 0,25` en 16:16 (+0,1), 16:20 (−0,2) y 16:23 (+0,3 ≥ 0,25 ⇒ no plano). La fila PLANO-01 invierte justo el caso 16:23.
2. La sustitución global de `≤ 0,25` se atribuye a «instrucción expresa actual de Javier», pero esa instrucción **no se incluye como artefacto** en el ZIP; su trazabilidad depende del mensaje del coordinador.
3. §4 dice «2 puntos exactos como umbral de confirmación retroactiva», mientras la fuente es «menos de 2 puntos es ruido» (v2.12 §2513: «inferior a 2,00 puntos es ruido»). Queda PENDIENTE por DEC-015/PR-g; riesgo de lectura como umbral = 2,00 exactos.
4. En el registro, `source_state` de 16:38 y 16:39 es `B`, mientras v003 §3 los etiqueta `[A/B]`. La divergencia está documentada en C-GOLDEN-38, pero el CSV no conserva la etiqueta literal.
5. El diff usa CRLF y el v2.12 histórico LF; un `patch` byte-exacto puede requerir normalización. El contenido reproduce el v2.13 línea a línea.

## 4. Limitaciones

- El ZIP **no contiene motor ni salida bruta del núcleo**. No se puede acreditar causalidad, prefijos, generalidad ni regresión de un motor. No se sustituye por `GOLDEN.py` ni por informes.
- No se ejecutaron tests de motor (no hay artefacto ejecutable en Fase 1).
- La validación funcional se limita a árbol, registro golden, matriz de evidencia, contradicciones y documentación de respaldo.
- `AGENT_COORDINATION.md` no existe en las raíces consultadas; se aplica la secuencia del mensaje del coordinador.

## 5. Veredicto funcional

**CON RESERVAS** — apto para auditoría técnica de MiMo, **no aprobado por Javier**.

- Conserva íntegros los estados A/B/C/D y el bloque 16:15–16:24.
- No eleva velas parciales ni pendientes.
- No declara reglas nuevas: la única regla cambiada (plano `< 0,25`) se atribuye a instrucción expresa y queda fuera de las pendientes.
- Requiere corregir la fila PLANO-01 de `TM_v2_13_REGLA_A_GOLDEN.csv` (16:23 debe figurar como caso de gap) y, si se desea, anexar la instrucción de Javier para trazabilidad.
- No autoriza replay ciego, AFS2, producción ni la Fase 2.
