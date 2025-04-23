# scripts/init_db.py

from sysmon_sdk.db.database import Base, engine, SessionLocal
from sysmon_sdk.db.models import User
from passlib.context import CryptContext
import logging
logger = logging.getLogger(__name__)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create a session
db = SessionLocal()

# Password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Add default admin user if not exists
def bootstrap_user(username, plain_password, role):
    if not db.query(User).filter_by(username=username).first():
        user = User(
            username=username,
            hashed_password=pwd_context.hash(plain_password),
            role=role,
            is_active=True
        )
        db.add(user)
        logger.info(f"Added user: {username} ({role})")
    else:
        logger.info(f"User {username} already exists. Skipping.")

bootstrap_user("admin", "password123", "admin")
bootstrap_user("user", "userpass", "user")
bootstrap_user("viewer", "viewerpass", "viewer")

# Commit and close
db.commit()
db.close()

