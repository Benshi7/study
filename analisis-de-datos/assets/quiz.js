/* Reusable multiple-choice quiz widget.
 *
 * Usage in a lesson:
 *   <div class="quiz" data-quiz-id="0001-calidad"></div>
 *   <script type="application/json" class="quiz-data">
 *     [{ "q": "Question", "options": ["A", "B"], "answer": 0, "why": "Explanation" }]
 *   </script>
 *   <script src="../assets/quiz.js"></script>
 *
 * - "answer" is the index of the correct option in "options" (before shuffling).
 * - Options are shuffled on every load so position never leaks the answer.
 * - Feedback is immediate; the explanation is shown for right and wrong answers.
 * - The best score is stored per quiz id (best effort; storage may be unavailable).
 */
(function () {
  "use strict";

  const STORAGE_PREFIX = "teach-quiz:";

  function shuffle(items) {
    const copy = items.slice();
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }

  function readBest(id) {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_PREFIX + id));
    } catch (_) {
      return null;
    }
  }

  function saveBest(id, correct, total) {
    try {
      const previous = readBest(id);
      if (!previous || correct / total > previous.correct / previous.total) {
        localStorage.setItem(STORAGE_PREFIX + id, JSON.stringify({ correct, total, at: Date.now() }));
      }
    } catch (_) {
      /* storage unavailable: the quiz still works, progress is just not remembered */
    }
  }

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function renderQuestion(question, number, onAnswered) {
    const wrap = el("div", "q");
    wrap.appendChild(el("div", "q-num", "PREGUNTA " + number));
    // A div (not a <p>) so questions can embed <pre class="code"> blocks.
    const text = el("div", "q-text");
    text.innerHTML = question.q;
    wrap.appendChild(text);

    const optionsBox = el("div", "q-options");
    const feedback = el("div", "q-feedback");
    feedback.hidden = true;

    const options = shuffle(question.options.map((label, index) => ({ label, index })));
    const buttons = options.map((option) => {
      const button = el("button", "q-option", option.label);
      button.type = "button";
      button.addEventListener("click", () => {
        const isCorrect = option.index === question.answer;
        buttons.forEach((b, i) => {
          b.disabled = true;
          if (options[i].index === question.answer) b.classList.add("correct");
        });
        if (!isCorrect) button.classList.add("wrong");
        feedback.hidden = false;
        feedback.className = "q-feedback " + (isCorrect ? "ok" : "bad");
        feedback.innerHTML = "<strong>" + (isCorrect ? "CORRECTO. " : "NO. ") + "</strong>" + question.why;
        onAnswered(isCorrect);
      });
      optionsBox.appendChild(button);
      return button;
    });

    wrap.appendChild(optionsBox);
    wrap.appendChild(feedback);
    return wrap;
  }

  function mountQuiz(container, questions) {
    const id = container.dataset.quizId || location.pathname;
    container.innerHTML = "";

    let answered = 0;
    let correct = 0;
    const missed = [];

    const score = el("div", "quiz-score");
    score.hidden = true;

    questions.forEach((question, i) => {
      container.appendChild(
        renderQuestion(question, i + 1, (isCorrect) => {
          answered += 1;
          if (isCorrect) correct += 1;
          else missed.push(question);
          if (answered === questions.length) showScore();
        })
      );
    });
    container.appendChild(score);

    function showScore() {
      saveBest(id, correct, questions.length);
      score.hidden = false;
      score.innerHTML = "";
      score.appendChild(el("div", null, "Resultado: " + correct + " / " + questions.length));
      if (missed.length) {
        const retry = el("button", null, "Repetir solo las falladas");
        retry.type = "button";
        retry.addEventListener("click", () => {
          mountQuiz(container, missed.slice());
          container.scrollIntoView({ behavior: "smooth" });
        });
        score.appendChild(retry);
      }
      const again = el("button", null, "Repetir todo (mezclado)");
      again.type = "button";
      again.addEventListener("click", () => {
        mountQuiz(container, shuffle(questions));
        container.scrollIntoView({ behavior: "smooth" });
      });
      score.appendChild(again);
    }
  }

  function init() {
    document.querySelectorAll(".quiz").forEach((container) => {
      const dataNode = container.nextElementSibling;
      if (!dataNode || !dataNode.classList.contains("quiz-data")) return;
      mountQuiz(container, JSON.parse(dataNode.textContent));
    });

    // Index page: show stored best scores next to each lesson link.
    document.querySelectorAll("[data-progress-for]").forEach((node) => {
      const best = readBest(node.dataset.progressFor);
      node.textContent = best ? "mejor: " + best.correct + "/" + best.total : "sin hacer";
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();

  window.TeachQuiz = { readBest };
})();
