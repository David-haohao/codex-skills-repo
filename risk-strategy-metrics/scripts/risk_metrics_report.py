#!/usr/bin/env python3
"""Generate AUC/KS/PSI summary for risk model scores."""

from __future__ import annotations

import argparse
import json
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve


EPS = 1e-10


def ks_from_scores(y_true: np.ndarray, score: np.ndarray) -> Tuple[float, float]:
    fpr, tpr, thresholds = roc_curve(y_true, score)
    diff = tpr - fpr
    idx = int(np.argmax(diff))
    return float(diff[idx]), float(thresholds[idx])


def make_quantile_bins(base_score: pd.Series, n_bins: int) -> np.ndarray:
    quantiles = np.linspace(0.0, 1.0, n_bins + 1)
    cuts = np.quantile(base_score.to_numpy(), quantiles)
    cuts = np.unique(cuts)

    if cuts.size < 2:
        min_v = float(base_score.min())
        max_v = float(base_score.max())
        if min_v == max_v:
            max_v = min_v + 1.0
        cuts = np.array([min_v, max_v], dtype=float)

    cuts[0] = -np.inf
    cuts[-1] = np.inf
    return cuts


def psi(base_score: pd.Series, oot_score: pd.Series, n_bins: int = 10) -> float:
    bins = make_quantile_bins(base_score, n_bins)
    base_bucket = pd.cut(base_score, bins=bins, include_lowest=True)
    oot_bucket = pd.cut(oot_score, bins=bins, include_lowest=True)

    base_dist = base_bucket.value_counts(normalize=True, sort=False).to_numpy(dtype=float)
    oot_dist = oot_bucket.value_counts(normalize=True, sort=False).to_numpy(dtype=float)

    base_dist = np.clip(base_dist, EPS, None)
    oot_dist = np.clip(oot_dist, EPS, None)

    return float(np.sum((oot_dist - base_dist) * np.log(oot_dist / base_dist)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Risk metrics report for score/probability columns.")
    parser.add_argument("--dev-csv", required=True, help="Development sample CSV path.")
    parser.add_argument("--target-col", required=True, help="Binary target column in dev sample.")
    parser.add_argument("--score-col", required=True, help="Score/probability column in dev sample.")
    parser.add_argument("--oot-csv", help="Optional OOT sample CSV path for PSI.")
    parser.add_argument("--oot-score-col", help="OOT score column; defaults to --score-col.")
    parser.add_argument("--bins", type=int, default=10, help="PSI quantile bins, default 10.")
    parser.add_argument("--sep", default=",", help="CSV delimiter, default ','.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    dev = pd.read_csv(args.dev_csv, sep=args.sep)
    y = dev[args.target_col].to_numpy()
    s = dev[args.score_col].to_numpy()

    auc = float(roc_auc_score(y, s))
    ks, ks_threshold = ks_from_scores(y, s)

    result = {
        "dev_auc": auc,
        "dev_ks": ks,
        "dev_ks_threshold": ks_threshold,
    }

    if args.oot_csv:
        oot = pd.read_csv(args.oot_csv, sep=args.sep)
        oot_col = args.oot_score_col or args.score_col
        psi_value = psi(dev[args.score_col], oot[oot_col], n_bins=args.bins)
        result["psi"] = psi_value

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

