# El alcance real del 1er parcial, y por qué los modelos de parcial engañan

Llegaron tres fuentes que fijan el alcance del parcial del **24/09/2026** con mucha más
precisión que el cronograma: las **pautas que dio el docente en clase** el 17/09
(`raw/PAUTAS_EXAMEN.md`), el deck de la última clase (`raw/Clase Indices y Txn .pptx`, que
internamente se titula "Clase 4") y la carpeta `raw/Material_Examen/` con los PDF por unidad
y dos modelos de parcial. Cruzarlas corrige el plan que se había armado a partir del parcial
que le pasó un compañero.

## Lo que se descubrió al cruzar las fuentes

1. **El parcial del compañero salía íntegro de un solo PDF: `unidad 4 DDL.pdf`.** No era una
   muestra representativa, era ese archivo convertido en examen. Está textual:
   `ALTER TABLE Curso drop duración` es la página 6, y el procedimiento
   `Desa_ETL_ADMIN.GET_LOAD_ID` que pedía explicar es la página 9, carácter por carácter.
   Las restricciones de la pregunta 3 son las páginas 2 a 5.

2. **Los docentes confirmaron que triggers, store procedures y DDL quedan diferidos al 2do
   parcial.** Eso vacía cuatro de las diez preguntas de ese modelo. El deck de la última
   clase no menciona ni procedimientos ni disparadores, y las pautas tampoco los listan
   entre los temas de teoría. Las lecciones `0029` y `0031` salen del plan del 1er parcial.

3. **`bd parcial 1a.jpg` y `1b.jpg` tampoco son un 1er parcial.** Piden componentes de un
   **Datawarehouse** (Unidad 9), la instrucción `EXISTS`, vistas y SQL sobre tablas de
   proveedores y envíos (Unidad 5). Son de un examen posterior. Útiles como práctica
   diferida, inútiles como predicción.

4. **Lo único confirmado por tres fuentes independientes es índices.** El docente dio la
   pregunta textual en clase ("¿cuál de todos los índices ordena físicamente los campos?"
   → el agrupado, más el "justifique"); las pautas piden "nombre de los tipos y para qué
   sirve cada uno, qué beneficio tiene cada uno"; y `bd parcial 1a` pregunta "Explique cada
   tipo de Índices: Agrupados, Principal y Secundarios. De un ejemplo". Cuando tres fuentes
   que no se hablan entre sí coinciden, eso es lo que se estudia primero.

5. **El material de índices se contradice consigo mismo, y hay que enseñar la contradicción.**
   Las páginas del índice principal lo definen como el de la clave primaria y le dan la
   unicidad; el ordenamiento físico se lo adjudican al agrupado. Pero el párrafo de
   denso/no denso está copiado textual de Elmasri p. 431, donde el principal *sí* implica
   que el fichero está ordenado por esa clave. Quien razone desde ese párrafo contesta
   "principal" y se lo marcan mal.

6. **Apareció el origen de "Precio_R", que quedaba sin explicar.** `unidad 3.pdf` p. 4 lo
   rotula como **atributo derivable** y da la fórmula: `Pcio R = Cant x P Unit`. O sea que
   la columna rara del ejercicio de normalización es la trampa del **error nº 1 que el
   docente dice que marca siempre**: modelar los campos calculados. Y la p. 11 tiene el
   modelo 3FN canónico de la cátedra, que ya estaba en la lección `0023`:
   `CabeceraFact (#NFact, Fecha, CodCli)` · `RenglonFact (#NFact, #CProd, Canti, Punit)` ·
   `Prod (#CProd, Descri)` · `Cli (#CodCli, NomCli)`.

7. **Entró un tema que no estaba en el radar: transacciones y ACID.** Es Unidad 6 en el
   programa, pero el docente las dictó al final de la clase de índices y las pautas dicen
   que "en algún parcial tomó las definiciones de ACID". De ahí la lección `0041`.

## Implicaciones para las próximas sesiones

- **Ningún modelo de parcial se toma a rajatabla.** Se cruza contra las pautas y contra el
  deck de la clase antes de darle peso. Lo que no esté en el material dictado, se marca
  como **diferido** y se practica después del parcial, no antes.
- **Teoría y práctica se aprueban por separado**, sin promediar. Y el docente dijo cuál es
  el perfil que desaprueba: el que ya trabaja con bases de datos, saca la práctica fácil y
  no estudia la teoría. Ése es exactamente el perfil de Bruno, así que la teoría va primero
  aunque la práctica se sienta más urgente.
- **Falta lo práctico a mano.** El parcial es en papel, una hora, sin ERDPlus. Queda
  pendiente la `0018` (modelar un MER desde un enunciado, dibujando) y la notación de
  memoria: doble elipse, elipse punteada, cardinalidades, pata de gallo. El docente nombró
  libros, autos, **farmacia** y celulares como enunciados posibles, y el TP1 de Farmacia
  con su resolución ya está en `raw/`.
- **`PARCIAL.md` es la superficie de estudio** y se mantiene al día con cada fuente nueva.
  `CURRICULUM.md` sigue siendo el contrato de las nueve unidades: no se le quita nada,
  sólo se marca qué entra en qué parcial.
