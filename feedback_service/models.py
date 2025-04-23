# PostgreSQL: feedback_service/models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from feedback_service.database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    comments = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

