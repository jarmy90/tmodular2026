# Informe de traspaso ? TM_CANON v2.13 R1

- Versi?n: `TM_CANON_v2_13_PROPUESTA_R1`; candidato pendiente de auditor?a MiMo y aprobaci?n Javier.
- ZIP congelado: `TM_CANON_v2_13_PROPUESTA_R1.zip`.
- SHA-256: `C79E6D49D039A8F78A436013DF71673B9150EE342CF68D303849B65C32D79C90`.
- Tama?o: 316.146 bytes; 25 payloads y 2 controles = 27 entradas.
- Archivos principales: ?rbol R1, diff inicial?R1, matriz regla-golden, registro golden, decisi?n de autoridad plano/GAP, informe de cambios, README, manifest y SHA256SUMS.
- Resultado: manifiesto y checksums 0 errores; 0 rutas prohibidas; 0 payloads ausentes; diff LF; `git apply` probado con `core.autocrlf=false` y reproduce el ?rbol byte a byte.
- Matriz PLANO-01: 16:16 (+0,1) y 16:20 (-0,2) quedan como ejemplos de plano; 16:23 (+0,3) queda como contraejemplo NO PLANO (`|apertura-cierre anterior| >= 0,25`, resultado ?no abre en plano?).
- Estados golden: 16:38/16:39 retienen source_state `[A/B]` y canonical_status `CONFIRMADA_PARCIAL`; golden v003 no se modifica.
- Reglas: no se cambian; el conflicto documental de 2 puntos permanece pendiente. El ?rbol estable sigue en v2.12 (SHA-256 `07880B12EE0A40FC09821D2248CD01071B9AE8C3EF4147130049B3EB39F997A8`).
- Traspaso Reader/MiMo: pendiente para R1. La auditor?a t?cnica v0.7.5.1 recibida de MiMo no corresponde a R1 ni al ZIP v2.13 inicial.
- Limitaciones/veredicto: paquete documental; no valida motor, causalidad, prefijos ni generalidad. Estado `CANDIDATO_PENDIENTE_AUDITORIA_MIMO_Y_APROBACION_JAVIER`, no aprobado por Javier.
