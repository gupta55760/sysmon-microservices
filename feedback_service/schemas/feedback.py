# feedback_service/schemas/feedback.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class FeedbackCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    rating: int = Field(..., ge=1, le=5)
    category: str
    comments: Optional[str] = None
    timestamp: Optional[datetime] = None

class FeedbackOut(FeedbackCreate):
    id: int

    class Config:
        from_attributes = True

