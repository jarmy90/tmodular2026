# TM_CANON_v2_13_PROPUESTA_R1

Estado: `CANDIDATO_PENDIENTE_AUDITORIA_MIMO_Y_APROBACION_JAVIER`. El arbol aprobado sigue siendo v2.12.

Archivos principales:
- `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA_R1.md`
- `DIFF_v2_13_inicial_a_R1.diff` (UTF-8/LF); arbol inicial exacto en `source/`
- `TM_v2_13_REGLA_A_GOLDEN.csv` (16:23 como NO PLANO)
- `TM_v2_13_REGISTRO_GOLDEN_HUMANO.csv` (etiqueta literal `[A/B]`)
- `DECISION_AUTORIDAD_PLANO_GAP_JAVIER.md`
- `INFORME_CAMBIOS_R1.md`, `manifest.json`, `SHA256SUMS.txt`

## Aplicacion exacta del diff en PowerShell

Ejecutar desde la raiz extraida del ZIP (requiere Git en PATH):

```powershell
$pkg = (Get-Location).Path
$work = Join-Path $env:TEMP ("tm-v213-r1-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $work | Out-Null
Copy-Item -LiteralPath (Join-Path $pkg 'source/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA_INICIAL.md') -Destination (Join-Path $work 'TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA.md')
$base = Join-Path $work 'TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA.md'
python -c "from pathlib import Path; p=Path(r'$base'); p.write_bytes(p.read_bytes().replace(b'\r\n',b'\n').replace(b'\r',b'\n'))"
Push-Location $work
git -c core.autocrlf=false apply --ignore-space-change --ignore-whitespace (Join-Path $pkg 'DIFF_v2_13_inicial_a_R1.diff')
Pop-Location
Move-Item -LiteralPath (Join-Path $work 'TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA.md') -Destination (Join-Path $work 'TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA_R1.md')
Get-FileHash -Algorithm SHA256 (Join-Path $work 'TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA_R1.md')
```

El resultado debe coincidir con el SHA-256 del arbol R1 registrado en `manifest.json`.

No incluye motor ni modifica golden, feed, reglas pendientes, tests o legado.
