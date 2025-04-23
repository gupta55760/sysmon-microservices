# api_gateway/auth.py

from jose import JWTError, jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"

def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # e.g. {"sub": "admin", "role": "admin"}
    except JWTError:
        return None

