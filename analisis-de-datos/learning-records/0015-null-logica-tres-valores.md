# = NULL devuelve 0 filas: lógica de tres valores

En la lección 0014 le fue bien, salvo en `SELECT * FROM clientes WHERE email = NULL`: "me comí el bait". La respuesta es 0 filas. No da error, porque la sintaxis es válida. `email = NULL` evalúa a UNKNOWN, no a TRUE, y WHERE solo deja pasar las filas en TRUE. Con `IS NULL` devolvería 1 fila (Beto).

**Evidence:** 27/09, lección 0014. Dijo que entiende por qué está mal.

**Implications:** Es un error de atención, no de concepto (igual que la FK de la estrella en [[0014-medallion-transformacion-en-capa-destino]]). Patrón: en las preguntas de "¿qué devuelve?", lee rápido y va a la respuesta intuitiva. Consejo para el examen: si en el código aparece NULL, frenar y revisar el operador. Volver a preguntarlo en el simulacro.
