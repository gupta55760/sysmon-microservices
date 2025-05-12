from fastapi import APIRouter, Request, HTTPException
from metrics_service.logging_config import setup_logger

# Setup logger
logger = setup_logger("metrics_service", "logs/metrics_service.log")

router = APIRouter()

@router.get("/metrics/status")
def get_status(request: Request):
    role = request.headers.get("x-user-role")
    logger.info(f"Status requested by role: {role}")
    if role not in ("admin", "user"):
        logger.warning("Access denied for status endpoint")
        raise HTTPException(status_code=403, detail="Access denied")
    return {"status": "Processed: status"}

@router.get("/metrics/metrics")
def get_metrics(request: Request):
    role = request.headers.get("x-user-role")
    logger.info(f"Metrics requested by role: {role}")
    if role not in ("admin", "user"):
        logger.warning("Access denied for metrics endpoint")
        raise HTTPException(status_code=403, detail="Access denied")

    logger.info(f"Returning metrics: {request.app.state.latest_metrics}")
    return request.app.state.latest_metrics

@router.get("/metrics/health")
def get_health():
    logger.info("Health check requested")
    return {"health": "ok"}

@router.get("/metrics/version")
def get_version():
    logger.info("Version check requested")
    return {"version": "1.0.0"}

