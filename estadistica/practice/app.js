/* Practice app: hash-routed tabs (quiz, guided, calculator, progress). Works from file:// (no fetch). */
(function () {
  'use strict';

  const BANK = Array.isArray(window.BANK) ? window.BANK : [];
  const RECIPES = Array.isArray(window.RECIPES) ? window.RECIPES : [];
  const S = window.Stats;
  const G = window.Generators;
  const view = document.getElementById('view');

  /* ============================== helpers ============================== */
  const TOPIC_LABELS = {
    'descriptiva': 'Descriptiva', 'probabilidad': 'Probabilidad', 'condicional-bayes': 'Condicional y Bayes',
    'contingencia': 'Contingencia', 'va-discreta': 'VA discreta', 'binomial': 'Binomial', 'poisson': 'Poisson',
    'hipergeometrica': 'Hipergeométrica', 'normal': 'Normal', 'suma-variables': 'Suma de variables',
    'muestral-media': 'Muestral: media', 'muestral-proporcion': 'Muestral: proporción', 'ic-media': 'IC media',
    'ic-proporcion': 'IC proporción', 'tamano-muestra': 'Tamaño de muestra', 'regresion': 'Regresión',
  };
  const PART1 = ['descriptiva', 'probabilidad', 'condicional-bayes', 'contingencia', 'va-discreta', 'binomial', 'poisson', 'hipergeometrica'];
  const PART2 = ['normal', 'suma-variables', 'muestral-media', 'muestral-proporcion', 'ic-media', 'ic-proporcion', 'tamano-muestra', 'regresion'];
  const KIND_LABELS = { numeric: 'Numérica', concept: 'Conceptual', planteo: 'Planteo' };
  const DIFF_LABELS = { 1: 'Fácil', 2: 'Media', 3: 'Difícil' };
  const LETTERS = ['A', 'B', 'C', 'D', 'E'];
  const topicLabel = (t) => TOPIC_LABELS[t] || t;

  const esc = (s) => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const ALLOWED_TAGS = 'b|i|u|em|strong|sub|sup|br|code|small|table|thead|tbody|tfoot|tr|th|td|caption|p|ul|ol|li';
  const TAG_RE = new RegExp('&lt;(\\/?)(' + ALLOWED_TAGS + ')((?:\\s+(?:colspan|rowspan)=&quot;\\d+&quot;)*)\\s*(\\/?)&gt;', 'gi');
  /** Inline SVG for scatter plots: only plain shapes/text and presentation attributes, values limited to a safe charset (no scripts, no hrefs, no events). */
  const SVG_RE = new RegExp('&lt;(\\/?)(svg|g|circle|line|path|rect|text|polyline|polygon)((?:\\s+[a-zA-Z0-9-]+=&quot;[\\w\\s.,#%()+:-]*&quot;)*)\\s*(\\/?)&gt;', 'g');
  const SVG_ATTR_RE = /\s+([a-zA-Z0-9-]+)=&quot;([\w\s.,#%()+:-]*)&quot;/g;
  const SVG_ATTRS = new Set(['viewbox', 'width', 'height', 'x', 'y', 'x1', 'y1', 'x2', 'y2', 'cx', 'cy', 'r', 'rx', 'd', 'points', 'fill', 'stroke', 'stroke-width', 'stroke-dasharray', 'stroke-linecap', 'font-size', 'font-family', 'text-anchor', 'transform', 'role', 'class', 'preserveaspectratio', 'xmlns', 'opacity', 'aria-label']);
  /** Escape everything, then re-enable a small whitelist of formatting/table tags (bank text is mostly plain). */
  function rich(s) {
    let out = String(s == null ? '' : s)
      .replace(/&(?!#?\w+;)/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    out = out.replace(TAG_RE, (m, slash, tag, attrs, selfc) => '<' + slash + tag + attrs.replace(/&quot;/g, '"') + selfc + '>');
    out = out.replace(SVG_RE, (m, slash, tag, attrs, selfc) => {
      const clean = attrs.replace(SVG_ATTR_RE, (a, name, val) => (SVG_ATTRS.has(name.toLowerCase()) && !/url|javascript/i.test(val) ? ' ' + name + '="' + val + '"' : ''));
      return '<' + slash + tag + (slash ? '' : clean) + selfc + '>';
    });
    return out.replace(/<table/gi, '<div class="tbl-scroll"><table').replace(/<\/table>/gi, '</table></div>');
  }
  const plain = (s) => String(s == null ? '' : s).replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
  const shuffle = (a) => { const r = a.slice(); for (let i = r.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; } return r; };
  const fmt = G.fmt, fa = G.fa;

  /** Accepts "1,5", "1.5", "1.234,5", "12,5%", unicode minus. Returns {v, pct} or null. */
  function parseNum(raw) {
    let s = String(raw == null ? '' : raw).trim().replace(/\s+/g, '').replace(/−/g, '-');
    let pct = false;
    if (s.endsWith('%')) { pct = true; s = s.slice(0, -1); }
    const hasC = s.includes(','), hasD = s.includes('.');
    if (hasC && hasD) s = s.lastIndexOf(',') > s.lastIndexOf('.') ? s.replace(/\./g, '').replace(',', '.') : s.replace(/,/g, '');
    else if (hasC) s = s.replace(',', '.');
    if (!/^[-+]?(\d+\.?\d*|\.\d+)(e[-+]?\d+)?$/i.test(s)) return null;
    return { v: Number(s), pct };
  }

  /* ============================== storage ============================== */
  const KEY = 'fep-practice-v1';
  let memDb = null;
  function freshDb() { return { q: {}, gen: {}, sim: [] }; }
  function loadDb() {
    try {
      const raw = window.localStorage.getItem(KEY);
      if (raw) {
        const db = JSON.parse(raw);
        if (db && typeof db === 'object') return Object.assign(freshDb(), db);
      }
    } catch (e) { /* storage unavailable: fall back to memory */ }
    return memDb || freshDb();
  }
  function saveDb(db) {
    memDb = db;
    try { window.localStorage.setItem(KEY, JSON.stringify(db)); } catch (e) { /* ignore */ }
  }
  function recordAnswer(id, ok) {
    const db = loadDb();
    const s = db.q[id] || { a: 0, c: 0, t: 0, last: 0 };
    s.a += 1; if (ok) s.c += 1; s.t = Date.now(); s.last = ok ? 1 : 0;
    db.q[id] = s;
    saveDb(db);
  }
  function recordGen(id, firstTry, total) {
    const db = loadDb();
    const g = db.gen[id] || { n: 0, f: 0, s: 0 };
    g.n += 1; g.f += firstTry; g.s += total;
    db.gen[id] = g;
    saveDb(db);
  }
  function errorPool() {
    const db = loadDb();
    const now = Date.now();
    return BANK.map((q) => {
      const s = db.q[q.id];
      if (!s) return null;
      const fails = s.a - s.c;
      if (!(fails > 0 && (s.last === 0 || fails > s.c))) return null;
      return { q, score: fails * 3 + (now - s.t) / 864e5 * 0.5 };
    }).filter(Boolean).sort((a, b) => b.score - a.score).map((x) => x.q);
  }

  /* ============================== router ============================== */
  const TABS = ['quiz', 'guiado', 'calculadora', 'progreso'];
  let currentTab = null;
  let timerId = null;
  function stopTimer() { if (timerId) { clearInterval(timerId); timerId = null; } }

  function route() {
    const parts = decodeURIComponent(location.hash.replace(/^#/, '')).split('/');
    const tab = TABS.includes(parts[0]) ? parts[0] : 'quiz';
    if (currentTab !== tab) stopTimer();
    currentTab = tab;
    document.querySelectorAll('#tabs a').forEach((a) => {
      if (a.dataset.tab === tab) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    if (tab === 'quiz' && quiz.run && quiz.run.mode === 'sim' && quiz.phase === 'run' && !timerId) timerId = setInterval(tickTimer, 1000);
    if (tab === 'quiz') renderQuiz();
    else if (tab === 'guiado') { if (parts[1] && !guided.ex && G.GENERATORS.some((g) => g.id === parts[1])) startGuided(parts[1]); else renderGuided(); }
    else if (tab === 'calculadora') renderCalc();
    else renderProgress();
    window.scrollTo(0, 0);
  }
  window.addEventListener('hashchange', route);

  /* ============================== QUIZ ============================== */
  const quiz = {
    phase: 'config',
    cfg: { topics: new Set(), kinds: new Set(), diffs: new Set(), count: 10, shuffle: true },
    run: null,
  };

  function pool() {
    const c = quiz.cfg;
    return BANK.filter((q) => (!c.topics.size || c.topics.has(q.topic)) && (!c.kinds.size || c.kinds.has(q.kind)) && (!c.diffs.size || c.diffs.has(q.difficulty)));
  }

  function makeItems(questions) {
    return questions.map((q) => {
      let perm = [0, 1, 2, 3, 4];
      const fixed = q.options.some((o) => /ninguna|todas|ambas|las anteriores|a\)|b\)/i.test(o));
      if (quiz.cfg.shuffle && !fixed) perm = shuffle(perm);
      return { q, perm };
    });
  }

  function startRun(questions, mode) {
    if (!questions.length) return;
    stopTimer();
    quiz.phase = 'run';
    quiz.run = { mode, items: makeItems(questions), idx: 0, answers: questions.map(() => null), shown: questions.map(() => 0), start: Date.now(), elapsed: 0, focus: null };
    if (mode === 'sim') timerId = setInterval(tickTimer, 1000);
    renderQuiz();
  }

  function simSelection() {
    // round-robin across topics so the mock exam is mixed
    const byTopic = {};
    shuffle(BANK).forEach((q) => { (byTopic[q.topic] = byTopic[q.topic] || []).push(q); });
    const lists = shuffle(Object.keys(byTopic)).map((t) => byTopic[t]);
    const out = [];
    while (out.length < 20 && lists.some((l) => l.length)) lists.forEach((l) => { if (l.length && out.length < 20) out.push(l.shift()); });
    return shuffle(out);
  }

  function fmtTime(ms) {
    const s = Math.floor(ms / 1000);
    return String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0');
  }
  function tickTimer() {
    const el = document.getElementById('timer');
    if (el && quiz.run) el.textContent = fmtTime(Date.now() - quiz.run.start);
  }

  function renderQuiz() {
    if (!BANK.length) {
      view.innerHTML = '<div class="empty-box">Todavía no hay preguntas cargadas. Generá el banco con <code>python3 practice/build.py</code> y recargá la página.</div>';
      return;
    }
    if (quiz.phase === 'run' && quiz.run) return renderRun();
    if (quiz.phase === 'result' && quiz.run) return renderResult();
    return renderConfig();
  }

  function chipHtml(kind, value, label, pressed, count) {
    return `<button type="button" class="chip" data-toggle="${kind}" data-value="${esc(value)}" aria-pressed="${pressed}">${esc(label)}${count != null ? `<span class="n">${count}</span>` : ''}</button>`;
  }

  function renderConfig() {
    const c = quiz.cfg;
    const countBy = {};
    BANK.forEach((q) => { countBy[q.topic] = (countBy[q.topic] || 0) + 1; });
    const group = (title, key, list) => `
      <div class="fieldset"><div class="legend"><span>${title}</span>
        <button type="button" class="mini" data-group="${key}" data-act="all">todos</button>
        <button type="button" class="mini" data-group="${key}" data-act="none">ninguno</button></div>
        <div class="chips" role="group" aria-label="${title}">${list.filter((t) => countBy[t]).map((t) => chipHtml('topic', t, topicLabel(t), c.topics.has(t), countBy[t])).join('')}</div></div>`;
    const errs = errorPool().length;
    view.innerHTML = `
      <h2>Quiz de práctica</h2>
      ${group('1er parcial', 'p1', PART1)}${group('2do parcial', 'p2', PART2)}
      <div class="fieldset"><div class="legend"><span>Tipo</span></div><div class="chips" role="group" aria-label="Tipo de pregunta">
        ${Object.keys(KIND_LABELS).map((k) => chipHtml('kind', k, KIND_LABELS[k], c.kinds.has(k))).join('')}</div></div>
      <div class="fieldset"><div class="legend"><span>Dificultad</span></div><div class="chips" role="group" aria-label="Dificultad">
        ${[1, 2, 3].map((d) => chipHtml('diff', String(d), DIFF_LABELS[d], c.diffs.has(d))).join('')}</div></div>
      <div class="row">
        <label for="cnt">Cantidad de preguntas</label>
        <input type="number" id="cnt" min="1" max="100" value="${c.count}" style="width:5.5rem">
        <label class="muted" style="display:flex;gap:.4rem;align-items:center"><input type="checkbox" id="shuf" ${c.shuffle ? 'checked' : ''}> Mezclar el orden de las opciones</label>
      </div>
      <p class="hint-text" id="avail" aria-live="polite"></p>
      <div class="row">
        <button type="button" class="btn primary" id="start">Empezar quiz</button>
        <button type="button" class="btn" id="sim">Simulacro (20 mezcladas, con tiempo)</button>
        <button type="button" class="btn ghost" id="rev" ${errs ? '' : 'disabled'}>Repasar mis errores${errs ? ` (${errs})` : ''}</button>
      </div>
      <p class="hint-text">Sin filtros se usan todas las preguntas. En el quiz podés responder con <span class="kbd">1</span>–<span class="kbd">5</span> o <span class="kbd">a</span>–<span class="kbd">e</span> y avanzar con <span class="kbd">Enter</span>.</p>`;
    updateAvail();
  }

  function updateAvail() {
    const el = document.getElementById('avail');
    if (!el) return;
    const n = pool().length;
    el.textContent = n ? `${n} pregunta${n === 1 ? '' : 's'} disponible${n === 1 ? '' : 's'} con estos filtros.` : 'Ninguna pregunta coincide con estos filtros.';
    const start = document.getElementById('start');
    if (start) start.disabled = !n;
  }

  /* ---- run ---- */
  function optionsHtml(run, it, i0) {
    const sim = run.mode === 'sim';
    const chosen = run.answers[i0];
    const locked = !sim && chosen != null;
    const correctDisp = it.perm.indexOf(it.q.answer);
    return it.perm.map((orig, d) => {
      let cls = 'opt';
      if (locked) {
        cls += ' locked';
        if (d === correctDisp) cls += ' correct'; else if (d === chosen) cls += ' wrong'; else cls += ' dim';
      }
      return `<button type="button" class="${cls}" role="radio" aria-checked="${chosen === d}" ${locked ? 'aria-disabled="true"' : ''} data-opt="${d}"><span class="k">${LETTERS[d]}</span><span>${rich(it.q.options[orig])}</span></button>`;
    }).join('');
  }

  function stepsHtml(q, n) {
    return q.steps.slice(0, n).map((s) => `<li class="step"><span class="label">${esc(s.label)}</span>
      ${s.text ? `<p>${rich(s.text)}</p>` : ''}${s.formula ? `<code class="fx">${esc(s.formula)}</code>` : ''}
      ${s.calc ? `<div class="calc-box"><span class="calc-title">🖩 En la calculadora</span><span class="path">${esc(s.calc)}</span></div>` : ''}</li>`).join('');
  }

  function feedbackHtml(run, it, i0) {
    const q = it.q, chosen = run.answers[i0];
    const correctDisp = it.perm.indexOf(q.answer);
    const ok = chosen === correctDisp;
    const trap = ok ? '' : (q.traps[it.perm[chosen]] || '');
    const shown = run.shown[i0];
    const total = q.steps.length;
    return `<div class="verdict ${ok ? 'ok' : 'ko'}" role="status">
        <span class="head">${ok ? '✓ CORRECTO' : '✗ INCORRECTO'}</span>
        ${ok ? '' : `<div>La respuesta correcta es la <strong>${LETTERS[correctDisp]}</strong>.</div>`}
        <p><strong>Por qué:</strong> ${rich(q.why)}</p>
        ${trap ? `<p class="trap">Elegiste esto porque probablemente… ${rich(trap)}</p>` : ''}
      </div>
      <ol class="steps" aria-label="Desarrollo paso a paso">${stepsHtml(q, shown)}</ol>`;
  }

  function renderRun() {
    const run = quiz.run, i0 = run.idx, it = run.items[i0], q = it.q;
    const sim = run.mode === 'sim';
    const answered = run.answers[i0] != null;
    const last = i0 === run.items.length - 1;
    const answeredCount = run.answers.filter((a) => a != null).length;
    const pct = Math.round(((sim ? answeredCount : i0 + (answered ? 1 : 0)) / run.items.length) * 100);
    const shown = run.shown[i0];
    const moreSteps = !sim && answered && shown < q.steps.length;
    const modeLabel = run.mode === 'sim' ? 'Simulacro' : run.mode === 'review' ? 'Repaso de errores' : 'Quiz';
    view.innerHTML = `
      <div class="row spread"><strong>${modeLabel}</strong>${sim ? `<span class="timer" id="timer" aria-label="Tiempo transcurrido">${fmtTime(Date.now() - run.start)}</span>` : ''}</div>
      <div class="progressbar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pct}"><i style="width:${pct}%"></i></div>
      ${sim ? `<div class="navgrid" aria-label="Ir a pregunta">${run.items.map((_, k) => `<button type="button" data-goto="${k}" class="${run.answers[k] != null ? 'answered' : ''}" ${k === i0 ? 'aria-current="true"' : ''} aria-label="Pregunta ${k + 1}${run.answers[k] != null ? ' respondida' : ''}">${k + 1}</button>`).join('')}</div>` : ''}
      <section class="card" aria-labelledby="qhead">
        <div class="q-meta"><strong id="qhead">Pregunta ${i0 + 1} de ${run.items.length}</strong>
          <span class="tag">${esc(topicLabel(q.topic))}</span><span class="tag">${esc(KIND_LABELS[q.kind] || q.kind)}</span><span class="tag">${esc(DIFF_LABELS[q.difficulty] || '')}</span>
          ${q.source && q.source !== 'original' ? `<span>${esc(q.source)}</span>` : ''}</div>
        <div class="q-stem">${rich(q.stem)}</div>
        <div class="opts" role="radiogroup" aria-label="Opciones de respuesta">${optionsHtml(run, it, i0)}</div>
        <div class="fb" id="fb" aria-live="polite">${!sim && answered ? feedbackHtml(run, it, i0) : ''}</div>
      </section>
      <div class="row">
        ${sim ? `<button type="button" class="btn ghost" id="prev" ${i0 === 0 ? 'disabled' : ''}>Anterior</button>
                 <button type="button" class="btn" id="next" ${last ? 'disabled' : ''}>Siguiente</button>
                 <button type="button" class="btn primary" id="finish">Terminar simulacro</button>`
        : `${moreSteps || (answered && shown === 0) ? `<button type="button" class="btn" id="steps">${shown === 0 ? `Ver desarrollo (${q.steps.length} pasos)` : `Siguiente paso (${shown + 1}/${q.steps.length})`}</button>` : ''}
           ${answered ? `<button type="button" class="btn primary" id="next">${last ? 'Ver resultados' : 'Siguiente pregunta'}</button>` : `<span class="hint-text">Elegí una opción (<span class="kbd">1</span>–<span class="kbd">5</span> / <span class="kbd">a</span>–<span class="kbd">e</span>).</span>`}
           <button type="button" class="btn ghost small" id="finish">Terminar ahora</button>`}
      </div>`;
    const f = run.focus; run.focus = null;
    if (f) { const el = document.getElementById(f); if (el) el.focus(); }
  }

  function chooseOption(d) {
    const run = quiz.run;
    if (!run) return;
    const it = run.items[run.idx];
    if (d < 0 || d > 4) return;
    if (run.mode !== 'sim') {
      if (run.answers[run.idx] != null) return;
      run.answers[run.idx] = d;
      recordAnswer(it.q.id, d === it.perm.indexOf(it.q.answer));
      run.focus = 'next';
    } else run.answers[run.idx] = d;
    renderRun();
  }

  function goNext() {
    const run = quiz.run;
    if (run.idx < run.items.length - 1) { run.idx++; window.scrollTo(0, 0); renderRun(); }
    else if (run.mode !== 'sim') finishRun();
  }

  function finishRun() {
    const run = quiz.run;
    stopTimer();
    run.elapsed = Date.now() - run.start;
    if (run.mode === 'sim') {
      run.items.forEach((it, i) => { if (run.answers[i] != null) recordAnswer(it.q.id, run.answers[i] === it.perm.indexOf(it.q.answer)); });
      const db = loadDb();
      const score = run.items.filter((it, i) => run.answers[i] === it.perm.indexOf(it.q.answer)).length;
      db.sim = (db.sim || []).concat([{ t: Date.now(), score, total: run.items.length, secs: Math.round(run.elapsed / 1000) }]).slice(-20);
      saveDb(db);
    }
    quiz.phase = 'result';
    renderResult();
    window.scrollTo(0, 0);
  }

  function renderResult() {
    const run = quiz.run;
    const rows = run.items.map((it, i) => ({ it, i, ans: run.answers[i], ok: run.answers[i] === it.perm.indexOf(it.q.answer) }));
    const score = rows.filter((r) => r.ok).length;
    const total = rows.length;
    const unanswered = rows.filter((r) => r.ans == null).length;
    const wrong = rows.filter((r) => !r.ok);
    const pct = total ? Math.round((score / total) * 100) : 0;
    view.innerHTML = `
      <h2>Resultado</h2>
      <div class="card"><div class="score" aria-live="polite">${score} / ${total} <span class="muted" style="font-size:1.1rem">(${pct}%)</span></div>
        <p class="muted">${run.mode === 'sim' ? `Tiempo: ${fmtTime(run.elapsed)}. ` : ''}${unanswered ? `${unanswered} sin responder (cuentan como incorrectas). ` : ''}${wrong.length ? 'Revisá cada error: la trampa te muestra por qué elegiste esa opción.' : 'Sin errores. Ahora probá con otro tema.'}</p></div>
      <div class="row">
        <button type="button" class="btn primary" id="again">Nuevo quiz</button>
        ${wrong.length ? `<button type="button" class="btn" id="retry">Repasar los que fallé (${wrong.length})</button>` : ''}
      </div>
      <h2>Revisión</h2>
      <div class="review">${rows.map((r) => reviewItem(r)).join('')}</div>`;
  }

  function reviewItem(r) {
    const q = r.it.q;
    const correctDisp = r.it.perm.indexOf(q.answer);
    const trap = r.ok || r.ans == null ? '' : (q.traps[r.it.perm[r.ans]] || '');
    return `<details><summary><span class="${r.ok ? 'ok' : 'ko'}">${r.ok ? '✓' : '✗'}</span> ${r.i + 1}. ${esc(plain(q.stem).slice(0, 110))}${plain(q.stem).length > 110 ? '…' : ''}</summary>
      <div class="body"><div class="q-stem">${rich(q.stem)}</div>
        <p>Tu respuesta: <strong>${r.ans == null ? 'sin responder' : LETTERS[r.ans] + '.'}</strong> ${r.ans == null ? '' : rich(q.options[r.it.perm[r.ans]])}</p>
        <p>Correcta: <strong>${LETTERS[correctDisp]}.</strong> ${rich(q.options[q.answer])}</p>
        <p><strong>Por qué:</strong> ${rich(q.why)}</p>
        ${trap ? `<p class="trap">Elegiste esto porque probablemente… ${rich(trap)}</p>` : ''}
        <ol class="steps">${stepsHtml(q, q.steps.length)}</ol></div></details>`;
  }

  /* ---- quiz events ---- */
  view.addEventListener('click', (e) => {
    if (currentTab !== 'quiz') return;
    const t = e.target.closest('button');
    if (!t || !view.contains(t)) return;
    const c = quiz.cfg;
    if (t.dataset.toggle) {
      const set = t.dataset.toggle === 'topic' ? c.topics : t.dataset.toggle === 'kind' ? c.kinds : c.diffs;
      const val = t.dataset.toggle === 'diff' ? Number(t.dataset.value) : t.dataset.value;
      if (set.has(val)) set.delete(val); else set.add(val);
      t.setAttribute('aria-pressed', String(set.has(val)));
      updateAvail();
    } else if (t.dataset.group) {
      const list = t.dataset.group === 'p1' ? PART1 : PART2;
      list.forEach((k) => { if (t.dataset.act === 'all') c.topics.add(k); else c.topics.delete(k); });
      list.forEach((k) => { const b = view.querySelector(`[data-toggle="topic"][data-value="${k}"]`); if (b) b.setAttribute('aria-pressed', String(c.topics.has(k))); });
      updateAvail();
    } else if (t.id === 'start') {
      const n = Math.max(1, Math.min(100, Number(document.getElementById('cnt').value) || 10));
      c.count = n;
      startRun(shuffle(pool()).slice(0, n), 'normal');
    } else if (t.id === 'sim') startRun(simSelection(), 'sim');
    else if (t.id === 'rev') startRun(errorPool().slice(0, 15), 'review');
    else if (t.dataset.opt != null) chooseOption(Number(t.dataset.opt));
    else if (t.id === 'next') goNext();
    else if (t.id === 'prev') { quiz.run.idx = Math.max(0, quiz.run.idx - 1); renderRun(); }
    else if (t.dataset.goto != null) { quiz.run.idx = Number(t.dataset.goto); renderRun(); }
    else if (t.id === 'steps') {
      const run = quiz.run;
      run.shown[run.idx] = Math.min(run.items[run.idx].q.steps.length, run.shown[run.idx] + 1);
      run.focus = run.shown[run.idx] < run.items[run.idx].q.steps.length ? 'steps' : 'next';
      renderRun();
    } else if (t.id === 'finish') {
      const run = quiz.run;
      const left = run.answers.filter((a) => a == null).length;
      if (run.mode === 'sim' && left && !window.confirm(`Te quedan ${left} preguntas sin responder. ¿Terminar igual?`)) return;
      finishRun();
    } else if (t.id === 'again') { quiz.phase = 'config'; quiz.run = null; renderConfig(); }
    else if (t.id === 'retry') {
      const run = quiz.run;
      startRun(run.items.filter((it, i) => run.answers[i] !== it.perm.indexOf(it.q.answer)).map((it) => it.q), 'review');
    }
  });
  view.addEventListener('change', (e) => {
    if (currentTab !== 'quiz') return;
    if (e.target.id === 'shuf') quiz.cfg.shuffle = e.target.checked;
    if (e.target.id === 'cnt') quiz.cfg.count = Math.max(1, Math.min(100, Number(e.target.value) || 10));
  });
  document.addEventListener('keydown', (e) => {
    if (currentTab !== 'quiz' || quiz.phase !== 'run' || !quiz.run) return;
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    const tag = (e.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
    const k = e.key.toLowerCase();
    let d = -1;
    if (/^[1-5]$/.test(k)) d = Number(k) - 1; else if (/^[a-e]$/.test(k)) d = k.charCodeAt(0) - 97;
    if (d >= 0) { e.preventDefault(); chooseOption(d); return; }
    if (e.key === 'Enter' && tag !== 'button') {
      const run = quiz.run;
      if (run.mode === 'sim' || run.answers[run.idx] != null) { e.preventDefault(); goNext(); }
    }
  });

  /* ============================== GUIDED ============================== */
  const guided = { ex: null, st: [], idx: 0, genId: null };

  function startGuided(id) {
    guided.genId = id;
    guided.ex = G.generate(id);
    guided.st = guided.ex.steps.map(() => ({ state: 'open', tries: 0, wrong: [], value: '', msg: '', first: false }));
    guided.idx = 0;
    renderGuided();
  }

  function renderGuided() {
    if (!guided.ex) {
      const db = loadDb();
      view.innerHTML = `
        <h2>Desarrollo guiado</h2>
        <p>Ejercicios generados al azar, resueltos paso a paso: elegís la distribución, los parámetros y la cola, y cada paso se destraba al responder el anterior. Cada vez salen números y contextos nuevos.</p>
        <div class="row"><button type="button" class="btn primary" data-gen="__random">Ejercicio al azar</button></div>
        <div class="gen-grid">${G.GENERATORS.map((g) => {
          const st = db.gen[g.id];
          return `<button type="button" class="gen-card" data-gen="${g.id}"><span class="t">${esc(g.title)}</span><span class="s">${esc(topicLabel(g.topic))}${st ? ` · ${st.n} resuelto${st.n === 1 ? '' : 's'} · ${Math.round(100 * st.f / Math.max(1, st.s))}% de pasos a la primera` : ''}</span></button>`;
        }).join('')}</div>`;
      return;
    }
    const ex = guided.ex;
    const allDone = guided.st.every((s) => s.state !== 'open');
    let html = `<div class="row spread"><h2 style="margin:0">${esc(ex.title)}</h2><button type="button" class="btn ghost small" data-act="menu">Cambiar de tipo</button></div>
      <div class="card"><div class="q-stem">${rich(ex.stem)}</div></div>`;
    if (ex.givens) html += `<div class="given-box"><span class="gt">${esc(ex.givens.title)}</span>${ex.givens.html}${ex.givens.note ? `<p class="note">${esc(ex.givens.note)}</p>` : ''}</div>`;
    ex.steps.forEach((step, i) => { if (i <= guided.idx) html += stepHtml(step, guided.st[i], i); });
    if (allDone) {
      const first = guided.st.filter((s) => s.first).length;
      html += `<div class="card" role="status"><h3>Ejercicio terminado</h3><p>Resolviste ${first} de ${guided.st.length} pasos a la primera. ${first === guided.st.length ? 'Impecable.' : 'Repetí este tipo hasta que el planteo te salga solo.'}</p>
        <div class="row"><button type="button" class="btn primary" data-act="again">Otro ejercicio igual</button><button type="button" class="btn" data-act="menu">Elegir otro tipo</button></div></div>`;
    }
    view.innerHTML = html;
    const input = document.getElementById('ans');
    if (input) { input.focus(); const v = input.value; input.setSelectionRange(v.length, v.length); }
  }

  function ansText(step) {
    if (step.type === 'choice') return rich(step.options[step.answer]);
    return esc(step.dec === undefined ? fa(step.answer, 4) : fmt(step.answer, step.dec)) + (step.unit ? ' ' + esc(step.unit) : '');
  }

  function stepHtml(step, st, i) {
    const n = `<span class="num">PASO ${i + 1} DE ${guided.ex.steps.length}</span>`;
    if (st.state !== 'open') {
      return `<div class="gstep done">${n}<p class="gp">${esc(step.prompt)}</p>
        <p class="res-line">${st.state === 'solved' ? '<span class="ok">✓ Correcto:</span>' : '<span class="rev">Respuesta:</span>'} ${ansText(step)}${st.state === 'revealed' ? ' <span class="muted">(la revelamos tras los intentos)</span>' : ''}</p>
        <p>${rich(step.explain)}</p>
        ${step.calc ? `<div class="calc-box"><span class="calc-title">🖩 En la calculadora</span><span class="path">${esc(step.calc)}</span></div>` : ''}
        ${step.viz ? bellSvg(step.viz) : ''}</div>`;
    }
    let control;
    if (step.type === 'choice') {
      control = `<div class="opts" role="radiogroup" aria-label="Opciones">${step.options.map((o, k) => {
        const bad = st.wrong.includes(k);
        return `<button type="button" class="opt ${bad ? 'wrong locked' : ''}" role="radio" aria-checked="false" ${bad ? 'aria-disabled="true"' : ''} data-gopt="${k}"><span class="k">${LETTERS[k] || k + 1}</span><span>${rich(o)}</span></button>`;
      }).join('')}</div>`;
    } else {
      control = `<form class="answer-line" data-form="num"><label class="muted" for="ans">Tu respuesta${step.unit ? ` (${esc(step.unit)})` : ''}:</label>
        <input type="text" id="ans" inputmode="decimal" autocomplete="off" value="${esc(st.value)}" aria-describedby="hint-${i}">
        <button type="submit" class="btn primary">Comprobar</button></form>
        <p class="hint-text" id="hint-${i}">Podés usar coma o punto. Se acepta un pequeño margen de redondeo.</p>`;
    }
    const hint = st.msg ? `<div class="hint-box" role="alert">${st.msg}</div>` : '';
    const reveal = st.tries >= 1 ? `<div class="row"><button type="button" class="btn ghost small" data-act="reveal">Mostrar respuesta</button></div>` : '';
    return `<div class="gstep active">${n}<p class="gp">${esc(step.prompt)}</p>${control}${hint}${reveal}</div>`;
  }

  function settleStep(i, state) {
    const st = guided.st[i];
    st.state = state;
    st.first = state === 'solved' && st.tries === 0;
    st.msg = '';
    if (i === guided.idx) {
      guided.idx = Math.min(guided.ex.steps.length - 1, guided.idx + 1);
      if (i === guided.ex.steps.length - 1) {
        const first = guided.st.filter((s) => s.first).length;
        recordGen(guided.ex.gen, first, guided.st.length);
      }
    }
    renderGuided();
  }

  function wrongTry(i, extra) {
    const step = guided.ex.steps[i], st = guided.st[i];
    st.tries += 1;
    if (st.tries >= 2) return settleStep(i, 'revealed');
    const hint = step.hint || (step.type === 'number' ? 'Revisá la fórmula, los signos y si te falta el complemento.' : 'Releé el enunciado y descartá las opciones que contradicen el planteo.');
    st.msg = `<strong>Todavía no.</strong> ${extra || ''}Pista: ${esc(hint)} Probá de nuevo.`;
    renderGuided();
  }

  view.addEventListener('submit', (e) => {
    if (currentTab !== 'guiado' || e.target.dataset.form !== 'num') return;
    e.preventDefault();
    const i = guided.idx, step = guided.ex.steps[i], st = guided.st[i];
    const raw = document.getElementById('ans').value;
    st.value = raw;
    const p = parseNum(raw);
    if (!p) { st.msg = 'Ingresá un número (podés usar coma o punto, por ejemplo 0,1587).'; renderGuided(); return; }
    const v = p.pct && step.unit !== '%' ? p.v / 100 : p.v;
    if (G.checkNumber(step, v)) settleStep(i, 'solved'); else wrongTry(i, '');
  });

  view.addEventListener('click', (e) => {
    if (currentTab !== 'guiado') return;
    const t = e.target.closest('button');
    if (!t || !view.contains(t)) return;
    if (t.dataset.gen) {
      startGuided(t.dataset.gen === '__random' ? G.GENERATORS[Math.floor(Math.random() * G.GENERATORS.length)].id : t.dataset.gen);
    } else if (t.dataset.act === 'menu') { guided.ex = null; renderGuided(); }
    else if (t.dataset.act === 'again') startGuided(guided.genId);
    else if (t.dataset.act === 'reveal') { guided.st[guided.idx].tries = 2; settleStep(guided.idx, 'revealed'); }
    else if (t.dataset.gopt != null) {
      const i = guided.idx, st = guided.st[i], k = Number(t.dataset.gopt);
      if (st.wrong.includes(k)) return;
      if (k === guided.ex.steps[i].answer) settleStep(i, 'solved');
      else { st.wrong.push(k); wrongTry(i, ''); }
    }
  });

  /* ---- mini SVG bell curve with the requested area shaded ---- */
  function bellSvg(v) {
    const W = 340, H = 128, pad = 16, base = 100, top = 12;
    const lo = v.mu - 3.6 * v.sd, hi = v.mu + 3.6 * v.sd;
    const X = (x) => pad + ((x - lo) / (hi - lo)) * (W - 2 * pad);
    const Y = (z) => base - (S.normalPdf(z) / S.normalPdf(0)) * (base - top);
    const zOf = (x) => (x - v.mu) / v.sd;
    const a = Math.max(v.lo, lo), b = Math.min(v.hi, hi);
    const pts = (from, to, n) => Array.from({ length: n + 1 }, (_, i) => { const x = from + ((to - from) * i) / n; return [X(x), Y(zOf(x))]; });
    const curve = pts(lo, hi, 120).map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' ');
    let area = '';
    if (b > a) {
      const ap = pts(a, b, 80);
      area = 'M' + X(a).toFixed(1) + ' ' + base + ' ' + ap.map((p) => 'L' + p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' ') + ' L' + X(b).toFixed(1) + ' ' + base + ' Z';
    }
    const marks = (v.marks || []).filter((m) => m.x > lo && m.x < hi);
    const label = (x) => (v.z ? 'z=' : '') + fa(x, 3);
    const nearMu = marks.some((m) => Math.abs(X(m.x) - X(v.mu)) < 34);
    const desc = `Campana normal con media ${fa(v.mu, 3)} y desvío ${fa(v.sd, 3)}; área sombreada ${v.lo === -Infinity ? 'a la izquierda de ' + label(v.hi) : v.hi === Infinity ? 'a la derecha de ' + label(v.lo) : 'entre ' + label(v.lo) + ' y ' + label(v.hi)}.`;
    return `<svg class="bell" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(desc)}"><title>${esc(desc)}</title>
      <line class="axis" x1="${pad}" y1="${base}" x2="${W - pad}" y2="${base}"/>
      ${area ? `<path class="area" d="${area}"/>` : ''}<path class="curve" d="${curve}"/>
      <line class="axis" x1="${X(v.mu)}" y1="${base}" x2="${X(v.mu)}" y2="${base + 4}"/>
      ${nearMu ? '' : `<text x="${X(v.mu)}" y="${base + 15}" text-anchor="middle">${v.z ? '0' : 'μ=' + fa(v.mu, 3)}</text>`}
      ${marks.map((m) => `<line class="mark" x1="${X(m.x)}" y1="${Y(zOf(m.x))}" x2="${X(m.x)}" y2="${base + 4}"/><text x="${X(m.x)}" y="${base + 15}" text-anchor="middle">${esc(label(m.x))}</text>`).join('')}</svg>`;
  }

  /* ============================== CALCULATOR ============================== */
  const RECIPE_GROUPS = [
    ['calculo-basico', 'Ajustes y cálculo básico'], ['estadistica-descriptiva', 'Estadística descriptiva'],
    ['variable-aleatoria-discreta', 'Variable aleatoria discreta'], ['distribucion-binomial', 'Binomial'],
    ['distribucion-poisson', 'Poisson'], ['distribucion-normal', 'Normal'], ['distribucion-muestral', 'Distribuciones muestrales'],
    ['intervalos-de-confianza', 'Intervalos de confianza'], ['tamano-de-muestra', 'Tamaño de muestra'],
    ['regresion-correlacion', 'Regresión y correlación'], ['limitaciones', 'Limitaciones de la calculadora'],
  ];
  let calcFilter = '';

  function recipeHtml(r) {
    const ex = r.example;
    const exIn = ex && ex.inputs ? Object.keys(ex.inputs).map((k) => `${esc(k)} = ${esc(ex.inputs[k])}`).join(', ') : '';
    return `<article class="recipe"><h3>${esc(r.title)}</h3>
      <p class="when"><strong>Cuándo usarla:</strong> ${esc(r.when)}</p>
      <ol class="keys" aria-label="Teclas">${(r.keys || []).map((k) => `<li><span class="keycap">${esc(k)}</span></li>`).join('')}</ol>
      ${r.inputs && r.inputs.length ? `<table><thead><tr><th>Dato</th><th>Qué es</th></tr></thead><tbody>${r.inputs.map((i) => `<tr><td><code>${esc(i.name)}</code></td><td>${esc(i.meaning)}</td></tr>`).join('')}</tbody></table>` : ''}
      <p class="out"><strong>Resultado:</strong> ${esc(r.output_meaning)}</p>
      ${r.traps && r.traps.length ? `<div><span class="tag-warn">⚠ Trampas</span><ul class="trap-list">${r.traps.map((t) => `<li>${esc(t)}</li>`).join('')}</ul></div>` : ''}
      ${ex ? `<p class="ex"><strong>Ejemplo:</strong> ${exIn}${ex.output != null ? ` → <code>${esc(ex.output)}</code>` : ''}</p>` : ''}</article>`;
  }

  function renderCalc() {
    if (!RECIPES.length) {
      view.innerHTML = '<h2>Calculadora Casio fx-991EX</h2><div class="empty-box">Todavía no hay recetas cargadas. Generalas con <code>python3 practice/build.py</code> y recargá.</div>';
      return;
    }
    view.innerHTML = `<h2>Calculadora Casio fx-991EX</h2>
      <p class="muted">Recetas de teclas para cada situación del final. El examen probablemente da las tablas; la calculadora sirve para verificar y para ahorrar tiempo.</p>
      <div class="row"><label for="rfilter" class="muted">Buscar</label><input type="search" id="rfilter" placeholder="binomial, media, regresión…" value="${esc(calcFilter)}" style="flex:1;min-width:12rem"></div>
      <div id="recipes"></div>`;
    paintRecipes();
  }

  function paintRecipes() {
    const q = calcFilter.trim().toLowerCase();
    const match = (r) => !q || [r.title, r.when, r.output_meaning, (r.keys || []).join(' '), (r.traps || []).join(' ')].join(' ').toLowerCase().includes(q);
    const known = new Set(RECIPE_GROUPS.map((g) => g[0]));
    const groups = RECIPE_GROUPS.concat([...new Set(RECIPES.map((r) => r.topic))].filter((t) => !known.has(t)).map((t) => [t, topicLabel(t)]));
    const html = groups.map(([key, label]) => {
      const items = RECIPES.filter((r) => r.topic === key && match(r));
      return items.length ? `<h2>${esc(label)}</h2><div class="recipes">${items.map(recipeHtml).join('')}</div>` : '';
    }).join('');
    document.getElementById('recipes').innerHTML = html || '<div class="empty-box">Ninguna receta coincide con la búsqueda.</div>';
  }
  view.addEventListener('input', (e) => {
    if (currentTab === 'calculadora' && e.target.id === 'rfilter') { calcFilter = e.target.value; paintRecipes(); }
  });

  /* ============================== PROGRESS ============================== */
  function renderProgress() {
    const db = loadDb();
    const byTopic = {};
    let attempts = 0, correct = 0, seen = 0;
    BANK.forEach((q) => {
      const s = db.q[q.id];
      if (!s) return;
      seen++; attempts += s.a; correct += s.c;
      const t = (byTopic[q.topic] = byTopic[q.topic] || { a: 0, c: 0 });
      t.a += s.a; t.c += s.c;
    });
    const errs = errorPool();
    const barRow = (t) => {
      const d = byTopic[t];
      const pct = d && d.a ? Math.round((100 * d.c) / d.a) : 0;
      const cls = pct >= 75 ? '' : pct >= 50 ? 'mid' : 'low';
      return `<div class="bar-row"><span>${esc(topicLabel(t))}</span><div class="bar" role="img" aria-label="${esc(topicLabel(t))}: ${d ? pct + '% de aciertos' : 'sin intentos'}"><i class="${cls}" style="width:${pct}%"></i></div><span class="muted">${d ? `${pct}% · ${d.c}/${d.a}` : 'sin datos'}</span></div>`;
    };
    const topFails = BANK.map((q) => ({ q, s: db.q[q.id] })).filter((x) => x.s && x.s.a > x.s.c).sort((a, b) => (b.s.a - b.s.c) - (a.s.a - a.s.c)).slice(0, 8);
    const sims = (db.sim || []).slice(-5).reverse();
    view.innerHTML = `
      <h2>Mis errores y progreso</h2>
      <div class="stat-grid">
        <div class="stat"><b>${attempts}</b><span>respuestas</span></div>
        <div class="stat"><b>${attempts ? Math.round((100 * correct) / attempts) : 0}%</b><span>de aciertos</span></div>
        <div class="stat"><b>${seen}/${BANK.length}</b><span>preguntas vistas</span></div>
        <div class="stat"><b>${errs.length}</b><span>para repasar</span></div>
      </div>
      <div class="row">
        <button type="button" class="btn primary" id="p-rev" ${errs.length ? '' : 'disabled'}>Repasar mis errores${errs.length ? ` (${Math.min(15, errs.length)})` : ''}</button>
        <button type="button" class="btn danger small" id="p-reset">Reiniciar progreso</button>
      </div>
      <p class="hint-text">El repaso prioriza lo que más fallaste y hace más tiempo que no ves.</p>
      <h2>Aciertos por tema</h2>
      <h3>1er parcial</h3><div class="bars">${PART1.filter((t) => BANK.some((q) => q.topic === t)).map(barRow).join('')}</div>
      <h3 style="margin-top:1rem">2do parcial</h3><div class="bars">${PART2.filter((t) => BANK.some((q) => q.topic === t)).map(barRow).join('')}</div>
      ${topFails.length ? `<h2>Las más falladas</h2><div class="review">${topFails.map((x) => `<details><summary><span class="ko">${x.s.a - x.s.c}×</span> ${esc(topicLabel(x.q.topic))}: ${esc(plain(x.q.stem).slice(0, 90))}…</summary><div class="body"><div class="q-stem">${rich(x.q.stem)}</div><p><strong>Correcta:</strong> ${rich(x.q.options[x.q.answer])}</p><p>${rich(x.q.why)}</p></div></details>`).join('')}</div>` : ''}
      ${sims.length ? `<h2>Últimos simulacros</h2><ul>${sims.map((s) => `<li>${new Date(s.t).toLocaleDateString('es-AR')}: ${s.score}/${s.total} en ${fmtTime(s.secs * 1000)}</li>`).join('')}</ul>` : ''}
      <h2>Desarrollo guiado</h2>
      <div class="bars">${G.GENERATORS.map((g) => { const s = db.gen[g.id]; const pct = s ? Math.round((100 * s.f) / Math.max(1, s.s)) : 0; return `<div class="bar-row"><span>${esc(g.title.split(':')[0])}</span><div class="bar"><i class="${pct >= 75 ? '' : pct >= 50 ? 'mid' : 'low'}" style="width:${pct}%"></i></div><span class="muted">${s ? `${s.n} ej. · ${pct}%` : 'sin datos'}</span></div>`; }).join('')}</div>`;
  }
  view.addEventListener('click', (e) => {
    if (currentTab !== 'progreso') return;
    const t = e.target.closest('button');
    if (!t) return;
    if (t.id === 'p-rev') { quiz.phase = 'config'; location.hash = '#quiz'; startRun(errorPool().slice(0, 15), 'review'); }
    else if (t.id === 'p-reset' && window.confirm('Se borra todo tu progreso (aciertos, errores y ejercicios guiados). ¿Seguro?')) { saveDb(freshDb()); renderProgress(); }
  });

  /* ============================== boot ============================== */
  route();
})();
