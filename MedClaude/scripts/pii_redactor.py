"""
MedCore+ PII Redactor
Scans and redacts patient identifiers from any text file.
"""
import re
import argparse
import json
from pathlib import Path
from datetime import datetime
import structlog

log = structlog.get_logger()

_PATTERNS = [
    (r"\b\d{3}-\d{2}-\d{4}\b", "SSN"),
    (r"\bMRN[:\s#]*\d+\b", "MRN"),
    (r"\b(DOB|Date of Birth)[:\s]+\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", "DOB"),
    (r"\b[A-Z][a-z]+ [A-Z][a-z]+\b(?=\s*,?\s*(?:DOB|MRN|born))", "PATIENT_NAME"),
    (r"\b\(\d{3}\) \d{3}-\d{4}\b", "PHONE"),
    (r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b", "EMAIL"),
]

_AUDIT_LOG = Path("observability/redaction_log.jsonl")


def redact(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for pattern, label in _PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            counts[label] = len(matches)
            text = re.sub(pattern, f"[{label}_REDACTED]", text, flags=re.IGNORECASE)
    return text, counts


def process_file(path: str, scan_only: bool = False) -> bool:
    p = Path(path)
    content = p.read_text()
    redacted, counts = redact(content)
    has_pii = bool(counts)

    if has_pii:
        log.warning("pii.detected", file=path, counts=counts)
        audit = {
            "timestamp": datetime.utcnow().isoformat(),
            "file": path,
            "pii_counts": counts,
            "scan_only": scan_only,
        }
        _AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(_AUDIT_LOG, "a") as f:
            f.write(json.dumps(audit) + "\n")

        if not scan_only:
            out_path = p.with_stem(p.stem + "_redacted")
            out_path.write_text(redacted)
            print(f"✓ Redacted: {out_path}")
            for label, count in counts.items():
                print(f"  {label}: {count} instance(s) redacted")
        else:
            print(f"⚠ PII found in {path}: {counts}")

    return has_pii


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    parser.add_argument("--scan-only", action="store_true")
    args = parser.parse_args()

    has_pii = process_file(args.path, args.scan_only)
    exit(1 if (args.scan_only and has_pii) else 0)
