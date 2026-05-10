#!/usr/bin/env bash
# Scan every file Claude writes for PII patterns.
# Blocks commit if PII detected in output files.
# No prompt. No exception. Always fires.

FILE=$(jq -r .tool_input.file_path)

# Only check data output files
if [[ "$FILE" == data/processed/* ]] || [[ "$FILE" == *report* ]]; then
  python scripts/pii_redactor.py --scan-only --path "$FILE"
  EXIT_CODE=$?
  if [ $EXIT_CODE -ne 0 ]; then
    echo "ERROR: PII detected in $FILE. Redact before saving."
    exit 1
  fi
fi

# Hooks are your guardrails.
