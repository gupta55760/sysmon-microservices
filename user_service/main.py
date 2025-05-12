from fastapi import FastAPI
from user_service.routes import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from user_service.logging_config import setup_logger

# Setup logger
logger = setup_logger("user_service", "logs/user_service.log")

app = FastAPI(title="User Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("User service started and middleware initialized")

# Include user-related routes
app.include_router(user_router)

