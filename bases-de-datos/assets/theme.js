/* Skin + light/dark switcher for lessons, references and the index.
 * Load it in <head> so the saved choice applies before first paint.
 * Keys are shared with the suite: "bd-suite:theme" (light|dark) and "bd-suite:skin" (rosa|sepia).
 * Everything visual lives in course.css; this only toggles <html data-skin> and <html data-theme>.
 */
(function () {
  "use strict";

  var root = document.documentElement;

  function read(key) {
    try { return JSON.parse(localStorage.getItem("bd-suite:" + key)); } catch (_) { return null; }
  }
  function write(key, value) {
    try { localStorage.setItem("bd-suite:" + key, JSON.stringify(value)); } catch (_) { /* storage unavailable */ }
  }

  function applySkin(skin) {
    if (skin === "sepia") root.setAttribute("data-skin", "sepia");
    else root.removeAttribute("data-skin");
  }
  function applyMode(mode) {
    if (mode === "dark" || mode === "light") root.setAttribute("data-theme", mode);
  }
  function currentMode() {
    return root.getAttribute("data-theme") ||
      (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  }

  applySkin(read("skin"));
  applyMode(read("theme"));

  function mount() {
    if (document.querySelector(".theme-switch")) return;
    var bar = document.createElement("div");
    bar.className = "theme-switch";
    bar.setAttribute("role", "group");
    bar.setAttribute("aria-label", "Tema de la página");

    function button(label, onClick) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = label;
      b.addEventListener("click", onClick);
      bar.appendChild(b);
      return b;
    }

    var rosa = button("Rosa", function () { applySkin("rosa"); write("skin", "rosa"); paint(); });
    var sepia = button("Sepia", function () { applySkin("sepia"); write("skin", "sepia"); paint(); });
    var sep = document.createElement("span");
    sep.className = "sep";
    bar.appendChild(sep);
    var mode = button("", function () {
      var next = currentMode() === "dark" ? "light" : "dark";
      applyMode(next);
      write("theme", next);
      paint();
    });

    function paint() {
      var isSepia = root.getAttribute("data-skin") === "sepia";
      rosa.setAttribute("aria-pressed", String(!isSepia));
      sepia.setAttribute("aria-pressed", String(isSepia));
      mode.textContent = currentMode() === "dark" ? "Claro" : "Oscuro";
      mode.setAttribute("aria-label", currentMode() === "dark" ? "Pasar a modo claro" : "Pasar a modo oscuro");
    }

    paint();
    document.body.appendChild(bar);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount);
  else mount();
})();
