/* ============================================================================
   sqlbox.js — in-browser SQL exercise with an automatic, immediate check.

   Runs real SQLite (sql.js 1.10.3 → SQLite 3.45) from cdnjs, so every lesson
   of Unidad 5 can grade a query the moment it is written. The user's code and
   the model solution each run against a FRESH copy of the same database, and
   the two outcomes are compared.

   Markup contract:

     <div class="sqlbox" data-seed="clinica" [data-ordered]>
       <p class="sqlbox__task">What to do.</p>
       <textarea class="sqlbox__code" spellcheck="false">-- starter code</textarea>
       <script type="text/plain" class="sqlbox__setup">  extra SQL run first (optional)  </script>
       <script type="text/plain" class="sqlbox__solution"> model answer </script>
       <script type="text/plain" class="sqlbox__check">    verification SQL (optional) </script>
     </div>

   - data-seed names a database in window.SQL_SEEDS (see assets/seeds/*.js,
     which must be loaded BEFORE this file). Omit it for an empty database.
   - Without a check, the result compared is that of the LAST statement that
     returns rows — of the user's code and of the solution.
   - With a check (DDL / DML / trigger exercises), the user's code runs, then the
     check, and the check's outcome is compared. If the check fails on the
     solution (e.g. an INSERT that a constraint must reject), the exercise
     passes only if it also fails for the user.
   - Rows compare as a multiset; column names are ignored. Add data-ordered
     when ORDER BY is part of the exercise.

   Foreign keys are ON in every database, so referential integrity behaves like
   the cátedra's engines and not like SQLite's lax default.
   ========================================================================== */

(function () {
  "use strict";

  var CDN = "https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/";
  var MAX_ROWS = 30;
  var sqlReady = null;

  function loadSql() {
    if (sqlReady) return sqlReady;
    sqlReady = new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = CDN + "sql-wasm.js";
      s.onload = function () {
        window.initSqlJs({ locateFile: function (f) { return CDN + f; } })
          .then(resolve, reject);
      };
      s.onerror = function () {
        reject(new Error("No se pudo cargar SQLite. Hace falta conexión a internet la primera vez."));
      };
      document.head.appendChild(s);
    });
    return sqlReady;
  }

  function seedFor(name) {
    if (!name) return "";
    var seeds = window.SQL_SEEDS || {};
    if (!(name in seeds)) throw new Error("Falta la base '" + name + "' (assets/seeds/" + name + ".js).");
    return seeds[name];
  }

  /* Runs a script; returns the last result set that had rows-shape, or an error. */
  function run(db, sql) {
    try {
      var res = db.exec(sql);
      return { result: res.length ? res[res.length - 1] : null };
    } catch (e) {
      return { error: String(e.message || e) };
    }
  }

  function outcome(SQL, box, code) {
    var db = new SQL.Database();
    try {
      db.exec("PRAGMA foreign_keys = ON;");
      db.exec(seedFor(box.seed));
      if (box.setup) db.exec(box.setup);
      var r = run(db, code);
      if (r.error) return { error: r.error, stage: "code" };
      if (box.check) {
        var c = run(db, box.check);
        if (c.error) return { error: c.error, stage: "check" };
        return c;
      }
      return r;
    } finally {
      db.close();
    }
  }

  function norm(v) {
    if (v === null || v === undefined) return "NULL";
    if (typeof v === "number") return String(Math.round(v * 1e6) / 1e6);
    if (v instanceof Uint8Array) return "[blob]";
    return String(v);
  }

  function rowKeys(result) {
    return result.values.map(function (row) { return row.map(norm).join("␟"); });
  }

  /* Classifies an engine error so a rejection only counts when it comes from the
     same rule: "CHECK constraint failed", "FOREIGN KEY constraint failed", …;
     a structural mistake (bad column count, typo) never counts; anything else is
     a trigger's RAISE, whose message the author is free to word. */
  function errorKind(msg) {
    var m = /^([A-Z ]+ constraint failed)/.exec(msg);
    if (m) return m[1];
    if (/syntax error|no such|values were supplied|has no column|already exists|incomplete input/i.test(msg)) return "structural";
    return "raise";
  }

  /* Returns { ok, msg } comparing user outcome against expected outcome. */
  function compare(got, exp, ordered) {
    if (exp.error) {
      if (got.error && got.stage === "code") return { ok: false, msg: "Tu código no llegó a correr: " + got.error };
      if (got.error && errorKind(got.error) !== errorKind(exp.error)) {
        return { ok: false, msg: "La base rechazó la operación, pero no por la regla que se buscaba. El motor dijo: " + got.error };
      }
      if (got.error) return { ok: true, msg: "Correcto: la base rechazó la operación, como debía. El motor dijo: " + got.error };
      return { ok: false, msg: "La operación se aceptó, pero la base debía rechazarla." };
    }
    if (got.error) {
      return { ok: false, msg: (got.stage === "check" ? "Tu código corrió, pero la verificación falló: " : "Error: ") + got.error };
    }
    if (!exp.result && !got.result) return { ok: true, msg: "Correcto." };
    /* sql.js omits empty result sets, so "no result" also means "0 rows". */
    if (!got.result) return { ok: false, msg: "El resultado quedó vacío (0 filas) y se esperaban " + exp.result.values.length + ". ¿Falta el SELECT, o el filtro no deja pasar nada?" };
    if (!exp.result) return { ok: false, msg: "No se esperaba un resultado con filas." };

    var ec = exp.result.columns.length, gc = got.result.columns.length;
    if (ec !== gc) return { ok: false, msg: "Se esperaban " + ec + " columna(s) y tu consulta devuelve " + gc + "." };

    var e = rowKeys(exp.result), g = rowKeys(got.result);
    if (e.length !== g.length) {
      return { ok: false, msg: "Se esperaban " + e.length + " fila(s) y tu consulta devuelve " + g.length + "." };
    }
    var count = {};
    e.forEach(function (k) { count[k] = (count[k] || 0) + 1; });
    var extra = 0;
    g.forEach(function (k) { if (count[k]) count[k]--; else extra++; });
    if (extra) return { ok: false, msg: "La cantidad de filas coincide, pero " + extra + " no son las esperadas. Revisá el filtro o las columnas." };
    if (ordered && e.join("\n") !== g.join("\n")) {
      return { ok: false, msg: "Las filas son las correctas, pero el orden no." };
    }
    return { ok: true, msg: "Correcto: " + e.length + " fila(s), igual que la solución." };
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function table(result) {
    if (!result) return '<p class="sqlbox__note">Sin filas para mostrar (la sentencia no devuelve resultado).</p>';
    var h = '<div class="sqlbox__table"><table class="datos"><thead><tr>';
    result.columns.forEach(function (c) { h += "<th>" + esc(c) + "</th>"; });
    h += "</tr></thead><tbody>";
    result.values.slice(0, MAX_ROWS).forEach(function (row) {
      h += "<tr>" + row.map(function (v) {
        return v === null ? '<td class="dim">NULL</td>' : "<td>" + esc(norm(v)) + "</td>";
      }).join("") + "</tr>";
    });
    h += "</tbody></table></div>";
    var more = result.values.length - MAX_ROWS;
    h += '<p class="sqlbox__note">' + result.values.length + " fila(s)" + (more > 0 ? " — se muestran " + MAX_ROWS : "") + "</p>";
    return h;
  }

  function schema(SQL, box) {
    var db = new SQL.Database();
    try {
      db.exec(seedFor(box.seed));
      if (box.setup) db.exec(box.setup);
      var t = db.exec("SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ORDER BY type, name");
      if (!t.length) return '<p class="sqlbox__note">La base arranca vacía.</p>';
      return '<ul class="sqlbox__schema">' + t[0].values.map(function (r) {
        var cols = db.exec("PRAGMA table_info('" + r[0] + "')")[0].values;
        return "<li><b>" + esc(r[0]) + "</b>(" + cols.map(function (c) {
          return c[5] ? "<u>" + esc(c[1]) + "</u>" : esc(c[1]);
        }).join(", ") + ")</li>";
      }).join("") + "</ul>";
    } finally {
      db.close();
    }
  }

  function storageKey(i) { return "sqlbox:" + location.pathname + ":" + i; }
  function load(i) { try { return localStorage.getItem(storageKey(i)); } catch (e) { return null; } }
  function save(i, v) { try { localStorage.setItem(storageKey(i), v); } catch (e) { /* private mode */ } }

  function text(el, sel) {
    var n = el.querySelector(sel);
    return n ? n.textContent.replace(/^\s*\n/, "").replace(/\s+$/, "") : "";
  }

  function button(label, cls) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "sqlbox__btn" + (cls ? " " + cls : "");
    b.textContent = label;
    return b;
  }

  function init(el, i) {
    var area = el.querySelector(".sqlbox__code");
    if (!area) return;
    var box = {
      seed: el.getAttribute("data-seed"),
      ordered: el.hasAttribute("data-ordered"),
      setup: text(el, ".sqlbox__setup"),
      solution: text(el, ".sqlbox__solution"),
      check: text(el, ".sqlbox__check")
    };
    var starter = area.value;
    var saved = load(i);
    if (saved !== null) area.value = saved;

    var bar = document.createElement("div");
    bar.className = "sqlbox__bar";
    var bCheck = button("Comprobar", "sqlbox__btn--main");
    var bRun = button("Ejecutar");
    var bSchema = button("Tablas");
    var bExp = button("Resultado esperado");
    var bSol = button("Solución");
    var bReset = button("Reiniciar");
    [bCheck, bRun, bSchema, bExp, bSol, bReset].forEach(function (b) { bar.appendChild(b); });
    var hint = document.createElement("span");
    hint.className = "sqlbox__hint";
    hint.textContent = "Ctrl+Enter comprueba";
    bar.appendChild(hint);

    var status = document.createElement("div");
    status.className = "sqlbox__status";
    status.setAttribute("aria-live", "polite");
    var out = document.createElement("div");
    out.className = "sqlbox__out";

    area.insertAdjacentElement("afterend", bar);
    bar.insertAdjacentElement("afterend", status);
    status.insertAdjacentElement("afterend", out);

    function withSql(fn) {
      status.className = "sqlbox__status";
      status.textContent = "Cargando SQLite…";
      loadSql().then(function (SQL) {
        status.textContent = "";
        try { fn(SQL); } catch (e) { status.className = "sqlbox__status is-wrong"; status.textContent = String(e.message || e); }
      }, function (e) {
        status.className = "sqlbox__status is-wrong";
        status.textContent = e.message;
      });
    }

    function show(o) {
      out.innerHTML = o.error
        ? '<p class="sqlbox__err">' + esc(o.error) + "</p>"
        : table(o.result);
    }

    bRun.addEventListener("click", function () {
      withSql(function (SQL) {
        var o = outcome(SQL, { seed: box.seed, setup: box.setup }, area.value);
        show(o);
        if (!o.error) { status.className = "sqlbox__status"; status.textContent = "Ejecutado (sin corregir)."; }
      });
    });

    bCheck.addEventListener("click", function () {
      withSql(function (SQL) {
        var got = outcome(SQL, box, area.value);
        var exp = outcome(SQL, box, box.solution);
        var v = compare(got, exp, box.ordered);
        status.className = "sqlbox__status " + (v.ok ? "is-correct" : "is-wrong");
        status.textContent = (v.ok ? "✓ " : "✗ ") + v.msg;
        el.classList.toggle("is-solved", v.ok);
        show(got);
      });
    });

    bExp.addEventListener("click", function () {
      withSql(function (SQL) {
        var exp = outcome(SQL, box, box.solution);
        status.className = "sqlbox__status";
        status.textContent = exp.error ? "Lo esperado es que la base RECHACE la operación." : "Resultado esperado:";
        out.innerHTML = exp.error ? '<p class="sqlbox__err">' + esc(exp.error) + "</p>" : table(exp.result);
      });
    });

    bSchema.addEventListener("click", function () {
      withSql(function (SQL) {
        status.className = "sqlbox__status";
        status.textContent = "Tablas disponibles (subrayada = parte de la PK):";
        out.innerHTML = schema(SQL, box);
      });
    });

    bSol.addEventListener("click", function () {
      status.className = "sqlbox__status";
      status.textContent = "Solución modelo (intentalo antes de mirarla):";
      out.innerHTML = "<pre><code>" + esc(box.solution) + "</code></pre>";
    });

    bReset.addEventListener("click", function () {
      area.value = starter;
      save(i, starter);
      out.innerHTML = "";
      status.textContent = "";
      el.classList.remove("is-solved");
    });

    area.addEventListener("input", function () { save(i, area.value); });
    area.addEventListener("keydown", function (ev) {
      if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") { ev.preventDefault(); bCheck.click(); }
      if (ev.key === "Tab" && !ev.shiftKey) {
        ev.preventDefault();
        var s = area.selectionStart;
        area.setRangeText("  ", s, area.selectionEnd, "end");
      }
    });

    loadSql().catch(function () { /* reported on first click */ });
  }

  /* Exposed for the offline test harness (node) and for suite/builder.js: same engine and
     same comparison the page uses. */
  window.SQLBox = { outcome: outcome, compare: compare, loadSql: loadSql, table: table, esc: esc, norm: norm };

  if (typeof document !== "undefined" && document.querySelectorAll) {
    Array.prototype.forEach.call(document.querySelectorAll(".sqlbox"), init);
  }
})();
