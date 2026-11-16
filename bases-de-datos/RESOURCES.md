# Bases de Datos — Recursos

Fuentes de confianza para este workspace. Las lecciones citan de acá, no de memoria.

## Knowledge

### Fuente primaria de la materia
- **[Libro] Elmasri, R. & Navathe, S. B. — _Fundamentos de Sistemas de Bases de Datos_, 5ª ed. (Pearson, 2007)**
  → `raw/Fundamentos-de-Sistemas-de-Bases-de-Datos.pdf` (1014 pág., en español)
  El texto base de la cátedra y el estándar de facto para el modelo ER. Es la referencia
  que define la notación de Chen tal como se enseña en la materia.
  **Usar para**: cualquier definición formal — entidad, entidad débil, razón de cardinalidad,
  restricción de participación, especialización/generalización, notación (min,max),
  y las reglas de pasaje ER → relacional.
  Capítulos clave: 3 (modelo ER), 4 (modelo ER extendido / EER), 7 (diseño relacional por
  mapeo ER/EER), 10 (dependencias funcionales y normalización).

### Material de cátedra (el que se evalúa)
- **`raw/Clase 1  Udeci.pptx`** — dato/información/conocimiento, DBMS, modelo relacional,
  SQL (DML/DDL/DCL), ciclo de vida de una BD.
  **Usar para**: vocabulario y encuadre que el docente da por sabido.
- **`raw/B Clase 2 Diseño Conceptual Udeci.pptx`** — el núcleo del cuatrimestre hasta hoy:
  niveles de abstracción, proceso de diseño, entidad débil, atributo multivaluado y derivable,
  relación unaria, histórico, notaciones alternativas, ISA, total/parcial, disjunta/solapada,
  N:N → tabla asociativa.
  **Usar para**: saber exactamente qué terminología y qué criterio espera la cátedra.
- **`raw/TP1_Base de Datos 2026 1er Cuatrimestre.pdf`** + **`raw/Rta-TP-Farmacia.erdplus`**
  Enunciado del TP1 y su resolución oficial en ERDPlus.
  **Usar para**: calibrar el nivel de detalle esperado en una entrega. Es la única muestra
  que tenemos de "modelo aprobado" según el docente.
- **`raw/Ej DER  Clinica.pptx`** — ejercicio de la clínica, **sin resolución**.
  **Usar para**: práctica integradora real y evaluable.

### Material de cátedra del 2do parcial (llegó el 2026-10-15)
- **`raw/DDL, SP , Triggers .pptx`** — CREATE con tipos y las seis restricciones, ON DELETE,
  ALTER, DROP, store procedures (con el `GET_LOAD_ID` del examen) y triggers. Es el mismo
  contenido que `raw/Material_Examen/unidad 4 DDL.pdf`. Los slides de SP y triggers salen de
  Elmasri §9.4.1 y §24.1. **Usar para**: lecciones 0029, 0031 y 0038.
- **`raw/SUMINISTROS/`** (llegó el 2026-10-17) — `SUMINISTROS.sql` + la base SQLite que usó el
  profe en clase, y `Ejercicios-Sql-Consultas.docx` con 31 consultas **sin resolver**. Misma base
  y datos que `bd parcial 1a/1b`. El profe nombra las columnas en todos sus INSERT.
  **Usar para**: `practica/suministros.html` (las 31 resueltas y verificadas en SQLite).
- **`raw/DML_Base de Datos.pptx`** — SELECT, operadores, ORDER/GROUP BY, HAVING, agregadas,
  JOINs, UNION, INSERT/UPDATE/DELETE, UPSERT. **Usar para**: lecciones 0032 a 0037.
- **`raw/TP5/TP DDL-DML  Clinica con DER.pptx`** — consigna del TP5 con el **DER de la cátedra**
  en el slide 8 (imagen EMF; extraída a `assets/diagrams/tp5-der-catedra.png`). **Usar para**: 0040.
- **`raw/Examen1.webp` (Q2, 3, 5, 6, 7)** y **`raw/Material_Examen/bd parcial 1a.jpg`, `1b.jpg`**
  — los modelos de examen de esta parte. Las tablas de 1b están en `assets/seeds/envios.js`.
- **Elmasri 5ª ed., capítulo 8** (SQL: §8.1–8.3 DDL, §8.4–8.5 consultas, §8.6 DML, §8.7
  triggers, §8.8 vistas), **§9.4** (procedimientos almacenados) y **§24.1** (bases activas y triggers).
- **[SQLite — SQL As Understood By SQLite](https://www.sqlite.org/lang.html)** — la referencia
  oficial del motor del grupo y de los ejercicios interactivos.

### Herramienta exigida por la cátedra
- **[ERDPlus](https://erdplus.com/)** — la herramienta de diagramación que pide el docente
  (slide 33 de la Clase 2). Guarda `.erdplus` (JSON) y exporta imagen.
  **Usar para**: producir la entrega. Ojo: su modelo de datos permite cardinalidad mínima
  y máxima, pero la resolución de la cátedra sólo completó la máxima.
- **[ERDPlus — Lesson 1: ER Diagram Basics](https://erdplus.com/learn/er-diagram-basics)**
  Tutorial oficial y gratuito de la herramienta.
  **Usar para**: aprender la mecánica de la herramienta, no la teoría.

### Complemento de alta confianza
- **[Stanford Online — _Databases_ (Jennifer Widom)](https://online.stanford.edu/courses/soe-ydatabases-databases)**
  Curso gratuito, dividido en módulos autoguiados. Widom es autoridad reconocida en el área.
  **Usar para**: normalización y teoría de diseño relacional cuando la materia llegue ahí.
- **[edX — StanfordOnline: Databases: Modeling and Theory](https://www.edx.org/learn/databases/stanford-university-databases-modeling-and-theory)**
  El módulo específico de modelado (UML, ER) y teoría de diseño relacional (FDs, formas normales).
  **Usar para**: 1FN → 2FN → 3FN → BCNF con ejercicios autocorregidos.

## Wisdom (Comunidades)

- **[dba.stackexchange.com](https://dba.stackexchange.com/)**
  Q&A moderado, con profesionales de bases de datos.
  **Usar para**: someter un modelo a crítica ("¿esta jerarquía debería ser ISA o una FK?").
- **[r/Database](https://www.reddit.com/r/Database/)**
  Subreddit de diseño de bases, señal decente.
  **Usar para**: pedir revisión de un DER antes de entregarlo.
- **Presencial: la clase y el docente.**
  La fuente de mayor autoridad para esta misión es el propio docente, porque él define el
  criterio de corrección. Ante una ambigüedad de notación, preguntar en clase gana a
  cualquier libro.

## Gaps

- **No hay resolución del Ej. Clínica.** Cuando lo trabajemos, mi propuesta es una
  interpretación fundada, no una respuesta oficial. Conviene contrastarla con el docente.
- **No hay apunte de la cátedra sobre normalización.** La Clase 2 muestra un resultado en 3FN
  (slide 35) pero no el procedimiento. Hasta que la cátedra lo dicte, apoyarse en
  Elmasri cap. 10 y en el módulo de Stanford.
- ~~No hay material de SQL práctico todavía.~~ Resuelto el 2026-10-15: llegaron los decks
  de DDL y DML (ver arriba). El motor que usa el grupo es SQLite (DBeaver); la cátedra no fijó
  uno, y sus ejemplos mezclan Teradata (`CREATE SET TABLE`, `:VAR`) con SQL estándar.
- **Sin documentación oficial de ERDPlus sobre notación.** El sitio tiene tutoriales de
  la herramienta, no un estándar de notación. La autoridad sobre notación es Elmasri
  + lo que corrija el docente.
