from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "openclaw-gemini-web"
    / "scripts"
    / "totp.py"
)


def load_totp_module():
    spec = importlib.util.spec_from_file_location("skill_totp", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load module from {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TotpScriptContractTest(unittest.TestCase):
    def test_generates_rfc6238_sha1_codes(self) -> None:
        totp = load_totp_module()
        secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"
        expectations = {
            59: "94287082",
            1111111109: "07081804",
            1111111111: "14050471",
        }

        for timestamp, expected in expectations.items():
            with self.subTest(timestamp=timestamp):
                self.assertEqual(
                    totp.generate_totp(secret, timestamp=timestamp, digits=8, algorithm="SHA1"),
                    expected,
                )

    def test_parses_otpauth_uri(self) -> None:
        totp = load_totp_module()
        config = totp.parse_totp_source(
            uri=(
                "otpauth://totp/Gemini:me@example.com"
                "?secret=JBSWY3DPEHPK3PXP"
                "&issuer=Gemini"
                "&algorithm=SHA1"
                "&digits=6"
                "&period=30"
            )
        )

        self.assertEqual(config.issuer, "Gemini")
        self.assertEqual(config.account_name, "me@example.com")
        self.assertEqual(config.secret_base32, "JBSWY3DPEHPK3PXP")
        self.assertEqual(config.algorithm, "SHA1")
        self.assertEqual(config.digits, 6)
        self.assertEqual(config.period, 30)

    def test_uses_defaults_for_plain_base32_secret(self) -> None:
        totp = load_totp_module()
        config = totp.parse_totp_source(secret="JBSWY3DPEHPK3PXP")

        self.assertEqual(config.secret_base32, "JBSWY3DPEHPK3PXP")
        self.assertEqual(config.algorithm, "SHA1")
        self.assertEqual(config.digits, 6)
        self.assertEqual(config.period, 30)


if __name__ == "__main__":
    unittest.main()
