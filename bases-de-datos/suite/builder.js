/* Constructor SQL · Base de Datos
 * Armá la consulta de cada ejercicio (SUMINISTROS y Slow Change Dimension) arrastrando o tocando
 * piezas de la paleta a los bloques SELECT / FROM / WHERE / GROUP BY / HAVING / ORDER BY, en vez
 * de escribirla de cero. En los ejercicios de vista el constructor envuelve el SELECT en CREATE VIEW.
 * Corre y corrige con el mismo SQLite del navegador que las prácticas (assets/sqlbox.js).
 * Los ejercicios salen de data/exercises.js (node suite/build-exercises.mjs).
 */
(function () {
  "use strict";

  const S = window.SUITE;
  if (!S || !window.EXERCISES) return;
  const { renderers, store, h, $, $$ } = S;

  const BLOCKS = [
    { key: "select", kw: "SELECT", ph: "Qué querés ver: ENVIOS.P_Id, COUNT(*)…" },
    { key: "from", kw: "FROM", ph: "De qué tablas, y cómo se unen (JOIN)" },
    { key: "where", kw: "WHERE", ph: "Condiciones sobre filas" },
    { key: "group", kw: "GROUP BY", ph: "“Para cada…”" },
    { key: "having", kw: "HAVING", ph: "Condiciones sobre grupos (totales, conteos)" },
    { key: "order", kw: "ORDER BY", ph: "Orden del resultado" }
  ];
  const LIST_BLOCKS = new Set(["select", "group", "order"]);
  const NO_COMMA_AFTER = /(?:[(,])$|\b(?:DISTINCT|AS)$/i;
  const EXERCISES = window.EXERCISES;

  // ---------------------------------------------------------------- chips

  const chips = new Map();
  let chipSeq = 0;
  function chip(label, text, kind, title) {
    const c = { id: "c" + chipSeq++, label, text, kind, title: title || text };
    chips.set(c.id, c);
    return c;
  }

  const STATIC = {
    comparar: ["=", "<>", ">", "<", ">=", "<="].map((t) => chip(t, t, "op")),
    logica: ["AND", "OR", "NOT"].map((t) => chip(t, t, "op")),
    predicados: [
      chip("IN (…)", "IN (…)", "op"),
      chip("NOT IN (…)", "NOT IN (…)", "op"),
      chip("BETWEEN … AND …", "BETWEEN … AND …", "op", "Rango inclusivo"),
      chip("LIKE", "LIKE '%…%'", "op"),
      chip("IS NULL", "IS NULL", "op"),
      chip("IS NOT NULL", "IS NOT NULL", "op"),
      chip("EXISTS (…)", "EXISTS (SELECT …)", "op"),
      chip("NOT EXISTS (…)", "NOT EXISTS (SELECT …)", "op")
    ],
    signos: [chip(",", ",", "op"), chip("(", "(", "op"), chip(")", ")", "op"), chip("*", "*", "op"),
      chip("DISTINCT", "DISTINCT", "op", "Sin repetidos"), chip("AS", "AS", "op"), chip("ASC", "ASC", "op"), chip("DESC", "DESC", "op")],
    funciones: [
      chip("COUNT(*)", "COUNT(*)", "agg", "Cuenta filas"),
      chip("COUNT(…)", "COUNT(…)", "agg", "Cuenta valores no nulos"),
      chip("COUNT(DISTINCT …)", "COUNT(DISTINCT …)", "agg"),
      chip("SUM(…)", "SUM(…)", "agg"), chip("AVG(…)", "AVG(…)", "agg"),
      chip("MIN(…)", "MIN(…)", "agg"), chip("MAX(…)", "MAX(…)", "agg")
    ],
    patrones: [
      chip("IN (subconsulta)", "IN (SELECT … FROM … WHERE …)", "tpl", "“un dato de otra tabla”, “al menos uno que…”"),
      chip("= mínimo / máximo", "= (SELECT MIN(…) FROM …)", "tpl", "“ningún otro tiene menos”"),
      chip("> promedio", "> (SELECT AVG(…) FROM … WHERE …)", "tpl", "“mayor que la media”. Si dice “de su…”, la subconsulta es correlacionada."),
      chip("NOT EXISTS", "NOT EXISTS (SELECT * FROM … WHERE … = …)", "tpl", "“los que no tienen…”"),
      chip("T1 y T2 (dos filas)", "= 'T1' AND … IN (SELECT … FROM … WHERE … = 'T2')", "tpl", "“T1 y T2”: dos filas distintas cumplen cada parte"),
      chip("todos los existentes", "COUNT(DISTINCT …) = (SELECT COUNT(*) FROM …)", "tpl", "“todos los…”: va en HAVING")
    ]
  };

  const STATIC_IDS = new Set(Object.values(STATIC).flat().map((c) => c.id));

  // ---------------------------------------------------------------- schema (read from the real database)

  const models = {};
  const modelFor = (seed) => models[seed] || (models[seed] = { state: "idle", error: null, tables: [], fks: [], values: [] });

  function loadModel(seed) {
    const model = modelFor(seed);
    if (model.state !== "idle") return;
    model.state = "loading";
    window.SQLBox.loadSql().then((SQL) => {
      const db = new SQL.Database();
      try {
        db.exec(window.SQL_SEEDS[seed]);
        const rows = (res) => (res.length ? res[0].values : []);
        const names = rows(db.exec("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY rowid")).map((r) => r[0]);
        const seen = new Set();
        for (const t of names) {
          const cols = rows(db.exec(`PRAGMA table_info('${t}')`)).map((c) => ({ name: c[1], pk: !!c[5] }));
          model.tables.push({ name: t, cols });
          rows(db.exec(`PRAGMA foreign_key_list('${t}')`)).forEach((f) => model.fks.push({ from: t, col: f[3], to: f[2], toCol: f[4] }));
          for (const c of cols) {
            const vals = rows(db.exec(`SELECT DISTINCT ${c.name} FROM ${t} ORDER BY ${c.name} LIMIT 13`)).map((r) => r[0]);
            const sig = vals.join("|");
            if (vals.length > 12 || seen.has(sig)) continue; // skip free-form numbers and repeated FK columns
            seen.add(sig);
            model.values.push({ table: t, col: c.name, vals });
          }
        }
        model.state = "ready";
      } catch (e) {
        model.state = "error";
        model.error = String(e.message || e);
      } finally {
        db.close();
      }
      if (isOpen()) render();
    }, (e) => {
      model.state = "error";
      model.error = e.message;
      if (isOpen()) render();
    });
  }

  // Views that an exercise's setup script creates ("la vista ya existe"): offered as tables to query.
  const extras = {};
  function loadExtra(ex) {
    const key = keyOf(ex);
    if (!ex.setup || key in extras) return;
    extras[key] = [];
    window.SQLBox.loadSql().then((SQL) => {
      const db = new SQL.Database();
      try {
        db.exec(window.SQL_SEEDS[ex.seed]);
        db.exec(ex.setup);
        const res = db.exec("SELECT name FROM sqlite_master WHERE type = 'view' ORDER BY rowid");
        extras[key] = (res.length ? res[0].values : []).map((r) => ({
          name: r[0],
          cols: db.exec(`PRAGMA table_info('${r[0]}')`)[0].values.map((c) => c[1])
        }));
      } catch (e) { /* the exercise still works without the shortcut */ } finally { db.close(); }
      if (isOpen() && exercise() === ex) render();
    });
  }

  // ---------------------------------------------------------------- state

  const SETS = window.EXERCISE_SETS || [{ set: "suministros", name: "SUMINISTROS" }];
  const inSet = (set) => EXERCISES.filter((e) => e.set === set);
  const lastMap = () => { const v = store.get("bldLast", {}); return v && typeof v === "object" ? v : { suministros: v }; };
  const st = { set: store.get("bldSet", "suministros"), n: 1, active: "select" };
  if (!SETS.some((x) => x.set === st.set)) st.set = SETS[0].set;
  st.n = lastMap()[st.set] || 1;
  if (!inSet(st.set).some((e) => e.n === st.n)) st.n = 1;
  const exercise = () => inSet(st.set).find((e) => e.n === st.n);
  // SUMINISTROS keeps its original storage keys (plain numbers) so earlier progress survives.
  const keyOf = (e) => (e.set === "suministros" ? "" : e.set + ":") + e.n;
  const saved = () => store.get("bld", {});
  const done = () => store.get("bldDone", {});
  const isOpen = () => !$("#v-armar").hidden;

  let els = {};      // block key -> textarea
  let ui = {};       // status/out containers of the current render

  // ---------------------------------------------------------------- inserting pieces

  function insert(key, c) {
    const ta = els[key];
    if (!ta) return;
    const v = ta.value;
    const s = ta._touched ? ta.selectionStart : v.length;
    const e = ta._touched ? ta.selectionEnd : v.length;
    const before = v.slice(0, s);
    const after = v.slice(e);
    const t = before.trimEnd();
    let prefix = "";
    if (t) {
      if (c.kind === "join") prefix = "\n";
      else if (key === "from" && c.kind === "table") prefix = /,$/.test(t) ? " " : ",\n";
      else if (LIST_BLOCKS.has(key) && (c.kind === "col" || c.kind === "agg") && !NO_COMMA_AFTER.test(t)) prefix = ", ";
      else if (!/[\s(]$/.test(before) && !/^[,)]/.test(c.text)) prefix = " ";
    }
    ta.value = before + prefix + c.text + after;
    const start = before.length + prefix.length;
    const hole = c.text.indexOf("…");
    if (hole >= 0) ta.setSelectionRange(start + hole, start + hole + 1);
    else ta.setSelectionRange(start + c.text.length, start + c.text.length);
    ta._touched = true;
    st.active = key;
    ta.focus();
    ta.dispatchEvent(new Event("input", { bubbles: true }));
  }

  function place(c) {
    let key = st.active;
    if (c.kind === "join") key = "from";
    else if (c.kind === "table" && key !== "where" && key !== "having") key = "from";
    insert(key, c);
  }

  function compose() {
    const parts = BLOCKS.map((b) => {
      const v = els[b.key].value.trim().replace(new RegExp("^" + b.kw.replace(" ", "\\s+") + "\\s+", "i"), "");
      return v ? b.kw + " " + v : "";
    }).filter(Boolean);
    return parts.length ? parts.join("\n") + ";" : "";
  }

  // What gets graded: the SELECT as composed, or wrapped in CREATE VIEW for the view exercises.
  function finalSql() {
    const sql = compose();
    const ex = exercise();
    return sql && ex.kind === "view" ? `CREATE VIEW ${ex.view} AS\n${sql}` : sql;
  }

  // ---------------------------------------------------------------- rendering

  function chipEl(c) {
    return h("button", {
      type: "button", class: "bld-chip bld-" + c.kind + (c.pk ? " pk" : ""), draggable: "true", title: c.title,
      onclick: () => place(c),
      ondragstart: (ev) => {
        ev.dataTransfer.setData("application/x-bld-chip", c.id);
        ev.dataTransfer.setData("text/plain", c.text);
        ev.dataTransfer.effectAllowed = "copy";
      }
    }, c.label);
  }

  const section = (title, body, open = true) =>
    h("details", { class: "bld-sec", open }, h("summary", {}, title), h("div", { class: "bld-sec-body" }, body));
  const chipRow = (list) => h("div", { class: "bld-chips" }, list.map(chipEl));

  function palette() {
    // Static chips live for the whole session; the table/column/value chips are rebuilt on every render.
    for (const id of Array.from(chips.keys())) if (!STATIC_IDS.has(id)) chips.delete(id);
    const wrap = h("aside", { class: "panel bld-palette", "aria-label": "Piezas" },
      h("p", { class: "muted bld-howto" }, "Arrastrá una pieza a un bloque, o tocala y va al bloque activo. El primer ", h("code", {}, "…"), " queda seleccionado: la siguiente pieza lo reemplaza. Tab salta al próximo ", h("code", {}, "…"), "."));

    const ex = exercise();
    const model = modelFor(ex.seed);
    const views = extras[keyOf(ex)] || [];
    if (views.length) {
      wrap.appendChild(section("Vistas que ya existen", views.map((v) => {
        const tc = chip(v.name, v.name, "table", "Vista " + v.name);
        const cols = v.cols.map((c) => chip(c, `${v.name}.${c}`, "col", `${v.name}.${c}`));
        return h("div", { class: "bld-tbl" }, chipEl(tc), h("div", { class: "bld-chips" }, cols.map(chipEl)));
      })));
    }
    if (model.state === "ready") {
      const tableChips = model.tables.map((t) => {
        const tc = chip(t.name, t.name, "table", "Tabla " + t.name);
        const cols = t.cols.map((c) => { const x = chip(c.name, `${t.name}.${c.name}`, "col", `${t.name}.${c.name}`); x.pk = c.pk; return x; });
        return h("div", { class: "bld-tbl" }, chipEl(tc), h("div", { class: "bld-chips" }, cols.map(chipEl)));
      });
      const fkRows = model.fks.map((f) => {
        const toP = chip("+ " + f.to, `JOIN ${f.to} ON ${f.to}.${f.toCol} = ${f.from}.${f.col}`, "join");
        const toC = chip("+ " + f.from, `JOIN ${f.from} ON ${f.from}.${f.col} = ${f.to}.${f.toCol}`, "join");
        return h("div", { class: "bld-fk" }, h("span", { class: "muted" }, f.col), chipEl(toP), chipEl(toC));
      });
      const valueRows = model.values.map((g) => h("div", { class: "bld-val-group" },
        h("span", { class: "muted" }, `${g.table}.${g.col}`),
        chipRow(g.vals.map((v) => chip(String(v), typeof v === "number" ? String(v) : `'${v}'`, "val")))));
      wrap.append(
        section("Tablas y columnas", tableChips),
        fkRows.length ? section("Unir tablas (JOIN)", fkRows) : "",
        section("Valores de la base", valueRows, false));
    } else if (model.state === "error") {
      wrap.appendChild(h("p", { class: "bld-err", role: "alert" }, "No se pudieron leer las tablas: " + model.error));
    } else {
      wrap.appendChild(h("p", { class: "muted" }, "Cargando las tablas desde SQLite…"));
    }
    wrap.append(
      section("Comparar y combinar", [chipRow(STATIC.comparar), chipRow(STATIC.logica), chipRow(STATIC.predicados)]),
      section("Funciones", chipRow(STATIC.funciones)),
      section("Signos y modificadores", chipRow(STATIC.signos)),
      section("Patrones de subconsulta", chipRow(STATIC.patrones), false));
    return wrap;
  }

  function blockEl(b, ex) {
    const ta = h("textarea", { class: "bld-ta", rows: "1", spellcheck: "false", placeholder: b.ph, "aria-label": b.kw });
    ta.value = (saved()[keyOf(ex)] || {})[b.key] || "";
    const grow = () => { ta.style.height = "auto"; ta.style.height = Math.max(ta.scrollHeight, 36) + "px"; };
    ta.addEventListener("focus", () => { ta._touched = true; st.active = b.key; paintActive(); });
    ta.addEventListener("input", () => {
      grow();
      const all = saved();
      all[keyOf(ex)] = Object.assign(all[keyOf(ex)] || {}, { [b.key]: ta.value });
      store.set("bld", all);
      if (ui.preview) ui.preview.textContent = finalSql() || "-- Armá la consulta con las piezas";
    });
    ta.addEventListener("keydown", (ev) => {
      if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") { ev.preventDefault(); check(); return; }
      if (ev.key === "Tab" && !ev.shiftKey) {
        const next = ta.value.indexOf("…", ta.selectionEnd);
        if (next >= 0) { ev.preventDefault(); ta.setSelectionRange(next, next + 1); }
      }
    });
    els[b.key] = ta;
    const clear = h("button", { type: "button", class: "bld-x", "aria-label": `Vaciar ${b.kw}`, title: "Vaciar",
      onclick: () => { ta.value = ""; ta.dispatchEvent(new Event("input", { bubbles: true })); ta.focus(); } }, "×");
    const card = h("div", { class: "bld-block", "data-block": b.key },
      h("label", { class: "bld-kw", onclick: () => ta.focus() }, b.kw), ta, clear);
    const wants = (ev) => Array.from(ev.dataTransfer ? ev.dataTransfer.types : []).includes("application/x-bld-chip");
    card.addEventListener("dragover", (ev) => { if (wants(ev)) { ev.preventDefault(); ev.dataTransfer.dropEffect = "copy"; card.classList.add("over"); } });
    card.addEventListener("dragleave", (ev) => { if (!card.contains(ev.relatedTarget)) card.classList.remove("over"); });
    card.addEventListener("drop", (ev) => {
      card.classList.remove("over");
      const c = chips.get(ev.dataTransfer.getData("application/x-bld-chip"));
      if (!c) return;
      ev.preventDefault();
      insert(b.key, c);
    });
    setTimeout(grow, 0);
    return card;
  }

  function paintActive() {
    $$(".bld-block").forEach((c) => c.classList.toggle("active", c.dataset.block === st.active));
  }

  function picker() {
    const d = done();
    const dots = h("div", { class: "dots", role: "group", "aria-label": "Ejercicios" },
      inSet(st.set).map((e) => {
        const btn = h("button", { type: "button", "aria-label": `Ejercicio ${e.n}`, "aria-current": e.n === st.n ? "true" : null }, String(e.n));
        if (d[keyOf(e)]) btn.classList.add("ok");
        if (e.n === st.n) btn.classList.add("current");
        btn.addEventListener("click", () => go(e.n));
        return btn;
      }));
    return dots;
  }

  function go(n) {
    st.n = n;
    st.active = "select";
    const all = lastMap();
    all[st.set] = n;
    store.set("bldLast", all);
    ensureLoaded();
    render();
  }

  function switchSet(set) {
    st.set = set;
    st.n = lastMap()[set] || 1;
    if (!inSet(set).some((e) => e.n === st.n)) st.n = 1;
    st.active = "select";
    store.set("bldSet", set);
    ensureLoaded();
    render();
  }

  function ensureLoaded() {
    const ex = exercise();
    loadModel(ex.seed);
    loadExtra(ex);
  }

  function render() {
    const root = $("#bld-root");
    root.innerHTML = "";
    els = {};
    ui = {};
    const ex = exercise();
    const d = done();
    const list = inSet(st.set);
    const total = list.length;
    const solved = list.filter((e) => d[keyOf(e)]).length;

    ui.status = h("div", { class: "bld-status", "aria-live": "polite" });
    ui.out = h("div", { class: "bld-out" });
    ui.preview = h("pre", { class: "code bld-preview" });

    const prev = h("button", { class: "btn ghost", type: "button", disabled: ex.n === 1, onclick: () => go(ex.n - 1) }, "← Anterior");
    const next = h("button", { class: "btn ghost", type: "button", disabled: ex.n === total, onclick: () => go(ex.n + 1) }, "Siguiente →");

    const actions = h("div", { class: "row" },
      h("button", { class: "btn", type: "button", onclick: check }, "Comprobar"),
      h("button", { class: "btn ghost", type: "button", onclick: () => run(false) }, "Ejecutar"),
      h("button", { class: "btn ghost", type: "button", onclick: expected }, "Resultado esperado"),
      h("button", { class: "btn ghost", type: "button", onclick: solution }, "Solución"),
      h("button", { class: "btn ghost", type: "button", onclick: copy }, "Copiar SQL"),
      h("button", { class: "btn ghost", type: "button", onclick: clearAll }, "Vaciar todo"),
      h("span", { class: "muted bld-keys" }, "Ctrl+Enter comprueba"));

    const canvas = h("div", { class: "bld-canvas" },
      h("div", { class: "panel" },
        h("div", { class: "segmented bld-sets", role: "group", "aria-label": "Conjunto de ejercicios" },
          SETS.map((x) => {
            const btn = h("button", { type: "button", "aria-pressed": String(x.set === st.set) }, `${x.name} (${inSet(x.set).length})`);
            btn.addEventListener("click", () => { if (x.set !== st.set) switchSet(x.set); });
            return btn;
          })),
        h("div", { class: "row", style: "justify-content: space-between" },
          h("p", { class: "eyebrow num" }, `Ejercicio ${ex.n} de ${total}`),
          h("span", { class: "chip neutral num" }, `${solved}/${total} resueltos`)),
        h("p", { class: "bld-task" }, ex.task),
        notes(ex),
        ex.hint ? h("details", { class: "bld-hint" }, h("summary", {}, "Pista: el patrón"), h("p", {}, ex.hint)) : null,
        picker(),
        h("div", { class: "row" }, prev, next)),
      h("div", { class: "bld-blocks" }, BLOCKS.map((b) => blockEl(b, ex))),
      actions, ui.status, ui.out,
      h("div", { class: "panel plain" }, h("p", { class: "eyebrow" }, "Tu consulta"), ui.preview));

    root.appendChild(h("div", { class: "bld" }, canvas, palette()));
    ui.preview.textContent = finalSql() || "-- Armá la consulta con las piezas";
    paintActive();
  }

  function notes(ex) {
    const lines = [];
    if (ex.set === "suministros") lines.push("En la base las claves se llaman P_Id, C_Id y T_Id (el enunciado dice P#, C#, T#).");
    if (ex.set === "scd") lines.push("Las fechas van como AAAA-MM-DD y la foto vigente termina en 2100-12-31.");
    if (ex.kind === "view") lines.push(`Armá sólo el SELECT: el constructor lo envuelve en CREATE VIEW ${ex.view} AS. Usá AS para los nombres de columna.`);
    return h("p", { class: "muted bld-note" }, lines.join(" "));
  }

  // ---------------------------------------------------------------- run / check

  const say = (cls, text) => { ui.status.className = "bld-status " + cls; ui.status.textContent = text; };
  const showOut = (o) => {
    ui.out.innerHTML = o.error
      ? '<p class="bld-err">' + window.SQLBox.esc(o.error) + "</p>"
      : window.SQLBox.table(o.result);
  };

  function withSql(fn) {
    say("", "Cargando SQLite…");
    window.SQLBox.loadSql().then((SQL) => {
      say("", "");
      try { fn(SQL); } catch (e) { say("bad", String(e.message || e)); }
    }, (e) => say("bad", e.message));
  }

  function run() {
    const sql = compose();
    if (!sql) { say("bad", "Todavía no hay consulta: arrastrá piezas a los bloques."); return; }
    withSql((SQL) => {
      const ex = exercise();
      const o = window.SQLBox.outcome(SQL, { seed: ex.seed, setup: ex.setup }, sql);
      showOut(o);
      if (!o.error) say("", "Ejecutado (sin corregir).");
    });
  }

  function check() {
    const sql = finalSql();
    if (!sql) { say("bad", "Todavía no hay consulta: arrastrá piezas a los bloques."); return; }
    const ex = exercise();
    withSql((SQL) => {
      const box = { seed: ex.seed, setup: ex.setup, check: ex.check };
      const got = window.SQLBox.outcome(SQL, box, sql);
      const exp = window.SQLBox.outcome(SQL, box, ex.solution);
      const v = window.SQLBox.compare(got, exp, ex.ordered);
      say(v.ok ? "ok" : "bad", (v.ok ? "✓ " : "✗ ") + v.msg);
      showOut(got);
      if (v.ok) {
        const d = done();
        if (!d[keyOf(ex)]) { d[keyOf(ex)] = true; store.set("bldDone", d); refreshProgress(); }
      }
    });
  }

  function refreshProgress() {
    const d = done();
    const dot = $$(".dots button", $("#bld-root"))[st.n - 1];
    if (dot) dot.classList.add("ok");
    const chipEl2 = $(".bld-canvas .chip.num");
    const list = inSet(st.set);
    if (chipEl2) chipEl2.textContent = `${list.filter((e) => d[keyOf(e)]).length}/${list.length} resueltos`;
  }

  function expected() {
    const ex = exercise();
    withSql((SQL) => {
      const exp = window.SQLBox.outcome(SQL, { seed: ex.seed, setup: ex.setup, check: ex.check }, ex.solution);
      say("", "Resultado esperado:");
      showOut(exp);
    });
  }

  function solution() {
    say("", "Solución modelo (intentalo antes de mirarla):");
    ui.out.innerHTML = "<pre class=\"code\"><code>" + window.SQLBox.esc(exercise().solution) + "</code></pre>";
  }

  function copy() {
    const sql = finalSql();
    if (!sql) return;
    const ok = () => say("", "SQL copiado: pegalo en DBeaver.");
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(sql).then(ok, () => say("bad", "No se pudo copiar."));
    else say("bad", "El navegador no permite copiar desde acá.");
  }

  function clearAll() {
    BLOCKS.forEach((b) => { els[b.key].value = ""; });
    const all = saved();
    delete all[keyOf(exercise())];
    store.set("bld", all);
    ui.out.innerHTML = "";
    say("", "");
    ui.preview.textContent = "-- Armá la consulta con las piezas";
    BLOCKS.forEach((b) => { els[b.key].style.height = "auto"; });
    st.active = "select";
    paintActive();
  }

  // ---------------------------------------------------------------- view

  renderers.armar = function () {
    ensureLoaded();
    render();
  };
})();
