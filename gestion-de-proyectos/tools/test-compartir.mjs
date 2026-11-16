// Tests for the shareable deliverable (compartir/).
// Run with: tools/test-compartir.sh
// Covers: data integrity, build output, privacy (no internal references), self-containment, mutation.
import { execFileSync } from 'node:child_process';
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import vm from 'node:vm';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const DATA_REL = 'tp/assets/canvas-data.js';
const TEMPLATE_REL = 'compartir/src/tp-cascada.template.html';
const OUT_REL = 'compartir/tp-cascada-canvas-y-partes.html';
const BUILD_REL = 'tools/build-compartir.sh';
const RENDER_REL = 'compartir/src/render.js';

let failed = 0;
let passed = 0;
function test(name, fn) {
  try { fn(); passed++; console.log('  ok   ' + name); }
  catch (e) { failed++; console.log('  FAIL ' + name + '\n       ' + String(e.message).split('\n').join('\n       ')); }
}
function assert(cond, msg) { if (!cond) throw new Error(msg); }

/* ── Data integrity (what a maintainer edits) ─────────────────────── */
const EXPECTED_BLOCKS = ['segmentos', 'pv', 'canales', 'relacion', 'ingresos', 'recursos', 'actividades', 'socios', 'costos'];
const OPTION_IDS = ['a', 'b', 'c', 'd'];
let data = null;
console.log('data: ' + DATA_REL);
test('canvas-data.js exists and loads in node (UMD)', () => {
  assert(existsSync(join(ROOT, DATA_REL)), DATA_REL + ' is missing');
  data = require(join(ROOT, DATA_REL));
  assert(data && typeof data === 'object', 'module did not export an object');
});
test('canvas-data.js also defines window.CANVAS_DATA in a browser-like context', () => {
  const src = readFileSync(join(ROOT, DATA_REL), 'utf8');
  const ctx = { self: {} };
  ctx.window = ctx.self;
  vm.runInNewContext(src, ctx);
  assert(ctx.self.CANVAS_DATA && ctx.self.CANVAS_DATA.options, 'CANVAS_DATA global not defined');
});
test('the four options exist with summary fields', () => {
  assert(data, 'no data');
  assert(JSON.stringify(Object.keys(data.options)) === JSON.stringify(OPTION_IDS), 'options must be a,b,c,d');
  OPTION_IDS.forEach((id) => {
    const o = data.options[id];
    ['name', 'idea', 'cliente', 'paga', 'borde', 'riesgo'].forEach((f) => assert(typeof o[f] === 'string' && o[f].length > 10, `option ${id}.${f} missing`));
  });
  assert(data.options.b.suggested === true, 'option b must be the suggested one');
  assert(OPTION_IDS.filter((id) => data.options[id].suggested).length === 1, 'exactly one option must be suggested');
});
test('every option fills all 9 blocks and has a 6-step flow', () => {
  assert(data, 'no data');
  assert(JSON.stringify(data.order.slice().sort()) === JSON.stringify(EXPECTED_BLOCKS.slice().sort()), 'order must list the 9 blocks');
  OPTION_IDS.forEach((id) => {
    EXPECTED_BLOCKS.forEach((b) => {
      const l = data.options[id].blocks[b];
      assert(Array.isArray(l) && l.length >= 1 && l.every((x) => typeof x === 'string' && x.trim()), `option ${id} block ${b} is empty`);
    });
    const f = data.options[id].flow;
    assert(Array.isArray(f) && f.length === 6 && f.every((r) => r.length === 3 && r.every((x) => x.trim())), `option ${id} flow must have 6 [sección, título, texto] rows`);
  });
  EXPECTED_BLOCKS.forEach((b) => {
    const d = data.blocks[b];
    assert(d && d.n >= 1 && d.n <= 9 && d.name && d.def && d.questions.length && d.types.length && d.src, `block definition ${b} incomplete`);
  });
});
test('comparison has one row per option; recommendation and value maps are present', () => {
  assert(data, 'no data');
  assert(data.comparison.length === 4 && data.comparison.every((r, i) => r.id === OPTION_IDS[i]), 'comparison rows must be a,b,c,d in order');
  data.comparison.forEach((r) => {
    ['segmento', 'plata', 'pregunta', 'conviene'].forEach((f) => assert(r[f], `comparison ${r.id}.${f} missing`));
    assert(['ok', 'mid', 'bad'].includes(r.trabajo.nivel) && r.trabajo.texto, `comparison ${r.id}.trabajo invalid`);
  });
  assert(data.recommendation && data.recommendation.titulo && data.recommendation.texto, 'recommendation missing');
  ['vecino', 'gcba'].forEach((k) => {
    const v = data.valueMaps[k];
    assert(v && v.who, `valueMaps.${k}.who missing`);
    ['tareas', 'frust', 'benef', 'pv', 'alivio', 'satis'].forEach((f) => assert(Array.isArray(v[f]) && v[f].length, `valueMaps.${k}.${f} empty`));
  });
});
test('data contains no internal file references', () => {
  const src = readFileSync(join(ROOT, DATA_REL), 'utf8');
  assert(!/(\.\.\/|raw\/|clases\/|\.pdf)/i.test(src), 'data must not point at local files');
  assert(!/<\/script/i.test(src), 'data must not contain </script (it gets inlined)');
});

/* ── Build ─────────────────────────────────────────────────────────── */
function build(rootDir) {
  execFileSync('bash', [join(rootDir, BUILD_REL)], { stdio: 'pipe' });
  return readFileSync(join(rootDir, OUT_REL), 'utf8');
}
let html = null;
console.log('build: ' + BUILD_REL);
test('template exists and carries the data marker exactly once', () => {
  assert(existsSync(join(ROOT, TEMPLATE_REL)), TEMPLATE_REL + ' is missing');
  const t = readFileSync(join(ROOT, TEMPLATE_REL), 'utf8');
  assert(t.split('<!--CANVAS_DATA-->').length === 2, 'template must contain <!--CANVAS_DATA--> exactly once');
});
test('build script produces the deliverable', () => {
  assert(existsSync(join(ROOT, BUILD_REL)), BUILD_REL + ' is missing');
  html = build(ROOT);
  assert(html.length > 10000, 'output suspiciously small');
  assert(!html.includes('<!--CANVAS_DATA-->'), 'marker was not replaced');
});

/* ── Output checks ─────────────────────────────────────────────────── */
function inlineScripts(h) {
  return [...h.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)].map((m) => m[1]);
}
console.log('output: ' + OUT_REL);
test('all four option ids and all 9 block names are in the inlined data', () => {
  assert(html, 'no build output');
  const scripts = inlineScripts(html);
  const ctx = { self: {} };
  ctx.window = ctx.self;
  ctx.document = undefined;
  let found = null;
  for (const s of scripts) {
    if (!s.includes('CANVAS_DATA')) continue;
    try { vm.runInNewContext(s, ctx); } catch (e) { /* page scripts need a DOM; the data script does not */ continue; }
    if (ctx.self.CANVAS_DATA) { found = ctx.self.CANVAS_DATA; break; }
  }
  assert(found, 'no inline script defines CANVAS_DATA');
  assert(JSON.stringify(Object.keys(found.options)) === JSON.stringify(OPTION_IDS), 'output data lacks options a–d');
  OPTION_IDS.forEach((id) => EXPECTED_BLOCKS.forEach((b) => {
    assert(found.options[id].blocks[b].length, `output data: option ${id} lacks ${b}`);
    assert(html.includes(found.blocks[b].name), `output lacks block name "${found.blocks[b].name}"`);
  }));
});
test('no internal/private terms', () => {
  assert(html, 'no build output');
  const bad = [
    [/(?<![a-z])lecci[oó]n(es)?/i, 'lección/lecciones'], [/clases\//i, 'clases/'], [/\braw\//i, 'raw/'], [/(^|[^a-z])tp\//i, 'tp/'],
    [/\bsuite\b/i, 'suite'], [/\bNOTES\b/i, 'NOTES'], [/\bagente\b/i, 'agente'], [/\bclaude\b/i, 'Claude'], [/\bengram\b/i, 'engram'],
    [/\bLEEME\b/i, 'LEEME'], [/mapa de conceptos/i, 'mapa de conceptos'], [/\/home\//, 'local path'], [/file:\/\//i, 'file:// URL'],
  ];
  const hits = bad.filter(([re]) => re.test(html)).map(([, n]) => n);
  assert(!hits.length, 'found: ' + hits.join(', '));
});
test('only https or #anchor links; no local src/href/@import', () => {
  assert(html, 'no build output');
  const refs = [...html.matchAll(/\b(?:href|src)\s*=\s*"([^"]*)"/gi)].map((m) => m[1]);
  const imports = [...html.matchAll(/@import\s+(?:url\()?["']?([^"')\s;]+)/gi)].map((m) => m[1]);
  const bad = refs.concat(imports).filter((r) => !(r.startsWith('https://') || r.startsWith('#')));
  assert(!bad.length, 'non-https references: ' + bad.join(', '));
});
test('no <script src>', () => {
  assert(html, 'no build output');
  assert(!/<script[^>]*\bsrc\s*=/i.test(html), 'external script tag found');
});
test('every inline script parses (node --check)', () => {
  assert(html, 'no build output');
  const dir = mkdtempSync(join(tmpdir(), 'chk-'));
  try {
    inlineScripts(html).forEach((s, i) => {
      const f = join(dir, `s${i}.js`);
      writeFileSync(f, s);
      try { execFileSync('node', ['--check', f], { stdio: 'pipe' }); }
      catch (e) { throw new Error(`inline script #${i} has a syntax error:\n${e.stderr}`); }
    });
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
test('single self-contained file stays small (< 200 KB)', () => {
  assert(html, 'no build output');
  assert(Buffer.byteLength(html) < 200 * 1024, 'output is ' + Buffer.byteLength(html) + ' bytes');
});

/* ── Mutation: editing the data must change the output ─────────────── */
test('editing canvas-data.js and rebuilding changes the output (temp copy)', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'mut-'));
  try {
    [DATA_REL, TEMPLATE_REL, RENDER_REL, BUILD_REL].forEach((rel) => {
      mkdirSync(dirname(join(tmp, rel)), { recursive: true });
      cpSync(join(ROOT, rel), join(tmp, rel));
    });
    const before = build(tmp);
    const p = join(tmp, DATA_REL);
    const src = readFileSync(p, 'utf8');
    const token = 'MUTATION-TOKEN-7431';
    const mutated = src.replace(/idea:\s*(['"`])/, (m, q) => m + token + ' ');
    assert(mutated !== src, 'could not apply the mutation (expected an `idea:` string in the data)');
    writeFileSync(p, mutated);
    const after = build(tmp);
    assert(after !== before && after.includes(token), 'output did not reflect the edit');
    assert(!before.includes(token), 'sanity: token leaked into the unmutated build');
  } finally { rmSync(tmp, { recursive: true, force: true }); }
});

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
