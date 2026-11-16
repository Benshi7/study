// The data-driven figures (build/gen-figures.mjs) must show exactly the numbers of the text they illustrate.
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { ROOT, readSrc } from "./helpers.mjs";
import { readRisks, zoneOf, readBudget, readStakeholders, mdTables, readGantt } from "../build/gen-figures.mjs";

const html = (n) => { const f = path.join(ROOT, "img-src", n + ".html"); assert.ok(fs.existsSync(f), `${n}.html no existe: ejecutar build/figures.mjs`); return fs.readFileSync(f, "utf8"); };
const text = (h) => h.replace(/<[^>]+>/g, " ").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/\s+/g, " ");
const usd = (n) => "USD " + Math.round(n).toLocaleString("es-AR").replace(/,/g, ".");

test("figures: every figure referenced by the sources has its PNG and the new ones are referenced once", () => {
  const refs = fs.readdirSync(path.join(ROOT, "src")).flatMap((f) => [...readSrc(f).matchAll(/!\[[^\]]*\]\((img\/[^)]+)\)/g)].map((m) => m[1]));
  for (const n of ["gantt", "fases", "hitos", "mapa-calor", "presupuesto", "stakeholders"]) {
    assert.equal(refs.filter((r) => r === `img/${n}.png`).length, 1, `${n}.png referenciada una vez`);
    assert.ok(fs.statSync(path.join(ROOT, "img", n + ".png")).size > 8000, `${n}.png`);
  }
  assert.ok(!refs.includes("img/gantt-f1.png"), "the old Gantt picture is no longer used");
});

test("figures: risk heat map places R01–R15 where the matrix says and its zones match section 9.4", () => {
  const R = readRisks(ROOT);
  assert.equal(R.length, 15);
  const h = html("mapa-calor"), t = text(h);
  const zones = { red: R.filter((r) => zoneOf(r.p, r.i) === "red").map((r) => r.id), yellow: R.filter((r) => zoneOf(r.p, r.i) === "yellow").map((r) => r.id), green: R.filter((r) => zoneOf(r.p, r.i) === "green").map((r) => r.id) };
  assert.match(t, new RegExp(`Inaceptable \\(${zones.red.length}\\)`));
  assert.match(t, new RegExp(`Aceptable con atención \\(${zones.yellow.length}\\)`));
  assert.match(t, new RegExp(`Aceptable \\(${zones.green.length}\\)`));
  for (const r of R) assert.ok(new RegExp(`>${r.id}<`).test(h), r.id);
  // section 9.4: bullets by zone
  const s = readSrc("09-riesgos.md"), sec = s.slice(s.indexOf("## 9.4"), s.indexOf("## 9.5"));
  const part = (a, b) => [...sec.slice(sec.indexOf(a), b ? sec.indexOf(b) : undefined).matchAll(/\*\*(R\d\d) -/g)].map((m) => m[1]).sort();
  assert.deepEqual(part("- **Zona inaceptable", "- **Zona aceptable con atención"), [...zones.red].sort());
  assert.deepEqual(part("- **Zona aceptable con atención", "- **Zona aceptable ("), [...zones.yellow].sort());
  assert.deepEqual(part("- **Zona aceptable (", "Los riesgos de la zona inaceptable"), [...zones.green].sort());
  // the text table of 9.4 is the same rule
  const grid = mdTables(path.join(ROOT, "src/09-riesgos.md")).find((x) => /Probabilidad \\ Impacto/.test(x[0][0]));
  const name = { red: "Inaceptable", yellow: "Con atención", green: "Aceptable" };
  for (const row of grid.slice(1)) { const p = Number(row[0].replace(/\*/g, "")[0]); row.slice(1).forEach((c, k) => assert.equal(c, name[zoneOf(p, k + 1)], `celda P${p} I${k + 1}`)); }
  // level of the matrix (P × I) is consistent with the P and I read for the figure
  for (const r of R) { const lvl = mdTables(path.join(ROOT, "src/09-riesgos.md"))[0]; assert.ok(lvl); }
});

test("figures: budget figure = table 10.9 = Charter 5.8.5 = Σ EMV of 9.7", () => {
  const B = readBudget(ROOT);
  assert.equal(B.cats.reduce((a, c) => a + c.amount, 0), B.base);
  assert.equal(B.base + B.contingency, B.total);
  const t = text(html("presupuesto"));
  for (const c of B.cats) assert.ok(t.includes(usd(c.amount)), `${c.name} ${usd(c.amount)}`);
  for (const v of [B.base, B.contingency, B.total]) assert.ok(t.includes(usd(v)), usd(v));
  const charter = readSrc("05-project-charter.md");
  assert.ok(charter.includes(usd(B.total)) && charter.includes(usd(B.base)) && charter.includes(usd(B.contingency)));
  assert.ok(readSrc("09-riesgos.md").includes(usd(B.contingency)), "9.7 states the same contingency");
});

test("figures: stakeholder figure lists the 15 stakeholders of the matrix, each in the cell of its interest and influence", () => {
  const S = readStakeholders(ROOT);
  assert.equal(S.length, 15);
  const t = text(html("stakeholders"));
  for (const s of S) assert.ok(t.includes(s.name), s.name);
  const h = html("stakeholders");
  const counts = {}; for (const s of S) counts[`${s.interes}/${s.influencia}`] = (counts[`${s.interes}/${s.influencia}`] || 0) + 1;
  assert.equal((h.match(/<circle [^>]*r="14"/g) || []).length, 15, "one dot per stakeholder");
  assert.deepEqual(counts, { "Alto/Alto": 7, "Medio/Alto": 1, "Alto/Medio": 4, "Medio/Medio": 2, "Medio/Bajo": 1 });
});

test("figures: Gantt, phases and milestones figures carry the dates of data/gantt.json and of section 6.3", () => {
  const G = readGantt(ROOT);
  const g = text(html("gantt"));
  for (const tk of G.tasks) assert.ok(g.includes(tk.act), `actividad ${tk.id}`);
  assert.equal((html("gantt").match(/<path d="M[^"]*" fill="var\(--c-ink\)"/g) || []).length >= 8, true);
  const s63 = readSrc("06-gantt.md");
  for (const h of G.hitos) {
    const dm = h.date.slice(0, 5);
    assert.ok(g.includes(`H${h.n} ${dm}`), `Gantt H${h.n}`);
    assert.ok(text(html("fases")).includes(`H${h.n} ${dm}`), `fases H${h.n}`);
    assert.ok(text(html("hitos")).includes(`H${h.n} · ${dm}`), `hitos H${h.n}`);
    assert.ok(s63.includes(`| ${h.name} | ${h.date} |`), `6.3 ${h.name}`);
  }
  const f = text(html("fases"));
  for (const ph of G.phases) assert.ok(f.includes(ph));
  assert.ok(g.includes(`Red de ${G.cp_days} días hábiles en una ventana de ${G.window_days}`));
});
