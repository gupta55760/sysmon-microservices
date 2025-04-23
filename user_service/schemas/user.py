# user_service/schemas/user.py

from pydantic import BaseModel, Field
from typing import Optional, List
import logging
logger = logging.getLogger(__name__)


class UserBase(BaseModel):
    username: str = Field(..., example="newuser")
    role: str = Field(..., example="user")


class UserCreate(UserBase):
    password: str = Field(..., example="securepassword123")


class UserUpdate(BaseModel):
    password: Optional[str] = Field(None, example="newpassword123")
    role: Optional[str] = Field(None, example="admin")
    is_active: Optional[bool] = Field(None, example=True)

class RefreshTokenInput(BaseModel):
    refresh_token: str = Field(..., example="eyJhbGciOiJIUzI1...")

class LoginInput(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., example="password123")


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

