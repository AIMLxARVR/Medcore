"""
MedCore+ Prompt Registry
Versioned, type-specific, hot-swappable prompts.
Never hardcode prompts inline — always use this registry.
"""
from dataclasses import dataclass
from enum import Enum


class PromptType(str, Enum):
    DIAGNOSTIC = "diagnostic"
    TRIAGE = "triage"
    REPORT = "report"
    LAB_INTERPRETATION = "lab_interpretation"
    DIFFERENTIAL = "differential"


@dataclass
class PromptTemplate:
    prompt_type: PromptType
    version: str
    system: str
    user_template: str  # use {variable} placeholders


_REGISTRY: dict[tuple[PromptType, str], PromptTemplate] = {}


def register(template: PromptTemplate) -> None:
    _REGISTRY[(template.prompt_type, template.version)] = template


def get(prompt_type: PromptType, version: str = "latest") -> PromptTemplate:
    if version == "latest":
        versions = [
            v for (pt, v) in _REGISTRY if pt == prompt_type
        ]
        if not versions:
            raise KeyError(f"No prompts registered for {prompt_type}")
        version = sorted(versions)[-1]
    key = (prompt_type, version)
    if key not in _REGISTRY:
        raise KeyError(f"Prompt not found: {prompt_type} v{version}")
    return _REGISTRY[key]


# Register all prompts below

register(PromptTemplate(
    prompt_type=PromptType.DIFFERENTIAL,
    version="1.0.0",
    system=(
        "You are a senior diagnostic physician at a tertiary care center. "
        "Generate a ranked differential diagnosis. Always include ICD-10 codes. "
        "Express confidence using calibrated language. "
        "Never use definitive language without diagnostic confirmation. "
        "This output will be reviewed by a clinician before any clinical action."
    ),
    user_template=(
        "Clinical presentation:\n{presentation}\n\n"
        "Structured symptoms:\n{symptoms_json}\n\n"
        "Lab values:\n{labs_json}\n\n"
        "Imaging findings:\n{imaging_summary}\n\n"
        "Generate a differential diagnosis following the MedCore+ output schema."
    ),
))

register(PromptTemplate(
    prompt_type=PromptType.TRIAGE,
    version="1.0.0",
    system=(
        "You are a triage specialist. Your job is to score urgency 0.0–1.0 "
        "and determine if immediate escalation is required. "
        "When in doubt, escalate. Safety over completeness."
    ),
    user_template=(
        "Patient presentation:\n{presentation}\n\n"
        "Vital signs:\n{vitals_json}\n\n"
        "Score urgency and provide escalation recommendation."
    ),
))
