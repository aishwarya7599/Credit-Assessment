# Credit Risk Assessment (PD Modeling) — Lending Club (Capital One Senior Business Analyst–style)

## Executive framing
This project builds an **application-time Probability of Default (PD) model** and translates the model into **risk tiers, approval thresholds, and pricing guidance**. The end deliverable is a decisioning approach that improves **risk-adjusted profitability** while maintaining competitive approvals.

This is intentionally structured to mirror how **Capital One–style analytics teams** operate: rigorous problem definition, SQL-first feature building, careful leakage controls, time-based validation, clear business trade-offs, and a monitoring plan.

## Dataset
- Lending Club loan-level dataset (2.2M+ loans, 145 columns)
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

## How to run (local)
1. Place `loan.csv` under `data/raw/loan.csv` (or set `RAW_LOAN_CSV` env var).
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Build dataset (leakage-safe feature set, time split, optional sampling):
   ```bash
   python -m src.make_dataset --sample-frac 0.20
   ```
4. Train baseline + tree model, export artifacts:
   ```bash
   python -m src.train --model logistic
   python -m src.train --model hgb
   ```
5. Score + create risk tiers:
   ```bash
   python -m src.score --model-path models/model.joblib
   ```
6. Monitoring metrics (PSI + cohort loss curves):
   ```bash
   python -m src.monitor
   ```

## Outputs you should highlight in interviews
- **Time-based validation** and stability by vintage (avoids optimistic random split results)
- **Precision/Recall trade-off** aligned to business costs (approve-bad vs reject-good)
- **Calibration** (PD accuracy matters in credit)
- **Risk tiers** with explainable drivers and threshold recommendation
- **Monitoring plan** (drift + performance tracking)

## Notes for a Capital One Senior Business Analyst pitch
- Frame insights as decisions: “What threshold maximizes risk-adjusted profit?” “What segments deteriorate first in downturn-like conditions?”
- Emphasize governance: leakage controls, model card, monitoring, bias checks
- Speak in portfolio language: PD, LGD, EAD, expected loss, net charge-off rate, vintage curves

