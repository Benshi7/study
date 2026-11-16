/* ============================================================================
   quiz.js — reusable retrieval-practice widget shared by every lesson.

   Markup contract:

     <div class="quiz" data-quiz>
       <span class="quiz__label">Recordá</span>
       <p class="quiz__q">Question text</p>
       <ul class="quiz__options">
         <li><button class="quiz__opt"
                     data-correct
                     data-feedback="Why this is right.">Answer A</button></li>
         <li><button class="quiz__opt"
                     data-feedback="Why this is wrong.">Answer B</button></li>
       </ul>
     </div>

   Behaviour: options are shuffled on every page load, then one click locks the
   question, marks the chosen option, reveals the correct one if missed, and
   prints the per-option feedback immediately. The feedback loop is the point —
   never defer it to a "check answers" button.

   Authoring note: write options in whatever order reads best; the shuffle makes
   source order irrelevant. Never write feedback that refers to an option by
   position ("the first one", "the option above") — say what it claims instead.

   Keep every option the same length in words and characters. Formatting must
   not leak the answer.
   ========================================================================== */

(function () {
  "use strict";

  /* Fisher-Yates over the <li> wrappers, so the correct answer never sits at a
     predictable index. Re-running it on every load also stops the position from
     being memorised across study passes. */
  function shuffle(quiz) {
    var list = quiz.querySelector(".quiz__options");
    if (!list) return;

    var items = Array.prototype.slice.call(list.children);
    for (var i = items.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = items[i];
      items[i] = items[j];
      items[j] = tmp;
    }
    items.forEach(function (item) {
      list.appendChild(item);
    });
  }

  function lock(quiz, chosen) {
    var options = quiz.querySelectorAll(".quiz__opt");
    var isRight = chosen.hasAttribute("data-correct");

    Array.prototype.forEach.call(options, function (opt) {
      opt.disabled = true;
      if (opt === chosen) {
        opt.classList.add(isRight ? "is-correct" : "is-wrong");
      } else if (opt.hasAttribute("data-correct") && !isRight) {
        opt.classList.add("is-missed");
      }
    });

    var feedback = document.createElement("p");
    feedback.className = "quiz__feedback " + (isRight ? "is-correct" : "is-wrong");
    feedback.innerHTML =
      "<b>" + (isRight ? "Correcto." : "No.") + "</b> " +
      (chosen.getAttribute("data-feedback") || "");
    quiz.appendChild(feedback);
    record();
  }

  /* Progress for the study suite (suite/index.html). Once every question on the
     page is answered, keep the best score under "bd-quiz:<lesson id>". Best effort:
     the quiz works the same when storage is unavailable. */
  function record() {
    var all = document.querySelectorAll("[data-quiz]");
    var answered = 0;
    var right = 0;
    Array.prototype.forEach.call(all, function (q) {
      if (q.querySelector(".quiz__feedback")) answered++;
      if (q.querySelector(".quiz__feedback.is-correct")) right++;
    });
    if (answered < all.length) return;
    try {
      var id = location.pathname.split("/").pop().replace(/\.html$/, "");
      var key = "bd-quiz:" + id;
      var best = JSON.parse(localStorage.getItem(key) || "null");
      if (!best || right / all.length > best.correct / best.total) {
        localStorage.setItem(key, JSON.stringify({ correct: right, total: all.length, at: Date.now() }));
      }
    } catch (e) { /* storage unavailable */ }
  }

  function init(quiz) {
    if (quiz.dataset.quizReady) return;
    quiz.dataset.quizReady = "1";

    shuffle(quiz);

    quiz.addEventListener("click", function (event) {
      var opt = event.target.closest(".quiz__opt");
      if (!opt || opt.disabled || !quiz.contains(opt)) return;
      lock(quiz, opt);
    });
  }

  function boot() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-quiz]"), init);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
