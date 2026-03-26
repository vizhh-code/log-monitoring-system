import time
import re
import os
import platform
from collections import defaultdict

# ------------------ CONFIG ------------------

BASE_DIR = os.getenv("BASE_DIR", "/home/ivsishnu/log_project")

ALERT_PATH = f"{BASE_DIR}/results/alerts.log"

# Dynamic log file selection
LOG_FILE = os.getenv("LOG_PATH")

if not LOG_FILE:
    if platform.system() == "Linux":
        LOG_FILE = "/var/log/auth.log"
    else:
        LOG_FILE = "test_logs.txt"

# Ensure results folder exists
os.makedirs(f"{BASE_DIR}/results", exist_ok=True)

# ------------------ GLOBALS ------------------

ip_fail_count = defaultdict(int)
threshold = 3

last_alert = None  # to avoid duplicate alerts


# ------------------ ALERT FUNCTION ------------------

def send_alert(severity, root_cause, line):
    global last_alert

    if line == last_alert:
        return

    last_alert = line

    with open(ALERT_PATH, "a") as f:
        f.write(f"ALERT | {severity} | {root_cause} | {line.strip()}\n")

    print("\n🚨 ALERT TRIGGERED 🚨")
    print(f"{severity} | {root_cause} | {line.strip()}\n")


# ------------------ PROCESS LOG ------------------

def process_log(line):
    line_lower = line.lower()

    label = "NORMAL"
    severity = "LOW"
    root_cause = "Normal Operation"

    # --- AUTH FAILURE ---
    if "authentication failure" in line_lower:
        label = "INCIDENT"

        if "sudo" in line_lower:
            root_cause = "Sudo Authentication Failure"
        else:
            root_cause = "Brute Force Login Attempt"

        ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)

        if ip_match:
            ip = ip_match.group()
            ip_fail_count[ip] += 1

            if ip_fail_count[ip] > threshold:
                severity = "HIGH"
            else:
                severity = "MEDIUM"
        else:
            severity = "MEDIUM"

    # --- MULTIPLE PASSWORD FAIL ---
    elif "incorrect password attempts" in line_lower:
        label = "INCIDENT"
        severity = "HIGH"
        root_cause = "Multiple Failed Sudo Attempts"

    # --- SSH BRUTE FORCE ---
    elif "failed password" in line_lower:
        label = "INCIDENT"
        severity = "HIGH"
        root_cause = "SSH Brute Force Attempt"

    # --- SYSTEM ERROR ---
    elif "error" in line_lower:
        label = "INCIDENT"
        severity = "MEDIUM"
        root_cause = "System Error"

    output = f"{label} | {severity} | {root_cause} | {line.strip()}"
    print(output)

    # Trigger alert
    if label == "INCIDENT" and severity == "HIGH":
        send_alert(severity, root_cause, line)


# ------------------ MONITOR ------------------

def monitor():
    print(f"\n📡 Monitoring log file: {LOG_FILE}\n")

    try:
        with open(LOG_FILE, "r") as f:
            f.seek(0, 2)

            while True:
                line = f.readline()

                if not line:
                    time.sleep(0.5)
                    continue

                process_log(line)

    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user.")

    except FileNotFoundError:
        print(f"❌ Log file not found: {LOG_FILE}")

    except PermissionError:
        print("❌ Permission denied. Try running with sudo.")


# ------------------ RUN ------------------

if __name__ == "__main__":
    monitor()
