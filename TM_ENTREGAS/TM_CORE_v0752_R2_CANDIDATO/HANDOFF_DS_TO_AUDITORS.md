# HANDOFF DS → auditores — v0.7.5.2 R2

## Artefacto congelado para revisión

- Motor: `python/TM_CORE_PYTHON_v0752_CANONICAL.py`, versión `0.7.5.2-R2`.
- ZIP: `TM_CORE_v0752_R2_CANDIDATO.zip` (hash registrado en el traspaso tras congelar).
- Estado: `MOTOR_v0752_CANDIDATO_PENDIENTE_READER_VALIDATOR_Y_MIMO`.
- Árbol R1 adjunto: hash ZIP congelado `C79E6D49D039A8F78A436013DF71673B9150EE342CF68D303849B65C32D79C90`; sigue pendiente de aprobación final de Javier.
- Golden v003 y feed maestro están incluidos sin cambios. El motor no abre el golden.

## Veredicto del implementador

`LECTURA_NO_REPRODUCIDA`. El paquete se ofrece para auditar el estado real y sus fallos; no cumple los criterios de salida.

### Cambios R2

- AUT local registra `AUT_SOURCE` para las rutas B y A-base.
- La transición AUT cierra la lectura anterior con genealogía e inicia una lectura hija para el nuevo 1 dominante.
- La confirmación local de 3 espera una extensión estructural de al menos 2 puntos.
- El límite existente protege hasta 3 lecturas primarias, pero la concurrencia total llegó a 4 cuando coincidieron 3 lecturas primarias y una local. Criterio global máximo 3: NO CUMPLE.

### Divergencias bloqueantes

- Golden 16:23: v003 declara AUT alcista cuando B supera el inicio de A. El feed y la salida bruta sitúan el primer cruce del nivel en sequence_id 1876 y el máximo B en 1879. Con la regla experta vigente, B Grande solo pasa a AUT al superar 127% de A + 0,25. El motor registra A=7,50 y B=8,60 puntos; el límite es 9,77. No emite AUT alcista. Se conserva el golden y se informa el conflicto; no se fuerza una función.
- Como consecuencia, no reproduce la secuencia AUT bajista de 16:23 ni la cadena A/B/AUT esperada al cierre de 16:24.
- R0062/R0064 existen en la salida, pero su geometría y referencias TT/FT no igualan v0.7.5.1; regresión exacta: NO CUMPLE.
- Matriz física completa de prefijos: no ejecutada. `prefix_failures=0` no acreditado.

## Resultados ejecutados

- Suite legacy congelada: `20/20`.
- Autoprueba: `8/8`.
- Transformaciones: precios desplazados, timestamps desplazados, dirección invertida y chunks/serialización: PASS.
- Hardcodes golden en motor: `0` coincidencias.
- Golden comparison: `6/9`; primera divergencia funcional en el AUT alcista 16:23.
- Raw: 20.335 ticks, 1.665 eventos, 135 lecturas totales; 59 lecturas locales históricas; cero módulos locales menores de 2 puntos; máxima concurrencia observada: 4.
- R0062/R0064: presentes, pero regresión no exacta (detalle en `out/R0062_R0064.json`).

## Orden de auditoría solicitado

Reader Validator inspecciona primero `out/CORE_RAW_OUTPUT.json` y confirma primera divergencia, estado previo y regla aplicada. MiMo recibe después exactamente el mismo ZIP y SHA-256 y reproduce manifiesto, hashes, tests, prefijos, generalidad, hardcodes, regresión y causalidad. Lectura y ejecución solamente; ningún auditor modifica archivos.

No autoriza replay ciego, AFS2 ni producción. No se declara aprobado por Javier.
