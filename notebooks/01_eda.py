# %% [markdown]
# # EDA — Lending Club credit risk (Capital One BA style)
# This notebook focuses on decision-relevant insights:
# - default rate by segment
# - drift by vintage
# - drivers: FICO, DTI, utilization proxies
#
# Run:
#   python -m src.make_dataset --sample-frac 0.20
# Then open this as a Jupyter notebook (VS Code supports percent scripts).

# %%
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_parquet("../data/processed/pd_dataset.parquet")
df["issue_month"] = pd.to_datetime(df["issue_dt"]).dt.to_period("M").astype(str)

# %%
df["y_default"].mean()

# %%
# Default rate by purpose
purpose = (df.groupby("purpose")["y_default"].mean().sort_values(ascending=False).head(15))
purpose.plot(kind="bar")
plt.title("Default rate by purpose")
plt.ylabel("Bad rate")
plt.tight_layout()
plt.show()

# %%
# Vintage bad rate (by issue month)
vintage = df.groupby("issue_month")["y_default"].mean()
vintage.plot()
plt.title("Vintage bad rate (final outcomes only)")
plt.ylabel("Bad rate")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
