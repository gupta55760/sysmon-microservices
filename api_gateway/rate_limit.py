from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_counts = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        request_times = self.request_counts[client_ip]

        # Keep only timestamps within the window
        request_times = [ts for ts in request_times if now - ts < self.window_seconds]
        self.request_counts[client_ip] = request_times

        if len(request_times) >= self.max_requests:
            response = JSONResponse(
                status_code=429,
                content={"detail": "⏳ Too many requests. Please try again later."},
            )

            # ✅ Fix CORS issue for 429
            origin = request.headers.get("origin")
            if origin:
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Credentials"] = "true"

            return response

        request_times.append(now)
        return await call_next(request)

