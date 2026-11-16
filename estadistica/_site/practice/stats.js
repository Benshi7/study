/* Numerical helpers for the practice suite. Works in the browser (window.Stats) and in Node (require). */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.Stats = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const SQRT_PI = Math.sqrt(Math.PI);
  const SQRT_2PI = Math.sqrt(2 * Math.PI);

  /* ---------- error function (series for |x|<3, continued fraction beyond) ---------- */
  function erfSeries(ax) {
    // erf(x) = 2/sqrt(pi) * exp(-x^2) * sum_{n>=0} 2^n x^(2n+1) / (2n+1)!!  (all terms positive: stable)
    let term = ax;
    let sum = ax;
    for (let n = 1; n < 400; n++) {
      term *= (2 * ax * ax) / (2 * n + 1);
      sum += term;
      if (term < 1e-17 * sum) break;
    }
    return (2 / SQRT_PI) * Math.exp(-ax * ax) * sum;
  }

  function erfcLarge(x) {
    // erfc(x) = exp(-x^2)/sqrt(pi) / (x + (1/2)/(x + (2/2)/(x + (3/2)/(x + ...))))
    let t = x;
    for (let k = 80; k >= 1; k--) t = x + (k / 2) / t;
    return Math.exp(-x * x) / SQRT_PI / t;
  }

  function erf(x) {
    if (x === 0) return 0;
    const ax = Math.abs(x);
    const r = ax < 3 ? erfSeries(ax) : 1 - erfcLarge(ax);
    return x < 0 ? -r : r;
  }

  function erfc(x) {
    if (x < 0) return 2 - erfc(-x);
    return x < 3 ? 1 - erfSeries(x) : erfcLarge(x);
  }

  /* ---------- normal ---------- */
  function normalPdf(z) { return Math.exp(-0.5 * z * z) / SQRT_2PI; }

  function normalCdf(z) {
    if (z === Infinity) return 1;
    if (z === -Infinity) return 0;
    return 0.5 * erfc(-z / Math.SQRT2);
  }

  /** P(lo < X < hi) for X ~ N(mu, sigma). Use +-Infinity for open tails. */
  function normalProb(lo, hi, mu, sigma) {
    return normalCdf((hi - mu) / sigma) - normalCdf((lo - mu) / sigma);
  }

  // Acklam's rational approximation + one Halley refinement step.
  function invNorm(p) {
    if (!(p > 0 && p < 1)) {
      if (p === 0) return -Infinity;
      if (p === 1) return Infinity;
      return NaN;
    }
    const a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02, 1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00];
    const b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02, 6.680131188771972e+01, -1.328068155288572e+01];
    const c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00, -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00];
    const d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00, 3.754408661907416e+00];
    const plow = 0.02425;
    let x;
    if (p < plow) {
      const q = Math.sqrt(-2 * Math.log(p));
      x = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) /
          ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);
    } else if (p <= 1 - plow) {
      const q = p - 0.5;
      const r = q * q;
      x = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q /
          (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);
    } else {
      const q = Math.sqrt(-2 * Math.log(1 - p));
      x = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) /
           ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);
    }
    const e = normalCdf(x) - p;
    const u = e * SQRT_2PI * Math.exp(x * x / 2);
    return x - u / (1 + x * u / 2);
  }

  /* ---------- gamma / discrete distributions ---------- */
  const LANCZOS = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
    -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];

  function logGamma(x) {
    if (x < 0.5) return Math.log(Math.PI / Math.abs(Math.sin(Math.PI * x))) - logGamma(1 - x);
    x -= 1;
    let a = LANCZOS[0];
    const t = x + 7.5;
    for (let i = 1; i < 9; i++) a += LANCZOS[i] / (x + i);
    return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(a);
  }

  function logChoose(n, k) { return logGamma(n + 1) - logGamma(k + 1) - logGamma(n - k + 1); }

  function binomPmf(k, n, p) {
    if (k < 0 || k > n || !Number.isInteger(k)) return 0;
    if (p === 0) return k === 0 ? 1 : 0;
    if (p === 1) return k === n ? 1 : 0;
    return Math.exp(logChoose(n, k) + k * Math.log(p) + (n - k) * Math.log(1 - p));
  }

  function binomCdf(k, n, p) {
    k = Math.floor(k);
    if (k < 0) return 0;
    if (k >= n) return 1;
    let s = 0;
    for (let i = 0; i <= k; i++) s += binomPmf(i, n, p);
    return Math.min(1, s);
  }

  function poissonPmf(k, lambda) {
    if (k < 0 || !Number.isInteger(k)) return 0;
    if (lambda === 0) return k === 0 ? 1 : 0;
    return Math.exp(-lambda + k * Math.log(lambda) - logGamma(k + 1));
  }

  function poissonCdf(k, lambda) {
    k = Math.floor(k);
    if (k < 0) return 0;
    let s = 0;
    for (let i = 0; i <= k; i++) s += poissonPmf(i, lambda);
    return Math.min(1, s);
  }

  /** Hypergeometric: N population, K successes in it, n draws. */
  function hypergeomPmf(k, N, K, n) {
    if (k < Math.max(0, n - (N - K)) || k > Math.min(n, K)) return 0;
    return Math.exp(logChoose(K, k) + logChoose(N - K, n - k) - logChoose(N, n));
  }

  /* ---------- descriptive ---------- */
  const sum = (xs) => xs.reduce((a, b) => a + b, 0);
  const mean = (xs) => sum(xs) / xs.length;
  function variance(xs, sample = true) {
    const m = mean(xs);
    return sum(xs.map((x) => (x - m) ** 2)) / (xs.length - (sample ? 1 : 0));
  }
  const sd = (xs, sample = true) => Math.sqrt(variance(xs, sample));

  /** Weighted mean / sd (grouped data). values = class marks, freqs = absolute frequencies. */
  function groupedStats(values, freqs, sample = true) {
    const n = sum(freqs);
    const m = sum(values.map((v, i) => v * freqs[i])) / n;
    const ss = sum(values.map((v, i) => freqs[i] * (v - m) ** 2));
    const s = Math.sqrt(ss / (n - (sample ? 1 : 0)));
    return { n, mean: m, sd: s, cv: s / m };
  }

  /** Least squares y = a + b x. Returns {a, b, r, r2, n}. */
  function linreg(xs, ys) {
    const n = xs.length;
    const mx = mean(xs);
    const my = mean(ys);
    let sxx = 0, syy = 0, sxy = 0;
    for (let i = 0; i < n; i++) {
      sxx += (xs[i] - mx) ** 2;
      syy += (ys[i] - my) ** 2;
      sxy += (xs[i] - mx) * (ys[i] - my);
    }
    const b = sxy / sxx;
    const a = my - b * mx;
    const r = sxy / Math.sqrt(sxx * syy);
    return { n, a, b, r, r2: r * r, mx, my };
  }

  /* ---------- critical values ---------- */
  // Two-sided t critical values, df = 1..30 (index 0 = df 1).
  const T_TABLE = {
    '0.90': [6.314, 2.920, 2.353, 2.132, 2.015, 1.943, 1.895, 1.860, 1.833, 1.812, 1.796, 1.782, 1.771, 1.761, 1.753, 1.746, 1.740, 1.734, 1.729, 1.725, 1.721, 1.717, 1.714, 1.711, 1.708, 1.706, 1.703, 1.701, 1.699, 1.697],
    '0.95': [12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101, 2.093, 2.086, 2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052, 2.048, 2.045, 2.042],
    '0.99': [63.657, 9.925, 5.841, 4.604, 4.032, 3.707, 3.499, 3.355, 3.250, 3.169, 3.106, 3.055, 3.012, 2.977, 2.947, 2.921, 2.898, 2.878, 2.861, 2.845, 2.831, 2.819, 2.807, 2.797, 2.787, 2.779, 2.771, 2.763, 2.756, 2.750],
  };
  // Table values for z as usually printed in textbooks (3 decimals).
  const Z_TABLE = { '0.90': 1.645, '0.95': 1.960, '0.99': 2.576 };

  function confKey(conf) { return (conf > 1 ? conf / 100 : conf).toFixed(2); }
  function zCrit(conf) { return Z_TABLE[confKey(conf)]; }
  function tCrit(conf, df) {
    const row = T_TABLE[confKey(conf)];
    if (!row || df < 1) return NaN;
    if (df > 30) return zCrit(conf);
    return row[df - 1];
  }

  return {
    erf, erfc, normalPdf, normalCdf, normalProb, invNorm,
    logGamma, logChoose, binomPmf, binomCdf, poissonPmf, poissonCdf, hypergeomPmf,
    sum, mean, variance, sd, groupedStats, linreg,
    T_TABLE, Z_TABLE, zCrit, tCrit,
  };
});
