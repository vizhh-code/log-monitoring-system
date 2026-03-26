import pandas as pd
import joblib

import os

BASE_DIR = os.getenv("BASE_DIR", "/home/ivsishnu/log_project")

DATASET_PATH = f"{BASE_DIR}/dataset/incidents_dataset.csv"
MODEL_PATH = f"{BASE_DIR}/model/incident_model.pkl"
RESULT_PATH = f"{BASE_DIR}/results/predictions.csv"
ALERT_PATH = f"{BASE_DIR}/results/alerts.log"


os.makedirs(f"{BASE_DIR}/dataset", exist_ok=True)
os.makedirs(f"{BASE_DIR}/results", exist_ok=True)
os.makedirs(f"{BASE_DIR}/model", exist_ok=True)

MODEL_PATH = "/home/ivsishnu/log_project/model/incident_model.pkl"
DATASET = "/home/ivsishnu/log_project/dataset/incidents_dataset.csv"

model = joblib.load(MODEL_PATH)

df = pd.read_csv(DATASET_PATH)

severity_map = {
    "LOW":0,
    "MEDIUM":1,
    "HIGH":2
}

df["severity_num"] = df["severity"].map(severity_map)

X = df[[
    "severity_num",
    "is_auth_failure",
    "is_sudo",
    "is_error"
]]

joblib.load("/home/ivsishnu/log_project/model/incident_model.pkl")

predictions = model.predict(X)

df["prediction"] = predictions

print("\nPredicted Incidents\n")
print(df.tail(50))

df.to_csv(RESULT_PATH, index=False)
