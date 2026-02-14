from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# --- Log Analyzer (reuse your own class design as needed) ---
import os

class LogAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.counts = {"INFO": 0, "WARNING": 0, "ERROR": 0, "UNKNOWN": 0}

    def read_logs(self):
        try:
            with open(self.log_file, "r") as f:
                return f.readlines()
        except Exception:
            return []

    def analyze(self, lines):
        self.counts = {k:0 for k in self.counts}
        for line in lines:
            if "INFO" in line:
                self.counts["INFO"] += 1
            elif "WARNING" in line:
                self.counts["WARNING"] += 1
            elif "ERROR" in line:
                self.counts["ERROR"] += 1
            else:
                self.counts["UNKNOWN"] += 1
        return self.counts

LOG_FILE_PATH = os.environ.get("LOG_FILE_PATH", "app.log")

@app.get("/health")
def health():
    return {"status": "ok", "service": "FastAPI DevOps Demo"}

@app.get("/logs")
def logs():
    analyzer = LogAnalyzer(LOG_FILE_PATH)
    lines = analyzer.read_logs()
    if not lines:
        return {"error": f"Log file '{LOG_FILE_PATH}' not found or empty."}
    summary = analyzer.analyze(lines)
    return summary

# --- Optional: include AWS endpoint if you wish and boto3 is set up ---
try:
    import boto3

    def list_ec2_instances():
        ec2 = boto3.client("ec2")
        instances_info = []
        try:
            response = ec2.describe_instances()
            for reservation in response.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    instances_info.append({
                        "InstanceId": instance.get("InstanceId"),
                        "State": instance.get("State", {}).get("Name")
                    })
        except Exception as e:
            instances_info.append({"error": str(e)})
        return instances_info

    def list_s3_buckets():
        s3 = boto3.client("s3")
        buckets = []
        try:
            response = s3.list_buckets()
            for bucket in response.get("Buckets", []):
                buckets.append(bucket.get("Name"))
        except Exception as e:
            buckets.append(f"Error: {str(e)}")
        return buckets

    @app.get("/aws")
    def aws():
        return {
            "EC2_Instances": list_ec2_instances(),
            "S3_Buckets": list_s3_buckets()
        }
except ImportError:
    pass
