# Agregado en WHERE: error; el filtro sobre SUM va en HAVING, después de GROUP BY

En el simulacro de escritura, consigna 1 (total por cliente mayor a 60), escribió:

```sql
SELECT * FROM clientes c
LEFT JOIN facturas f ON c.id == f.cliente_id
WHERE SUM(total) > 60
```

Tiene cuatro problemas:
- Usa SUM en WHERE: SQLite devuelve "misuse of aggregate function SUM()".
- Le falta el GROUP BY.
- Usa `SELECT *` con una agregación.
- Usa `==`, que funciona en SQLite pero no es SQL estándar; hay que escribir `=`.

La idea del JOIN es válida si se quiere mostrar el nombre del cliente. Verificado con SQLite: INNER JOIN + GROUP BY c.id, c.nombre + HAVING devuelve (1, Ana, 150) y (2, Beto, 80).

**Evidence:** 28/09. En el choice sabía que "WHERE filtra filas y HAVING filtra grupos", pero al escribir la consulta no lo aplicó. Es la brecha entre reconocer y producir que anticipó el aviso del profe.

**Implications:** Antes de escribir, preguntarse "¿el filtro es sobre un agregado?". Si lo es, va GROUP BY + HAVING. Si hay agregación, el SELECT lleva solo las columnas del GROUP BY y los agregados. Volver a pedirle una consulta con HAVING escrita a mano.
