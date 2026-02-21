import boto3
from datetime import datetime, timezone, timedelta


# ── S3 ────────────────────────────────────────────────────────────────────────

def get_bucket_info() -> dict:
    """
    List all S3 buckets and classify them as new (< 90 days) or old (>= 90 days).

    Returns:
        dict: Summary with total, new, and old bucket counts and their names.
    """
    s3_client = boto3.client("s3")
    buckets = s3_client.list_buckets()["Buckets"]
    current_date = datetime.now(timezone.utc)
    threshold_date = current_date - timedelta(days=90)

    new_buckets, old_buckets = [], []

    for bucket in buckets:
        bucket_name = bucket["Name"]
        creation_date = bucket["CreationDate"]
        # Ensure timezone-aware comparison
        if creation_date.tzinfo is None:
            creation_date = creation_date.replace(tzinfo=timezone.utc)

        if creation_date >= threshold_date:
            new_buckets.append(bucket_name)
        else:
            old_buckets.append(bucket_name)

    return {
        "total_buckets": len(buckets),
        "new_buckets_count": len(new_buckets),
        "old_buckets_count": len(old_buckets),
        "new_bucket_names": new_buckets,
        "old_bucket_names": old_buckets,
    }


# ── EC2 ───────────────────────────────────────────────────────────────────────

def get_ec2_info() -> dict:
    """
    List all EC2 instances across all regions (or just the default region) and
    return a summary grouped by their current state.

    Returns:
        dict: Total instance count, per-state counts, and per-instance details.
    """
    ec2_client = boto3.client("ec2")

    response = ec2_client.describe_instances()

    instances = []
    state_counts: dict[str, int] = {}

    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            instance_id = instance.get("InstanceId", "N/A")
            instance_type = instance.get("InstanceType", "N/A")
            state = instance.get("State", {}).get("Name", "unknown")
            launch_time = instance.get("LaunchTime")
            public_ip = instance.get("PublicIpAddress", "N/A")
            private_ip = instance.get("PrivateIpAddress", "N/A")
            az = instance.get("Placement", {}).get("AvailabilityZone", "N/A")

            # Extract Name tag if present
            name = "N/A"
            for tag in instance.get("Tags", []):
                if tag.get("Key") == "Name":
                    name = tag.get("Value", "N/A")
                    break

            # Calculate running duration
            running_since = "N/A"
            if launch_time:
                if launch_time.tzinfo is None:
                    launch_time = launch_time.replace(tzinfo=timezone.utc)
                delta = datetime.now(timezone.utc) - launch_time
                running_since = str(timedelta(seconds=int(delta.total_seconds())))

            state_counts[state] = state_counts.get(state, 0) + 1

            instances.append({
                "instance_id": instance_id,
                "name": name,
                "instance_type": instance_type,
                "state": state,
                "availability_zone": az,
                "public_ip": public_ip,
                "private_ip": private_ip,
                "running_since": running_since,
            })

    return {
        "total_instances": len(instances),
        "state_summary": state_counts,
        "instances": instances,
    }