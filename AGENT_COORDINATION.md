# AGENT_COORDINATION — Cadena TM v0.7.5.1

Fecha de creación: 2026-10-28. Creado por TM SUPERVISOR MIMO tras confirmar que el archivo no existía en ninguna parte (lo indicó TM_READER_VALIDATOR en su informe).

## Cadena de auditoría v0.7.5.1

| Paso | Agente | Rol | Estado |
|---|---|---|---|
| 1 | DS TM BOSS (`agent-ece275c8-…`) | Implementa el parche, congela ZIP | ENTREGADO — ZIP `deliverables_v0751_corrected_COMPLETE.zip`, SHA-256 `9ECF30117FF878EEE970F95096DA0337E0E026BA74EC1529A9B0D3FBC4473418` |
| 2 | TM_READER_VALIDATOR (`agent-47b92cd3-…`) | Auditoría funcional (golden, tick a tick) | HECHA — veredicto **CON RESERVAS** en `TM_ENTREGAS\INFORME_TRASPASO_FUNCIONAL_v0751.md` (F1 BUG_MOTOR 16:37; F2/F4 REGLA_ABIERTA; F3 ALTERNATIVA_VALIDA; F5 observación de cobertura del auto-check) |
| 3 | TM SUPERVISOR MIMO (`agent-41b55ab1-…`) | Auditoría técnica (integridad, tests, prefijos, hardcodes, causalidad) | HECHA — veredicto **APROBADO (técnico)** con observaciones en `TM_ENTREGAS\INFORME_TRASPASO_TECNICO_v0751_MIMO.md` |
| 4 | Copilot / Javier | Decisión experta (F1, F2, F4 y observaciones) | PENDIENTE |

## Reglas de la cadena

- DS TM BOSS no modifica v0.7.5.1 mientras siga en auditoría: toda corrección exige versión y ZIP nuevos.
- Nadie toca motor, tests, golden ni árbol por cuenta propia; solo Javier cierra reglas abiertas.
- El ZIP auditado por Reader y por MiMo es el mismo (`9ECF3011…3418`); no auditar copias distintas.
- AFS2 sigue NO listo (`AFS2_READY=false`); nada de replay ciego ni producción.

## Informes publicados

- `C:\Users\profesor\tm\Teoria Modular\TM_ENTREGAS\INFORME_TRASPASO_FUNCIONAL_v0751.md` (Reader)
- `C:\Users\profesor\tm\Teoria Modular\TM_ENTREGAS\INFORME_TRASPASO_TECNICO_v0751_MIMO.md` (MiMo)

## Pendiente de Javier (según Reader + MiMo)

1. F1 — criterio de módulo cuando el extremo cae en el último segundo de vela (16:37).
2. F2 — orden AUT ↔ TT cuando el 127 %+0,25 se cruza con TT aún pendiente (16:31).
3. F4 — tope de 3 lecturas activas frente al golden (no lo contempla).
4. Observación MiMo A1 — yardstick del «2» local (rango High−Low vs desplazamiento direccional).
5. Observación MiMo A2 — redacción del umbral plano: `< 0,25` (implementado, brief de MiMo) vs `≤ 1 tick` (H14 en REGLAS_CERRADAS). Sin impacto en este feed (0 gaps de exactamente 0,25).


# Cadena de auditoria: arbol v2.13 R1 y motor v0.7.5.2 candidato

Fecha: 2026-10-28. Este bloque aplica a la nueva propuesta y no altera el registro historico v0.7.5.1 de arriba.

## Arbol R1 congelado

- ZIP: `TM_ENTREGAS/TM_CANON_v2_13_PROPUESTA_R1.zip`
- SHA-256: `C79E6D49D039A8F78A436013DF71673B9150EE342CF68D303849B65C32D79C90`
- Estado: `CANDIDATO_PENDIENTE_AUDITORIA_MIMO_Y_APROBACION_JAVIER`
- R0 inicial: hash `A42274932680493CFEA99F0D8587258B11C61E7B7EC8C9FDB49322403FC01E3F`; Reader lo reviso CON RESERVAS.
- La respuesta tecnica recibida de MiMo sobre hash `9ECF3011...` fue de `deliverables_v0751_corrected_COMPLETE.zip`, no de R0 ni R1; R1 aun requiere auditoria tecnica.
- Cambios R1 limitados a la matriz plano/gap, decision de autoridad, etiqueta literal `[A/B]` en 16:38/16:39, diff normalizado y registro de cambios. Golden y reglas pendientes no se modifican.

## Secuencia

1. TM_READER_VALIDATOR revisa funcionalmente R1; solo lectura.
2. TM SUPERVISOR MIMO audita tecnicamente el mismo ZIP/hash; solo lectura/ejecucion.
3. DS puede avanzar por carril separado al motor v0.7.5.2 tras congelar R1, conforme a autorizacion provisional de Javier; no cambia R1 durante auditoria.
4. El motor candidato se entrega primero a Reader y despues a MiMo. Ningun auditor cambia motor, tests, arbol, golden o reglas.
5. Javier conserva la autoridad final; nada se marca aprobado por Javier.

El informe vigente de traspaso esta en `TM_ENTREGAS/INFORME_TRASPASO_FASE1_R1.md`.

## Motor v0.7.5.2 candidato — entrega DS congelada

- ZIP: `TM_ENTREGAS/TM_CORE_v0752_CANONICAL.zip`
- SHA-256: `3380C0A82B779EC1E49D8270687F3E3E7627A524C16D8347C70C489107B7892A`
- Salida bruta SHA-256: `CD5C6FEB858DBDD6D31FD39EE7C3085E8D56D93F82B5E8D8BA39A81C9D1F31D7`
- Estado: `MOTOR_v0752_CANDIDATO_PENDIENTE_READER_VALIDATOR_Y_MIMO` / veredicto de implementador `LECTURA_NO_REPRODUCIDA`.
- Reader recibe primero el artefacto. MiMo recibirá exactamente el mismo ZIP/hash después de la revisión funcional; ambos en solo lectura.
- Resultado DS: autoprueba 8/8; transformaciones, inversión y serialización PASS; hardcodes 0; golden 16:19–16:24 8/9; primera divergencia AUT 16:23, esperado seq1879, emitido seq1876; se emiten AUT locales adicionales; R0062/R0064 ausentes; matriz completa de prefijos no ejecutada.
- Informe: `TM_ENTREGAS/INFORME_TRASPASO_MOTOR_v0752_CANDIDATO.md`.
- No autoriza replay ciego, AFS2 ni producción.

## DS delivery — v0.7.5.2-R3 (2026-10-28)

- Frozen ZIP: `TM_ENTREGAS/TM_CORE_v0752_R3_B_AUT.zip`
- SHA-256: `450379BD5F1E22380614E6112E3FB52C2A653EE8358BF7E5238995AF99D3B7DB`
- Version: v0.7.5.2-R3; tree candidate v2.13 R2. v2.12 remains approved base.
- Files installed separately as candidates: `TM_CANON_ACTIVO/01_ARBOL/CANDIDATO_v2_13_R2/` and `TM_CANON_ACTIVO/04_MOTOR_PYTHON/CANDIDATO_v0752_R3/`; new project source `tm-explorer/python/TM_CORE_PYTHON_v0752_CANONICAL_R3.py`. Existing candidates and stable active files were not replaced.
- Results: 16/16 new tests; 20/20 frozen legacy; selftest 8/8; transformations PASS; 20,335 feed ticks, 1,266 events, 88 readings; transition prefixes 12/12; R0062/R0064 match frozen references; golden 6/9 with known 16:23 conflict, golden unchanged. No full 500-random-cut matrix.
- Audit sequence: Reader Validator first, then MiMo; both read/execute only on the exact frozen ZIP. R3 remains candidate pending audits/Javier; no replay blind, AFS2, FT expansion or production.
- Handoff: `TM_ENTREGAS/HANDOFF_DS_TO_AUDITORS_R3.md`.
