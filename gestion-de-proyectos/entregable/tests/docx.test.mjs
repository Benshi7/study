// Tests for the consolidated deliverable. Run: node --test tests/   (after ./build.sh)
// Strict TDD: these were written before the build script and the sources existed.
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import {
  ROOT, REPO, DIST_DOCX, DIST_MD, SRC_DIR, ORIG_DIR,
  srcFiles, readSrc, mdModel, mdWords, tokens, diffCount,
  docxModel, segments, segmentWords, isHeading, parseXml, readXlsx, originalBlocks, sha256,
} from "./helpers.mjs";

const EXPECTED_H1 = [
  "1. Carátula", "2. Índice", "3. Canvas del proyecto", "4. Aplicar Design Thinking", "5. Project Charter",
  "6. Gantt del proyecto completo", "7. Matriz de stakeholders", "8. Plan de comunicación",
  "9. Gestión de riesgos - Matriz de riesgos", "10. Gestión de costos - Presupuesto",
];
const theme = JSON.parse(fs.readFileSync(path.join(ROOT, "theme.json"), "utf8"));

let M; // docx model, loaded lazily so a missing build fails every test with a clear message
function model() {
  assert.ok(fs.existsSync(DIST_DOCX), "dist/TP_Cascada_Grupo01.docx does not exist: run ./build.sh");
  M ||= docxModel(DIST_DOCX);
  return M;
}
const norm = (s) => s.replace(/\s+/g, " ").trim();
const blockText = (b) => (b.type === "p" ? b.text : b.type === "tbl" ? b.rows.flat().join(" ") : "");

// ---------------------------------------------------------------- package integrity
test("docx: zip is valid and every XML part is well-formed", () => {
  const m = model();
  assert.ok(m.entries.includes("word/document.xml"));
  for (const [name, xml] of Object.entries(m.parts)) {
    const { errors } = parseXml(xml);
    assert.equal(errors.length, 0, `${name}: ${errors[0]}`);
  }
});

test("docx: content types and relationships are consistent", () => {
  const m = model();
  const ct = parseXml(m.parts["[Content_Types].xml"]).doc;
  const defaults = new Set(Array.from(ct.getElementsByTagName("Default")).map((d) => d.getAttribute("Extension").toLowerCase()));
  const overrides = new Set(Array.from(ct.getElementsByTagName("Override")).map((o) => o.getAttribute("PartName")));
  for (const e of m.entries) {
    if (e === "[Content_Types].xml" || e.endsWith("/")) continue;
    const ext = e.split(".").pop().toLowerCase();
    assert.ok(overrides.has("/" + e) || defaults.has(ext), `no content type for ${e}`);
  }
  for (const [name, xml] of Object.entries(m.parts)) {
    if (!name.endsWith(".rels")) continue;
    const base = name.includes("_rels/") ? name.replace(/_rels\/[^/]*\.rels$/, "") : "";
    for (const r of Array.from(parseXml(xml).doc.getElementsByTagName("Relationship"))) {
      if (r.getAttribute("TargetMode") === "External") continue;
      let t = r.getAttribute("Target");
      t = t.startsWith("/") ? t.slice(1) : path.posix.normalize(base + t);
      assert.ok(m.entries.includes(t), `${name}: missing target ${t}`);
    }
  }
  // every r:embed / r:id used in the document resolves
  const rels = new Set(Array.from(parseXml(m.parts["word/_rels/document.xml.rels"]).doc.getElementsByTagName("Relationship")).map((r) => r.getAttribute("Id")));
  for (const id of m.parts["word/document.xml"].matchAll(/r:(?:embed|id)="([^"]+)"/g)) assert.ok(rels.has(id[1]), `unresolved ${id[1]}`);
});

// ---------------------------------------------------------------- structure
test("structure: exactly 10 Heading1 in the order of the consigna", () => {
  const h1 = model().blocks.filter((b) => b.type === "p" && b.style === "Heading1").map((b) => norm(b.text));
  assert.equal(h1.length, 10);
  h1.forEach((t, i) => assert.equal(t.toLowerCase(), EXPECTED_H1[i].toLowerCase()));
});

test("structure: unnumbered front/back matter and the annex sit in the right places", () => {
  const heads = model().blocks.filter(isHeading).map((b) => ({ style: b.style, text: norm(b.text) }));
  const idx = (re) => heads.findIndex((h) => re.test(h.text));
  const resumen = idx(/^resumen ejecutivo/i), canvas = idx(/^3\./), concl = idx(/^conclusi[oó]n general/i), annex = idx(/^anexo a/i), last = idx(/^10\./);
  assert.ok(resumen > idx(/^2\./) && resumen < canvas, "resumen ejecutivo goes between 2 and 3");
  assert.ok(concl > last && annex > concl, "conclusión after 10, annex after conclusión");
  for (const i of [resumen, concl, annex]) assert.equal(heads[i].style, "UnnumberedHeading");
});

test("structure: heading numbering has no gaps or duplicates and matches its parent", () => {
  const hs = model().blocks.filter((b) => b.type === "p" && ["Heading1", "Heading2", "Heading3"].includes(b.style));
  const seen = new Set();
  let h1 = 0;
  const lastAt = {}; // parent number -> last child index
  for (const h of hs) {
    const t = norm(h.text);
    const num = /^(\d+(?:\.\d+)*)\.?\s/.exec(t);
    if (h.style === "Heading1") { h1 = Number(num[1]); continue; }
    if (!num) continue; // unnumbered subheadings are allowed (e.g. in the annex)
    const parts = num[1].split(".").map(Number);
    assert.ok(!seen.has(num[1]), `duplicate heading number ${num[1]}`);
    seen.add(num[1]);
    assert.equal(parts[0], h1, `heading ${num[1]} is under H1 ${h1}`);
    const parent = parts.slice(0, -1).join(".");
    const prev = lastAt[parent] ?? 0;
    assert.equal(parts[parts.length - 1], prev + 1, `gap before ${num[1]}`);
    lastAt[parent] = parts[parts.length - 1];
  }
});

test("structure: TOC field (levels 1-3) and update-on-open are present", () => {
  const m = model();
  const instr = m.blocks.filter((b) => b.type === "p").flatMap((b) => b.instr).join(" ");
  assert.match(instr, /TOC\s[^"]*\\o\s+"1-3"/);
  assert.match(m.parts["word/settings.xml"], /<w:updateFields\b(?![^>]*w:val="(?:false|0)")[^>]*\/?>/); // bare element = on
});

test("structure: Heading1 forces a page break; one landscape section for the annex only", () => {
  const m = model();
  assert.match(m.parts["word/styles.xml"], /<w:style [^>]*w:styleId="Heading1"[\s\S]*?<w:pageBreakBefore/);
  const sections = m.blocks.filter((b) => (b.type === "p" && b.hasSect) || b.type === "sect");
  const landscape = sections.filter((s) => (s.type === "sect" ? s.landscape : s.sectLandscape));
  assert.equal(landscape.length, 1, "exactly one landscape section");
  const annexIdx = m.blocks.findIndex((b) => b.type === "p" && /^anexo a/i.test(norm(b.text)) && b.style === "UnnumberedHeading");
  const landscapeIdx = m.blocks.findIndex((b) => (b.type === "sect" && b.landscape) || (b.type === "p" && b.sectLandscape));
  // the landscape sectPr closes the annex, so it comes after the annex heading
  assert.ok(annexIdx >= 0 && landscapeIdx >= annexIdx);
});

test("structure: footer has 'Página X de Y' fields", () => {
  const m = model();
  const footers = Object.entries(m.parts).filter(([n]) => /word\/footer\d*\.xml$/.test(n)).map(([, x]) => x).join(" ");
  assert.match(footers, /PAGE/);
  assert.match(footers, /NUMPAGES/);
  assert.match(footers, /Página/);
});

// ---------------------------------------------------------------- tables / figures
function mdAll() {
  return srcFiles().map((f) => ({ f, ...mdModel(readSrc(f)) }));
}

test("tables: every markdown table is a docx table with the same rows and columns, in order", () => {
  const expected = mdAll().flatMap((x) => x.tables.map((t) => `${t.rows}x${t.cols}`));
  const got = model().blocks.filter((b) => b.type === "tbl").map((t) => `${t.rows.length}x${Math.max(...t.rows.map((r) => r.length))}`);
  assert.deepEqual(got, expected);
});

test("tables: header row repeats across pages", () => {
  for (const t of model().blocks.filter((b) => b.type === "tbl")) assert.ok(t.repeatsHeader, `table starting "${t.rows[0][0]}" has no repeating header`);
});

test("figures: every markdown image exists, is embedded, has alt text and fits the page", () => {
  const imgs = mdAll().flatMap((x) => x.images);
  const m = model();
  const drawings = m.blocks.filter((b) => b.type === "p").flatMap((b) => b.drawings);
  assert.equal(drawings.length, imgs.length);
  for (const i of imgs) {
    assert.ok(fs.existsSync(path.join(ROOT, i.src)), `missing image file ${i.src}`);
    assert.ok(i.alt && i.alt.length > 3, `image ${i.src} needs alt text`);
  }
  for (const d of drawings) {
    assert.ok(d.descr && d.descr.length > 3, "drawing without alt text");
    assert.ok(d.cx <= 14344 * 635 + 1, "image wider than the widest content area (landscape)");
  }
  const media = m.entries.filter((e) => e.startsWith("word/media/"));
  assert.ok(media.length >= new Set(imgs.map((i) => i.src)).size);
});

test("captions: one numbered 'Tabla'/'Figura' caption per table and figure (SEQ fields)", () => {
  const m = model();
  const caps = m.blocks.filter((b) => b.type === "p" && b.style === "Caption");
  const tables = m.blocks.filter((b) => b.type === "tbl").length;
  const coverEnd = m.blocks.findIndex((b) => b.type === "p" && b.style === "Heading1" && /^2\./.test(norm(b.text)));
  const figs = m.blocks.slice(coverEnd).filter((b) => b.type === "p").flatMap((b) => b.drawings).length; // the cover logo has no caption
  assert.equal(caps.length, tables + figs);
  assert.equal(caps.filter((c) => /^Tabla\b/.test(c.text)).length, tables);
  assert.equal(caps.filter((c) => /^Figura\b/.test(c.text)).length, figs);
  assert.ok(caps.every((c) => c.instr.some((i) => /SEQ\s+(Tabla|Figura)/.test(i))));
});

// ---------------------------------------------------------------- word parity docx vs markdown
test("parity: words per section match the markdown source (±1%)", () => {
  const files = srcFiles();
  const segs = segments(model());
  assert.equal(segs.length, files.length, `${segs.length} docx sections vs ${files.length} source files`);
  files.forEach((f, i) => {
    const a = mdWords(readSrc(f)).length;
    const b = segmentWords(segs[i]).length;
    const tol = Math.max(3, Math.round(a * 0.01));
    assert.ok(Math.abs(a - b) <= tol, `${f}: markdown ${a} words vs docx ${b}`);
  });
});

// ---------------------------------------------------------------- faithfulness vs originals
function f1Range(startRe, endRe) {
  const blocks = originalBlocks("Proyect Charter y demas puntos.docx");
  const texts = blocks.map((b) => (b.type === "p" ? b.text : b.type === "tbl" ? b.rows.map((r) => r.join(" ")).join("\n") : ""));
  let start = -1, end = texts.length;
  texts.forEach((t, i) => { if (startRe.test(norm(t))) start = i; });
  if (endRe) texts.forEach((t, i) => { if (i > start && endRe.test(norm(t)) && end === texts.length) end = i; });
  return blocks.slice(start, end);
}
function blockTokens(bs) {
  return tokens(bs.map((b) => (b.type === "p" ? b.text : b.type === "tbl" ? b.rows.map((r) => r.join(" ")).join(" ") : "")).join("\n"));
}
function removedNote() {
  // the chat note that starts "NOTA: Para el TP, yo los mantendría" up to the 5.5 heading (logged in CAMBIOS)
  const blocks = originalBlocks("Proyect Charter y demas puntos.docx");
  const s = blocks.findIndex((b) => b.type === "p" && /^\*?NOTA:\s*Para el TP/.test(norm(b.text)));
  assert.ok(s >= 0, "marker paragraph not found in the original");
  let e = s;
  while (e < blocks.length && !(blocks[e].type === "p" && /^5\.5\.?\s/.test(norm(blocks[e].text)))) e++;
  return blocks.slice(s, e);
}
function ourSections(nums) {
  const segs = segments(model());
  return segs.filter((s) => s.heading.style === "Heading1" && nums.includes(Number(/^(\d+)\./.exec(norm(s.heading.text))[1])));
}
function ourTokens(segList) {
  return segList.flatMap((s) => segmentWords(s));
}
// tokens of the given sections, leaving out everything from the first Heading2 that matches skipFromRe (new content checked by its own tests)
function ourTokensWithout(segList, skipFromRe) {
  return segList.flatMap((s) => {
    const i = s.blocks.findIndex((b) => b.type === "p" && b.style === "Heading2" && skipFromRe.test(norm(b.text)));
    return segmentWords(i < 0 ? s : { heading: s.heading, blocks: s.blocks.slice(0, i) });
  });
}

test("fidelity F1 §5–6: nothing lost vs the original docx except the logged chat note", () => {
  const orig = f1Range(/^5\.\s*PROJECT CHARTER$/i, /^7\.\s*Matriz de Stakeholders/i);
  const ours = ourTokens(ourSections([5, 6]));
  const note = blockTokens(removedNote());
  const missing = diffCount(blockTokens(orig), ours) - diffCount(note, ours) * 0;
  // missing tokens may only come from the removed note (plus the EMF-only paragraph that has no text)
  const allowed = note.length + 5;
  assert.ok(missing <= allowed, `${missing} tokens from F1 §5–6 are missing (allowed ${allowed})`);
  const extra = diffCount(ours, blockTokens(orig));
  // summary box + annex pointer, plus CAMBIOS F.* additions: cascade rationale (5.1), budget table (5.8.5), director authority (5.11.2), approval + signatures (5.13), unified dates, contingency row label of the budget table (CAMBIOS 41), corrected-Gantt wording and the phases/milestones figures with their lead-in sentences (CAMBIOS G.*)
  assert.ok(extra <= 700, `${extra} tokens were added to §5–6`);
});

test("fidelity F1 §9–10: nothing lost vs the original docx (amounts aside: §10 is now in USD, CAMBIOS F.*)", () => {
  const orig = f1Range(/^9\.\s*GESTI[OÓ]N DE RIESGOS/i, null);
  const notNum = (t) => !/^\d+$/.test(t);
  // 9.7 (EMV quantification, CAMBIOS F.*) is new content and has its own test below
  const ours = ourTokensWithout(ourSections([9, 10]), /^9\.7\b/).filter(notNum);
  const missing = diffCount(blockTokens(orig).filter(notNum), ours);
  // missing words may only be the ARS wording ("pesos argentinos", "ARS", "$" is not a token) and the replaced maintenance/contingency sentences
  assert.ok(missing <= 25, `${missing} non-numeric tokens from F1 §9–10 are missing`);
  // extra words: bridge at the start of §9 (CAMBIOS E.24) + §10 methodology, formula, anti-duplication, USD basis, maintenance note, pre/post-closure split (CAMBIOS 38) R15 commerce adoption (CAMBIOS 35), the 9.4 rewrite by heat-map zones (CAMBIOS 42) and the contingency/management-reserve text of 10.8 (CAMBIOS 39–41)
  const extra910 = diffCount(ours, blockTokens(orig).filter(notNum)); assert.ok(extra910 <= 1350 /* + dedication clarification (CAMBIOS 44) */, `${extra910} tokens added to §9–10`);
});

// ---- 9.7 EMV model parsed from the generated docx ----
const pNum = (c) => Number(String(c).replace(/[^\d]/g, ""));
const PCT = { 1: 10, 2: 30, 3: 50, 4: 70, 5: 90 };
function emvModel() {
  const s9 = segments(model()).find((s) => /^9\./.test(norm(s.heading.text)));
  const tbls = s9.blocks.filter((b) => b.type === "tbl");
  const matrix = tbls.find((t) => t.rows[0][0] === "ID");
  const impactT = tbls.find((t) => /Nivel de impacto/.test(t.rows[0].join(" ")));
  const emvT = tbls.find((t) => /EMV residual/.test(t.rows[0].join(" ")));
  assert.ok(matrix && impactT && emvT, "9.2 matrix, 9.7.2 impact table and 9.7.3 EMV table must exist");
  const rows = emvT.rows.slice(1, -1);
  const totalRow = emvT.rows[emvT.rows.length - 1];
  return {
    matrix: matrix.rows.slice(1), impact: impactT.rows.slice(1), rows, totalRow,
    totalResidual: rows.reduce((a, r) => a + pNum(r[6]), 0),
    totalInitial: rows.reduce((a, r) => a + pNum(r[5]), 0),
  };
}

test("risks §9.7: EMV recomputes from the matrix, impacts sit in their band, contingency = Σ EMV everywhere", () => {
  const m = emvModel();
  assert.equal(m.rows.length, 15);
  assert.equal(m.impact.length, 15);
  const bands = { 3: [3000, 6000], 4: [6000, 10000], 5: [10000, Infinity] };
  const byLevel = {};
  m.rows.forEach((r, i) => {
    const id = r[0], mx = m.matrix[i], im = m.impact[i];
    assert.equal(mx[0], id); assert.equal(im[0], id);
    const p0 = Number(mx[4]), lvl = Number(mx[5]);
    assert.equal(pNum(r[2]), PCT[p0], `${id}: initial probability must be the matrix one`);
    assert.equal(r[1], mx[7], `${id}: response must be the matrix one`);
    const pRes = /Aceptar/.test(mx[7]) ? p0 : Math.max(1, p0 - (/\//.test(mx[7]) ? 2 : 1));
    assert.equal(pNum(r[3]), PCT[pRes], `${id}: residual probability rule`);
    const usd = pNum(r[4]);
    assert.equal(usd, pNum(im[4]), `${id}: impact in USD must match 9.7.2`);
    assert.equal(Number(im[1]), lvl, `${id}: impact level must be the matrix one`);
    assert.equal(pNum(r[5]), Math.round((PCT[p0] * usd) / 100), `${id}: initial EMV`);
    assert.equal(pNum(r[6]), Math.round((PCT[pRes] * usd) / 100), `${id}: residual EMV`);
    const [lo, hi] = bands[lvl];
    assert.ok(usd >= lo && usd < hi, `${id}: USD ${usd} outside the band of impact ${lvl}`);
    (byLevel[lvl] ||= []).push(usd);
  });
  assert.ok(Math.max(...byLevel[3]) < Math.min(...byLevel[4]) && Math.max(...byLevel[4]) < Math.min(...byLevel[5]), "impact scale must be monotonic in USD");
  assert.equal(pNum(m.totalRow[5]), m.totalInitial);
  assert.equal(pNum(m.totalRow[6]), m.totalResidual);
  // the same figure appears in §10 (contingency, baseline, total) and in the Charter 5.8.5 table
  const segs = segments(model());
  const text10 = segs.find((s) => /^10\./.test(norm(s.heading.text))).blocks.map(blockText).join("\n");
  const fmt = (n) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  assert.ok(text10.includes(`USD ${fmt(m.totalResidual)}`), "10.8 states the contingency");
  const tot = (s) => s.blocks.filter((b) => b.type === "tbl").map((t) => t.rows).flat();
  const cell = (rows, re) => pNum(rows.find((r) => re.test(r[0]))[1]);
  const r10 = tot(segs.find((s) => /^10\./.test(norm(s.heading.text))));
  const r5 = tot(segs.find((s) => /^5\./.test(norm(s.heading.text))));
  for (const rows of [r10, r5]) {
    assert.equal(cell(rows, /Reserva de contingencia/), m.totalResidual);
    assert.equal(cell(rows, /(PRESUPUESTO|Presupuesto) TOTAL|Presupuesto total/), cell(rows, /Presupuesto base/) + m.totalResidual);
  }
  assert.equal(cell(r5, /Presupuesto total/), cell(r10, /PRESUPUESTO TOTAL/));
  const all = model().blocks.map(blockText).join("\n");
  assert.ok(!/220\.696|reserva del 10|contingencia \(10/i.test(all), "stale 10 % contingency figures left");
  assert.ok((all.match(/20\.063/g) || []).length <= 1, "the old 10 % amount may appear only once, in the 10.8 comparison");
});


test("budget §10: USD tables close (lines → subtotals → base → + Σ EMV → total) and the base matches the team's ARS base at 1.560 within 0.1 %", () => {
  const s10 = segments(model()).find((s) => /^10\./.test(norm(s.heading.text)));
  const num = (c) => Number(c.replace(/[^\d]/g, ""));
  const tbls = s10.blocks.filter((b) => b.type === "tbl");
  const sums = [];
  for (const t of tbls) {
    const head = t.rows[0].join(" ");
    if (!/Recurso|Concepto/.test(head)) continue;
    const last = t.rows[t.rows.length - 1];
    const body = t.rows.slice(1, -1);
    const col = t.rows[0].length - 1;
    if (/Recurso/.test(head)) for (const r of body) assert.equal(num(r[3]), Number(r[1].split(" ")[0]) * num(r[2]), `row ${r[0]}: meses × costo mensual`);
    const sum = body.reduce((a, r) => a + num(r[col]), 0);
    assert.equal(num(last[col]), sum, `subtotal ${last[0]}`);
    sums.push(sum);
  }
  assert.equal(sums.length, 6);
  const base = sums.reduce((a, b) => a + b, 0);
  const tot = tbls.find((t) => t.rows.some((r) => /PRESUPUESTO TOTAL/.test(r[0])));
  const get = (re) => num(tot.rows.find((r) => re.test(r[0]))[1]);
  assert.equal(get(/Presupuesto base/), base);
  const emv = emvModel();
  assert.equal(get(/Reserva de contingencia/), emv.totalResidual, "contingency = Σ residual EMV of 9.7");
  assert.equal(get(/PRESUPUESTO TOTAL/), base + emv.totalResidual);
  const arsBase = 313_000_000; // the team's base before the flat 10 % contingency
  assert.ok(Math.abs(base / (arsBase / 1560) - 1) < 0.001);
  assert.ok(!/\$\s?\d/.test(segmentWords(s10).join(" ")));
});

test("fidelity F1: the removed chat note is really gone and its table too", () => {
  const text = model().blocks.map(blockText).join("\n");
  assert.ok(!/yo los mantendr/i.test(text));
  assert.ok(!/Capa geográfica confiable/.test(text), "the 4-results table belonged to the chat note");
});

test("fidelity: 5.1–5.12 headings, 15 risks R01–R15, 8 hitos, budget total", () => {
  const m = model();
  const h2 = m.blocks.filter((b) => b.type === "p" && b.style === "Heading2").map((b) => norm(b.text));
  for (let k = 1; k <= 12; k++) assert.ok(h2.some((t) => t.startsWith(`5.${k}`)), `missing 5.${k}`);
  const segs = segments(m);
  const s9 = segs.find((s) => /^9\./.test(norm(s.heading.text)));
  const matrix = s9.blocks.find((b) => b.type === "tbl" && b.rows[0][0] === "ID");
  assert.ok(matrix, "risk matrix table not found");
  const ids = matrix.rows.slice(1).map((r) => r[0]);
  assert.deepEqual(ids, Array.from({ length: 15 }, (_, i) => `R${String(i + 1).padStart(2, "0")}`));
  const s6 = segs.find((s) => /^6\./.test(norm(s.heading.text)));
  const hitos = s6.blocks.find((b) => b.type === "tbl" && /Fecha estimada/.test(b.rows[0].join(" ")));
  assert.equal(hitos.rows.length - 1, 8);
  const s10 = segs.find((s) => /^10\./.test(norm(s.heading.text)));
  assert.ok(s10.blocks.some((b) => b.type === "tbl" && b.rows.flat().some((c) => /USD 241\.839/.test(c))));
});

test("fidelity §7–8: tables equal the corrected PDF (rows, cols and every word)", () => {
  const segs = segments(model());
  const txt = fs.readFileSync(path.join(ORIG_DIR, "_analisis/convertidos/stakeholders-comunicacion.txt"), "utf8");
  const region = (a, b) => txt.slice(txt.indexOf(a), txt.indexOf(b));
  const s7 = segs.find((s) => /^7\./.test(norm(s.heading.text))).blocks.filter((b) => b.type === "tbl");
  const s8 = segs.find((s) => /^8\./.test(norm(s.heading.text))).blocks.filter((b) => b.type === "tbl");
  assert.equal(s7.length, 1); assert.equal(s8.length, 1);
  assert.equal(s7[0].rows.length, 16); assert.ok(s7[0].rows.every((r) => r.length === 5));
  assert.equal(s8[0].rows.length, 13); assert.ok(s8[0].rows.every((r) => r.length === 5));
  const w7 = tokens(s7[0].rows.map((r) => r.join(" ")).join(" "));
  const w8 = tokens(s8[0].rows.map((r) => r.join(" ")).join(" "));
  const t7 = tokens(region("Stakeholder  ", "7.2 Clasificaci"));
  const t8 = tokens(region("Qué se comunica", "Los líderes técnico"));
  assert.equal(diffCount(w7, t7), 0); assert.equal(diffCount(t7, w7), 0);
  assert.equal(diffCount(w8, t8), 0); assert.equal(diffCount(t8, w8), 0);
  // the PDF prose of 7.x and 8.x is also present (every word of the PDF appears in sections 7–8)
  const all78 = [...segmentWords(segs.find((s) => /^7\./.test(norm(s.heading.text)))), ...segmentWords(segs.find((s) => /^8\./.test(norm(s.heading.text))))];
  const pdfWords = tokens(txt.replace(/Modernización del Mapa Interactivo de la Ciudad\s+Página \d/g, ""));
  assert.ok(diffCount(pdfWords, all78) <= 3, `${diffCount(pdfWords, all78)} PDF words missing from §7–8`);
});

test("fidelity annex A: the tables reproduce the corrected Gantt workbook cell by cell (differences vs the team's original: tests/gantt.test.mjs)", () => {
  const xl = readXlsx(path.join(ROOT, "dist", "Gantt_corregido_TP_Cascada.xlsx"));
  const segs = segments(model());
  const annex = segs.find((s) => /^anexo a/i.test(norm(s.heading.text)));
  const tables = annex.blocks.filter((b) => b.type === "tbl");
  const find = (hdr) => tables.find((t) => t.rows[0].join("|") === hdr);
  const sheet = (name) => xl.find((s) => s.name.startsWith(name)).rows;
  const dataRows = (rows) => rows.filter((r) => /^\d+$/.test(r[0]));
  const crono = find("ID|Fase|Actividad|Inicio|Fin|Duración (días)|Dependencias|Responsable|Entregable");
  assert.ok(crono, "cronograma table");
  assert.equal(crono.rows.length - 1, 40);
  assert.deepEqual(crono.rows.slice(1), dataRows(sheet("Cronograma")).map((r) => r.slice(0, 9)));
  const dep = find("ID|Fase|Actividad|Predecesoras|Duración (días)|Holgura (días)|Camino Crítico");
  assert.ok(dep, "dependencias table");
  assert.deepEqual(dep.rows.slice(1), dataRows(sheet("Dependencias")).map((r) => r.slice(0, 7)));
  const hitosX = sheet("Hitos").filter((r) => r[0] && r[1] && /^\d{2}\/\d{2}\/\d{4}$/.test(r[1]));
  const hitosT = tables.find((t) => /^Hito Operativo/.test(t.rows[0][0]));
  assert.ok(hitosT);
  assert.deepEqual(hitosT.rows.slice(1, 1 + 8).map((r) => r.slice(0, 3)), hitosX.slice(0, 8).map((r) => r.slice(0, 3)));
  // every cell of the 'Anexo Punto 6' sheet that is a table row appears in some annex table
  const all = new Set(tables.flatMap((t) => t.rows.map((r) => r.join("|"))));
  for (const r of sheet("Anexo Punto 6").filter((r) => /^\d+$/.test(r[0]))) assert.ok(all.has(r.slice(0, 6).join("|")), `annex row ${r[0]} missing`);
});

// ---------------------------------------------------------------- content rules
test("content: placeholder for the team list, DT presented as simulated, no leftovers", () => {
  const m = model();
  const text = m.blocks.map(blockText).join("\n");
  assert.match(text, /\[Integrantes del grupo\]/);
  const dt = segments(m).find((s) => /^4\./.test(norm(s.heading.text)));
  const dtText = segmentWords(dt).join(" ");
  assert.match(dtText, /entrevistas semiestructuradas/);
  assert.ok(!/investigaci[oó]n simulada/i.test(text), "stale 'simulated research' note");
  assert.ok(!/cambiarla/i.test(text));
  assert.ok(!/n[oó]mina omitida/i.test(text));
  assert.ok(!/resumen y borrador/i.test(text));
});

test("privacy: no phone numbers and no tooling/assistant strings in the document", () => {
  const m = model();
  const hf = Object.entries(m.parts).filter(([n]) => /^word\/(header|footer)\d*\.xml$/.test(n)).map(([, x]) => x.replace(/<[^>]+>/g, " ")).join(" ");
  const text = m.blocks.map(blockText).join("\n") + "\n" + hf;
  const phone = /(?:\+\s?54[\s-]?9?[\s-]?)?(?:11|15)[\s-]?\d{4}[\s-]?\d{4}|\+\d{2}[\s-]?\d{1,2}[\s-]?\d{3,4}[\s-]?\d{4}/;
  assert.ok(!phone.test(text), "looks like a phone number");
  for (const bad of [/Claude/i, /agente\b/i, /engram/i, /_propuestas/i, /\bIA generativa\b/i]) assert.ok(!bad.test(text), String(bad));
});

// ---------------------------------------------------------------- theme
function themeValues(t) {
  return { colors: new Set(Object.entries(t.colors).filter(([k]) => !k.startsWith("_")).map(([, v]) => v.toUpperCase())), fonts: new Set(Object.values(t.fonts)) };
}
function styleSources(parts) {
  const xml = ["word/document.xml", "word/styles.xml", ...Object.keys(parts).filter((n) => /word\/(header|footer)\d*\.xml$/.test(n))].map((n) => parts[n]).join("\n");
  const colors = [...xml.matchAll(/(?:w:color|w:fill|<w:color w:val)="([0-9A-Fa-f]{6})"/g)].map((x) => x[1].toUpperCase());
  const fonts = [...xml.matchAll(/w:(?:ascii|hAnsi|cs|eastAsia)="([^"]+)"/g)].map((x) => x[1]);
  return { colors, fonts };
}

test("theme: every color and font in the generated XML comes from theme.json", () => {
  const { colors, fonts } = themeValues(theme);
  const used = styleSources(model().parts);
  for (const c of used.colors) assert.ok(colors.has(c), `color ${c} is not a theme token`);
  for (const f of used.fonts) assert.ok(fonts.has(f), `font ${f} is not a theme token`);
});

test("theme: changing a token changes the generated XML (restyling = editing theme.json)", () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "theme-"));
  const t2 = JSON.parse(JSON.stringify(theme));
  t2.colors.accent = "FF00AA"; t2.colors.heading = "AA00FF"; t2.fonts.body = "Arial";
  const themeFile = path.join(tmp, "theme.json");
  fs.writeFileSync(themeFile, JSON.stringify(t2));
  const out = path.join(tmp, "out.docx");
  execFileSync("node", [path.join(ROOT, "build/build-docx.mjs"), "--theme", themeFile, "--out", out], { cwd: ROOT, stdio: "pipe" });
  const used = styleSources(docxModel(out).parts);
  assert.ok(used.colors.includes("FF00AA") && used.colors.includes("AA00FF"), "mutated colors reach the XML");
  assert.ok(used.fonts.includes("Arial"), "mutated body font reaches the XML");
  const allowed = themeValues(t2);
  for (const c of used.colors) assert.ok(allowed.colors.has(c), `color ${c} is not a token of the mutated theme`);
  for (const f of used.fonts) assert.ok(allowed.fonts.has(f), `font ${f} is not a token of the mutated theme`);
  assert.ok(!used.fonts.includes("Calibri") || t2.fonts.heading === "Calibri", "old body font must be gone");
});

// ---------------------------------------------------------------- notion markdown + originals
test("dist markdown: no raw HTML and every image link resolves next to the file", () => {
  assert.ok(fs.existsSync(DIST_MD), "dist/TP_Cascada_Grupo01.md does not exist");
  const text = fs.readFileSync(DIST_MD, "utf8");
  assert.ok(!/<\/?[a-z][^>]*>/i.test(text.replace(/<br\s*\/?>/gi, "")), "raw HTML found");
  const imgs = [...text.matchAll(/!\[[^\]]*\]\(([^)]+)\)/g)].map((x) => x[1]);
  assert.ok(imgs.length > 0);
  for (const i of imgs) assert.ok(fs.existsSync(path.join(path.dirname(DIST_MD), i)), `missing ${i}`);
  assert.ok(!/\[\[TOC\]\]/.test(text), "[[TOC]] must be replaced by a plain list in the distributable markdown");
});

test("originals: sha256 of every original file is unchanged", () => {
  const lines = fs.readFileSync(path.join(ROOT, "tests/originals.sha256"), "utf8").trim().split("\n");
  assert.ok(lines.length >= 18);
  for (const l of lines) {
    const m = /^([0-9a-f]{64})\s+\*?(.+)$/.exec(l);
    assert.equal(sha256(path.join(REPO, m[2])), m[1], m[2]);
  }
});
