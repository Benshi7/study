/* ============================================================================
   repaso.js — cram widget shared by the final-review pages.

   Markup contract:

     <div class="toolbar" data-toolbar>          <!-- optional, one per page -->
       <button class="toolbar__btn" data-toggle="exam-mode">Modo examen</button>
       <button class="toolbar__btn" data-toggle="hide-known">Ocultar las que sé</button>
       <button class="toolbar__btn" data-reset>Reiniciar</button>
       <span class="toolbar__count" data-count></span>
     </div>

     <article class="card" data-card="unique-id">
       <p class="card__q">Question</p>
       <ul class="chips">…</ul>
       <details class="reveal">…</details>
       <div class="card__mark">
         <button class="mark" data-mark="ok">La sé</button>
         <button class="mark" data-mark="rev">Repasar</button>
       </div>
     </article>

   Behaviour: each card's status ("ok" / "rev" / none) is stored per card id and
   restored on load, so a second pass can skip what is already known. "Modo
   examen" hides the keywords and the model answers so the card is attempted
   cold — that is the retrieval practice; reading the answer first is not.

   Storage is best-effort. The page must work with storage unavailable (file://
   in a locked-down browser, private windows), so every access is guarded and a
   failure degrades to a session that simply does not persist.
   ========================================================================== */

(function () {
  "use strict";

  var KEY = "repaso:" + (document.body.dataset.repasoKey || location.pathname);

  function load() {
    try {
      return JSON.parse(localStorage.getItem(KEY) || "{}") || {};
    } catch (e) {
      return {};
    }
  }

  function save(state) {
    try {
      localStorage.setItem(KEY, JSON.stringify(state));
    } catch (e) {
      /* Storage blocked or full: the page keeps working, it just forgets. */
    }
  }

  var state = load();
  var cards = Array.prototype.slice.call(document.querySelectorAll("[data-card]"));
  var countEl = document.querySelector("[data-count]");

  function paint(card) {
    var id = card.dataset.card;
    var status = state[id] || "";
    if (status) card.dataset.status = status;
    else card.removeAttribute("data-status");

    card.querySelectorAll("[data-mark]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", btn.dataset.mark === status ? "true" : "false");
    });
  }

  function tally() {
    if (!countEl) return;
    var ok = 0, rev = 0;
    cards.forEach(function (c) {
      var s = state[c.dataset.card];
      if (s === "ok") ok++;
      else if (s === "rev") rev++;
    });
    countEl.textContent =
      ok + " sabidas · " + rev + " a repasar · " + (cards.length - ok - rev) + " sin tocar";
  }

  cards.forEach(function (card) {
    paint(card);
    card.querySelectorAll("[data-mark]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var id = card.dataset.card;
        /* Clicking the active mark clears it, so a mistake is one click to undo. */
        state[id] = state[id] === btn.dataset.mark ? "" : btn.dataset.mark;
        if (!state[id]) delete state[id];
        save(state);
        paint(card);
        tally();
      });
    });
  });

  document.querySelectorAll("[data-toggle]").forEach(function (btn) {
    btn.setAttribute("aria-pressed", "false");
    btn.addEventListener("click", function () {
      var on = btn.getAttribute("aria-pressed") !== "true";
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      document.body.classList.toggle(btn.dataset.toggle, on);
      /* Leaving a reveal open under exam mode would defeat the point. */
      if (btn.dataset.toggle === "exam-mode" && on) {
        document.querySelectorAll(".card .reveal[open]").forEach(function (d) {
          d.open = false;
        });
      }
    });
  });

  document.querySelectorAll("[data-reset]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      state = {};
      save(state);
      cards.forEach(paint);
      tally();
    });
  });

  tally();
})();
