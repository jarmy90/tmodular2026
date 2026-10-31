# ROLLBACK_PLAN_v1 — TM_PROGRAM_INTEGRAL_V1

**Fecha:** 2026-10-30
**Alcance:** nuevo espacio de trabajo `TM_TRABAJO_TEMPORAL/TM_PROGRAM_INTEGRAL_V1/`
**Originales afectados:** ninguno

---

## 1. Principio

Todo el programa vive en una carpeta nueva. Los originales se leen, nunca se escriben.

```text
PROTEGIDOS (solo lectura):
  TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md
  TM_CANON_ACTIVO/02_TICKS/TM_TICKFEED_1615_1730.csv
  TM_CANON_ACTIVO/03_LECTURAS_HUMANAS/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v005.txt
  TM_CANON_ACTIVO/04_MOTOR_PYTHON/CANDIDATO_v0752_R3/...
  TM_CANON_ACTIVO/04_MOTOR_PYTHON/TM_MOTOR_ACTIVO.py
  R5 auditado y R5 empaquetado
  ZIP R3, ZIP R5
  goldens, manifiestos históricos
```

## 2. Rollback total

Si el programa debe cancelarse:

```bash
rm -rf "TM_TRABAJO_TEMPORAL/TM_PROGRAM_INTEGRAL_V1"
```

Eso elimina únicamente los artefactos nuevos. No toca ningún original ni la auditoría previa (`FREEBUFF_AUDIT_V219`).

## 3. Rollback por fase

Cada fase debe escribir en su propia carpeta y dejar un manifiesto con:

- archivos creados;
- hashes;
- comandos ejecutados;
- resultado de gates;
- versión.

Para revertir una fase sin afectar a las demás:

```bash
rm -rf "TM_TRABAJO_TEMPORAL/TM_PROGRAM_INTEGRAL_V1/<carpeta_de_fase>"
```

Nunca se borra `00_INPUTS/INPUT_MANIFEST.json` ni este plan.

## 4. Verificación de integridad antes y después de cada fase

```bash
sha256sum \
  "TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md" \
  "TM_CANON_ACTIVO/02_TICKS/TM_TICKFEED_1615_1730.csv" \
  "TM_CANON_ACTIVO/03_LECTURAS_HUMANAS/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v005.txt"
```

Debe coincidir con:

```text
94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17
5F701BE2307352CB559ABBD7BB856A6FD2A1F91E5D269A93DCC9AE2992E2C9FF
F5D7550C42C90897D833E6C2A3FAF772753A129640FD4411DE4190CB2CF94226
```

## 5. Regla de oro

Si un comando pudiera escribir fuera de `TM_PROGRAM_INTEGRAL_V1/`, se detiene y se revisa antes de ejecutarlo. Ninguna fase tiene autorización para modificar los originales, ni siquiera para «corregir» un manifiesto.
