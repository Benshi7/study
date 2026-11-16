# remove(x) saca la PRIMERA aparición del valor; pop(i) saca por posición

En la lección 0008 le fue bien. Falló la 11 por comerse el bait, aunque dice que la sabe. Preguntó qué pasa con los repetidos: "¿el pop elimina todos los 3?". Mezcló pop con remove.

**Evidence:** 27/09, verificado con Python:
- `[3,8,3,6].remove(3)` → `[8,3,6]`
- `pop()` devuelve el último (6)
- `pop(0)` devuelve el primero
- `remove` de un valor que no está → `ValueError`

**Implications:** Las listas admiten repetidos. `remove` trabaja por valor (solo la primera aparición), `pop` trabaja por índice (sin argumento, el último) y devuelve el elemento. Para sacar todos los repetidos hace falta una comprensión o un bucle. Es una trampa probable de "¿qué imprime?": diferenciar valor de posición.
