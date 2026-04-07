from __future__ import annotations

import unittest
from pathlib import Path


RUNBOOK_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "GEMINI_LOGIN_RUNBOOK.md"
)


class GeminiLoginRunbookContractTest(unittest.TestCase):
    def test_runbook_records_verified_login_and_region_diagnosis_baseline(self) -> None:
        source = RUNBOOK_PATH.read_text(encoding="utf-8")

        self.assertIn("结论先行", source)
        self.assertIn("已验证通过的基线", source)
        self.assertIn("真 Chrome 或 OpenClaw 托管浏览器", source)
        self.assertIn("This browser or app may not be secure", source)
        self.assertIn("Lightpanda", source)
        self.assertIn("#totpPin", source)
        self.assertIn("myaccount.google.com/personal-info", source)
        self.assertIn("Reply with exactly: READY", source)
        self.assertIn("READY", source)
        self.assertIn("地区问题", source)
        self.assertIn("登录问题", source)


if __name__ == "__main__":
    unittest.main()
