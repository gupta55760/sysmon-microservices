import httpx
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from api_gateway.auth import verify_jwt_token
from api_gateway.logging_config import setup_logger

logger = setup_logger("api_gateway", "logs/api_gateway.log")

def is_protected(path: str) -> bool:
    PUBLIC_PATHS = [
        "/api/users/login",
        "/api/users/refresh",
        "/api/users/logout",
        "/api/metrics/version",
        "/api/metrics/health",
    ]
    if any(path.startswith(pub) for pub in PUBLIC_PATHS):
        return False
    return any(path.startswith(p) for p in ["/api/users", "/api/metrics", "/api/feedback"])

async def forward_request(request: Request, target_url: str) -> Response:
    logger.info(f"Forwarding request to: {target_url}")
    if is_protected(request.url.path):
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("Missing or invalid Authorization header")
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid Authorization header"})

        token = auth_header[7:]
        decoded = verify_jwt_token(token)
        if not decoded:
            logger.warning("Invalid or expired JWT token")
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

        logger.info(f"JWT validated for user: {decoded.get('sub')}")

        headers = {
            k: v for k, v in request.headers.items()
            if k.lower() not in ("host", "x-user-role", "x-user-id")
        }
        headers["x-user-id"] = decoded.get("sub", "")
        headers["x-user-role"] = decoded.get("role", "")
    else:
        logger.info("Public route accessed")
        headers = {
            k: v for k, v in request.headers.items() if k.lower() != "host"
        }

    body = await request.body()

    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=target_url,
            content=body,
            headers=headers,
            params=request.query_params,
        )

    logger.info(f"Received response {resp.status_code} from {target_url}")
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=dict(resp.headers),
    )

