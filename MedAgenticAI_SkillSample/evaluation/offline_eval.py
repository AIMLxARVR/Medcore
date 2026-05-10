"""
MedCore+ Offline Evaluation Pipeline
Run against golden_dataset.json to measure diagnostic accuracy.
"""
import json
import argparse
from pathlib import Path
from dataclasses import dataclass
import structlog

log = structlog.get_logger()


@dataclass
class EvalResult:
    case_id: str
    top1_correct: bool
    top3_correct: bool
    urgency_correct: bool
    escalation_correct: bool
    cannot_miss_covered: bool
    icd10_present: bool
    confidence_calibrated: bool


def run_eval(dataset_path: str) -> None:
    cases = json.loads(Path(dataset_path).read_text())
    results: list[EvalResult] = []

    log.info("eval.start", n_cases=len(cases))

    for case in cases:
        # TODO: call the diagnostic pipeline and compare output
        log.info("eval.case", case_id=case["case_id"])

    # Aggregate metrics
    if results:
        top1_acc = sum(r.top1_correct for r in results) / len(results)
        top3_acc = sum(r.top3_correct for r in results) / len(results)
        escalation_acc = sum(r.escalation_correct for r in results) / len(results)

        print(f"\n{'='*50}")
        print(f"MedCore+ Eval Results — {len(results)} cases")
        print(f"{'='*50}")
        print(f"Top-1 Accuracy:     {top1_acc:.1%}")
        print(f"Top-3 Accuracy:     {top3_acc:.1%}")
        print(f"Escalation Acc:     {escalation_acc:.1%}")
        print(f"{'='*50}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="evaluation/golden_dataset.json")
    args = parser.parse_args()
    run_eval(args.dataset)
