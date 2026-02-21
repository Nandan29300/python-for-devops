import os
import re
from collections import defaultdict
from datetime import datetime
from typing import Optional


# Regex pattern to parse a standard log line:
#   2025-01-10 09:00:01 INFO Application started successfully
LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>INFO|WARNING|ERROR|DEBUG|CRITICAL)"
    r"(?P<message>.*)"
)


def analyze_log_file(log_path: str, filter_level: Optional[str] = None) -> dict:
    """
    Analyze a log file and return a structured summary.

    Args:
        log_path (str): Absolute or relative path to the .log file.
        filter_level (str, optional): If given, only count lines with that log level.

    Returns:
        dict: Log summary with counts, recent errors, and health assessment.

    Raises:
        FileNotFoundError: If the log file does not exist.
        ValueError: If the log file is empty.
    """
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"Log file not found: {log_path}")

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if not lines:
        raise ValueError("Log file is empty.")

    counts: dict[str, int] = defaultdict(int)
    recent_errors: list[dict] = []
    recent_warnings: list[dict] = []
    unknown_lines = 0
    parsed_entries = []

    for line in lines:
        match = LOG_PATTERN.match(line)
        if match:
            level = match.group("level")
            timestamp = match.group("timestamp")
            message = match.group("message").strip()

            counts[level] += 1

            entry = {"timestamp": timestamp, "level": level, "message": message}
            parsed_entries.append(entry)

            if level == "ERROR":
                recent_errors.append(entry)
            elif level == "WARNING":
                recent_warnings.append(entry)
        else:
            unknown_lines += 1

    # Apply level filter if requested
    if filter_level:
        filter_level = filter_level.upper()
        filtered_count = counts.get(filter_level, 0)
        return {
            "log_file": os.path.basename(log_path),
            "filter_level": filter_level,
            "total_lines": len(lines),
            "matched_count": filtered_count,
        }

    # Health assessment
    error_count = counts.get("ERROR", 0)
    warning_count = counts.get("WARNING", 0)

    if error_count > 10:
        health = "Critical"
    elif error_count > 3:
        health = "Degraded"
    elif warning_count > 5:
        health = "Warning"
    else:
        health = "Healthy"

    # Keep only the 5 most recent errors/warnings
    recent_errors = recent_errors[-5:]
    recent_warnings = recent_warnings[-5:]

    return {
        "log_file": os.path.basename(log_path),
        "total_lines": len(lines),
        "unknown_lines": unknown_lines,
        "counts": {
            "INFO": counts.get("INFO", 0),
            "WARNING": counts.get("WARNING", 0),
            "ERROR": counts.get("ERROR", 0),
            "DEBUG": counts.get("DEBUG", 0),
            "CRITICAL": counts.get("CRITICAL", 0),
        },
        "health_status": health,
        "recent_errors": recent_errors,
        "recent_warnings": recent_warnings,
    }
