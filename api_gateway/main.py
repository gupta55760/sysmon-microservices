from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_gateway.routes import router
from api_gateway.rate_limit import RateLimiterMiddleware
from fastapi.openapi.utils import get_openapi
from api_gateway.logging_config import setup_logger

# Setup logger
logger = setup_logger("api_gateway", "logs/api_gateway.log")

app = FastAPI(
    title="SysMon API Gateway",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": False
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimiterMiddleware, max_requests=100, window_seconds=60)

logger.info("API Gateway started with CORS and Rate Limiting enabled")

@app.get("/health", summary="Check apigateway health")
def health_check():
    logger.info("Health check hit")
    return {"status": "ok"}

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

    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

