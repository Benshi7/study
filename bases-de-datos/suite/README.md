# Suite de estudio

Abrir `suite/index.html` directo desde el disco: no necesita servidor ni build.

| Archivo | Qué es | A mano o generado |
|---|---|---|
| `data/bank.js` | Preguntas y lista de lecciones | **Generado** por `node suite/build-bank.mjs` desde los quizzes de `lessons/*.html` |
| `data/content.js` | Mapa de ideas, fichas, clasificadores, frases | **A mano**, sale de los decks |
| `data/exercises.js` | Los 31 ejercicios del Constructor SQL | **Generado** por `node suite/build-exercises.mjs` desde `practica/suministros.html` |
| `builder.js` | Constructor SQL: arrastrar piezas a SELECT/FROM/WHERE… y corregir | A mano |
| `suite.js`, `suite.css`, `index.html` | La app | A mano |

## Cuando llega un deck nuevo (.pptx)

1. `python3 -I suite/extract-pptx.py raw /tmp/decks` y leer el Markdown.
2. En `data/content.js`:
   - `CONCEPTS`: un objeto por idea (`def` textual del deck; `trap` si hay una confusión típica; `lesson`/`ref` si existen). Respetar la grilla de `x`/`y` y no pasar de ~18 caracteres en `label`.
   - `EDGES`: conectar cada concepto nuevo con al menos uno existente. Una etiqueta de arista dice qué relación hay.
   - `EXTRA_CARDS`: definiciones textuales y casos numéricos que no merecen un nodo.
   - `DRILLS`: sólo si hay una familia de conceptos que se confunden entre sí.
3. Si el deck abre un bloque nuevo, agregarlo en `CLUSTERS`, en `BLOCKS` de `suite.js`, en `BLOCK_BY_LESSON` de `build-bank.mjs` y como `--c-<bloque>` en `suite.css`.
4. Si escribís lecciones con quizzes: `node suite/build-bank.mjs`.

Las lecciones son la fuente de verdad del banco de preguntas; no se edita `bank.js`.
El progreso por lección se guarda al responder todos los quizzes de la página
(`assets/quiz.js`, clave `bd-quiz:<lección>`); lo demás, en `bd-suite:*`.

## Constructor SQL

Vista `#armar`. Las piezas (tablas, columnas, JOIN por clave foránea, valores) se leen de la base
real con `PRAGMA`, así que si cambia `assets/seeds/suministros.js` la paleta se actualiza sola.
Corrige con el mismo motor y la misma comparación que `assets/sqlbox.js` (`window.SQLBox`).
Tiene dos conjuntos: SUMINISTROS (`practica/suministros.html`) y Slow Change Dimension (`lessons/0052-*.html`). Para sumar ejercicios: agregarlos en esas páginas como bloques `sqlbox` y correr `node suite/build-exercises.mjs`; para un conjunto nuevo, agregarlo a `SETS` del script y cargar su seed en `index.html`. Entran los SELECT y los `CREATE VIEW` (el constructor envuelve el SELECT); los DML (UPDATE, INSERT…) se escriben a mano y el script los lista como omitidos.
Necesita internet la primera vez (SQLite WASM desde cdnjs); después queda en la caché del navegador.
