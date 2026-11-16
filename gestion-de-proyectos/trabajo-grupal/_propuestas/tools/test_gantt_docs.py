"""Checks over the GENERATED Gantt documents: they must agree with the team's Excel, recomputed here from scratch."""
import csv
import io
import json
import pathlib
import re
import unittest

import cpm
import data as D
import team_gantt as tg

ROOT = pathlib.Path(__file__).resolve().parent.parent
STALE = ["sin predecesoras", "sin duraciones tabuladas", "no tenía duraciones", "propuestas derivadas", "cae el 30/04",
         "Gate 2 al 30/04", "Gate 2 = 30/04", "no estaba en la carpeta", "123 d.h.", "123 días hábiles"]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def has_stale(text):
    """Stale phrases that would reintroduce the claims we retracted (allowed only inside the correction note)."""
    return [s for s in STALE if s in text and s != "no tenía duraciones"]


class NoStaleClaims(unittest.TestCase):
    FILES = ["00-resumen.md", "01-charter-condensado.md", "02-gantt/gantt.md", "03-presupuesto/presupuesto.md", "04-riesgos.md",
             "05-canvas-dt-smart.md", "06-coherencia.md", "07-formato-entrega.md", "propuestas-de-mejora.html"]

    def test_no_stale_phrases_anywhere(self):
        for rel in self.FILES:
            self.assertEqual(has_stale(read(rel)), [], rel)

    def test_the_stale_detector_can_fail(self):
        self.assertEqual(has_stale("el Gantt está sin predecesoras"), ["sin predecesoras"])

    def test_the_correction_is_stated_plainly(self):
        for rel in ("02-gantt/gantt.md", "00-resumen.md", "propuestas-de-mejora.html"):
            t = read(rel)
            self.assertIn("Corrección", t, rel)
            self.assertIn("Excel", t, rel)


class GanttDocMatchesTheExcel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.team = tg.load()
        cls.cal = tg.weekday_calendar()
        cls.text = read("02-gantt/gantt.md")
        e = cpm.schedule(tg.acts_for_cpm(cls.team, "endpoints"))
        r = cpm.schedule(tg.acts_for_cpm(cls.team, "range"))
        cls.cpm_total = cpm.project_duration(e)
        cls.range_total = cpm.project_duration(r)
        cls.crit = sorted(i for i, x in e.items() if x["critical"])

    def test_cpm_numbers_in_the_document_are_recomputed_ones(self):
        self.assertEqual((self.cpm_total, self.range_total), (126, 129))
        self.assertIn(f"**{self.cpm_total} días hábiles, {len(self.crit)} actividades críticas", self.text)
        self.assertIn(f"da **{self.range_total} días hábiles**", self.text)

    def test_scenario_table_has_every_total_and_end_date(self):
        for total, end in ((126, "23/09/2026"), (129, "28/09/2026"), (131, "30/09/2026"), (130, "29/09/2026"), (139, "12/10/2026")):
            self.assertRegex(self.text, rf"\| {total} \| {end} \|")

    def test_overlap_table_lists_exactly_the_seven_pairs(self):
        sec = self.text.split("### 2 ·", 1)[1].split("**Celdas a corregir", 1)[0]
        pairs = re.findall(r"^\| (\d+) \| [^|]+\| (\d+) \| [^|]+\| (\d+) \|", sec, flags=re.M)
        self.assertEqual([(int(a), int(b), int(c)) for a, b, c in pairs],
                         [(2, 1, 2), (3, 1, 2), (8, 7, 2), (9, 7, 2), (14, 13, 2), (15, 12, 2), (16, 14, 3)])

    def test_cells_to_fix_are_the_seven_with_their_explicit_text(self):
        sec = self.text.split("**Celdas a corregir", 1)[1].split("**Celdas que solo", 1)[0]
        rows = re.findall(r"^\| (\d+) \| [^|]+\| ([^|]+) \| ([^|]+) \|", sec, flags=re.M)
        self.assertEqual([int(r[0]) for r in rows], [8, 9, 10, 14, 15, 16, 27])
        got = {int(a): (w.strip(), p.strip()) for a, w, p in rows}
        self.assertEqual(got[8], ("5-7", "5, 6"))
        self.assertEqual(got[27], ("18-23", "26"))

    def test_published_and_corrected_critical_sets_are_both_quoted(self):
        net = tg.corrected_network(self.team)
        res = cpm.schedule(net)
        path = cpm.critical_path(net, res)
        self.assertIn(", ".join(map(str, path)), self.text)
        self.assertIn(", ".join(map(str, cpm.critical_path(tg.acts_for_cpm(self.team, "endpoints"), cpm.schedule(tg.acts_for_cpm(self.team, "endpoints"))))), self.text)

    def test_all_forty_activities_appear_in_the_table_with_a_role(self):
        sec = self.text.split("## Las 40 actividades", 1)[1].split("## Opciones", 1)[0]
        ids = [int(m) for m in re.findall(r"^\| (\d+) \|", sec, flags=re.M)]
        self.assertEqual(ids, list(range(1, 41)))
        roles = {r[1] for r in D.TEAM_ROLES}
        for line in sec.splitlines():
            if re.match(r"^\| \d+ \|", line):
                self.assertIn(line.rsplit("|", 2)[-2].strip(), roles, line)


class ScheduleCsv(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = list(csv.DictReader(io.StringIO(read("02-gantt/schedule.csv"))))

    def test_forty_rows_with_the_teams_own_values(self):
        self.assertEqual(len(self.rows), 40)
        team = {a["id"]: a for a in tg.load()["activities"]}
        for r in self.rows:
            a = team[int(r["ID"])]
            self.assertEqual((r["Actividad"], int(r["Duración (d.h.)"]), r["Dependencias (como las escribió el equipo)"]),
                             (a["name"], a["dur"], a["deps_raw"]))
            self.assertEqual(r["Inicio (equipo)"], a["start"].strftime("%d/%m/%Y"))
            self.assertEqual(r["Fin (equipo)"], a["end"].strftime("%d/%m/%Y"))

    def test_explicit_dependencies_and_change_flags(self):
        by = {int(r["ID"]): r for r in self.rows}
        self.assertEqual(by[8]["Predecesoras propuestas (explícitas)"], "5, 6")
        self.assertEqual(by[2]["Predecesoras propuestas (explícitas)"], "1 (inicio-a-inicio +1 día)")
        self.assertEqual([i for i, r in by.items() if r["Cambia"] == "Sí"], [8, 9, 10, 14, 15, 16, 27])
        self.assertEqual([i for i, r in by.items() if r["Cambia"] == "Inicio-a-inicio"], [2, 3])
        self.assertEqual([i for i, r in by.items() if r["Cambia"] == "Aclarar"], [4, 17, 31, 39, 40])

    def test_team_slack_column_equals_the_endpoints_computation(self):
        for r in self.rows:
            self.assertEqual(r["Holgura hoja del equipo"], r["Holgura (extremos)"], r["ID"])

    def test_every_activity_has_an_accountable_role(self):
        roles = {x[1] for x in D.TEAM_ROLES}
        for r in self.rows:
            self.assertIn(r["Responsable propuesto (rol)"], roles)


class NumbersJson(unittest.TestCase):
    def test_numbers_json_matches_a_fresh_computation(self):
        import build_all
        fresh, *_ = build_all.compute()
        saved = json.loads((ROOT / "tools" / "numbers.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["calendar"]["cpm_wd"], fresh["calendar"]["cpm_wd"])
        self.assertEqual(saved["ladder_b"], fresh["ladder_b"])
        self.assertEqual(saved["critical_path_corrected"], fresh["critical_path_corrected"])


class HtmlGantt(unittest.TestCase):
    def test_html_has_the_correction_and_the_same_numbers(self):
        t = read("propuestas-de-mejora.html")
        self.assertIn('id="gantt"', t)
        self.assertIn("Gantt: ya tiene lo que pide la cátedra", t)
        self.assertRegex(t, r"<strong>126 días hábiles</strong>")
        self.assertIn("129", t)
        self.assertIn("12/10/2026", t)


if __name__ == "__main__":
    unittest.main()
