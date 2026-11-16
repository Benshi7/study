"""Tests for risk scoring and EMV (written first)."""
import unittest

import risks


class LevelTests(unittest.TestCase):
    def test_level_bands_follow_team_scale(self):
        self.assertEqual(risks.level(1 * 4), "Bajo")
        self.assertEqual(risks.level(5), "Medio")
        self.assertEqual(risks.level(9), "Medio")
        self.assertEqual(risks.level(10), "Alto")
        self.assertEqual(risks.level(16), "Alto")
        self.assertEqual(risks.level(17), "Crítico")
        self.assertEqual(risks.level(25), "Crítico")

    def test_score(self):
        self.assertEqual(risks.score(4, 5), 20)

    def test_score_range(self):
        with self.assertRaises(ValueError):
            risks.score(0, 3)
        with self.assertRaises(ValueError):
            risks.score(3, 6)


class EmvTests(unittest.TestCase):
    SCALE = {
        "prob": {1: 0.10, 2: 0.30, 3: 0.50, 4: 0.70, 5: 0.90},
        "impact_pct_of_base": {1: 0.005, 2: 0.01, 3: 0.02, 4: 0.04, 5: 0.08},
    }

    def test_emv(self):
        self.assertAlmostEqual(risks.emv(0.5, 100.0), 50.0)

    def test_emv_from_scale(self):
        # P=4 -> 70 %, I=5 -> 8 % of a 100 base = 8 -> EMV 5.6
        self.assertAlmostEqual(risks.emv_from_levels(4, 5, base=100.0, scale=self.SCALE), 5.6)

    def test_totals_threats_only_vs_net(self):
        rows = [
            {"emv": 10.0, "kind": "amenaza"},
            {"emv": 4.0, "kind": "amenaza"},
            {"emv": 3.0, "kind": "oportunidad"},
        ]
        self.assertAlmostEqual(risks.total_emv(rows, mode="threats_only"), 14.0)
        self.assertAlmostEqual(risks.total_emv(rows, mode="net"), 11.0)

    def test_total_mode_validated(self):
        with self.assertRaises(ValueError):
            risks.total_emv([], mode="whatever")

    def test_sort_by_emv_desc_stable_ids(self):
        rows = [{"id": "R2", "emv": 1.0}, {"id": "R1", "emv": 5.0}, {"id": "R3", "emv": 5.0}]
        self.assertEqual([r["id"] for r in risks.sort_by_emv(rows)], ["R1", "R3", "R2"])


class ResidualTests(unittest.TestCase):
    def test_residual_never_exceeds_initial(self):
        with self.assertRaises(ValueError):
            risks.check_residual(p0=3, i0=4, p1=4, i1=4)

    def test_residual_ok(self):
        risks.check_residual(p0=4, i0=5, p1=2, i1=4)


if __name__ == "__main__":
    unittest.main()
