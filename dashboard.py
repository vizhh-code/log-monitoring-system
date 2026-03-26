import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=60000)


import os

BASE_DIR = os.getenv("BASE_DIR", "/home/ivsishnu/log_project")
RESULT_PATH = f"{BASE_DIR}/results/predictions.csv"


st.title("🚨 Incident Monitoring Dashboard")

df=pd.read_csv(RESULT_PATH)

st.subheader("Dataset Preview")
st.dataframe(df.tail(20))

st.subheader("Incident Statistics")


high = len(df[df["severity"] == "HIGH"])
medium = len(df[df["severity"] == "MEDIUM"])
low = len(df[df["severity"] == "LOW"])

col1, col2, col3 = st.columns(3)

col1.metric("High Severity", high)
col2.metric("Medium Severity", medium)
col3.metric("Low Severity", low)

st.subheader("Severity Distribution")

severity_counts = df["severity"].value_counts()

st.bar_chart(severity_counts)

st.subheader("Root Cause Analysis")

root_counts = df["root_cause"].value_counts()

st.bar_chart(root_counts)

st.subheader("ML Prediction Comparison")

if "prediction" in df.columns:
    prediction_counts = df["prediction"].value_counts()
    st.bar_chart(prediction_counts)
else:
    st.warning("Prediction results not available yet. Run the ML prediction pipeline.")


st.subheader("Incident Records")

incidents = df[df["label"] == "INCIDENT"]
st.dataframe(incidents.tail(20))


st.subheader("🚨 Recent Alerts (HIGH Severity)")

alerts = df[df["severity"] == "HIGH"]

if not alerts.empty:
    st.dataframe(alerts.tail(10))
else:
    st.info("No high severity alerts")
