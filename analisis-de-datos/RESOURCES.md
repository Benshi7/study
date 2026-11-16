# Análisis de Datos I Resources

## Knowledge

Para este parcial, la fuente de mayor confianza es **la cátedra**: el examen evalúa sus definiciones. Las fuentes externas sirven solo para profundizar.

### Material de la cátedra (fuente primaria)
- [Slides: Introducción, parte 1](raw/001_INTRODUCCION.pdf)
  Big Data (las V, importancia, beneficios), casos UPS / Telefónica-BBVA / Generali, revoluciones industriales, tipos de datos (slide 24). Use for: lecciones 0004 y 0006.
- [Slides: Introducción, parte 2](raw/001_INTRODUCCION_parte_2.pdf)
  Organización data-driven, dimensiones de calidad (slide 3), profiling/cleansing, C-level (slide 12), CDO (13–14), governance, tipos de análisis (24), DIKW, flujo del Data Analyst. Use for: lecciones 0001, 0002, 0003, 0005. **Casi todo son imágenes: hace falta OCR o mirar el slide.**
- [Slides: Introducción, parte 3](raw/001_INTRODUCCION_parte_3.pdf)
  Roles: Business Analyst, Data Viz Specialist, Data Engineer, Data Scientist. Use for: lección 0005.
- [Cuestionario Unidad 1 (Moodle)](raw/Unidad%201%20Cuestionario.md)
  20 preguntas; es probable que reciclen algunas. Use for: práctica final y referencia `reference/cuestionario-unidad-1.html`.
- [Slides: Fundamentos de SQL](raw/unicaba_fundamentos_sql.pdf)
  Tipos de bases de datos, modelo relacional, OLTP/OLAP, estrella, medallion, DDL/DML/DCL/TCL, SELECT básico. Use for: bloque SQL.
- [Taller SQL II (Chinook)](raw/2%20-%20C.I.A%20SQL%20II%20de%20II.docx)
  Agregación, subconsultas, funciones ventana, tablas temporales, índices. Use for: bloque SQL.
- Notebooks y Kahoot: `raw/notebooks/*.ipynb`, `raw/KAHOOT-ALUMNOS.pdf` (escaneado).
  Use for: bloque Python (preguntas trampa de sintaxis).
- [Pautas de cursada](raw/PAUTAS_GENERALES_CURSADA_Y_TP_ACTUALIZADO.pdf)
  Qué entra en el parcial y cómo se aprueba.
- [Programa 2026](raw/programa_2026.pdf) (escaneado: requiere OCR)
  Temario oficial: Tema 1 Intro (ciclo de vida del análisis, identificación de problemas de negocio, roles y perfiles, intro a los datos), Tema 2 SQL (SELECT/INSERT/UPDATE/DELETE; JOIN, GROUP BY, HAVING, subconsultas, agregaciones), Tema 3 Python (sintaxis, listas, diccionarios, Colab; Pandas y NumPy). Los Temas 4 a 7 no entran en el parcial.

### Videos de la clase 1 (casos de éxito)
- [CIO vs CTO: What do these titles mean?](https://www.youtube.com/watch?v=3proO1AtUhE): IT opera sistemas; Ingeniería construye productos.
- [El rol del Chief Data Officer (Raúl Arrabales, Accenture)](https://www.youtube.com/watch?v=7QGuYzlQcg4): evolución de BI hacia analítica avanzada y nacimiento del CDO.
- [Generali Seguros: "Pago como conduzco"](https://www.youtube.com/watch?v=pwXZxZgRT_Q): servicio personalizado con telemática.
- [LUCA Tourism (Telefónica)](https://www.youtube.com/watch?v=bd_Nc1w5zVY): Big Data de red móvil aplicado al turismo.
- [Google Assistant hace llamadas](https://www.youtube.com/watch?v=l9BTMWOupGM): IA conversacional como ejemplo de la 4ª revolución.
- Resúmenes de los videos: `raw/casos-de-exito/*.txt`.

### Externas (para profundizar, no para el examen)
- [DAMA-DMBOK (DAMA International)](https://www.dama.org/cpages/body-of-knowledge)
  Marco de referencia de gestión de datos. La definición de data governance de los slides cita a DAMA. Use for: dudas sobre governance o calidad fuera del encuadre de la cátedra.
- Klaus Schwab, "The Fourth Industrial Revolution: what it means and how to respond" (World Economic Forum, 2016). No verificado: el sitio bloquea el acceso automático. Es la fuente de la cita del slide sobre la 4ª revolución.

## Wisdom (Communities)
- Foro y Moodle de la materia, y los compañeros de cursada.
  Use for: confirmar las respuestas dudosas del cuestionario (#2b, #16e, #19, #20) y cómo son las preguntas del parcial.
- Consultas a los docentes (Carballo Llosa, Vázquez).
  Use for: si el parcial es a libro abierto y cuál es el formato exacto.

## Gaps
- **Data Products** (cuestionario #20): no aparece en ningún slide revisado.
- El Kahoot escaneado (`KAHOOT-ALUMNOS.pdf`) todavía no está revisado a fondo.

### Material del profe de EDA (`material_eda/`, agregado 19/10)
- [PDF 003 Análisis Exploratorio](material_eda/1-Teoría-Conceptual/003_ANALISIS_EXPLORATORIO_Data_Science_RESUMIDO_2_2026.pdf)
  Fuentes de datos, tipos de análisis, flujo de 5 pasos, clasificación de variables, medidas descriptivas, problemas en los datos, histogramas, asimetría, boxplots, scatter, correlación, outliers, interpretación. Use for: lecciones 0016 a 0021. Parte de las láminas son imágenes: `lit parse --ocr-language spa`.
- Mapa mental (`Mapa Mental`, PNG sin extensión) y "Guía visual" (PNG con tabla): coinciden con el PDF.
- **"Guía Fundamental del EDA" (PNG de Gemini): tiene errores** (RIC = Q2 − Q1, caja = 80% central). No usar como fuente.
- Notebooks 0 a 8 (`2-Notebooks Introductorios`, `3-Notebooks Trabajo en Equipos`, `4-Tarea`) sobre `sample_dataset.csv` (Breast Cancer Wisconsin ensuciado: faltantes y `area error` como texto). El 8 usa el CSV original desde Hugging Face.
- `Detective_de_Datos.mp4`: video, no revisado.
