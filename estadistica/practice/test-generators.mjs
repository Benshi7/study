// Run: node practice/test-generators.mjs   (200 instances per generator, seeded)
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const S = require('./stats.js');
const G = require('./generators.js');

const N = 200;
let errors = 0;
const seen = new Set();
function fail(gen, i, msg) {
  errors++;
  if (errors <= 40) console.error(`FAIL [${gen} #${i}] ${msg}`);
}
const near = (a, b, tol) => Number.isFinite(a) && Number.isFinite(b) && Math.abs(a - b) <= tol;

function checkStructure(gen, i, ex) {
  if (typeof ex.stem !== 'string' || ex.stem.length < 20) fail(gen, i, 'bad stem');
  if (/undefined|NaN|\[object/.test(ex.stem)) fail(gen, i, 'stem has undefined/NaN: ' + ex.stem.slice(0, 200));
  if (!Array.isArray(ex.steps) || ex.steps.length < 3) fail(gen, i, 'too few steps');
  if (ex.givens && !/<table/.test(ex.givens.html)) fail(gen, i, 'givens without table');
  ex.steps.forEach((st, k) => {
    const where = `step ${k + 1}`;
    for (const key of ['prompt', 'explain']) {
      if (typeof st[key] !== 'string' || !st[key]) fail(gen, i, `${where}: missing ${key}`);
      else if (/undefined|NaN|\[object/.test(st[key])) fail(gen, i, `${where}: ${key} has undefined/NaN: ${st[key]}`);
    }
    if (st.calc && /undefined|NaN/.test(st.calc)) fail(gen, i, `${where}: calc has undefined/NaN`);
    if (st.type === 'number') {
      if (!Number.isFinite(st.answer)) fail(gen, i, `${where}: non-finite answer`);
      if (!(st.tol >= 0)) fail(gen, i, `${where}: bad tol`);
      if (st.prob && !(st.answer >= 0 && st.answer <= 1)) fail(gen, i, `${where}: probability ${st.answer} outside [0,1]`);
      if (!G.checkNumber(st, st.answer)) fail(gen, i, `${where}: own answer rejected`);
      if (st.viz) for (const key of ['mu', 'sd']) if (!Number.isFinite(st.viz[key])) fail(gen, i, `${where}: viz ${key}`);
    } else if (st.type === 'choice') {
      if (!Array.isArray(st.options) || st.options.length < 3) fail(gen, i, `${where}: <3 options`);
      else {
        if (new Set(st.options).size !== st.options.length) fail(gen, i, `${where}: duplicate options`);
        if (!Number.isInteger(st.answer) || st.answer < 0 || st.answer >= st.options.length) fail(gen, i, `${where}: answer index`);
        if (st.options.some((o) => /undefined|NaN/.test(o))) fail(gen, i, `${where}: option has undefined/NaN`);
      }
    } else fail(gen, i, `${where}: unknown type ${st.type}`);
  });
}

const lastNumberStep = (ex) => [...ex.steps].reverse().find((s) => s.type === 'number');

function discreteTruth(type, k, k2, F, f) {
  switch (type) {
    case 'exact': return f(k);
    case 'atmost': return F(k);
    case 'less': return F(k - 1);
    case 'atleast': { let s = 0; for (let x = 0; x < k; x++) s += f(x); return 1 - s; }
    case 'more': { let s = 0; for (let x = 0; x <= k; x++) s += f(x); return 1 - s; }
    default: { let s = 0; for (let x = k; x <= k2; x++) s += f(x); return s; }
  }
}

const checks = {
  binomial(ex, i) {
    const m = ex.meta;
    const t = discreteTruth(m.type, m.k, m.k2, (x) => S.binomCdf(x, m.n, m.p), (x) => S.binomPmf(x, m.n, m.p));
    if (!near(lastNumberStep(ex).answer, t, 1e-9) && !near(ex.steps[3].answer, t, 1e-9)) fail('binomial', i, `prob mismatch ${t}`);
    if (!near(ex.steps[3].answer, t, 1e-9)) fail('binomial', i, `step4 ${ex.steps[3].answer} != ${t}`);
    if (m.type === 'atleast' && m.k < 1) fail('binomial', i, 'k<1 atleast');
    if (m.k > m.n || (m.k2 && m.k2 > m.n)) fail('binomial', i, 'k > n');
  },
  poisson(ex, i) {
    const m = ex.meta;
    if (!near(ex.steps[1].answer, m.rate * m.f, 1e-9)) fail('poisson', i, 'lambda mismatch');
    const t = discreteTruth(m.type, m.k, m.k2, (x) => S.poissonCdf(x, m.lambda), (x) => S.poissonPmf(x, m.lambda));
    if (!near(ex.steps[3].answer, t, 1e-9)) fail('poisson', i, 'prob mismatch');
  },
  'normal-prob'(ex, i) {
    const m = ex.meta;
    const exact = m.type === 'lt' ? S.normalProb(-Infinity, m.a, m.mu, m.sigma)
      : m.type === 'gt' ? S.normalProb(m.a, Infinity, m.mu, m.sigma) : S.normalProb(m.a, m.b, m.mu, m.sigma);
    if (!near(m.answer, exact, 1e-3)) fail('normal-prob', i, `table-z answer ${m.answer} vs exact ${exact}`);
    if (!near(lastNumberStep(ex).answer, m.answer, 1e-12)) fail('normal-prob', i, 'last step != meta');
    if (m.answer < 0.003 || m.answer > 0.997) fail('normal-prob', i, 'degenerate probability');
  },
  'normal-inversa'(ex, i) {
    const m = ex.meta;
    if (!near(S.normalCdf((m.answer - m.mu) / m.sigma), m.area, 1e-9)) fail('normal-inversa', i, 'x does not give area');
  },
  'normal-mu-sigma'(ex, i) {
    const m = ex.meta;
    if (!(m.sigma > 0)) fail('normal-mu-sigma', i, 'sigma <= 0');
    if (!near(m.mu + m.z1 * m.sigma, m.a, 1e-9) || !near(m.mu + m.z2 * m.sigma, m.b, 1e-9)) fail('normal-mu-sigma', i, 'system inconsistent');
    if (m.b <= m.a) fail('normal-mu-sigma', i, 'b <= a');
    // exact-z solution must be within the step tolerance
    const z1 = S.invNorm(m.p1), z2 = S.invNorm(1 - m.q);
    const sg = (m.b - m.a) / (z2 - z1);
    if (!G.checkNumber(ex.steps[2], sg)) fail('normal-mu-sigma', i, `exact sigma ${sg} rejected vs ${m.sigma}`);
    if (!G.checkNumber(ex.steps[3], m.a - z1 * sg)) fail('normal-mu-sigma', i, 'exact mu rejected');
  },
  'muestral-media'(ex, i) {
    const m = ex.meta;
    const sd = m.variant === 'mean' ? m.sigma / Math.sqrt(m.n) : Math.sqrt(m.n) * m.sigma;
    const mu = m.variant === 'mean' ? m.mu : m.n * m.mu;
    if (!near(sd, m.sd2, 1e-9) || !near(mu, m.mu2, 1e-9)) fail('muestral-media', i, 'sd/mu mismatch');
    const exact = m.type === 'lt' ? S.normalProb(-Infinity, m.xs[0], mu, sd) : m.type === 'gt' ? S.normalProb(m.xs[0], Infinity, mu, sd) : S.normalProb(m.xs[0], m.xs[1], mu, sd);
    if (!near(m.answer, exact, 1e-9) && !near(m.answer, exact, 1.5e-3)) fail('muestral-media', i, 'prob mismatch');
    if (m.n < 30 && m.n !== 16 && m.n !== 25) fail('muestral-media', i, 'n');
  },
  'muestral-prop'(ex, i) {
    const m = ex.meta;
    const exact = m.type === 'lt' ? S.normalProb(-Infinity, m.a, m.p, m.se) : m.type === 'gt' ? S.normalProb(m.a, Infinity, m.p, m.se) : S.normalProb(m.a, m.b, m.p, m.se);
    if (!near(m.answer, exact, 3e-3)) fail('muestral-prop', i, `prob ${m.answer} vs ${exact}`);
    if (m.n * m.p < 5 || m.n * (1 - m.p) < 5) fail('muestral-prop', i, 'normal approx condition');
  },
  'ic-media'(ex, i) {
    const m = ex.meta;
    if (!near(m.lo, m.xbar - m.E, 1e-9) || !near(m.hi, m.xbar + m.E, 1e-9)) fail('ic-media', i, 'limits');
    if (!near(m.E, m.crit * m.sigma / Math.sqrt(m.n), 1e-9)) fail('ic-media', i, 'E');
    if (!Number.isFinite(m.crit) || m.crit <= 0) fail('ic-media', i, 'crit');
    const widthStep = ex.steps.find((s) => /amplitud/.test(s.prompt));
    if (!near(widthStep.answer, 2 * m.E, 1e-9)) fail('ic-media', i, 'width != 2E');
    if (m.useT && m.n >= 30) fail('ic-media', i, 'n too large for t');
    if (!ex.stem.includes(`del ${Math.round(m.conf * 100)}%`)) fail('ic-media', i, 'confidence level missing in stem');
  },
  'ic-prop'(ex, i) {
    const m = ex.meta;
    if (!near(m.E, m.z * Math.sqrt(m.ph * (1 - m.ph) / m.n), 1e-12)) fail('ic-prop', i, 'E');
    if (m.lo < 0 || m.hi > 1) fail('ic-prop', i, 'limits outside [0,1]');
    if (m.x < 5 || m.n - m.x < 5) fail('ic-prop', i, 'condition');
  },
  'tamano-muestra'(ex, i) {
    const m = ex.meta;
    if (m.nFinal !== Math.ceil(m.raw) || !Number.isInteger(m.nFinal)) fail('tamano-muestra', i, 'not ceil');
    const last = lastNumberStep(ex);
    if (last.answer !== m.nFinal || last.tol !== 0) fail('tamano-muestra', i, 'final step');
    const rawExact = m.variant === 'mean'
      ? (S.invNorm(1 - (1 - (m.z === 1.645 ? 0.9 : m.z === 1.96 ? 0.95 : 0.99)) / 2) * m.sigma / m.E) ** 2
      : (S.invNorm(1 - (1 - (m.z === 1.645 ? 0.9 : m.z === 1.96 ? 0.95 : 0.99)) / 2)) ** 2 * m.p * (1 - m.p) / m.E ** 2;
    if (Math.ceil(rawExact) !== m.nFinal) fail('tamano-muestra', i, 'exact z gives a different n');
  },
  'tabla-frecuencias'(ex, i) {
    const m = ex.meta;
    const st = S.groupedStats(m.marks, m.freqs);
    if (!near(st.mean, m.mean, 1e-9) || !near(st.cv * 100, m.cv, 1e-9)) fail('tabla-frecuencias', i, 'stats');
    const band = m.cv <= 10 ? 'rep' : m.cv <= 20 ? 'hom' : 'het';
    if (band !== m.band) fail('tabla-frecuencias', i, 'band');
    // population sd must also be accepted by the s step
    const pop = S.groupedStats(m.marks, m.freqs, false);
    if (!G.checkNumber(ex.steps[2], pop.sd)) fail('tabla-frecuencias', i, 'population sd rejected');
  },
  regresion(ex, i) {
    const m = ex.meta;
    const r = S.linreg(m.xs, m.ys);
    if (!near(r.b, m.b, 1e-9) || !near(r.r, m.r, 1e-9) || !near(r.r2, m.r * m.r, 1e-9)) fail('regresion', i, 'reg');
    if (!near(m.pred, m.a + m.b * m.x0, 1e-9)) fail('regresion', i, 'pred');
    if (m.xs.length < 6 || m.xs.length > 8 || new Set(m.xs).size !== m.xs.length) fail('regresion', i, 'xs');
    if (Math.sign(m.b) !== Math.sign(m.r)) fail('regresion', i, 'sign');
  },
  bayes(ex, i) {
    const m = ex.meta;
    const sumP = m.priors.reduce((a, b) => a + b, 0);
    if (!near(sumP, 1, 1e-9)) fail('bayes', i, `priors sum ${sumP}`);
    const tot = m.priors.reduce((a, p, k) => a + p * m.lk[k], 0);
    if (!near(tot, m.total, 1e-12) || !near(m.priors[m.j] * m.lk[m.j] / tot, m.post, 1e-12)) fail('bayes', i, 'posterior');
    const posts = m.priors.map((p, k) => p * m.lk[k] / tot).reduce((a, b) => a + b, 0);
    if (!near(posts, 1, 1e-9)) fail('bayes', i, 'posteriors do not sum to 1');
  },
  contingencia(ex, i) {
    const m = ex.meta;
    const tot = m.cell.flat().reduce((a, b) => a + b, 0);
    if (tot !== m.N || m.cell.flat().some((v) => v < 0)) fail('contingencia', i, 'table totals');
    const ind = m.cell[0][0] * m.cell[1][1] === m.cell[0][1] * m.cell[1][0];
    if (ind !== m.isInd) fail('contingencia', i, 'independence flag');
    if (!near(m.pCond, m.pJoint / (m.C[m.ci] / m.N), 1e-12)) fail('contingencia', i, 'conditional');
  },
  'normal-binomial'(ex, i) {
    const m = ex.meta;
    const pExact = m.type === 'lt' ? S.normalProb(-Infinity, m.a, m.mu, m.sigma) : S.normalProb(m.a, Infinity, m.mu, m.sigma);
    if (!near(m.p, pExact, 1.5e-3)) fail('normal-binomial', i, `p ${m.p} vs ${pExact}`);
    const k = m.k;
    const exactAns = discreteTruth(m.etype, k, undefined, (x) => S.binomCdf(x, m.n, pExact), (x) => S.binomPmf(x, m.n, pExact));
    const last = lastNumberStep(ex);
    if (!G.checkNumber(last, exactAns)) fail('normal-binomial', i, `exact-p answer ${exactAns} rejected vs ${last.answer}`);
  },
};

let total = 0;
for (const g of G.GENERATORS) {
  G.setRng(G.mulberry32(12345 + g.id.length));
  let uniq = new Set();
  for (let i = 0; i < N; i++) {
    let ex;
    try { ex = G.generate(g.id); } catch (e) { fail(g.id, i, 'threw ' + e.message); continue; }
    total++;
    uniq.add(ex.stem);
    checkStructure(g.id, i, ex);
    try { (checks[g.id] || (() => fail(g.id, i, 'no check defined')))(ex, i); } catch (e) { fail(g.id, i, 'check threw ' + e.stack.split('\n')[1]); }
  }
  console.log(`${g.id.padEnd(18)} ${N} instances, ${uniq.size} distinct stems`);
}
// also: unseeded run to make sure Math.random path works
G.setRng(null);
for (const g of G.GENERATORS) G.generate(g.id);
console.log(`${total} exercises generated, ${errors} failures`);
process.exit(errors ? 1 : 0);
