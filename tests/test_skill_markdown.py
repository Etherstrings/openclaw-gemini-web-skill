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
    def test_declares_required_metadata_and_general_gemini_web_scope(self) -> None:
        source = SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn("name: openclaw-gemini-web", source)
        self.assertIn("version: 0.1.2", source)
        self.assertIn("description:", source)
        self.assertIn('bins: ["python3"]', source)
        self.assertIn("GEMINI_WEB_EMAIL", source)
        self.assertIn("GEMINI_WEB_PASSWORD", source)
        self.assertIn("GEMINI_WEB_TOTP_SECRET", source)
        self.assertIn("https://gemini.google.com/", source)
        self.assertIn("./output/gemini/YYYY-MM-DD/", source)
        self.assertIn("General Conversations", source)
        self.assertIn("File And Image Uploads", source)
        self.assertIn("Text Analysis, Drafting, And Research", source)
        self.assertIn("Google Authenticator TOTP flow has been verified end to end", source)
        self.assertIn("continue or branch Gemini threads", source)
        self.assertIn("upload files for Gemini to analyze", source)
        self.assertIn("ask Gemini questions", source)
        self.assertIn("summarize", source)
        self.assertIn("draft", source)
        self.assertIn("Images are one supported mode", source)


if __name__ == "__main__":
    unittest.main()
