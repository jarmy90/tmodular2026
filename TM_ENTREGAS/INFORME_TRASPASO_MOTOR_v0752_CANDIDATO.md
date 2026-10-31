# Traspaso DS → Reader Validator / MiMo — v0.7.5.2 candidato

Fecha: 2026-10-28

## Artefactos congelados

- Árbol R1: `TM_CANON_v2_13_PROPUESTA_R1.zip`, 316.146 bytes, SHA-256 `C79E6D49D039A8F78A436013DF71673B9150EE342CF68D303849B65C32D79C90`.
- Motor: `TM_CORE_v0752_CANONICAL.zip`, 1.356.866 bytes, SHA-256 `3380C0A82B779EC1E49D8270687F3E3E7627A524C16D8347C70C489107B7892A`, 25 entradas físicas, manifiesto 25/25, rutas POSIX válidas, 0 hashes incorrectos.
- Salida bruta: 20.335 ticks, 6.559 eventos, 1.426 lecturas totales y 4.901 eventos locales. SHA-256 `CD5C6FEB858DBDD6D31FD39EE7C3085E8D56D93F82B5E8D8BA39A81C9D1F31D7`.
- Golden comparison: 8/9, separada y de solo lectura. El SHA-256 de CORE_RAW_OUTPUT es idéntico antes y después.
- Ruta de reproducción desde ZIP: `python repro/run_all.py`.

## Verificación del implementador

- Autoprueba: 8/8.
- Precio desplazado + timestamps desplazados: PASS.
- Dirección invertida: PASS.
- Chunks y serialización/restauración: PASS.
- Búsqueda de hardcodes golden en el motor: 0 coincidencias.
- Comparación exacta de funciones: 8/9. La primera divergencia está en 16:23: v003 sitúa el AUT alcista en sequence_id 1879; el primer AUT del núcleo aparece en 1876 (precio 29851,4). v003 registra 29852,6 en 1879. La causa exacta de la diferencia de confirmación no se ha cerrado; el golden no se modificó.
- El motor emite funciones locales adicionales después de esos puntos; no se declara reproducción autónoma completa.
- R0062/R0064 no se encuentran con esos IDs en la salida candidata.
- Prefijos físicos: batería completa de 75 cierres + 500 cortes con semilla 7552 no ejecutada; `prefix_failures` no está acreditado. El ZIP contiene un runner y registra honestamente `NOT_RUN_FULL_MATRIX`.

## Veredicto y coordinación

`LECTURA_NO_REPRODUCIDA`. Candidato pendiente de Reader Validator y MiMo, no aprobado por Javier. Reader recibe primero exactamente el ZIP y hash indicados; MiMo recibirá el mismo artefacto después del informe funcional. La entrega no habilita replay ciego, AFS2 ni producción.

Informe interno del paquete: `TM_CORE_v0752_CANDIDATO/HANDOFF_DS_TO_AUDITORS.md`.
