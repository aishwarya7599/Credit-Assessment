# Executive Summary (template)

## Business objective
Predict PD at origination to improve risk-adjusted profit: reduce losses while maintaining approvals.

## Data and approach
- Dataset: Lending Club originated loans (2007–2018)
- Target: Fully Paid vs Charged Off/Default (final outcomes only)
- Leakage controls: removed post-origination servicing variables; used application-time features only
- Validation: time-based split (train pre-2017, test 2017+)

## Results (fill after training)
- ROC-AUC: __
- PR-AUC: __
- Brier score: __
- Recommended approval threshold: __ (based on profit optimization assumptions)

## Key insights
1. Top drivers: __
2. High-risk segments: __
3. Operational recommendation: __

## Monitoring plan
PSI, tier-mix, observed bad rate by band/vintage, calibration drift.
