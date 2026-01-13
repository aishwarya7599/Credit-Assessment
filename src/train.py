import argparse
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss

from .config import Paths, DEFAULT_TRAIN_END, RANDOM_STATE

NUMERIC = [
    "loan_amnt","annual_inc","dti","fico_mid","delinq_2yrs","inq_last_6mths","open_acc",
    "pub_rec","revol_bal","revol_util_pct","total_acc","acc_open_past_24mths","avg_cur_bal",
    "bc_util","all_util","mort_acc","num_rev_accts","pct_tl_nvr_dlq","tot_cur_bal",
    "total_rev_hi_lim","total_bc_limit","credit_hist_mths","term_mths"
]
CATEGORICAL = [
    "emp_length","home_ownership","verification_status","purpose","addr_state",
    "application_type","disbursement_method","initial_list_status"
]

def _time_split(df: pd.DataFrame, train_end: str):
    cut = pd.to_datetime(train_end)
    train = df[df["issue_dt"] < cut].copy()
    test  = df[df["issue_dt"] >= cut].copy()
    return train, test

def _build_preprocess(df: pd.DataFrame):
    num = [c for c in NUMERIC if c in df.columns]
    cat = [c for c in CATEGORICAL if c in df.columns]

    numeric_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler(with_mean=False)),
    ])
    cat_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    pre = ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, num),
            ("cat", cat_pipe, cat),
        ],
        remainder="drop",
        sparse_threshold=0.0
    )
    return pre, num, cat

def train_model(df_path: Path, model_kind: str, out_path: Path, train_end: str = DEFAULT_TRAIN_END):
    df = pd.read_parquet(df_path)
    # Ensure issue_dt exists
    if "issue_dt" not in df.columns:
        df["issue_dt"] = pd.to_datetime(df["issue_d"], format="%b-%Y", errors="coerce")

    train, test = _time_split(df, train_end)
    y_train = train["y_default"].astype(int).values
    y_test  = test["y_default"].astype(int).values

    pre, num, cat = _build_preprocess(df)

    if model_kind == "logistic":
        clf = LogisticRegression(max_iter=200, n_jobs=None, class_weight="balanced")
    elif model_kind == "hgb":
        clf = HistGradientBoostingClassifier(max_depth=6, learning_rate=0.06, max_iter=250, random_state=RANDOM_STATE)
    else:
        raise ValueError("model must be 'logistic' or 'hgb'")

    pipe = Pipeline(steps=[("pre", pre), ("model", clf)])
    X_train = train[num + cat]
    X_test = test[num + cat]

    pipe.fit(X_train, y_train)
    p_test = pipe.predict_proba(X_test)[:,1] if hasattr(pipe, "predict_proba") else pipe.predict(X_test)

    metrics = {
        "model": model_kind,
        "train_end": train_end,
        "n_train": int(len(train)),
        "n_test": int(len(test)),
        "default_rate_test": float(y_test.mean()),
        "roc_auc": float(roc_auc_score(y_test, p_test)),
        "pr_auc": float(average_precision_score(y_test, p_test)),
        "brier": float(brier_score_loss(y_test, p_test)),
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": pipe, "metrics": metrics, "num": num, "cat": cat}, out_path)
    return metrics

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default=str(Paths().data_processed / "pd_dataset.parquet"))
    ap.add_argument("--model", choices=["logistic","hgb"], default="logistic")
    ap.add_argument("--train-end", default=DEFAULT_TRAIN_END)
    ap.add_argument("--out", default=str(Paths().models / "model.joblib"))
    args = ap.parse_args()

    metrics = train_model(Path(args.dataset), args.model, Path(args.out), train_end=args.train_end)
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    import json
    main()
