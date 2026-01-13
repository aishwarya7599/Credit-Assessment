import argparse
from pathlib import Path
import pandas as pd
import numpy as np
from .config import Paths, DEFAULT_TRAIN_END

GOOD = {"Fully Paid", "Does not meet the credit policy. Status:Fully Paid"}
BAD  = {"Charged Off", "Default", "Does not meet the credit policy. Status:Charged Off"}

LEAKAGE_PREFIXES = (
    "total_pymnt", "total_rec_", "recoveries", "collection_recovery_fee",
    "out_prncp", "last_pymnt", "next_pymnt", "last_credit_pull",
    "hardship_", "settlement_", "debt_settlement_", "pymnt_plan"
)

# A conservative, interview-safe feature set (application-time)
FEATURES = [
    "loan_amnt","term","emp_length","home_ownership","annual_inc","verification_status","purpose",
    "addr_state","dti","fico_range_low","fico_range_high","delinq_2yrs","inq_last_6mths",
    "open_acc","pub_rec","revol_bal","revol_util","total_acc","application_type","disbursement_method",
    "acc_open_past_24mths","avg_cur_bal","bc_util","all_util","mort_acc","num_rev_accts",
    "pct_tl_nvr_dlq","tot_cur_bal","total_rev_hi_lim","total_bc_limit",
    "earliest_cr_line","issue_d"
]

def _parse_issue_date(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, format="%b-%Y", errors="coerce")

def _parse_earliest(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, format="%b-%Y", errors="coerce")

def _clean_term(s: pd.Series) -> pd.Series:
    # ' 36 months' -> 36
    return pd.to_numeric(s.astype(str).str.extract(r"(\d+)")[0], errors="coerce")

def _clean_pct(s: pd.Series) -> pd.Series:
    # '13.56%' -> 13.56
    return pd.to_numeric(s.astype(str).str.replace("%","", regex=False), errors="coerce")

def build_dataset(raw_csv: Path, out_parquet: Path, sample_frac: float = 1.0) -> pd.DataFrame:
    # Load only necessary columns if they exist
    # Some columns are missing in certain file versions; use intersection.
    cols = pd.read_csv(raw_csv, nrows=0).columns.tolist()
    usecols = [c for c in ["loan_status"] + FEATURES if c in cols]

    df = pd.read_csv(raw_csv, usecols=usecols, low_memory=False)
    if sample_frac < 1.0:
        df = df.sample(frac=sample_frac, random_state=42)

    # Target mapping
    df = df[df["loan_status"].isin(GOOD | BAD)].copy()
    df["y_default"] = df["loan_status"].isin(BAD).astype(int)

    # Dates
    if "issue_d" in df.columns:
        df["issue_dt"] = _parse_issue_date(df["issue_d"])
    if "earliest_cr_line" in df.columns:
        df["earliest_cr_dt"] = _parse_earliest(df["earliest_cr_line"])
        # Credit history in months at origination
        df["credit_hist_mths"] = ((df["issue_dt"] - df["earliest_cr_dt"]).dt.days / 30.44).clip(lower=0)

    # Numeric cleanup
    if "term" in df.columns:
        df["term_mths"] = _clean_term(df["term"])
    if "revol_util" in df.columns:
        df["revol_util_pct"] = _clean_pct(df["revol_util"])
    if "fico_range_low" in df.columns and "fico_range_high" in df.columns:
        df["fico_mid"] = (df["fico_range_low"] + df["fico_range_high"]) / 2.0

    # Drop obvious leakage columns if they slipped into usecols
    for c in list(df.columns):
        cl = c.lower()
        if any(cl.startswith(p.lower()) for p in LEAKAGE_PREFIXES):
            df.drop(columns=[c], inplace=True)

    # Minimal final set: target, split field, engineered features, raw features
    keep = [c for c in df.columns if c not in ("loan_status",)]
    df = df[keep]

    out_parquet.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_parquet, index=False)
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-csv", default=str(Paths().data_raw / "loan.csv"),
                    help="Path to loan.csv (raw).")
    ap.add_argument("--out", default=str(Paths().data_processed / "pd_dataset.parquet"),
                    help="Output parquet path.")
    ap.add_argument("--sample-frac", type=float, default=0.20,
                    help="Fraction of rows to sample for faster iteration.")
    args = ap.parse_args()

    df = build_dataset(Path(args.raw_csv), Path(args.out), sample_frac=args.sample_frac)
    print(f"Saved dataset: {args.out}")
    print(df[["y_default"]].value_counts(normalize=True).head())

if __name__ == "__main__":
    main()
