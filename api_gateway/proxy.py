import httpx
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from api_gateway.auth import verify_jwt_token


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
    print(f"🔥 PATH RECEIVED: {request.url.path!r}")
    if is_protected(request.url.path):
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid Authorization header"})

        token = auth_header[7:]
        print(f"auth_header is {auth_header}")
        print(f"token is {token}")
        decoded = verify_jwt_token(token)
        print(f"decoded token is {decoded}")
        if not decoded:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

        # Inject identity headers
        headers = {
          k: v for k, v in request.headers.items()
          if k.lower() not in ("host", "x-user-role", "x-user-id")
        }

        headers["x-user-id"] = decoded.get("sub", "")
        headers["x-user-role"] = decoded.get("role", "")
    else:
        # No auth check for login/refresh
        print(f"aaaaaaaaaaaaaaaaaa")
        headers = {
            k: v for k, v in request.headers.items() if k.lower() != "host"
        }
        print(f"headers is {headers}")

    body = await request.body()

    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=target_url,
            content=body,
            headers=headers,
            params=request.query_params,
        )

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=dict(resp.headers),
    )

