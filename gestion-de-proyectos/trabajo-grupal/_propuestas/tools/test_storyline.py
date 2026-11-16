"""Tests for the narrative spine (08-guion-narrativo.md) and its consistency with the rest of the pack (written first).

A 'thread object' is a fact that must reappear identically across sections (segment, milestones, critical path, USD figures,
exchange rate, top risks). The test reads the OTHER documents of the pack, so a divergence anywhere fails here.
"""
import io
import pathlib
import re
import unittest
import xml.etree.ElementTree as ET
import zipfile

import build_all
import data as D
from fmt import n, usd

PACK = pathlib.Path(__file__).resolve().parent.parent
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
CONSIGNA = ["Carátula", "Índice", "Canvas del proyecto", "Aplicar Design Thinking", "Project Charter", "Gantt del proyecto completo",
            "Matriz de stakeholders", "Plan de comunicación", "Gestión de riesgos - Matriz de riesgos", "Gestión de costos - Presupuesto"]


def text_of(rel):
    p = PACK / rel
    if p.suffix == ".docx":
        root = ET.fromstring(zipfile.ZipFile(io.BytesIO(p.read_bytes())).read("word/document.xml"))
        return " ".join("".join(t.text or "" for t in para.iter(W + "t")) for para in root.iter(W + "p"))
    return p.read_text(encoding="utf-8")


def section(text, start, end=None):
    i = text.index(start)
    j = text.index(end, i + 1) if end else len(text)
    return text[i:j]


class SpineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = text_of("08-guion-narrativo.md")

    def test_has_the_five_sections(self):
        for h in ("## 1. El papel de cada sección", "## 2. Objetos del hilo", "## 3. Frases puente",
                  "## 4. Resumen ejecutivo", "## 5. Tabla de consistencia"):
            self.assertIn(h, self.t)

    def test_ten_sections_in_the_order_of_the_consigna(self):
        s1 = section(self.t, "## 1. El papel de cada sección", "## 2. Objetos del hilo")
        rows = [l for l in s1.splitlines() if re.match(r"\| (\d+) \|", l)]
        self.assertEqual(len(rows), 10)
        for i, (row, name) in enumerate(zip(rows, CONSIGNA), 1):
            self.assertTrue(row.startswith(f"| {i} | {name} |"), (i, name, row[:60]))

    def test_every_row_says_what_it_receives_and_delivers(self):
        s1 = section(self.t, "## 1. El papel de cada sección", "## 2. Objetos del hilo")
        for l in (l for l in s1.splitlines() if re.match(r"\| (\d+) \|", l)):
            cells = [c.strip() for c in l.strip("|").split("|")]
            self.assertEqual(len(cells), 5, l[:50])
            self.assertTrue(all(cells), l[:50])

    def test_bridges_cover_every_transition(self):
        s3 = section(self.t, "## 3. Frases puente", "## 4. Resumen ejecutivo")
        for key in ("apertura", "3", "4", "5", "6", "7", "8", "9", "10", "cierre"):
            self.assertIn(D.BRIDGES[key], s3, key)

    def test_bridge_for_design_thinking_no_longer_claims_real_people(self):
        self.assertNotIn("personas reales", D.BRIDGES["4"])
        self.assertIn("simulada", D.BRIDGES["4"])

    def test_executive_summary_length_and_content(self):
        s4 = section(self.t, "## 4. Resumen ejecutivo", "## 5. Tabla de consistencia")
        body = "\n".join(l for l in s4.splitlines() if not l.startswith("#"))
        words = len(re.findall(r"\w+", body))
        self.assertGreaterEqual(words, 200)
        self.assertLessEqual(words, 330)
        o, *_ = build_all.compute(with_sens=False)
        for needed in (usd(o["ladder_b"]["total"]), f"{o['calendar']['cpm_wd']} días hábiles", "hogar", "simulación", "ARS " + n(o["fx"]["value"], 2)):
            self.assertIn(needed, body)


class ThreadObjectsTests(unittest.TestCase):
    """The same fact, in every document where it must appear."""

    @classmethod
    def setUpClass(cls):
        cls.o, *_ = build_all.compute(with_sens=False)
        cls.docx = "01-charter/Project_Charter_completado.docx"

    def check(self, value, files):
        for rel in files:
            self.assertIn(value.lower(), text_of(rel).lower(), f"{value!r} is missing from {rel}")

    def test_project_name(self):
        self.check("Modernización del Mapa Interactivo de la Ciudad", ["08-guion-narrativo.md", "01-charter-condensado.md", self.docx])

    def test_segment(self):
        self.check("hogares de la Ciudad", ["08-guion-narrativo.md", "05-canvas-dt-smart.md", "05b-design-thinking-revisado.md", self.docx])

    def test_the_eight_milestones_and_their_dates(self):
        for h in D.TEAM["hitos"]:
            d = h["date"].strftime("%d/%m/%Y")
            self.check(d, ["08-guion-narrativo.md", "02-gantt/gantt.md", "01-charter-condensado.md", self.docx])

    def test_critical_path_duration(self):
        self.check(f"{self.o['calendar']['cpm_wd']} días hábiles", ["08-guion-narrativo.md", self.docx])
        self.check(str(self.o["calendar"]["cpm_wd"]), ["02-gantt/gantt.md", "06-coherencia.md"])

    def test_budget_figures_in_usd(self):
        lb = self.o["ladder_b"]
        for value in (usd(lb["total"]), usd(lb["baseline"]), usd(lb["mgmt_reserve"]), usd(lb["contingency"])):
            self.check(value, ["08-guion-narrativo.md", "03-presupuesto/presupuesto.md", "03-presupuesto/memoria-de-calculo.md", self.docx])
        self.check(usd(self.o["maint_usd"]), ["08-guion-narrativo.md", "03-presupuesto/presupuesto.md", self.docx])

    def test_exchange_rate(self):
        self.check("ARS " + n(self.o["fx"]["value"], 2), ["08-guion-narrativo.md", "03-presupuesto/presupuesto.md", "03-presupuesto/memoria-de-calculo.md", self.docx, "06-coherencia.md"])

    def test_top_three_risks(self):
        for r in self.o["risks"]["sorted"][:3]:
            self.check(r["id"], ["08-guion-narrativo.md", "04-riesgos.md", "03-presupuesto/presupuesto.md"])

    def test_four_results_of_the_charter(self):
        for needle in ("Capa geográfica confiable", "Integración multicanal", "Reportes y seguimiento"):
            self.check(needle, ["08-guion-narrativo.md", "05-canvas-dt-smart.md", self.docx])

    def test_consistency_table_lists_each_object_with_its_value(self):
        t = text_of("08-guion-narrativo.md")
        s5 = section(t, "## 5. Tabla de consistencia")
        for obj in ("Nombre del proyecto", "Segmento", "Funcionalidades núcleo", "Hitos", "Duración", "Presupuesto", "Tipo de cambio", "Riesgos principales", "Resultados del Charter", "Simulación"):
            self.assertIn(f"| {obj}", s5, obj)
        self.assertIn(usd(self.o["ladder_b"]["total"]), s5)


class SummaryAndFormatUpdatedTests(unittest.TestCase):
    def test_summary_lists_the_new_items(self):
        t = text_of("00-resumen.md")
        for needle in ("Project_Charter_completado.docx", "05b", "auditoria.md", "08-guion-narrativo.md"):
            self.assertIn(needle, t)

    def test_format_doc_uses_the_final_bridges_and_plan(self):
        t = text_of("07-formato-entrega.md")
        for key in ("4", "10"):
            self.assertIn(D.BRIDGES[key], t)
        self.assertIn("08-guion-narrativo.md", t)
        self.assertIn("Project_Charter_completado.docx", t)

    def test_html_lists_the_new_items(self):
        t = text_of("propuestas-de-mejora.html")
        for needle in ("plantilla", "Design Thinking", "auditoría", "guion"):
            self.assertIn(needle.lower(), t.lower())


if __name__ == "__main__":
    unittest.main()
