"""Tests for the revised Design Thinking material (written first).

The team's deck claimed ten real interviews; the group decided they were invented and that no real interviews are needed,
so the honest fix is to relabel the research as a simulated academic exercise (proto-personas, hypotheses, public sources).
"""
import pathlib
import re
import unittest

import build_all
import data as D

PACK = pathlib.Path(__file__).resolve().parent.parent
DT = PACK / "05b-design-thinking-revisado.md"


def read(rel):
    return (PACK / rel).read_text(encoding="utf-8")


def section(text, start, end=None):
    i = text.index(start)
    j = text.index(end, i + 1) if end else len(text)
    return text[i:j]


class StructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = DT.read_text(encoding="utf-8")

    def test_has_the_seven_sections(self):
        for h in ("## 1. Qué cambia y por qué", "## 2. Copia revisada, slide por slide", "## 3. Trazabilidad",
                  "## 4. Texto para la sección 4 del documento", "## 5. Decisión del grupo: «Mi hogar»",
                  "## 6. Clase 7: qué verificar cuando llegue el PDF", "## 7. Para después"):
            self.assertIn(h, self.t)

    def test_eight_slides_of_revised_copy(self):
        copy = section(self.t, "## 2. Copia revisada", "## 3. Trazabilidad")
        self.assertEqual(re.findall(r"^### Slide (\d)", copy, flags=re.M), [str(i) for i in range(1, 9)])

    def test_before_after_table_keeps_the_old_claims_only_in_section_1(self):
        s1 = section(self.t, "## 1. Qué cambia", "## 2. Copia revisada")
        self.assertIn("10 vecinos", s1)
        self.assertIn("Antes", s1)
        self.assertIn("Después", s1)


class HonestyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = DT.read_text(encoding="utf-8")
        cls.copy = section(cls.t, "## 2. Copia revisada", "## 3. Trazabilidad")

    def test_revised_copy_has_no_claim_of_real_fieldwork(self):
        for bad in ("10 vecinos", "entrevistas semiestructuradas", "muestra por conveniencia", "HOGARES CON CHICOS", "Cambiarla"):
            self.assertNotIn(bad, self.copy, bad)

    def test_revised_copy_declares_the_simulation(self):
        for needed in ("Investigación simulada", "no se realizaron entrevistas", "hipótesis", "ficticia"):
            self.assertIn(needed, self.copy, needed)

    def test_cover_uses_the_agreed_segment(self):
        self.assertIn("HOGARES DE LA CIUDAD × ÁREAS DEL GCBA", self.copy)

    def test_three_proto_personas(self):
        s5 = section(self.copy, "### Slide 5", "### Slide 6")
        for needed in ("Lucía", "adulto mayor", "movilidad reducida"):
            self.assertIn(needed, s5)

    def test_public_facts_are_cited_and_flagged_for_reverification(self):
        for needed in ("mapa.buenosaires.gob.ar", "14 APIs", "re-verificar"):
            self.assertIn(needed, self.t)

    def test_no_invented_quotes_or_counts_in_hypotheses(self):
        s2 = section(self.copy, "### Slide 2", "### Slide 3")
        hyp = section(s2, "HIPÓTESIS DE TRABAJO", "ANCLAJE")
        self.assertIsNone(re.search(r"\d+\s*(%|de cada|personas|vecinos)", hyp))
        self.assertNotIn("«", hyp)

    def test_testear_slide_stays_simulated(self):
        s8 = section(self.copy, "### Slide 8")
        self.assertIn("FICTICIAS", s8)
        self.assertIn("simulada", s8.lower())


class TraceabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = DT.read_text(encoding="utf-8")
        cls.tr = section(cls.t, "## 3. Trazabilidad", "## 4. Texto para la sección 4")

    def test_five_phases_in_the_table(self):
        rows = [l for l in self.tr.splitlines() if l.startswith("| ") and not l.startswith("| Fase") and not l.startswith("|---")]
        self.assertEqual(len(rows), 5)
        for phase in ("Empatizar", "Definir", "Idear", "Prototipo", "Testear"):
            self.assertTrue(any(r.startswith(f"| {phase}") for r in rows), phase)

    def test_every_risk_id_exists_in_the_register(self):
        ids = set(re.findall(r"\bR\d{2}\b", self.tr))
        known = {r["id"] for r in D.RISKS}
        self.assertTrue(ids)
        self.assertLessEqual(ids, known)
        self.assertIn("R10", ids)                                   # personal data: the prototype says «sin datos personales para reportar»

    def test_charter_results_and_gates_exist(self):
        for o in ("O1", "O2", "O3", "O4"):
            self.assertIn(o, self.tr)
        gates = {f"G{p[0]}": p[5] for p in D.PHASES}
        for g in re.findall(r"\bG(\d)\b", self.tr):
            self.assertIn(f"G{g}", gates)
        for name in (gates["G3"], gates["G6"]):
            self.assertIn(name, self.tr)

    def test_activities_cited_match_the_gantt_names(self):
        names = {a["id"]: a["name"] for a in D.ACTIVITIES}
        self.assertIn(names[16], self.tr)                             # Diseño UX/UI
        self.assertIn(names[29], self.tr)                             # Pruebas de usabilidad


class DocumentTextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = DT.read_text(encoding="utf-8")
        cls.s4 = section(cls.t, "## 4. Texto para la sección 4 del documento", "## 5. Decisión del grupo")

    def test_about_one_page(self):
        words = len(re.findall(r"\w+", self.s4))
        self.assertGreaterEqual(words, 250)
        self.assertLessEqual(words, 650)

    def test_has_the_five_phase_table_and_both_bridges(self):
        for phase in ("Empatizar", "Definir", "Idear", "Prototipo", "Testear"):
            self.assertIn(phase, self.s4)
        self.assertIn("Puente Canvas → Design Thinking", self.s4)
        self.assertIn("Puente Design Thinking → Charter", self.s4)

    def test_lists_which_slides_to_export_and_how(self):
        self.assertIn("Export slides to", self.s4)
        self.assertIn("slide 7", self.s4.lower())

    def test_declares_the_simulation_in_the_document_text(self):
        self.assertIn("simulada", self.s4.lower())
        self.assertIn("no se realizaron entrevistas", self.s4)


class DecisionAndClass7Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = DT.read_text(encoding="utf-8")

    def test_mi_hogar_is_a_group_decision_with_the_alternative(self):
        s5 = section(self.t, "## 5. Decisión del grupo: «Mi hogar»", "## 6. Clase 7")
        for needed in ("Decisión del grupo", "fuera del MVP", "opt-in", "Opción A", "Opción B", "R10"):
            self.assertIn(needed, s5)

    def test_class7_checklist(self):
        s6 = section(self.t, "## 6. Clase 7", "## 7. Para después")
        self.assertIn("a confirmar", s6)
        self.assertGreaterEqual(len([l for l in s6.splitlines() if l.startswith("- ")]), 4)

    def test_mock_is_for_later(self):
        s7 = section(self.t, "## 7. Para después")
        self.assertIn("mock", s7.lower())
        self.assertIn("al final", s7.lower())

    def test_no_phone_numbers(self):
        self.assertIsNone(re.search(r"\+?\d[\d\s-]{9,}\d", re.sub(r"https?://\S+", "", self.t)))   # URLs carry long ids


class PackIsConsistentTests(unittest.TestCase):
    STALE = ("5 a 8 entrevistas", "plan mínimo", "Plan mínimo", "tabla de entrevistas", "Prueba de un wireframe", "Si se hizo un mínimo")

    def test_no_stale_interview_plan_anywhere(self):
        for rel in ("00-resumen.md", "05-canvas-dt-smart.md", "06-coherencia.md", "07-formato-entrega.md", "propuestas-de-mejora.html", "01-charter-condensado.md"):
            t = read(rel)
            for s in self.STALE:
                self.assertNotIn(s, t, f"{rel}: {s}")

    def test_the_canvas_doc_points_to_the_revised_dt(self):
        t = read("05-canvas-dt-smart.md")
        self.assertIn("05b-design-thinking-revisado.md", t)
        self.assertIn("Investigación simulada", t)

    def test_summary_mentions_the_dt_decision_and_the_new_file(self):
        t = read("00-resumen.md")
        self.assertIn("05b", t)
        self.assertIn("simulada", t.lower())

    def test_html_mentions_the_dt_decision(self):
        t = read("propuestas-de-mejora.html")
        self.assertIn("simulada", t.lower())


if __name__ == "__main__":
    unittest.main()
