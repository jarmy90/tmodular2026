# HANDOFF_DS_TO_AUDITORS

## Entrega congelada

- Versión: `TM_CORE_PYTHON_v0752_CANONICAL.py`, v0.7.5.2 candidato.
- Estado: `MOTOR_v0752_CANDIDATO_PENDIENTE_READER_VALIDATOR_Y_MIMO`.
- ZIP: `TM_CORE_v0752_CANONICAL.zip` (hash y tamaño se registran en `manifest.json` del paquete y en el informe externo de traspaso).
- Alcance: lectura causal local 16:15–16:24; no AFS2 ni ampliación de FT.
- Árbol de referencia adjunto: R1, ZIP congelado SHA-256 `C79E6D49D039A8F78A436013DF71673B9150EE342CF68D303849B65C32D79C90`; continúa pendiente de auditoría y aprobación final de Javier.
- Entradas: feed maestro y golden v003 incluidos físicamente.
- Separación: `CORE_RAW_OUTPUT.json` se genera primero por el motor. `GOLDEN_COMPARISON.json` se genera después y solo lee la salida bruta.

## Resultados reproducidos

- Core raw completo: 20.335 ticks; 6.559 eventos; 1.426 lecturas totales (incluye capa local); una genealogía local serializada; 4.901 eventos locales en todo el tramo.
- Autoprueba: 8/8.
- Generalidad: precios desplazados + timestamps desplazados, dirección invertida y checkpoint/chunks: PASS.
- Hardcodes en el motor: 0 coincidencias para horas, precios y sequence_id golden buscados.
- Golden básico 16:19–16:24: 8/9; no acredita reproducción exacta.
- Primera divergencia exacta: 16:23, AUT alcista. Esperado en sequence_id 1879 según v003; primer AUT emitido en 1876 (precio 29851,4). El estado esperado conserva A bajista hasta el ascenso registrado en 29852,6. Criterio causal exacto de confirmación requiere formalización/validación; no se cambió v003.
- El flujo también emite AUT locales adicionales posteriores, por lo que no se debe interpretar 8/9 como lectura completa.
- R0062/R0064: no encontrados con esos IDs en la salida candidata. La prueba R0062/R0064 no pasa.
- Prefijos: existe comparación causal por evento dentro de `GOLDEN_COMPARISON`, pero la batería física completa de 75 cierres + 500 cortes aleatorios no se ha aprobado. No declarar `prefix_failures=0`.

## Solicitud a Reader Validator

Inspeccionar primero la salida bruta y confirmar el primer tick divergente, estado anterior, salida y regla ausente/infringida. Solo lectura; no editar archivos del paquete. Comprobar que la comparación no altera el hash del raw.

## Traspaso técnico posterior

MiMo debe recibir exactamente el mismo ZIP y SHA-256 después del informe funcional de Reader Validator. Reproducir desde cero, verificar manifiesto, hashes, tests, prefijos, desplazamientos/inversión, hardcodes, R0062/R0064, regresión y causalidad. Solo lectura.

## Veredicto del implementador

`LECTURA_NO_REPRODUCIDA`. Entrega reproducible para auditoría del fallo, no aprobada funcional ni técnicamente. No autoriza replay ciego, AFS2 ni producción. No se declara aprobada por Javier.
