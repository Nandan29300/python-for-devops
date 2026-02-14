# Day 01 – Introduction to Python for DevOps


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


