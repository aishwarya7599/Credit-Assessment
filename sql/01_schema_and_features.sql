-- Example warehouse schema (Postgres/Snowflake-like)
CREATE TABLE IF NOT EXISTS raw_lendingclub_loan (
  id BIGINT,
  issue_d VARCHAR,
  loan_status VARCHAR,
  loan_amnt DOUBLE PRECISION,
  term VARCHAR,
  emp_length VARCHAR,
  home_ownership VARCHAR,
  annual_inc DOUBLE PRECISION,
  verification_status VARCHAR,
  purpose VARCHAR,
  addr_state VARCHAR,
  dti DOUBLE PRECISION,
  fico_range_low INTEGER,
  fico_range_high INTEGER,
  delinq_2yrs DOUBLE PRECISION,
  inq_last_6mths DOUBLE PRECISION,
  open_acc DOUBLE PRECISION,
  pub_rec DOUBLE PRECISION,
  revol_bal DOUBLE PRECISION,
  revol_util VARCHAR,
  total_acc DOUBLE PRECISION,
  application_type VARCHAR,
  disbursement_method VARCHAR
);

-- A feature table built from raw with leakage-safe columns
CREATE TABLE IF NOT EXISTS model_features_pd AS
SELECT
  id,
  issue_d,
  CASE
    WHEN loan_status IN ('Charged Off','Default','Does not meet the credit policy. Status:Charged Off') THEN 1
    WHEN loan_status IN ('Fully Paid','Does not meet the credit policy. Status:Fully Paid') THEN 0
    ELSE NULL
  END AS y_default,
  loan_amnt,
  term,
  emp_length,
  home_ownership,
  annual_inc,
  verification_status,
  purpose,
  addr_state,
  dti,
  (fico_range_low + fico_range_high)/2.0 AS fico_mid,
  delinq_2yrs,
  inq_last_6mths,
  open_acc,
  pub_rec,
  revol_bal,
  NULLIF(REPLACE(revol_util,'%',''), '')::DOUBLE PRECISION AS revol_util_pct,
  total_acc,
  application_type,
  disbursement_method
FROM raw_lendingclub_loan
WHERE loan_status IN ('Charged Off','Default','Does not meet the credit policy. Status:Charged Off',
                      'Fully Paid','Does not meet the credit policy. Status:Fully Paid');
