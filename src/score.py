import argparse
from pathlib import Path
import joblib
import pandas as pd
import numpy as np

from .config import Paths

def risk_tier(pd_hat: pd.Series) -> pd.Series:
    bins = [-np.inf, 0.02, 0.05, 0.10, 0.20, np.inf]
    labels = ["Excellent","Good","Fair","Poor","Very High"]
    return pd.cut(pd_hat, bins=bins, labels=labels)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default=str(Paths().data_processed / "pd_dataset.parquet"))
    ap.add_argument("--model-path", default=str(Paths().models / "model.joblib"))
    ap.add_argument("--out", default=str(Paths().reports / "scored_sample.parquet"))
    ap.add_argument("--sample-n", type=int, default=200000)
    args = ap.parse_args()

    bundle = joblib.load(args.model_path)
    pipe = bundle["pipeline"]
    num = bundle["num"]; cat = bundle["cat"]

    df = pd.read_parquet(args.dataset)
    if len(df) > args.sample_n:
        df = df.sample(n=args.sample_n, random_state=42)

    X = df[num + cat]
    pd_hat = pipe.predict_proba(X)[:,1] if hasattr(pipe, "predict_proba") else pipe.predict(X)
    df = df.copy()
    df["pd_hat"] = pd_hat
    df["risk_tier"] = risk_tier(df["pd_hat"]).astype(str)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)
    print(f"Saved scored sample: {out_path}")
    print(df["risk_tier"].value_counts(normalize=True).head())

if __name__ == "__main__":
    main()
