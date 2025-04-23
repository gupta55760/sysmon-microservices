# api_gateway/schemas.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# --------------------
# User-related Schemas
# --------------------
class LoginInput(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., example="password123")

class RefreshTokenInput(BaseModel):
    refresh_token: str = Field(..., example="eyJhbGciOiJIUzI1...")

class UserBase(BaseModel):
    username: str = Field(..., example="newuser")
    role: str = Field(..., example="user")

class UserCreate(UserBase):
    password: str = Field(..., example="securepassword123")

class UserUpdate(BaseModel):
    password: Optional[str] = Field(None, example="newpassword123")
    role: Optional[str] = Field(None, example="admin")
    is_active: Optional[bool] = Field(None, example=True)

class UserOut(UserBase):
    is_active: bool

    model_config = {
        "from_attributes": True
    }

class UserListOut(BaseModel):
    total: int
    users: List[UserOut]

    model_config = {
        "from_attributes": True
    }

# --------------------
# Feedback-related Schemas
# --------------------
class FeedbackCreate(BaseModel):
    firstname: str = Field(..., example="Arun")
    lastname: str = Field(..., example="Gupta")
    email: EmailStr = Field(..., example="arun@example.com")
    rating: int = Field(..., ge=1, le=5, example=5)
    category: str = Field(..., example="Online Order")
    comments: Optional[str] = Field(None, example="Great service!")
    timestamp: Optional[str] = Field(None, example="2025-04-21T15:30:00Z")

class FeedbackOut(FeedbackCreate):
    id: int

    model_config = {
        "from_attributes": True
    }

