# Notes

## Estructura de la suite (desde 30/9)
```
index.html            hub: fechas, clases, cadena del TP, lo que falta
assets/               fuente única de course.css, theme.js, quiz.js + suite-data.js y suite-render.js (solo hub)
raw/                  PDFs de la cátedra (no se comparte con el equipo si no hace falta)
clases/               lecciones de concepto, una por clase (personales; se pueden compartir)
tp/                   AUTOCONTENIDA y compartible: index, avance, decisiones (votación offline), guías seccion-04…10, plan, hilo-conductor, canvas-*, LEEME.txt, assets/ propios
tools/                check-links.sh · sync-assets.sh · share-tp.sh
learning-records/     registros de la sesión de estudio
```

## Acuerdo de trabajo
- Conceptos en `clases/` (una lección por clase, a partir de `clases/_template.html`). Todo lo que el equipo tiene que ver, discutir o votar va en `tp/`.
- `assets/` es la fuente única de `course.css`, `theme.js` y `quiz.js`. Después de tocarlos: `tools/sync-assets.sh` (copia a `tp/assets/`). Nunca editar a mano esas copias.
- `tp/assets/` tiene además archivos propios que no se sincronizan: `logic.js` (lógica pura de votos y avance, testeada aparte), `tp-data.js` (catálogo de la carpeta compartida), `tp-common.js`, `tp.css`, `tp-nav.css`. `tools/check-links.sh` verifica que `tp-data.js` y `assets/suite-data.js` coincidan.
- Votación: `tp/decisiones.html` (bloque `EDIT HERE`; no cambiar los `id` de decisiones ya votadas). Códigos: votos `TPV1.<base64url>`, estado `TPS1.<base64url>`. Regla de fusión: gana el timestamp más nuevo (por persona en votos, por sección en el avance); en empate, el último pegado (votos) o el local (avance).
- Antes de compartir: `tools/check-tp-standalone.sh` (lo corre `share-tp.sh`).
- `assets/suite-data.js` es el catálogo del hub. Para marcar una lección como lista: crearla y poner `status: "listo"`.
- En `tp/` los links a PDFs y a cualquier cosa fuera de la carpeta llevan `class="local-only"` (solo funcionan en la copia completa). Antes de compartir: `tools/check-links.sh` y `tools/share-tp.sh` (genera `dist/tp-cascada.zip`).
- Tema claro/oscuro: botón arriba a la derecha; por defecto sigue al sistema. Paleta = la de las diapositivas (magenta + violeta sobre blanco).

## Preferencias del alumno
- Quiere entender y producir, no dominar a la perfección. Lecciones cortas, orientadas a "qué pongo en el TP". Eso vale para la ruta cascada; la ruta ágil no menciona el TP (ver «Ruta ágil sin TP», 14/11).
- Lecciones en HTML; se puede usar la skill diagram-design donde un diagrama aporte (Gantt/PERT, matriz poder-interés, matriz P×I, mapa de conceptos).
- Trabaja en equipo: los archivos relacionados con el TP tienen que poder compartirse con los compañeros para votar decisiones juntos.
- Estilo de artefactos: español neutro, sin voseo.

## Working notes
- El cronograma de la cátedra tiene 16 clases (12/8 al 25/11). Los PDFs "Clase N" coinciden con el número de clase del cronograma; "Clase 0" es solo la presentación.
- Las diapositivas de la Clase 6 mencionan "**Clase 12: Plan de comunicación**": es la numeración de otra cursada. Acá corresponde a la clase 6 (16/9).
- Ejemplo transversal mientras no haya material propio: el Canvas de insumos médicos de `raw/Ejemplo Clase.pdf`.
- Ya dados según los PDFs: clases 0–6. Pendientes de PDF: 7 (Design Thinking) y 8 (cascada/ágil/Cynefin).

## Proyecto del equipo (desde 23/9)
- "Proyecto de Modernización del Mapa Interactivo de la Ciudad" (mapa.buenosaires.gob.ar, v4.1). El profesor aprobó la idea el 9/9.
- Visión del equipo: una identidad geográfica única que atraviesa las áreas de gobierno; perfil por hogar; proactividad; loop de reclamos; vista de gestión; capa consumida por Boti/DisfrutemosBA. Ideas: promos Banco Ciudad, Pase Cultural.
- Borrador de Canvas: le faltan Propuesta de valor y Relación con clientes; los segmentos son demasiado amplios; los ingresos son vagos.
- Pregunta abierta del equipo: cómo separar lo "interno" de lo "externo" (consultar con los profes).
- "80 APIs" NO verificado: la página oficial lista 14. Riesgo a futuro: el perfil por hogar implica datos sensibles → PESTEL (Legal) y matriz de riesgos (Ley 25.326).
- No incluir en los artefactos los teléfonos del equipo que aparecen en los chats.

## Bloque ágil y defensa (desde 25/10)
- `slides/<NN-tema>/index.html`: decks html-ppt de cada clase ágil (tema propio `slides/assets/themes/unicaba.css`, copia local de `base.css`/`runtime.js`; no depende del skill). Teclas: ← →, S notas, O vista general, F pantalla completa. Cada slide lleva notas del orador en `<div class="notes">`.
- `diagramas/*.html` y los SVG incrustados se generan con `python3 tools/diagramas.py` (fuente: ese script; estilos en `assets/diagram.css`, clases `dg-*`). Las páginas piden un diagrama con el par de marcadores `<!--diagram:slug-->...<!--/diagram:slug-->`. `--check` falla si alguna copia quedó vieja. No editar a mano el SVG entre marcadores.
- Perfil de diagram-design: `~/.diagram-design/profiles/unicaba-cursada.md`, elegido por el marcador `.diagram-design` en la raíz. Paleta = `assets/course.css`.
- Los PDFs ágiles usan otra numeración: «Clase 2 - Concepto de agilidad» es la clase 8 del cronograma (30/9) y «Clase 4 - Scrum Parte 1» es la clase 9 (7/10). En las lecciones se cita con la numeración del cronograma y se aclara en una nota.
- Lecciones de defensa (`clases/defensa-01..03`): relato, cifras y preguntas difíciles. Todo número sale del TP final (`entregable/dist/TP_Cascada_Grupo01.md`); si el TP cambia, revisar las tres. Seis puntos flojos verificados (investigación de DT, fechas pasadas, éxito sin metas, matriz de comunicación sin tipo/respuesta, sin riesgos positivos, mantenimiento post-cierre y reserva de gestión).
- Cuando la Guía de Scrum 2020 contradice las diapositivas (Developers, hasta 10 personas, sin DoR), gana la cátedra y se anota como «Complemento».

## Parcial ágil y deck de defensa (desde 26/10)
- Las clases 10 a 13 **no tienen PDF de la cátedra**: las lecciones `10-ceremonias-scrum` (cubre clases 10 y 11) y `12-lean-xp-kanban` se armaron con la Guía de Scrum 2020, Wikipedia (Muda, Lean software development, Extreme programming, Kanban) y la Kanban Guide 2025. Todo eso está marcado como «Complemento»: contrastar con los audios/videos de clase y corregir (la cátedra gana). Pendiente: definición de Sprint 0 y de las técnicas de retrospectiva, si se vio el octavo desperdicio y las preguntas de la Daily.
- `clases/parcial-agil-guia.html`: hilo conductor del parcial (11/11), tabla de estado de fuentes, comparación Scrum/Lean/XP/Kanban, casos y plan de estudio. Es el lugar para actualizar cuando lleguen los materiales (clase 13, IA, sin lección todavía).
- `slides/defensa-tp/index.html`: pitch de la defensa (15 slides, guion en las notas, tecla S). Cada slide empareja un concepto de cascada con lo que hizo el TP. La tercera frase del pedido (confirmar a las áreas dueñas del dato) es una propuesta del asistente, no del TP.
- Diagramas nuevos en `tools/diagramas.py`: `sprint-ciclo` y `kanban-flujo`.
- El parcial es uno solo (cronograma, clase 14, 11/11). Si el usuario lo llama «primer parcial», es el mismo.


## Scrum parte 2 y 3 con PDF de la cátedra (desde 28/10)
- PDFs nuevos: «Clase 5 - Scrum Parte.pdf» = **Scrum parte 2** = clase 10 del cronograma (14/10); «Clase 6 -  Scrum Parte 3.pdf» = **Scrum parte 3** = clase 11 (21/10). Ojo: hay otros PDFs «Clase 5» y «Clase 6» (riesgos, comunicación) de la parte cascada.
- `clases/10-ceremonias-scrum.html` se reescribió con la cátedra (Sprint, Sprint 0, Planning, DoR, estimación y planning poker, splitting, slicing, HU, refinamiento). Nueva `clases/11-retrospectiva.html` (Daily, Review, Retro: 7 pasos, Starfish, Sailing Boat ↔ FODA, actividad del robot). El deck `slides/10-ceremonias` también se pasó a la cátedra (13 slides).
- Diferencias cátedra vs. Guía 2020 que cuentan en el parcial: Sprint de 2 semanas a 2 meses; Daily con 3 preguntas; DoR existe; refinamiento lo modera el PO y «Scrum lo ve como parte de la planning»; Sprint 0 máx. 2 Sprints.
- Capturas de diapositivas de la cátedra en `clases/img/*.jpg` (estilo `figure.slide` en `assets/diagram.css`). Se generan con PyMuPDF vía `uv run --with pymupdf` (no hay poppler instalado).
- Diagramas nuevos en `tools/diagramas.py`: `hu-slicing`, `retro-starfish`, `retro-velero`, `push-pull`; `sprint-ciclo` pasó a la versión de la cátedra.
- El profesor dijo que en los parciales casi siempre pregunta **el objetivo de Kanban**: según la diapositiva de la cátedra (captura en `clases/img/clase12-kanban.png`) es **eliminar cuellos de botella** (Toyota, Taiichi Ohno, años 50, Kaizen; «registro visual»; pull; 3 reglas: mostrar el proceso, limitar el trabajo en curso, optimizar el flujo). Puede tomar «limitar el trabajo en curso» (`12b-kanban.html#limitar-wip`). Clase 12 con PDF desde el 29/10 (ver abajo).
- TP Cascada: nota **8**. Defensa el 18/11.
- Pendiente (más adelante, otra sesión): armar juntos la presentación de la defensa con un estilo **académico y de ventas a la vez**: cubrir los contenidos y sumar una parte de pitch. No hubo devolución del profesor sobre el TP.

## Formato pedagógico y rutas (auditoría del 28/10, skill teach)
- La suite tiene **dos rutas**: Ruta 1 Cascada (clases 1–7 → mapa de conceptos → Defensa 1–3 → deck; sirve al TP y a la defensa del 18/11) y Ruta 2 Ágil (clases 8–12 → guía del parcial + glosario; sirve al parcial del 11/11). El hub (`index.html`) y `clases/index.html` las muestran por separado; `extras` en `suite-data.js` llevan `track`.
- Navegación: índice | anterior | siguiente, **solo dentro de la ruta**. El puente entre rutas es la Clase 8 (su repaso inicial pregunta por cascada como concepto). Las lecciones ágiles ya no tienen sección «Aplicado al TP» (ver «Ruta ágil sin TP», 14/11).
- Cada lección ágil abre con «Antes de empezar · repaso» (espaciado). Quizzes: opciones con la misma cantidad de palabras (ruta ágil corregida; excepción: Starfish, cuyas opciones son los nombres literales de la cátedra).
- Referencia: `reference/agil-glosario.html` (glosario + hoja de repaso imprimible). Registros: `learning-records/0001-…`.
- Pendiente: igualar quizzes de la ruta cascada; lección 10 larga (~2.500 palabras; la 12 ya se partió en 12a y 12b); glosario de cascada; clase 7 sin PDF.

## Clase 12 con PDF de la cátedra (desde 29/10)
- «Clase 7 - Kanban Lean y XP.pdf» = **clase 12 del cronograma** (28/10). No confundir con la clase 7 del cronograma (Design Thinking), que sigue sin PDF. Diapositivas en `clases/img/klx-pNN.jpg`.
- Se mantuvo el corte 12a (Lean + XP) / 12b (Kanban). Lo nuevo de la cátedra: objetivo de Lean («optimizar los procesos en base a eliminar el desperdicio»), Ohno + Kaizen, ciclo de Deming (PDCA); XP de Chrysler, años 90, Kent Beck, previo al Manifiesto, 5 bases con aclaraciones y 12 prácticas con nombres de la cátedra (cliente in situ, semana de 40 horas, testing UT/regresión/UAT…); tablero To do / WIP / Done y tarjeta mínima (descripción, responsable, fechas); herramientas Trello/Jira/Azure DevOps. Debate de clase «¿pair programming es desperdicio?» en `12a#pair-programming`.
- Las actividades del PDF (Trello, Galletas Julieta) no se convirtieron en contenido, por pedido del alumno. La versión simplificada de Starfish (start, stop, continue/keep) del repaso se sumó a la Clase 11.
- Los 7 principios de Poppendieck, la muda tipo I/II, las métricas de la Kanban Guide y la definición de la Kanban Guide quedaron como «Complemento» comprimido.

## Ciclo de estudio con el agente (acordado el 28/10)
- La clase 12 se partió en `12a-lean-xp.html` y `12b-kanban.html` (como 3a/3b); la comparación de los cuatro enfoques pasó a `parcial-agil-guia.html#enfoques`. Si llega el PDF de la clase 12 (u otro material), revisar si conviene readaptar el corte.
- Las preguntas de práctica muestran «Pregunta N» (contador CSS en `assets/course.css`), así el alumno puede decir «fallé la pregunta 3 de la 12b».
- Bruno va a reportar después de estudiar: «leí la lección X, me quedó claro A, fallé tal pregunta». Por cada reporte:
  1. Escribir un learning record en `learning-records/` (siguiente número) **solo** si cumple el formato: comprensión demostrada, concepto previo declarado o error corregido. Una pregunta fallada cuenta como error a corregir: anotar qué confundió y por qué.
  2. Si de una clase quedan puntos flojos, proponer una **clase de repaso** `NN.1-repaso-<tema>.html` (por ejemplo `12.1-repaso-kanban.html`): corta, solo sobre lo flojo, con recuperación y preguntas nuevas que mezclen con clases anteriores (interleaving). Va en la misma ruta, justo después de su clase (navegación y `lessonMore` en `suite-data.js`).
  3. Usar los registros para decidir qué repasar antes del parcial (11/11).

## Simulacro del parcial (desde 14/11)
- El parcial ágil pasó al **miércoles 18/11** y sería de opción múltiple (dato de Bruno, de oídas). Los textos de las lecciones que dicen «parcial del 11/11» quedaron viejos.
- `clases/simulacro-parcial-agil.html`: banco de 75 preguntas nuevas (clases 8 a 12 + integradoras), sorteo por tema, corrección al entregar, puntaje por tema, «solo las falladas» y resumen para pegar en el chat. Los ids (`8.3`, `12b.2`, `M.1`) son estables: Bruno reporta los fallos con esos ids. Solo usa contenido de la cátedra; la clase 13 (IA) sigue sin material y no está.
- 14/11: Bruno confirmó que **IA aplicada (clase 13) no entra al parcial**; no hace falta lección. Las slides actuales no le molestan: no rehacerlas.
- Primer simulacro: 18/30. Registro `learning-records/0002-…` y repaso `clases/11.1-repaso-listas-que-se-confunden.html` (entre la 11 y la 12a).
- 14/11, `slides/assets/runtime.js` (cambios locales, marcados «unicaba»): el lienzo crece hasta llenar la ventana (antes quedaban márgenes y la barra del título parecía cortada fuera de 16:9) y la rueda del mouse pasa de diapositiva (abajo = siguiente). Copiado también a `slides/defensa-equipo-web/assets/`. Si se actualiza el runtime desde el skill html-ppt, volver a aplicar los dos bloques.
- 14/11, versión web: `python3 tools/build-netlify.py` genera `dist/suite-netlify/` y `dist/suite-netlify.zip` para Netlify Drop (inicio, clases, simulacro, glosario, diagramas y decks de clase + `defensa-tp`). Quedan afuera a propósito, porque el sitio es público: `raw/`, `tp/`, `entregable/`, `trabajo-grupal/` y el deck del equipo; sus links pasan a texto atenuado. Volver a correrlo y a subir después de cada cambio.

## Ruta ágil sin TP (desde 14/11)
- Pedido de Bruno: las lecciones y slides ágiles (8 a 12b, guía del parcial) **no referencian el TP Cascada** ni el Mapa Interactivo: el TP es de cascada y no tiene que ver. «Cascada» sigue apareciendo solo como concepto (ágil vs. cascada, Cynefin).
- Ejemplo transversal de la ruta ágil: la **web de reservas de restaurantes** (el ejemplo de MoSCoW de la cátedra, Clase 9 p13). Comensal, restaurante, «Reservas en línea» como épica, confirmación por WhatsApp como historia incierta, equipo de 4 desarrolladores + 1 persona que prueba para Kanban. En mudas, además, una fábrica de galletitas.
- Cada lección ágil cierra con **«Trampas de opción múltiple»** (`#trampas`: opción tentadora → por qué está mal) en lugar de «Aplicado al TP». Decks: slide «Trampas» en `08-agilidad`, backlog de la cátedra (p11) en `09-scrum`, cadena Lean–Kanban en `12-lean-xp-kanban`.
- Único «TP» que queda: el ejemplo literal de Starfish de la cátedra («actividades relacionadas al TP», Scrum parte 3 p11), en la captura y en el diagrama `retro-starfish`.
- Sumado desde los PDFs: Scrum «no requiere grandes cambios estructurales, se aprende en 3 horas, hasta un año en dominarlo» y el conteo «4 roles» (Scrum parte 2, p3 y p4); backlog de ejemplo (Clase 9, p11); Daily = Stand Up = Meeting, única ceremonia que se repite, impedimentos por fuera de la reunión (repaso de la clase 12, p3).
- `parcial-agil-guia.html`: sin IA ni defensa; fila «Origen» con datos de la cátedra; plan de estudio del 14 al 18/11.
- Leyenda del diagrama `cynefin`: «único dominio en cascada» (antes «el caso de nuestro TP»).

## Hub de la suite (15/11)
- Páginas: `index.html` (Inicio: fechas, retomar lectura, accesos, rutas plegables), `clases/index.html` (rutas con secciones por clase), `diagramas/index.html` (galería, la genera `tools/diagramas.py`; los grupos están en `GALLERY`), `slides/index.html` (decks con vista previa) y `repaso.html` (historial del simulacro, práctica y trampas por clase).
- `assets/suite-nav.js` (con `defer` en todas las páginas de `clases/`, `reference/` y del hub): barra superior, «Marcar leída» y la última sección leída, en localStorage (`suite-progress-v1`, `suite-last-v1`, `suite-ui-v1`). Estilos en `assets/suite.css`.
- `tools/suite-index.py` genera `assets/suite-index.js` (secciones de cada lección, decks, diagramas) y agrega `id` a los `<h2>` que no lo tienen. Orden al cambiar contenido: `python3 tools/diagramas.py && python3 tools/suite-index.py && tools/check-links.sh && python3 tools/build-netlify.py`.
- Un diagrama nuevo tiene que sumarse a `GALLERY` en `tools/diagramas.py` (si falta, el script corta con error).
