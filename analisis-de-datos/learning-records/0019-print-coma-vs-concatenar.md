# print con coma separa con espacio; + concatena sin espacio

En la lección 0009 dudó si `print("Hola", nombre)` imprime "HolaAna". Imprime "Hola Ana": el `sep` por defecto de print es un espacio. Con `+` se concatena sin espacio. En el primer intento falló 3 o 4 preguntas; en el segundo, bien. Dice que lo tiene "más o menos claro" y que necesita releer. En el recall contestó bien input → str (hay que castear con int()) y remove (primera aparición, ValueError si no está).

**Evidence:** 27/09, verificado con Python: "Hola Ana", "HolaAna" y, con `sep=''`, "HolaAna".

**Implications:** La 0009 es la lección más floja hasta ahora. Priorizarla en el repaso del lunes y en el simulacro de la noche. Función sin return → None ya OK.
