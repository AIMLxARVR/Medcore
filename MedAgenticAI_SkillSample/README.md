# MedCore+ Diagnostic AI

> Clinical-grade AI diagnostic assistant. One Claude becomes a diagnostic team.

⚠️ **All AI outputs require clinician review before any clinical action.**

---

## Architecture

```
User query
    └── diagnostic-orchestrator
            ├── symptom-analyst        (parallel)
            ├── lab-interpreter        (parallel)
            └── imaging-reader         (parallel)
                        ↓
            differential-builder
            drug-checker               (parallel)
                        ↓
            triage-escalation          (if urgency > 0.7)
                        ↓
            report-generator
```

## Quick start

```bash
# Install plugin (once)
/plugin install medcore-diagnostic-ai

# Run a diagnosis
/diagnose

# Evaluate pipeline quality
/eval-pipeline

# Redact PII from a file
/redact --path data/raw/case_001.txt
```

## Key files

| File | Purpose |
|---|---|
| `CLAUDE.md` | AI instruction manual — project rules |
| `AGENTS.md` | Agent roster + spawn patterns |
| `.claude/settings.json` | Permissions, hooks, model |
| `.claude/agents/` | All subagent definitions |
| `.claude/commands/` | Slash commands |
| `.claude/hooks/` | Pre/post tool guardrails |
| `.claude/skills/` | Persistent capabilities |

## Safety guarantees

- 3-layer security: `input_guard` → LLM → `output_filter`
- PII redaction on all patient data
- All outputs include disclaimer + confidence scores
- Critical values trigger auto-escalation
- Audit log for all tool calls

## Docs

- `docs/architecture.md`
- `docs/api-reference.md`
- `docs/deployment.md`
