ITERACION_08_DIRECT_AUT - BUILD_COMMIT_REASON

estado: ZIP no producido en este ciclo
razones documentadas:

1. build_iteration_08.py no esta en la ruta ejecutada hoy.
   No hay forma de invocarlo con la rutina actual de ejecucion;
   la carpeta 13_ITERATION_PACKAGES no esta representada en la
   sesion activa en este momento y el archivo build_iteration_08.py
   no se puede ejecutar aqui.

2. La comprobacion de existencia del ZIP muestra que
   TM_ITERATION_08_REVIEW.zip no esta presente en
   TM_ENTREGAS_ITERACION al final del ciclo.

3. La carpeta plana
   TM_ENTREGAS_ITERACION/ITERACION_08_DIRECT_AUT_20261030_1826
   existe, pero el chequeo de integridad del ZIP no se pudo completar
   en esta ejecucion porque no hubo ZIP que verificar.

4. El marker de ejecucion build_08_running_indicator.txt no se pudo
   acceder de forma confiable en este ciclo, lo que confirma que la
   ejecucion activa del builder no esta visible en la sesion actual.

accion explicita recomendada:
no intentar reconstruir hasta disponer de una sesion donde
el archivo build_iteration_08.py este realmente ejecutable y la
carpeta TM_TRABAJO_TEMPORAL/TM_TREE_AND_REFERENCE_ENGINE_V1/13_ITERATION_PACKAGES
este accesible con escritura.

contenido disponible:
carpeta plana 08 existe
ingresos esperados documentados en DELIVERABLES_ITERACION_08_CONFIRMACION.md
reglas de gate documentadas:
GATE_AUT_DIRECT_BY_A_PASS
NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_INCOMPLETE
