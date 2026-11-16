// Suite top bar + reading memory. Load with <script src="<base>assets/suite-nav.js" defer></script>.
// - Injects assets/suite.css and a sticky bar: Inicio · Clases · Diagramas · Slides · Repaso.
// - On study pages (clases/*, reference/*): remembers the last page and section read ("Seguir donde quedé")
//   and adds a "Marcar leída" toggle. Both live in localStorage of this browser only.
// - Exposes window.SuiteStore for the hub renderer (assets/suite-render.js).
(function () {
  var script = document.currentScript;
  var ROOT = new URL("..", script ? script.src : location.href).href; // folder that holds assets/
  var KEY_DONE = "suite-progress-v1";
  var KEY_LAST = "suite-last-v1";
  var KEY_UI = "suite-ui-v1";

  function read(key, fallback) {
    try { var v = JSON.parse(localStorage.getItem(key)); return v == null ? fallback : v; } catch (e) { return fallback; }
  }
  function write(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* storage blocked: lasts for this page */ }
  }

  function rel(href) {
    var u = (href || location.href).split("#")[0].split("?")[0];
    if (u.indexOf(ROOT) !== 0) return null;
    var p = decodeURI(u.slice(ROOT.length));
    return p === "" || p.slice(-1) === "/" ? p + "index.html" : p;
  }

  window.SuiteStore = {
    root: ROOT,
    url: function (path) { return new URL(path, ROOT).href; },
    done: function () { return read(KEY_DONE, {}); },
    isDone: function (path) { return !!read(KEY_DONE, {})[path]; },
    setDone: function (path, on) { var d = read(KEY_DONE, {}); if (on) d[path] = Date.now(); else delete d[path]; write(KEY_DONE, d); },
    last: function () { return read(KEY_LAST, null); },
    ui: function () { return read(KEY_UI, {}); },
    setUi: function (id, open) { var d = read(KEY_UI, {}); d[id] = open; write(KEY_UI, d); },
    sim: function () { return read("simulacro-agil-v1", {}); },
  };

  var here = rel();
  var isStudy = here && /^(clases|reference)\//.test(here) && !/\/index\.html$/.test(here);

  function link(href, text, current) {
    var a = document.createElement("a");
    a.href = new URL(href, ROOT).href;
    a.textContent = text;
    if (current) a.setAttribute("aria-current", "page");
    return a;
  }

  function bar() {
    if (document.querySelector(".suite-bar")) return;
    var css = document.createElement("link");
    css.rel = "stylesheet";
    css.href = ROOT + "assets/suite.css";
    document.head.appendChild(css);

    var nav = document.createElement("nav");
    nav.className = "suite-bar";
    nav.setAttribute("aria-label", "Suite de estudio");
    var brand = link("index.html", "", false);
    brand.className = "brand";
    brand.innerHTML = "<b>●</b> Suite";
    nav.appendChild(brand);
    [
      ["index.html", "Inicio", here === "index.html"],
      ["clases/index.html", "Clases", here === "clases/index.html" || isStudy && here.indexOf("clases/") === 0],
      ["diagramas/index.html", "Diagramas", here && here.indexOf("diagramas/") === 0],
      ["slides/index.html", "Slides", here === "slides/index.html"],
      ["repaso.html", "Repaso", here === "repaso.html" || /simulacro|parcial-agil-guia|glosario/.test(here || "")],
    ].forEach(function (x) { nav.appendChild(link(x[0], x[1], x[2])); });

    if (isStudy) {
      var sp = document.createElement("span");
      sp.className = "spacer";
      nav.appendChild(sp);
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "mark";
      var paint = function () {
        var on = window.SuiteStore.isDone(here);
        btn.setAttribute("aria-pressed", on ? "true" : "false");
        btn.textContent = on ? "✓ Leída" : "Marcar leída";
      };
      btn.addEventListener("click", function () { window.SuiteStore.setDone(here, !window.SuiteStore.isDone(here)); paint(); });
      paint();
      nav.appendChild(btn);
    }
    document.body.insertBefore(nav, document.body.firstChild);
  }

  function remember() {
    if (!isStudy || /simulacro/.test(here)) return;
    var title = document.title;
    var save = function (id, label) { write(KEY_LAST, { path: here, title: title, id: id || "", section: label || "", t: Date.now() }); };
    save("", "");
    var heads = Array.prototype.slice.call(document.querySelectorAll("main h2[id]"));
    if (!heads.length || !("IntersectionObserver" in window)) return;
    var timer = null;
    var io = new IntersectionObserver(function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        var current = null;
        heads.forEach(function (h) { if (h.getBoundingClientRect().top < window.innerHeight * 0.4) current = h; });
        if (current) save(current.id, current.textContent.trim());
      }, 400);
    }, { rootMargin: "0px 0px -60% 0px" });
    heads.forEach(function (h) { io.observe(h); });
  }

  function init() { bar(); remember(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
