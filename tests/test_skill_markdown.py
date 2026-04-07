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
        self.assertIn("version: 0.1.5", source)
        self.assertIn("description:", source)
        self.assertIn('bins: ["python3"]', source)
        self.assertIn("GEMINI_WEB_EMAIL", source)
        self.assertIn("GEMINI_WEB_PASSWORD", source)
        self.assertIn("GEMINI_WEB_TOTP_SECRET", source)
        self.assertIn("https://gemini.google.com/", source)
        self.assertIn("This browser or app may not be secure", source)
        self.assertIn("#totpPin", source)
        self.assertIn("https://myaccount.google.com/personal-info", source)
        self.assertIn("Reply with exactly: READY", source)
        self.assertIn("./output/gemini/YYYY-MM-DD/", source)
        self.assertIn("### 常规对话", source)
        self.assertIn("### 文件与图片上传", source)
        self.assertIn("### 文本分析、起草与研究", source)
        self.assertIn("### 4. 区分地区问题与登录问题", source)
        self.assertIn("Google Authenticator TOTP 流程", source)
        self.assertIn("续接或分叉 Gemini 线程", source)
        self.assertIn("上传文件和图片，让 Gemini 做分析", source)
        self.assertIn("向 Gemini 提问", source)
        self.assertIn("总结", source)
        self.assertIn("起草", source)
        self.assertIn("图片只是这个 skill 支持的一种模式", source)
        self.assertIn(
            "https://github.com/Etherstrings/openclaw-gemini-web-skill#donate", source
        )


if __name__ == "__main__":
    unittest.main()
