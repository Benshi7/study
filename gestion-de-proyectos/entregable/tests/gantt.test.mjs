// Tests for the corrected Gantt (dist/Gantt_corregido_TP_Cascada.xlsx, data/gantt.json) against the team's original Excel.
// The original stays untouched (sha256 test in docx.test.mjs). Everything is recomputed here in JS, independently of
// tools/gen-gantt-corregido.py, from the workbook cells.
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { ROOT, ORIG_DIR, readXlsx, readSrc } from "./helpers.mjs";

const ORIG = path.join(ORIG_DIR, "Gantt_y_Camino_Critico_Hitos_Anexo_Punto_6.xlsx");
const CORR = path.join(ROOT, "dist", "Gantt_corregido_TP_Cascada.xlsx");
const ROLES = new Set(["Project Manager", "Analistas funcionales", "Desarrolladores", "Especialistas en datos y GIS", "UX/UI", "QA y testing",
  "Seguridad informática", "Infraestructura/DevOps", "Documentación y capacitación", "Sponsor"]);
const HITO_ACT = [4, 10, 17, 23, 26, 32, 35, 40];

const pd = (s) => { const [d, m, y] = s.split("/").map(Number); return new Date(Date.UTC(y < 100 ? 2000 + y : y, m - 1, d)); };
const wd = (d) => d.getUTCDay() >= 1 && d.getUTCDay() <= 5;
const nextWd = (d) => { let x = new Date(d.getTime() + 864e5); while (!wd(x)) x = new Date(x.getTime() + 864e5); return x; };
const busy = (a, b) => { let n = 0; for (let d = a; d <= b; d = new Date(d.getTime() + 864e5)) if (wd(d)) n++; return n; };
const fmt4 = (d) => `${String(d.getUTCDate()).padStart(2, "0")}/${String(d.getUTCMonth() + 1).padStart(2, "0")}/${d.getUTCFullYear()}`;
// «a-b» = las actividades a y b (así calcula el CPM del equipo); «a, b» / «a,b» = las listadas
const parseDeps = (s) => {
  if (!s || s === "-") return [];
  const out = [];
  for (const p of s.split(/\s*,\s*/)) { const m = /^(\d+)-(\d+)$/.exec(p.trim()); if (m) out.push(Number(m[1]), Number(m[2])); else if (p.trim()) out.push(Number(p)); }
  return [...new Set(out)].sort((a, b) => a - b);
};
const sheet = (xl, name) => xl.find((s) => s.name.startsWith(name)).rows;
const taskRows = (rows) => rows.filter((r) => /^\d+$/.test(r[0]));

function load(file) {
  const xl = readXlsx(file);
  const tasks = taskRows(sheet(xl, "Cronograma")).map((r) => ({ id: Number(r[0]), fase: r[1], act: r[2], start: pd(r[3]), end: pd(r[4]), dur: Number(r[5]), depsText: r[6], deps: parseDeps(r[6]), resp: r[7] ?? "", ent: r[8] }));
  return { xl, tasks, byId: new Map(tasks.map((t) => [t.id, t])) };
}

function cpm(tasks) {
  const es = new Map(), ef = new Map();
  for (const t of [...tasks].sort((a, b) => a.id - b.id)) { es.set(t.id, Math.max(0, ...t.deps.map((p) => ef.get(p)))); ef.set(t.id, es.get(t.id) + t.dur); }
  const L = Math.max(...ef.values()), lf = new Map(), ls = new Map();
  for (const t of [...tasks].sort((a, b) => b.id - a.id)) {
    const succ = tasks.filter((s) => s.deps.includes(t.id));
    lf.set(t.id, succ.length ? Math.min(...succ.map((s) => ls.get(s.id))) : L);
    ls.set(t.id, lf.get(t.id) - t.dur);
  }
  return { L, slack: new Map(tasks.map((t) => [t.id, ls.get(t.id) - es.get(t.id)])) };
}

const O = () => load(ORIG), C = () => { assert.ok(fs.existsSync(CORR), "dist/Gantt_corregido_TP_Cascada.xlsx no existe: ejecutar tools/gen-gantt-corregido.py"); return load(CORR); };

test("gantt: the corrected workbook has 40 activities and every duration equals its working days", () => {
  const { tasks } = C();
  assert.equal(tasks.length, 40);
  for (const t of tasks) assert.equal(busy(t.start, t.end), t.dur, `actividad ${t.id}: duración distinta de los días hábiles entre inicio y fin`);
});

test("gantt: no activity starts before its predecessors end (the original had 7 such overlaps)", () => {
  const o = O(), c = C();
  const overlaps = (g) => g.tasks.filter((t) => t.deps.some((p) => t.start <= g.byId.get(p).end)).map((t) => t.id);
  assert.deepEqual(overlaps(o), [2, 3, 8, 9, 14, 15, 16], "the original overlaps listed in CAMBIOS");
  assert.deepEqual(overlaps(c), []);
});

test("gantt: CPM recomputed from durations and dependencies = 126 working days, 23 critical, same slacks as the team's sheet", () => {
  const c = C(), { L, slack } = cpm(c.tasks);
  assert.equal(L, 126);
  assert.equal([...slack.values()].filter((s) => s === 0).length, 23);
  const dep = taskRows(sheet(c.xl, "Dependencias"));
  assert.equal(dep.length, 40);
  for (const r of dep) {
    assert.equal(Number(r[5]), slack.get(Number(r[0])), `holgura de la actividad ${r[0]}`);
    assert.equal(r[6] === "SÍ", slack.get(Number(r[0])) === 0, `crítica ${r[0]}`);
  }
  // the CPM is the team's: identical to the original sheet
  const o = O(), { slack: so } = cpm(o.tasks);
  assert.deepEqual([...slack], [...so]);
});

test("gantt: the project ends on 30/09/2026 and 126 + 5 idle working days fill the 131-day window", () => {
  const { tasks } = C();
  const end = new Date(Math.max(...tasks.map((t) => t.end)));
  assert.equal(fmt4(end), "30/09/2026");
  assert.equal(fmt4(new Date(Math.min(...tasks.map((t) => t.start)))), "01/04/2026");
  const window = busy(pd("01/04/2026"), pd("30/09/2026"));
  assert.equal(window, 131);
  const g = JSON.parse(fs.readFileSync(path.join(ROOT, "data/gantt.json"), "utf8"));
  assert.equal(g.window_days - g.cp_days, g.idle_days);
  assert.equal(g.idle_days, 5);
});

test("gantt: the 8 hitos are the end dates of their activities, in every place of the document", () => {
  const c = C();
  const hitos = sheet(c.xl, "Hitos").filter((r) => r[0] && /^\d{2}\/\d{2}\/\d{4}$/.test(r[1])).slice(0, 8);
  assert.equal(hitos.length, 8);
  hitos.forEach((h, k) => assert.equal(h[1], fmt4(c.byId.get(HITO_ACT[k]).end), `hito ${k + 1}`));
  const dates = hitos.map((h) => h[1]);
  assert.deepEqual([...dates].sort((a, b) => pd(a) - pd(b)), dates, "hitos in chronological order");
  // 6.3 table and the Charter
  const g63 = readSrc("06-gantt.md");
  const rows = g63.split("\n").filter((l) => /^\| .* \| \d{2}\/\d{2}\/\d{4} \|/.test(l)).map((l) => l.split("|").map((x) => x.trim()));
  assert.deepEqual(rows.map((r) => r[2]), dates);
  assert.deepEqual(rows.map((r) => r[1]), hitos.map((h) => h[0]));
  const charter = readSrc("05-project-charter.md");
  const [d, m] = dates[0].split("/"); const months = ["", "enero", "febrero", "marzo", "abril"];
  assert.ok(charter.includes(`El Charter se aprueba el ${Number(d)} de ${months[Number(m)]} de 2026`), "Charter approval date = hito 1");
  // the annex sheet repeats the same 8 dates
  const annex = sheet(c.xl, "Anexo Punto 6").filter((r) => r[0] && /^\d{2}\/\d{2}\/\d{4}$/.test(r[1])).map((r) => r[1]);
  assert.deepEqual(annex, dates);
  // no academic dates or "current time" wording left in the sheets
  assert.ok(!c.xl.flatMap((s) => s.rows.flat()).some((v) => /14\/10\/2026|18\/11\/2026|Hitos acad/i.test(v)));
});

test("gantt: differences against the team's original are exactly the documented ones (dates, dependency notation, Responsable)", () => {
  const o = O(), c = C();
  for (let k = 0; k < 40; k++) {
    const a = o.tasks[k], b = c.tasks[k];
    for (const f of ["id", "fase", "act", "dur", "ent"]) assert.equal(b[f], a[f], `${f} de la actividad ${a.id} no debe cambiar`);
    assert.deepEqual(b.deps, a.deps, `las predecesoras de ${a.id} no cambian (solo la notación)`);
    assert.ok(/^(-|\d+(, \d+)*)$/.test(b.depsText), `notación explícita en ${a.id}: «${b.depsText}»`);
    assert.ok(ROLES.has(b.resp), `rol de ${a.id}: «${b.resp}»`);
    assert.equal(a.resp, "", "the original has no Responsable");
  }
  // changed dates are the ones in data/gantt.json
  const g = JSON.parse(fs.readFileSync(path.join(ROOT, "data/gantt.json"), "utf8"));
  const changed = c.tasks.filter((t, k) => +t.start !== +o.tasks[k].start || +t.end !== +o.tasks[k].end).map((t) => t.id);
  assert.deepEqual(changed, g.changes.filter((x) => x.campo === "Inicio / Fin").map((x) => x.id));
  // an activity that did not overlap and whose predecessors did not move keeps its original dates
  for (const t of c.tasks) if (!changed.includes(t.id)) assert.equal(+t.start, +o.byId.get(t.id).start);
  // the shift is minimal: a changed activity starts either the day after its last predecessor or on its original date
  for (const t of c.tasks) {
    const lastPred = t.deps.length ? new Date(Math.max(...t.deps.map((p) => c.byId.get(p).end))) : null;
    const earliest = lastPred ? nextWd(lastPred) : t.start;
    assert.equal(+t.start, Math.max(+earliest, +o.byId.get(t.id).start), `inicio mínimo de la actividad ${t.id}`);
  }
  // dependency sheet: same slacks / critical flags / durations, predecessors equal as sets
  const od = taskRows(sheet(o.xl, "Dependencias")), cd = taskRows(sheet(c.xl, "Dependencias"));
  od.forEach((r, k) => { for (const i of [0, 1, 2, 4, 5, 6]) assert.equal(cd[k][i], r[i]); assert.deepEqual(parseDeps(cd[k][3]), parseDeps(r[3])); });
  // hitos sheet: only the dates may change
  const oh = sheet(o.xl, "Hitos").filter((r) => r[0] && /^\d{2}\/\d{2}\/\d{4}$/.test(r[1])), ch = sheet(c.xl, "Hitos").filter((r) => r[0] && /^\d{2}\/\d{2}\/\d{4}$/.test(r[1]));
  oh.forEach((r, k) => { for (const i of [0, 2, 3]) assert.equal(ch[k][i], r[i]); });
  assert.deepEqual(oh.map((r, k) => (r[1] === ch[k][1] ? 0 : 1)), [1, 1, 1, 1, 1, 0, 0, 0], "hitos 1 to 5 move; 6 to 8 keep their dates");
});

test("gantt: data/gantt.json is consistent with the workbook and with the annex table of the document", () => {
  const c = C(), g = JSON.parse(fs.readFileSync(path.join(ROOT, "data/gantt.json"), "utf8"));
  assert.equal(g.tasks.length, 40);
  g.tasks.forEach((t, k) => {
    const x = c.tasks[k];
    assert.equal(t.id, x.id); assert.equal(t.deps_text, x.depsText); assert.equal(t.resp, x.resp);
    assert.equal(t.start, sheet(c.xl, "Cronograma").find((r) => Number(r[0]) === t.id)[3]);
  });
  const annex = readSrc("12-anexo-a.md");
  for (const t of g.tasks) assert.ok(annex.includes(`| ${t.id} | ${t.fase} | ${t.act} | ${t.start} | ${t.end} | ${t.dur} | ${t.deps_text} | ${t.resp} | ${t.ent} |`), `fila ${t.id} del anexo`);
});
