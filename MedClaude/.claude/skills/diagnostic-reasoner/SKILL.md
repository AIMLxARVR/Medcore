---
name: diagnostic-reasoner
description: >
  Clinical diagnostic reasoning skill for MedCore+. Use this skill whenever Claude is
  building or evaluating differential diagnoses, interpreting symptoms in clinical context,
  working with ICD-10 codes, or reasoning through any medical diagnostic scenario.
  Trigger on: "differential", "diagnosis", "what could cause", "clinical presentation",
  "rule out", "workup", "symptom", "lab value", "imaging finding". Do not skip this skill
  for any medical reasoning task — it encodes critical safety and accuracy patterns.
---

# Diagnostic Reasoning Skill

## Core reasoning framework

Always apply this sequence:
1. **Illness script matching** — match presentation to prototypical disease patterns
2. **Bayesian updating** — adjust probability with each new piece of evidence
3. **Anchoring check** — explicitly ask "what am I missing?"
4. **Cannot-miss scan** — always consider life-threatening mimics

## Confidence language mapping

| Confidence | Language to use |
|---|---|
| > 0.85 | "strongly consistent with", "most likely" |
| 0.6–0.85 | "suggestive of", "may represent" |
| 0.4–0.6 | "possible", "cannot exclude" |
| < 0.4 | "less likely but worth considering" |

Never use: "is", "confirms", "rules out" (without testing)

## ICD-10 coding rules
- Symptom codes (R-codes) for unconfirmed diagnoses
- Disease codes only after diagnostic confirmation
- Always include in output — no exceptions

## Red flag pattern library
See `references/red-flags.md` for the full list.

## Evidence grading
When citing literature: Grade A (RCT), B (cohort), C (case series), D (expert opinion)
Always disclose evidence grade in recommendations.

## Output schema
Always return structured JSON. See `references/output-schema.md`.
