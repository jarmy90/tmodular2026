# Contradicciones resueltas y pendientes — propuesta v2.13

## Resueltas en esta propuesta

| ID | Textos enfrentados | Autoridad aplicada | Decisión | Estado previo |
|---|---|---|---|---|
| C-PLANO-01 | DEC-009, DEC-013, H14/REGLAS_CERRADAS, AGENTS.md y v2.12 definen plano con `≤ 0,25`; la instrucción actual fija plano solo con `< 0,25`. | Instrucción expresa actual de Javier para v2.13. | `|apertura − cierre anterior| < 0,25` es plano; `≥ 0,25` es no plano/gap. Todas las fórmulas inclusivas de plano quedan SUPERADAS en esta propuesta. La referencia al cierre de la vela anterior se conserva. | DEC-009/013 y archivos fuente originales no se editan; su formulación inclusiva se conserva como historial. |
| C-GOLDEN-38 | Resumen v003 etiqueta 16:38 como A/B en apartados distintos; detalle de vela dice rama parcial y resultado completo pendiente. | Instrucción expresa actual de Javier: 16:38–16:39 son parciales. | Estado de registro B, no completo. | No se eleva por motor ni por la mención A del resumen. |
| C-TERCERO-01 | Dossiers históricos y v2.12 contienen «Tercero» como función o clasificación. | Ontología expresa de esta fase. | Solo `3` es función. «Tercero» aparece en la propuesta exclusivamente como término histórico superado. | La historia fuente se conserva sin editar. |
| C-ZIP-01 | Manifiesto interno del ZIP corrected v0.7.5.1 declara 46 archivos; el archivo físico tiene 48 entradas. | Revisión aprobada de Fase 0. | Los 2 controles adicionales son `manifest.json` y `SHA256SUMS.txt`; el `file_count` de 46 enumera payloads y excluye esos dos controles. El paquete original no se altera. | Nota añadida al manifiesto activo de organización. |

## Pendientes preservados, sin modificación de reglas abiertas

| ID | Contradicción/duda | Autoridad y evidencia | Tratamiento v2.13 |
|---|---|---|---|
| P-DUDA-009 | Regla general de módulo por descarte y alcance del segundo disparador de AUT. | DEC-014; `PREGUNTAS_PENDIENTES.md`; `REGLAS_PROVISIONALES.md`. | PENDIENTE; el caso golden 16:22 no se generaliza a regla por precio. |
| P-RUIDO-01 | v2.12 contiene umbral 2 puntos como cerrado; DEC-015 deja abierto el umbral numérico; la instrucción anterior de Fase 1 lo enuncia. | DEC-015 / PR-g y requisito de fase. | Se conserva el enunciado en §4 con su conflicto y alcance; no se edita el control de pendientes ni se añade regla de fragmentación. |
| P-TT-FT-01 | Semántica de TT fallido, expiración FT, entrada FT tardía y ciertos estados post-TT. | Reglas provisionales y readiness técnica v0.7.5.1. | PENDIENTE; no se promueve ningún caso histórico contradictorio a regla cerrada. |
| P-FT-02 | Confirmación matemática completa de FT, pérdida de velocidad, umbral y misma vela. | Dossier v3 §8.4; `REGLAS_PROVISIONALES.md` P6; instrucciones actuales solo fijan límites acotados. | PENDIENTE; v2.13 no amplía FT. |
| P-CUT-03 | Secuencias históricas de reset/continuidad tras CUT y «Tercero». | Dossiers y anexos antiguos frente a ontología vigente. | Solo queda vigente C→CUT al superar el final de A; desenlaces adicionales HISTÓRICOS/PENDIENTES. |
| P-CONC-04 | Prioridad, empates en el mismo tick y sustitución completa entre lecturas concurrentes. | DEC-015 cierra el criterio general; P5 conserva lo no decidido. | Se conserva el alcance cerrado compatible; detalles pendientes sin cambios. |
| P-GOLDEN-33 | Resumen v003 marca 16:33–16:36 como B; sección 5 describe referencia física y función abierta, lenguaje que puede mapear a C según definición inicial. | v003 §3 frente a §5. | Se conserva B como el estado explícito del resumen; se anota la divergencia textual y no se eleva a A. |
