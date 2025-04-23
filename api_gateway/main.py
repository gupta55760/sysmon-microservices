from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_gateway.routes import router
from api_gateway.rate_limit import RateLimiterMiddleware  # 👈 Add this import
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="SysMon API Gateway",
    docs_url="/docs",             # Swagger UI
    redoc_url="/redoc",           # ReDoc UI (optional)
    openapi_url="/openapi.json",   # OpenAPI schema
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",  # 👈 Required for Authorize flow
    swagger_ui_init_oauth={  # Enables 'Authorize' button
        "usePkceWithAuthorizationCodeGrant": False
    }
)

# ✅ CORS for React dev server at :3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Add rate limiting middleware (e.g. 20 requests per minute)
app.add_middleware(RateLimiterMiddleware, max_requests=100, window_seconds=60)

@app.get("/health", summary="Check apigateway health")
def health_check():
    return {"status": "ok"}

# ✅ Include proxy routes
app.include_router(router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Set default security for all endpoints
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

