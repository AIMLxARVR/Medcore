---
name: report-generator
description: >
  Clinical report generation skill. Use when Claude needs to write, format, or structure
  any medical diagnostic report, clinical summary, or patient-facing output in MedCore+.
  Trigger on: "generate report", "write summary", "document findings", "clinical note",
  "discharge summary", "diagnostic report". Enforces all compliance and safety formatting
  rules. Always use this skill — never write clinical reports from scratch without it.
---

# Report Generation Skill

## Report types supported
- Diagnostic Report (standard output)
- Triage Summary (urgent cases)
- Evidence Brief (literature-backed recommendations)
- Escalation Notice (for human handoff)

## Mandatory sections (all report types)
1. AI-generated disclaimer footer
2. Confidence score and uncertainty section
3. "Requires clinician review" statement
4. ICD-10 codes for all conditions mentioned
5. Evidence grade for any clinical recommendation

## Formatting rules
- Use structured Markdown + YAML frontmatter
- Clinician-facing: formal tone, no hedging on safety flags
- Uncertainty = explicit, never buried
- Reports > 500 words: include a TL;DR summary block at top

## PII handling
- All patient identifiers replaced with context_hash
- No names, DOBs, MRNs in any file output
- Run pii_redactor.py scan before finalizing

## Compliance checkboxes (mentally verify each)
- [ ] Disclaimer present
- [ ] Confidence scores on all differentials
- [ ] ICD-10 codes present
- [ ] Uncertainty section non-empty
- [ ] No PII in output
- [ ] Evidence grades cited where applicable
