🚨 Automated Log Monitoring & Incident Prediction System

📌 Overview

This project is an end-to-end **DevOps-based log monitoring system** that analyzes system logs to detect incidents, classify their severity, trigger alerts, and visualize insights through a dashboard.

It combines **rule-based detection**, **machine learning**, and **real-time monitoring** to improve system reliability and reduce manual log analysis.


🎯 Key Features

* 🔍 Real-time log monitoring (Linux logs)
* ⚠️ Incident detection using rule-based engine
* 🤖 Machine Learning-based incident prediction
* 🚨 Alert system for high-severity issues
* 📊 Interactive dashboard using Streamlit
* 🔄 Automated pipeline using Airflow
* 🐳 Dockerized for easy deployment

---

🧠 System Workflow

```
System Logs
   ↓
Detection Engine (Rules)
   ↓
Dataset Creation
   ↓
ML Model (Training & Prediction)
   ↓
Real-Time Monitoring → Alerts
   ↓
Dashboard Visualization
```

---

Tech Stack

* **Programming:** Python
* **Data Processing:** Pandas
* **Machine Learning:** scikit-learn
* **Visualization:** Streamlit
* **Automation:** Apache Airflow
* **Deployment:** Docker
* **OS Logs:** Linux (auth.log), HDFS logs


🚀 How to Run (Local Setup)

Step 1: Run pipeline


python src/detect_incident.py
python src/train_model.py
python src/predict_incidents.py

Step 2: Launch dashboard

streamlit run dashboard.py


👉 Open in browser:
http://localhost:8501


🐳 Docker Deployment

Build image

docker build -t log-monitor .


Run container

docker run -p 8502:8501 log-monitor


👉 Open in browser:
http://localhost:8502


🔍 Types of Incidents Detected

* Multiple failed sudo attempts
* Authentication failures
* SSH brute-force attempts
* System errors


🚨 Severity Levels

* **LOW** → Normal system activity
* **MEDIUM** → Suspicious activity
* **HIGH** → Critical incidents (alerts triggered)



Current Limitations

* Batch processing (may cause duplicate entries)
* Imbalanced dataset (more NORMAL than INCIDENT)
* Limited log source support (mainly Linux logs)

---

🔮 Future Improvements

* Real-time streaming (Kafka / Log pipelines)
* Multi-server log ingestion
* Advanced ML models & feature engineering
* Integration with alerting tools (Email, Slack)

---

💡 Project Significance

This project demonstrates key **DevOps principles**:

* Monitoring & observability
* Incident detection & alerting
* Automation of workflows
* Containerized deployment


📷 Screenshots (Optional)

*Add your dashboard screenshots here*


🧑‍💻 Author

**Vishnu Ram**



⭐ Final Note

This project is a lightweight implementation of a **log monitoring and incident management system**, inspired by real-world tools like ELK Stack and Splunk.


