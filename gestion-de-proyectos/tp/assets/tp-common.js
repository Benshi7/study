// Shared behaviour for every page in tp/: top navigation, copy buttons, countdowns,
// checklist rendering and a storage wrapper that never throws (file:// / private windows).
// Needs tp-data.js (window.TP). Lives only in tp/assets/.
(function () {
  var TP = window.TP || { nav: [], checklist: [], sections: [], dates: {} };
  var memory = {};

  var store = {
    get: function (key) {
      try {
        var v = localStorage.getItem(key);
        return v === null ? (key in memory ? memory[key] : null) : v;
      } catch (e) {
        return key in memory ? memory[key] : null;
      }
    },
    set: function (key, value) {
      memory[key] = value;
      try {
        localStorage.setItem(key, value);
        return true;
      } catch (e) {
        return false; // kept in memory for this page only
      }
    },
    remove: function (key) {
      delete memory[key];
      try {
        localStorage.removeItem(key);
      } catch (e) {
        /* ignore */
      }
    },
  };

  function el(tag, attrs, html) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { node.setAttribute(k, attrs[k]); });
    if (html != null) node.innerHTML = html;
    return node;
  }

  function currentPage() {
    var p = decodeURIComponent(location.pathname.split("/").pop() || "index.html");
    return p || "index.html";
  }

  /* ---- live region + toast ---- */
  var live;
  function say(message) {
    if (!live) {
      live = el("div", { class: "tp-toast", role: "status", "aria-live": "polite" });
      document.body.appendChild(live);
    }
    live.textContent = message;
    live.classList.add("is-on");
    clearTimeout(say.t);
    say.t = setTimeout(function () { live.classList.remove("is-on"); }, 2600);
  }

  /* ---- clipboard (works on file:// where navigator.clipboard may be missing) ---- */
  function copyText(text) {
    function fallback() {
      var area = el("textarea", { "aria-hidden": "true", tabindex: "-1" });
      area.value = text;
      area.style.cssText = "position:fixed;top:0;left:0;opacity:0";
      document.body.appendChild(area);
      area.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
      document.body.removeChild(area);
      return ok;
    }
    if (navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext) {
      return navigator.clipboard.writeText(text).then(function () { return true; }, function () { return fallback(); });
    }
    return Promise.resolve(fallback());
  }

  function bindCopyButtons() {
    document.addEventListener("click", function (event) {
      var btn = event.target.closest("[data-copy]");
      if (!btn) return;
      var source = document.querySelector(btn.getAttribute("data-copy"));
      if (!source) return;
      var text = "value" in source ? source.value : source.textContent;
      copyText(text.replace(/^\n/, "")).then(function (ok) {
        say(ok ? "Copiado al portapapeles" : "No se pudo copiar: seleccionar el texto y copiar a mano");
      });
    });
  }

  /* ---- top navigation ---- */
  function mountNav() {
    var main = document.querySelector("main");
    if (!main || main.querySelector(".tp-top")) return;
    var nav = el("nav", { class: "tp-top", "aria-label": "Navegación del TP" });
    var here = currentPage();
    TP.nav.forEach(function (item) {
      var a = el("a", { href: item.href });
      a.textContent = item.label;
      if (item.href === here) a.setAttribute("aria-current", "page");
      nav.appendChild(a);
    });
    main.insertBefore(nav, main.firstChild);
  }

  /* ---- countdown ---- */
  function daysUntil(iso) {
    var parts = String(iso).split("-").map(Number);
    var target = new Date(parts[0], parts[1] - 1, parts[2]);
    var now = new Date();
    var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    return Math.round((target - today) / 86400000);
  }

  function mountCountdowns() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-countdown]"), function (node) {
      var iso = node.getAttribute("data-countdown");
      var d = daysUntil(iso);
      node.textContent = isNaN(d) ? "" : d > 1 ? "faltan " + d + " días" : d === 1 ? "es mañana" : d === 0 ? "es hoy" : "ya pasó";
    });
  }

  /* ---- coherence checklist (text lives in tp-data.js) ---- */
  function renderChecklist(target, withInputs, isDone, onToggle) {
    target.innerHTML = "";
    TP.checklist.forEach(function (item) {
      var li = el("li");
      if (withInputs) {
        var id = "cl-" + item.id;
        var box = el("input", { type: "checkbox", id: id });
        box.checked = !!(isDone && isDone(item.id));
        box.addEventListener("change", function () { onToggle(item.id, box.checked); });
        var label = el("label", { for: id }, item.html);
        li.appendChild(box);
        li.appendChild(document.createTextNode(" "));
        li.appendChild(label);
      } else {
        li.innerHTML = item.html;
      }
      target.appendChild(li);
    });
  }

  function mountPlainChecklists() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-render='checklist']"), function (ul) {
      renderChecklist(ul, false);
    });
  }

  function statusChip(status) {
    if (status === "guia") return '<span class="chip ok">Guía lista</span>';
    if (status === "pendiente-clase") return '<span class="chip warn">Falta la clase 7</span>';
    return '<span class="chip todo">Al final</span>';
  }

  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  ready(function () {
    mountNav();
    mountCountdowns();
    mountPlainChecklists();
    bindCopyButtons();
  });

  window.TPCommon = {
    store: store,
    copyText: copyText,
    say: say,
    el: el,
    renderChecklist: renderChecklist,
    statusChip: statusChip,
    daysUntil: daysUntil,
    ready: ready,
  };
})();
