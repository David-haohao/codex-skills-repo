# Toad Workflow Notes

This reference condenses practical usage from the official toad tutorial.

## 1. Core Imports

```python
import toad
from toad.selection import select, stepwise
from toad.transform import Combiner, WOETransformer
```

## 2. Data Diagnosis

```python
eda = toad.detect(df)
quality = toad.quality(df, target='target')
```

Use these outputs to quickly check:
- missing and unique rates
- cardinality and suspicious constants
- IV-based signal strength

## 3. Feature Selection

```python
selected, dropped = select(
    df,
    target='target',
    empty=0.9,      # remove features with >90% missing
    iv=0.02,        # remove low-IV features
    corr=0.7,       # remove high-correlation features
    return_drop=True
)
```

Tune thresholds by business tolerance and sample size.

## 4. Binning

```python
combiner = Combiner()
combiner.fit(selected, y='target', method='chi', min_samples=0.05)

binned = combiner.transform(selected)
```

Use `combiner.export()` to inspect split points and keep versioned artifacts.

## 5. WOE Transformation

```python
woe_tr = WOETransformer()
woe_tr.fit(binned, binned['target'])
woe_df = woe_tr.transform(binned)
```

Apply the fitted `combiner` and `woe_tr` to validation/OOT data without refitting.

## 6. Stepwise Selection

```python
train_woe = woe_df.drop(columns=['target'])
step = stepwise(train_woe.join(woe_df['target']), target='target', direction='both')
```

Stepwise is a baseline filter. Keep domain constraints in final manual review.

## 7. Evaluation Utilities in toad

Typical tutorial flow includes:
- KS and AUC computation
- scorecard transformation utilities
- PSI checks for stability

Use this with your own model outputs and compare across time windows.

## 8. Scorecard Build (Optional)

```python
card = toad.ScoreCard(combiner=combiner, transer=woe_tr)
card.fit(X_train, y_train)
score = card.predict(X_test)
```

Build scorecard only after binning and WOE mapping are stable.

