# feedback_service/routes.py
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from feedback_service.database import get_db
from feedback_service.models import Feedback
from feedback_service.schemas.feedback import FeedbackCreate, FeedbackOut

router = APIRouter()

@router.post("/feedback", response_model=FeedbackOut)
def create_feedback(request: Request, feedback: FeedbackCreate, db: Session = Depends(get_db)):
    role = request.headers.get("x-user-role")
    if role != "admin":
      raise HTTPException(status_code=403, detail="Only admin can ingest feedback records")

    db_feedback = Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.get("/feedback", summary="List all feedback records (admin only)")
def get_all_feedback(request: Request, db: Session = Depends(get_db)):
    role = request.headers.get("x-user-role")
    if role != "admin":
      raise HTTPException(status_code=403, detail="Admin access required")
    return db.query(Feedback).order_by(Feedback.timestamp.desc()).all()

@router.get("/feedback/health")
def health_check():
    return {"status": "ok"}
