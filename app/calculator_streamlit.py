import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Loan PD + Risk Tier (Demo)", layout="centered")

st.title("Loan PD + Risk Tier (Credit Risk Demo)")
st.caption("Demo decisioning tool: estimate PD and assign risk tier using the trained model artifact.")

MODEL_PATH = st.sidebar.text_input("Model path", value="models/model.joblib")

def tier(pd_hat: float) -> str:
    if pd_hat < 0.02: return "Excellent"
    if pd_hat < 0.05: return "Good"
    if pd_hat < 0.10: return "Fair"
    if pd_hat < 0.20: return "Poor"
    return "Very High"

@st.cache_resource
def load_model(path: str):
    bundle = joblib.load(path)
    return bundle["pipeline"], bundle["num"], bundle["cat"]

try:
    pipe, num_cols, cat_cols = load_model(MODEL_PATH)
except Exception as e:
    st.error(f"Could not load model: {e}")
    st.stop()

st.subheader("Applicant inputs (subset)")
loan_amnt = st.number_input("Loan amount", min_value=500, max_value=40000, value=12000, step=500)
term_mths = st.selectbox("Term (months)", [36, 60], index=0)
annual_inc = st.number_input("Annual income", min_value=5000, max_value=500000, value=75000, step=1000)
dti = st.number_input("DTI", min_value=0.0, max_value=60.0, value=18.0, step=0.5)
fico_mid = st.number_input("FICO mid", min_value=300, max_value=850, value=700, step=5)
revol_util_pct = st.number_input("Revolving utilization (%)", min_value=0.0, max_value=200.0, value=35.0, step=1.0)

home_ownership = st.selectbox("Home ownership", ["RENT","MORTGAGE","OWN","OTHER"], index=1)
verification_status = st.selectbox("Verification status", ["Not Verified","Source Verified","Verified"], index=1)
purpose = st.selectbox("Purpose", ["debt_consolidation","credit_card","home_improvement","major_purchase","small_business","car","other"], index=0)

# Build a single-row dataframe with required columns; fill others with NA so the pipeline can impute.
row = {c: np.nan for c in (num_cols + cat_cols)}
row.update({
    "loan_amnt": loan_amnt,
    "term_mths": term_mths,
    "annual_inc": annual_inc,
    "dti": dti,
    "fico_mid": fico_mid,
    "revol_util_pct": revol_util_pct,
    "home_ownership": home_ownership,
    "verification_status": verification_status,
    "purpose": purpose
})

X = pd.DataFrame([row])
pd_hat = float(pipe.predict_proba(X)[:,1])
st.metric("Predicted PD", f"{pd_hat:.2%}")
st.metric("Risk Tier", tier(pd_hat))

st.write("**How to use**: Train a model (`python -m src.train`) then point this app at `models/model.joblib`.")
