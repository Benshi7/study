// Single source of truth for the shareable tp/ folder (works from file://, no fetch).
// Used by index.html (chain), avance.html (tracker + coherence checklist) and plan.html (checklist).
// The root hub keeps its own catalog in ../assets/suite-data.js: when a section page or status changes, update both.
//
// sections[].status: "guia" (guide page ready) | "pendiente-clase" (waiting for a class) | "al-final" (written last)
window.TP = {
  dates: { entrega: "2026-10-14", defensa: "2026-11-18" },

  // Top navigation injected by tp-common.js on every page.
  nav: [
    { href: "index.html", label: "Inicio" },
    { href: "avance.html", label: "Avance" },
    { href: "decisiones.html", label: "Decisiones" },
    { href: "plan.html", label: "Plan" },
    { href: "hilo-conductor.html", label: "Hilo" },
  ],

  // The 10 sections required by the consigna (exact titles).
  sections: [
    { n: 1, title: "Carátula", question: "¿Quiénes somos y qué presentamos?", page: null, status: "al-final", dependsOn: [], source: "—" },
    { n: 2, title: "Índice", question: "¿En qué orden se cuenta la historia?", page: null, status: "al-final", dependsOn: [], source: "Se arma al final" },
    { n: 3, title: "Canvas del proyecto", question: "¿Qué negocio y para quién?", page: "canvas-taller.html", status: "guia", dependsOn: [], source: "Clase 1" },
    { n: 4, title: "Aplicar Design Thinking", question: "¿El problema es real? ¿Cuál es la mejor solución?", page: "seccion-04-design-thinking.html", status: "pendiente-clase", dependsOn: [3], source: "Clase 7 (sin material todavía)" },
    { n: 5, title: "Project Charter", question: "¿Qué hacemos, por qué y con qué límites?", page: "seccion-05-charter.html", status: "guia", dependsOn: [3, 4], source: "Clases 2 y 3" },
    { n: 6, title: "Gantt del proyecto completo", question: "¿Qué tareas, en qué orden y cuánto duran?", page: "seccion-06-gantt.html", status: "guia", dependsOn: [5], source: "Clase 3" },
    { n: 7, title: "Matriz de stakeholders", question: "¿A quién afecta y con cuánto poder e interés?", page: "seccion-07-stakeholders.html", status: "guia", dependsOn: [5], source: "Clase 3" },
    { n: 8, title: "Plan de comunicación", question: "¿Qué, a quién, cuándo y por qué canal?", page: "seccion-08-comunicacion.html", status: "guia", dependsOn: [7], source: "Clase 6" },
    { n: 9, title: "Gestión de riesgos - Matriz de riesgos", question: "¿Qué puede pasar y qué hacemos?", page: "seccion-09-riesgos.html", status: "guia", dependsOn: [5, 6, 7], source: "Clase 5" },
    { n: 10, title: "Gestión de costos - Presupuesto", question: "¿Cuánto cuesta?", page: "seccion-10-presupuesto.html", status: "guia", dependsOn: [6, 9], source: "Clase 4" },
  ],

  // Per-section checks in the tracker.
  checks: [
    { id: "bridge", label: "Abre con una frase puente" },
    { id: "template", label: "Plantilla completa (sin [completar])" },
    { id: "consistent", label: "Coherente con las secciones de las que depende" },
    { id: "reviewed", label: "Revisada por otra persona" },
  ],

  // Coherence checklist: rendered by plan.html and avance.html, so the text lives only here.
  checklist: [
    { id: "hitos", html: "Los <strong>hitos</strong> del Charter tienen la misma fecha en el Gantt." },
    { id: "presupuesto", html: "El <strong>presupuesto de alto nivel</strong> del Charter coincide con el total del Presupuesto." },
    { id: "riesgos", html: "Los <strong>riesgos de alto nivel</strong> del Charter están en la Matriz de riesgos." },
    { id: "stakeholders", html: "Los <strong>stakeholders principales</strong> del Charter están en la Matriz de stakeholders, y todos los de la Matriz tienen fila en el Plan de comunicación." },
    { id: "reserva", html: "La <strong>reserva de contingencia</strong> sale de los EMV de la Matriz de riesgos." },
    { id: "mano-obra", html: "El <strong>costo de mano de obra</strong> usa las duraciones del Gantt." },
    { id: "puente", html: "Cada sección abre con una <strong>frase puente</strong> que cita un dato de la anterior." },
  ],
};
