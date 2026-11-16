# Notas de trabajo

## Preferencias del usuario
- Responde y aprende en español (rioplatense). Los artefactos técnicos (código, HTML,
  identificadores) van en inglés; el CONTENIDO DIDÁCTICO va en español, porque la materia
  se rinde en español y la terminología evaluada es la de la cátedra.
- Quiere clases incrementales y cortas. No volcar todo el temario de una.
- Pidió explícitamente usar la skill `diagram-design` para los diagramas — la materia es
  visual y los DER se entienden mejor dibujados.
- Ya tiene conocimientos: el valor está en la PRECISIÓN y en los casos borde, no en la
  introducción.

## Cobertura del temario — REGLA PRINCIPAL

El plan completo vive en `CURRICULUM.md` y es el contrato de cobertura: nueve unidades,
49 lecciones, en orden. **Antes de escribir cualquier lección, verificar dónde cae en ese
mapa.** "De a poquito" es el tamaño de cada lección, no el alcance del curso.

Numeración: las lecciones se numeran en **orden de temario**, no en orden de creación.
Por eso la lección de cardinalidad, escrita primero, quedó como `0010`.

## Estado de la materia (al 2026-09-10)
Cubierto en clase según `raw/`:
- Clase 1: dato/información/conocimiento, DBMS, modelo relacional, SQL (DML/DDL/DCL),
  ciclo de vida de una BD.
- Clase 2: niveles de abstracción (físico/lógico/vistas), proceso de diseño
  (requisitos → conceptual → lógico → físico), entidad, atributo, entidad débil,
  atributo multivaluado, atributo derivable, relación unaria y su cardinalidad,
  histórico (historia de precios), notaciones alternativas (Chen, pata de gallo/UML),
  especialización, generalización, ISA, total/parcial, disjunta/solapada,
  relaciones N:N → tabla asociativa, ejemplo de modelo relacional en 3FN.
- Ejercicios: TP1 Farmacia (con resolución en ERDPlus) y Ej. DER Clínica (sin resolución).

## Observaciones sobre el material de la cátedra
- La resolución `Rta-TP-Farmacia.erdplus` sólo declara cardinalidad MÁXIMA
  (`minCardinality: "Unspecified"` en todos los conectores). La cátedra, en la práctica,
  evalúa la razón de cardinalidad; la participación total/parcial no aparece marcada.
  Enseñar ambas, pero avisar qué exige el docente.
- En la resolución, `Empleado` es supertipo con subtipos `Farmaceutico` y `Propio`,
  total y disjunta. Hay typos en el archivo original ("Emleado", "Antoguedad").
- Falta en la resolución: `matricula` del farmacéutico y el código postal de la ciudad,
  aunque el enunciado los pide. Buen material para una lección sobre trazabilidad
  enunciado → modelo.

## Ideas de lecciones futuras
- 0002: participación total vs parcial y el trazo doble (min-max).
- 0003: entidad débil vs entidad fuerte con FK — el error clásico.
- 0004: atributos compuesto / multivaluado / derivado — cuándo cada uno.
- 0005: ISA — total/parcial × disjunta/solapada, las 4 combinaciones.
- 0006: relación N:N con atributos propios → tabla asociativa.
- 0007: relaciones unarias y su cardinalidad.
- 0008: histórico (historia de precios) — el patrón temporal.
- 0009: pasaje conceptual → relacional, reglas de mapeo.
- 0010: normalización 1FN → 2FN → 3FN.
- Práctica integradora: resolver el Ej. Clínica completo, que NO tiene resolución dada.

## Decisiones técnicas del workspace (2026-08-30)

- **Skin de diagramas**: se creó el perfil `bases-de-datos-udeci` en
  `~/.diagram-design/profiles/`, con los tokens de `assets/course.css` (papel cálido,
  tinta cálida, acento óxido). El marcador `.diagram-design` en la raíz lo selecciona.
  Así los diagramas embebidos y las lecciones se ven como un solo curso.
  El perfil `default` quedó respaldado antes de tocar nada.
- **Notación de los diagramas**: la cátedra usa Chen (rectángulo / rombo / óvalo). El
  `type-er.md` de diagram-design describe el dialecto de caja con listado de campos, que
  es otra cosa. Se aplican sus REGLAS (grilla de 4px, conectores ortogonales, máscaras con
  6–10px de aire, contrato SVG accesible, presupuesto de complejidad) sobre primitivas de
  Chen. Dejar esto dicho en cada diagrama nuevo.
- **Fuente de verdad de los diagramas**: `assets/diagrams/*.svg`, auto-tematizados con
  `prefers-color-scheme`. Las lecciones los referencian con `<img>`, no los inlinean, para
  no duplicar. Un solo archivo por diagrama.
- **Componentes**: `assets/course.css` (hoja compartida por TODA lección y referencia) y
  `assets/quiz.js` (widget de práctica de recuperación con feedback inmediato). Reusar,
  no forkear. Contrato de markup documentado arriba de `quiz.js`.

## Hallazgos sobre la resolución oficial del TP1 (para futuras lecciones)

Mapa completo de la resolución `Rta-TP-Farmacia.erdplus`, ya extraído:

| Relación | Extremos | Razón |
|---|---|---|
| Crea | Laboratorio (One) — Medicamentos (Many) | 1:N |
| Ubica | Ciudad (One) — Farmacia (Many) | 1:N |
| Tiene | Ciudad (One) — Farmaceutico (One) | 1:1 |
| Tiene | Farmacia (One) — Empleado (Many) | 1:N |
| Tiene | Medicamentos (Many) — Presentacion (Many) + atributo `Cantidad` | N:N |
| Stock | Farmacia (Many) — Medicamentos (Many) | N:N |

- `Empleado` es supertipo; `Farmaceutico` y `Propio` son subtipos, **total y disjunta**
  (`totalSpecialization: true`, `supertypeDefinition: "Disjointed"`).
- Atributos marcados: `Telefono` multivaluado, `Direccion` compuesto (Calle, Nro),
  `Antoguedad` derivado. Buen material para la lección de tipos de atributo.
- **Posible error de la cátedra, muy buen material didáctico**: el atributo `Cantidad`
  cuelga del N:N Medicamento–Presentación, pero el enunciado dice que la cantidad en
  existencia es "del mismo en cada farmacia". El stock depende de la farmacia, así que
  debería colgar de la relación `Stock`. Usarlo en la lección de atributos de relación N:N,
  con cuidado: presentarlo como pregunta para el docente, no como "la cátedra se equivocó".
- **Faltantes respecto del enunciado**: no aparecen `matricula` del farmacéutico ni el
  código postal de la ciudad, aunque el TP los pide (una consulta pedida es "cantidad de
  empleados farmacéuticos y propios según su código postal"). Material para una lección
  sobre trazabilidad enunciado → modelo → consultas que el modelo debe poder responder.
- Typos en el archivo original: "Emleado", "Antoguedad". No replicarlos.


## Material de la Clase 3 y los ejercicios del 10/09 (agregado 2026-09-11)

### De dónde sale cada cosa
- **`raw/Clase 3 Base de Datos - Normalización Udeci.pptx`** — 17 slides. Las tablas de
  datos son **imágenes**, no tablas de pptx: hay que extraerlas del zip
  (`ppt/slides/_rels/*.rels` → `ppt/media/*`) y mirarlas. El texto solo no alcanza.
- **`raw/Respuesta_Ejercicio20260910.png`** — planilla con 1FN/2FN/3FN del ejercicio de
  órdenes. La tabla original está cortada arriba; se reconstruye desde el cuadro de 1FN.
- **`/mnt/f/.../Ejercicios/Clase3_Ej1_Proveedores_RS.erdplus`** — resolución oficial del
  Ejercicio 1 (`diagramType: 2` = relational schema; las tablas están en `data.nodes`
  con `columns`, y las FK en `foreignKeyProps`).

### Otro workspace de /teach en /mnt/f
La carpeta de la materia en `F:` tiene su propio workspace anterior (MISSION, GLOSSARY,
NOTES, RESOURCES, 1 lección, 3 learning-records, `reference/Del_Enunciado_al_DER.html`),
acotado a **modelado conceptual**. Se usa como **fuente**, no se edita: el workspace vivo
es éste. Su `GLOSSARY.md` tiene vocabulario útil y compatible — vale mirarlo antes de
inventar términos nuevos. Su MISSION declara la normalización fuera de alcance; la de acá
la cubre entera, así que **mandan `MISSION.md` y `CURRICULUM.md` de este repo**.

### Convención de lecciones de procedimiento
Las lecciones 0019–0026 establecieron un formato que conviene repetir en las unidades
que vienen: definición textual de la cátedra → diagnóstico → **el paso con los datos reales
en tablas antes/después** → qué se arregló → qué NO se arregló → quiz.
Los componentes están en `assets/course.css`: `.datos`, `.paso`, `.paso--tres`, `.rel`,
`.move`. **Reusarlos, no volver a escribir estilos dentro de una lección.**


## Material_Examen y el alcance real del 1er parcial (agregado 2026-09-18)

`raw/Material_Examen/` trae los mismos decks en PDF, reorganizados por unidad, más dos
modelos de examen. Lo que salió de revisarlo:

- **Los PDF coinciden con los PPTX**, con una asimetría que informa: la Unidad 4 viene
  partida en `unidad 4 conceptos.pdf` (coincide casi textual con el PPTX "Clase Indices y
  Txn") y `unidad 4 DDL.pdf`, que **no tiene PPTX equivalente**. Lo que tiene deck, se dio.
- **`unidad 4 DDL.pdf` es la fuente íntegra del examen del compañero** (`raw/Examen1.webp`,
  `Examen2.webp`): cinco de sus preguntas salen de ahí, dos textuales —
  `ALTER TABLE Curso drop duración` (p. 6) y el procedimiento `GET_LOAD_ID` (p. 9).
  Los docentes confirmaron que ese material queda **diferido al 2do parcial**.
- **`bd parcial 1a.jpg` / `1b.jpg` no es un 1er parcial**: pide componentes de un
  Datawarehouse (Unidad 9), `EXISTS`, vistas y SQL con subconsultas (Unidad 5). Es un examen
  posterior. Lo único reutilizable es su pregunta 2, que vuelve a ser índices.
- **`unidad 3.pdf` tiene el ejercicio de normalización resuelto por la cátedra.** La p. 4
  rotula `Pcio R = Cant x P Unit` como atributo derivable — de ahí sale el `Precio_R` de los
  modelos, y es la trampa del error nº 1. La p. 11 da el modelo 3FN canónico y la p. 12 las
  definiciones textuales de las tres formas normales. **Usar esa redacción, no una mejor.**
- **`unidad 1.pdf` p. 5** tiene el ciclo de vida completo con las cuatro etapas descritas.

### Faltantes detectados en el material
- `unidad 2.pdf` páginas 4 a 12: **sólo imágenes, sin capa de texto**. Ahí vive la notación
  del DER, que es justo lo que hay que dibujar a mano en el parcial. Hay que extraerlas del
  PDF para poder armar la lección de notación.
- La p. 13 de `unidad 2.pdf` referencia un **`Pasaje de DER a MER.pdf` que no está en `raw/`**.
  Pedírselo a Bruno antes de escribir la 0016 o la 0018.

### Registro lingüístico de las lecciones — decidido
Las lecciones usan **voseo ligero** en el trato directo ("fijate", "guardá", "mirá"), sin
slang, sin CAPS y sin exclamaciones. Es el registro de las 14 primeras lecciones y se
mantiene por consistencia del corpus: una lección nueva no debe leerse como otro curso.
El contenido técnico y las definiciones evaluadas van en la redacción literal de la cátedra.


## Método de estudio de Bruno — escritura a mano (2026-09-19)

Bruno propuso **reescribir a mano** algunos conceptos mientras lee, con lapicera y papel.
Confirmado como método principal, con una corrección de timing:

- **Copiar mientras se lee no sirve** (es lectura con pasos extra, produce fluidez ilusoria).
  **Escribir con la lección cerrada, sí** — eso es recuperación y construye retención.
- Protocolo acordado: **leer una sección → cerrar → escribir de memoria → abrir y comparar**,
  marcando en otro color lo que faltó. Los huecos son la lista de estudio.
- Para este parcial la escritura a mano no es sólo técnica de estudio: **es ensayo de las
  condiciones reales** (papel, una hora, sin ERDPlus, notación de memoria). Escribir en
  teclado no transfiere al dibujo a mano.
- Lo que conviene que pase por lapicera: los tres tipos de índice con beneficio y costo,
  las cuatro definiciones ACID, las tres formas normales en la redacción de la cátedra,
  el modelo 3FN canónico con sus PK, y sobre todo **la notación del DER**.
- Las lecciones ya están escritas para esto: la 0028 tiene un prompt de recuperación
  explícito **antes** de mostrar la tabla. Respetarlo al escribir lecciones nuevas.

## Unidad 5 / 2do parcial — decisiones del workspace (2026-10-15)

- **Componente `assets/sqlbox.js` + `sqlbox.css`**: ejercicio SQL con corrección automática.
  Corre SQLite 3.45 (sql.js 1.10.3 desde cdnjs) en el navegador, con `PRAGMA foreign_keys = ON`.
  Contrato de markup documentado arriba del archivo. Compara el resultado del alumno contra
  la solución modelo, cada uno sobre una copia limpia de la base. Si se espera un rechazo
  (CHECK, FK, NOT NULL, RAISE), sólo cuenta como bien si el error es del mismo tipo.
  Necesita internet la primera vez (CDN).
- **Bases de práctica** en `assets/seeds/*.js` (se cargan con `<script>`, no con fetch, para
  que funcionen desde `file://`): `clinica` = el relacional del DER de la cátedra del TP5
  (13 tablas, lección 0040); `envios` = las tablas de `bd parcial 1a/1b`.
- **Test offline** de todos los ejercicios: el harness de node vive en el scratchpad de la
  sesión del 15/10, así que no es persistente. Para recrearlo: cargar `sql-wasm.js`, definir
  `global.window`, evaluar seeds y `sqlbox.js`, y llamar a `window.SQLBox.outcome/compare`
  por cada `.sqlbox`. Un ejercicio está mal si la solución no corre o si el código inicial
  ya aprueba.
- **SQLite no tiene stored procedures**: la parte de SP de la 0029 se practica en papel, con
  respuesta modelo. Los triggers sí se practican (sintaxis SQLite con BEGIN…END y RAISE).
- **`pre` agregado a `course.css`** para bloques SQL de sólo lectura (`.k` keyword, `.c` comentario).
- El "hoy" de todos los ejercicios con fechas es **2026-10-15** (fijo, para que la corrección
  sea determinística).
