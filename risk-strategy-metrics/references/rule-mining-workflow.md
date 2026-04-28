# Rule-Mining Workflow (No LR/XGBoost)

Use this workflow when the goal is strategy/rule discovery rather than model training.

## 1) Input Contract

Typical required columns:
- `application_no` (primary key)
- `borrower_no`
- `apply_dt`
- `Adm` (`0` reject, `1` approve)
- `bg_flag` (`0` good/normal, `1` bad/overdue, `2` not matured)
- `loan_no`
- `loan_amt`
- `outstanding_print_amt`
- feature columns (`feature_table`)

Suggested validations:
- `application_no` is unique and non-null.
- `Adm` in `{0,1}`, `bg_flag` in `{0,1,2}`.
- Amount fields are numeric.

## 2) EDA Output

Report at least:
- Apply count, apply people count, pass count, pass rate.
- Disbursement count, disbursement amount, outstanding principal.
- Overdue people count, overdue people rate.
- Overdue amount, overdue amount rate (`overdue_outstanding / disbursed_amount`).

Note:
- In "approve then immediate disbursement" products, only `Adm=1` has `loan_no` and repayment outcomes.

## 3) Feature Descriptive Stats

For each numeric feature, output:
- `count` (non-missing count)
- `miss` (missing count)
- `max`, `min`, `avg`
- `p10`, `p25`, `p50`, `p75`, `p90`

## 4) Binning Rules (toad-first)

Population for binning:
- Usually approved samples (`Adm=1`).
- For IV/KS label calculations, exclude not-mature records when required (for example drop `bg_flag=2`).

Binning method:
- Keep `MISSING` as one dedicated bin.
- Apply `toad.transform.Combiner(method='chi')` to remaining non-missing values (including 0).
- Target bins: `<=5`; hard max `8`.

Practical note:
- If `toad` cannot cleanly handle a corner case, use custom merge/post-processing but keep output format unchanged.

## 5) Bin-Level and Feature-Level Metrics

Per-bin table fields:
- `feature`, `bin_label`, `count`, `bad_cnt`, `good_cnt`
- `bad_rate` (`bad_cnt / count`)
- `woe`, `iv_bin`
- cumulative bad/good rates and `ks_bin`

Feature summary fields:
- `feature`, `iv`, `ks`, `is_monotonic`, `bin_cnt`
- sort by `iv` descending
- Monotonicity rule: exclude the `MISSING` bin first; judge monotonicity on the remaining bins.

Metric APIs:
- IV: `toad.stats.IV(...)`
- KS: `toad.metrics.KS(...)`

## 6) Single-Rule Threshold Mining (TopN by IV)

For TopN features by IV:
- Scan thresholds using `<=t` and `>t`.
- Output for each threshold:
  - sample count / sample ratio
  - bad count / good count
  - bad rate
  - lift (`segment_bad_rate / base_bad_rate`)

## 7) Recommended Deliverables

Example output files:
- `eda_overall_summary.csv`
- `eda_loan_risk_summary.csv`
- `feature_descriptive_stats.csv`
- `feature_bins_analysis.csv`
- `feature_bins_summary.csv`
- `single_rule_lift_topn.csv`

If user asks for a repo script convention, implement in the requested code folder and keep CLI arguments for input/output paths and bin controls.
