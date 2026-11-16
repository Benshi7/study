// Single source of truth for the suite hub (index.html, clases/index.html).
// Plain script (no fetch) so it works from file://.
//
// To flip a lesson to "ready": create the file in clases/ and set status to "listo".
// To add a class: add an entry to `classes` (same fields) and, if needed, a TP section link.
//
// classes[].status:
//   "listo"             lesson page exists (hub links it)
//   "pendiente-leccion" PDF is in raw/, lesson not written yet
//   "pendiente-pdf"     class happened or is coming, no PDF in raw/ yet
//   "fuera-tp"          outside the TP Cascada (agile block, exams)
// classes[].track: "cascada" | "agil" | "eval"
// classes[].placeholder: optional boolean; the lesson page exists but only as a reserved page (no PDF yet):
//   the hub links it while the card stays greyed out. Remove it when the real lesson replaces the placeholder.
// classes[].slides: optional path to the html-ppt deck of the class (shown as "Slides de la clase" once the lesson is ready)
// classes[].lessonMoreLabels: optional display names for lessonMore (same order); falls back to the file name
// classes[].milestone: null | "entrega" | "defensa" | "parcial" | "recuperatorio"
// tpSections[].status: "guia" | "pendiente-guia" | "pendiente-clase" | "al-final"
// tpSections[].page: a page inside tp/. tp/assets/tp-data.js keeps its own copy of section pages/status (tp/ is shared on its own): update both.
window.SUITE = {
  course: "Taller de Gestión de Proyectos Digitales",
  institution: "Universidad de la Ciudad de Buenos Aires · 2do cuatrimestre 2026",
  dates: {
    entrega: "2026-10-14",
    parcial: "2026-11-18",
    defensa: "2026-11-11",
  },

  classes: [
    {
      number: 1, date: "2026-08-12", unit: "1", modality: "Presencial", track: "cascada",
      title: "Modelo Canvas, propuesta de valor y OKR",
      topics: "Presentación de la materia. Segmentación de mercado. Modelo Canvas. Propuesta de valor. OKR.",
      pdf: "Clase 1 - Modelo Canvas FN.pptx (2).pdf",
      extraPdfs: ["Clase 0 - Presentación Materia FN.pptx.pdf", "Ejemplo Clase.pdf"],
      lesson: "clases/01-canvas.html", lessonMore: [],
      status: "listo", tpSections: [3], milestone: null,
      unlocks: "Sección 3 (Canvas) y objetivos SMART del Charter.",
    },
    {
      number: 2, date: "2026-08-19", unit: "2", modality: "Virtual", track: "cascada",
      title: "Proyectos y dirección de proyectos",
      topics: "Proyecto y gestión de proyectos. Labor del director. PMI, PMBOK, grupos de procesos, áreas de conocimiento, objetivos. Ciclo de vida.",
      pdf: "Clase 2  - Proyectos.pdf", extraPdfs: [],
      lesson: "clases/02-proyectos.html", lessonMore: [],
      status: "listo", tpSections: [5], milestone: null,
      unlocks: "Justificar que el TP es un proyecto y por qué se gestiona en cascada.",
    },
    {
      number: 3, date: "2026-08-26", unit: "2", modality: "Presencial", track: "cascada",
      title: "Gestión del cronograma",
      topics: "Project Charter. Stakeholders en cada fase. Fases. Definir tareas y EDT. Tipos de secuenciamiento. Actividades. Línea base.",
      pdf: "Clase 3 - Gestión del cronograma.pdf", extraPdfs: [],
      lesson: "clases/03a-charter-stakeholders-edt.html",
      lessonMore: ["clases/03b-cronograma-camino-critico.html"],
      lessonMoreLabels: ["Parte 2: cronograma y camino crítico"],
      status: "listo", tpSections: [5, 6, 7], milestone: null,
      unlocks: "Secciones 5 (Charter), 6 (Gantt) y 7 (Matriz de stakeholders).",
    },
    {
      number: 4, date: "2026-09-02", unit: "2", modality: "Presencial", track: "cascada",
      title: "Gestión de costos y PESTEL",
      topics: "Estructura de costes y flujos de ingresos. Estimación, reservas, curva S. PESTEL.",
      pdf: "Clase 4- Gestión de costos.pptx.pdf", extraPdfs: [],
      lesson: "clases/04-costos-pestel.html", lessonMore: [],
      status: "listo", tpSections: [10], milestone: null,
      unlocks: "Sección 10 (Presupuesto).",
    },
    {
      number: 5, date: "2026-09-09", unit: "2", modality: "Presencial", track: "cascada",
      title: "Gestión de riesgos y FODA",
      topics: "Identificación, priorización y cuantificación de riesgos. FODA para identificar riesgos. Matriz P×I, EMV, respuestas.",
      pdf: "Clase 5 - Gestión de riesgos.pdf", extraPdfs: [],
      lesson: "clases/05-riesgos-foda.html", lessonMore: [],
      status: "listo", tpSections: [9], milestone: null,
      unlocks: "Sección 9 (Matriz de riesgos) y la reserva de contingencia del Presupuesto.",
    },
    {
      number: 6, date: "2026-09-16", unit: "2", modality: "Presencial", track: "cascada",
      title: "Cambios, comunicación y negociación",
      topics: "Gestión de cambios. Componentes, canales, dimensiones y barreras de la comunicación. Matriz de comunicación. Negociación (Fisher, Ury, Patton), BATNA.",
      pdf: "Clase 6 - Comunicacion y Negociación.pdf", extraPdfs: [],
      lesson: "clases/06-cambios-comunicacion-negociacion.html", lessonMore: [],
      status: "listo", tpSections: [8], milestone: null,
      unlocks: "Sección 8 (Plan de comunicación) y el proceso de control de cambios.",
    },
    {
      number: 7, date: "2026-09-23", unit: "1, 2, 3", modality: "Presencial", track: "cascada",
      title: "Design Thinking y definición de producto",
      topics: "Definición de producto. Design Thinking: fases y técnicas.",
      pdf: null, extraPdfs: [],
      lesson: "clases/07-design-thinking.html", lessonMore: [],
      status: "pendiente-pdf", placeholder: true, tpSections: [4], milestone: null,
      unlocks: "Sección 4 (Aplicar Design Thinking): validar el problema del segmento elegido en el Canvas.",
    },
    {
      number: 8, date: "2026-09-30", unit: "3", modality: "Virtual", track: "agil",
      title: "Metodología cascada, manifiesto ágil y Cynefin",
      topics: "Metodología cascada. Manifiesto ágil. Metodologías ágiles. CYNEFIN.",
      pdf: "Clase 2 - Concepto de agilidad.pdf", extraPdfs: [],
      lesson: "clases/08-agilidad-manifiesto-cynefin.html", lessonMore: [],
      slides: "slides/08-agilidad/index.html",
      status: "listo", tpSections: [5], milestone: null,
      unlocks: "Abre el bloque ágil del parcial: decidir entre cascada y ágil con Cynefin.",
    },
    {
      number: 9, date: "2026-10-07", unit: "3", modality: "Presencial", track: "agil",
      title: "Scrum: actores, sprint y gestión del producto",
      topics: "Responsabilidades de los actores en Scrum. Sprint y ceremonias. Gestión del producto.",
      pdf: "Clase 4 - Scrum Parte 2do Cuat.pptx.pdf", extraPdfs: [],
      lesson: "clases/09-scrum-roles-artefactos.html", lessonMore: [],
      slides: "slides/09-scrum/index.html",
      status: "listo", tpSections: [], milestone: null,
      unlocks: "Parcial del 18/11 (no forma parte del TP Cascada).",
    },
    {
      number: 10, date: "2026-10-14", unit: "3", modality: "Presencial", track: "agil",
      title: "El Sprint por dentro · Entrega del TP Cascada",
      topics: "Sprint y Sprint 0, Sprint Planning, DoR, estimación ágil y planning poker, splitting, refinamiento y slicing, historias de usuario.",
      pdf: "Clase 5 - Scrum Parte.pdf", extraPdfs: [], lesson: "clases/10-ceremonias-scrum.html", lessonMore: [],
      slides: "slides/10-ceremonias/index.html",
      status: "listo", tpSections: [], milestone: "entrega",
      unlocks: "Entrega del Trabajo Práctico Cascada. Parcial del 18/11. PDF «Clase 5: Scrum Parte 2».",
    },
    {
      number: 11, date: "2026-10-21", unit: "3", modality: "Presencial", track: "agil",
      title: "Retrospectiva y actividad integradora",
      topics: "Daily (tres preguntas), Sprint Review, Sprint Retrospective: pasos, Starfish y Sailing Boat. Actividad integradora (robot en 4 Sprints).",
      pdf: "Clase 6 -  Scrum Parte 3.pdf", extraPdfs: [], lesson: "clases/11-retrospectiva.html", lessonMore: ["clases/11.1-repaso-listas-que-se-confunden.html"], lessonMoreLabels: ["Repaso: listas que se confunden"],
      slides: "slides/10-ceremonias/index.html",
      status: "listo", tpSections: [], milestone: null,
      unlocks: "Parcial del 18/11. PDF «Clase 6: Scrum Parte 3».",
    },
    {
      number: 12, date: "2026-10-28", unit: "3", modality: "Virtual", track: "agil",
      title: "Lean, XP y Kanban",
      topics: "Lean (objetivo, PDCA) y las 7 MUDA. XP: origen, 5 bases y 12 prácticas. Kanban: objetivo, 3 reglas, tablero y tarjetas, herramientas, pull y push.",
      pdf: "Clase 7 - Kanban Lean y XP.pdf", extraPdfs: [], lesson: "clases/12a-lean-xp.html", lessonMore: ["clases/12b-kanban.html"], lessonMoreLabels: ["Parte 2: Kanban"],
      slides: "slides/12-lean-xp-kanban/index.html",
      status: "listo", tpSections: [], milestone: null,
      unlocks: "Parcial del 18/11. El profesor casi siempre pregunta el objetivo de Kanban (12b). Con PDF de la cátedra («Clase 7: Kanban, Lean y XP»).",
    },
    {
      number: 13, date: "2026-11-04", unit: "3", modality: "Presencial", track: "agil",
      title: "IA aplicada a la gestión de proyectos",
      topics: "IA aplicada a la gestión de proyectos.",
      pdf: null, extraPdfs: [], lesson: null, lessonMore: [],
      status: "fuera-tp", tpSections: [], milestone: null,
      unlocks: "Parcial del 18/11.",
    },
    {
      number: 14, date: "2026-11-11", unit: "", modality: "Presencial", track: "eval",
      title: "Defensa del TP Cascada",
      topics: "Defensa de los trabajos prácticos.",
      pdf: null, extraPdfs: [], lesson: null, lessonMore: [],
      status: "fuera-tp", tpSections: [], milestone: "defensa",
      unlocks: "",
    },
    {
      number: 15, date: "2026-11-18", unit: "", modality: "Presencial", track: "eval",
      title: "Parcial de metodologías ágiles",
      topics: "Examen parcial.",
      pdf: null, extraPdfs: [], lesson: null, lessonMore: [],
      status: "fuera-tp", tpSections: [], milestone: "parcial",
      unlocks: "",
    },
    {
      number: 16, date: "2026-11-25", unit: "", modality: "Presencial", track: "eval",
      title: "Recuperatorio (parcial o defensa)",
      topics: "Recuperatorio del parcial o de la defensa.",
      pdf: null, extraPdfs: [], lesson: null, lessonMore: [],
      status: "fuera-tp", tpSections: [], milestone: "recuperatorio",
      unlocks: "",
    },
  ],

  // Extra learning pages that are not tied to a single class. track: "cascada" (TP y defensa) | "agil" (parcial).
  extras: [
    {
      id: "mapa-de-conceptos", track: "cascada", title: "Mapa de conceptos",
      description: "Cómo se conectan Canvas, Charter, cronograma, costos, riesgos y comunicación.",
      path: "clases/mapa-de-conceptos.html", status: "listo",
    },
    {
      id: "parcial-agil", track: "agil", title: "Guía del parcial ágil",
      description: "El temario ágil en una página: hilo conductor, qué viene de la cátedra, casos y plan de estudio.",
      path: "clases/parcial-agil-guia.html", status: "listo",
    },
    {
      id: "simulacro-agil", track: "agil", title: "Simulacro del parcial ágil",
      description: "Opción múltiple: banco de 75 preguntas de las clases 8 a 12, corrección al entregar y puntaje por tema.",
      path: "clases/simulacro-parcial-agil.html", status: "listo",
    },
    {
      id: "agil-glosario", track: "agil", title: "Glosario y hoja de repaso ágil",
      description: "Todos los términos del bloque ágil en una hoja imprimible, con la versión de la cátedra.",
      path: "reference/agil-glosario.html", status: "listo",
    },
    {
      id: "defensa-deck", track: "cascada", title: "Deck de defensa del TP",
      description: "Quince slides con guion hablado en las notas (tecla S): el pitch, las cifras y los puntos flojos.",
      path: "slides/defensa-tp/index.html", status: "listo",
    },
    {
      id: "defensa-01", track: "cascada", title: "Defensa 1 · El relato",
      description: "Cómo contar y vender el TP en 90 segundos y qué le pasa cada sección a la siguiente.",
      path: "clases/defensa-01-relato.html", status: "listo",
    },
    {
      id: "defensa-02", track: "cascada", title: "Defensa 2 · Las cifras",
      description: "De dónde sale cada número: 126 días, USD 4.833 por semana, EMV, reserva y línea base.",
      path: "clases/defensa-02-cifras.html", status: "listo",
    },
    {
      id: "defensa-03", track: "cascada", title: "Defensa 3 · Preguntas difíciles",
      description: "Diecinueve preguntas probables del jurado y los seis puntos flojos del TP.",
      path: "clases/defensa-03-preguntas.html", status: "listo",
    },
  ],

  // The 10 sections required by the "Consigna TP Cascada".
  tpSections: [
    { number: 1, title: "Carátula", question: "¿Quiénes somos y qué presentamos?", feedsFrom: [], page: null, status: "al-final" },
    { number: 2, title: "Índice", question: "¿En qué orden se cuenta la historia?", feedsFrom: [], page: null, status: "al-final" },
    { number: 3, title: "Canvas del proyecto", question: "¿Qué negocio y para quién?", feedsFrom: [1], page: "tp/canvas-taller.html", status: "guia" },
    { number: 4, title: "Aplicar Design Thinking", question: "¿El problema es real? ¿Cuál es la mejor solución?", feedsFrom: [7], page: "tp/seccion-04-design-thinking.html", status: "pendiente-clase" },
    { number: 5, title: "Project Charter", question: "¿Qué hacemos, por qué y con qué límites?", feedsFrom: [2, 3], page: "tp/seccion-05-charter.html", status: "guia" },
    { number: 6, title: "Gantt del proyecto completo", question: "¿Qué tareas, en qué orden y cuánto duran?", feedsFrom: [3], page: "tp/seccion-06-gantt.html", status: "guia" },
    { number: 7, title: "Matriz de stakeholders", question: "¿A quién afecta y con cuánto poder e interés?", feedsFrom: [3], page: "tp/seccion-07-stakeholders.html", status: "guia" },
    { number: 8, title: "Plan de comunicación", question: "¿Qué, a quién, cuándo y por qué canal?", feedsFrom: [6], page: "tp/seccion-08-comunicacion.html", status: "guia" },
    { number: 9, title: "Gestión de riesgos - Matriz de riesgos", question: "¿Qué puede pasar y qué hacemos?", feedsFrom: [5], page: "tp/seccion-09-riesgos.html", status: "guia" },
    { number: 10, title: "Gestión de costos - Presupuesto", question: "¿Cuánto cuesta?", feedsFrom: [4], page: "tp/seccion-10-presupuesto.html", status: "guia" },
  ],
};
