# continue saltea UNA vuelta; break corta el bucle

En la lección 0010 falló solo "¿cuántos números imprime?" en un `for i in range(6)` con `if i == 2: continue`. Marcó 3; la respuesta es 5 (0, 1, 3, 4, 5). Dice que lo entendió.

**Evidence:** 27/09, lección 0010, verificado con Python: con continue imprime [0, 1, 3, 4, 5]; con break, [0, 1].

**Implications:** Hay que contrastar continue y break, y recordar que range(6) va de 0 a 5 (6 números). Volver a preguntarlo en el simulacro. El resto de la 0010 (try/except, imports) quedó OK.
