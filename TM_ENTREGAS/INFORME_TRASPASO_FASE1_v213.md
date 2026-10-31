# Informe de traspaso ? coordinaci?n TM, Fase 1

- Versi?n: `TM_CANON_v2_13_PROPUESTA`, candidata pendiente de aprobaci?n de Javier.
- ZIP congelado durante auditor?a: `TM_CANON_v2_13_PROPUESTA.zip`.
- SHA-256: `A42274932680493CFEA99F0D8587258B11C61E7B7EC8C9FDB49322403FC01E3F`; tama?o: 306875 bytes; 23 entradas f?sicas (21 payloads + 2 controles).
- Archivos revisados: ?rbol propuesto, diff, contradicciones, reglas superadas, registro golden, matriz regla?golden, README, manifiesto, sumas y fuentes incluidas.
- Resultado funcional (TM_READER_VALIDATOR): **CON RESERVAS**. Verific? SHA antes de abrir, sumas internas 22/22, golden y v2.12 id?nticos a sus autoridades, 75/75 minutos y estados A=14, B=13, C=0, D=48; 17/17 citas de reglas superadas literales; el diff reproduce el documento propuesto.
- Primera divergencia funcional: matriz `TM_v2_13_REGLA_A_GOLDEN.csv`, fila `PLANO-01`, lista 16:23 (+0,3) como ejemplo de plano. El golden v003 ?10 dice que +0,3 >= 0,25 no abre en plano: es gap. Clasificaci?n del auditor: defecto de transcripci?n de la matriz; golden y regla no fallan.
- Observaciones: falta incluir en el ZIP la instrucci?n de Javier como respaldo documental de `<0,25`; ?4 formula el umbral de ruido de 2 puntos y DEC-015/PR-g lo mantiene pendiente; v003 etiqueta 16:38?16:39 `[A/B]` en un resumen, mientras la instrucci?n de Javier exige parcialidad; el CSV conserva B parcial, pero no la etiqueta literal; el diff tiene finales CRLF y v2.12 LF. No se cambi? ninguna regla pendiente.
- Limitaci?n: el paquete es documental; no contiene motor ni salida bruta, por lo que no acredita prefijos, generalidad, causalidad o regresi?n de motor.
- Auditor?a t?cnica: la respuesta recibida de MiMo acredita la auditor?a de otro artefacto (`deliverables_v0751_corrected_COMPLETE.zip`, SHA `9ECF3011?3418`), no de este ZIP v2.13. Por tanto, el traspaso t?cnico v2.13 sigue pendiente; el ZIP contin?a congelado.
- Veredicto de coordinaci?n actual: **PENDIENTE_AUDITORIA_TECNICA_MIMO**. No es aprobaci?n de Javier. No se ha corregido ni regenerado el ZIP.
- `AGENT_COORDINATION.md` se cre? despu?s en la ra?z del proyecto, pero su alcance documentado es la cadena v0.7.5.1. Para v2.13 se sigue la secuencia m?s reciente especificada por Javier.
