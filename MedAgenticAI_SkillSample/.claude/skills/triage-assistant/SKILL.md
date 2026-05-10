---
name: triage-assistant
description: >
  Clinical triage and urgency scoring skill for MedCore+. Use whenever Claude needs to
  assess urgency, determine escalation need, prioritize cases, or score clinical severity.
  Trigger on: "how urgent", "should I escalate", "triage", "priority", "emergency",
  "critical", "vital signs", "hemodynamic", "deteriorating". Always use this skill before
  any routing decision — safety depends on it.
---

# Triage Assistant Skill

## Urgency scoring (0.0–1.0)

| Score | Level | Action |
|---|---|---|
| 0.9–1.0 | Code Blue | Immediate — spawn triage-escalation agent |
| 0.7–0.9 | Emergent | Escalate within 15 min |
| 0.5–0.7 | Urgent | Escalate within 1 hour |
| 0.3–0.5 | Semi-urgent | Same-day review |
| 0.0–0.3 | Routine | Standard workup |

## Auto-escalate triggers (score = 1.0, no exceptions)
- Airway compromise
- Respiratory rate > 30 or < 8
- SpO2 < 88% on room air
- Systolic BP < 80
- GCS < 8 or acute change
- Chest pain + diaphoresis + dyspnea
- Signs of stroke (FAST positive)
- Active hemorrhage
- Anaphylaxis signs

## Pediatric adjustments
Vital sign thresholds differ by age. See `references/pediatric-vitals.md`.
Always flag if age < 2 years — auto-escalate to attending.

## Scoring algorithm
1. Vital signs → base score
2. Red flag symptoms → +0.2 per flag, max 1.0
3. Age/comorbidity modifiers
4. Delta from last visit (if available) → +0.1 per significant change

Document scoring rationale in output.
