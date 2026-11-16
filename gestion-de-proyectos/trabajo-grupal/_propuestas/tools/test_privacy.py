"""Scans the shareable HTML for private references (written first)."""
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML = ROOT / "propuestas-de-mejora.html"
FORBIDDEN = [
    r"lecci[oó]n(?!es? )", r"\blecciones\b", r"clases/", r"raw/", r"\btp/", r"\bsuite\b", r"\bNOTES\b",
    r"\bagente\b", r"Claude", r"engram", r"/home/", r"_analisis", r"_propuestas", r"mapa de conceptos",
]


class PrivacyTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(HTML.exists(), "propuestas-de-mejora.html must be built first")
        self.text = HTML.read_text(encoding="utf-8")

    def test_no_private_terms(self):
        for pat in FORBIDDEN:
            hits = re.findall(pat, self.text, flags=re.I)
            # 'elección' contains 'lección'; allow it explicitly
            hits = [h for h in hits if h.lower() not in ("elección",)]
            self.assertEqual(hits, [], f"forbidden pattern {pat!r} found")

    def test_only_https_or_anchor_links(self):
        for m in re.finditer(r'(?:href|src)="([^"]*)"', self.text):
            url = m.group(1)
            self.assertTrue(url.startswith("https://") or url.startswith("#") or url.startswith("data:"), url)

    def test_no_local_script_or_css(self):
        self.assertIsNone(re.search(r'<script[^>]+src=', self.text))

    def test_amounts_are_in_usd_with_the_exchange_rate_declared(self):
        self.assertIn("USD", self.text)
        self.assertIsNone(re.search(r"\$\s?[\d.,]+ M\b", self.text), "ARS-million notation left in the HTML")
        self.assertIn("Tipo de cambio", self.text)
        self.assertIn("09/10/2026", self.text)

    def test_segment_is_households_and_all_items_are_votable(self):
        self.assertIn("Hogares de la Ciudad", self.text)
        self.assertNotIn("vecinos que reportan", self.text)
        self.assertGreaterEqual(len(re.findall(r"data-agree=", self.text)), 7)

    def test_no_phone_numbers(self):
        self.assertIsNone(re.search(r"\b\d{2}[\s-]?\d{4}[\s-]?\d{4}\b", self.text))


if __name__ == "__main__":
    unittest.main()
