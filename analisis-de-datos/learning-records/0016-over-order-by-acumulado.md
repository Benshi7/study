# ORDER BY dentro de OVER = acumulado; OVER () vacío = total general

En la lección 0015 falló dos preguntas de ventanas:
- `SUM(total) OVER (ORDER BY fecha)` en la tercera fila de 100, 80, 50, 20: marcó 250 (el total general); la respuesta es 230 (acumulado). Además el enunciado era confuso, porque no mostraba la columna fecha.
- `LAG(total)` en la primera fila: marcó 0; la respuesta es NULL. Dijo que lo entendió.

**Evidence:** 27/09, lección 0015. Verificado con SQLite: acumulado 100/180/230/250; `OVER ()` da 250 en todas las filas; LAG da None, 100, 80, 50.

**Implications:** El concepto que faltaba es que el ORDER BY dentro de OVER define el marco hasta la fila actual (acumulado), mientras que `OVER ()` vacío toma todas las filas. En LAG/LEAD, cuando no hay fila vecina el resultado es NULL, no 0: va con el patrón de NULL de [[0015-null-logica-tres-valores]]. Se reescribió el enunciado de la pregunta 10 (ahora con fechas explícitas) y se amplió el párrafo de ventanas de la lección 0015.
