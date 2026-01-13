# 2) Data preparation and leakage controls

## Leakage rule
Only variables available **at application/approval time** may be used as model features.

## Target mapping (recommended)
- BAD=1: Charged Off, Default, Does not meet credit policy. Status:Charged Off
- GOOD=0: Fully Paid, Does not meet credit policy. Status:Fully Paid
- Exclude: Current, Late, In Grace Period

## Leakage blacklist (drop from features)
Typical post-origination fields in Lending Club files include:
- Payment aggregates: total_pymnt*, total_rec_*, recoveries, collection_recovery_fee
- Outstanding principal: out_prncp*
- Post-origination dates: last_pymnt_d, next_pymnt_d, last_credit_pull_d
- Hardship/settlement program fields: hardship_*, settlement_*, debt_settlement_*

The pipeline enforces a conservative drop list and logs the removed columns for review.

## Split strategy
Use a **time-based split** by `issue_d`:
- Train: vintages prior to a cut date
- Test: later vintages
This approximates how performance is measured in production and reduces leakage from policy drift.
