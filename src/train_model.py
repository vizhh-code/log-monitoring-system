import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib

import os

BASE_DIR = os.getenv("BASE_DIR", "/home/ivsishnu/log_project")

DATASET_PATH = f"{BASE_DIR}/dataset/incidents_dataset.csv"
MODEL_PATH = f"{BASE_DIR}/model/incident_model.pkl"
RESULT_PATH = f"{BASE_DIR}/results/predictions.csv"
ALERT_PATH = f"{BASE_DIR}/results/alerts.log"

DATASET = "/home/ivsishnu/log_project/dataset/incidents_dataset.csv"
MODEL_PATH = "/home/ivsishnu/log_project/model/incident_model.pkl"

df = pd.read_csv(DATASET_PATH)



# convert text → numbers
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
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,y,test_size=0.2,random_state=42
)

model = DecisionTreeClassifier(class_weight="balanced")
model.fit(X_train,y_train)

joblib.dump(model,MODEL_PATH)

print("Model training complete")
from sklearn.metrics import classification_report

y_pred = model.predict(X_test)

print("\nModel Evaluation:\n")
print(classification_report(y_test, y_pred))
