// Reusable multiple-choice quiz.
// Markup:
//   <div class="quiz">
//     <p class="prompt">Question</p>
//     <div class="options">
//       <button data-ok data-why="Why this is right">Option</button>
//       <button data-why="Why this is wrong">Option</button>
//     </div>
//   </div>
//   <p class="quiz-score"></p>   (optional, one per page)
// Options are shuffled on load so position never hints at the answer.

(function () {
  const quizzes = [...document.querySelectorAll(".quiz")];
  const scoreEl = document.querySelector(".quiz-score");
  let answered = 0;
  let correct = 0;

  function shuffle(container) {
    const items = [...container.children];
    for (let i = items.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [items[i], items[j]] = [items[j], items[i]];
    }
    items.forEach((el) => container.appendChild(el));
  }

  function updateScore() {
    if (!scoreEl) return;
    scoreEl.textContent = `Resultado: ${correct} de ${quizzes.length} correctas al primer intento (${answered} respondidas).`;
  }

  quizzes.forEach((quiz) => {
    const options = quiz.querySelector(".options");
    const feedback = document.createElement("p");
    feedback.className = "feedback";
    quiz.appendChild(feedback);
    shuffle(options);

    let firstTry = true;
    options.addEventListener("click", (event) => {
      const button = event.target.closest("button");
      if (!button || button.disabled) return;
      const isOk = button.hasAttribute("data-ok");
      button.classList.add(isOk ? "is-ok" : "is-bad");
      feedback.textContent = (isOk ? "✓ " : "✗ ") + (button.dataset.why || "");
      if (firstTry) {
        answered++;
        if (isOk) correct++;
        firstTry = false;
        updateScore();
      }
      if (isOk) options.querySelectorAll("button").forEach((b) => (b.disabled = true));
      else button.disabled = true;
    });
  });

  updateScore();
})();
