#!/usr/bin/env bash
# Auto-format every file Claude edits.
# Fires after every PostToolUse. No questions asked.

FILE=$(jq -r .tool_input.file_path)

case "$FILE" in
  *.py)
    ruff format "$FILE" ;;
  *.ts|*.tsx|*.js|*.jsx)
    npx prettier --write "$FILE" ;;
  *.json)
    python -m json.tool "$FILE" --indent 2 > "$FILE.tmp" && mv "$FILE.tmp" "$FILE" ;;
  *.md)
    # no-op: markdown is intentionally unformatted
    ;;
esac

# Fires after every Edit.
# No questions asked.
