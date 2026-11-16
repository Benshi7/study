// Light/dark theme toggle.
// Load synchronously in <head> so data-theme is set before first paint.
// Until the reader chooses, no data-theme is set and CSS follows prefers-color-scheme.

(function () {
  var KEY = "course-theme";
  var root = document.documentElement;

  function stored() {
    try {
      var v = localStorage.getItem(KEY);
      return v === "light" || v === "dark" ? v : null;
    } catch (e) {
      return null;
    }
  }

  function save(value) {
    try {
      localStorage.setItem(KEY, value);
    } catch (e) {
      /* storage blocked: the choice lasts for this page only */
    }
  }

  function systemTheme() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function current() {
    return root.getAttribute("data-theme") || systemTheme();
  }

  var initial = stored();
  if (initial) root.setAttribute("data-theme", initial);

  var SUN =
    '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  var MOON =
    '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';

  function render(button) {
    var dark = current() === "dark";
    button.setAttribute("aria-pressed", String(dark));
    button.setAttribute("aria-label", dark ? "Cambiar a modo claro" : "Cambiar a modo oscuro");
    button.title = dark ? "Modo claro" : "Modo oscuro";
    // Show the icon of the mode the click will switch to.
    button.innerHTML = dark ? SUN : MOON;
  }

  function mount() {
    if (document.querySelector(".theme-toggle")) return;
    var button = document.createElement("button");
    button.type = "button";
    button.className = "theme-toggle";
    render(button);
    button.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      save(next);
      render(button);
    });
    document.body.appendChild(button);

    // Keep the icon right if the system theme changes while no choice was made.
    if (window.matchMedia) {
      var mq = window.matchMedia("(prefers-color-scheme: dark)");
      var onChange = function () {
        if (!stored()) render(button);
      };
      if (mq.addEventListener) mq.addEventListener("change", onChange);
      else if (mq.addListener) mq.addListener(onChange);
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount);
  else mount();
})();
