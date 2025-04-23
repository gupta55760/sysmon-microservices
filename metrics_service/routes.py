from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.get("/metrics/status")
def get_status(request: Request):
    role = request.headers.get("x-user-role")
    if role not in ("admin", "user"):
        raise HTTPException(status_code=403, detail="Access denied")
    return {"status": "Processed: status"}

@router.get("/metrics/metrics")
def get_metrics(request: Request):
    role = request.headers.get("x-user-role")
    if role not in ("admin", "user"):
        raise HTTPException(status_code=403, detail="Access denied")

    print("🚀 /api/metrics returning:", request.app.state.latest_metrics)
    return request.app.state.latest_metrics

@router.get("/metrics/health")
def get_health():
    return {"health": "ok"}

@router.get("/metrics/version")
def get_version():
    return {"version": "1.0.0"}
