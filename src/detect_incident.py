import re
from collections import defaultdict, Counter
import os

BASE_DIR = os.getenv("BASE_DIR", "/home/ivsishnu/log_project")

DATASET_PATH = f"{BASE_DIR}/dataset/incidents_dataset.csv"
MODEL_PATH = f"{BASE_DIR}/model/incident_model.pkl"
RESULT_PATH = f"{BASE_DIR}/results/predictions.csv"
ALERT_PATH = f"{BASE_DIR}/results/alerts.log"


os.makedirs(f"{BASE_DIR}/dataset", exist_ok=True)
os.makedirs(f"{BASE_DIR}/results", exist_ok=True)
os.makedirs(f"{BASE_DIR}/model", exist_ok=True)

BASE_DIR = "/home/ivsishnu/log_project"
linux_file = "/var/log/auth.log"
hdfs_file = BASE_DIR + "/processed/hdfs_clean.txt"

dataset_file = DATASET_PATH

linux_output = BASE_DIR + "/results/linux_results.txt"
hdfs_output = BASE_DIR + "/results/hdfs_results.txt"
# Root cause mapping
ROOT_CAUSES = {
    "authentication failure": "Brute Force Login Attempt",
    "failed password": "SSH Login Failure",
    "session opened": "User Login",
    "session closed": "User Logout",
    "sudo": "Privilege Escalation",
    "cron": "Scheduled Task",
    "error": "System Error",
    "failed": "Operation Failure",
    "corrupt": "Data Corruption",
    "disconnect": "Network Issue"
}


def analyze_linux():

    attacker_counter = Counter()
    ip_fail_count = defaultdict(int)
    severity_counter = Counter()
    threshold = 5

    import csv

    with open(linux_file, "r", errors="ignore") as f:
        lines = f.readlines()

    # PASS 1 → count failed logins per IP
    for line in lines:

        if "authentication failure" in line.lower():

            ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)

            if ip_match:
                ip = ip_match.group()
                ip_fail_count[ip] += 1

    with open(dataset_file, "w", newline="") as d:
        writer = csv.writer(d)
        writer.writerow([
        "label",
        "severity",
        "root_cause",
        "is_auth_failure",
        "is_sudo",
        "is_error"
    ])
        for line in lines:

            line_lower = line.lower()

            label = "NORMAL"
            severity = "LOW"
            root_cause = "Normal Operation"

            if "authentication failure" in line_lower:

                label = "INCIDENT"
                root_cause = ROOT_CAUSES["authentication failure"]

                ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)

                if ip_match:
                    ip = ip_match.group()

                    if ip_fail_count[ip] > threshold:
                        severity = "HIGH"
                    else:
                        severity = "MEDIUM"

            elif "error" in line_lower or "alert" in line_lower:

                label = "INCIDENT"
                severity = "MEDIUM"
                root_cause = ROOT_CAUSES["error"]

            elif "session opened" in line_lower:

                root_cause = ROOT_CAUSES["session opened"]


            elif "failed password" in line_lower:
                label = "INCIDENT"
                severity = "HIGH"
                root_cause = "SSH Brute Force Attempt"
            severity_counter[severity] += 1

            is_auth_failure = 1 if "authentication failure" in line_lower else 0
            is_sudo = 1 if "sudo" in line_lower else 0
            is_error = 1 if "error" in line_lower else 0
            writer.writerow([
                label,
                severity,
                root_cause,
                is_auth_failure,
                is_sudo,
                is_error
            ])
def analyze_hdfs():

    severity_counter = Counter()

    with open(hdfs_file, "r", errors="ignore") as f:
        lines = f.readlines()

    with open(hdfs_output, "w") as out:

        for line in lines:

            line_lower = line.lower()

            label = "NORMAL"
            severity = "LOW"
            root_cause = "Normal Operation"

            if "exception" in line_lower or "failed" in line_lower:

                label = "INCIDENT"
                severity = "HIGH"
                root_cause = ROOT_CAUSES["failed"]

            elif "corrupt" in line_lower:

                label = "INCIDENT"
                severity = "HIGH"
                root_cause = ROOT_CAUSES["corrupt"]

            elif "disconnect" in line_lower:

                label = "INCIDENT"
                severity = "MEDIUM"
                root_cause = ROOT_CAUSES["disconnect"]

            severity_counter[severity] += 1

            out.write(f"{label} | {severity} | {root_cause} | {line}")

    print("\nHDFS Analysis Complete")

    print("\nHDFS Incident Summary:")
    print(f"HIGH   : {severity_counter['HIGH']}")
    print(f"MEDIUM : {severity_counter['MEDIUM']}")
    print(f"LOW    : {severity_counter['LOW']}")


analyze_linux()
analyze_hdfs()




