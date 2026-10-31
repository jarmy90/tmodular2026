RESUMEN_PROVISORIO_DEL_TRABAJO

1. Objetivo entendido:
llevar a su extrema consecuencia el desarrollo del árbol TM y un
intérprete Python de referencia sobre la base acordada, avanzando
transición por transición y empaquetando cada iteración como entregable
revisible sin modificar los originales protegidos.

2. Parte del proyecto analizada:
se centró en la capa de referencia construida sobre el árbol
v2.19 acumulado, especialmente en el núcleo 1/2/3/módulo y en las
transiciones hacia B Grande, AUT por B y AUT directo por A, junto con
las políticas experimentales asociadas que fueron retiradas o
reclasificadas.

3. Decisiones funcionales aplicadas:
- mantener el árbol como autoridad y el Python como referencia;
- separar las vías AUT por B y AUT directo por A;
- retirar la política experimental de salto de 4 puntos;
- clasificar las pruebas dependientes de esa política como
  experimentales retiradas;
- conservar el núcleo 19/19 y las anclas como regresiones base;
- tratar el AUT directo por A como gate de intérprete, no como
  congelación del árbol ni como motor oficial.

4. Código escrito:
- intérprete de referencia para el núcleo;
- intérprete para A/B candidata;
- intérprete para B Grande + AUT por B;
- intérprete para AUT directo por A;
- scripts de prueba conceptual;
- scripts de empaquetado por iteración;
- script de verificación de ZIP;
- varios manifiestos y verificaciones de integridad.

5. Documentos generados:
- checkpoints por iteración;
- trees ejecutables;
- especificaciones de transición;
- matrices de pruebas;
- reglas abiertas;
- informes de correcciones y checkpoints intermedios.

6. Scripts auxiliares creados:
- builders de iteración;
- runners de pruebas;
- verificador de ZIP;
- scripts de manifiesto y checksums.

7. Scripts ejecutados:
- varios builders e inspectores durante la intervención;
- al menos una ejecución final que produjo el ZIP de revisión 08;
- verificaciones de existencia de archivos y de integridad del ZIP.

8. Pruebas ejecutadas:
- pruebas conceptuales del núcleo;
- pruebas conceptuales de A/B candidata;
- pruebas conceptuales de B Grande / AUT por B;
- pruebas conceptuales de AUT directo por A;
- verificaciones de determinismo y regresiones base.

9. Resultados obtenidos:
- el núcleo y los bloques superiores atravesaron sus gates
  correspondientes;
- el AUT directo por A quedó preparado como versión de referencia;
- se construyeron dos versiones del empaquetado 08, una incompleta y
  otra con ZIP verificado pero con una diferencia menor de conjunto;
- el ZIP final tiene todos los hashes por miembro coincidentes,
  aunque el verificador externo detectó un desacuerdo menor de
  comparación de conjuntos.

10. Partes abiertas:
- congelación del árbol no autorizada;
- motor oficial no declarado;
- reglas centrales pendientes;
- zonas de gap, concurrencia interna, integración de módulos y
  ciclo general de 1 aún no cerradas en esta capa.

11. Parte provisional:
- el empaquetado 08 usado como entrega de trabajo;
- la diferencia de conjunto reportada por el verificador externo;
- la doble copia del intérprete en rutas distintas;
- cualquier script auxiliar no yet reclasificado.

12. Parte confirmada:
- los archivos base protegidos no fueron modificados;
- los resultados de regresión base se conservaron como anclas.

13. Reglas TM cambiadas:
no se cambió el árbol v2.19 ni las reglas canónicas protegidas.

14. Políticas experimentales introducidas o reclasificadas:
- se retiró la política experimental de salto de 4 puntos;
- se reclasificaron pruebas dependientes;
- se mantuvieron políticas experimentales marcadas como tal en los
  documentos de reglas abiertas.

15. Archivos promovidos o declarados oficiales:
no se declaró oficial ningún archivo nuevo; todo quedó dentro del
espacio de referencia y entregas provisionales.

estado_actual:
la auditoría sigue en curso.
