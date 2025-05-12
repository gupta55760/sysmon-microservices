from fastapi import APIRouter, Request, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
from user_service.auth import hash_password
from user_service.logging_config import setup_logger

from .models import User
from .schemas.user import UserCreate, UserUpdate, UserOut, UserListOut, LoginInput
from .auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password
)
from .database import get_db

logger = setup_logger("user_service", "logs/user_service.log")
router = APIRouter()

@router.post("/users/login")
def login(payload: LoginInput, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for user: {payload.username}")
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        logger.warning(f"Failed login for user: {payload.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username, "role": user.role})
    refresh_token = create_refresh_token({"sub": user.username, "role": user.role})

    logger.info(f"Issued tokens for user: {user.username}")

    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        path="/api/users/refresh",
        max_age=14 * 24 * 60 * 60,
    )
    return response


@router.post("/users/refresh")
def refresh_token(request: Request):
    logger.info("Token refresh requested")
    token = request.cookies.get("refresh_token")
    if not token:
        logger.warning("Missing refresh token")
        raise HTTPException(status_code=401, detail="Missing refresh token")

    payload = decode_token(token)
    if not payload or "sub" not in payload or "role" not in payload:
        logger.warning("Invalid refresh token")
        raise HTTPException(status_code=401, detail="Invalid or malformed refresh token")

    logger.info(f"Issuing new access token for user: {payload['sub']}")
    access_token = create_access_token({
        "sub": payload["sub"],
        "role": payload["role"]
    })
    return {"access_token": access_token}


@router.post("/users/logout")
def logout():
    logger.info("User logged out")
    response = JSONResponse(content={"detail": "Logged out"})
    response.delete_cookie("refresh_token", path="/api/users/refresh")
    return response


@router.get("/users", response_model=UserListOut)
def list_users(request: Request, db: Session = Depends(get_db),
               skip: int = 0, limit: int = 10,
               sort_by: str = Query("id", enum=["id", "username"]),
               sort_order: str = Query("asc", enum=["asc", "desc"]),
               search: Optional[str] = None):
    role = request.headers.get("x-user-role")
    logger.info(f"User list requested by role: {role}")
    if role != "admin":
        logger.warning("Unauthorized access to user list")
        raise HTTPException(status_code=403, detail="Only admin can view users")

    query = db.query(User)
    if search:
        query = query.filter(User.username.contains(search))
    if sort_by == "username":
        sort_column = User.username.desc() if sort_order == "desc" else User.username.asc()
    else:
        sort_column = User.id.desc() if sort_order == "desc" else User.id.asc()

    users = query.order_by(sort_column).offset(skip).limit(limit).all()
    total = query.count()
    logger.info(f"Returned {len(users)} users out of {total}")
    return {"users": users, "total": total}


@router.post("/users/create_user", response_model=UserOut)
def create_user(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    role = request.headers.get("x-user-role")
    logger.info(f"Create user request from role: {role}")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create users")

    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        logger.warning(f"Attempt to create existing user: {user.username}")
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
        role=user.role,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User created: {new_user.username}")
    return new_user


@router.put("/users/{username}")
def update_user(username: str, request: Request, payload: UserUpdate, db: Session = Depends(get_db)):
    role = request.headers.get("x-user-role")
    logger.info(f"Update user request for {username} by role: {role}")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update users")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        logger.warning(f"User not found: {username}")
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    logger.info(f"User updated: {username}")
    return {"message": f"User {username} updated"}


@router.delete("/users/{username}")
def delete_user(username: str, request: Request, db: Session = Depends(get_db)):
    role = request.headers.get("x-user-role")
    logger.info(f"Delete user request for {username} by role: {role}")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete users")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        logger.warning(f"User not found: {username}")
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    logger.info(f"User deleted: {username}")
    return {"message": f"User {username} deleted"}


@router.get("/users/health")
def health_check():
    logger.info("Health check requested")
    return {"status": "ok"}

