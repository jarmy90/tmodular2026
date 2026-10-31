# TM Explorer - instrucciones maestras

## Mision
Construir y validar un motor determinista de Teoria Modular (TM) que procese ticks en orden temporal, sin datos futuros, sin memorizar el dataset y sin consultar el golden desde el nucleo.

## Autoridad y fuentes
Javier es la fuente experta final de TM. Los agentes no inventan reglas ni convierten una hipotesis en regla cerrada.

Leer en este orden cuando existan los archivos:
1. `control/00_LEEME_PRIMERO_PRIORIDAD_DOCUMENTOS_TM.txt`
2. `control/DECISIONES_EXPERTO.md`
3. `control/REGLAS_CERRADAS.md`
4. `dossier/Dossier_TM_v3_Lectura_Obligatoria.txt`
5. `dossier/Dossier_TM_v4_Concurrencia_Reclasificacion.txt`
6. `control/REGLAS_PROVISIONALES.md`
7. `control/CONTRADICCIONES.md`
8. `control/DICCIONARIO_TM.md`

Si falta un archivo, registrarlo como pendiente. No sustituirlo por una version historica.

## Reglas cerradas esenciales
- TM lee movimientos, no colores de velas.
- El cambio de vela no termina automaticamente un movimiento.
- Una vela puede contener varios movimientos.
- Pueden coexistir varias lecturas mientras sigan siendo matematicamente validas.
- El movimiento contrario a A Grande comienza como B Grande candidata.
- Antes del 100 % de A Grande sigue siendo B Grande candidata.
- Al alcanzar al menos el 100 % de A Grande, sin superar `127 % + 0,25 puntos`, se confirma B Grande.
- Una vez confirmada B Grande, todo movimiento posterior contrario a B Grande es C Grande, no C Grande candidata.
- Si el mismo recorrido supera `127 % + 0,25 puntos`, deja de ser B Grande y se confirma AUT inmediatamente.
- Una vela que alcanza AUT puede ser simultaneamente un 1 y un TT pequeno.
- Velas posteriores pueden completar el TT del 1 original.
- Retrocesos posteriores pueden reclasificar conjuntamente velas previas como modulo o como 1.
- Reclasificar no significa borrar la cronologia anterior.
- B Grande y AUT no coexisten: al superar `127 % + 0,25 puntos`, el recorrido deja de ser B Grande y se confirma AUT.
- Orden causal de la regla de 2: apertura nueva -> gap -> (si no hay gap) salida en plano <= 0,25 respecto del cierre de la VELA anterior -> cola observable <= 0,25 -> posible 2 -> 2 confirmado al alcanzar el tamano direccional de 1. Con gap no hay salida en plano, ni posible 2, ni 2.

## Gate Cero
`core-tm-engineer` no implementa una regla TM si esa regla esta abierta, provisional o contradictoria.

Antes de programar:
1. Reconstruir movimientos.
2. Separar hechos, inferencias y dudas.
3. Formular una sola pregunta concreta a Javier cuando exista bloqueo.
4. Registrar la respuesta literal en `control/DECISIONES_EXPERTO.md`.
5. Convertirla en regla general.
6. Escribir primero el test rojo.
7. Implementar despues.
8. Ejecutar regresion desde el primer tick.

## Golden y anti-spoiler
- El golden es externo y provisional hasta validacion experta.
- El golden no es fuente de reglas.
- `src/core/` no puede leer `golden/`, fixtures esperados ni resultados futuros.
- Si el golden contradice una decision experta, prevalece la decision experta y se marca el golden para revision.

## Prohibiciones
- No usar `B_EXCESIVA`.
- No clasificar por color de vela.
- No hardcodear precios, fechas, simbolos, numero de vela ni resultados del golden.
- No usar ticks futuros.
- No programar reglas provisionales.
- No extraer reglas de `historical/` salvo auditoria expresamente encargada.
- No modificar simultaneamente el mismo archivo desde dos agentes.

## Orquestacion
- El orquestador asigna un propietario unico por artefacto.
- Paralelizar solo tareas independientes.
- Comprension en paralelo: `rules-analyst`, `movement-reconstructor`, `data-auditor`.
- Sintesis posterior: `scene-questioner`, `tm-reviewer`.
- Implementacion secuencial: `tdd-guide` y luego `core-tm-engineer`.
- Validacion final independiente: `e2e-validator` y `tm-reviewer`.
- Cada resultado debe indicar archivos leidos, evidencia, dudas, cambios y estado del Gate Cero.

## Verificacion minima
Tras cada cambio:
1. Tests unitarios.
2. Replay desde el primer tick.
3. Identificacion del primer tick de desviacion.
4. Revision anti-spoiler.
5. Revision de vocabulario TM.
6. Registro de regresiones.

Nunca declarar exito sin mostrar los comandos ejecutados y sus resultados reales.
