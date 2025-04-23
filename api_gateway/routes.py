from fastapi import APIRouter, Request, Body, Query
from typing import Optional
from api_gateway.proxy import forward_request
from api_gateway.schemas import (
    LoginInput,
    RefreshTokenInput,
    UserCreate,
    UserUpdate,
    FeedbackCreate
)

router = APIRouter()

# ----------- Auth Routes -----------
@router.post("/api/users/login", summary="Authenticate user and return access token", tags=["Auth"])
async def proxy_login(request: Request, credentials: LoginInput = Body(...)):
    return await forward_request(request, "http://user_service:8000/users/login")

@router.post("/api/users/refresh", summary="Refresh access token using refresh token", tags=["Auth"])
async def proxy_refresh(request: Request, payload: RefreshTokenInput = Body(...)):
    return await forward_request(request, "http://user_service:8000/users/refresh")

@router.post("/api/users/logout", summary="Log out user and invalidate session", tags=["Auth"])
async def proxy_logout(request: Request):
    return await forward_request(request, "http://user_service:8000/users/logout")

# ----------- User Routes -----------
@router.get("/api/users", summary="List all users", tags=["Users"])
async def proxy_users(
    request: Request,
    skip: int = Query(0),
    limit: int = Query(10),
    sort_by: str = Query("id", enum=["id", "username"]),
    sort_order: str = Query("asc", enum=["asc", "desc"]),
    search: Optional[str] = Query(None),
):
    return await forward_request(request, "http://user_service:8000/users")

@router.post("/api/users", summary="Create a new user", tags=["Users"])
async def proxy_user_create(request: Request, user: UserCreate = Body(...)):
    return await forward_request(request, "http://user_service:8000/users/create_user")

@router.put("/api/users/{username}", summary="Update an existing user", tags=["Users"])
async def proxy_user_update(username: str, request: Request, user: UserUpdate = Body(...)):
    return await forward_request(request, f"http://user_service:8000/users/{username}")

@router.delete("/api/users/{username}", summary="Delete an existing user", tags=["Users"])
async def proxy_user_delete(username: str, request: Request):
    return await forward_request(request, f"http://user_service:8000/users/{username}")

@router.get("/api/users/health", summary="Check user service health", tags=["Users"])
async def proxy_user_health(request: Request):
    return await forward_request(request, "http://user_service:8000/health")


# ----------- Metrics Service Routes -----------

@router.get("/api/metrics/status", summary="Get system status", tags=["Metrics"])
async def proxy_status(request: Request):
    return await forward_request(request, "http://metrics_service:8001/metrics/status")

@router.get("/api/metrics/metrics", summary="Get latest metrics", tags=["Metrics"])
async def proxy_metrics(request: Request):
    return await forward_request(request, "http://metrics_service:8001/metrics/metrics")

@router.get("/api/metrics/health", summary="Check metrics service health", tags=["Metrics"])
async def proxy_health(request: Request):
    return await forward_request(request, "http://metrics_service:8001/metrics/health")

@router.get("/api/metrics/version", summary="Get metrics service version", tags=["Metrics"])
async def proxy_version(request: Request):
    return await forward_request(request, "http://metrics_service:8001/metrics/version")


# ----------- Ingest Service Routes -----------

@router.post("/api/feedback", summary="Provide user feedback", tags=["Feedback"])
async def proxy_feedback(request: Request, feedback: FeedbackCreate = Body(...)):
    return await forward_request(request, "http://feedback_service:8002/feedback")

@router.get("/api/feedback", summary="List feedback records", tags=["Feedback"])
async def proxy_get_feedback(request: Request):
    return await forward_request(request, "http://feedback_service:8002/feedback")

@router.get("/api/feedback/health", summary="Check feedback service health", tags=["Feedback"])
async def proxy_feedback_health(request: Request):
    return await forward_request(request, "http://feedback_service:8002/feedback/health")

