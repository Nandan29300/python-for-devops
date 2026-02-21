from fastapi import APIRouter, HTTPException, Query
from services.metrics_service import get_system_metrics

router = APIRouter()


@router.get("/metrics", status_code=200)
def get_metrics(cpu_threshold: int = Query(default=80, ge=1, le=100, description="CPU % alert threshold (1-100)")):
    """
    Returns live system metrics: CPU, Memory, Disk, Network I/O, and overall health status.

    - **cpu_threshold**: Percentage above which system status becomes 'High CPU' (default: 80)
    """
    try:
        metrics = get_system_metrics(cpu_threshold=cpu_threshold)
        return metrics
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )
