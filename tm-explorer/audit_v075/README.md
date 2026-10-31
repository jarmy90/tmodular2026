# Auditoria v0.7.5 - entrega audit2

Esta entrega audita el motor `TM_CORE_PYTHON_v075_STREAMING.py` (v0.7.5) sin modificarlo.
Resultado global: **auditoria completa, no apto para AFS2 en produccion**.

## Contenido

- `motor/`: motor v0.7.5, tests originales y reportes oficiales.
- `audit_v075/`: scripts de auditoria (build, prefijos fisicos, finalizacion).
- `out_v075_audit2/`: resultados canonicos A00-A22, P00-P03, R00 y evidencia de ejecucion.
- `datos/`: feeds de entrada, lecturas confirmadas y arbol canonico usados.
- `tests/`: tests de auditoria del paquete.
- `HASHES.sha256`: hashes SHA-256 de los archivos de contenido; excluye `HASHES.sha256` y `MANIFEST.json`.
- `MANIFEST.json`: inventario, tamanos y hashes.

## Resultado ejecutivo

| Dimension | Resultado |
|---|---|
| Regresion tramo comun | PASS, 873 eventos y 67 lecturas exactas |
| R0062 anterior -> R0064 ampliado | PASS, 26 eventos y geometria exacta |
| Prefijos fisicos | PASS, 3327/3327, 0 fallos |
| Prefijos dentro de R0062 | PASS, 1782/1782 |
| Golden humano 16:15-16:22 | 1/8; fallan 16:15, 16:16, 16:17, 16:19, 16:20, 16:21, 16:22 |
| GAP canonico | 12 GAP espurios con `|gap| < 0.25` |
| Estados finales FT | 0/37 canonicos; el motor usa `CONFIRMADO` |
| Integridad fin de feed | 72 movimientos no explicados sin `PENDIENTE_POR_REGLA` |
| Cobertura funcional causal | 2166/2238 |
| Owner de ticks | 19901/20335; 434 sin owner |
| Reglas TM abiertas | 9; no se cierran por inferencia |

## Lectura correcta

El motor es causalmente estable y reproduce exactamente el tramo comun y la geometria de R0062.
No obstante, no cumple la semantica canonica completa: GAP, plano, lecturas humanas, estados finales FT,
integridad de fin de feed y cobertura funcional siguen abiertos.

La fuente de verdad es `R00_Readiness.json`; los veredictos estan separados para no confundir
causalidad, geometria, cobertura y disponibilidad AFS2.
