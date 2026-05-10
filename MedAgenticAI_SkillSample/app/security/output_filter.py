"""
MedCore+ Output Filter — Layer 3 of 3 security filters.
Validates all LLM output before it reaches clinicians.
"""
import re
from dataclasses import dataclass
import structlog

log = structlog.get_logger()

# Dangerous definitive language patterns
_DEFINITIVE_LANGUAGE = [
    r"\b(is|are) (definitely|certainly) (caused by|due to)\b",
    r"\brules? out\b",
    r"\bconfirms?\b",
    r"\bdiagnosis is\b(?! (?:uncertain|unclear|pending))",
]

# Hallucination risk: fabricated drug doses
_DOSE_PATTERN = r"\b\d+\s*(?:mg|mcg|mEq|units?|IU)\b"

_DISCLAIMER = (
    "\n\n---\n"
    "⚠️ **This report is AI-generated and requires clinician review before any clinical action.**\n"
    "MedCore+ Diagnostic AI | Not a substitute for professional medical judgment."
)


@dataclass
class OutputFilterResult:
    passed: bool
    modified: bool
    issues: list[str]
    output: str


class OutputFilter:
    """Validates and enriches LLM output before delivery."""

    def check(self, text: str) -> OutputFilterResult:
        issues = []
        output = text
        modified = False

        # Check for definitive language
        for pattern in _DEFINITIVE_LANGUAGE:
            if re.search(pattern, text, re.IGNORECASE):
                issues.append(f"Definitive language: {pattern}")

        # Check disclaimer is present
        if "AI-generated" not in text and "clinician review" not in text:
            output += _DISCLAIMER
            modified = True
            log.info("output_filter.disclaimer_added")

        # Check dose mentions (flag, don't block — clinician reviews)
        dose_mentions = re.findall(_DOSE_PATTERN, text)
        if dose_mentions:
            issues.append(f"Drug doses present (requires pharmacist review): {dose_mentions[:3]}")

        passed = len([i for i in issues if "Definitive" in i]) == 0

        if not passed:
            log.warning("output_filter.failed", issues=issues)

        return OutputFilterResult(
            passed=passed,
            modified=modified,
            issues=issues,
            output=output,
        )
