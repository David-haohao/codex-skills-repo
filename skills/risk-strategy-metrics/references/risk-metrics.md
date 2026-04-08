# Risk Metric Reference

## 1. AUC

Definition:
- Area under ROC curve; measures ranking ability of good vs bad samples.

Interpretation:
- 0.5: random
- 0.6-0.7: weak to moderate
- 0.7-0.8: acceptable
- 0.8+: strong (depends on data and leakage risk)

## 2. KS

Definition:
- Maximum gap between cumulative bad rate and cumulative good rate across score thresholds.
- Equivalent implementation via `max(TPR - FPR)` from ROC points.

Interpretation:
- Higher KS indicates stronger separation.
- Threshold expectations vary by portfolio and sample design.

## 3. PSI

Definition:
- Population Stability Index measures distribution shift from baseline to current population.

Formula:
- PSI = sum((actual_i - expected_i) * ln(actual_i / expected_i))

Typical bucket method:
- Build bins on baseline score quantiles.
- Compute each bin proportion for baseline and current samples.
- Sum PSI term across bins.

Common guideline (not universal rule):
- <0.1: stable
- 0.1-0.25: moderate shift
- >0.25: significant shift; investigate drift source

## 4. IV

Definition:
- Information Value summarizes predictive power from WOE bins.

Formula:
- IV = sum((dist_good_i - dist_bad_i) * WOE_i)
- WOE_i = ln(dist_good_i / dist_bad_i)

Typical rough bands (portfolio dependent):
- <0.02: weak
- 0.02-0.1: useful
- 0.1-0.3: medium
- 0.3-0.5: strong
- >0.5: often suspicious; check leakage/overfit

## 5. WOE

Definition:
- Weight of Evidence transforms categorical or binned numeric values into monotonic risk-friendly values.

Good practice:
- Keep bins business-interpretable.
- Avoid tiny bins with unstable bad rates.
- Verify trend consistency between development and OOT.

## 6. Lift and Recall at Cutoff

Use when strategy needs reject/approve threshold decisions.

Report together:
- pass rate
- bad capture rate
- bad rate at selected threshold
- incremental lift vs random targeting

## 7. Practical Reporting Checklist

- Always include sample window and population definition.
- Separate discrimination, calibration, and stability statements.
- If KPI worsens, check whether cause is drift (PSI) or ranking degradation (AUC/KS).

