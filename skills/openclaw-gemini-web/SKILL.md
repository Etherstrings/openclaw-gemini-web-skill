---
name: openclaw-gemini-web
version: 0.1.0
description: Use when the user wants OpenClaw to sign into Gemini Web, continue a Gemini browser session, chat with Gemini in the web UI, upload reference images, or generate and download Gemini images from the browser.
homepage: https://github.com/Etherstrings/openclaw-gemini-web-skill
metadata:
  openclaw:
    emoji: "🖼️"
    requires:
      bins: ["python3"]
---

# OpenClaw Gemini Web

Control the Gemini web UI through OpenClaw's browser tools.

This skill is for browser-driven Gemini work, not the Gemini API and not the Gemini CLI.

## What This Skill Covers

- Reuse Gemini login state in OpenClaw's dedicated browser profile
- Best-effort credential login when the user has provided account secrets to OpenClaw
- TOTP / 2FA code generation through `scripts/totp.py`
- Multi-turn text chats in Gemini Web
- Reference-image upload and browser-based image generation
- Downloading Gemini outputs into a stable local folder

## Login Policy

OpenClaw's own docs recommend manual login first. Follow this order:

1. Prefer an already-authenticated Gemini tab or an existing Gemini login in OpenClaw's managed browser profile.
2. If Gemini is not logged in and the environment already contains credentials, try a best-effort automated login.
3. If Google presents CAPTCHA, device confirmation, suspicious-login review, phone verification, or any page that cannot be completed safely by automation, stop and let the user complete it in the opened browser window.

Never ask the user to paste credentials into the chat if they already said OpenClaw has them.
Never echo passwords or TOTP secrets back into logs, markdown, or summaries.

## Credential Sources

Optional environment variables:

- `GEMINI_WEB_EMAIL`
- `GEMINI_WEB_PASSWORD`
- `GEMINI_WEB_TOTP_SECRET`
- `GEMINI_WEB_TOTP_URI`

If both `GEMINI_WEB_TOTP_URI` and `GEMINI_WEB_TOTP_SECRET` exist, prefer the URI.

`scripts/totp.py` accepts any one of these source styles:

- a plain Base32 secret
- an `otpauth://totp/...` URI
- a JSON file plus key name

Useful examples:

```bash
python3 {baseDir}/scripts/totp.py --env GEMINI_WEB_TOTP_SECRET
python3 {baseDir}/scripts/totp.py --env GEMINI_WEB_TOTP_URI
python3 {baseDir}/scripts/totp.py --secret JBSWY3DPEHPK3PXP
python3 {baseDir}/scripts/totp.py --uri 'otpauth://totp/Gemini:me@example.com?secret=JBSWY3DPEHPK3PXP&issuer=Gemini'
python3 {baseDir}/scripts/totp.py --json-file ~/.secrets/gemini.json --json-key totp
```

Resolve `{baseDir}` to this skill directory before using the script.

## Browser Workflow

### 1. Open Gemini

- Use OpenClaw's managed browser, not the user's daily profile.
- Navigate to `https://gemini.google.com/`.
- If Gemini is already usable, continue with the current tab and preserve thread state unless the user asked for a fresh thread.

### 2. Detect Login State

Treat Gemini as ready when the composer or chat UI is visible.
Treat it as unauthenticated when Google account forms, account chooser pages, or sign-in buttons are visible.

### 3. Best-Effort Automated Login

Only do this when the required environment values already exist:

- Fill the email identifier from `GEMINI_WEB_EMAIL`
- Fill the password from `GEMINI_WEB_PASSWORD`
- If prompted for a 2FA code:
  - generate a code with `scripts/totp.py`
  - fill the current code immediately

If any login step becomes ambiguous or Google changes the challenge flow unexpectedly, stop and ask the user to finish the challenge manually in the same browser window.

## Gemini Interaction Patterns

### Text Conversations

- Reuse the current Gemini thread when the user is refining the same task.
- Start a fresh Gemini thread when the user explicitly asks for "new chat", "fresh thread", or a clearly unrelated task.
- Wait for Gemini's response to finish before summarizing.

### Image Generation

- If Gemini exposes an image-generation toggle or mode switch, enable it before sending the prompt.
- If no explicit toggle is visible, send a clear image-generation prompt in the main composer.
- Upload reference images before the prompt when the user has provided local files.
- After generation, inspect the returned tiles and download the strongest candidate that best matches the user's latest instruction.

### Refinement Loops

- Keep the same thread for "make it warmer", "change the pose", "more like reference 2", and similar revisions.
- For failed generations, try one prompt refinement before escalating to the user.
- If Gemini starts drifting across too many edits, start a fresh thread and restate the latest approved prompt more cleanly.

## Output Handling

Default download folder:

```text
./output/gemini/YYYY-MM-DD/
```

If the user gives a different destination, use that instead.

After downloading:

1. Move the file into the target folder immediately if Gemini or the browser saved it elsewhere first.
2. Rename it to a stable, lowercase, hyphenated filename based on the prompt or user-supplied name.
3. Keep extensions intact when possible.
4. If multiple variants are downloaded, suffix them as `-01`, `-02`, and so on.

For repeated asset sessions, keep a short `session-notes.md` in the same folder only when the user asks for provenance or the batch is large enough to justify it.

## Recommended Response Style

- Tell the user when Gemini is already logged in versus when a login attempt is needed.
- If automation hits a Google safety wall, say that clearly and keep the browser ready for takeover.
- After each successful Gemini run, report:
  - whether this was a fresh thread or a continuation
  - what kind of output Gemini returned
  - where downloaded files were saved

## Hard Stops

Stop and ask the user to intervene when any of these happens:

- CAPTCHA
- phone approval prompt
- device review / suspicious sign-in page
- recovery email or phone challenge
- account locked / temporary block
- terms or policy interstitials that require human acceptance

## Trigger Examples

- "Log into Gemini for me and generate images from this prompt."
- "Use Gemini Web to continue the last thread and refine the picture."
- "Upload these references to Gemini and ask for three variants."
- "Open Gemini in OpenClaw, log in with the stored credentials, and download the best image."
