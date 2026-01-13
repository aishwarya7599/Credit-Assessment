# %% [markdown]
# # Modeling — PD estimation with time split
# Trains a baseline model and prints ROC-AUC / PR-AUC / Brier score.
# Prefer running the CLI:
#   python -m src.train --model logistic
#   python -m src.train --model hgb

# %%
import joblib, pandas as pd
from pathlib import Path
from src.train import train_model
from src.config import Paths

metrics = train_model(Path(Paths().data_processed/"pd_dataset.parquet"), "logistic", Path(Paths().models/"model.joblib"))
metrics
