---
name: rule-analysis
description: Reconstruct and analyze rule-engine pass/reject performance on tabular data. Use when Codex needs to implement or audit admission rules, run pure rule-simulation backtesting from reject_code/rule-hit signals, compare with Adm when needed, and generate single-rule plus sequential funnel reports.
---

# Rule Analysis Workflow

Implement and validate a reproducible rule-analysis pipeline for CSV datasets.

## 1) Ground Inputs and Output Targets

1. Locate source data and expected output directories.
2. First-gate check: confirm entering samples have features/signals required to construct rules.
   - If reconstructing from feature conditions: verify required feature columns exist and are parseable.
   - If simulating from existing reject results: verify `reject_code` exists and rule codes are parseable.
3. Confirm required fields exist before coding.
4. Default to CLI parameters with sensible relative paths:
   - `--input` for source CSV
   - `--output` or `--output-dir` for report files

Fail fast if required columns are missing.

## 2) Reconstruct Rule Engine

1. Initialize per-row defaults:
   - `offline_Adm = 1`
   - `offline_reject_code = ""`
2. Define ordered rule list as `(reject_code, condition)` pairs.
3. Convert numeric fields with `pd.to_numeric(errors="coerce")`.
4. Evaluate rules in fixed order and accumulate matched reject codes with commas.
5. Set `offline_Adm = 0` when at least one rule hits.

Keep rule order deterministic, because output reject-code order depends on it.

## 3) Build Core Metrics

Generate at least these report layers:

1. Overall summary (can keep dual view)
   - Simulation view: `sample_cnt`, `offline_pass_cnt`, `offline_reject_cnt`, `offline_pass_rate`, `offline_reject_rate`
   - Optional Adm view: `adm_pass_cnt`, `adm_reject_cnt`, `adm_pass_rate`, `adm_reject_rate`
2. Single-rule summary (independent, simulation-only)
   - `rule_code`, `sample_cnt`, `hit_cnt`, `pass_nums`, `pass_pct`, `reject_pct`
   - Formulas: `pass_nums = sample_cnt - hit_cnt`; `pass_pct = pass_nums / sample_cnt`; `reject_pct = hit_cnt / sample_cnt`
3. Funnel summary (sequential, simulation-only)
   - step-wise `sample_cnt`, `hit_cnt`, `pass_nums`, `pass_pct`, `reject_pct`
   - Rule-order constraint: next-step `sample_cnt` must equal previous-step `pass_nums`
   - Optional diagnostics: `remaining_before_cnt`, `funnel_hit_cnt`, `funnel_hit_rate`
   - `cumulative_reject_cnt`, `cumulative_reject_rate`
   - `remaining_after_cnt`, `remaining_after_rate`

Use safe division to avoid divide-by-zero crashes.

## 4) Format and Export

1. Round ratio fields to 4 decimals.
2. Export CSV files in UTF-8.
3. Keep stable filenames for downstream usage, for example:
   - `rule_overall_summary.csv`
   - `rule_single_summary.csv`
   - `rule_funnel_summary.csv`

If exact display precision is required, format ratio columns as fixed 4-decimal strings before writing.

## 5) Validate Results

Run lightweight consistency checks after export:

1. Reject codes in output are all within the configured rule set.
2. Output row count matches input row count for row-level result tables.
3. Single-rule math is valid for every rule:
   - `sample_cnt - hit_cnt == pass_nums`
4. Funnel math is valid for every step:
   - `sample_cnt - hit_cnt == pass_nums`
   - next-step `sample_cnt == previous-step pass_nums`
5. Funnel math is monotonic:
   - `remaining_before_cnt - funnel_hit_cnt == remaining_after_cnt`
   - `cumulative_reject_cnt` is non-decreasing.
6. If `offline_Adm/offline_reject_code` are reconstructed, verify consistency:
   - `offline_Adm == 0` count equals non-empty `offline_reject_code` count.

Print concise run summary with input path, output paths, row counts, and key rates.
