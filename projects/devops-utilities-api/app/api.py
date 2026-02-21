from fastapi import FastAPI  # Importing FastAPI Class
from routers import metrics, aws, logs

app = FastAPI(
    title="Internal DevOps Utilities API",
    description="This is an Internal API Utilities App for Monitoring Metrics, AWS Usage, Log Analysis, etc.",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.get("/", tags=["Health"])
def hello():
    """
    Health check endpoint — confirms the API is running.
    """
    return {"message": "Hello Dosto, This is DevOps Utilities API 🚀"}


# ── Routers ──────────────────────────────────────────────
app.include_router(metrics.router, prefix="/system", tags=["System Metrics"])
app.include_router(aws.router,     prefix="/aws",    tags=["AWS"])
app.include_router(logs.router,    prefix="/logs",   tags=["Log Analysis"])