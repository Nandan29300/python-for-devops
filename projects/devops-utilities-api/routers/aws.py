from fastapi import APIRouter, HTTPException
from services.aws_service import get_bucket_info, get_ec2_info

router = APIRouter()


@router.get("/s3", status_code=200)
def get_buckets():
    """
    Returns a summary of all S3 buckets in the AWS account.

    Classifies buckets as:
    - **New**: Created within the last 90 days
    - **Old**: Created more than 90 days ago
    """
    try:
        buckets_info = get_bucket_info()
        return buckets_info
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch S3 bucket info: {str(e)}"
        )


@router.get("/ec2", status_code=200)
def get_instances():
    """
    Returns a summary of all EC2 instances in the default AWS region.

    Provides:
    - Total instance count
    - Per-state counts (running, stopped, terminated, etc.)
    - Per-instance details: ID, Name tag, type, state, IPs, AZ, running duration
    """
    try:
        ec2_info = get_ec2_info()
        return ec2_info
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch EC2 instance info: {str(e)}"
        )
