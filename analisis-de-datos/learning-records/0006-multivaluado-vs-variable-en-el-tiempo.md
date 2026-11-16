# Atributo multivaluado no es lo mismo que atributo que cambia en el tiempo

Ante la localidad vieja de Jorge Pérez preguntó si el valor, al ser "multivaluado", debería ir en otra tabla. No es multivaluado (en cada momento hay un solo valor): cambia en el tiempo, y en un DW eso se modela como SCD tipo 2. Multivaluado sería, por ejemplo, tener varios teléfonos a la vez, que sí va a otra tabla por la 1FN.

**Implications:** Útil para el bloque SQL (normalización, modelo relacional, dimensiones). No hace falta profundizar en SCD para el parcial.
