/* Claro / oscuro para los decks.
 * Cargalo en <head>, después del <link id="theme-link">, para que la elección guardada
 * se aplique antes del primer pintado.
 * Comparte la clave "bd-suite:theme" (light|dark) con assets/theme.js: lo que elegiste en
 * las lecciones vale acá y al revés. Pone <html data-mode>, porque runtime.js ya usa
 * data-theme para el nombre del tema del deck. Tecla L o el botón de la esquina.
 */
(function () {
  "use strict";

  var root = document.documentElement;
  var KEY = "bd-suite:theme";

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY)); } catch (_) { return null; }
  }
  function write(value) {
    try { localStorage.setItem(KEY, JSON.stringify(value)); } catch (_) { /* sin storage: no persiste */ }
  }
  function current() {
    return root.getAttribute("data-mode") ||
      (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  }

  var saved = read();
  if (saved === "light" || saved === "dark") root.setAttribute("data-mode", saved);

  var btn;
  function paint() {
    if (!btn) return;
    var dark = current() === "dark";
    btn.textContent = dark ? "Claro" : "Oscuro";
    btn.setAttribute("aria-label", dark ? "Pasar a tema claro" : "Pasar a tema oscuro");
  }
  function toggle() {
    var next = current() === "dark" ? "light" : "dark";
    root.setAttribute("data-mode", next);
    write(next);
    paint();
  }

  function mount() {
    btn = document.createElement("button");
    btn.type = "button";
    btn.className = "mode-btn";
    btn.title = "Cambiar claro / oscuro (L)";
    btn.addEventListener("click", function (e) { toggle(); e.currentTarget.blur(); });
    document.body.appendChild(btn);
    paint();
  }

  document.addEventListener("keydown", function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.key === "l" || e.key === "L") toggle();
  });

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount);
  else mount();
})();
