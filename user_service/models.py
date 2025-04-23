# PostgreSQL: user_service/models.py
from sqlalchemy import Column, Integer, String, Boolean
from user_service.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # 'admin', 'user', 'viewer'
    is_active = Column(Boolean, default=True)

