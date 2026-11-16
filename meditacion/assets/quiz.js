/* ===========================================================================
   quiz.js — reusable retrieval-practice widget.

   Usage in a lesson:

     <div class="quiz" data-quiz></div>
     <script src="../assets/quiz.js"></script>
     <script>
       renderQuiz(document.querySelector('[data-quiz]'), [
         {
           question: 'Question text',
           options: ['Answer one', 'Answer two', 'Answer three'],
           correct: 1,
           feedback: 'Why that answer is the right one.'
         }
       ]);
     </script>

   Design constraints:
   - Options must be kept close to equal length by the lesson author; length is
     a formatting cue and cues defeat retrieval practice.
   - Feedback is immediate and appears on the same screen as the answer.
   - Order of options is preserved (not shuffled) so a printed lesson and the
     interactive lesson describe the same thing.
   =========================================================================== */

function renderQuiz(root, items) {
  if (!root || !items || !items.length) return;

  let index = 0;
  let score = 0;

  function draw() {
    const item = items[index];

    root.innerHTML = '';

    const progress = document.createElement('div');
    progress.className = 'quiz__progress';
    progress.textContent = index + 1 + ' / ' + items.length;

    const kicker = document.createElement('div');
    kicker.className = 'quiz__kicker';
    kicker.textContent = 'Recuperación';

    const question = document.createElement('p');
    question.className = 'quiz__question';
    question.textContent = item.question;

    const list = document.createElement('ul');
    list.className = 'quiz__options';

    const buttons = item.options.map(function (text, i) {
      const li = document.createElement('li');
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'quiz__option';
      button.textContent = text;
      button.addEventListener('click', function () {
        answer(i, buttons, item);
      });
      li.appendChild(button);
      list.appendChild(li);
      return button;
    });

    root.appendChild(kicker);
    root.appendChild(progress);
    root.appendChild(question);
    root.appendChild(list);
  }

  function answer(chosen, buttons, item) {
    const right = chosen === item.correct;
    if (right) score += 1;

    buttons.forEach(function (button, i) {
      button.disabled = true;
      if (i === item.correct) button.classList.add('quiz__option--correct');
      else if (i === chosen) button.classList.add('quiz__option--wrong');
      else button.classList.add('quiz__option--muted');
    });

    const feedback = document.createElement('div');
    feedback.className = 'quiz__feedback';
    const verdict = document.createElement('strong');
    verdict.textContent = right ? 'Correcto. ' : 'No. ';
    feedback.appendChild(verdict);
    feedback.appendChild(document.createTextNode(item.feedback));
    root.appendChild(feedback);

    const next = document.createElement('button');
    next.type = 'button';
    next.className = 'quiz__next';
    next.textContent = index + 1 < items.length ? 'Siguiente' : 'Terminar';
    next.addEventListener('click', function () {
      index += 1;
      if (index < items.length) draw();
      else finish();
    });
    root.appendChild(next);
  }

  function finish() {
    root.innerHTML = '';

    const kicker = document.createElement('div');
    kicker.className = 'quiz__kicker';
    kicker.textContent = 'Resultado';

    const summary = document.createElement('p');
    summary.className = 'quiz__done';
    summary.textContent = score + ' de ' + items.length + '. ' + (
      score === items.length
        ? 'Los conceptos quedaron. Ahora hay que sostener la práctica.'
        : 'Volvé sobre las que fallaste antes de pasar a la próxima lección.'
    );

    const again = document.createElement('button');
    again.type = 'button';
    again.className = 'quiz__next';
    again.textContent = 'Repetir';
    again.addEventListener('click', function () {
      index = 0;
      score = 0;
      draw();
    });

    root.appendChild(kicker);
    root.appendChild(summary);
    root.appendChild(again);
  }

  draw();
}
