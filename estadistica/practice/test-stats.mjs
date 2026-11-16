// Run: node practice/test-stats.mjs
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const S = require('./stats.js');

let failed = 0;
let passed = 0;
function near(name, got, want, tol = 1e-4) {
  const ok = Number.isFinite(got) && Math.abs(got - want) <= tol;
  if (ok) passed++; else { failed++; console.error(`FAIL ${name}: got ${got}, want ${want} (tol ${tol})`); }
}

// Known values
near('Phi(1.96)', S.normalCdf(1.96), 0.9750, 5e-5);
near('Phi(-1)', S.normalCdf(-1), 0.1587, 5e-5);
near('Phi(0)', S.normalCdf(0), 0.5, 1e-15);
near('Phi(1)', S.normalCdf(1), 0.8413447460685429, 1e-13);
near('Phi(3.5)', S.normalCdf(3.5), 0.9997673709209645, 1e-13);
near('Phi(-4)', S.normalCdf(-4), 3.167124183311992e-5, 1e-15);
near('Phi(-6)', S.normalCdf(-6), 9.865876450376946e-10, 1e-18);
near('erf(0.5)', S.erf(0.5), 0.5204998778130465, 1e-14);
near('erf(2.9)', S.erf(2.9), 0.9999589021219005, 1e-14);
near('erf(3.1)', S.erf(3.1), 0.9999883513426328, 1e-14);
near('invNorm(0.975)', S.invNorm(0.975), 1.95996, 1e-5);
near('invNorm(0.5)', S.invNorm(0.5), 0, 1e-12);
near('invNorm(0.9)', S.invNorm(0.9), 1.2815515655446004, 1e-9);
near('invNorm(0.025)', S.invNorm(0.025), -1.95996398454005, 1e-9);
near('invNorm(0.001)', S.invNorm(0.001), -3.090232306167813, 1e-9);
for (const p of [0.001, 0.01, 0.1, 0.3, 0.5, 0.77, 0.95, 0.999]) near(`roundtrip ${p}`, S.normalCdf(S.invNorm(p)), p, 1e-12);
near('Bin(10,.3) P(X<=2)', S.binomCdf(2, 10, 0.3), 0.3828, 5e-5);
near('Bin(10,.3) P(X=2)', S.binomPmf(2, 10, 0.3), 0.2334744405, 1e-9);
near('Bin(10,.5) sums to 1', S.binomCdf(10, 10, 0.5), 1, 1e-12);
near('Pois(2) P(X=0)', S.poissonPmf(0, 2), 0.1353, 5e-5);
near('Pois(2) P(X<=2)', S.poissonCdf(2, 2), 0.6766764161830635, 1e-12);
near('Pois(4.5) P(X=3)', S.poissonPmf(3, 4.5), 0.1687, 5e-5);
near('Hyper(N=20,K=8,n=5,k=2)', S.hypergeomPmf(2, 20, 8, 5), 0.3973168215, 1e-9);
near('mean', S.mean([4, 8, 6, 5, 7]), 6, 1e-12);
near('sd sample', S.sd([4, 8, 6, 5, 7]), Math.sqrt(2.5), 1e-12);
near('sd pop', S.sd([4, 8, 6, 5, 7], false), Math.sqrt(2), 1e-12);
const g = S.groupedStats([10, 20, 30], [1, 2, 1]);
near('grouped mean', g.mean, 20, 1e-12);
near('grouped sd', g.sd, Math.sqrt(200 / 3), 1e-12);
const reg = S.linreg([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]);
near('reg b', reg.b, 0.6, 1e-12);
near('reg a', reg.a, 2.2, 1e-12);
near('reg r', reg.r, 0.7745966692414834, 1e-12);
near('reg r2', reg.r2, 0.6, 1e-12);

// t table vs numerical integration of the t density (independent check)
function tPdf(t, df) {
  return Math.exp(S.logGamma((df + 1) / 2) - S.logGamma(df / 2)) / Math.sqrt(df * Math.PI) * Math.pow(1 + t * t / df, -(df + 1) / 2);
}
function tCdfUpper(t, df) { // P(0 < T < t) with Simpson on a substitution that tames heavy tails
  const n = 20000;
  const h = t / n;
  let s = tPdf(0, df) + tPdf(t, df);
  for (let i = 1; i < n; i++) s += tPdf(i * h, df) * (i % 2 ? 4 : 2);
  return s * h / 3;
}
for (const conf of [0.90, 0.95, 0.99]) {
  for (let df = 1; df <= 30; df++) {
    const t = S.tCrit(conf, df);
    near(`t table ${conf} df=${df}`, 2 * tCdfUpper(t, df), conf, (df === 1 ? 1.5e-3 : 5e-4));
  }
}
near('zCrit 95', S.zCrit(95), 1.960, 1e-9);
near('tCrit df>30 fallback', S.tCrit(0.95, 60), 1.960, 1e-9);

console.log(`${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
