# MedCore+ Agent Roster

All agents live in `.claude/agents/`. Each runs in isolation with its own context window.

---

## Orchestrator
**`diagnostic-orchestrator`** — Master coordinator. Decomposes incoming clinical queries,
routes to specialist agents, merges outputs into a final structured report.
Spawn first. Always.

---

## Diagnostic Agents

| Agent | File | Role |
|---|---|---|
| `symptom-analyst` | symptom-analyst.md | Extracts structured symptoms from free text |
| `differential-builder` | differential-builder.md | Generates ranked differential diagnoses |
| `lab-interpreter` | lab-interpreter.md | Interprets lab values in clinical context |
| `imaging-reader` | imaging-reader.md | Describes imaging findings from reports |
| `drug-checker` | drug-checker.md | Checks contraindications & interactions |
| `triage-escalation` | triage-escalation.md | Routes urgent/OOD cases to human review |
| `report-generator` | report-generator.md | Produces final structured diagnostic report |
| `literature-searcher` | literature-searcher.md | Retrieves relevant clinical evidence |

---

## Spawn Patterns

```
User query
    └── diagnostic-orchestrator
            ├── symptom-analyst        (parallel)
            ├── lab-interpreter        (parallel)
            └── imaging-reader         (parallel)
                        ↓
            differential-builder       (after above)
            drug-checker               (parallel with differential)
                        ↓
            triage-escalation          (if urgency > 0.7)
                        ↓
            report-generator           (final synthesis)
```

Each agent has: own tools, own permissions, own context.
One Claude becomes a diagnostic team.
