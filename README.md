# Credit Risk Assessment (PD Modeling) — Lending Club

This project builds an **application-time Probability of Default (PD) model** and translates the model into **risk tiers, approval thresholds, and pricing guidance**. The end deliverable is a decisioning approach that improves **risk-adjusted profitability** while maintaining competitive approvals.

This is  structured to mirror how **analytics teams** operate: rigorous problem definition, SQL-first feature building, careful leakage controls, time-based validation, clear business trade-offs, and a monitoring plan.

## Dataset
- Lending Club loan-level dataset (1M+ loans, 145 columns)
- Time range: 2007–2018 (`issue_d`)
- Label: `loan_status` (mapped to default / non-default)

**Important**: Lending Club includes many post-origination servicing variables (payments, recoveries, last payment dates). Those are excluded from model inputs.

## What’s in this repo
- `src/` — reproducible pipeline: dataset build → model training → evaluation → scoring → monitoring
- `sql/` — schema + feature queries + monitoring queries (warehouse-ready)
- `docs/` — model card, leakage controls, business decisioning, monitoring plan
- `app/` — simple approval + tier + indicative pricing calculator (Streamlit)
- `reports/` — outputs (metrics, plots, scored sample)

## Target definition
For a clean PD model:
- **BAD (1)**: `Charged Off`, `Default`, and `Does not meet the credit policy. Status:Charged Off`
- **GOOD (0)**: `Fully Paid` and `Does not meet the credit policy. Status:Fully Paid`
- Excluded as ambiguous: `Current`, `Late (...)`, `In Grace Period`

