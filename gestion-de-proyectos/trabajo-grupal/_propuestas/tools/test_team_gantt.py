"""Characterization tests for the team's REAL Gantt (Excel annex to section 6), written before the code.

The Excel lives next to the other originals in trabajo-grupal/. The tools never modify it; a snapshot
(team_gantt.json) makes the pack self-contained and a test proves the snapshot equals the live file.
"""
import datetime as dt
import hashlib
import json
import pathlib
import unittest

import calendar_ar as car
import cpm
import team_gantt as tg
import xlsx_reader as xr

TOOLS = pathlib.Path(__file__).resolve().parent
TRABAJO = TOOLS.parent.parent
XLSX = TRABAJO / "Gantt_y_Camino_Critico_Hitos_Anexo_Punto_6.xlsx"


class OriginalsGuard(unittest.TestCase):
    def test_original_files_are_byte_identical_to_the_recorded_hashes(self):
        lines = [l for l in (TOOLS / "originals.sha256").read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertEqual(len(lines), 5)
        for l in lines:
            digest, name = l.split("  ", 1)
            p = TRABAJO / name
            self.assertTrue(p.exists(), f"{name} is missing")
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), digest, f"{name} was modified")


class Reader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wb = dict(xr.read_workbook(XLSX))

    def test_four_sheets_in_order(self):
        self.assertEqual(list(self.wb), ["Cronograma y Gantt", "Dependencias y Camino Crítico", "Hitos Operativos y Académicos", "Anexo Punto 6"])

    def test_forty_activities_in_the_first_two_sheets(self):
        for name in ("Cronograma y Gantt", "Dependencias y Camino Crítico"):
            ids = [int(r[0]) for r in self.wb[name] if r and r[0].isdigit()]
            self.assertEqual(ids, list(range(1, 41)), name)

    def test_title_and_simulation_note(self):
        rows = self.wb["Cronograma y Gantt"]
        self.assertIn("01/04/2026 - 30/09/2026", rows[0][0])
        self.assertIn("ficticio", rows[1][0])

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            xr.read_workbook(TRABAJO / "does-not-exist.xlsx")


class Parsed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tg.from_workbook(XLSX)

    def test_activities_have_the_team_fields(self):
        a = self.d["activities"]
        self.assertEqual([x["id"] for x in a], list(range(1, 41)))
        first = a[0]
        self.assertEqual((first["name"], first["phase"], first["dur"], first["deps_raw"]), ("Definición del proyecto y alcance", "Inicio", 3, "-"))
        self.assertEqual((first["start"], first["end"]), (dt.date(2026, 4, 1), dt.date(2026, 4, 3)))
        self.assertEqual(a[39]["end"], dt.date(2026, 9, 30))

    def test_sheets_one_and_two_agree(self):
        for a in self.d["activities"]:
            s2 = self.d["sheet2"][a["id"]]
            self.assertEqual(s2["dur"], a["dur"])
            self.assertEqual(s2["preds_raw"], a["deps_raw"])
            self.assertEqual(s2["name"], a["name"])

    def test_every_stated_range_is_exactly_the_stated_number_of_weekdays(self):
        for a in self.d["activities"]:
            days = [a["start"] + dt.timedelta(k) for k in range((a["end"] - a["start"]).days + 1)]
            self.assertEqual(sum(1 for x in days if x.weekday() < 5), a["dur"], a["id"])

    def test_responsable_is_empty_for_all(self):
        self.assertTrue(all(a["responsable"] == "" for a in self.d["activities"]))

    def test_eight_hitos_with_dates(self):
        h = self.d["hitos"]
        self.assertEqual(len(h), 8)
        self.assertEqual((h[0]["name"], h[0]["date"]), ("Charter aprobado", dt.date(2026, 4, 10)))
        self.assertEqual((h[7]["name"], h[7]["date"]), ("Cierre del proyecto", dt.date(2026, 9, 30)))
        self.assertEqual(h[1]["date"], dt.date(2026, 5, 1))

    def test_anexo_lists_23_critical_activities(self):
        self.assertEqual(len(self.d["anexo_critical"]), 23)
        self.assertEqual(self.d["anexo_critical"][0], 1)
        self.assertEqual(self.d["anexo_critical"][-1], 40)

    def test_the_annex_spells_out_the_dash_notation_as_the_two_endpoints(self):
        # Annex row for activity 4 says '1, 3' while the schedule sheet says '1-3': the team's own reading
        rows = self.d["anexo_rows"]
        self.assertEqual(len(rows), 23)
        by_id = {a["id"]: a for a in self.d["activities"]}
        for r in rows:
            self.assertEqual(tg.parse_deps(r["deps_raw"], "range"), tg.parse_deps(by_id[r["id"]]["deps_raw"], "endpoints"), r["id"])
        self.assertEqual(next(r for r in rows if r["id"] == 4)["deps_raw"], "1, 3")
        # and at least one row where the two readings really differ
        self.assertNotEqual(tg.parse_deps("1-3", "range"), tg.parse_deps(next(r for r in rows if r["id"] == 4)["deps_raw"], "range"))

    def test_team_sheet_critical_flags_match_the_annex(self):
        flagged = sorted(i for i, s in self.d["sheet2"].items() if s["critical"])
        self.assertEqual(flagged, sorted(self.d["anexo_critical"]))

    def test_snapshot_equals_the_live_excel(self):
        snap = tg.load()
        self.assertEqual(snap["activities"], self.d["activities"])
        self.assertEqual(snap["sheet2"], self.d["sheet2"])
        self.assertEqual(snap["hitos"], self.d["hitos"])
        self.assertEqual(snap["anexo_critical"], self.d["anexo_critical"])


class DependencyNotation(unittest.TestCase):
    def test_range_reading(self):
        self.assertEqual(tg.parse_deps("1-3", "range"), [1, 2, 3])
        self.assertEqual(tg.parse_deps("15,18", "range"), [15, 18])
        self.assertEqual(tg.parse_deps("-", "range"), [])

    def test_endpoints_reading(self):
        self.assertEqual(tg.parse_deps("1-3", "endpoints"), [1, 3])
        self.assertEqual(tg.parse_deps("10-14", "endpoints"), [10, 14])
        self.assertEqual(tg.parse_deps("15,18", "endpoints"), [15, 18])
        self.assertEqual(tg.parse_deps("-", "endpoints"), [])

    def test_unknown_mode(self):
        with self.assertRaises(ValueError):
            tg.parse_deps("1-3", "other")

    def test_only_dashes_spanning_three_or_more_numbers_are_truly_ambiguous(self):
        # '8-9' or '24-25' read the same either way; '1-3' means {1,2,3} or {1,3}
        self.assertFalse(tg.is_ambiguous("8-9"))
        self.assertFalse(tg.is_ambiguous("-"))
        self.assertFalse(tg.is_ambiguous("15,18"))
        self.assertTrue(tg.is_ambiguous("1-3"))
        d = tg.load()
        amb = [a["id"] for a in d["activities"] if tg.is_ambiguous(a["deps_raw"])]
        self.assertEqual(amb, [4, 8, 9, 15, 16, 17, 27, 31, 39, 40])


class CpmReadings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tg.load()

    def _run(self, mode, extra=()):
        acts = tg.acts_for_cpm(self.d, mode, extra)
        res = cpm.schedule(acts)
        return res, cpm.project_duration(res)

    def test_endpoints_reading_reproduces_the_team_sheet_exactly(self):
        res, total = self._run("endpoints")
        self.assertEqual(total, 126)
        diff = tg.compare_to_team_sheet(res, self.d)
        self.assertEqual(diff["slack"], [])
        self.assertEqual(diff["critical"], [])

    def test_range_reading_gives_129_and_documented_mismatches(self):
        res, total = self._run("range")
        self.assertEqual(total, 129)
        diff = tg.compare_to_team_sheet(res, self.d)
        self.assertEqual([i for i, _, _ in diff["slack"]], [2, 6, 11, 12, 15, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 37])
        self.assertEqual(diff["critical"], [25, 26, 27, 28, 30])

    def test_critical_set_of_the_team_has_23_activities(self):
        res, _ = self._run("endpoints")
        self.assertEqual(sum(1 for r in res.values() if r["critical"]), 23)

    def test_adding_the_missing_link_26_to_27_pushes_the_end_far_beyond_the_declared_close(self):
        _, total = self._run("endpoints", extra=[(26, 27)])
        self.assertEqual(total, 139)


class StatedDatesVsDependencies(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tg.load()
        cls.cal = tg.weekday_calendar()

    def test_seven_activities_start_on_or_before_a_predecessor_finishes(self):
        for mode in ("endpoints", "range"):
            self.assertEqual(tg.overlap_pairs(self.d, mode),
                             [(2, 1), (3, 1), (8, 7), (9, 7), (14, 13), (15, 12), (16, 14)], mode)

    def test_overlap_lead_in_working_days(self):
        lead = {(s, p): k for s, p, k in tg.overlap_leads(self.d, "endpoints", self.cal)}
        self.assertEqual(lead, {(2, 1): 2, (3, 1): 2, (8, 7): 2, (9, 7): 2, (14, 13): 2, (15, 12): 2, (16, 14): 3})

    def test_stated_span_is_131_weekdays_versus_126_of_the_cpm(self):
        idx = tg.stated_index(self.d, self.cal)
        self.assertEqual(max(e for _, e in idx.values()), 131)

    def test_activity_27_starts_the_day_after_26_ends_without_listing_it_as_predecessor(self):
        cands = tg.adjacent_unlisted_links(self.d, "endpoints", self.cal)
        self.assertIn((26, 27), cands)
        self.assertNotIn((17, 18), cands)

    def test_idle_time_between_a_successor_and_its_latest_listed_predecessor(self):
        # 27 waits 13 working days after 23 (it really waits for 26, which is not listed) and 32 starts one day after 31 could finish
        gaps = tg.idle_gaps(self.d, "endpoints", self.cal)
        self.assertEqual(gaps, [(23, 27, 13), (31, 32, 1)])


class Holidays(unittest.TestCase):
    def test_activities_whose_dates_include_national_holidays(self):
        d = tg.load()
        hit = tg.holiday_hits(d, car.HOLIDAYS_2026)
        ids = [i for i, _ in hit]
        self.assertIn(1, ids)       # 02/04 and 03/04
        self.assertIn(10, ids)      # 01/05
        self.assertIn(17, ids)      # 25/05
        self.assertEqual(dict(hit)[1], [dt.date(2026, 4, 2), dt.date(2026, 4, 3)])


class Hitos(unittest.TestCase):
    def test_hito_dates_equal_the_end_of_their_closing_activity(self):
        d = tg.load()
        closing = {"Charter aprobado": 4, "Requerimientos aprobados": 10, "Diseño aprobado": 17, "Desarrollo completado": 23,
                   "Integraciones validadas": 26, "Pruebas aprobadas": 32, "Puesta en funcionamiento": 35, "Cierre del proyecto": 40}
        end = {a["id"]: a["end"] for a in d["activities"]}
        for h in d["hitos"]:
            self.assertEqual(h["date"], end[closing[h["name"]]], h["name"])

    def test_phase_windows_from_the_excel(self):
        d = tg.load()
        w = tg.phase_windows(d)
        self.assertEqual(w["Inicio"], (dt.date(2026, 4, 1), dt.date(2026, 4, 10)))
        self.assertEqual(w["Implementación"], (dt.date(2026, 8, 28), dt.date(2026, 9, 16)))
        self.assertEqual(w["Cierre"], (dt.date(2026, 9, 17), dt.date(2026, 9, 30)))


class SnapshotFile(unittest.TestCase):
    def test_snapshot_is_valid_json(self):
        json.loads((TOOLS / "team_gantt.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
