---
description: Analyze diff and write a conventional commit message
---

# /commit

Run `git status` and `git diff --staged`.
Identify the *why*, not the *what*.

## Format
- Subject: 50 chars max, imperative mood
- Prefix: MC-XXX: description
- Body: explain the clinical or technical reasoning
- Co-Authored-By: [current user]

## Never
- Push without asking
- Use --no-verify
- Commit files matching `*_redacted.*` or `*.env`
- Commit to main directly

## Slash commands = fastest UX.
