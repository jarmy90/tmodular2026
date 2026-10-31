# HANDOFF DS -> auditores — TM Core 0.7.5.2-R3

## Artefacto congelado

- ZIP: `TM_CORE_v0752_R3_B_AUT.zip` en la carpeta padre de este paquete.
- SHA-256 del ZIP: consultar `HANDOFF_DS_TO_AUDITORS_R3.md` en TM_ENTREGAS; se calcula al congelar.
- Version motor: `0.7.5.2-R3`.
- Estado: `MOTOR_v0752_R3_CANDIDATO_PENDIENTE_READER_VALIDATOR_Y_MIMO`.
- Arbol: propuesta `v2.13 R2`, candidata, no aprobada por Javier; v2.12 permanece como base aprobada.
- Auditar exactamente el mismo ZIP/hash. Reader Validator revisa primero la salida bruta; MiMo audita tecnicamente despues. Ninguno debe editar el paquete.

## Cambios

- B Grande se mide desde el final de A: candidata antes de 100%; confirmacion exacta en 100%; B vigente hasta inclusive 127% + 0,25; AUT solo al superar estrictamente el limite.
- Ambas transiciones primarias emiten en el primer tick observado. Las anclas sobreviven a los cambios de vela.
- La ruta A directa confirma AUT al superar estrictamente la base funcional atacada, promueve la propia A a nuevo 1 dominante, y no crea B ni TT.
- AUT causa queda como `B_EXCEEDS_127_PLUS_0_25` o `A_CROSSES_STRUCTURE_BASE`.
- C Grande comienza directamente tras B Grande confirmada; retrocesos internos de B no reinician su extremo.

## Resultados observados en este artefacto

- Pruebas nuevas: 16/16.
- Tests legacy: 20/20, con fixture original v0.10 dentro del ZIP.
- Selftest: 8/8.
- Transformaciones: PASS (chunks/serializacion, traslacion de precios/timestamps, inversion direccional); hardcodes en motor: 0.
- Replay: 20.335 ticks, 88 lecturas, 1.266 eventos; coverage flags geometric/functional=True.
- Prefijos fisicos: 12/12 PASS, 0 fallos; procesos nuevos y CSV cortados.
- R0062/R0064: referencias estructurales, TT, FT coinciden con baseline congelado.
- Golden Comparison: 6/9. Primera divergencia: v003 afirma AUT alcista 16:23 cuando B supera 100% pero no 127% + 0,25. Golden preservado; 16:23 AUT bajista y cadena 16:24 siguen sin reproducirse.
- Estado: `LECTURA_NO_REPRODUCIDA`; ninguna declaracion de autonomia perfecta, replay ciego, AFS2 ni produccion.

## Limites

La matriz completa de todos los cierres de 75 velas + 500 cortes aleatorios no se ejecuto. La matriz de transiciones cubre 12 cortes alrededor de eventos funcionales. El conflicto de golden 16:23 sigue abierto frente a la regla universal expresamente vigente. El resultado requiere auditoria independiente y decision final de Javier.

## Reproduccion

Desde la raiz extraida, instalar `requirements.txt` y ejecutar `python repro/run_all.py`. El runner hace todas las pruebas, replay, comparacion posterior, prefijos, diffs, manifiesto, hashes y ZIP. El proceso termina con codigo distinto de cero mientras GOLDEN_COMPARISON tenga divergencias conocidas.
