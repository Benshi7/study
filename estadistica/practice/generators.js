/* Guided-exercise generators. Browser: window.Generators. Node: require('./generators.js').
   Each generator returns {gen, title, topic, stem, givens?, steps[], meta}. Steps:
   {prompt, type:"choice"|"number", options?, answer, tol, tolMode:"abs"|"rel", explain, hint?, calc?, viz?, unit?, prob?}
   (all user-facing strings are Spanish; identifiers/comments are English) */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./stats.js'));
  else root.Generators = factory(root.Stats);
})(typeof self !== 'undefined' ? self : this, function (S) {
  'use strict';

  /* ======================= random + formatting helpers ======================= */
  let rng = Math.random;
  function setRng(fn) { rng = fn || Math.random; }
  function mulberry32(seed) {
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const randInt = (a, b) => a + Math.floor(rng() * (b - a + 1));
  const pick = (arr) => arr[Math.floor(rng() * arr.length)];
  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(rng() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }
  const round = (x, d = 0) => { const f = 10 ** d; return Math.round((x + Number.EPSILON * Math.sign(x)) * f) / f; };
  const clamp = (x, lo, hi) => Math.min(hi, Math.max(lo, x));

  /** es-AR style: decimal comma, thousands dot from 10.000. d = fixed decimals. */
  function fmt(x, d = 2) {
    if (!Number.isFinite(x)) return String(x);
    let s = Math.abs(x).toFixed(d);
    let [int, dec] = s.split('.');
    if (int.length > 4) int = int.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    const neg = x < 0 && Number(s) !== 0;
    return (neg ? '−' : '') + int + (dec ? ',' + dec : '');
  }
  /** Up to `max` decimals, trailing zeros trimmed. */
  function fa(x, max = 4) {
    let s = round(x, max).toFixed(max);
    if (s.includes('.')) s = s.replace(/0+$/, '').replace(/\.$/, '');
    return fmt(Number(s), (s.split('.')[1] || '').length);
  }
  const pr = (p) => fmt(p, 4);                     // probability, 4 decimals
  const pc = (p, d = 1) => fa(p * 100, d) + '%';   // percentage text
  const Phi = S.normalCdf;

  function tbl(headers, rows, cls = 'given') {
    const th = headers.map((h) => `<th>${h}</th>`).join('');
    const tr = rows.map((r) => `<tr>${r.map((c) => `<td>${c}</td>`).join('')}</tr>`).join('');
    return `<table class="${cls}"><thead><tr>${th}</tr></thead><tbody>${tr}</tbody></table>`;
  }

  /* ======================= step builders ======================= */
  function numStep(prompt, answer, o = {}) {
    return Object.assign({ type: 'number', prompt, answer, tol: 0.001, tolMode: 'abs', explain: '' }, o);
  }
  /** correct: text; wrong: array of texts. Options are shuffled. */
  function choiceStep(prompt, correct, wrong, o = {}) {
    const uniqueWrong = [];
    for (const w of wrong) if (w !== correct && !uniqueWrong.includes(w)) uniqueWrong.push(w);
    const opts = shuffle([correct, ...uniqueWrong]);
    return Object.assign({ type: 'choice', prompt, options: opts, answer: opts.indexOf(correct), explain: '' }, o);
  }
  function checkNumber(step, v) {
    if (!Number.isFinite(v)) return false;
    const diff = Math.abs(v - step.answer);
    return step.tolMode === 'rel' ? diff <= step.tol * Math.abs(step.answer) : diff <= step.tol;
  }

  /* ======================= normal scenarios ======================= */
  const NORMAL_SC = [
    { subject: 'La duración de las baterías de cierto modelo de celular', unit: 'horas', mus: [18, 20, 24, 30], sigs: [2, 3, 4], dec: 1 },
    { subject: 'El peso de los paquetes de yerba que llena una máquina', unit: 'g', mus: [500, 1000], sigs: [4, 5, 8, 10], dec: 0 },
    { subject: 'La nota obtenida por los alumnos en un parcial de Estadística', unit: 'puntos', mus: [60, 65, 70, 72], sigs: [8, 10, 12, 15], dec: 0 },
    { subject: 'El tiempo que tarda un operador de call center en resolver una consulta', unit: 'segundos', mus: [180, 240, 300], sigs: [30, 40, 50], dec: 0 },
    { subject: 'El diámetro de los ejes que fabrica un torno', unit: 'mm', mus: [25, 30, 40], sigs: [0.4, 0.5, 0.8], dec: 2 },
    { subject: 'La altura de los alumnos de primer año de la facultad', unit: 'cm', mus: [165, 168, 172], sigs: [6, 7, 8], dec: 0 },
    { subject: 'El consumo mensual de energía de los hogares de un barrio', unit: 'kWh', mus: [250, 300, 350, 400], sigs: [40, 50, 60, 80], dec: 0 },
    { subject: 'El contenido de las botellas que llena una embotelladora', unit: 'ml', mus: [500, 750, 1000], sigs: [5, 8, 10, 15], dec: 0 },
  ];
  const withUnit = (x, sc, d) => `${fa(x, d === undefined ? sc.dec + 1 : d)} ${sc.unit}`;

  /** All z (2 decimals) for which mu + z*sigma is exactly representable with `dec` decimals. */
  function validZs(mu, sigma, dec, lo = 0.2, hi = 2.6) {
    const out = [];
    for (let k = Math.round(-hi * 100); k <= Math.round(hi * 100); k++) {
      const z = k / 100;
      if (Math.abs(z) < lo) continue;
      const x = mu + z * sigma;
      if (Math.abs(round(x, dec) - x) < 1e-9) out.push(z);
    }
    return out;
  }
  /** Draw mu, sigma and `count` distinct z values (sorted) such that every x is exact at `dec` decimals. */
  function drawNormal(sc, count = 1) {
    for (let tries = 0; tries < 300; tries++) {
      const mu = pick(sc.mus);
      const sigma = pick(sc.sigs);
      const zs = validZs(mu, sigma, sc.dec);
      if (zs.length < 8) continue;
      const chosen = [];
      let guard = 0;
      while (chosen.length < count && guard++ < 100) {
        const z = pick(zs);
        if (chosen.every((c) => Math.abs(c - z) >= 0.4)) chosen.push(z);
      }
      if (chosen.length < count) continue;
      chosen.sort((a, b) => a - b);
      return { mu, sigma, zs: chosen, xs: chosen.map((z) => round(mu + z * sigma, sc.dec)) };
    }
    const mu = sc.mus[0], sigma = sc.sigs[0];
    const zs = count === 2 ? [-1, 1] : [1];
    return { mu, sigma, zs, xs: zs.map((z) => round(mu + z * sigma, sc.dec)) };
  }

  /** Table of Phi(z) for the z values needed plus two distractors, like the exam gives. */
  function phiGiven(needed) {
    const need = [...new Set(needed.map((z) => round(Math.abs(z), 2)))];
    const pool = [];
    for (let k = 25; k <= 275; k += 5) if (!need.some((n) => Math.abs(n - k / 100) < 0.2)) pool.push(k / 100);
    const extra = shuffle(pool).slice(0, 2);
    const zs = [...need, ...extra].sort((a, b) => a - b);
    return {
      title: 'Valores dados: Φ(z) de la normal estándar',
      html: tbl(['z', 'Φ(z)'], zs.map((z) => [fmt(z, 2), fmt(Phi(z), 4)])),
      note: 'Para un z negativo usá la simetría: Φ(−z) = 1 − Φ(z). Algunos valores de la tabla no hacen falta.',
    };
  }

  const zTxt = (z) => fmt(z, 2);
  const zPar = (z) => (z < 0 ? `(${zTxt(z)})` : zTxt(z));

  /** Steps shared by several generators: standardize, choose the Phi expression, compute the probability. */
  function normalProbSteps(o) {
    const { mu, sd, type, a, b, tol = 0.0015, unitTxt = '', sdSymbol = 'σ', meanSymbol = 'μ', dec = 2, popName = 'X' } = o;
    const za = round((a - mu) / sd, 2);
    const zb = b === undefined ? undefined : round((b - mu) / sd, 2);
    const zStepTol = { tol: 0.011, tolMode: 'abs' };
    const steps = [];
    const stdHint = `z = (valor − ${meanSymbol}) / ${sdSymbol}. Restá la media y dividí por el desvío (el de ${popName}, no la varianza).`;
    const u = (x) => `${fa(x, 4)}${unitTxt ? ' ' + unitTxt : ''}`;
    if (type === 'between') {
      steps.push(numStep(`Estandarizá el límite inferior ${u(a)}: z₁ = (x − ${meanSymbol}) / ${sdSymbol}. (Dos decimales.)`, za, Object.assign({
        explain: `z₁ = (${fa(a, 4)} − ${fa(mu, 4)}) / ${fa(sd, 4)} = ${zTxt(za)}.`, hint: stdHint, dec: 2,
        calc: `Calculadora: (${fa(a, 4)} − ${fa(mu, 4)}) ÷ ${fa(sd, 4)} = ${zTxt(za)}`,
      }, zStepTol)));
      steps.push(numStep(`Estandarizá el límite superior ${u(b)}: z₂ = (x − ${meanSymbol}) / ${sdSymbol}.`, zb, Object.assign({
        explain: `z₂ = (${fa(b, 4)} − ${fa(mu, 4)}) / ${fa(sd, 4)} = ${zTxt(zb)}.`, hint: stdHint, dec: 2,
        calc: `Calculadora: (${fa(b, 4)} − ${fa(mu, 4)}) ÷ ${fa(sd, 4)} = ${zTxt(zb)}`,
      }, zStepTol)));
    } else {
      steps.push(numStep(`Estandarizá ${u(a)}: z = (x − ${meanSymbol}) / ${sdSymbol}. (Dos decimales.)`, za, Object.assign({
        explain: `z = (${fa(a, 4)} − ${fa(mu, 4)}) / ${fa(sd, 4)} = ${zTxt(za)}.`, hint: stdHint, dec: 2,
        calc: `Calculadora: (${fa(a, 4)} − ${fa(mu, 4)}) ÷ ${fa(sd, 4)} = ${zTxt(za)}`,
      }, zStepTol)));
    }

    let correct, wrong, event, prob, calc, viz;
    if (type === 'lt') {
      event = `P(${popName} < ${fa(a, 4)})`;
      correct = `Φ(${zTxt(za)})`;
      wrong = ['1 − Φ(' + zTxt(za) + ')', `Φ(${zTxt(za)}) − 0,5`, `2·Φ(${zTxt(za)}) − 1`];
      prob = Phi(za);
      calc = `MENU → 7 Distribución → Normal CD → Lower = −1E99, Upper = ${fa(a, 4)}, σ = ${fa(sd, 4)}, μ = ${fa(mu, 4)}`;
      viz = { mu, sd, lo: -Infinity, hi: a, marks: [{ x: a }] };
    } else if (type === 'gt') {
      event = `P(${popName} > ${fa(a, 4)})`;
      correct = `1 − Φ(${zTxt(za)})`;
      wrong = [`Φ(${zTxt(za)})`, `Φ(${zTxt(za)}) − 0,5`, `2·(1 − Φ(${zTxt(za)}))`];
      prob = 1 - Phi(za);
      calc = `MENU → 7 Distribución → Normal CD → Lower = ${fa(a, 4)}, Upper = 1E99, σ = ${fa(sd, 4)}, μ = ${fa(mu, 4)}`;
      viz = { mu, sd, lo: a, hi: Infinity, marks: [{ x: a }] };
    } else {
      event = `P(${fa(a, 4)} < ${popName} < ${fa(b, 4)})`;
      correct = `Φ(${zTxt(zb)}) − Φ(${zTxt(za)})`;
      wrong = [`Φ(${zTxt(za)}) − Φ(${zTxt(zb)})`, `1 − (Φ(${zTxt(zb)}) − Φ(${zTxt(za)}))`, `Φ(${zTxt(zb)}) + Φ(${zTxt(za)})`];
      prob = Phi(zb) - Phi(za);
      calc = `MENU → 7 Distribución → Normal CD → Lower = ${fa(a, 4)}, Upper = ${fa(b, 4)}, σ = ${fa(sd, 4)}, μ = ${fa(mu, 4)}`;
      viz = { mu, sd, lo: a, hi: b, marks: [{ x: a }, { x: b }] };
    }
    steps.push(choiceStep(`¿Cómo se expresa ${event} con la normal estándar?`, correct, wrong, {
      explain: type === 'lt' ? 'La tabla y la calculadora acumulan desde la izquierda: P(Z < z) = Φ(z) directamente.'
        : type === 'gt' ? 'La cola derecha es el complemento de lo acumulado: P(Z > z) = 1 − Φ(z).'
          : 'El área entre dos valores es la acumulada del mayor menos la acumulada del menor.',
      hint: 'Dibujá la campana y sombreá lo que pide el enunciado. La tabla siempre acumula desde la cola izquierda.',
    }));
    steps.push(numStep(`Calculá ${event}.`, prob, {
      tol, prob: true, dec: 4, viz,
      explain: `${event} = ${type === 'lt' ? `Φ(${zTxt(za)})` : type === 'gt' ? `1 − Φ(${zTxt(za)})` : `Φ(${zTxt(zb)}) − Φ(${zTxt(za)})`} = ${pr(prob)}.`,
      calc,
      hint: 'Con la tabla: buscá Φ(|z|) y usá Φ(−z) = 1 − Φ(z) si hace falta. Verificá que el resultado tenga sentido con el dibujo (¿más o menos que 0,5?).',
    }));
    return { steps, prob, za, zb };
  }

  /* ======================= (a)+(b) discrete helpers ======================= */
  /** Builds the event description, the CD expression, distractors and the calculator path. */
  function discreteEvent(type, k, k2, dist) {
    const F = dist.cdf, f = dist.pmf;
    const X = 'P(X';
    const out = {};
    switch (type) {
      case 'exact':
        out.text = `exactamente ${k}`; out.prob = f(k);
        out.correct = `${X} = ${k}) (función de probabilidad, PD)`;
        out.wrong = [`${X} ≤ ${k})`, `1 − ${X} ≤ ${k})`, `${X} ≤ ${k}) − ${X} ≤ ${k + 1})`];
        out.calc = `MENU → 7 Distribución → ${dist.pd} → x = ${k}, ${dist.params}`;
        out.event = `P(X = ${k})`;
        break;
      case 'atmost':
        out.text = `a lo sumo ${k}`; out.prob = F(k);
        out.correct = `${X} ≤ ${k}) = CD(${k})`;
        out.wrong = [`${X} ≤ ${k - 1})`, `1 − ${X} ≤ ${k})`, `${X} = ${k})`];
        out.calc = `MENU → 7 Distribución → ${dist.cd} → x = ${k}, ${dist.params}`;
        out.event = `P(X ≤ ${k})`;
        break;
      case 'less':
        out.text = `menos de ${k}`; out.prob = F(k - 1);
        out.correct = `${X} ≤ ${k - 1}) = CD(${k - 1})`;
        out.wrong = [`${X} ≤ ${k})`, `1 − ${X} ≤ ${k - 1})`, `${X} = ${k - 1})`];
        out.calc = `MENU → 7 Distribución → ${dist.cd} → x = ${k - 1}, ${dist.params}`;
        out.event = `P(X < ${k}) = P(X ≤ ${k - 1})`;
        break;
      case 'atleast':
        out.text = `al menos ${k}`; out.prob = 1 - F(k - 1);
        out.correct = `1 − ${X} ≤ ${k - 1}) = 1 − CD(${k - 1})`;
        out.wrong = [`1 − ${X} ≤ ${k})`, `${X} ≤ ${k})`, `${X} ≤ ${k - 1})`];
        out.calc = `MENU → 7 Distribución → ${dist.cd} → x = ${k - 1}, ${dist.params} → anotá el resultado y calculá 1 − CD(${k - 1})`;
        out.event = `P(X ≥ ${k}) = 1 − P(X ≤ ${k - 1})`;
        break;
      case 'more':
        out.text = `más de ${k}`; out.prob = 1 - F(k);
        out.correct = `1 − ${X} ≤ ${k}) = 1 − CD(${k})`;
        out.wrong = [`1 − ${X} ≤ ${k - 1})`, `${X} ≤ ${k})`, `${X} = ${k + 1})`];
        out.calc = `MENU → 7 Distribución → ${dist.cd} → x = ${k}, ${dist.params} → anotá el resultado y calculá 1 − CD(${k})`;
        out.event = `P(X > ${k}) = 1 − P(X ≤ ${k})`;
        break;
      default: // between (inclusive)
        out.text = `entre ${k} y ${k2} (inclusive)`; out.prob = F(k2) - F(k - 1);
        out.correct = `${X} ≤ ${k2}) − ${X} ≤ ${k - 1}) = CD(${k2}) − CD(${k - 1})`;
        out.wrong = [`${X} ≤ ${k2}) − ${X} ≤ ${k})`, `${X} ≤ ${k2}) + ${X} ≤ ${k - 1})`, `${X} ≤ ${k}) − ${X} ≤ ${k2})`];
        out.calc = `MENU → 7 Distribución → ${dist.cd} → x = ${k2}, ${dist.params} (anotá), luego x = ${k - 1} (anotá) y restá: CD(${k2}) − CD(${k - 1})`;
        out.event = `P(${k} ≤ X ≤ ${k2}) = P(X ≤ ${k2}) − P(X ≤ ${k - 1})`;
    }
    return out;
  }
  const DISCRETE_TYPES = ['exact', 'atleast', 'atmost', 'more', 'less', 'between'];
  function drawEvent(type, mean, max) {
    const base = Math.round(mean);
    let k = clamp(base + randInt(-2, 2), 1, max - 1);
    let k2;
    if (type === 'between') {
      k = clamp(base - randInt(0, 2), 1, max - 2);
      k2 = clamp(k + randInt(1, 3), k + 1, max);
    }
    return { k, k2 };
  }

  const distChoiceWrong = {
    bin: ['Poisson', 'Normal', 'Hipergeométrica'],
    poisson: ['Binomial', 'Normal', 'Hipergeométrica'],
  };

  /* ======================= (a) Binomial ======================= */
  const BIN_SC = [
    { intro: (p) => `Una fábrica de tornillos produce con un ${pc(p)} de piezas defectuosas.`, sample: (n) => `Se inspeccionan ${n} tornillos elegidos al azar (la producción es muy grande: las piezas se consideran independientes).`, what: 'sean defectuosos', p: [0.05, 0.08, 0.1, 0.12, 0.15, 0.2], trial: 'cada tornillo es defectuoso o no, con la misma probabilidad' },
    { intro: (p) => `En un call center, el ${pc(p)} de las llamadas salientes termina en una venta.`, sample: (n) => `Un operador realiza ${n} llamadas independientes entre sí.`, what: 'terminen en venta', p: [0.1, 0.15, 0.2, 0.25, 0.3], trial: 'cada llamada termina en venta o no, con la misma probabilidad' },
    { intro: (p) => `El ${pc(p)} de los alumnos de Estadística aprueba el final en primera instancia.`, sample: (n) => `Se elige al azar a ${n} alumnos, independientes entre sí.`, what: 'aprueben', p: [0.4, 0.5, 0.6, 0.7, 0.75], trial: 'cada alumno aprueba o no, con la misma probabilidad' },
    { intro: (p) => `Una aseguradora sabe que el ${pc(p)} de sus asegurados presenta un siniestro en el año.`, sample: (n) => `Se revisan ${n} asegurados elegidos al azar.`, what: 'hayan presentado un siniestro', p: [0.05, 0.1, 0.15, 0.2], trial: 'cada asegurado tiene o no un siniestro, con la misma probabilidad' },
    { intro: (p) => `Un lote de semillas germina con probabilidad ${fmt(p, 2)}.`, sample: (n) => `Se plantan ${n} semillas, cada una en una maceta distinta.`, what: 'germinen', p: [0.6, 0.7, 0.75, 0.8, 0.85, 0.9], trial: 'cada semilla germina o no, con la misma probabilidad' },
  ];

  function genBinomial() {
    const sc = pick(BIN_SC);
    const n = randInt(8, 20);
    const p = pick(sc.p);
    const type = pick(DISCRETE_TYPES);
    const { k, k2 } = drawEvent(type, n * p, n);
    const dist = {
      cdf: (x) => S.binomCdf(x, n, p), pmf: (x) => S.binomPmf(x, n, p),
      pd: 'Binomial PD (4)', cd: 'Binomial CD (▼ 1)', params: `N = ${n}, p = ${fa(p)}`,
    };
    const ev = discreteEvent(type, k, k2, dist);
    const steps = [];
    steps.push(choiceStep('¿Qué distribución modela la cantidad X de casos en la muestra?', 'Binomial', distChoiceWrong.bin, {
      explain: `Hay ${n} ensayos independientes, ${sc.trial}, y se cuenta cuántos éxitos hubo: X ~ Binomial(n, p).`,
      hint: 'Fijate si hay un número fijo de ensayos independientes, con dos resultados posibles y p constante.',
    }));
    steps.push(choiceStep('¿Cuáles son los parámetros?', `n = ${n}, p = ${fa(p)}`,
      [`n = ${n}, p = ${fa(1 - p)}`, `n = ${n - 1}, p = ${fa(p)}`, `n = ${fa(p)}, p = ${n}`], {
        explain: `n es la cantidad de ensayos (${n}) y p la probabilidad de "éxito", que es lo que se cuenta: ${fa(p)}.`,
        hint: 'p es la probabilidad del evento que se cuenta (el "éxito"), no la de su complemento.',
      }));
    steps.push(choiceStep(`Se pide la probabilidad de que ${ev.text} ${sc.what}. ¿Cómo se calcula con la función acumulada CD(x) = P(X ≤ x)?`, ev.correct, ev.wrong, {
      explain: `${ev.event}. La calculadora (y la tabla) acumulan hacia la izquierda: solo entrega P(X ≤ x).`,
      hint: 'Recordá que Binomial CD da P(X ≤ x). "Al menos k" es el complemento de "k − 1 o menos"; "menos de k" llega hasta k − 1.',
    }));
    steps.push(numStep(`Calculá la probabilidad de que ${ev.text} ${sc.what}.`, ev.prob, {
      tol: 0.0006, prob: true, dec: 4, calc: ev.calc,
      explain: `${ev.event} = ${pr(ev.prob)}.`,
      hint: 'Revisá los parámetros que cargaste (N y p) y si hace falta el complemento 1 − CD(...).',
    }));
    steps.push(numStep('¿Cuántos casos se esperan en promedio en la muestra? E(X) = n·p', n * p, {
      tol: 0.01, dec: 2, explain: `E(X) = n·p = ${n} · ${fa(p)} = ${fa(n * p)}.`, hint: 'Es el producto n · p.',
      calc: `Calculadora: ${n} × ${fa(p)} = ${fa(n * p)}`,
    }));
    return {
      title: 'Binomial: exactamente, al menos, a lo sumo, entre',
      stem: `${sc.intro(p)} ${sc.sample(n)} Sea X la cantidad de tornillos/casos que cumplen la condición. ¿Cuál es la probabilidad de que ${ev.text} ${sc.what}?`.replace('tornillos/casos que cumplen la condición', 'unidades que cumplen la condición'),
      steps, meta: { dist: 'bin', n, p, type, k, k2, answer: ev.prob },
    };
  }

  /* ======================= (b) Poisson ======================= */
  const POI_SC = [
    { place: 'un call center', ev: 'llamadas', verb: 'lleguen', per: 'hora', rate: [3, 12], targets: [['en 30 minutos', 0.5], ['en 15 minutos', 0.25], ['en 2 horas', 2], ['en 90 minutos', 1.5]] },
    { place: 'una fábrica de telas', ev: 'defectos', verb: 'se detecten', per: 'metro cuadrado', rate: [1, 4], targets: [['en 2 metros cuadrados', 2], ['en 3 metros cuadrados', 3], ['en medio metro cuadrado', 0.5]] },
    { place: 'una editorial', ev: 'errores de tipeo', verb: 'se encuentren', per: 'página', rate: [1, 3], targets: [['en 2 páginas', 2], ['en 4 páginas', 4], ['en 5 páginas', 5]] },
    { place: 'la caja de un supermercado', ev: 'clientes', verb: 'lleguen', per: 'hora', rate: [4, 14], targets: [['en 30 minutos', 0.5], ['en 15 minutos', 0.25], ['en 3 horas', 3]] },
    { place: 'una guardia hospitalaria', ev: 'ingresos', verb: 'se registren', per: 'hora', rate: [2, 8], targets: [['en 2 horas', 2], ['en 30 minutos', 0.5], ['en 45 minutos', 0.75]] },
  ];

  function genPoisson() {
    const sc = pick(POI_SC);
    const rate = randInt(sc.rate[0], sc.rate[1]);
    const [targetTxt, f] = pick(sc.targets);
    const lambda = round(rate * f, 4);
    const type = pick(DISCRETE_TYPES);
    const { k, k2 } = drawEvent(type, lambda, Math.max(12, Math.ceil(lambda * 2.5)));
    const dist = {
      cdf: (x) => S.poissonCdf(x, lambda), pmf: (x) => S.poissonPmf(x, lambda),
      pd: 'Poisson PD (▼ 2)', cd: 'Poisson CD (▼ 3)', params: `λ = ${fa(lambda)}`,
    };
    const ev = discreteEvent(type, k, k2, dist);
    const steps = [];
    steps.push(choiceStep('¿Qué distribución modela la cantidad de eventos en el intervalo?', 'Poisson', distChoiceWrong.poisson, {
      explain: `Se cuentan ocurrencias al azar en un intervalo de tiempo/espacio con una tasa media conocida, sin un "n" de ensayos: Poisson.`,
      hint: 'No hay una cantidad fija de ensayos; se cuentan eventos por unidad de tiempo o espacio.',
    }));
    steps.push(numStep(`La tasa es de ${rate} por ${sc.per}, pero se pregunta por un intervalo distinto. ¿Cuál es el λ para "${targetTxt}"?`, lambda, {
      tol: 0.005, dec: 2,
      explain: `λ se reescala proporcionalmente al intervalo: λ = ${rate} × ${fa(f)} = ${fa(lambda)}.`,
      hint: `Multiplicá la tasa por cuánto vale el nuevo intervalo medido en "${sc.per}" (por ejemplo, 30 minutos = 0,5 horas).`,
      calc: `Calculadora: ${rate} × ${fa(f)} = ${fa(lambda)}`,
    }));
    steps.push(choiceStep(`Se pide la probabilidad de que ${ev.text}. ¿Cómo se calcula con CD(x) = P(X ≤ x)?`, ev.correct, ev.wrong, {
      explain: `${ev.event}.`,
      hint: 'Poisson CD da P(X ≤ x). Pensá si el evento es hacia la izquierda, hacia la derecha o un punto.',
    }));
    steps.push(numStep(`Calculá la probabilidad de que ${sc.verb} ${ev.text} ${sc.ev} ${targetTxt}.`, ev.prob, {
      tol: 0.0006, prob: true, dec: 4, calc: ev.calc,
      explain: `${ev.event} = ${pr(ev.prob)} (con λ = ${fa(lambda)}).`,
      hint: 'Usá el λ del intervalo pedido (no el de la tasa original) y el complemento si corresponde.',
    }));
    return {
      title: 'Poisson: reescalar λ a otro intervalo',
      stem: `En ${sc.place} se registran, en promedio, ${rate} ${sc.ev} por ${sc.per}, al azar e independientemente. ¿Cuál es la probabilidad de que ${sc.verb} ${ev.text} ${sc.ev} ${targetTxt}?`,
      steps, meta: { dist: 'poisson', rate, f, lambda, type, k, k2, answer: ev.prob },
    };
  }

  /* ======================= (c) Normal probability ======================= */
  function genNormalProb() {
    const sc = pick(NORMAL_SC);
    const type = pick(['lt', 'gt', 'between']);
    const d = drawNormal(sc, type === 'between' ? 2 : 1);
    const a = d.xs[0];
    const b = d.xs[1];
    const ask = type === 'lt' ? `sea menor que ${withUnit(a, sc)}` : type === 'gt' ? `supere ${withUnit(a, sc)}` : `esté entre ${withUnit(a, sc)} y ${withUnit(b, sc)}`;
    const res = normalProbSteps({ mu: d.mu, sd: d.sigma, type, a, b, unitTxt: sc.unit, tol: 0.0012 });
    const needed = type === 'between' ? [res.za, res.zb] : [res.za];
    return {
      title: 'Normal: P(X < a), P(X > a), P(a < X < b)',
      stem: `${sc.subject} se distribuye normalmente con media μ = ${withUnit(d.mu, sc)} y desvío estándar σ = ${withUnit(d.sigma, sc)}. Si se elige un caso al azar, ¿cuál es la probabilidad de que el valor ${ask}?`,
      givens: phiGiven(needed), steps: res.steps,
      meta: { type, mu: d.mu, sigma: d.sigma, a, b, answer: res.prob },
    };
  }

  /* ======================= (d) Normal inverse ======================= */
  const Z_PCT = { 0.75: 0.67, 0.80: 0.84, 0.90: 1.28, 0.95: 1.645, 0.975: 1.96, 0.99: 2.33 };
  function zPercentTable() {
    const keys = Object.keys(Z_PCT).map(Number);
    return {
      title: 'Valores dados: percentiles de la normal estándar',
      html: tbl(['Área a la izquierda', 'z'], keys.map((k) => [fmt(k, 3).replace(/0$/, ''), fmt(Z_PCT[k], Z_PCT[k] === 1.645 ? 3 : 2)])),
      note: 'Para áreas menores que 0,5 usá la simetría: z(1 − q) = −z(q).',
    };
  }

  function genNormalInverse() {
    const sc = pick(NORMAL_SC);
    const d = drawNormal(sc, 1);
    const mu = d.mu, sigma = d.sigma;
    const high = pick([0.75, 0.8, 0.9, 0.95, 0.975, 0.99]);
    const variant = pick(['left_hi', 'right_top', 'left_lo', 'right_big']);
    let area, text;
    if (variant === 'left_hi') { area = high; text = `el ${pc(area)} de los casos tiene un valor menor que x`; }
    else if (variant === 'right_top') { area = high; text = `solo el ${pc(1 - area)} de los casos supera el valor x`; }
    else if (variant === 'left_lo') { area = round(1 - high, 3); text = `el ${pc(area)} de los casos queda por debajo de x`; }
    else { area = round(1 - high, 3); text = `el ${pc(1 - area)} de los casos supera el valor x`; }
    const z = S.invNorm(area);
    const x = mu + z * sigma;
    const steps = [];
    const wrongAreas = [round(1 - area, 3), round(area / 2, 4), round(0.5 - Math.abs(area - 0.5), 4)];
    steps.push(choiceStep('Inverse Normal trabaja con el área a la IZQUIERDA. ¿Qué área hay que ingresar?', fmt(area, 3).replace(/0$/, ''),
      wrongAreas.map((w) => fmt(w, 3).replace(/0$/, '')), {
        explain: variant === 'left_hi' || variant === 'left_lo' ? `El enunciado ya da el área acumulada a la izquierda: ${fa(area, 3)}.`
          : `Si ${fa(variant === 'right_top' ? 1 - area : 1 - area, 3)} queda a la derecha, a la izquierda quedan ${fa(area, 3)} (complemento).`,
        hint: 'Dibujá la campana: ¿el porcentaje del enunciado está a la izquierda o a la derecha de x? Si está a la derecha, usá el complemento.',
      }));
    steps.push(numStep('Encontrá el z que deja esa área a su izquierda.', z, {
      tol: 0.015, dec: 3, viz: { mu: 0, sd: 1, lo: -Infinity, hi: z, marks: [{ x: z }], z: true },
      explain: `z = invNorm(${fa(area, 3)}) = ${fmt(z, 3)}${area < 0.5 ? ' (negativo porque queda a la izquierda de la media)' : ''}.`,
      calc: `MENU → 7 Distribución → Inverse Normal → Area = ${fa(area, 3)}, σ = 1, μ = 0 → z = ${fmt(z, 3)}`,
      hint: area < 0.5 ? 'Si el área izquierda es menor que 0,5, el z es negativo.' : 'Mirá la tabla dada: el z es el valor que corresponde a esa área acumulada.',
    }));
    steps.push(numStep(`Destandarizá: x = μ + z·σ  (en ${sc.unit})`, x, {
      tol: 0.011 * sigma, dec: sc.dec + 1,
      explain: `x = ${fa(mu)} + (${fmt(z, 3)})·${fa(sigma)} = ${fa(x, 3)} ${sc.unit}.`,
      calc: `MENU → 7 Distribución → Inverse Normal → Area = ${fa(area, 3)}, σ = ${fa(sigma)}, μ = ${fa(mu)} → x = ${fa(x, 3)}`,
      hint: 'Es la estandarización al revés: x = μ + z·σ. Cuidado con el signo de z.',
      viz: { mu, sd: sigma, lo: -Infinity, hi: x, marks: [{ x }] },
    }));
    return {
      title: 'Normal inversa: hallar x para un percentil',
      stem: `${sc.subject} se distribuye normalmente con media μ = ${withUnit(mu, sc)} y desvío estándar σ = ${withUnit(sigma, sc)}. Se sabe que ${text}. ¿Cuánto vale x?`,
      givens: zPercentTable(), steps, meta: { mu, sigma, area, answer: x },
    };
  }

  /* ======================= (e) mu and sigma from two percentiles ======================= */
  const Z_TAB_E = { 0.70: 0.52, 0.75: 0.67, 0.80: 0.84, 0.85: 1.04, 0.90: 1.28, 0.95: 1.645, 0.975: 1.96 };
  function genMuSigma() {
    const sc = pick(NORMAL_SC.filter((s) => s.dec <= 1));
    const d = drawNormal(sc, 1);
    const mu0 = d.mu, sg0 = d.sigma;
    const p1 = pick([0.1, 0.15, 0.2, 0.25, 0.3]);
    const q = pick([0.1, 0.15, 0.2, 0.25]);
    const z1 = -Z_TAB_E[round(1 - p1, 2)];
    const z2 = Z_TAB_E[round(1 - q, 2)];
    const dec = Math.max(sc.dec, 1);
    const a = round(mu0 + z1 * sg0, dec);
    const b = round(mu0 + z2 * sg0, dec);
    const sigma = (b - a) / (z2 - z1);
    const mu = a - z1 * sigma;
    const keys = Object.keys(Z_TAB_E);
    const steps = [];
    steps.push(numStep(`El ${pc(p1)} queda por debajo de ${fa(a)}. ¿Cuál es el z que corresponde a ${fa(a)}? (Tabla: z con área ${fa(1 - p1, 2)} es ${fmt(Z_TAB_E[round(1 - p1, 2)], 2)}; ojo con el signo.)`, z1, {
      tol: 0.011, dec: 2, explain: `El área izquierda ${fa(p1, 2)} es menor que 0,5, así que z₁ es negativo: z₁ = −${fmt(Z_TAB_E[round(1 - p1, 2)], 2)}.`,
      hint: 'Por simetría, z(0,10) = −z(0,90).',
      calc: `MENU → 7 Distribución → Inverse Normal → Area = ${fa(p1, 2)}, σ = 1, μ = 0`,
    }));
    steps.push(numStep(`El ${pc(q)} supera ${fa(b)}, o sea que a la izquierda de ${fa(b)} queda el ${pc(1 - q)}. ¿Cuál es z₂?`, z2, {
      tol: 0.011, dec: 2, explain: `Área izquierda = 1 − ${fa(q, 2)} = ${fa(1 - q, 2)} → z₂ = ${fmt(z2, z2 === 1.645 ? 3 : 2)}.`,
      hint: 'Convertí "supera" en área a la izquierda con el complemento.',
      calc: `MENU → 7 Distribución → Inverse Normal → Area = ${fa(1 - q, 2)}, σ = 1, μ = 0`,
    }));
    steps.push(numStep('Planteá a = μ + z₁σ y b = μ + z₂σ y restalas. ¿Cuánto vale σ?', sigma, {
      tol: 0.03, tolMode: 'rel', dec: 3, unit: sc.unit,
      explain: `b − a = (z₂ − z₁)σ → σ = (${fa(b)} − ${fa(a)}) / (${fmt(z2, 3)} − (${fmt(z1, 3)})) = ${fa(sigma, 3)}.`,
      hint: 'Al restar las dos ecuaciones desaparece μ: b − a = (z₂ − z₁)·σ.',
      calc: `Calculadora: (${fa(b)} − ${fa(a)}) ÷ (${fmt(z2, 3)} − (${fmt(z1, 3)})) = ${fa(sigma, 3)}`,
    }));
    steps.push(numStep('Con σ, despejá μ de a = μ + z₁σ.', mu, {
      tol: 0.03, tolMode: 'rel', dec: 3, unit: sc.unit,
      explain: `μ = a − z₁σ = ${fa(a)} − (${fmt(z1, 3)})(${fa(sigma, 3)}) = ${fa(mu, 3)}.`,
      hint: 'μ = a − z₁·σ (z₁ es negativo, así que se suma).',
      calc: `Calculadora: ${fa(a)} − (${fmt(z1, 3)}) × ${fa(sigma, 3)} = ${fa(mu, 3)}`,
    }));
    return {
      title: 'Normal: hallar μ y σ con dos percentiles',
      stem: `${sc.subject} se distribuye normalmente. Se sabe que el ${pc(p1)} de los casos tiene un valor menor que ${fa(a)} ${sc.unit} y que el ${pc(q)} supera los ${fa(b)} ${sc.unit}. Hallá la media y el desvío estándar.`,
      givens: {
        title: 'Valores dados: percentiles de la normal estándar',
        html: tbl(['Área a la izquierda', 'z'], keys.map((k) => [fmt(Number(k), 2), fmt(Z_TAB_E[k], Z_TAB_E[k] === 1.645 ? 3 : 2)])),
        note: 'Para áreas menores que 0,5 usá la simetría.',
      },
      steps, meta: { a, b, z1, z2, sigma, mu, p1, q },
    };
  }

  /* ======================= (f) sampling distribution of the mean / sum ======================= */
  function genSamplingMean() {
    const sc = pick(NORMAL_SC.filter((s) => s.dec <= 1));
    const variant = pick(['mean', 'mean', 'sum']);
    const mu = pick(sc.mus);
    const root = pick([4, 5, 6, 7, 8, 10]);
    const n = root * root;
    // sigma = se * root with a "nice" se so that every threshold is exact
    const se = pick([0.5, 1, 1.5, 2, 2.5, 4, 5]);
    const sigma = se * root;
    const type = pick(['gt', 'lt', 'between']);
    const dec = 2;
    let mu2, sd2;
    if (variant === 'mean') { mu2 = mu; sd2 = se; } else { mu2 = n * mu; sd2 = root * sigma; }
    const zs = [];
    const validK = [];
    for (let k = -230; k <= 230; k++) {
      const z = k / 100;
      if (Math.abs(z) < 0.2) continue;
      const x = mu2 + z * sd2;
      if (Math.abs(round(x, dec) - x) < 1e-9) validK.push(z);
    }
    while (zs.length < (type === 'between' ? 2 : 1)) {
      const z = pick(validK);
      if (zs.every((c) => Math.abs(c - z) >= 0.4)) zs.push(z);
    }
    zs.sort((x, y) => x - y);
    const xs = zs.map((z) => round(mu2 + z * sd2, dec));
    const label = variant === 'mean' ? 'x̄' : 'S';
    const word = variant === 'mean' ? 'la media muestral' : 'la suma de los valores de la muestra';
    const ask = type === 'gt' ? `supere ${fa(xs[0])}` : type === 'lt' ? `sea menor que ${fa(xs[0])}` : `esté entre ${fa(xs[0])} y ${fa(xs[1])}`;
    const steps = [];
    const sdWrongs = variant === 'mean'
      ? [sigma, se / root, sigma * root]
      : [sigma, sigma / root, n * sigma];
    steps.push(choiceStep(`¿Cuál es la distribución de ${label}?`,
      `Normal(μ = ${fa(mu2)}; desvío = ${fa(sd2, 3)})`,
      sdWrongs.map((w) => `Normal(μ = ${fa(mu2)}; desvío = ${fa(w, 3)})`).concat([`Normal(μ = ${fa(mu)}; desvío = ${fa(sigma, 3)}) (la misma que la población)`]), {
        explain: variant === 'mean'
          ? `Por el TCL (n = ${n} ≥ 30) x̄ es aproximadamente normal con media μ y desvío σ/√n = ${fa(sigma)}/${root} = ${fa(se, 3)}.`
          : `La suma de n = ${n} valores tiene media n·μ = ${fa(mu2)} y desvío √n·σ = ${root}·${fa(sigma)} = ${fa(sd2, 3)}.`,
        hint: variant === 'mean' ? 'El promedio de muestras varía menos que un dato individual: el desvío se divide por √n.' : 'En la suma, la media se multiplica por n y el desvío por √n (no por n).',
      }));
    steps.push(numStep(variant === 'mean' ? 'Calculá el error estándar σ/√n.' : 'Calculá el desvío de la suma, √n·σ.', sd2, {
      tol: 0.005 * sd2, dec: 3, unit: sc.unit,
      explain: variant === 'mean' ? `σ/√n = ${fa(sigma)}/√${n} = ${fa(se, 3)}.` : `√n·σ = √${n} · ${fa(sigma)} = ${fa(sd2, 3)}.`,
      hint: variant === 'mean' ? 'σ dividido por la raíz de n.' : 'σ multiplicado por la raíz de n.',
      calc: variant === 'mean' ? `Calculadora: ${fa(sigma)} ÷ √${n} = ${fa(se, 3)}` : `Calculadora: √${n} × ${fa(sigma)} = ${fa(sd2, 3)}`,
    }));
    const res = normalProbSteps({ mu: mu2, sd: sd2, type, a: xs[0], b: xs[1], unitTxt: '', tol: 0.0012, sdSymbol: variant === 'mean' ? '(σ/√n)' : '(√n·σ)', meanSymbol: variant === 'mean' ? 'μ' : 'n·μ', popName: label });
    steps.push(...res.steps);
    const needed = type === 'between' ? [res.za, res.zb] : [res.za];
    return {
      title: variant === 'mean' ? 'Distribución muestral de la media (σ/√n)' : 'Distribución de la suma de n valores (√n·σ)',
      stem: `${sc.subject} tiene media μ = ${withUnit(mu, sc, 1)} y desvío σ = ${withUnit(sigma, sc, 2)} (distribución cualquiera, ${variant === 'mean' ? 'se toma' : 'se toman'} una muestra aleatoria de n = ${n}). ¿Cuál es la probabilidad de que ${word} ${ask}?`,
      givens: phiGiven(needed), steps, meta: { variant, type, mu, sigma, n, mu2, sd2, xs, answer: res.prob },
    };
  }

  /* ======================= (g) sampling distribution of the proportion ======================= */
  const PROP_SC = [
    { who: 'los clientes de una tienda online', what: 'compran con tarjeta de crédito' },
    { who: 'los votantes de un distrito', what: 'apoyan a cierto candidato' },
    { who: 'las piezas que produce una máquina', what: 'son defectuosas' },
    { who: 'los usuarios de una app', what: 'renuevan la suscripción' },
  ];
  function genSamplingProp() {
    const sc = pick(PROP_SC);
    const p = pick([0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7]);
    const n = pick([100, 150, 200, 250, 400]);
    const se = Math.sqrt(p * (1 - p) / n);
    const type = pick(['gt', 'lt', 'between']);
    const z0 = pick([-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2]);
    const a = round(p + z0 * se, 3);
    const b = type === 'between' ? round(a + pick([0.04, 0.05, 0.06, 0.08]), 3) : undefined;
    const ask = type === 'gt' ? `supere ${fa(a, 3)}` : type === 'lt' ? `sea menor que ${fa(a, 3)}` : `esté entre ${fa(a, 3)} y ${fa(b, 3)}`;
    const steps = [];
    steps.push(choiceStep('¿Cuál es la distribución aproximada de la proporción muestral p̂?',
      `Normal(p; √(p(1−p)/n)) = Normal(${fa(p)}; ${fa(se, 4)})`,
      [`Normal(${fa(p)}; ${fa(Math.sqrt(p * (1 - p)), 4)})`, `Normal(${fa(p)}; ${fa(p * (1 - p) / n, 5)})`, `Normal(${fa(p)}; ${fa(Math.sqrt(p / n), 4)})`], {
        explain: `n·p = ${fa(n * p)} y n(1 − p) = ${fa(n * (1 - p))} son ≥ 5 (cumple la condición), así que p̂ ≈ Normal con media p y desvío √(p(1−p)/n).`,
        hint: 'El desvío de p̂ es la raíz de p(1 − p) dividido n (no la varianza, no sin dividir por n).',
      }));
    steps.push(numStep('Calculá el error estándar de p̂: √(p(1 − p)/n).', se, {
      tol: 0.0008, dec: 4,
      explain: `√(${fa(p)}·${fa(1 - p)}/${n}) = ${fa(se, 4)}.`,
      calc: `Calculadora: √(${fa(p)} × ${fa(1 - p)} ÷ ${n}) = ${fa(se, 4)}`,
      hint: 'Reemplazá p y n en √(p(1 − p)/n); no olvides la raíz.',
    }));
    const res = normalProbSteps({ mu: p, sd: se, type, a, b, tol: 0.003, sdSymbol: 'EE', meanSymbol: 'p', popName: 'p̂' });
    steps.push(...res.steps);
    const needed = type === 'between' ? [res.za, res.zb] : [res.za];
    return {
      title: 'Distribución muestral de la proporción',
      stem: `Se sabe que el ${pc(p)} de ${sc.who} ${sc.what}. Se toma una muestra aleatoria de n = ${n}. ¿Cuál es la probabilidad de que la proporción muestral p̂ ${ask}?`,
      givens: phiGiven(needed), steps, meta: { p, n, se, type, a, b, answer: res.prob },
    };
  }

  /* ======================= (h) confidence interval for the mean ======================= */
  const IC_SC = [
    { what: 'el tiempo de espera (en minutos) de los clientes de un banco', unit: 'minutos', mus: [12, 15, 20, 25], sig: [3, 4, 5, 6] },
    { what: 'el peso (en kg) de los paquetes que despacha una empresa de logística', unit: 'kg', mus: [18, 22, 30, 40], sig: [2, 3, 4, 5] },
    { what: 'las horas semanales de estudio de los alumnos de Estadística', unit: 'horas', mus: [8, 10, 12, 14], sig: [2, 3, 4] },
    { what: 'el gasto mensual (en miles de pesos) de los clientes de una app de delivery', unit: 'miles de $', mus: [30, 40, 50, 60], sig: [8, 10, 12, 15] },
  ];
  const CONF = [0.90, 0.95, 0.99];
  function icTable(conf, df, useT) {
    const rows = [];
    const c1 = conf, key = (c) => `${fa(c * 100, 0)}%`;
    rows.push(['z', key(c1), '—', fmt(S.zCrit(c1), 3)]);
    for (const c of CONF) if (c !== c1) rows.push(['z', key(c), '—', fmt(S.zCrit(c), 3)]);
    if (useT) {
      const dfs = [df - 1, df, df + 1].filter((d) => d >= 1);
      for (const d of dfs) rows.push(['t', key(c1), d, fmt(S.tCrit(c1, d), 3)]);
      const other = CONF.find((c) => c !== c1);
      rows.push(['t', key(other), df, fmt(S.tCrit(other, df), 3)]);
    }
    return { title: 'Valores críticos dados (bilaterales)', html: tbl(['Distribución', 'Confianza', 'gl', 'Valor crítico'], rows), note: 'Hay valores que no corresponden a este problema.' };
  }

  function genIcMean() {
    const sc = pick(IC_SC);
    const useT = rng() < 0.5;
    const conf = pick(CONF);
    const mu = pick(sc.mus);
    const xbar = round(mu + randInt(-10, 10) / 10, 1);
    const sigma = pick(sc.sig);
    const n = useT ? randInt(8, 20) : pick([36, 49, 64, 81, 100, 144]);
    const df = n - 1;
    const crit = useT ? S.tCrit(conf, df) : S.zCrit(conf);
    const se = sigma / Math.sqrt(n);
    const E = crit * se;
    const lo = xbar - E, hi = xbar + E;
    const critTxt = (type, v, extra) => `${type} = ${fmt(v, 3)}${extra ? ` (${extra})` : ''}`;
    const other = CONF.find((c) => c !== conf);
    const steps = [];
    steps.push(choiceStep('¿Qué distribución/valor crítico corresponde usar?',
      useT ? `t de Student con n − 1 gl` : 'Z (normal estándar)',
      useT ? ['Z (normal estándar)', 't de Student con n gl', 'Chi-cuadrado'] : ['t de Student con n − 1 gl', 'Chi-cuadrado', 'Binomial'], {
        explain: useT ? `σ es desconocida (se estima con s) y n = ${n} es chica: se usa t con gl = n − 1.`
          : `σ es conocida (σ = ${fa(sigma)}): se usa Z.`,
        hint: 'σ conocida → Z. σ desconocida (se usa s) con n chica → t con n − 1 grados de libertad.',
      }));
    if (useT) {
      steps.push(numStep('¿Cuántos grados de libertad hay?', df, {
        tol: 0, dec: 0, explain: `gl = n − 1 = ${n} − 1 = ${df}.`, hint: 'Es n − 1.',
      }));
    }
    const correctCrit = critTxt(useT ? 't' : 'z', crit, useT ? `gl = ${df}, ${fa(conf * 100, 0)}%` : `${fa(conf * 100, 0)}%`);
    const wrongCrit = useT
      ? [critTxt('t', S.tCrit(conf, Math.min(df + 1, 30)), `gl = ${df + 1}, ${fa(conf * 100, 0)}%`), critTxt('z', S.zCrit(conf), `${fa(conf * 100, 0)}%`), critTxt('t', S.tCrit(other, df), `gl = ${df}, ${fa(other * 100, 0)}%`)]
      : [critTxt('z', S.zCrit(other), `${fa(other * 100, 0)}%`), critTxt('z', S.zCrit(conf) / 2, `mitad del valor`), critTxt('z', S.zCrit(conf) + 0.5, 'otro valor')];
    steps.push(choiceStep(`¿Qué valor crítico se usa para ${fa(conf * 100, 0)}% de confianza?`, correctCrit, wrongCrit, {
      explain: `Para ${fa(conf * 100, 0)}% (bilateral, α/2 en cada cola) el valor es ${fmt(crit, 3)}.`,
      hint: useT ? 'Buscá la columna del nivel de confianza pedido y la fila con gl = n − 1.' : 'Cada nivel de confianza tiene su z: 90% → 1,645; 95% → 1,960; 99% → 2,576.',
    }));
    const dev = useT ? 's' : 'σ';
    steps.push(numStep(`Calculá el error (margen) E = ${useT ? 't' : 'z'} · ${dev}/√n.`, E, {
      tol: 0.012, tolMode: 'rel', dec: 3, unit: sc.unit,
      explain: `E = ${fmt(crit, 3)} · ${fa(sigma)}/√${n} = ${fmt(crit, 3)} · ${fa(se, 4)} = ${fa(E, 3)}.`,
      hint: `No olvides dividir ${dev} por √n antes de multiplicar por el valor crítico.`,
      calc: `Calculadora: ${fmt(crit, 3)} × ${fa(sigma)} ÷ √${n} = ${fa(E, 3)}`,
    }));
    steps.push(numStep('Límite inferior del intervalo: x̄ − E.', lo, {
      tol: 0.03 * E, dec: 3, unit: sc.unit, explain: `${fa(xbar)} − ${fa(E, 3)} = ${fa(lo, 3)}.`, hint: 'Restá E a la media muestral.',
      calc: `Calculadora: ${fa(xbar)} − ${fa(E, 3)} = ${fa(lo, 3)}`,
    }));
    steps.push(numStep('Límite superior del intervalo: x̄ + E.', hi, {
      tol: 0.03 * E, dec: 3, unit: sc.unit, explain: `${fa(xbar)} + ${fa(E, 3)} = ${fa(hi, 3)}.`, hint: 'Sumá E a la media muestral.',
      calc: `Calculadora: ${fa(xbar)} + ${fa(E, 3)} = ${fa(hi, 3)}`,
    }));
    steps.push(numStep('¿Cuál es la amplitud (ancho) total del intervalo?', 2 * E, {
      tol: 0.012, tolMode: 'rel', dec: 3, unit: sc.unit,
      explain: `Amplitud = límite superior − límite inferior = 2E = ${fa(2 * E, 3)}. (E es solo la mitad.)`, hint: 'El error E es la distancia al centro; el ancho completo es el doble.',
    }));
    const lvl = fa(conf * 100, 0);
    steps.push(choiceStep('¿Cuál es la interpretación correcta?',
      `Tenemos ${lvl}% de confianza de que la verdadera media poblacional está entre ${fa(lo, 2)} y ${fa(hi, 2)} ${sc.unit}.`,
      [`Hay ${lvl}% de probabilidad de que la media muestral x̄ esté entre ${fa(lo, 2)} y ${fa(hi, 2)}.`,
        `El ${lvl}% de las observaciones individuales está entre ${fa(lo, 2)} y ${fa(hi, 2)} ${sc.unit}.`,
        `La media poblacional vale exactamente ${fa(xbar, 2)} con ${lvl}% de seguridad.`], {
        explain: `El ${lvl}% describe el método: si repitiéramos el muestreo muchas veces, aproximadamente ${lvl}% de los intervalos construidos así contendrían a μ. No se refiere a datos individuales ni a x̄ (que ya es conocida).`,
        hint: 'El intervalo es sobre el parámetro μ (fijo), no sobre x̄ ni sobre los datos individuales.',
      }));
    const dataTxt = useT
      ? `una muestra aleatoria de n = ${n} observaciones (población normal) dio x̄ = ${fa(xbar)} y s = ${fa(sigma)}`
      : `una muestra aleatoria de n = ${n} observaciones dio x̄ = ${fa(xbar)}, y se sabe que σ = ${fa(sigma)}`;
    return {
      title: useT ? 'IC para la media con σ desconocida (t)' : 'IC para la media con σ conocida (Z)',
      stem: `Se estudia ${sc.what}: ${dataTxt} ${sc.unit}. Construí un intervalo de confianza del ${lvl}% para la media poblacional.`,
      givens: icTable(conf, df, useT), steps, meta: { useT, conf, n, xbar, sigma, crit, E, lo, hi },
    };
  }

  /* ======================= (i) confidence interval for a proportion ======================= */
  function genIcProp() {
    const sc = pick(PROP_SC);
    const conf = pick(CONF);
    const n = pick([100, 120, 150, 200, 250, 400, 500]);
    const x = Math.round(n * pick([0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.55, 0.6, 0.65]));
    const ph = x / n;
    const z = S.zCrit(conf);
    const se = Math.sqrt(ph * (1 - ph) / n);
    const E = z * se;
    const lo = ph - E, hi = ph + E;
    const lvl = fa(conf * 100, 0);
    const steps = [];
    steps.push(choiceStep('¿Qué intervalo corresponde?', 'p̂ ± z · √(p̂(1 − p̂)/n)',
      ['x̄ ± z · σ/√n', 'p̂ ± t · √(p̂(1 − p̂)/n)', 'p̂ ± z · p̂(1 − p̂)/n'], {
        explain: `Es una proporción con n grande (n·p̂ = ${x} y n(1 − p̂) = ${n - x} ≥ 5): IC con Z y error estándar √(p̂(1 − p̂)/n).`,
        hint: 'Para proporciones el estimador es p̂ y su error estándar lleva la raíz de p̂(1 − p̂)/n; con n grande va Z.',
      }));
    steps.push(numStep('Calculá la proporción muestral p̂ = x/n.', ph, {
      tol: 0.0006, dec: 4, explain: `p̂ = ${x}/${n} = ${fa(ph, 4)}.`, hint: 'Casos sobre tamaño de la muestra.', prob: true,
      calc: `Calculadora: ${x} ÷ ${n} = ${fa(ph, 4)}`,
    }));
    steps.push(numStep('Calculá el error estándar √(p̂(1 − p̂)/n).', se, {
      tol: 0.008, tolMode: 'rel', dec: 4, explain: `√(${fa(ph, 4)}·${fa(1 - ph, 4)}/${n}) = ${fa(se, 4)}.`, hint: 'No olvides la raíz cuadrada ni dividir por n.',
      calc: `Calculadora: √(${fa(ph, 4)} × ${fa(1 - ph, 4)} ÷ ${n}) = ${fa(se, 4)}`,
    }));
    steps.push(numStep(`Calculá el margen de error E = z · EE con z = ${fmt(z, 3)} (${lvl}%).`, E, {
      tol: 0.012, tolMode: 'rel', dec: 4, explain: `E = ${fmt(z, 3)} · ${fa(se, 4)} = ${fa(E, 4)}.`, hint: 'Multiplicá el valor crítico por el error estándar.',
      calc: `Calculadora: ${fmt(z, 3)} × ${fa(se, 4)} = ${fa(E, 4)}`,
    }));
    steps.push(numStep('Límite inferior p̂ − E.', lo, {
      tol: 0.03 * E, dec: 4, prob: true, explain: `${fa(ph, 4)} − ${fa(E, 4)} = ${fa(lo, 4)}.`, hint: 'Restá E a p̂.',
    }));
    steps.push(numStep('Límite superior p̂ + E.', hi, {
      tol: 0.03 * E, dec: 4, prob: true, explain: `${fa(ph, 4)} + ${fa(E, 4)} = ${fa(hi, 4)}.`, hint: 'Sumá E a p̂.',
    }));
    steps.push(choiceStep('¿Cuál es la interpretación correcta?',
      `Con ${lvl}% de confianza, la proporción poblacional está entre ${pc(lo, 1)} y ${pc(hi, 1)}.`,
      [`El ${lvl}% de ${sc.who} está entre ${pc(lo, 1)} y ${pc(hi, 1)}.`,
        `Hay ${lvl}% de probabilidad de que p̂ esté entre ${pc(lo, 1)} y ${pc(hi, 1)}.`,
        `La proporción poblacional es ${pc(ph, 1)} con ${lvl}% de seguridad.`], {
        explain: 'El nivel de confianza describe la fiabilidad del método sobre el parámetro p, no un porcentaje de individuos ni la probabilidad de p̂.',
        hint: 'El intervalo se refiere a la proporción poblacional (parámetro fijo).',
      }));
    return {
      title: 'IC para una proporción',
      stem: `En una muestra aleatoria de n = ${n} de ${sc.who}, ${x} ${sc.what}. Construí un intervalo de confianza del ${lvl}% para la proporción poblacional.`,
      givens: {
        title: 'Valores críticos dados (Z)',
        html: tbl(['Confianza', 'z'], CONF.map((c) => [`${fa(c * 100, 0)}%`, fmt(S.zCrit(c), 3)])),
        note: 'Elegí el que corresponde a este problema.',
      },
      steps, meta: { n, x, conf, ph, z, se, E, lo, hi },
    };
  }

  /* ======================= (j) sample size ======================= */
  function genSampleSize() {
    const variant = pick(['mean', 'prop', 'prop']);
    const conf = pick(CONF);
    const z = S.zCrit(conf);
    const lvl = fa(conf * 100, 0);
    const givens = {
      title: 'Valores críticos dados (Z)',
      html: tbl(['Confianza', 'z'], CONF.map((c) => [`${fa(c * 100, 0)}%`, fmt(S.zCrit(c), 3)])),
      note: 'Elegí el que corresponde.',
    };
    for (let tries = 0; tries < 200; tries++) {
      if (variant === 'mean') {
        const sc = pick(IC_SC);
        const sigma = pick(sc.sig) * pick([1, 1, 2]);
        const E = pick([0.25, 0.5, 1, 1.5, 2]);
        const raw = (z * sigma / E) ** 2;
        const rawExact = (S.invNorm(1 - (1 - conf) / 2) * sigma / E) ** 2;
        if (Math.ceil(raw) !== Math.ceil(rawExact) || raw > 3000 || raw < 15) continue;
        const nFinal = Math.ceil(raw);
        const steps = [];
        steps.push(choiceStep('¿Qué fórmula corresponde para estimar una media con σ conocida?', 'n = (z·σ/E)²',
          ['n = z·σ/E', 'n = z²·p(1 − p)/E²', 'n = (z·σ/E)² / 2'], {
            explain: 'Se despeja n de E = z·σ/√n.', hint: 'De E = z·σ/√n, despejá √n y elevá al cuadrado.',
          }));
        steps.push(numStep('Calculá n con la fórmula (sin redondear todavía).', raw, {
          tol: 0.01, tolMode: 'rel', dec: 2, explain: `n = (${fmt(z, 3)}·${fa(sigma)}/${fa(E)})² = ${fa(raw, 2)}.`,
          hint: 'Primero z·σ/E y después elevá al cuadrado.', calc: `Calculadora: (${fmt(z, 3)} × ${fa(sigma)} ÷ ${fa(E)})² = ${fa(raw, 2)}`,
        }));
        steps.push(numStep('¿Cuál es el tamaño de muestra mínimo? (entero)', nFinal, {
          tol: 0, dec: 0, explain: `Siempre se redondea hacia ARRIBA: n = ${nFinal}. Si redondearas hacia abajo, el error quedaría mayor que ${fa(E)}.`,
          hint: 'El tamaño de muestra se redondea siempre hacia arriba (aunque el decimal sea chico).',
        }));
        return {
          title: 'Tamaño de muestra para estimar una media',
          stem: `Se quiere estimar ${sc.what} con una confianza del ${lvl}% y un error máximo de ${fa(E)} ${sc.unit}. Por estudios previos se sabe que σ = ${fa(sigma)} ${sc.unit}. ¿Cuántas observaciones hacen falta como mínimo?`,
          givens, steps, meta: { variant, z, sigma, E, raw, nFinal },
        };
      }
      const sc = pick(PROP_SC);
      const known = rng() < 0.5;
      const pPrior = known ? pick([0.2, 0.3, 0.4, 0.6, 0.7, 0.8]) : 0.5;
      const E = pick([0.02, 0.03, 0.04, 0.05]);
      const raw = z * z * pPrior * (1 - pPrior) / (E * E);
      const zx = S.invNorm(1 - (1 - conf) / 2);
      const rawExact = zx * zx * pPrior * (1 - pPrior) / (E * E);
      if (Math.ceil(raw) !== Math.ceil(rawExact) || raw > 4000) continue;
      const nFinal = Math.ceil(raw);
      const steps = [];
      steps.push(choiceStep('¿Qué fórmula corresponde para estimar una proporción?', 'n = z²·p(1 − p)/E²',
        ['n = (z·σ/E)²', 'n = z·p(1 − p)/E', 'n = z²·p(1 − p)/E'], {
          explain: 'Se despeja n de E = z·√(p(1 − p)/n).', hint: 'De E = z·√(p(1 − p)/n), elevá al cuadrado y despejá n.',
        }));
      steps.push(choiceStep('¿Qué valor de p se usa?', known ? `p = ${fa(pPrior)} (dato previo)` : 'p = 0,5 (caso más desfavorable)',
        known ? ['p = 0,5 (caso más desfavorable)', `p = ${fa(1 - pPrior)}`, `p = ${fa(E)}`] : [`p = ${fa(E)}`, 'p = 0 (no hay información)', 'p = 1'], {
          explain: known ? `Se conoce una estimación previa, p = ${fa(pPrior)}; p(1 − p) = ${fa(pPrior * (1 - pPrior), 4)}.`
            : 'Si no hay información previa se usa p = 0,5, que maximiza p(1 − p) y garantiza el error pedido en cualquier caso.',
          hint: known ? 'Si el enunciado da una proporción previa, usala.' : 'Sin información, se toma el peor caso: el de mayor variabilidad.',
        }));
      steps.push(numStep('Calculá n con la fórmula (sin redondear todavía).', raw, {
        tol: 0.01, tolMode: 'rel', dec: 2, explain: `n = ${fmt(z, 3)}²·${fa(pPrior)}·${fa(1 - pPrior)}/${fa(E)}² = ${fa(raw, 2)}.`,
        hint: 'z se eleva al cuadrado, y E también (en el denominador).',
        calc: `Calculadora: ${fmt(z, 3)}² × ${fa(pPrior)} × ${fa(1 - pPrior)} ÷ ${fa(E)}² = ${fa(raw, 2)}`,
      }));
      steps.push(numStep('¿Cuál es el tamaño de muestra mínimo? (entero)', nFinal, {
        tol: 0, dec: 0, explain: `Se redondea hacia ARRIBA: n = ${nFinal}.`, hint: 'El tamaño de muestra se redondea siempre hacia arriba.',
      }));
      return {
        title: 'Tamaño de muestra para estimar una proporción',
        stem: `Se quiere estimar la proporción de ${sc.who} que ${sc.what}, con ${lvl}% de confianza y un error máximo de ${fa(E * 100, 1)} puntos porcentuales. ${known ? `Una encuesta previa estimó esa proporción en ${pc(pPrior, 0)}.` : 'No se dispone de ninguna información previa sobre la proporción.'} ¿Cuántas observaciones hacen falta como mínimo?`,
        givens, steps, meta: { variant, z, p: pPrior, E, raw, nFinal },
      };
    }
    throw new Error('sample size generator did not converge');
  }

  /* ======================= (k) grouped frequency table ======================= */
  const GROUP_SC = [
    { what: 'la edad (en años) de los socios de un club', unit: 'años', center: [30, 40, 50], widths: [4, 5, 10] },
    { what: 'el tiempo de espera (en minutos) en una guardia', unit: 'minutos', center: [20, 30, 45], widths: [5, 10] },
    { what: 'el peso (en kg) de los paquetes de una empresa de envíos', unit: 'kg', center: [20, 30, 40], widths: [2, 5] },
    { what: 'el gasto mensual (en miles de pesos) de los clientes de un comercio', unit: 'miles de $', center: [50, 80, 100], widths: [10, 20] },
  ];
  function cvClass(cv) { return cv <= 10 ? 'rep' : cv <= 20 ? 'hom' : 'het'; }

  function genGrouped() {
    const sc = pick(GROUP_SC);
    for (let tries = 0; tries < 400; tries++) {
      const wantBand = pick(['rep', 'hom', 'het']);
      const w = pick(sc.widths);
      const k = pick([5, 6]);
      const center = pick(sc.center);
      const L0 = center - Math.floor(k / 2) * w - w / 2;
      if (L0 <= 0) continue;
      const total = pick([60, 80, 100, 120, 150]);
      const targetCv = wantBand === 'rep' ? 0.07 : wantBand === 'hom' ? 0.15 : 0.3;
      const sdT = Math.min(targetCv * center, w * 1.6);
      const marks = [], freqs = [], edges = [];
      for (let i = 0; i < k; i++) {
        const lo = L0 + i * w, hi = lo + w;
        edges.push([lo, hi]); marks.push((lo + hi) / 2);
        const pr0 = S.normalCdf((hi - center - w * (rng() - 0.5) * 0.5) / sdT) - S.normalCdf((lo - center) / sdT);
        freqs.push(Math.max(1, Math.round(total * Math.max(pr0, 0.02) + (rng() - 0.5) * 4)));
      }
      const st = S.groupedStats(marks, freqs);
      const cv = st.cv * 100;
      if (cvClass(cv) !== wantBand) continue;
      if (Math.abs(cv - 10) < 1.2 || Math.abs(cv - 20) < 1.5) continue;
      if (st.n < 50) continue;
      const idx = randInt(1, k - 2);
      const rows = edges.map((e, i) => [`${fa(e[0])} – ${fa(e[1])}`, freqs[i]]);
      rows.push([`<strong>Total</strong>`, `<strong>${st.n}</strong>`]);
      const band = cvClass(cv);
      const jOpts = {
        rep: 'Homogénea y la media es representativa (CV ≤ 10%)',
        hom: 'Homogénea, pero la media no es tan representativa (10% < CV ≤ 20%)',
        het: 'Heterogénea (CV > 20%): la media no es representativa',
      };
      const steps = [];
      steps.push(numStep(`¿Cuál es la marca de clase del intervalo ${fa(edges[idx][0])} – ${fa(edges[idx][1])}?`, marks[idx], {
        tol: 0.001, dec: 2, explain: `Marca de clase = punto medio = (${fa(edges[idx][0])} + ${fa(edges[idx][1])})/2 = ${fa(marks[idx])}.`,
        hint: 'Es el promedio de los dos límites del intervalo.', calc: `Calculadora: (${fa(edges[idx][0])} + ${fa(edges[idx][1])}) ÷ 2 = ${fa(marks[idx])}`,
      }));
      const statCalc = 'SHIFT MENU (SETUP) → ▼ → 3 Statistics → 1 On (columna Freq). Luego MENU → 6 Statistics → 1 1-Variable: marcas de clase en x y frecuencias en Freq → AC → OPTN → 3 1-Variable Calc';
      steps.push(numStep('Calculá la media x̄ con las marcas de clase ponderadas por las frecuencias.', st.mean, {
        tol: 0.005, tolMode: 'rel', dec: 3, unit: sc.unit, explain: `x̄ = Σ(xᵢ·fᵢ)/n = ${fa(st.mean, 3)} ${sc.unit}.`,
        hint: 'Si no activás la columna de frecuencias, la calculadora trata cada marca como un dato único.',
        calc: `${statCalc} → x̄ = ${fa(st.mean, 3)}`,
      }));
      steps.push(numStep('Calculá el desvío estándar muestral s (el sx de la calculadora, con n − 1).', st.sd, {
        tol: 0.025, tolMode: 'rel', dec: 3, unit: sc.unit, explain: `s = √(Σfᵢ(xᵢ − x̄)²/(n − 1)) = ${fa(st.sd, 3)} ${sc.unit}.`,
        hint: 'La calculadora muestra σx (divide por n) y sx (divide por n − 1); acá usamos sx.',
        calc: `${statCalc} → sx = ${fa(st.sd, 3)}`,
      }));
      steps.push(numStep('Calculá el coeficiente de variación CV = s / x̄ · 100 (en %).', cv, {
        tol: 0.03, tolMode: 'rel', dec: 2, unit: '%', pct: true, explain: `CV = ${fa(st.sd, 3)} / ${fa(st.mean, 3)} · 100 = ${fa(cv, 2)}%.`,
        hint: 'Es el desvío dividido por la media, expresado en porcentaje.', calc: `Calculadora: ${fa(st.sd, 3)} ÷ ${fa(st.mean, 3)} × 100 = ${fa(cv, 2)}`,
      }));
      steps.push(choiceStep('¿Qué conclusión corresponde? (criterio de la cátedra: CV ≤ 20% homogénea; CV ≤ 10% la media es representativa)', jOpts[band],
        Object.keys(jOpts).filter((b) => b !== band).map((b) => jOpts[b]).concat(['Es heterogénea porque s es mayor que 1']), {
          explain: `CV = ${fa(cv, 2)}% → ${jOpts[band]}.`, hint: 'Compará el CV con 10% y con 20%.',
        }));
      return {
        title: 'Tabla de frecuencias agrupada: x̄, s y CV',
        stem: `Se registró ${sc.what}. Los datos agrupados son:${tbl(['Intervalo', 'Frecuencia (fᵢ)'], rows, 'data')} Calculá x̄, s y el CV, y concluí sobre la homogeneidad.`,
        steps, meta: { marks, freqs, mean: st.mean, sd: st.sd, cv, band },
      };
    }
    throw new Error('grouped generator did not converge');
  }

  /* ======================= (l) regression ======================= */
  const REG_SC = [
    { x: 'las horas de estudio semanales', y: 'la nota del parcial', xs: [2, 14, 1], a0: [30, 45], b0: [2.5, 4], noise: 4, xu: 'horas', yu: 'puntos', dec: 0, sign: 1 },
    { x: 'la inversión en publicidad (miles de $)', y: 'las ventas mensuales (miles de $)', xs: [5, 40, 5], a0: [100, 150], b0: [3, 6], noise: 12, xu: 'miles de $', yu: 'miles de $', dec: 0, sign: 1 },
    { x: 'la temperatura máxima del día (°C)', y: 'el consumo de helados (kg)', xs: [18, 38, 2], a0: [-40, -20], b0: [4, 7], noise: 8, xu: '°C', yu: 'kg', dec: 0, sign: 1 },
    { x: 'la antigüedad del auto (años)', y: 'el precio de reventa (miles de USD)', xs: [1, 12, 1], a0: [20, 28], b0: [-2.2, -1.4], noise: 1.6, xu: 'años', yu: 'miles de USD', dec: 1, sign: -1 },
    { x: 'la distancia al centro (km)', y: 'el alquiler mensual (miles de $)', xs: [1, 15, 1], a0: [400, 520], b0: [-22, -12], noise: 18, xu: 'km', yu: 'miles de $', dec: 0, sign: -1 },
  ];
  function rStrength(r) {
    const a = Math.abs(r);
    return a >= 0.9 ? 'muy fuerte' : a >= 0.7 ? 'fuerte' : a >= 0.4 ? 'moderada' : 'débil';
  }
  function genRegression() {
    const sc = pick(REG_SC);
    for (let tries = 0; tries < 300; tries++) {
      const n = randInt(6, 8);
      const [lo, hi, st] = sc.xs;
      const pool = [];
      for (let v = lo; v <= hi; v += st) pool.push(v);
      if (pool.length < n) continue;
      const xs = shuffle(pool).slice(0, n).sort((a, b) => a - b);
      const a0 = sc.a0[0] + rng() * (sc.a0[1] - sc.a0[0]);
      const b0 = sc.b0[0] + rng() * (sc.b0[1] - sc.b0[0]);
      const ys = xs.map((x) => round(a0 + b0 * x + (rng() * 2 - 1) * sc.noise, sc.dec));
      const reg = S.linreg(xs, ys);
      if (Math.abs(reg.r) < 0.8 || Math.abs(reg.r) > 0.985 || Math.sign(reg.b) !== sc.sign) continue;
      const x0 = pick(xs.slice(1, -1)) + (st >= 2 ? 1 : 0.5);
      const x0r = clamp(x0, lo, hi);
      const pred = reg.a + reg.b * x0r;
      const bTxt = fmt(reg.b, 3), aTxt = fmt(reg.a, 3);
      const dir = reg.b > 0 ? 'aumenta' : 'disminuye';
      const opp = reg.b > 0 ? 'disminuye' : 'aumenta';
      const strength = rStrength(reg.r);
      const rDirTxt = reg.r > 0 ? 'positiva (directa)' : 'negativa (inversa)';
      const oppDirTxt = reg.r > 0 ? 'negativa (inversa)' : 'positiva (directa)';
      const strengths = ['muy fuerte', 'fuerte', 'moderada', 'débil'];
      const wrongStrength = strengths.find((s) => s !== strength && Math.abs(strengths.indexOf(s) - strengths.indexOf(strength)) === 2) || 'débil';
      const steps = [];
      const calcReg = 'MENU → 6 Statistics → 2 y=a+bx → cargá X en la 1ª columna e Y en la 2ª → AC → OPTN → ▼ 4 Regression (1 a, 2 b, 3 r)';
      steps.push(choiceStep(`Queremos predecir ${sc.y} a partir de ${sc.x}. ¿Qué variable va en X (explicativa)?`, `X = ${sc.x}`, [`X = ${sc.y}`, 'Da lo mismo cuál va en X', 'X = el número de observaciones'], {
        explain: `La variable que se usa para predecir va en X; la predicha va en Y (ŷ = a + b·x).`, hint: 'La variable explicativa es la que "explica" o se usa para predecir.',
      }));
      steps.push(numStep('Calculá la pendiente b de la recta ŷ = a + b·x.', reg.b, {
        tol: 0.015, tolMode: 'rel', dec: 3, explain: `b = Sxy/Sxx = ${bTxt}.`, hint: 'Cargá bien las dos columnas de datos; b es el coeficiente de X.',
        calc: `${calcReg} → b = ${bTxt}`,
      }));
      steps.push(numStep('Calculá la ordenada al origen a.', reg.a, {
        tol: 0.02, tolMode: 'rel', dec: 3, explain: `a = ȳ − b·x̄ = ${fa(reg.my, 3)} − (${bTxt})(${fa(reg.mx, 3)}) = ${aTxt}.`, hint: 'a = ȳ − b·x̄ (la calculadora lo muestra como "a").',
        calc: `${calcReg} → a = ${aTxt}`,
      }));
      steps.push(choiceStep(`¿Cómo se interpreta la pendiente b = ${bTxt}?`,
        `Por cada ${sc.xu === 'miles de $' ? 'mil pesos' : sc.xu.replace(/s$/, '')} adicional de X, Y ${dir} en promedio ${fmt(Math.abs(reg.b), 2)} ${sc.yu}.`,
        [`Por cada unidad adicional de X, Y ${opp} en promedio ${fmt(Math.abs(reg.b), 2)} ${sc.yu}.`,
          `Cuando X vale 0, Y vale ${fmt(Math.abs(reg.b), 2)}.`,
          `Y ${dir} un ${fmt(Math.abs(reg.b), 2)}% por cada unidad de X.`], {
          explain: 'La pendiente es el cambio promedio de Y por cada unidad que aumenta X; su signo indica el sentido de la relación.',
          hint: 'b mide el cambio en Y por unidad de X (no es un porcentaje, y no es el valor en X = 0: eso es a).',
        }));
      steps.push(numStep('Calculá el coeficiente de correlación r.', reg.r, {
        tol: 0.006, dec: 4, explain: `r = ${fmt(reg.r, 4)}.`, hint: 'Tiene el mismo signo que la pendiente. En la calculadora aparece como "r".',
        calc: `${calcReg} → r = ${fmt(reg.r, 4)}`,
      }));
      steps.push(choiceStep(`¿Cómo se interpreta r = ${fmt(reg.r, 3)}?`,
        `Correlación lineal ${rDirTxt} y ${strength}.`,
        [`Correlación lineal ${oppDirTxt} y ${strength}.`, `Correlación lineal ${rDirTxt} y ${wrongStrength}.`, `El ${fa(Math.abs(reg.r) * 100, 1)}% de la variación de Y se explica por X.`], {
          explain: `El signo da el sentido (${reg.r > 0 ? '+' : '−'}) y |r| = ${fmt(Math.abs(reg.r), 3)} da la fuerza (${strength}). Lo que se explica es r², no r.`,
          hint: 'Signo → sentido de la relación; |r| cerca de 1 → relación fuerte. Cuidado: el porcentaje explicado es r², no r.',
        }));
      steps.push(numStep('Calculá el coeficiente de determinación R² = r².', reg.r2, {
        tol: 0.006, dec: 4, explain: `R² = (${fmt(reg.r, 4)})² = ${fmt(reg.r2, 4)}: el ${fa(reg.r2 * 100, 1)}% de la variabilidad de Y es explicada por la relación lineal con X.`,
        hint: 'Elevá r al cuadrado. Siempre da positivo.', prob: true, calc: `Calculadora: ${fmt(reg.r, 4)}² = ${fmt(reg.r2, 4)}`,
      }));
      steps.push(numStep(`Predecí ${sc.y} para X = ${fa(x0r)} ${sc.xu}.`, pred, {
        tol: 0.015, tolMode: 'rel', dec: 3, unit: sc.yu, explain: `ŷ = ${aTxt} + (${bTxt})(${fa(x0r)}) = ${fa(pred, 3)} ${sc.yu}. (X = ${fa(x0r)} está dentro del rango observado, así que es una interpolación razonable.)`,
        hint: 'Reemplazá X en ŷ = a + b·X con los signos correctos.', calc: `Calculadora: ${aTxt} + (${bTxt}) × ${fa(x0r)} = ${fa(pred, 3)}`,
      }));
      return {
        title: 'Regresión lineal: a, b, r, R² y predicción',
        stem: `Se registraron, para ${n} casos, ${sc.x} (X) y ${sc.y} (Y):${tbl(['X', ...xs.map(String)].map((h) => h), [['Y', ...ys.map((y) => fa(y))]], 'data')} Ajustá la recta de regresión de Y sobre X.`,
        steps, meta: { xs, ys, a: reg.a, b: reg.b, r: reg.r, r2: reg.r2, x0: x0r, pred },
      };
    }
    throw new Error('regression generator did not converge');
  }

  /* ======================= (m) Bayes ======================= */
  const BAYES_SC = [
    {
      branches: ['Máquina A', 'Máquina B', 'Máquina C'], priors: [[0.5, 0.3, 0.2], [0.45, 0.35, 0.2], [0.6, 0.25, 0.15], [0.5, 0.25, 0.25]],
      lik: [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08],
      intro: (b, pri) => `Una fábrica produce con tres máquinas: ${b.map((x, i) => `${x} aporta el ${pc(pri[i], 0)}`).join(', ')} de la producción.`,
      evt: 'defectuoso', evtTxt: 'defectuosa', lk: (x, p) => `la probabilidad de que una pieza de ${x} sea defectuosa es ${pc(p, 0)}`,
      ask: (b) => `Se elige al azar una pieza y resulta defectuosa. ¿Cuál es la probabilidad de que provenga de ${b}?`,
    },
    {
      branches: ['Proveedor 1', 'Proveedor 2', 'Proveedor 3'], priors: [[0.4, 0.35, 0.25], [0.5, 0.3, 0.2], [0.6, 0.3, 0.1]],
      lik: [0.02, 0.03, 0.05, 0.07, 0.1],
      intro: (b, pri) => `Un taller compra repuestos a tres proveedores: ${b.map((x, i) => `${x} provee el ${pc(pri[i], 0)}`).join(', ')}.`,
      evt: 'fallado', evtTxt: 'falla', lk: (x, p) => `el ${pc(p, 0)} de los repuestos de ${x} falla antes de tiempo`,
      ask: (b) => `Se elige un repuesto que falló antes de tiempo. ¿Cuál es la probabilidad de que sea de ${b}?`,
    },
  ];

  function genBayes() {
    const sc = pick(BAYES_SC);
    const three = rng() < 0.6;
    let priors = pick(sc.priors);
    let names = sc.branches.slice();
    if (!three) { priors = [priors[0], round(1 - priors[0], 2)]; names = names.slice(0, 2); }
    // distinct likelihoods
    const lk = shuffle(sc.lik).slice(0, names.length);
    const joint = priors.map((p, i) => p * lk[i]);
    const total = joint.reduce((a, b) => a + b, 0);
    const j = randInt(0, names.length - 1);
    const post = joint[j] / total;
    const steps = [];
    steps.push(choiceStep('¿Qué probabilidad se está pidiendo?', `P(${names[j]} | defecto/falla): una probabilidad condicional "invertida" (Bayes)`,
      [`P(defecto/falla | ${names[j]}): el dato directo del enunciado`, `P(${names[j]}): la probabilidad previa`, 'P(defecto/falla): la probabilidad total'], {
        explain: `Ya se sabe que ocurrió el evento (defecto/falla) y se pregunta de dónde viene: es P(${names[j]} | evento), que se resuelve con Bayes.`,
        hint: 'Mirá qué es lo conocido (lo que "ya pasó") y qué se pregunta: se condiciona por el evento observado.',
      }));
    steps.push(numStep('Calculá la probabilidad total de que ocurra el evento: P(E) = Σ P(Aᵢ)·P(E|Aᵢ).', total, {
      tol: 0.0006, prob: true, dec: 4,
      explain: `P(E) = ${names.map((n, i) => `${fa(priors[i], 2)}·${fa(lk[i], 2)}`).join(' + ')} = ${pr(total)}.`,
      hint: 'Sumá, para cada rama, probabilidad de la rama × probabilidad condicional del evento.',
      calc: `Calculadora: ${names.map((n, i) => `${fa(priors[i], 2)} × ${fa(lk[i], 2)}`).join(' + ')} = ${pr(total)}`,
    }));
    steps.push(numStep(`Calculá la probabilidad conjunta P(${names[j]} ∩ E) = P(${names[j]})·P(E|${names[j]}).`, joint[j], {
      tol: 0.0006, prob: true, dec: 4, explain: `${fa(priors[j], 2)} · ${fa(lk[j], 2)} = ${pr(joint[j])}.`,
      hint: 'Es la rama del árbol que lleva a ese proveedor/máquina y al evento: se multiplican sus probabilidades.',
      calc: `Calculadora: ${fa(priors[j], 2)} × ${fa(lk[j], 2)} = ${pr(joint[j])}`,
    }));
    steps.push(numStep(`Aplicá Bayes: P(${names[j]} | E) = P(${names[j]} ∩ E) / P(E).`, post, {
      tol: 0.003, prob: true, dec: 4, explain: `${pr(joint[j])} / ${pr(total)} = ${pr(post)}.`,
      hint: 'Dividí la conjunta de la rama pedida por la probabilidad total (no por la probabilidad previa).',
      calc: `Calculadora: ${pr(joint[j])} ÷ ${pr(total)} = ${pr(post)}`,
    }));
    const givensRows = names.map((n, i) => [n, pc(priors[i], 0), pc(lk[i], 0)]);
    return {
      title: 'Bayes: probabilidad total y posterior',
      stem: `${sc.intro(names, priors)} Se sabe que ${names.map((x, i) => sc.lk(x, lk[i])).join('; ')}. ${sc.ask(names[j])}`,
      givens: { title: 'Árbol de probabilidades (datos)', html: tbl(['Origen', 'P(origen)', 'P(evento | origen)'], givensRows), note: 'Es el mismo dato del enunciado ordenado como las ramas de un árbol.' },
      steps, meta: { priors, lk, total, post, j, joint },
    };
  }

  /* ======================= (n) 2x2 contingency table ======================= */
  const CONT_SC = [
    { rows: ['Turno mañana', 'Turno tarde'], cols: ['Defectuoso', 'No defectuoso'], what: 'piezas producidas en una fábrica', rn: ['de turno mañana', 'de turno tarde'], cn: ['defectuosas', 'no defectuosas'] },
    { rows: ['Mujer', 'Varón'], cols: ['Aprobó', 'Desaprobó'], what: 'alumnos que rindieron un examen', rn: ['mujeres', 'varones'], cn: ['aprobaron', 'desaprobaron'] },
    { rows: ['Plan básico', 'Plan premium'], cols: ['Renovó', 'No renovó'], what: 'clientes de un servicio de suscripción', rn: ['del plan básico', 'del plan premium'], cn: ['renovaron', 'no renovaron'] },
    { rows: ['Sucursal Norte', 'Sucursal Sur'], cols: ['Compra online', 'Compra en el local'], what: 'compras registradas por una cadena de tiendas', rn: ['de la sucursal Norte', 'de la sucursal Sur'], cn: ['online', 'en el local'] },
  ];
  function genContingency() {
    const sc = pick(CONT_SC);
    const independent = rng() < 0.45;
    let c;
    for (let tries = 0; tries < 200; tries++) {
      const N = pick([200, 400]);
      const pa = pick([0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75]);
      const pb = pick([0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75]);
      const a = Math.round(N * pa * pb);
      const r1 = Math.round(N * pa), c1 = Math.round(N * pb);
      c = { N, a, b: r1 - a, c: c1 - a, d: N - r1 - c1 + a };
      if (!independent) {
        const delta = pick([-1, 1]) * Math.round(N * pick([0.04, 0.06, 0.08]));
        c = { N, a: a + delta, b: c.b - delta, c: c.c - delta, d: c.d + delta };
      }
      if (Object.values(c).every((v) => v >= 5)) {
        const isInd = c.a * c.d === c.b * c.c;
        if (isInd === independent) break;
      }
      c = null;
    }
    if (!c) c = { N: 200, a: 40, b: 60, c: 40, d: 60 };
    const { N } = c;
    const R = [c.a + c.b, c.c + c.d];
    const C = [c.a + c.c, c.b + c.d];
    const cell = [[c.a, c.b], [c.c, c.d]];
    const ri = randInt(0, 1), ci = randInt(0, 1);
    const pRow = R[ri] / N, pCol = C[ci] / N, pJoint = cell[ri][ci] / N;
    const pCond = pJoint / pCol;
    const isInd = c.a * c.d === c.b * c.c;
    const tableHtml = tbl([' ', sc.cols[0], sc.cols[1], 'Total'], [
      [sc.rows[0], c.a, c.b, R[0]], [sc.rows[1], c.c, c.d, R[1]], ['<strong>Total</strong>', `<strong>${C[0]}</strong>`, `<strong>${C[1]}</strong>`, `<strong>${N}</strong>`],
    ], 'data');
    const R_ = `${sc.rows[ri]}`, C_ = `${sc.cols[ci]}`;
    const steps = [];
    steps.push(numStep(`Probabilidad marginal: P(${R_}) = total de la fila / total general.`, pRow, {
      tol: 0.0006, prob: true, dec: 4, explain: `P(${R_}) = ${R[ri]}/${N} = ${pr(pRow)}.`, hint: 'Usá el total de la fila (margen derecho) dividido por el total general.',
      calc: `Calculadora: ${R[ri]} ÷ ${N} = ${pr(pRow)}`,
    }));
    steps.push(numStep(`Probabilidad conjunta: P(${R_} ∩ ${C_}).`, pJoint, {
      tol: 0.0006, prob: true, dec: 4, explain: `Es el casillero (${R_}, ${C_}) sobre el total general: ${cell[ri][ci]}/${N} = ${pr(pJoint)}.`,
      hint: 'La conjunta es el casillero interior dividido por el total general (N).', calc: `Calculadora: ${cell[ri][ci]} ÷ ${N} = ${pr(pJoint)}`,
    }));
    steps.push(choiceStep(`¿Cómo se calcula P(${R_} | ${C_})?`, `P(${R_} ∩ ${C_}) / P(${C_})  =  ${cell[ri][ci]} / ${C[ci]}`,
      [`P(${R_} ∩ ${C_}) / P(${R_})  =  ${cell[ri][ci]} / ${R[ri]}`, `P(${R_}) · P(${C_})`, `${cell[ri][ci]} / ${N}`], {
        explain: `El que está después de la barra es la condición: el universo se reduce a la columna "${C_}" (total ${C[ci]}).`,
        hint: 'El evento que aparece después de la barra "|" es el que define el nuevo total (denominador).',
      }));
    steps.push(numStep(`Calculá P(${R_} | ${C_}).`, pCond, {
      tol: 0.0006, prob: true, dec: 4, explain: `${cell[ri][ci]}/${C[ci]} = ${pr(pCond)}.`, hint: `El denominador es el total de la columna "${C_}", no el total general.`,
      calc: `Calculadora: ${cell[ri][ci]} ÷ ${C[ci]} = ${pr(pCond)}`,
    }));
    const indOK = `Independientes: P(${R_} | ${C_}) = ${pr(pCond)} es igual a P(${R_}) = ${pr(pRow)}`;
    const indNo = `No independientes: P(${R_} | ${C_}) = ${pr(pCond)} es distinto de P(${R_}) = ${pr(pRow)}`;
    steps.push(choiceStep('¿Los eventos son independientes?', isInd ? indOK : indNo,
      [isInd ? indNo : indOK, `Son mutuamente excluyentes porque P(${R_} ∩ ${C_}) ≠ 0`, 'No se puede saber sin conocer la población'], {
        explain: isInd ? 'Hay independencia: saber la columna no cambia la probabilidad de la fila (P(A|B) = P(A), o equivalentemente P(A∩B) = P(A)·P(B)).'
          : 'Si P(A|B) ≠ P(A) los eventos NO son independientes. (Excluyentes sería P(A∩B) = 0, que acá no ocurre: son conceptos distintos.)',
        hint: 'Compará P(A|B) con P(A) (o P(A∩B) con P(A)·P(B)). Excluyente e independiente no son lo mismo.',
      }));
    return {
      title: 'Tabla 2×2: marginal, conjunta, condicional e independencia',
      stem: `Se clasificaron ${N} ${sc.what}:${tableHtml} Se elige un caso al azar.`,
      steps, meta: { cell, R, C, N, ri, ci, pRow, pJoint, pCond, isInd },
    };
  }

  /* ======================= (o) Normal -> p -> Binomial ======================= */
  const COMBO_SC = [
    { sc: NORMAL_SC[1], bad: (t, a) => `Un paquete se considera fuera de norma si pesa ${t === 'lt' ? 'menos de' : 'más de'} ${a} g`, unitWord: 'paquetes', what: 'fuera de norma' },
    { sc: NORMAL_SC[4], bad: (t, a) => `Un eje se descarta si su diámetro es ${t === 'lt' ? 'menor que' : 'mayor que'} ${a} mm`, unitWord: 'ejes', what: 'descartados' },
    { sc: NORMAL_SC[2], bad: (t, a) => `Un alumno desaprueba si obtiene ${t === 'lt' ? 'menos de' : 'más de'} ${a} puntos`, unitWord: 'alumnos', what: 'desaprobados' },
    { sc: NORMAL_SC[7], bad: (t, a) => `Una botella se rechaza si contiene ${t === 'lt' ? 'menos de' : 'más de'} ${a} ml`, unitWord: 'botellas', what: 'rechazadas' },
  ];
  function genNormalBinomial() {
    const cs = pick(COMBO_SC);
    const type = pick(['lt', 'gt']);
    let d;
    for (let tries = 0; tries < 100; tries++) {
      d = drawNormal(cs.sc, 1);
      const pTry = type === 'lt' ? Phi(d.zs[0]) : 1 - Phi(d.zs[0]);
      if (pTry >= 0.02 && pTry <= 0.35) break; // a "defect" should be a rare-ish event
    }
    const a = d.xs[0];
    const res = normalProbSteps({ mu: d.mu, sd: d.sigma, type, a, unitTxt: cs.sc.unit, tol: 0.0012 });
    const p = round(res.prob, 4);
    const n = randInt(5, 12);
    const etype = pick(['atleast', 'atleast', 'exact', 'atmost']);
    const k = etype === 'atleast' ? 1 : clamp(Math.round(n * p) + randInt(0, 1), 0, 3) || 1;
    const dist = {
      cdf: (x) => S.binomCdf(x, n, p), pmf: (x) => S.binomPmf(x, n, p),
      pd: 'Binomial PD (4)', cd: 'Binomial CD (▼ 1)', params: `N = ${n}, p = ${pr(p)}`,
    };
    const ev = discreteEvent(etype, k, undefined, dist);
    const steps = res.steps.slice();
    steps.push(choiceStep(`Ahora se toman ${n} ${cs.unitWord} independientes y se cuenta cuántos están ${cs.what}. ¿Qué distribución tiene esa cantidad?`,
      `Binomial(n = ${n}, p = ${pr(p)})`, [`Binomial(n = ${n}, p = ${pr(1 - p)})`, `Normal(μ = ${fa(d.mu)}; σ = ${fa(d.sigma)})`, `Poisson(λ = ${pr(p)})`], {
        explain: `La normal sirvió para obtener p = ${pr(p)} de "estar ${cs.what}"; con ese p, contar casos en n ensayos independientes es una Binomial.`,
        hint: 'La probabilidad del paso anterior es el "p" de la binomial; n es la cantidad de unidades tomadas.',
      }));
    steps.push(choiceStep(`¿Cómo se expresa la probabilidad de que ${ev.text} estén ${cs.what}?`, ev.correct, ev.wrong, {
      explain: `${ev.event}.`, hint: 'Binomial CD da P(X ≤ x). "Al menos uno" es el complemento de "ninguno": 1 − P(X = 0).',
    }));
    steps.push(numStep(`Calculá la probabilidad de que ${ev.text} estén ${cs.what} (usá p = ${pr(p)}).`, ev.prob, {
      tol: 0.002, prob: true, dec: 4, calc: ev.calc,
      explain: `${ev.event} = ${pr(ev.prob)}.`,
      hint: 'Usá el p que calculaste con la normal y el n del enunciado; para "al menos uno" calculá 1 − (1 − p)ⁿ.',
    }));
    return {
      title: 'Combo: Normal → p → Binomial',
      stem: `${cs.sc.subject} se distribuye normalmente con media μ = ${withUnit(d.mu, cs.sc)} y desvío σ = ${withUnit(d.sigma, cs.sc)}. ${cs.bad(type, fa(a, 4))}. Se eligen ${n} ${cs.unitWord} al azar, de forma independiente. ¿Cuál es la probabilidad de que ${ev.text} estén ${cs.what}?`,
      givens: phiGiven([res.za]), steps, meta: { type, mu: d.mu, sigma: d.sigma, a, p, n, etype, k, answer: ev.prob },
    };
  }

  /* ======================= registry ======================= */
  const GENERATORS = [
    { id: 'binomial', title: 'Binomial: exactamente / al menos / a lo sumo / entre', topic: 'binomial', make: genBinomial },
    { id: 'poisson', title: 'Poisson: reescalar λ a otro intervalo', topic: 'poisson', make: genPoisson },
    { id: 'normal-prob', title: 'Normal: P(X < a), P(X > a), P(a < X < b)', topic: 'normal', make: genNormalProb },
    { id: 'normal-inversa', title: 'Normal inversa: x para un percentil', topic: 'normal', make: genNormalInverse },
    { id: 'normal-mu-sigma', title: 'Normal: hallar μ y σ con dos percentiles', topic: 'normal', make: genMuSigma },
    { id: 'muestral-media', title: 'Muestral: media (σ/√n) y suma (√n·σ)', topic: 'muestral-media', make: genSamplingMean },
    { id: 'muestral-prop', title: 'Muestral: proporción p̂', topic: 'muestral-proporcion', make: genSamplingProp },
    { id: 'ic-media', title: 'IC para la media (Z con σ conocida / t con σ desconocida)', topic: 'ic-media', make: genIcMean },
    { id: 'ic-prop', title: 'IC para una proporción', topic: 'ic-proporcion', make: genIcProp },
    { id: 'tamano-muestra', title: 'Tamaño de muestra (media y proporción)', topic: 'tamano-muestra', make: genSampleSize },
    { id: 'tabla-frecuencias', title: 'Tabla agrupada: x̄, s, CV y homogeneidad', topic: 'descriptiva', make: genGrouped },
    { id: 'regresion', title: 'Regresión: a, b, r, R² y predicción', topic: 'regresion', make: genRegression },
    { id: 'bayes', title: 'Bayes: probabilidad total y posterior', topic: 'condicional-bayes', make: genBayes },
    { id: 'contingencia', title: 'Tabla 2×2: marginal, conjunta, condicional, independencia', topic: 'contingencia', make: genContingency },
    { id: 'normal-binomial', title: 'Combo: Normal → p → Binomial', topic: 'binomial', make: genNormalBinomial },
  ];

  function generate(id) {
    const g = GENERATORS.find((x) => x.id === id) || pick(GENERATORS);
    const ex = g.make();
    ex.gen = g.id;
    ex.topic = g.topic;
    return ex;
  }

  return { GENERATORS, generate, setRng, mulberry32, checkNumber, fmt, fa };
});
