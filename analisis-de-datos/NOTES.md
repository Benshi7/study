# Notes

## Preferencias del estudiante
- Habla en español rioplatense. Las lecciones van en español neutro, porque el examen es en español y hay que usar la terminología de la cátedra.
- Piensa en **modelos mentales**: árboles, tablas de decisión, "qué pregunta responde cada cosa". Tiene el plugin `diagram-design` disponible si un tema necesita un diagrama más elaborado.
- Si una respuesta aproximada está cerca de lo correcto, le sirve. Si se desvía mucho, avisarle.
- Trabaja como **Data Engineer**: tiende a responder con el criterio de la industria (SCD, profiling con % de nulls, etc.). Siempre marcar la diferencia entre ese criterio y el de la cátedra.
- Los casos de éxito no son ni más ni menos importantes que el resto. El libro opcional no se lee.
- Quiere que las lecciones sigan el formato de la skill `teach`: HTML en `lessons/`, referencias en `reference/`.

## Formato del parcial (lo que se sabe)
- Online, probablemente choice, parecido al cuestionario de Moodle de la Unidad 1.
- Además de la Unidad 1, van a sumar preguntas de los ejercicios (notebooks, Kahoot).
- La clase de repaso del 21/09 se suspendió (Día del Estudiante): **no dieron pistas**.
- **Mensaje del docente (confirmado):** el parcial es el lunes 28/09 y solo entra lo visto en clase: Introducción a los Datos, Introducción y Taller de SQL, e Introducción y Taller de Python. Está orientado a **comprender los conceptos y el código**. Puede traer:
  - análisis de código y de consultas SQL;
  - **escritura de consultas básicas**;
  - ejercicios sencillos de Python;
  - preguntas teóricas.
  Las consignas pueden ser multiple choice, **a desarrollar**, **para completar** u otras. Hasta ahora se practicó sobre todo reconocimiento (choice): falta práctica de producción, es decir, escribir consultas y código, y definir conceptos con las palabras de la cátedra.
- `raw/KAHOOT-ALUMNOS.pdf` tiene las preguntas reales del Kahoot de Python con la respuesta de la cátedra, por ejemplo "¿cuál es un IDE?" → PyCharm (no Jupyter ni Colab). Es el mejor predictor que tenemos para el bloque Python.

## Notas de trabajo
- Entorno WSL. Para abrir HTML: `explorer.exe "$(wslpath -w <archivo>)"`.
- Hay que pasar por OCR muchos slides que son imágenes: `lit parse <pdf> --ocr-language spa`. Para confirmar un slide puntual: `lit screenshot <pdf> --target-pages N --dpi 110`.
- Los slides dicen **"Configuración"** (no "Conformidad"), **"Tempestividad"** e **"Integridad"**. Binarias va dentro de **Cualitativos**.
- Bloque Python hecho (lecciones 0007 a 0011). Las salidas de los quizzes se verificaron ejecutando el código (hay un venv con pandas en el tmp del job, que se borra al cerrarlo).
- Bloque SQL hecho (lecciones 0012 a 0015). Las salidas de las preguntas se verificaron con SQLite.
- **Suite de estudio** en `suite/`: app vanilla sin build (`suite/index.html`). El banco de preguntas se GENERA desde las lecciones: después de editar o agregar una lección, correr `node suite/build-bank.mjs`. El contenido del mapa, las fichas y los clasificadores está en `suite/data/content.js`. El estado del usuario vive en localStorage con prefijo `adi-suite:`; el progreso de las lecciones se lee de `teach-quiz:`.
- **Diagramas** en `diagrams/` (skill diagram-design, perfil `adi-unicaba` en `~/.diagram-design/profiles/`, seleccionado por `.diagram-design`). Se generan con `python3 diagrams/build.py`: escribe una página por diagrama, la galería, y los inserta en las lecciones entre marcadores `<!-- diagram:slug -->` (el build es idempotente). Estilos en `assets/diagrams.css`, con tokens para claro y oscuro. Para agregar uno: una función `@diagram` más en `build.py`.
- **Temas de las lecciones:** `assets/course.css` tiene dos skins por tokens, **Rosa** (por defecto, estética de la suite) y **Sepia** (Tufte original), cada uno con modo claro y oscuro. `assets/theme.js` (cargado en el `<head>` de lecciones, referencias e índice) setea `data-skin` y `data-theme` en `<html>` y los guarda en `adi-suite:skin` / `adi-suite:theme` (la clave de modo es la misma que usa la suite). Páginas nuevas: linkear course.css + theme.js.
- Colores de la suite: blanco y rosa frambuesa (#D81B72) / ciruela y rosa (#FF5FA2) en modo oscuro. No se pudieron verificar los colores oficiales de UNICABA: el sitio no respondía y los slides usan azul marino y naranja.
- Workflow acordado: una lección, después un chat nuevo con `/teach` pasando puntaje y preguntas falladas. Se charla solo lo que falló, no página por página.

## Bloque 4: EDA (desde 19/10)
- Profe nuevo, material en `material_eda/`. Lecciones 0016 a 0021 + `reference/eda.html`. Las lecciones de notebooks traen `<details class="answers">` con respuestas guía para las preguntas ✍️ (estilo en `course.css`).
- Todos los números se verificaron ejecutando el código con pandas 3 en un venv temporal. En Colab (pandas 2.x) `area error` sale `object`, no `str`.
- Trampas detectadas: la lámina calcula cuartiles de 2,4,4,6,10 como Q1=3/Q3=8 (pandas da 4/6) y desvío 2,68 (da 2,71 poblacional o 3,03 muestral). La infografía de Gemini tiene errores. `target` 0 = maligno, pero en el notebook 8 `maligno` 1 = M (el signo de la correlación se invierte).
- Vocabulario: el profe de EDA dice categóricas/numéricas (Unidad 1: cualitativos/cuantitativos) y "problemas en los datos" en vez de dimensiones de calidad. Se agregaron puentes en 0001, 0006, 0011 y `reference/datos-y-analisis.html`.
- La suite tiene un bloque `eda` (lecciones ≥ 16) en `build-bank.mjs` y `suite.js`.
