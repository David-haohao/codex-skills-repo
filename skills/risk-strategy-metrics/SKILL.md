---
name: risk-strategy-metrics
description: Credit risk strategy analysis workflow with toad for feature diagnostics, binning, WOE/IV transformation, model evaluation, and monitoring. Use when working on scorecard or binary default-risk tasks, especially for requests about AUC, KS, PSI, IV, Lift, variable screening, or stable feature engineering with Python.
---

# Risk Strategy Metrics

## Overview

Use this skill to run a practical risk-model analysis loop around `toad`, from data quality checks to model monitoring. Follow the sequence below unless the user requests only one specific metric.

When the user asks for **rule mining only** (not LR/XGBoost/scorecard training), switch to the dedicated rule-mining branch in this skill and skip modeling steps.

## Quick Start

1. Confirm binary target column and sample split (`dev` vs `oot` or `train` vs `test`).
2. Run data quality detection and feature filtering.
3. Build bins, transform to WOE, and perform variable selection.
4. Train baseline logistic regression.
5. Evaluate AUC/KS and inspect bad-rate monotonicity.
6. Monitor PSI and key metric drift across time windows.

For rule-mining-only tasks, see `references/rule-mining-workflow.md` and use this sequence:
1. Validate required business columns and analysis scope.
2. Produce EDA summary and feature descriptive statistics.
3. Bin approved samples with `toad` chi-binning (special bin for missing only).
4. Compute per-bin count/bad/good/bad_rate and feature-level IV/KS/monotonicity.
5. Rank by IV and run single-feature threshold lift scans on TopN features.

## Workflow

### 1) Validate Input and Data Scope

- Ensure target is binary (`0/1`) and define positive class explicitly.
- Prefer keeping an ID column for traceability, but exclude it from modeling.
- Separate development and validation windows before any fit/transform operation.

### 2) Diagnose Data with `toad`

Use `references/toad-workflow.md` for code snippets.

- Run `toad.detect(df)` for missing rate, uniqueness, and distribution checks.
- Run `toad.quality(df, target='target')` for IV and other quality signals.
- Use `toad.selection.select(...)` to remove high-missing, low-IV, and high-correlation features.

### 3) Binning and WOE Transformation

- Fit `toad.transform.Combiner` on development data.
- Check bin definitions and bad-rate trend; merge sparse/noisy bins if needed.
- Fit `toad.transform.WOETransformer` on binned dev data and apply the same transformer to validation/OOT.
- Never fit bins or WOE on test/OOT directly.

### 4) Variable Selection and Modeling

- Apply `toad.selection.stepwise(...)` on WOE features as a baseline screening step.
- Train logistic regression first; keep tree models as challenger models if requested.
- Preserve feature list and transformation artifacts for reproducibility.

### 5) Evaluation and Monitoring

Use `references/risk-metrics.md` for metric definitions and interpretation.

- Discrimination: AUC, KS, Lift/Recall at business cut points.
- Stability: PSI by score band and feature-level PSI.
- Explainability: IV ranking and WOE trend consistency.
- For quick calculation, run `scripts/risk_metrics_report.py`.

### 6) Reporting Standards

- Report all metrics with exact sample window and denominator definition.
- Distinguish model-fit metrics (`train/test`) from population-shift metrics (`dev/oot`).
- If thresholds are used (for KS, PSI, reject strategy), state the business context and expected trade-off.

## Rule-Mining Branch (Non-Modeling)

Use this branch when users explicitly say "rule mining", "single-rule threshold", "no LR/XGBoost", or data volume is too small for train/test/OOT.

Core requirements:
- No model training and no scorecard fitting.
- If data is very small, allow no train/test/OOT split when user confirms.
- Restrict binning/IV/KS to approved population when required by business logic (for example `Adm=1`).
- Exclude not-mature samples from performance labels when required (for example remove `bg_flag=2` from IV/KS).

Implementation guidance:
- Prefer `toad.transform.Combiner(method='chi')` for numeric bins.
- Keep missing as an explicit special bin before chi-binning the remaining non-missing values.
- Target compact bins (typically <=5), never exceed 8 bins.
- Use `toad.stats.IV` and `toad.metrics.KS` when feasible; custom post-processing is allowed for special-bin handling and reporting format.
- For monotonicity checks, exclude the missing bin and judge monotonicity on the remaining ordered bins.

Standard outputs for this branch:
- EDA summary (apply/pass/disbursement/overdue and amount-based rates).
- Feature descriptive statistics (include missing count).
- Per-feature bin detail table: `count`, `bad_cnt`, `good_cnt`, `bad_rate`, `IV/KS components`.
- Feature summary table: `IV`, `KS`, monotonicity flag, sorted by IV descending.
- TopN IV single-rule threshold lift table.

## References

- Read `references/toad-workflow.md` when implementing or debugging `toad`-based code.
- Read `references/risk-metrics.md` when users ask metric meaning, formula, interpretation, or threshold guidance.
- Read `references/rule-mining-workflow.md` for non-modeling rule-mining tasks and output templates.

## Script

- Run `python scripts/risk_metrics_report.py --help` for command options.
- Use the script for AUC/KS and PSI summary from score/probability columns.

