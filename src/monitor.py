import argparse
from pathlib import Path
import numpy as np
import pandas as pd

from .config import Paths

def psi(expected: pd.Series, actual: pd.Series, bins=10) -> float:
    # PSI between two distributions
    e = expected.dropna().astype(float)
    a = actual.dropna().astype(float)
    if len(e) == 0 or len(a) == 0:
        return np.nan

    quantiles = np.linspace(0, 1, bins+1)
    cuts = np.unique(np.quantile(e, quantiles))
    if len(cuts) < 3:
        return np.nan

    e_counts, _ = np.histogram(e, bins=cuts)
    a_counts, _ = np.histogram(a, bins=cuts)
    e_dist = np.clip(e_counts / e_counts.sum(), 1e-6, None)
    a_dist = np.clip(a_counts / a_counts.sum(), 1e-6, None)
    return float(np.sum((a_dist - e_dist) * np.log(a_dist / e_dist)))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scored", default=str(Paths().reports / "scored_sample.parquet"))
    ap.add_argument("--out", default=str(Paths().reports / "monitoring_summary.csv"))
    args = ap.parse_args()

    df = pd.read_parquet(args.scored)
    df["issue_month"] = pd.to_datetime(df["issue_dt"]).dt.to_period("M").astype(str)

    # Example: drift from early vintages to late vintages
    early = df[df["issue_month"] <= df["issue_month"].sort_values().iloc[len(df)//4]]
    late  = df[df["issue_month"] >= df["issue_month"].sort_values().iloc[3*len(df)//4]]

    candidates = [c for c in ["fico_mid","dti","revol_util_pct","annual_inc","credit_hist_mths","pd_hat"] if c in df.columns]
    rows = []
    for c in candidates:
        rows.append({"feature": c, "psi_early_vs_late": psi(early[c], late[c], bins=10)})

    out = pd.DataFrame(rows).sort_values("psi_early_vs_late", ascending=False)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)
    print(out.head(10))

if __name__ == "__main__":
    main()
