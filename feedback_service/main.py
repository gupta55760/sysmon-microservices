# feedback_service/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from feedback_service.routes import router
from feedback_service.database import Base, engine
from feedback_service import models
from feedback_service.logging_config import setup_logger

# Setup logger
logger = setup_logger("feedback_service", "logs/feedback_service.log")

app = FastAPI(title="Feedback")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup_event():
    logger.info("Creating database tables on startup")
    Base.metadata.create_all(bind=engine)

app.include_router(router)

