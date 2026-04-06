from __future__ import annotations

import unittest
from pathlib import Path


SKILL_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "openclaw-gemini-web"
    / "SKILL.md"
)


class SkillMarkdownContractTest(unittest.TestCase):
    def test_declares_required_metadata_and_workflow_hints(self) -> None:
        source = SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn("name: openclaw-gemini-web", source)
        self.assertIn("description:", source)
        self.assertIn('bins: ["python3"]', source)
        self.assertIn("GEMINI_WEB_EMAIL", source)
        self.assertIn("GEMINI_WEB_PASSWORD", source)
        self.assertIn("GEMINI_WEB_TOTP_SECRET", source)
        self.assertIn("https://gemini.google.com/", source)
        self.assertIn("./output/gemini/YYYY-MM-DD/", source)


if __name__ == "__main__":
    unittest.main()
