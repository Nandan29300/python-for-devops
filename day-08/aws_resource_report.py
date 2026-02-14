import boto3
import json

def list_ec2_instances():
    ec2 = boto3.client('ec2')
    instances = []
    try:
        response = ec2.describe_instances()
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instances.append({
                    "InstanceId": instance.get("InstanceId"),
                    "State": instance.get("State", {}).get("Name")
                })
    except Exception as e:
        print("Failed to fetch EC2 instances:", e)
    return instances

def list_s3_buckets():
    s3 = boto3.client('s3')
    buckets = []
    try:
        response = s3.list_buckets()
        for bucket in response.get('Buckets', []):
            buckets.append(bucket.get("Name"))
    except Exception as e:
        print("Failed to fetch S3 buckets:", e)
    return buckets

def main():
    print("Fetching AWS resources...")

    ec2_instances = list_ec2_instances()
    s3_buckets = list_s3_buckets()

    report = {
        "EC2_Instances": ec2_instances,
        "S3_Buckets": s3_buckets
    }

    print("EC2 Instances:")
    for inst in ec2_instances:
        print(f"  - {inst['InstanceId']} ({inst['State']})")

    print("\nS3 Buckets:")
    for name in s3_buckets:
        print(f"  - {name}")

    # Save JSON report
    try:
        with open("aws_report.json", "w") as f:
            json.dump(report, f, indent=2)
        print("\nReport written to aws_report.json")
    except Exception as e:
        print("Could not write aws_report.json:", e)

if __name__ == "__main__":
    main()