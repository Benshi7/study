# En un JOIN, la izquierda es la tabla del FROM, no la del ON

En el simulacro inventado (bloque 2) falló un par de preguntas de JOIN, y en el segundo intento le fue mejor. Tenía un concepto equivocado: creía que la izquierda y la derecha se leen en el ON y que el orden del FROM "da igual". Es al revés.

**Evidence:** 27/09 a la noche. Se verificó con SQLite: invertir el orden del ON da el mismo resultado; invertir el FROM cambia el resultado (Oli con NULL vs RRHH con NULL). En Python falló `s[0:2]`: creyó que incluía el índice 2.

**Implications:** Hay que repasarlo el lunes a la mañana. La tabla de la izquierda es la del FROM, antes de JOIN; la de la derecha, la que va después de LEFT JOIN; el ON solo dice cómo emparejar. Se agregó un recuadro de trampa en la lección 0015. El slicing sigue la misma regla que range: el final no se incluye.

**Chequeo 27/09 (falló):** en `FROM facturas f LEFT JOIN clientes c ON c.id = f.cliente_id` respondió que se conserva clientes; es facturas. Sigue anclado en "clientes es siempre la izquierda" o en el primer nombre del ON. Se le dio la lectura literal: la tabla que queda a la izquierda de la palabra JOIN en la línea. Volver a chequearlo antes de cerrar.

**Verificado 28/09:** en `FROM areas a LEFT JOIN empleados e` respondió bien que se conserva areas. Lectura literal incorporada.
