# TM_CANON_v2_13_PROPUESTA

Estado: **CANDIDATO_PENDIENTE_APROBACION**. v2.12 continúa como base activa hasta aprobación expresa.

## Contenido

- `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA.md`: propuesta canónica, con normas vigentes separadas de historia y pendientes.
- `DIFF_v2_12_a_v2_13_PROPUESTA.diff`: diff unificado completo contra el v2.12 exacto incluido en `historical/`.
- `TM_v2_13_REGISTRO_GOLDEN_HUMANO.csv`: inventario humano minuto a minuto 16:15–17:29, estados A/B/C/D conservados.
- `TM_v2_13_REGLA_A_GOLDEN.csv`: matriz de evidencia y límites.
- `REGLAS_SUPERADAS.csv`: citas/ubicaciones de fórmulas de plano inclusivas sustituidas por `<0,25`.
- `CONTRADICCIONES_RESUELTAS_Y_PENDIENTES.md`: decisiones editoriales y dudas preservadas.
- `CLASIFICACION_CONTENIDO_v2_12.csv.md`: clasificación del contenido heredado.
- `source/` y `historical/`: copias verificables de documentos de entrada; los originales no se modificaron.

## Estado golden

`A=14; B=13; C=0; D=48; total=75`. 16:15–16:24 queda completo A. 16:30–16:32 y 16:37 conservan A. 16:38–16:39 permanece B parcial. Los tramos restantes mantienen el estado de v003, con la divergencia 16:33–16:36 anotada sin promoción.

## Reproducibilidad

No se ejecutan tests ni se modifica código, motor, golden o feed en Fase 1. Para comprobar SHA-256 desde la raíz descomprimida:

```powershell
Get-Content SHA256SUMS.txt | ForEach-Object { $p=$_.Substring(66); $h=$_.Substring(0,64); if ((Get-FileHash -Algorithm SHA256 $p).Hash -ne $h) { throw $p } }
```

Las entradas físicas del ZIP son las rutas del manifiesto más `manifest.json` y `SHA256SUMS.txt`, controles de archivo.
