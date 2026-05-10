---
description: Run the evaluation pipeline against the golden dataset
---

# /eval-pipeline

Run `python evaluation/offline_eval.py --dataset evaluation/golden_dataset.json`.
Compare outputs to expected differentials using scoring rubrics.

## Metrics computed
- Top-1 accuracy (correct diagnosis at rank 1)
- Top-3 accuracy (correct diagnosis in top 3)
- Critical-value detection rate
- Escalation precision/recall
- Mean confidence calibration error
- PII leakage scan

## Format
Print a results table per case, then aggregate stats.
Flag any regressions vs. last run (stored in `evaluation/eval_results/`).
Save results to `evaluation/eval_results/YYYY-MM-DD-HH-MM.json`.

## Slash commands = quality gates. Run before every release.
