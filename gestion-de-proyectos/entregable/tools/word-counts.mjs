// Prints word counts of F1 (original docx) per part vs the consolidated docx (used for BASE-F1-agregar-quitar.md).
import { originalBlocks, docxModel, segments, segmentWords, tokens, DIST_DOCX } from "../tests/helpers.mjs";
const norm = (s) => s.replace(/\s+/g, " ").trim();
const bt = (b) => (b.type === "p" ? b.text : b.type === "tbl" ? b.rows.map((r) => r.join(" ")).join(" ") : "");
const f1 = originalBlocks("Proyect Charter y demas puntos.docx");
const texts = f1.map(bt);
const last = (re) => { let k = -1; texts.forEach((t, i) => { if (re.test(norm(t))) k = i; }); return k; };
const cuts = { toc: texts.findIndex((t) => /^ÍNDICE$/i.test(norm(t))), s5: last(/^5\.\s*PROJECT CHARTER$/i), s6: last(/^6\.\s*GANTT/i), s7: last(/^7\.\s*Matriz de Stakeholders/i), s8: last(/^8\.\s*Plan de Comunicaci/i), s9: last(/^9\.\s*GESTI/i), s10: last(/^10\.\s*Gesti/i) };
const w = (a, b) => tokens(texts.slice(a, b).join("\n")).length;
const rep = {
  "F1 cabecera+índice manual (antes de §5)": w(0, cuts.s5),
  "F1 §5 Project Charter": w(cuts.s5, cuts.s6),
  "F1 §6 Gantt": w(cuts.s6, cuts.s7),
  "F1 §7 Stakeholders": w(cuts.s7, cuts.s8),
  "F1 §8 Comunicación": w(cuts.s8, cuts.s9),
  "F1 §9 Riesgos": w(cuts.s9, cuts.s10),
  "F1 §10 Presupuesto": w(cuts.s10, texts.length),
  "F1 total": w(0, texts.length),
};
console.log(JSON.stringify(rep, null, 1));
const segs = segments(docxModel(DIST_DOCX));
const ours = {};
for (const s of segs) ours[norm(s.heading.text).slice(0, 48)] = segmentWords(s).length;
console.log(JSON.stringify(ours, null, 1));
console.log("ours total (sections):", Object.values(ours).reduce((a, b) => a + b, 0));
