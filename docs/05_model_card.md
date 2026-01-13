# 5) Model card (condensed)

## Intended use
Application-time PD estimation for consumer unsecured loans, used for segmentation and decision support.

## Data
Lending Club originated loans (2007–2018). Labels derived from `loan_status` with ambiguous statuses excluded.

## Key limitations
- Dataset reflects Lending Club’s underwriting policies and economic conditions of the period.
- Missingness is non-random for some credit bureau variables.
- No direct protected-class demographics; fairness checks rely on proxies (e.g., geography) and should be interpreted cautiously.

## Governance
- Documented leakage blacklist
- Time-based validation
- Calibration checks
- Monitoring plan (PSI, stability, cohort loss)
