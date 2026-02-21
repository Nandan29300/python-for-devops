import os
from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from services.log_service import analyze_log_file

router = APIRouter()

# Default sample log location (relative to project root when running main.py)
DEFAULT_LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "app.log")


@router.get("/analyze", status_code=200)
def analyze_log(
    log_path: str = Query(
        default=None,
        description="Absolute path to the log file on the server. "
                    "Defaults to the bundled app.log sample."
    ),
    filter_level: str = Query(
        default=None,
        description="Optional log level filter: INFO | WARNING | ERROR | DEBUG | CRITICAL"
    ),
):
    """
    Analyze a log file on the server and return a structured summary.

    - **log_path**: Path to the log file (server-side). Leave blank to use the bundled sample.
    - **filter_level**: Return only the count for a specific log level.

    Returns counts per log level, overall health status, and the 5 most recent
    errors and warnings.
    """
    path = log_path or os.path.abspath(DEFAULT_LOG_PATH)

    try:
        result = analyze_log_file(path, filter_level=filter_level)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post("/analyze/upload", status_code=200)
async def analyze_uploaded_log(
    file: UploadFile = File(..., description="Upload a .log file for analysis"),
    filter_level: str = Query(
        default=None,
        description="Optional log level filter: INFO | WARNING | ERROR | DEBUG | CRITICAL"
    ),
):
    """
    Upload a `.log` file and receive an instant analysis.

    - **file**: The log file to upload (`.log` or `.txt`).
    - **filter_level**: Optional — return only the count for a specific level.
    """
    # Save to a temp file
    import tempfile
    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".log", mode="wb") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        result = analyze_log_file(tmp_path, filter_level=filter_level)
        # Override log_file name with the original filename
        result["log_file"] = file.filename
        return result
    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Clean up temp file
        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)
