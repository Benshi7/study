"""data.py must mirror the team's real Gantt (written before the data change)."""
import datetime as dt
import unittest

import data as D
import team_gantt as tg


class ActivitiesMirrorTheExcel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.team = tg.load()
        cls.acts = {a["id"]: a for a in D.ACTIVITIES}

    def test_same_ids_names_durations_and_dates(self):
        self.assertEqual(sorted(self.acts), list(range(1, 41)))
        for t in self.team["activities"]:
            a = self.acts[t["id"]]
            self.assertEqual((a["name"], a["dur"], a["start"], a["end"]), (t["name"], t["dur"], t["start"], t["end"]), t["id"])
            self.assertEqual(a["deps_raw"], t["deps_raw"])

    def test_predecessors_use_the_reading_that_matches_the_teams_cpm(self):
        for t in self.team["activities"]:
            self.assertEqual(self.acts[t["id"]]["preds"], tg.parse_deps(t["deps_raw"], "endpoints"), t["id"])

    def test_phase_numbers_follow_the_excel_phase_names(self):
        for t in self.team["activities"]:
            self.assertEqual(tg.PHASES[self.acts[t["id"]]["phase"] - 1], t["phase"], t["id"])
        self.assertEqual(self.acts[36]["phase"], 7)   # Monitoreo inicial belongs to Implementación in the Excel

    def test_no_invented_three_point_estimates_in_the_base_data(self):
        for a in D.ACTIVITIES:
            for k in ("o", "m", "p"):
                self.assertNotIn(k, a)


class PhasesAndGates(unittest.TestCase):
    def test_gate_dates_and_names_are_the_excel_hitos(self):
        team = tg.load()
        self.assertEqual(len(D.PHASES), 8)
        for ph, h in zip(D.PHASES, team["hitos"]):
            self.assertEqual(ph[4], h["date"])
            self.assertEqual(ph[5], h["name"])
        self.assertEqual(D.GATES["G2"], dt.date(2026, 5, 1))

    def test_the_declared_gate_dates_equal_the_excel_ones(self):
        self.assertEqual(D.GATES, D.GATES_DECLARED)

    def test_gate_activities_end_on_the_gate_date(self):
        ends = {a["id"]: a["end"] for a in D.ACTIVITIES}
        for ph in D.PHASES:
            self.assertEqual(max(ends[i] for i in D.PHASE_GATE_ACTS[ph[0]]), ph[4], ph[1])


class DeclaredInOtherDocuments(unittest.TestCase):
    def test_document_two_phase_windows_disagree_with_the_excel(self):
        diffs = tg.phase_window_differences(tg.load(), D.F2_PHASE_WINDOWS)
        names = {d["phase"] for d in diffs}
        self.assertEqual(names, {"Inicio", "Análisis", "Diseño", "Implementación", "Cierre"})
        saturday = [d for d in diffs if d["declared_start"].weekday() >= 5]
        self.assertEqual({d["phase"] for d in saturday}, {"Análisis", "Diseño"})

    def test_document_one_control_points_are_seven_not_eight(self):
        self.assertEqual(len(D.CHARTER_GATES_6_5), 7)
        self.assertEqual(len(tg.load()["hitos"]), 8)


class OwnersByRole(unittest.TestCase):
    def test_every_activity_has_a_role_that_works_in_its_window(self):
        roles = {r[1]: set(r[4]) for r in D.TEAM_ROLES}
        for a in D.ACTIVITIES:
            role = D.ACTIVITY_OWNER[a["id"]]
            self.assertIn(role, roles, a["id"])
            self.assertIn(a["id"], roles[role], f"activity {a['id']} is outside the window of {role}")


class PertIllustration(unittest.TestCase):
    def test_illustration_is_anchored_on_the_teams_durations(self):
        team = {a["id"]: a for a in D.ACTIVITIES}
        self.assertGreaterEqual(len(D.PERT_EXAMPLE), 5)
        for r in D.PERT_EXAMPLE:
            self.assertLessEqual(r["o"], r["m"])
            self.assertLessEqual(r["m"], r["p"])
            self.assertEqual(r["m"], team[r["id"]]["dur"], r["id"])


if __name__ == "__main__":
    unittest.main()
