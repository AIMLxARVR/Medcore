"""
MedCore+ Input Guard — Layer 1 of 3 security filters.
Validates and sanitizes all clinical input before LLM processing.
"""
import re
from dataclasses import dataclass
import structlog

log = structlog.get_logger()

# PII patterns
_PII_PATTERNS = [
    (r"\b\d{3}-\d{2}-\d{4}\b", "SSN"),
    (r"\bMRN[:\s#]*\d+\b", "MRN"),
    (r"\b\d{10,}\b", "POTENTIAL_ID"),
    (r"\b[A-Z][a-z]+ [A-Z][a-z]+\b(?= (?:DOB|born|age \d))", "NAME_DOB_COMBO"),
]

# Prompt injection patterns
_INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"you are now",
    r"system prompt",
    r"<\|.*?\|>",
    r"OVERRIDE",
]


@dataclass
class GuardResult:
    passed: bool
    pii_detected: list[str]
    injection_detected: bool
    token_count: int
    sanitized_text: str
    rejection_reason: str | None = None


class InputGuard:
    """
    Validates clinical queries before they reach the LLM.
    All inputs must pass this guard.
    """

    def __init__(self, max_tokens: int = 8000, pii_scan: bool = True):
        self.max_tokens = max_tokens
        self.pii_scan = pii_scan

    def check(self, text: str) -> GuardResult:
        pii_found = []
        sanitized = text

        # Check length (rough token estimate: chars / 4)
        token_estimate = len(text) // 4
        if token_estimate > self.max_tokens:
            return GuardResult(
                passed=False,
                pii_detected=[],
                injection_detected=False,
                token_count=token_estimate,
                sanitized_text=text,
                rejection_reason=f"Input too long: ~{token_estimate} tokens",
            )

        # PII scan
        if self.pii_scan:
            for pattern, label in _PII_PATTERNS:
                if re.search(pattern, text, re.IGNORECASE):
                    pii_found.append(label)
                    sanitized = re.sub(pattern, f"[{label}_REDACTED]", sanitized, flags=re.IGNORECASE)

        # Injection scan
        injection = any(
            re.search(p, text, re.IGNORECASE) for p in _INJECTION_PATTERNS
        )
        if injection:
            log.warning("input_guard.injection_attempt", text_preview=text[:100])
            return GuardResult(
                passed=False,
                pii_detected=pii_found,
                injection_detected=True,
                token_count=token_estimate,
                sanitized_text=sanitized,
                rejection_reason="Potential prompt injection detected",
            )

        if pii_found:
            log.warning("input_guard.pii_detected", types=pii_found)

        return GuardResult(
            passed=True,
            pii_detected=pii_found,
            injection_detected=False,
            token_count=token_estimate,
            sanitized_text=sanitized,
        )
