# LECTURA_NO_REPRODUCIDA — diagnóstico R2

## Primera divergencia funcional

- Vela: 16:23.
- Secuencia golden de referencia: 1879 (máximo B, precio 29852,6).
- Primer cruce físico del inicio de A: sequence_id 1876, precio 29851,4.
- Estado previo: A bajista confirmada; comienza/continúa B alcista.
- Golden esperado: AUT alcista cuando B supera el inicio de A.
- Regla aplicada: AUT por B solo cuando B supera 127% de A + 0,25.
- Raw del motor: A=7,50 puntos; B=8,60 puntos; umbral=9,77 puntos; AUT alcista no emitido.
- Clasificación: contradicción entre decisión experta vigente y expectativa humana v003. El motor no fuerza AUT ni cambia el golden.

La diferencia entre 1876 y 1879 no es por sí sola un error de causalidad: 1876 es el primer cruce; 1879 es el máximo. La divergencia funcional es que ese cruce no satisface el umbral universal vigente.

## Efecto aguas abajo

Al no confirmarse el AUT alcista que v003 usa como nuevo módulo, la salida no produce la genealogía AUT bajista de 16:23 ni la cadena A/B/AUT esperada en 16:24.

## Regla ausente o infringida

Ninguna regla del motor se omitió para el disparo B. El núcleo aplicó el umbral vigente. El golden v003 conserva una expectativa incompatible con ese umbral en este tramo. No se modifica el golden y no se declara conformidad.
