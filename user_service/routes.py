from fastapi import APIRouter, Request, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
from user_service.auth import hash_password

from .models import User
from .schemas.user import UserCreate, UserUpdate, UserOut, UserListOut, LoginInput
from .auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password
)
from .database import get_db

router = APIRouter()

@router.post("/users/login")
def login(payload: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username, "role": user.role})
    print(f"Access token is {access_token}")
    refresh_token = create_refresh_token({"sub": user.username, "role": user.role})

    print(f"Refresh token is {refresh_token}")

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
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    payload = decode_token(token)
    if not payload or "sub" not in payload or "role" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or malformed refresh token")


    access_token = create_access_token({
        "sub": payload["sub"],
        "role": payload["role"]
    })

    return {"access_token": access_token}


@router.post("/users/logout")
def logout():
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
    if role != "admin":
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
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    return {"users": users, "total": total}

@router.post("/users/create_user", response_model=UserOut)
def create_user(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    role = request.headers.get("x-user-role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create users")

    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
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
    return new_user

@router.put("/users/{username}")
def update_user(username: str, request: Request, payload: UserUpdate, db: Session = Depends(get_db)):
    role = request.headers.get("x-user-role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update users")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    return {"message": f"User {username} updated"}

@router.delete("/users/{username}")
def delete_user(username: str, request: Request, db: Session = Depends(get_db)):
    role = request.headers.get("x-user-role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete users")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": f"User {username} deleted"}

@router.get("/users/health")
def health_check():
    return {"status": "ok"}
