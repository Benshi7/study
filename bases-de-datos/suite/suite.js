/* Study suite · Base de Datos
 * Vanilla JS, no build step: works opened straight from disk (file://).
 * Data comes from data/bank.js (generated from the lessons) and data/content.js.
 */
(function () {
  "use strict";

  // ------------------------------------------------------------------ utils

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  function h(tag, attrs = {}, ...children) {
    const node = document.createElement(tag);
    for (const [key, value] of Object.entries(attrs)) {
      if (value === null || value === undefined || value === false) continue;
      if (key === "class") node.className = value;
      else if (key === "html") node.innerHTML = value;
      else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
      else node.setAttribute(key, value === true ? "" : value);
    }
    for (const child of children.flat()) {
      if (child === null || child === undefined || child === false) continue;
      node.appendChild(typeof child === "string" || typeof child === "number" ? document.createTextNode(String(child)) : child);
    }
    return node;
  }

  function shuffle(items) {
    const copy = items.slice();
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }

  // Storage is a convenience: every read/write tolerates it being unavailable.
  const store = {
    get(key, fallback) {
      try {
        const raw = localStorage.getItem("bd-suite:" + key);
        return raw === null ? fallback : JSON.parse(raw);
      } catch (_) { return fallback; }
    },
    set(key, value) {
      try { localStorage.setItem("bd-suite:" + key, JSON.stringify(value)); } catch (_) { /* ignore */ }
    },
    lessonBest(id) {
      try { return JSON.parse(localStorage.getItem("bd-quiz:" + id)); } catch (_) { return null; }
    }
  };

  const BLOCKS = {
    fund: { name: "Fundamentos", short: "Fundamentos" },
    der: { name: "Modelo entidad-relación", short: "DER" },
    norm: { name: "Normalización", short: "Normalización" },
    fis: { name: "Índices y transacciones", short: "Índices y txn" },
    sql: { name: "SQL", short: "SQL" },
    dw: { name: "Data warehouse", short: "Data warehouse" }
  };
  const lessonById = Object.fromEntries((window.LESSONS || []).map((l) => [l.id, l]));
  const lessonHref = (id) => `../lessons/${id}.html`;
  const refHref = (id) => `../reference/${id}.html`;
  const lessonNum = (id) => (id || "").slice(0, 4);
  // Concepts that have a drawn figure in ../assets/diagrams/ (file name without extension).
  const DIAGRAMS = [
    ["anatomia-relacion", "Anatomía de una relación", ["modelo_rel", "claves"]],
    ["tres-niveles", "Los tres niveles", ["tres_niveles", "indep"]],
    ["ciclo-de-vida-bd", "Ciclo de vida de una base de datos", ["ciclo_vida"]],
    ["notacion-der-simbolos", "Símbolos del DER", ["notaciones", "entidad", "atributo", "multivaluado", "derivable", "entidad_debil"]],
    ["er-razon-cardinalidad", "Razón de cardinalidad", ["cardinalidad"]],
    ["especializacion-cuatro-combinaciones", "Especialización: cuatro combinaciones", ["especializacion", "total_parcial", "excl_solap"]],
    ["especializacion-conteo", "Contar registros del supertipo", ["especializacion"]],
    ["tipos-de-dependencia", "Tipos de dependencia", ["dep_funcional", "dep_parcial", "transitiva"]],
    ["tipos-de-indice", "Tipos de índice", ["indice", "idx_principal", "idx_agrupado", "idx_secundario"]],
    ["componentes-dw", "Componentes de un Data Warehouse", ["componentes_dw", "etl", "ods_mdm_dq"]],
    ["esquema-estrella", "Estrella y copo de nieve", ["estrella", "copo_nieve"]]
  ];
  const diagramFor = (conceptId) => (DIAGRAMS.find(([, , ids]) => ids.includes(conceptId)) || [])[0];
  const diagramHref = (slug) => `../assets/diagrams/${slug}.svg`;

  // ------------------------------------------------------------------ theme

  function initTheme() {
    const saved = store.get("theme", null);
    if (saved) document.documentElement.setAttribute("data-theme", saved);
    const label = $("#theme-label");
    const current = () => document.documentElement.getAttribute("data-theme") ||
      (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    const paint = () => { label.textContent = current() === "dark" ? "Modo claro" : "Modo oscuro"; };
    $("#theme-toggle").addEventListener("click", () => {
      const next = current() === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      store.set("theme", next);
      paint();
    });
    paint();
  }

  // ------------------------------------------------------------------ countdown

  function initCountdown() {
    const big = $("#countdown-big");
    const chip = $("#countdown-chip");
    const exam = window.EXAM;
    if (!exam.date) {
      big.textContent = "Noviembre";
      $("#countdown-sub").textContent = "Fecha a confirmar con los docentes";
      chip.innerHTML = `2.º parcial<span class="long"> · mediados de noviembre</span>`;
      return;
    }
    const target = exam.date.getTime();
    function tick() {
      const ms = target - Date.now();
      if (ms <= 0) {
        big.textContent = ms > -3 * 3600e3 ? "¡Hoy!" : "Ya pasó";
        chip.textContent = ms > -3 * 3600e3 ? "Parcial: hoy" : "Parcial rendido";
        return;
      }
      const d = Math.floor(ms / 86400e3);
      const hrs = Math.floor((ms % 86400e3) / 3600e3);
      const min = Math.floor((ms % 3600e3) / 60e3);
      big.innerHTML = d > 0
        ? `${d}<span class="unit"> d </span>${hrs}<span class="unit"> h</span>`
        : `${hrs}<span class="unit"> h </span>${String(min).padStart(2, "0")}<span class="unit"> min</span>`;
      chip.innerHTML = `Parcial en ${d > 0 ? d + " d " : ""}${hrs} h<span class="long"> · ${exam.label}</span>`;
      $("#countdown-sub").textContent = exam.label;
    }
    tick();
    setInterval(tick, 30000);
  }

  // ------------------------------------------------------------------ router

  const VIEWS = ["inicio", "mapa", "fichas", "simulacro", "armar", "herramientas", "biblioteca"];
  const renderers = {};
  // Extension point: suite/builder.js registers its own view here.
  window.SUITE = { renderers, store, h, $, $$ };

  function route() {
    const name = VIEWS.includes(location.hash.slice(1)) ? location.hash.slice(1) : "inicio";
    for (const section of $$(".view")) section.hidden = section.dataset.view !== name;
    for (const link of $$(".rail a")) {
      if (link.dataset.view === name) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    }
    if (renderers[name]) renderers[name]();
    window.scrollTo(0, 0);
  }

  // ------------------------------------------------------------------ inicio

  const PLAN = [
    ["ddl", "DDL: lecciones 0031 y 0038 (CREATE TABLE, restricciones, ALTER, DROP, ON DELETE)"],
    ["consultas", "Consultas: lecciones 0032 a 0036 (SELECT, NULL, JOIN, GROUP BY, subconsultas)"],
    ["modif", "Modificar datos y vistas: lecciones 0037 y 0039"],
    ["sp", "Teoría (choice en papel) de store procedures y triggers: lección 0029 y la referencia SQL"],
    ["tp5", "Vistas con indicadores y consultas sobre la vista: lección 0040 y la práctica del TP5"],
    ["dw", "Data warehouse: lecciones 0049 a 0051 (teoría choice: OLTP/OLAP, componentes, estrella, Inmon/Kimball)"],
    ["scd", "Slow Change Dimension: lección 0052 con los 8 ejercicios (estado actual, a una fecha, vistas, el cambio)"],
    ["fis", "Índices y transacciones: lecciones 0027, 0028 y 0041"],
    ["norm", "Repaso de normalización con el simulacro (lecciones 0019 a 0026)"],
    ["bld", "Constructor SQL: los 31 ejercicios de SUMINISTROS (el parcial toma 2 de esa dificultad)"],
    ["sim", "Simulacro de 20 preguntas en modo examen con nota ≥ 7"],
    ["fichas", "Fichas hasta que todas estén en la caja 3"]
  ];

  const STATIC_WEAK = [
    { title: "NULL en CHECK y en WHERE", note: "En un CHECK, DESCONOCIDO pasa; en un WHERE, descarta la fila.", lesson: "0033-condiciones-y-null" },
    { title: "“No es jefe” contra “tiene jefe”", note: "Lo que no tiene pareja se pide con NOT EXISTS o LEFT JOIN … IS NULL.", lesson: "0036-subconsultas-exists" },
    { title: "“Ambos T1 y T2”", note: "Dos filas distintas cumplen cada parte: hacen falta dos condiciones, no un solo IN.", lesson: "0036-subconsultas-exists" },
    { title: "Total + solapada y parcial + exclusiva", note: "Las dos marcas son independientes; el conteo del supertipo cambia con cada combinación.", lesson: "0014-contar-registros-del-supertipo" }
  ];

  function blockProgress(block) {
    const lessons = (window.LESSONS || []).filter((l) => l.block === block);
    let done = 0, correct = 0, total = 0;
    for (const lesson of lessons) {
      const best = store.lessonBest(lesson.id);
      if (best) { done += 1; correct += best.correct; total += best.total; }
    }
    return { lessons: lessons.length, done, pct: total ? Math.round((correct / total) * 100) : null };
  }

  renderers.inicio = function () {
    const meters = $("#block-meters");
    meters.innerHTML = "";
    for (const [key, block] of Object.entries(BLOCKS)) {
      const p = blockProgress(key);
      if (!p.lessons) continue;
      const width = p.lessons ? Math.round((p.done / p.lessons) * 100) : 0;
      meters.appendChild(h("div", { class: "panel" },
        h("div", { class: "meter" },
          h("div", { class: "meter-top" }, h("strong", {}, block.name), h("span", { class: "num muted" }, `${p.done}/${p.lessons} lecciones`)),
          h("div", { class: "bar", role: "progressbar", "aria-valuenow": width, "aria-valuemin": 0, "aria-valuemax": 100 }, h("span", { style: `width:${width}%` }))
        ),
        h("p", { class: "muted", style: "font-size:0.88rem" },
          p.pct === null ? "Todavía no hiciste ningún quiz de este bloque." : `Acierto promedio en los quizzes hechos: ${p.pct}%.`)
      ));
    }

    const done = store.get("plan", {});
    const plan = $("#plan");
    plan.innerHTML = "";
    const count = () => { $("#plan-count").textContent = `${Object.values(store.get("plan", {})).filter(Boolean).length}/${PLAN.length}`; };
    for (const [id, text] of PLAN) {
      const input = h("input", { type: "checkbox", id: "plan-" + id });
      input.checked = !!done[id];
      input.addEventListener("change", () => {
        const state = store.get("plan", {});
        state[id] = input.checked;
        store.set("plan", state);
        count();
      });
      plan.appendChild(h("li", {}, h("label", { for: "plan-" + id }, input, h("span", {}, text))));
    }
    count();

    const weak = $("#weak");
    weak.innerHTML = "";
    for (const item of STATIC_WEAK) {
      weak.appendChild(h("li", {},
        h("strong", {}, item.title),
        h("small", {}, item.note, " ", h("a", { href: lessonHref(item.lesson) }, `Lección ${lessonNum(item.lesson)}`))));
    }
    const misses = store.get("misses", {});
    const worst = Object.entries(misses).filter(([, n]) => n > 0).sort((a, b) => b[1] - a[1]).slice(0, 4);
    const byId = Object.fromEntries(window.BANK.map((q) => [q.id, q]));
    for (const [id, n] of worst) {
      const q = byId[id];
      if (!q) continue;
      const text = q.q.replace(/<pre[\s\S]*?<\/pre>/g, " [código] ").replace(/<[^>]+>/g, "");
      weak.appendChild(h("li", {},
        h("strong", {}, text.length > 110 ? text.slice(0, 107) + "…" : text),
        h("small", {}, `Fallada ${n} ${n === 1 ? "vez" : "veces"} en el simulacro · `, h("a", { href: lessonHref(q.lesson) }, `Lección ${lessonNum(q.lesson)}`))));
    }
  };

  // ------------------------------------------------------------------ mapa

  const SVG_NS = "http://www.w3.org/2000/svg";
  const svgEl = (tag, attrs = {}) => {
    const node = document.createElementNS(SVG_NS, tag);
    for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
    return node;
  };
  const conceptById = Object.fromEntries(window.CONCEPTS.map((c) => [c.id, c]));
  const nodeWidth = (label) => Math.round(label.length * 7.3 + 30);
  const mapState = { selected: null, filter: "all", pathStep: null, built: false };

  function neighborsOf(id) {
    return window.EDGES
      .filter(([a, b]) => a === id || b === id)
      .map(([a, b, label]) => ({ id: a === id ? b : a, label, outgoing: a === id }));
  }

  function buildMap() {
    const svg = $("#map-svg");
    svg.innerHTML = "";
    const clusterLabels = [
      ["Fundamentos", 55, 22], ["Modelo entidad-relación", 595, 22],
      ["Normalización", 55, 362], ["Índices y transacciones", 595, 362],
      ["SQL · definir la estructura (DDL)", 55, 702], ["SQL · consultar y modificar (DML)", 55, 862],
      ["Data warehouse", 55, 1302], ["Data warehouse · historicidad (SCD)", 55, 1542]
    ];
    for (const [text, x, y] of clusterLabels) {
      const t = svgEl("text", { x, y, class: "map-cluster-label" });
      t.textContent = text;
      svg.appendChild(t);
    }
    const edgeLayer = svgEl("g");
    const labelLayer = svgEl("g");
    const nodeLayer = svgEl("g");
    svg.append(edgeLayer, labelLayer, nodeLayer);

    window.EDGES.forEach(([a, b, label], i) => {
      const A = conceptById[a], B = conceptById[b];
      if (!A || !B) return;
      // Gentle curve so parallel edges stay distinguishable.
      const mx = (A.x + B.x) / 2, my = (A.y + B.y) / 2;
      const dx = B.x - A.x, dy = B.y - A.y;
      const len = Math.hypot(dx, dy) || 1;
      const bend = Math.min(40, len * 0.12);
      const cx = mx - (dy / len) * bend, cy = my + (dx / len) * bend;
      const path = svgEl("path", { d: `M${A.x},${A.y} Q${cx},${cy} ${B.x},${B.y}`, class: "map-edge", "data-a": a, "data-b": b, "data-i": i });
      edgeLayer.appendChild(path);
      const text = svgEl("text", { x: (A.x + 2 * cx + B.x) / 4, y: (A.y + 2 * cy + B.y) / 4 + 4, "text-anchor": "middle", class: "map-edge-label", "data-i": i });
      text.textContent = label;
      text.style.display = "none";
      labelLayer.appendChild(text);
    });

    for (const c of window.CONCEPTS) {
      const w = nodeWidth(c.label);
      const g = svgEl("g", { class: "map-node", tabindex: "0", role: "button", "data-id": c.id, "aria-label": c.label });
      g.appendChild(svgEl("rect", { x: c.x - w / 2, y: c.y - 16, width: w, height: 32, rx: 16, stroke: `var(--c-${c.cluster})` }));
      g.appendChild(svgEl("circle", { class: "dot", cx: c.x - w / 2 + 14, cy: c.y, r: 4, fill: `var(--c-${c.cluster})` }));
      const t = svgEl("text", { x: c.x + 5, y: c.y + 4.5, "text-anchor": "middle" });
      t.textContent = c.label;
      g.appendChild(t);
      g.addEventListener("click", () => { mapState.pathStep = null; selectConcept(c.id); revealDetail(); });
      g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); mapState.pathStep = null; selectConcept(c.id); revealDetail(); } });
      nodeLayer.appendChild(g);
    }

    const filter = $("#map-filter");
    filter.innerHTML = "";
    const options = [["all", "Todo"], ...Object.entries(window.CLUSTERS).map(([k, v]) => [k, v.name])];
    for (const [key, name] of options) {
      const btn = h("button", { type: "button", "aria-pressed": String(key === mapState.filter) }, name);
      btn.addEventListener("click", () => {
        mapState.filter = key;
        $$("button", filter).forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
        paintMap();
      });
      filter.appendChild(btn);
    }
    $("#path-start").addEventListener("click", () => { mapState.pathStep = 0; selectConcept(window.PATH[0].id); revealDetail(); });
    mapState.built = true;
  }

  // When the detail panel sits below the map, bring it into view only if it is off-screen.
  function revealDetail() {
    const detail = $("#map-detail");
    const box = detail.getBoundingClientRect();
    if (box.top > window.innerHeight - 120 || box.bottom < 0) {
      detail.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
    }
  }

  function paintMap() {
    const sel = mapState.selected;
    const near = new Set(sel ? neighborsOf(sel).map((n) => n.id) : []);
    const pathIds = mapState.pathStep !== null ? window.PATH.slice(0, mapState.pathStep + 1).map((s) => s.id) : [];
    const pathEdges = new Set();
    for (let i = 1; i < pathIds.length; i++) pathEdges.add(pathIds[i - 1] + "|" + pathIds[i]);

    for (const g of $$(".map-node")) {
      const id = g.dataset.id;
      const c = conceptById[id];
      const inFilter = mapState.filter === "all" || c.cluster === mapState.filter;
      g.classList.toggle("selected", id === sel);
      g.classList.toggle("neighbor", near.has(id) || (pathIds.includes(id) && id !== sel));
      g.classList.toggle("dim", !inFilter && id !== sel && !near.has(id));
    }
    for (const path of $$(".map-edge")) {
      const { a, b, i } = path.dataset;
      const hot = sel && (a === sel || b === sel);
      const onPath = pathEdges.has(a + "|" + b) || pathEdges.has(b + "|" + a);
      path.classList.toggle("hot", !!hot && !onPath);
      path.classList.toggle("path", onPath);
      const label = $(`.map-edge-label[data-i="${i}"]`);
      if (label) label.style.display = hot || onPath ? "" : "none";
    }
  }

  function selectConcept(id) {
    mapState.selected = id;
    paintMap();
    const c = conceptById[id];
    const detail = $("#map-detail");
    detail.innerHTML = "";

    if (mapState.pathStep !== null) {
      const step = mapState.pathStep;
      const prev = h("button", { class: "btn ghost", type: "button", disabled: step === 0 }, "← Anterior");
      const next = h("button", { class: "btn", type: "button" }, step === window.PATH.length - 1 ? "Terminar" : "Siguiente →");
      prev.addEventListener("click", () => { mapState.pathStep -= 1; selectConcept(window.PATH[mapState.pathStep].id); });
      next.addEventListener("click", () => {
        if (mapState.pathStep === window.PATH.length - 1) { mapState.pathStep = null; selectConcept(id); return; }
        mapState.pathStep += 1;
        selectConcept(window.PATH[mapState.pathStep].id);
      });
      detail.appendChild(h("div", { class: "path-box" },
        h("span", { class: "step num" }, `Paso ${step + 1} de ${window.PATH.length}`),
        h("p", {}, window.PATH[step].text),
        h("div", { class: "row" }, prev, next)));
    }

    const cluster = window.CLUSTERS[c.cluster];
    detail.appendChild(h("span", { class: "chip neutral cluster-tag" }, cluster.name));
    detail.appendChild(h("h3", {}, c.label));
    detail.appendChild(h("p", { class: "def" }, c.def));
    if (c.trap) detail.appendChild(h("div", { class: "callout" }, h("strong", {}, "Trampa: "), c.trap));
    const links = h("div", { class: "row" });
    if (c.lesson && lessonById[c.lesson]) links.appendChild(h("a", { class: "btn ghost", href: lessonHref(c.lesson) }, `Lección ${lessonNum(c.lesson)}`));
    if (c.ref) links.appendChild(h("a", { class: "btn ghost", href: refHref(c.ref) }, "Referencia"));
    if (diagramFor(id)) links.appendChild(h("a", { class: "btn ghost", href: diagramHref(diagramFor(id)) }, "Diagrama"));
    detail.appendChild(links);

    const list = h("ul", { class: "neighbors" });
    for (const n of neighborsOf(id)) {
      const other = conceptById[n.id];
      const btn = h("button", { type: "button" },
        h("small", {}, n.outgoing ? `${n.label} →` : `← ${n.label} → ${c.label}`),
        h("strong", {}, other.label));
      btn.addEventListener("click", () => { mapState.pathStep = null; selectConcept(n.id); });
      list.appendChild(h("li", {}, btn));
    }
    detail.appendChild(h("p", { class: "eyebrow" }, `Se conecta con (${neighborsOf(id).length})`));
    detail.appendChild(list);
  }

  renderers.mapa = function () {
    if (!mapState.built) buildMap();
    selectConcept(mapState.selected || "dbms");
  };

  // ------------------------------------------------------------------ fichas

  const allCards = [
    ...window.CONCEPTS.map((c) => ({
      id: "c:" + c.id, block: window.CLUSTERS[c.cluster].block, front: c.label, back: c.def, trap: c.trap, lesson: c.lesson
    })),
    ...window.EXTRA_CARDS.map((c, i) => ({ id: "x:" + i, ...c }))
  ];
  const cardState = { filter: "all", queue: [], current: null, flipped: false };

  function cardBoxes() { return store.get("cards", {}); }

  function buildQueue() {
    const boxes = cardBoxes();
    const pool = allCards.filter((c) => cardState.filter === "all" || c.block === cardState.filter);
    // Lowest box first; shuffle inside each box so the order is not memorised.
    cardState.queue = [1, 2, 3].flatMap((box) => shuffle(pool.filter((c) => (boxes[c.id] || 1) === box)));
  }

  function paintBoxes() {
    const boxes = cardBoxes();
    const pool = allCards.filter((c) => cardState.filter === "all" || c.block === cardState.filter);
    const counts = [1, 2, 3].map((b) => pool.filter((c) => (boxes[c.id] || 1) === b).length);
    const labels = ["Caja 1 · a repasar", "Caja 2 · casi", "Caja 3 · dominadas"];
    const wrap = $("#card-boxes");
    wrap.innerHTML = "";
    counts.forEach((n, i) => wrap.appendChild(h("div", { class: "box-stat" }, h("strong", {}, String(n)), h("span", {}, labels[i]))));
  }

  function showCard() {
    const card = $("#flashcard");
    card.innerHTML = "";
    cardState.flipped = false;
    card.classList.remove("flipped");
    $("#card-miss").disabled = true;
    $("#card-hit").disabled = true;
    if (!cardState.queue.length) buildQueue();
    cardState.current = cardState.queue.shift();
    const c = cardState.current;
    if (!c) { card.appendChild(h("p", {}, "No hay fichas para este filtro.")); return; }
    card.appendChild(h("span", { class: "eyebrow" }, BLOCKS[c.block].short));
    card.appendChild(h("div", { class: "front" }, c.front));
    card.appendChild(h("p", { class: "muted" }, "Pensá la respuesta y tocá para ver."));
  }

  function flipCard() {
    const c = cardState.current;
    if (!c || cardState.flipped) return;
    cardState.flipped = true;
    const card = $("#flashcard");
    card.classList.add("flipped");
    card.innerHTML = "";
    card.appendChild(h("span", { class: "eyebrow" }, c.front));
    card.appendChild(h("p", { class: "back" }, c.back));
    if (c.trap) card.appendChild(h("p", { class: "trap" }, "Trampa: " + c.trap));
    if (c.lesson) card.appendChild(h("a", { href: lessonHref(c.lesson), onclick: (e) => e.stopPropagation() }, `Lección ${lessonNum(c.lesson)}`));
    $("#card-miss").disabled = false;
    $("#card-hit").disabled = false;
  }

  function gradeCard(knew) {
    const c = cardState.current;
    if (!c) return;
    const boxes = cardBoxes();
    boxes[c.id] = knew ? Math.min(3, (boxes[c.id] || 1) + 1) : 1;
    store.set("cards", boxes);
    if (!knew) cardState.queue.splice(Math.min(3, cardState.queue.length), 0, c); // see it again soon
    paintBoxes();
    showCard();
  }

  let cardsWired = false;
  renderers.fichas = function () {
    if (!cardsWired) {
      const filter = $("#card-filter");
      for (const [key, name] of [["all", "Todas"], ...Object.entries(BLOCKS).map(([key, block]) => [key, block.short])]) {
        const btn = h("button", { type: "button", "aria-pressed": String(key === "all") }, name);
        btn.addEventListener("click", () => {
          cardState.filter = key;
          $$("button", filter).forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
          buildQueue(); paintBoxes(); showCard();
        });
        filter.appendChild(btn);
      }
      $("#flashcard").addEventListener("click", flipCard);
      $("#flashcard").addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); flipCard(); } });
      $("#card-flip").addEventListener("click", flipCard);
      $("#card-miss").addEventListener("click", () => gradeCard(false));
      $("#card-hit").addEventListener("click", () => gradeCard(true));
      cardsWired = true;
      buildQueue();
      showCard();
    }
    paintBoxes();
  };

  // ------------------------------------------------------------------ simulacro

  const sim = { phase: "config", questions: [], answers: [], idx: 0, mode: "examen", deadline: null, timer: null, config: null };
  const LETTERS = "abcdefgh";

  function simRoot() { return $("#sim-root"); }

  function renderSimConfig() {
    clearInterval(sim.timer);
    sim.phase = "config";
    const root = simRoot();
    root.innerHTML = "";
    const cfg = Object.assign({ n: 20, blocks: Object.keys(BLOCKS), mode: "examen", weak: false, timed: false }, store.get("simConfig", {}));

    const nBox = h("div", { class: "segmented", role: "group", "aria-label": "Cantidad de preguntas" });
    for (const n of [10, 20, 40, 0]) {
      const btn = h("button", { type: "button", "aria-pressed": String(cfg.n === n) }, n === 0 ? "Todas" : String(n));
      btn.addEventListener("click", () => { cfg.n = n; $$("button", nBox).forEach((b) => b.setAttribute("aria-pressed", String(b === btn))); });
      nBox.appendChild(btn);
    }
    const blockBox = h("div", { class: "checks" });
    for (const [key, block] of Object.entries(BLOCKS)) {
      const count = window.BANK.filter((q) => q.block === key).length;
      if (!count) continue;
      const input = h("input", { type: "checkbox", id: "sim-b-" + key });
      input.checked = cfg.blocks.includes(key);
      input.addEventListener("change", () => {
        cfg.blocks = input.checked ? [...new Set([...cfg.blocks, key])] : cfg.blocks.filter((b) => b !== key);
      });
      blockBox.appendChild(h("label", { for: "sim-b-" + key }, input, `${block.name} (${count})`));
    }
    const modeBox = h("div", { class: "segmented", role: "group", "aria-label": "Modo" });
    for (const [key, name] of [["examen", "Examen: respuestas al final"], ["practica", "Práctica: feedback inmediato"]]) {
      const btn = h("button", { type: "button", "aria-pressed": String(cfg.mode === key) }, name);
      btn.addEventListener("click", () => { cfg.mode = key; $$("button", modeBox).forEach((b) => b.setAttribute("aria-pressed", String(b === btn))); });
      modeBox.appendChild(btn);
    }
    const extras = h("div", { class: "checks" });
    const weakInput = h("input", { type: "checkbox", id: "sim-weak" });
    weakInput.checked = cfg.weak;
    weakInput.addEventListener("change", () => { cfg.weak = weakInput.checked; });
    const timedInput = h("input", { type: "checkbox", id: "sim-timed" });
    timedInput.checked = cfg.timed;
    timedInput.addEventListener("change", () => { cfg.timed = timedInput.checked; });
    extras.append(
      h("label", { for: "sim-weak" }, weakInput, "Priorizar las que más fallé"),
      h("label", { for: "sim-timed" }, timedInput, "Con reloj (1 min 30 s por pregunta)"));

    const error = h("p", { class: "muted", role: "alert" });
    const start = h("button", { class: "btn", type: "button" }, "Empezar simulacro");
    start.addEventListener("click", () => {
      if (!cfg.blocks.length) { error.textContent = "Elegí al menos un bloque."; return; }
      store.set("simConfig", cfg);
      startSim(cfg);
    });

    root.appendChild(h("div", { class: "grid-2" },
      h("div", { class: "panel config" },
        h("div", { class: "field" }, h("span", {}, "Cantidad de preguntas"), nBox),
        h("div", { class: "field" }, h("span", {}, "Bloques"), blockBox),
        h("div", { class: "field" }, h("span", {}, "Modo"), modeBox),
        h("div", { class: "field" }, h("span", {}, "Opciones"), extras),
        h("div", { class: "row" }, start, error)),
      renderHistoryPanel()));
  }

  function renderHistoryPanel() {
    const history = store.get("history", []);
    const panel = h("div", { class: "panel" }, h("h3", {}, "Intentos anteriores"));
    if (!history.length) {
      panel.appendChild(h("p", { class: "muted" }, "Todavía no hiciste ningún simulacro. Un buen primer objetivo: 20 preguntas en modo examen."));
      panel.appendChild(h("p", { class: "muted" }, `El banco tiene ${window.BANK.length} preguntas de ${(window.LESSONS || []).length} lecciones.`));
      return panel;
    }
    const table = h("table", { class: "history" },
      h("thead", {}, h("tr", {}, h("th", {}, "Fecha"), h("th", {}, "Preguntas"), h("th", {}, "Nota"))),
      h("tbody", {}, history.slice().reverse().map((r) =>
        h("tr", {}, h("td", {}, new Date(r.at).toLocaleString("es-AR", { dateStyle: "short", timeStyle: "short" })),
          h("td", { class: "num" }, `${r.correct}/${r.n}`),
          h("td", { class: "num" }, h("span", { class: "chip " + (r.grade >= 7 ? "ok" : r.grade >= 4 ? "neutral" : "bad") }, r.grade.toFixed(1)))))));
    panel.appendChild(h("div", { class: "table-wrap" }, table));
    return panel;
  }

  function startSim(cfg) {
    let pool = window.BANK.filter((q) => cfg.blocks.includes(q.block));
    if (cfg.weak) {
      const misses = store.get("misses", {});
      pool = shuffle(pool).sort((a, b) => (misses[b.id] || 0) - (misses[a.id] || 0));
    } else {
      pool = shuffle(pool);
    }
    const n = cfg.n === 0 ? pool.length : Math.min(cfg.n, pool.length);
    sim.questions = shuffle(pool.slice(0, n)).map((q) => ({ ...q, order: shuffle(q.options.map((_, i) => i)) }));
    sim.answers = new Array(sim.questions.length).fill(null);
    sim.idx = 0;
    sim.mode = cfg.mode;
    sim.config = cfg;
    sim.phase = "exam";
    sim.deadline = cfg.timed ? Date.now() + sim.questions.length * 90e3 : null;
    clearInterval(sim.timer);
    if (sim.deadline) sim.timer = setInterval(() => {
      const clock = $("#sim-clock");
      if (!clock) return;
      const left = sim.deadline - Date.now();
      if (left <= 0) { finishSim(); return; }
      clock.textContent = `${Math.floor(left / 60000)}:${String(Math.floor((left % 60000) / 1000)).padStart(2, "0")}`;
    }, 1000);
    renderExam();
  }

  function renderExam() {
    const root = simRoot();
    root.innerHTML = "";
    const q = sim.questions[sim.idx];
    const chosen = sim.answers[sim.idx];
    const reveal = sim.mode === "practica" && chosen !== null;
    const answeredCount = sim.answers.filter((a) => a !== null).length;

    const top = h("div", { class: "exam-top" },
      h("span", { class: "eyebrow num" }, `Pregunta ${sim.idx + 1} de ${sim.questions.length} · ${BLOCKS[q.block].short}`),
      h("span", { class: "row" },
        sim.deadline ? h("span", { class: "chip num", id: "sim-clock" }, "…") : null,
        h("span", { class: "chip neutral num" }, `${answeredCount} respondidas`)));
    const bar = h("div", { class: "bar" }, h("span", { style: `width:${Math.round(((sim.idx + 1) / sim.questions.length) * 100)}%` }));

    const options = h("div", { class: "options" });
    q.order.forEach((optIndex, pos) => {
      const btn = h("button", { class: "option", type: "button", disabled: reveal },
        h("span", { class: "key" }, LETTERS[pos] + ")"), h("span", {}, q.options[optIndex]));
      if (chosen === optIndex) btn.classList.add("chosen");
      if (reveal) {
        if (optIndex === q.answer) btn.classList.add("correct");
        else if (optIndex === chosen) btn.classList.add("wrong");
      }
      btn.addEventListener("click", () => { sim.answers[sim.idx] = optIndex; renderExam(); });
      options.appendChild(btn);
    });

    const prev = h("button", { class: "btn ghost", type: "button", disabled: sim.idx === 0 }, "← Anterior");
    prev.addEventListener("click", () => { sim.idx -= 1; renderExam(); });
    const last = sim.idx === sim.questions.length - 1;
    const next = h("button", { class: "btn" + (last ? "" : " ghost"), type: "button" }, last ? "Terminar y corregir" : "Siguiente →");
    next.addEventListener("click", () => { if (last) finishSim(); else { sim.idx += 1; renderExam(); } });
    const quit = h("button", { class: "btn ghost", type: "button" }, "Terminar ahora");
    quit.addEventListener("click", finishSim);

    const dots = h("div", { class: "dots", "aria-label": "Ir a una pregunta" });
    sim.questions.forEach((qq, i) => {
      const d = h("button", { type: "button", "aria-label": `Pregunta ${i + 1}` }, String(i + 1));
      if (sim.answers[i] !== null) d.classList.add("answered");
      if (sim.mode === "practica" && sim.answers[i] !== null) d.classList.add(sim.answers[i] === qq.answer ? "ok" : "bad");
      if (i === sim.idx) d.classList.add("current");
      d.addEventListener("click", () => { sim.idx = i; renderExam(); });
      dots.appendChild(d);
    });

    root.appendChild(h("div", { class: "exam" },
      top, bar,
      h("div", { class: "q-text", html: q.q }),
      options,
      reveal ? h("div", { class: "why", html: `<strong>${chosen === q.answer ? "Correcto." : "No."}</strong> ${q.why}` }) : null,
      h("div", { class: "row" }, prev, next, h("span", { style: "flex:1" }), quit),
      dots));
  }

  function finishSim() {
    clearInterval(sim.timer);
    sim.phase = "results";
    const n = sim.questions.length;
    const misses = store.get("misses", {});
    let correct = 0;
    const perBlock = {};
    sim.questions.forEach((q, i) => {
      const ok = sim.answers[i] === q.answer;
      if (ok) correct += 1;
      perBlock[q.block] = perBlock[q.block] || { ok: 0, n: 0 };
      perBlock[q.block].n += 1;
      if (ok) perBlock[q.block].ok += 1;
      if (ok) { if (misses[q.id]) misses[q.id] = Math.max(0, misses[q.id] - 1); }
      else misses[q.id] = (misses[q.id] || 0) + 1;
    });
    store.set("misses", misses);
    const grade = n ? (correct / n) * 10 : 0;
    const history = store.get("history", []);
    history.push({ at: Date.now(), n, correct, grade });
    store.set("history", history.slice(-12));

    const root = simRoot();
    root.innerHTML = "";
    const verdict = grade >= 7 ? ["ok", "Muy sólido (≥ 7)"] : grade >= 4 ? ["neutral", "Aprobaría (≥ 4)"] : ["bad", "No aprobaría (< 4)"];
    root.appendChild(h("div", { class: "panel" },
      h("div", { class: "score" },
        h("div", { class: "score-num num" }, grade.toFixed(1).replace(".", ","), h("small", {}, " / 10")),
        h("div", { style: "display:grid;gap:10px" },
          h("div", { class: "row" }, h("span", { class: "chip " + verdict[0] }, verdict[1]), h("span", { class: "muted num" }, `${correct} de ${n} correctas`)),
          ...Object.entries(perBlock).map(([block, r]) => h("div", { class: "meter" },
            h("div", { class: "meter-top" }, h("span", {}, BLOCKS[block].name), h("span", { class: "num muted" }, `${r.ok}/${r.n}`)),
            h("div", { class: "bar" }, h("span", { style: `width:${Math.round((r.ok / r.n) * 100)}%` })))))),
      h("p", { class: "muted", style: "font-size:0.85rem" }, "Nota estimada en escala de 0 a 10, suponiendo que todas las preguntas valen lo mismo. El examen real separa teoría y práctica.")));

    const wrong = sim.questions.map((q, i) => ({ q, chosen: sim.answers[i] })).filter((r) => r.chosen !== r.q.answer);
    const actions = h("div", { class: "row" });
    if (wrong.length) {
      const redo = h("button", { class: "btn", type: "button" }, `Repetir las ${wrong.length} falladas`);
      redo.addEventListener("click", () => {
        sim.questions = shuffle(wrong.map((r) => ({ ...r.q, order: shuffle(r.q.options.map((_, i) => i)) })));
        sim.answers = new Array(sim.questions.length).fill(null);
        sim.idx = 0;
        sim.phase = "exam";
        sim.deadline = null;
        renderExam();
      });
      actions.appendChild(redo);
    }
    const again = h("button", { class: "btn ghost", type: "button" }, "Nuevo simulacro");
    again.addEventListener("click", renderSimConfig);
    actions.appendChild(again);
    root.appendChild(actions);

    if (wrong.length) {
      root.appendChild(h("h3", { style: "margin-top:8px" }, "Revisión de las falladas"));
      root.appendChild(h("ul", { class: "review" }, wrong.map(({ q, chosen }) =>
        h("li", {},
          h("span", { class: "eyebrow" }, `${BLOCKS[q.block].short} · Lección ${lessonNum(q.lesson)}`),
          h("div", { class: "q-text", html: q.q }),
          h("div", { class: "ans" },
            h("span", {}, h("span", { class: "chip bad" }, "Tu respuesta"), " ", chosen === null ? "sin responder" : q.options[chosen]),
            h("span", {}, h("span", { class: "chip ok" }, "Correcta"), " ", q.options[q.answer])),
          h("div", { class: "why", html: q.why }),
          h("a", { href: lessonHref(q.lesson) }, `Repasar la lección ${lessonNum(q.lesson)} →`)))));
    } else {
      root.appendChild(h("p", {}, "Sin errores. Probá con más preguntas o con reloj."));
    }
  }

  renderers.simulacro = function () {
    if (sim.phase === "config") renderSimConfig();
  };

  // ------------------------------------------------------------------ herramientas

  const TOOLS = [
    ["clasificador", "Clasificador"],
    ["joins", "JOINs en Venn"],
    ["orden", "Orden de SQL"],
    ["frases", "Frase → herramienta"]
  ];
  let currentTool = "clasificador";

  function renderToolTabs() {
    const tabs = $("#tool-tabs");
    tabs.innerHTML = "";
    for (const [key, name] of TOOLS) {
      const btn = h("button", { type: "button", role: "tab", "aria-selected": String(key === currentTool) }, name);
      btn.addEventListener("click", () => { currentTool = key; renderToolTabs(); renderTool(); });
      tabs.appendChild(btn);
    }
  }

  function renderTool() {
    const root = $("#tool-root");
    root.innerHTML = "";
    ({ clasificador: toolClassifier, joins: toolJoins, orden: toolOrder, frases: toolPhrases })[currentTool](root);
  }

  // --- Clasificador: one engine, many datasets.
  const drillState = { set: "formas", queue: [], item: null, streak: 0, ok: 0, n: 0 };

  function toolClassifier(root) {
    const setBox = h("div", { class: "segmented", role: "group", "aria-label": "Qué clasificar" });
    for (const [key, drill] of Object.entries(window.DRILLS)) {
      const btn = h("button", { type: "button", "aria-pressed": String(key === drillState.set) }, drill.name);
      btn.addEventListener("click", () => {
        Object.assign(drillState, { set: key, queue: [], item: null, streak: 0, ok: 0, n: 0 });
        renderTool();
      });
      setBox.appendChild(btn);
    }
    const drill = window.DRILLS[drillState.set];
    if (!drillState.queue.length) drillState.queue = shuffle(drill.items);
    if (!drillState.item) drillState.item = drillState.queue.shift();
    const [text, expected] = drillState.item;

    const feedback = h("p", { "aria-live": "polite" });
    const next = h("button", { class: "btn", type: "button", hidden: true }, "Siguiente →");
    next.addEventListener("click", () => { drillState.item = null; renderTool(); });
    const cats = h("div", { class: "cat-grid" });
    for (const cat of drill.categories) {
      const btn = h("button", { type: "button" }, cat);
      btn.addEventListener("click", () => {
        const ok = cat === expected;
        drillState.n += 1;
        if (ok) { drillState.ok += 1; drillState.streak += 1; } else drillState.streak = 0;
        $$("button", cats).forEach((b) => {
          b.disabled = true;
          if (b.textContent === expected) b.classList.add("correct");
        });
        if (!ok) btn.classList.add("wrong");
        feedback.innerHTML = ok ? "<strong>Correcto.</strong>" : `<strong>No:</strong> es <strong>${expected}</strong>.`;
        score.textContent = `${drillState.ok}/${drillState.n}`;
        streak.textContent = String(drillState.streak);
        next.hidden = false;
        next.focus();
      });
      cats.appendChild(btn);
    }
    const score = h("span", { class: "num" }, `${drillState.ok}/${drillState.n}`);
    const streak = h("span", { class: "streak" }, String(drillState.streak));
    root.appendChild(h("div", { class: "grid-2", style: "grid-template-columns: minmax(0,2fr) minmax(0,1fr)" },
      h("div", { class: "panel" },
        setBox,
        h("p", { class: "eyebrow" }, `¿Qué ${drill.name.toLowerCase()} es?`),
        h("div", { class: "drill-item" }, text),
        cats,
        h("div", { class: "row" }, feedback, h("span", { style: "flex:1" }), next)),
      h("div", { class: "panel" },
        h("p", { class: "eyebrow" }, "Esta ronda"),
        h("p", {}, "Aciertos: ", score),
        h("p", {}, "Racha: ", streak),
        h("p", { class: "muted", style: "font-size:0.9rem" }, "Clasificar rápido y en voz baja entrena exactamente lo que pide un choice."),
        drill.lesson ? h("a", { href: lessonHref(drill.lesson) }, `Repasar en la lección ${lessonNum(drill.lesson)}`) : null)));
  }

  // --- JOINs: tables, Venn and live result.
  const CLIENTES = [[1, "Ana"], [2, "Beto"], [3, "Caro"], [4, "Dani"]];
  const FACTURAS = [[10, 1, 100], [11, 1, 50], [12, 2, 80], [13, 3, 20], [14, 9, 70]];
  let joinKind = "INNER";

  function joinRows(kind) {
    const rows = [];
    const matched = new Set();
    for (const [cid, nombre] of CLIENTES) {
      const fs = FACTURAS.filter((f) => f[1] === cid);
      fs.forEach((f) => matched.add(f[0]));
      if (kind === "ANTI") { if (!fs.length) rows.push([cid, nombre, null, null]); continue; }
      if (fs.length) fs.forEach((f) => rows.push([cid, nombre, f[0], f[2]]));
      else if (kind === "LEFT") rows.push([cid, nombre, null, null]);
    }
    if (kind === "RIGHT") {
      // Every invoice survives; the orphan one gets NULL client columns.
      return FACTURAS.map((f) => {
        const c = CLIENTES.find((cl) => cl[0] === f[1]);
        return [c ? c[0] : null, c ? c[1] : null, f[0], f[2]];
      });
    }
    return rows;
  }

  function toolJoins(root) {
    const kinds = [["INNER", "INNER JOIN"], ["LEFT", "LEFT JOIN"], ["RIGHT", "RIGHT JOIN"], ["ANTI", "LEFT JOIN + IS NULL"]];
    const seg = h("div", { class: "segmented", role: "group", "aria-label": "Tipo de JOIN" });
    for (const [key, name] of kinds) {
      const btn = h("button", { type: "button", "aria-pressed": String(key === joinKind) }, name);
      btn.addEventListener("click", () => { joinKind = key; renderTool(); });
      seg.appendChild(btn);
    }
    const leftOnly = joinKind === "LEFT" || joinKind === "ANTI";
    const both = joinKind !== "ANTI";
    const rightOnly = joinKind === "RIGHT";
    const venn = `
      <svg viewBox="0 0 320 190" role="img" aria-label="Diagrama de Venn del ${joinKind} JOIN">
        <defs><clipPath id="clipA"><circle cx="120" cy="95" r="70"/></clipPath></defs>
        <circle cx="120" cy="95" r="70" class="${leftOnly ? "area-on" : "area-off"}"/>
        <circle cx="200" cy="95" r="70" class="${rightOnly ? "area-on" : "area-off"}"/>
        <circle cx="200" cy="95" r="70" clip-path="url(#clipA)" class="${both ? "area-on" : (leftOnly || rightOnly ? "area-cut" : "area-off")}"/>
        <circle cx="120" cy="95" r="70" class="ring"/>
        <circle cx="200" cy="95" r="70" class="ring"/>
        <text x="80" y="100" text-anchor="middle">clientes</text>
        <text x="240" y="100" text-anchor="middle">facturas</text>
      </svg>`;
    const sql = {
      INNER: "SELECT c.nombre, f.id, f.total\nFROM clientes c\nINNER JOIN facturas f ON f.cliente_id = c.id;",
      LEFT: "SELECT c.nombre, f.id, f.total\nFROM clientes c\nLEFT JOIN facturas f ON f.cliente_id = c.id;",
      RIGHT: "SELECT c.nombre, f.id, f.total\nFROM clientes c\nRIGHT JOIN facturas f ON f.cliente_id = c.id;",
      ANTI: "SELECT c.nombre\nFROM clientes c\nLEFT JOIN facturas f ON f.cliente_id = c.id\nWHERE f.id IS NULL;"
    }[joinKind];
    const rows = joinRows(joinKind);
    const result = h("table", {},
      h("thead", {}, h("tr", {}, h("th", {}, "c.nombre"), h("th", {}, "f.id"), h("th", {}, "f.total"))),
      h("tbody", {}, rows.map((r) => h("tr", { class: r.includes(null) ? "null-row" : "" },
        h("td", {}, r[1] ?? "NULL"), h("td", { class: "num" }, r[2] ?? "NULL"), h("td", { class: "num" }, r[3] ?? "NULL")))));
    const tables = h("div", { class: "grid-2" },
      h("div", { class: "table-wrap" }, h("table", {},
        h("thead", {}, h("tr", {}, h("th", {}, "clientes.id"), h("th", {}, "nombre"))),
        h("tbody", {}, CLIENTES.map(([id, n]) => h("tr", {}, h("td", { class: "num" }, id), h("td", {}, n)))))),
      h("div", { class: "table-wrap" }, h("table", {},
        h("thead", {}, h("tr", {}, h("th", {}, "facturas.id"), h("th", {}, "cliente_id"), h("th", {}, "total"))),
        h("tbody", {}, FACTURAS.map(([id, cid, t]) => h("tr", {}, h("td", { class: "num" }, id), h("td", { class: "num" }, cid), h("td", { class: "num" }, t)))))));

    root.appendChild(h("div", { class: "grid-2" },
      h("div", { class: "panel" }, seg, h("div", { class: "venn", html: venn }), h("pre", { class: "code" }, sql)),
      h("div", { class: "panel" },
        h("div", { class: "row", style: "justify-content:space-between" }, h("h3", {}, "Resultado"), h("span", { class: "chip neutral num" }, `${rows.length} filas`)),
        h("div", { class: "table-wrap" }, result),
        h("p", { class: "muted", style: "font-size:0.88rem" }, "La factura 14 apunta al cliente 9, que no existe. Eso violaría la integridad referencial; está solo para que el RIGHT JOIN muestre algo distinto."))));
    root.appendChild(h("div", { class: "panel plain" }, h("h3", {}, "Tablas de ejemplo"), tables));
  }

  // --- Orden lógico de SQL.
  const CLAUSES = ["FROM", "WHERE", "GROUP BY", "HAVING", "SELECT", "ORDER BY", "LIMIT"];
  const orderState = { pool: [], seq: [], checked: false };

  function toolOrder(root) {
    if (!orderState.pool.length && !orderState.seq.length) orderState.pool = shuffle(CLAUSES);
    const pool = h("div", { class: "clause-pool" });
    const seq = h("div", { class: "clause-seq", "aria-label": "Tu orden" });
    orderState.pool.forEach((c) => {
      const b = h("button", { class: "clause", type: "button" }, c);
      b.addEventListener("click", () => { orderState.pool = orderState.pool.filter((x) => x !== c); orderState.seq.push(c); orderState.checked = false; renderTool(); });
      pool.appendChild(b);
    });
    orderState.seq.forEach((c, i) => {
      const cls = orderState.checked ? (CLAUSES[i] === c ? " ok" : " bad") : "";
      const b = h("button", { class: "clause" + cls, type: "button", title: "Quitar" }, `${i + 1}. ${c}`);
      b.addEventListener("click", () => { orderState.seq.splice(i, 1); orderState.pool.push(c); orderState.checked = false; renderTool(); });
      seq.appendChild(b);
    });
    const check = h("button", { class: "btn", type: "button", disabled: orderState.seq.length !== CLAUSES.length }, "Corregir");
    check.addEventListener("click", () => { orderState.checked = true; renderTool(); });
    const reset = h("button", { class: "btn ghost", type: "button" }, "Mezclar de nuevo");
    reset.addEventListener("click", () => { Object.assign(orderState, { pool: shuffle(CLAUSES), seq: [], checked: false }); renderTool(); });
    const allOk = orderState.checked && orderState.seq.every((c, i) => CLAUSES[i] === c);

    root.appendChild(h("div", { class: "grid-2" },
      h("div", { class: "panel" },
        h("h3", {}, "¿En qué orden EVALÚA el motor cada cláusula?"),
        h("p", { class: "muted" }, "Tocá las cláusulas en orden. Tocá una ya elegida para devolverla."),
        pool, seq,
        h("div", { class: "row" }, check, reset),
        orderState.checked ? h("p", {}, allOk ? "Perfecto: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT." : "Hay cláusulas fuera de lugar (en rojo).") : null),
      h("div", { class: "panel" },
        h("h3", {}, "¿Por qué sirve saberlo?"),
        h("p", {}, "Explica las preguntas trampa: WHERE filtra filas ANTES de agrupar y HAVING filtra grupos DESPUÉS. Y como SELECT se evalúa después de WHERE, un alias del SELECT no se puede usar en el WHERE."),
        h("pre", { class: "code" }, "SELECT pais, COUNT(*) AS total   -- 5\nFROM clientes                     -- 1\nWHERE email IS NOT NULL           -- 2\nGROUP BY pais                     -- 3\nHAVING COUNT(*) > 1               -- 4\nORDER BY total DESC               -- 6\nLIMIT 3;                          -- 7"),
        h("a", { href: lessonHref("0035-group-by-having") }, "Lección 0035"))));
  }

  // --- Frase del enunciado -> herramienta SQL.
  let hideTool = false;
  function toolPhrases(root) {
    const toggle = h("button", { class: "btn ghost", type: "button", "aria-pressed": String(hideTool) }, hideTool ? "Mostrar todo" : "Modo práctica: ocultar la herramienta");
    toggle.addEventListener("click", () => { hideTool = !hideTool; renderTool(); });
    let lastGroup = null;
    const rows = [];
    for (const [phrase, tool, group, source] of window.FRASES) {
      if (group && group !== lastGroup) {
        rows.push(h("tr", { class: "phrase-group" }, h("th", { colspan: "2", scope: "colgroup" }, group)));
        lastGroup = group;
      }
      const cell = h("td", { class: hideTool ? "hidden-cell" : "" }, h("span", {}, tool));
      if (hideTool) cell.addEventListener("click", () => cell.classList.remove("hidden-cell"));
      const first = h("td", {}, phrase);
      if (source) first.appendChild(h("span", { class: "phrase-src" }, " · " + source));
      rows.push(h("tr", {}, first, cell));
    }
    const body = h("tbody", {}, rows);
    root.appendChild(h("div", { class: "panel" },
      h("div", { class: "row", style: "justify-content:space-between" },
        h("h3", {}, "Cómo se dice en el enunciado, cómo se escribe en SQL"), toggle),
      h("p", { class: "muted" }, "Sale de la referencia SQL y de las consignas de SUMINISTROS, los TP y los modelos de parcial (1a y 1b). En modo práctica, pensá la herramienta y tocá la celda para comprobarla."),
      h("div", { class: "table-wrap" }, h("table", { class: "eq-table" },
        h("thead", {}, h("tr", {}, h("th", {}, "Si el enunciado dice…"), h("th", {}, "Usá…"))), body)),
      h("a", { href: refHref("0006-sql-ddl-dml") }, "Referencia SQL")));
  }

  renderers.herramientas = function () { renderToolTabs(); renderTool(); };

  // ------------------------------------------------------------------ biblioteca

  renderers.biblioteca = function () {
    const lib = $("#library");
    lib.innerHTML = "";
    for (const [key, block] of Object.entries(BLOCKS)) {
      const list = h("ul", { class: "lib-list" });
      for (const l of (window.LESSONS || []).filter((x) => x.block === key)) {
        const best = store.lessonBest(l.id);
        list.appendChild(h("li", {},
          h("span", {}, h("span", { class: "num-tag" }, lessonNum(l.id)), h("a", { href: l.file }, l.title)),
          h("span", { class: "chip " + (best ? (best.correct / best.total >= 0.8 ? "ok" : "neutral") : "neutral") + " num" },
            best ? `${best.correct}/${best.total}` : `${l.count} preguntas`)));
      }
      lib.appendChild(h("div", { class: "panel" }, h("h3", {}, block.name), list));
    }
    const refs = [
      ["0001-cardinalidad", "Cardinalidad en el DER"], ["0002-normalizacion", "Normalización y pasaje a relacional"],
      ["0003-indices-y-transacciones", "Índices y transacciones"], ["0004-notacion-der-a-mano", "Notación DER a mano"],
      ["0005-del-enunciado-al-der", "Del enunciado al DER"], ["0006-sql-ddl-dml", "SQL en una hoja"]
    ];
    lib.appendChild(h("div", { class: "panel" }, h("h3", {}, "Referencias imprimibles"),
      h("ul", { class: "lib-list" }, refs.map(([id, name]) => h("li", {}, h("a", { href: refHref(id) }, name))))));
    lib.appendChild(h("div", { class: "panel" }, h("h3", {}, "Figuras"),
      h("ul", { class: "lib-list" },
        DIAGRAMS.map(([slug, name]) => h("li", {}, h("a", { href: diagramHref(slug) }, name))))));
    const sources = [
      ["../raw/Clase%201%20%20Udeci.pptx", "Deck · Clase 1: bases de datos, relacional, SQL y ciclo de vida"],
      ["../raw/B%20Clase%202%20Dise%C3%B1o%20Conceptual%20Udeci.pptx", "Deck · Clase 2: diseño conceptual y modelo entidad-relación"],
      ["../raw/Clase%203%20Base%20de%20Datos%20-%20Normalizaci%C3%B3n%20Udeci.pptx", "Deck · Clase 3: normalización"],
      ["../raw/Clase%20Indices%20y%20Txn%20.pptx", "Deck · Índices y transacciones"],
      ["../raw/DDL,%20SP%20,%20Triggers%20.pptx", "Deck · DDL, store procedures y triggers"],
      ["../raw/DML_Base%20de%20Datos.pptx", "Deck · DML"],
      ["../raw/Ej%20DER%20%20Clinica.pptx", "Ejercicio · DER de la Clínica"],
      ["../raw/Intro%20Datawarehouse%20.pptx", "Deck · Introducción al Data Warehouse"],
      ["../raw/Slow%20Change%20Dimension.pptx", "Deck · Slow Change Dimension"],
      ["../raw/TP%20Slow%20Change%20Dimension.pptx", "TP · Slow Change Dimension"],
      ["../raw/SUMINISTROS/Ejercicios-Sql-Consultas.docx", "Ejercicios · 31 consultas SQL sobre SUMINISTROS (docx)"],
      ["../practica/suministros.html", "Práctica · las mismas 31 consultas, con corrección"],
      ["../raw/PAUTAS_EXAMEN.md", "Pautas del examen (lo que dijo el docente)"],
      ["../PARCIAL.md", "Mapa de estudio del parcial"],
      ["../CURRICULUM.md", "Plan de clases: temario completo"]
    ];
    lib.appendChild(h("div", { class: "panel" }, h("h3", {}, "Fuentes de la cátedra"),
      h("ul", { class: "lib-list" }, sources.map(([href, name]) =>
        h("li", {}, h("a", { href, target: href.startsWith("http") ? "_blank" : null, rel: href.startsWith("http") ? "noopener" : null }, name))))));
  };

  // ------------------------------------------------------------------ boot

  function boot() {
    initTheme();
    initCountdown();
    window.addEventListener("hashchange", route);
    route();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
