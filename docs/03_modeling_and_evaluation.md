# 3) Modeling and evaluation

## Models
- Logistic regression (interpretable baseline)
- Histogram Gradient Boosting (strong non-linear baseline within scikit-learn)

## Metrics (credit-appropriate)
- ROC-AUC (ranking)
- PR-AUC (useful under class imbalance)
- Calibration / Brier score (PD quality)
- Confusion matrix at chosen threshold (operational impact)

## Business translation
Threshold selection is driven by a simple **expected value** model:
- Expected Loss (EL) = PD * LGD * EAD
- Expected Profit ≈ Expected Interest Income − EL − servicing cost (simplified)

The repo includes an example optimization routine to choose a threshold that maximizes profit under assumptions.
