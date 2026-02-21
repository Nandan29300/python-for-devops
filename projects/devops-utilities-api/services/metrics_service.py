import psutil
from datetime import datetime, timedelta


def get_system_metrics(cpu_threshold: int = 80) -> dict:
    """
    Collect live system metrics.

    Args:
        cpu_threshold (int): CPU % value above which status is 'High CPU'. Default 80.

    Returns:
        dict: CPU, Memory, Disk, Network I/O, Uptime, and System Health status.
    """
    # ── CPU ──────────────────────────────────────────────
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count_logical = psutil.cpu_count(logical=True)
    cpu_count_physical = psutil.cpu_count(logical=False)

    # ── Memory ───────────────────────────────────────────
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()

    # ── Disk ─────────────────────────────────────────────
    disk = psutil.disk_usage("/")

    # ── Network I/O ──────────────────────────────────────
    net = psutil.net_io_counters()

    # ── Uptime ───────────────────────────────────────────
    boot_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_timestamp)
    uptime_seconds = (datetime.now() - boot_time).total_seconds()
    uptime_str = str(timedelta(seconds=int(uptime_seconds)))

    # ── Health Status ─────────────────────────────────────
    issues = []
    if cpu_percent > cpu_threshold:
        issues.append(f"High CPU ({cpu_percent}%)")
    if vm.percent > 90:
        issues.append(f"High Memory ({vm.percent}%)")
    if disk.percent > 90:
        issues.append(f"High Disk ({disk.percent}%)")

    status = "Healthy" if not issues else " | ".join(issues)

    return {
        "cpu": {
            "usage_percent": cpu_percent,
            "logical_cores": cpu_count_logical,
            "physical_cores": cpu_count_physical,
            "threshold_percent": cpu_threshold,
        },
        "memory": {
            "usage_percent": vm.percent,
            "total_gb": round(vm.total / (1024 ** 3), 2),
            "used_gb": round(vm.used / (1024 ** 3), 2),
            "available_gb": round(vm.available / (1024 ** 3), 2),
            "swap_usage_percent": swap.percent,
        },
        "disk": {
            "usage_percent": disk.percent,
            "total_gb": round(disk.total / (1024 ** 3), 2),
            "used_gb": round(disk.used / (1024 ** 3), 2),
            "free_gb": round(disk.free / (1024 ** 3), 2),
        },
        "network": {
            "bytes_sent_mb": round(net.bytes_sent / (1024 ** 2), 2),
            "bytes_recv_mb": round(net.bytes_recv / (1024 ** 2), 2),
            "packets_sent": net.packets_sent,
            "packets_recv": net.packets_recv,
        },
        "uptime": uptime_str,
        "system_status": status,
    }
