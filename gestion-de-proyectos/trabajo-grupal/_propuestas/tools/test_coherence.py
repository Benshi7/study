"""Tests for cross-section coherence checks (written first)."""
import unittest

import coherence as co


class CoherenceTests(unittest.TestCase):
    def test_milestones_match(self):
        r = co.check_milestones({"G1": "2026-04-10", "G2": "2026-04-30"}, {"G1": "2026-04-10", "G2": "2026-04-30"})
        self.assertTrue(r.ok)

    def test_milestones_mismatch_reports_ids(self):
        r = co.check_milestones({"G1": "2026-04-10", "G2": "2026-05-01"}, {"G1": "2026-04-10", "G2": "2026-04-30"})
        self.assertFalse(r.ok)
        self.assertIn("G2", r.detail)

    def test_milestones_missing(self):
        r = co.check_milestones({"G1": "x"}, {"G1": "x", "G2": "y"})
        self.assertFalse(r.ok)

    def test_budget_total_matches(self):
        self.assertTrue(co.check_budget_total(charter_total=344.3, budget_total=344.3).ok)

    def test_budget_total_tolerance_is_tiny(self):
        self.assertFalse(co.check_budget_total(charter_total=344.3, budget_total=344.4).ok)

    def test_charter_risks_subset(self):
        self.assertTrue(co.check_subset("riesgos", ["R02", "R05"], ["R01", "R02", "R05"]).ok)

    def test_charter_risks_not_subset(self):
        r = co.check_subset("riesgos", ["R02", "R99"], ["R01", "R02"])
        self.assertFalse(r.ok)
        self.assertIn("R99", r.detail)

    def test_contingency_rule(self):
        self.assertTrue(co.check_contingency(contingency=10.0, emv_total=10.0).ok)
        self.assertFalse(co.check_contingency(contingency=10.0, emv_total=12.0).ok)

    def test_labour_from_gantt(self):
        # tolerance in months
        self.assertTrue(co.check_labour_months({"dev": 3.0}, {"dev": 3.0}).ok)
        self.assertFalse(co.check_labour_months({"dev": 3.0}, {"dev": 4.0}).ok)

    def test_stakeholders_consistent(self):
        r = co.check_stakeholders(charter=["Sponsor", "Hacienda"], matrix=["Sponsor", "Hacienda", "Vecinos"],
                                  comms=["Sponsor", "Hacienda", "Vecinos"])
        self.assertTrue(r.ok)

    def test_stakeholders_missing_in_comms(self):
        r = co.check_stakeholders(charter=["Sponsor"], matrix=["Sponsor", "Vecinos"], comms=["Sponsor"])
        self.assertFalse(r.ok)
        self.assertIn("Vecinos", r.detail)

    def test_bridge_phrases(self):
        self.assertTrue(co.check_bridges({"5": "Tomando como base el segmento…"}, ["5"]).ok)
        self.assertFalse(co.check_bridges({"5": ""}, ["5"]).ok)


if __name__ == "__main__":
    unittest.main()
