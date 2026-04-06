from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPO_ROOT / "README.md"
FUNDING_PATH = REPO_ROOT / ".github" / "FUNDING.yml"
ALIPAY_QR_PATH = REPO_ROOT / "docs" / "assets" / "donate" / "alipay.jpg"
WECHAT_QR_PATH = REPO_ROOT / "docs" / "assets" / "donate" / "wechat.jpg"


class RepositoryMetadataContractTest(unittest.TestCase):
    def test_readme_exposes_donate_section(self) -> None:
        source = README_PATH.read_text(encoding="utf-8")

        self.assertIn('## <a id="donate"></a>赞助支持', source)
        self.assertIn("Sponsor", source)
        self.assertIn("docs/assets/donate/alipay.jpg", source)
        self.assertIn("docs/assets/donate/wechat.jpg", source)
        self.assertIn("## 功能简介", source)
        self.assertIn("## 已验证流程", source)

    def test_funding_links_to_readme_donate_anchor(self) -> None:
        source = FUNDING_PATH.read_text(encoding="utf-8")

        self.assertIn("custom:", source)
        self.assertIn(
            "https://github.com/Etherstrings/openclaw-gemini-web-skill#donate", source
        )

    def test_donate_images_exist(self) -> None:
        self.assertTrue(ALIPAY_QR_PATH.is_file())
        self.assertTrue(WECHAT_QR_PATH.is_file())


if __name__ == "__main__":
    unittest.main()
