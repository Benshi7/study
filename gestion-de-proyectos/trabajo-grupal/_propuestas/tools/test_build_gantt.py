"""build_all.compute() on the team's real Gantt (written before the rebase of the model)."""
import datetime as dt
import unittest

import budget as bud
import build_all
import calendar_ar as car
import data as D
import team_gantt as tg


class Compute(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o, cls.res, cls.acts, cls.cal = build_all.compute(with_sens=False)
        cls.team = tg.load()

    def test_calendar_block_has_every_reading(self):
        c = self.o["calendar"]
        self.assertEqual((c["total_wd"], c["cpm_wd"]), (126, 126))
        self.assertEqual((c["range_wd"], c["span_wd"], c["dated_wd"], c["strict_wd"], c["corrected_wd"]), (129, 131, 130, 139, 130))
        self.assertEqual(c["corrected_end"], "29/09/2026")
        self.assertEqual(c["end"], "23/09/2026")
        self.assertEqual(c["span_end"], "30/09/2026")
        self.assertEqual(c["dated_end"], "29/09/2026")
        self.assertEqual(c["strict_end"], "12/10/2026")

    def test_working_days_are_monday_to_friday_without_holidays(self):
        self.assertEqual(self.cal.holidays, frozenset())
        self.assertEqual(self.cal.finish_date(131), dt.date(2026, 9, 30))

    def test_res_holds_the_stated_dates_and_the_teams_slack_and_flags(self):
        for t in self.team["activities"]:
            r = self.res[t["id"]]
            self.assertEqual(self.cal.start_date(r["es"]), t["start"], t["id"])
            self.assertEqual(self.cal.finish_date(r["ef"]), t["end"], t["id"])
            s2 = self.team["sheet2"][t["id"]]
            self.assertEqual((r["slack"], r["critical"]), (s2["slack"], s2["critical"]), t["id"])

    def test_critical_paths(self):
        self.assertEqual(len(self.o["critical_path"]), 22)
        self.assertEqual(self.o["n_critical"], 23)
        self.assertNotIn(25, self.o["critical_path"])
        self.assertIn(25, self.o["critical_path_dated"])
        self.assertEqual(self.o["n_critical_dated"], 26)
        self.assertEqual(self.o["critical_path_corrected"], [1, 3, 4, 5, 8, 10, 12, 16, 17, 18, 23, 25, 26, 27, 29, 31, 32, 34, 35, 36, 38, 39, 40])
        self.assertEqual(self.o["n_critical_corrected"], 27)

    def test_gates_all_land_on_the_excel_hitos(self):
        self.assertTrue(self.o["gates_ok"])
        self.assertEqual([g["computed"] for g in self.o["gates"]],
                         ["10/04/2026", "01/05/2026", "26/05/2026", "02/07/2026", "21/07/2026", "27/08/2026", "09/09/2026", "30/09/2026"])
        self.assertTrue(all(g["declared"] == g["proposed"] for g in self.o["gates"]))

    def test_gantt_findings(self):
        g = self.o["gantt"]
        self.assertEqual([s["key"] for s in g["scenarios"]], ["escrito", "rango", "fechas_del_equipo", "corregida", "con_adelantos", "fs_estricto"])
        self.assertEqual(len(g["leads"]), 7)
        self.assertEqual(g["corrected_cells_range"], [8, 9, 10, 14, 15, 16, 27])
        self.assertEqual(g["corrected_cells_endpoints"], [4, 8, 9, 10, 14, 15, 16, 17, 27, 31, 39, 40])
        self.assertEqual(len(g["corrected_text"]), 40)
        self.assertEqual(g["corrected_text"]["8"], "5, 6")
        self.assertEqual(g["idle_gaps"], [[23, 27, 13], [31, 32, 1]])
        self.assertEqual(len(g["phase_diffs"]), 5)
        self.assertEqual(g["ambiguous_ids"], [4, 8, 9, 15, 16, 17, 27, 31, 39, 40])
        self.assertEqual(len(g["range_slack_mismatches"]), 17)
        self.assertEqual(g["range_critical_mismatches"], [25, 26, 27, 28, 30])
        self.assertEqual(g["gap"]["leads_saved"], 9)

    def test_holidays_are_reported_but_do_not_change_the_base_calendar(self):
        g = self.o["gantt"]
        ids = [h["id"] for h in g["holiday_hits"]]
        for i in (1, 10, 17):
            self.assertIn(i, ids)
        real = car.Calendar(D.SIM_START)
        self.assertEqual(g["real_calendar_end"], real.finish_date(131).strftime("%d/%m/%Y"))
        self.assertEqual(g["holiday_weekdays_in_window"], 8)

    def test_pert_illustration_is_computed(self):
        rows = {r["id"]: r for r in self.o["gantt"]["pert_example"]}
        self.assertAlmostEqual(rows[7]["te"], 8.0)
        self.assertAlmostEqual(rows[25]["te"], 9.0)
        self.assertAlmostEqual(rows[31]["te"], (5 + 4 * 7 + 16) / 6)

    def test_labour_months_derive_from_the_stated_dates(self):
        pm = next(r for r in self.o["labour"] if r["key"] == "pm")
        self.assertEqual(pm["wd"], 130)    # the stated span is 131 days, but 21/08 has no activity (idle day 31 -> 32)
        for r in self.o["labour"]:
            ids = next(x[4] for x in D.TEAM_ROLES if x[0] == r["key"])
            self.assertEqual(r["wd"], bud.role_workdays(self.res, ids), r["key"])

    def test_owners_per_activity_are_exported(self):
        self.assertEqual(len(self.o["gantt"]["owners"]), 40)

    def test_buffer_to_the_entrega_uses_the_real_calendar(self):
        # 01/10..13/10 minus the 12/10 holiday = 8 working days before the 14/10 delivery day itself... counted to 14/10 inclusive: 9
        self.assertEqual(self.o["buffer_wd"], 9)

    def test_phase_windows_in_working_days(self):
        pw = self.o["phase_wd"]
        self.assertEqual(sorted(pw), list(range(1, 9)))
        self.assertEqual(pw[4], 27)        # Desarrollo 27/05–02/07 in Mon-Fri days


class FxStillParametric(unittest.TestCase):
    def test_default_fx_comes_from_the_constant(self):
        o, *_ = build_all.compute(with_sens=False)
        self.assertEqual(o["fx"]["value"], D.FX_ARS_PER_USD)


if __name__ == "__main__":
    unittest.main()
