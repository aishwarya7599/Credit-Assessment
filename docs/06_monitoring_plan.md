# 6) Monitoring plan

## What to monitor (monthly)
1. **Data drift**: PSI for top features (e.g., FICO, DTI, utilization proxies)
2. **Score drift**: PD distribution shift, tier mix
3. **Performance**: observed bad rate by score band (with maturation lag)
4. **Calibration**: predicted PD vs observed default by band/vintage

## Alerting thresholds (example)
- PSI > 0.2: investigate; PSI > 0.3: potential action
- Tier mix shift > 10% relative: review policy/channel mix
- Bad rate uplift vs expectation: tighten threshold / increase verification
