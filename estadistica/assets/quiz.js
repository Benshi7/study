/* ============================================================================
   quiz.js — shared multiple-choice widget for every lesson of the course.

   Markup contract (see course.css, section "quiz"):

     <div class="quiz" data-quiz>
       <p class="q">1. Question text</p>
       <label><input type="radio" name="q1" value="a"><span class="opt">a. Option</span></label>
       <label><input type="radio" name="q1" value="b"><span class="opt">b. Option</span></label>
       <div class="feedback wrong"   data-for="a">Why option a is wrong.</div>
       <div class="feedback correct" data-for="b">Why option b is right.</div>
     </div>

   Behaviour: choosing an option (mouse, touch, or arrow keys / space on the
   focused radio group) immediately reveals the feedback written for THAT
   option inside the same .quiz. Choosing another option swaps the feedback, so
   every wrong answer can be explored. Feedback is scoped to the parent .quiz,
   so quizzes never interfere with each other and ids are not needed.

   Accessibility: each quiz becomes a labelled radio group, and the verdict is
   also written to a polite live region so screen readers announce it.
   ========================================================================== */

(function () {
  "use strict";

  var uid = 0;

  function qAll(root, selector) {
    return Array.prototype.slice.call(root.querySelectorAll(selector));
  }

  /* One visually hidden live region per quiz: the feedback boxes toggle between
     display:none and display:block, which assistive tech does not announce. */
  function makeLiveRegion(quiz) {
    var live = document.createElement("div");
    live.setAttribute("aria-live", "polite");
    live.setAttribute("role", "status");
    live.style.cssText =
      "position:absolute;width:1px;height:1px;margin:-1px;padding:0;" +
      "overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0;";
    quiz.appendChild(live);
    return live;
  }

  function show(quiz, live, value) {
    var found = null;
    qAll(quiz, ".feedback").forEach(function (box) {
      var match = box.getAttribute("data-for") === value;
      box.style.display = match ? "block" : "none";
      if (match) found = box;
    });
    if (!found) return;

    var verdict = found.classList.contains("correct") ? "Correcto. " : "Incorrecto. ";
    live.textContent = verdict + found.textContent;
  }

  function init(quiz) {
    if (quiz.getAttribute("data-quiz-ready")) return;
    quiz.setAttribute("data-quiz-ready", "1");

    uid += 1;
    var question = quiz.querySelector(".q");
    if (question) {
      if (!question.id) question.id = "quiz-q-" + uid;
      quiz.setAttribute("role", "radiogroup");
      quiz.setAttribute("aria-labelledby", question.id);
    }

    var live = makeLiveRegion(quiz);

    quiz.addEventListener("change", function (event) {
      var input = event.target;
      if (!input || input.type !== "radio" || !quiz.contains(input)) return;
      show(quiz, live, input.value);
    });
  }

  function boot() {
    qAll(document, ".quiz").forEach(init);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
