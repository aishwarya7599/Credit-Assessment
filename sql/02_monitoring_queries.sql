-- Monitoring examples: score distribution and observed bad rates by vintage and score band
-- Assume a scored table 'loan_scores' with fields: id, issue_month, pd, risk_tier, y_default

-- 1) Tier mix by month
SELECT issue_month, risk_tier, COUNT(*) AS loans,
       COUNT(*)*1.0 / SUM(COUNT(*)) OVER (PARTITION BY issue_month) AS pct_of_month
FROM loan_scores
GROUP BY 1,2
ORDER BY 1,2;

-- 2) Observed default by pd band (matured loans only)
SELECT
  issue_month,
  WIDTH_BUCKET(pd, 0.0, 0.5, 10) AS pd_decile,
  AVG(y_default) AS observed_bad_rate,
  AVG(pd) AS avg_pred_pd,
  COUNT(*) AS n
FROM loan_scores
WHERE y_default IS NOT NULL
GROUP BY 1,2
ORDER BY 1,2;

-- 3) Simple PSI skeleton (feature-level PSI typically computed in Python)
