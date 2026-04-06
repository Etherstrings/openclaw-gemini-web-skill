# OpenClaw Gemini Web Skill

An OpenClaw skill project for driving the Gemini web UI through OpenClaw's managed browser.

## What It Does

- reuses Gemini login state in OpenClaw's browser profile
- performs best-effort credential login when secrets already exist in the OpenClaw run
- generates TOTP / 2FA codes without third-party dependencies
- supports Gemini text chat, thread continuation, file and image uploads, analysis and drafting tasks, image generation, and download handling

## Verified Flow

This project has been exercised end to end in a clean OpenClaw browser profile:

- Google account email step
- Google password step
- Google Authenticator TOTP / two-factor verification
- Gemini web app entry at `https://gemini.google.com/app`
- successful prompt and response round-trip inside Gemini

## Project Layout

```text
skills/openclaw-gemini-web/
  SKILL.md
  scripts/totp.py
tests/
  test_totp.py
```

## Local Validation

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
openclaw skills list
openclaw skills info openclaw-gemini-web
```

Run the OpenClaw commands from this repository root so the workspace-level `skills/` folder is visible.

## TOTP Helper

Examples:

```bash
python3 skills/openclaw-gemini-web/scripts/totp.py --secret JBSWY3DPEHPK3PXP
python3 skills/openclaw-gemini-web/scripts/totp.py --env GEMINI_WEB_TOTP_SECRET
python3 skills/openclaw-gemini-web/scripts/totp.py --uri 'otpauth://totp/Gemini:me@example.com?secret=JBSWY3DPEHPK3PXP&issuer=Gemini'
```

## Publish To ClawHub

```bash
clawhub publish skills/openclaw-gemini-web \
  --slug openclaw-gemini-web \
  --name "OpenClaw Gemini Web" \
  --version 0.1.2 \
  --changelog "Document verified Google password + TOTP login flow and Gemini interaction round-trip"
```
