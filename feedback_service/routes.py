# feedback_service/routes.py
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from feedback_service.database import get_db
from feedback_service.models import Feedback
from feedback_service.schemas.feedback import FeedbackCreate, FeedbackOut
from feedback_service.logging_config import setup_logger

logger = setup_logger("feedback_service", "logs/feedback_service.log")

router = APIRouter()

@router.post("/feedback", response_model=FeedbackOut)
def create_feedback(request: Request, feedback: FeedbackCreate, db: Session = Depends(get_db)):
    role = request.headers.get("x-user-role")
    logger.info(f"Create feedback request from role: {role}")
    if role != "admin":
        logger.warning("Unauthorized feedback creation attempt")
        raise HTTPException(status_code=403, detail="Only admin can ingest feedback records")

    db_feedback = Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    logger.info(f"Feedback created with ID: {db_feedback.id}")
    return db_feedback

@router.get("/feedback", summary="List all feedback records (admin only)")
def get_all_feedback(request: Request, db: Session = Depends(get_db)):
    role = request.headers.get("x-user-role")
    logger.info(f"List feedback request from role: {role}")
    if role != "admin":
        logger.warning("Unauthorized attempt to list feedback")
        raise HTTPException(status_code=403, detail="Admin access required")
    
    feedbacks = db.query(Feedback).order_by(Feedback.timestamp.desc()).all()
    logger.info(f"Returned {len(feedbacks)} feedback records")
    return feedbacks

@router.get("/feedback/health")
def health_check():
    logger.info("Health check requested")
    return {"status": "ok"}

