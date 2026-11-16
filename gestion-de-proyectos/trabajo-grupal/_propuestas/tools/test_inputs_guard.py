"""Guard (written first): every input read by this pack - the cátedra PDFs and the Charter template in raw/ and the team's
Design Thinking deck - must stay byte-identical to the hashes recorded in tools/inputs.sha256 (paths relative to the project root)."""
import hashlib
import pathlib
import unittest

TOOLS = pathlib.Path(__file__).resolve().parent
PROJECT = TOOLS.parent.parent.parent


class InputsGuard(unittest.TestCase):
    def test_inputs_are_byte_identical_to_the_recorded_hashes(self):
        lines = [l for l in (TOOLS / "inputs.sha256").read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertGreaterEqual(len(lines), 12)
        names = []
        for l in lines:
            digest, name = l.split("  ", 1)
            names.append(name)
            p = PROJECT / name
            self.assertTrue(p.exists(), f"{name} is missing")
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), digest, f"{name} was modified")
        self.assertIn("raw/Project_Charter_Template5.docx", names)
        self.assertIn("trabajo-grupal/Design Thinking - Mapa Interactivo GCBA.pdf", names)


if __name__ == "__main__":
    unittest.main()
