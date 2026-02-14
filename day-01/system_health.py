# Day 01 – Introduction to Python for DevOps

## Task Completion Report

### Task Overview

- **Write your first Python script**
- Script requirements:
  - Take threshold values (CPU, disk, memory) from user input
  - Fetch system metrics using a Python library (`psutil`)
  - Compare metrics against thresholds
  - Print the result to the terminal



### Steps Taken

1. **Created `system_health.py` script**
2. Used `input()` to get CPU, disk, and memory thresholds from the user
3. Used `psutil` to fetch current system metrics
4. Compared metrics against user-provided thresholds with `if`/`else`
5. Printed results to terminal for each metric
6. Wrapped metric checks in functions for code clarity



### Python Script Example


import psutil

def get_thresholds():
    thresholds = {}
    thresholds['cpu'] = float(input("Enter CPU usage threshold (%): "))
    thresholds['disk'] = float(input("Enter Disk usage threshold (%): "))
    thresholds['memory'] = float(input("Enter Memory usage threshold (%): "))
    return thresholds

def get_metrics():
    metrics = {}
    metrics['cpu'] = psutil.cpu_percent(interval=1)
    metrics['disk'] = psutil.disk_usage('/').percent
    metrics['memory'] = psutil.virtual_memory().percent
    return metrics

def check_health(metrics, thresholds):
    for key in metrics:
        if metrics[key] > thresholds[key]:
            print(f"{key.upper()} ALERT: {metrics[key]}% exceeds threshold of {thresholds[key]}%")
        else:
            print(f"{key.upper()} OK: {metrics[key]}% is within threshold {thresholds[key]}%")

def main():
    print("=== System Health Check ===")
    thresholds = get_thresholds()
    metrics = get_metrics()
    check_health(metrics, thresholds)

if __name__ == "__main__":
    main()


