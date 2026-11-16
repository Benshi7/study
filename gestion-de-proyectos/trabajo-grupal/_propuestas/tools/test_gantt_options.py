"""The three ways to read the team's Gantt and what each one does to the end date (written before the code)."""
import datetime as dt
import unittest

import cpm
import team_gantt as tg


class Scenarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tg.load()
        cls.cal = tg.weekday_calendar()
        cls.rows = {r["key"]: r for r in tg.scenarios(cls.d, cls.cal)}

    def test_as_written_with_endpoints_is_the_team_cpm(self):
        r = self.rows["escrito"]
        self.assertEqual((r["total"], r["end"], r["n_critical"]), (126, dt.date(2026, 9, 23), 23))

    def test_as_written_with_range_is_129(self):
        r = self.rows["rango"]
        self.assertEqual((r["total"], r["end"]), (129, dt.date(2026, 9, 28)))

    def test_strict_finish_to_start_plus_the_missing_link_slips_past_the_declared_close(self):
        r = self.rows["fs_estricto"]
        self.assertEqual((r["total"], r["end"]), (139, dt.date(2026, 10, 12)))
        self.assertGreater(r["end"], dt.date(2026, 9, 30))

    def test_with_leads_and_the_missing_link_the_dates_are_consistent(self):
        r = self.rows["con_adelantos"]
        self.assertEqual((r["total"], r["end"]), (130, dt.date(2026, 9, 29)))

    def test_stated_dates_are_131_weekdays_ending_on_30_09(self):
        r = self.rows["fechas_del_equipo"]
        self.assertEqual((r["total"], r["end"]), (131, dt.date(2026, 9, 30)))

    def test_scenarios_come_in_a_fixed_order(self):
        self.assertEqual([r["key"] for r in tg.scenarios(self.d, self.cal)],
                         ["escrito", "rango", "fechas_del_equipo", "corregida", "con_adelantos", "fs_estricto"])

    def test_corrected_dependencies_reproduce_the_dates(self):
        r = self.rows["corregida"]
        self.assertEqual((r["total"], r["end"], r["n_critical"]), (130, dt.date(2026, 9, 29), 27))


class DatedNetwork(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tg.load()
        cls.cal = tg.weekday_calendar()
        cls.net = tg.dated_network(cls.d, "endpoints", cls.cal)
        cls.res = cpm.schedule(cls.net)
        cls.idx = tg.stated_index(cls.d, cls.cal)

    def test_early_starts_equal_the_stated_dates_up_to_activity_31(self):
        for i in range(1, 32):
            self.assertEqual(self.res[i]["es"], self.idx[i][0], i)

    def test_from_32_on_the_team_starts_one_working_day_later_than_necessary(self):
        for i in range(32, 41):
            self.assertEqual(self.res[i]["es"] + 1, self.idx[i][0], i)

    def test_the_leads_are_exactly_the_seven_overlaps(self):
        leads = {}
        for a in self.net:
            for p, lag in cpm.links(a):
                if lag:
                    leads[(a["id"], p)] = lag
        self.assertEqual(leads, {(2, 1): -2, (3, 1): -2, (8, 7): -2, (9, 7): -2, (14, 13): -2, (15, 12): -2, (16, 14): -3})

    def test_the_critical_path_now_goes_through_the_channel_integration(self):
        path = cpm.critical_path(self.net, self.res)
        self.assertEqual(path, [1, 3, 4, 7, 8, 10, 13, 14, 16, 17, 18, 23, 25, 26, 27, 30, 31, 32, 34, 35, 36, 38, 39, 40])

    def test_the_published_path_skips_25_and_26(self):
        res0 = cpm.schedule(tg.acts_for_cpm(self.d, "endpoints"))
        path0 = cpm.critical_path(tg.acts_for_cpm(self.d, "endpoints"), res0)
        self.assertNotIn(25, path0)
        self.assertNotIn(26, path0)
        self.assertEqual(len(path0), 22)

    def test_activities_with_extra_slack_in_the_dated_network(self):
        crit = sorted(i for i, r in self.res.items() if r["critical"])
        self.assertEqual(len(crit), 26)
        self.assertIn(25, crit)
        self.assertIn(5, crit)


class CorrectedDependencies(unittest.TestCase):
    """Dependencies re-derived from the stated dates: the 'dates say, column does not' cells."""

    @classmethod
    def setUpClass(cls):
        cls.d = tg.load()
        cls.cal = tg.weekday_calendar()
        cls.net = tg.corrected_network(cls.d)
        cls.res = cpm.schedule(cls.net)
        cls.idx = tg.stated_index(cls.d, cls.cal)

    def test_early_starts_equal_the_stated_dates_up_to_31_and_one_day_earlier_after(self):
        for i in range(1, 32):
            self.assertEqual(self.res[i]["es"], self.idx[i][0], i)
        for i in range(32, 41):
            self.assertEqual(self.res[i]["es"] + 1, self.idx[i][0], i)

    def test_no_activity_starts_before_a_finish_to_start_predecessor_ends(self):
        for a in self.net:
            for p, lag in cpm.links(a):
                self.assertGreaterEqual(self.idx[a["id"]][0], self.idx[p][1] + lag, (a["id"], p))

    def test_only_two_leads_remain_and_they_are_start_to_start_plus_one(self):
        leads = {(a["id"], p): lag for a in self.net for p, lag in cpm.links(a) if lag}
        self.assertEqual(leads, {(2, 1): -2, (3, 1): -2})

    def test_cells_that_differ_from_both_readings_of_the_written_text(self):
        # the 7 cells whose written list is wrong whichever way '-' is read
        self.assertEqual(tg.corrected_cells(self.d, "range"), [8, 9, 10, 14, 15, 16, 27])

    def test_cells_that_differ_from_the_teams_own_endpoints_reading(self):
        self.assertEqual(tg.corrected_cells(self.d, "endpoints"), [4, 8, 9, 10, 14, 15, 16, 17, 27, 31, 39, 40])

    def test_critical_path_of_the_corrected_network(self):
        path = cpm.critical_path(self.net, self.res)
        self.assertEqual(path, [1, 3, 4, 5, 8, 10, 12, 16, 17, 18, 23, 25, 26, 27, 29, 31, 32, 34, 35, 36, 38, 39, 40])
        crit = sorted(i for i, r in self.res.items() if r["critical"])
        self.assertEqual(crit, [1, 3, 4, 5, 6, 8, 9, 10, 12, 13, 16, 17, 18, 23, 25, 26, 27, 29, 30, 31, 32, 34, 35, 36, 38, 39, 40])

    def test_explicit_text_for_the_spreadsheet(self):
        txt = tg.explicit_deps_text(self.net)
        self.assertEqual(txt[8], "5, 6")
        self.assertEqual(txt[10], "7, 8, 9")
        self.assertEqual(txt[2], "1 (inicio-a-inicio +1 día)")
        self.assertEqual(txt[1], "-")
        self.assertEqual(txt[27], "26")
        self.assertEqual(txt[17], "11, 12, 13, 14, 15, 16")


class WorkingDayGap(unittest.TestCase):
    def test_gap_between_stated_end_and_cpm_is_explained_by_the_missing_link_net_of_the_leads(self):
        d = tg.load()
        cal = tg.weekday_calendar()
        g = tg.gap_explanation(d, cal)
        self.assertEqual(g["stated_total"], 131)
        self.assertEqual(g["as_written_total"], 126)
        self.assertEqual(g["with_link_strict_total"], 139)
        self.assertEqual(g["leads_saved"], 9)        # 139 strict FS vs 130 with the leads
        self.assertEqual(g["idle_days"], 1)          # 130 vs 131
        self.assertEqual(g["with_link_strict_total"] - g["leads_saved"] + g["idle_days"], g["stated_total"])


if __name__ == "__main__":
    unittest.main()
