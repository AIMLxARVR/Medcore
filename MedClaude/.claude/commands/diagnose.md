---
description: Run the full MedCore+ diagnostic pipeline on a clinical presentation
---

# /diagnose

Run `python app/main.py diagnose --interactive` to collect clinical inputs.
Identify patient context, chief complaint, symptoms, available labs and imaging.

## Pipeline
1. Validate input through `app/security/input_guard.py`
2. Spawn `diagnostic-orchestrator` with full context
3. Stream agent outputs to terminal as they complete
4. Write final report to `data/processed/reports/`
5. Log usage to `observability/cost_tracker.py`

## Format
- Print urgency score prominently at the top
- Use color coding: red = escalate, yellow = urgent, green = routine
- End with: report file path + token cost estimate

## Never
- Run without input validation
- Output report before output_filter passes
- Skip cost logging
