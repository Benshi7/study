/* ===========================================================================
   timer.js — reusable practice timer with an optional "rep" counter.

   Usage in a lesson:

     <div class="timer" data-timer data-seconds="300" data-reps="true"></div>
     <script src="../assets/timer.js"></script>
     <script>renderTimer(document.querySelector('[data-timer]'));</script>

   Options are read from data attributes:
     data-seconds  session length in seconds (default 300)
     data-reps     "true" to show the rep counter (default off)

   The rep counter is the pedagogical point of lesson 1: the learner taps it
   every time they notice attention has wandered. A high count is a good
   session, not a bad one.

   Sound is synthesised with the Web Audio API so the lesson stays a single
   self-contained file with no external assets.
   =========================================================================== */

function renderTimer(root) {
  if (!root) return;

  const total = parseInt(root.dataset.seconds || '300', 10);
  const showReps = root.dataset.reps === 'true';

  let remaining = total;
  let reps = 0;
  let ticking = null;

  const display = document.createElement('div');
  display.className = 'timer__display';

  const caption = document.createElement('div');
  caption.className = 'timer__caption';
  caption.textContent = 'Sentado, ojos cerrados o mirada baja. Cuando quieras.';

  const controls = document.createElement('div');
  controls.className = 'timer__controls';

  const startBtn = document.createElement('button');
  startBtn.type = 'button';
  startBtn.className = 'timer__btn timer__btn--primary';
  startBtn.textContent = 'Empezar';

  const resetBtn = document.createElement('button');
  resetBtn.type = 'button';
  resetBtn.className = 'timer__btn';
  resetBtn.textContent = 'Reiniciar';

  controls.appendChild(startBtn);
  controls.appendChild(resetBtn);

  root.appendChild(display);
  root.appendChild(caption);
  root.appendChild(controls);

  let repBtn = null;
  let repCount = null;

  if (showReps) {
    const wrap = document.createElement('div');
    wrap.className = 'timer__reps';

    repCount = document.createElement('div');
    repCount.className = 'timer__reps-count';
    repCount.textContent = '0';

    const label = document.createElement('div');
    label.className = 'timer__reps-label';
    label.textContent = 'repeticiones — tocá cada vez que notes que te fuiste';

    repBtn = document.createElement('button');
    repBtn.type = 'button';
    repBtn.className = 'timer__btn';
    repBtn.textContent = 'Volví';
    repBtn.style.marginTop = '0.9rem';
    repBtn.addEventListener('click', function () {
      reps += 1;
      repCount.textContent = String(reps);
    });

    wrap.appendChild(repCount);
    wrap.appendChild(label);
    wrap.appendChild(repBtn);
    root.appendChild(wrap);
  }

  function paint() {
    const m = Math.floor(remaining / 60);
    const s = remaining % 60;
    display.textContent = m + ':' + String(s).padStart(2, '0');
  }

  function chime() {
    try {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if (!Ctx) return;
      const ctx = new Ctx();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.value = 528;
      gain.gain.setValueAtTime(0.0001, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.25, ctx.currentTime + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 2.6);
      osc.connect(gain).connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 2.7);
    } catch (e) {
      /* silence is an acceptable failure mode for a meditation timer */
    }
  }

  function stop() {
    clearInterval(ticking);
    ticking = null;
    startBtn.textContent = 'Empezar';
  }

  function finish() {
    stop();
    chime();
    remaining = 0;
    paint();
    caption.textContent = showReps
      ? 'Terminado. ' + reps + ' repeticiones. Cada una fue la práctica en sí.'
      : 'Terminado.';
  }

  startBtn.addEventListener('click', function () {
    if (ticking) {
      stop();
      caption.textContent = 'En pausa.';
      return;
    }
    if (remaining === 0) remaining = total;
    startBtn.textContent = 'Pausar';
    caption.textContent = 'Respirá normal. No la controles, sólo notala.';
    ticking = setInterval(function () {
      remaining -= 1;
      paint();
      if (remaining <= 0) finish();
    }, 1000);
  });

  resetBtn.addEventListener('click', function () {
    stop();
    remaining = total;
    reps = 0;
    if (repCount) repCount.textContent = '0';
    caption.textContent = 'Sentado, ojos cerrados o mirada baja. Cuando quieras.';
    paint();
  });

  paint();
}
