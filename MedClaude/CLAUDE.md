# MedCore+ Diagnostic AI — Project Instructions

## Overview
MedCore+ is a clinical-grade AI diagnostic assistant. It helps clinicians triage patients,
reason through differentials, and generate structured diagnostic reports.
Never replace clinical judgment. Always surface uncertainty.

---

## Code Standards & Conventions
- Python 3.11+, strict typing everywhere (`mypy --strict`)
- No `Any` types. Use `TypedDict`, `dataclasses`, or Pydantic models
- All LLM calls go through `services/llm_client.py` — never call Anthropic SDK directly
- Use `structlog` for all logging — never `print()`
- Pydantic v2 for all data validation

## Architecture
- FastAPI backend — async everywhere
- All agent logic lives in `app/agents/` — never in routes
- Prompts are versioned in `app/prompts/registry.py` — never hardcoded inline
- Security filters MUST wrap every LLM input and output
- RAG pipeline uses hybrid search (BM25 + dense) with a reranker

## Medical Domain Rules
- NEVER output a diagnosis without a confidence score and differential list
- ALWAYS include ICD-10 codes when referencing conditions
- Flag any out-of-distribution query to the `triage-escalation` agent
- Redact all PII before logging (patient name, DOB, MRN)

## Commit Format (after every change)
- MC-XXX: clear imperative description
- Co-Authored-By: [your name]
- Reference ticket in body

## Never
- Push to `main` without PR approval
- Skip the output_filter on any patient-facing response
- Hardcode API keys or credentials
- Use `rm -rf` on data directories

## Agent Orchestration
See AGENTS.md for the full agent roster and spawn patterns.
