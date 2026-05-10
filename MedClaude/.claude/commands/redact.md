---
description: Scan and redact PII from a file or directory before processing
---

# /redact

Run `python scripts/pii_redactor.py --path $ARGS`.

## What it redacts
- Patient names (NER-based)
- DOB, age if combined with name
- MRN, insurance ID, SSN patterns
- Phone numbers, email addresses
- Addresses

## Output
- Creates `<original>_redacted.<ext>` alongside original
- Prints redaction summary: count per category
- Logs audit trail to `observability/redaction_log.jsonl`

## Never modify the original file.
## Always verify output before downstream processing.
