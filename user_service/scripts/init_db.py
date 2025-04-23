# user_service/scripts/init_db.py

from user_service.database import Base, engine, SessionLocal
from user_service.models import User
from user_service.auth import hash_password
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create a session
db = SessionLocal()

# Add default users
def bootstrap_user(username, plain_password, role):
    if not db.query(User).filter_by(username=username).first():
        user = User(
            username=username,
            hashed_password=hash_password(plain_password),
            role=role
        )
        db.add(user)
        logger.info(f"✅ Added user: {username} ({role})")
    else:
        logger.info(f"⏭️ User {username} already exists. Skipping.")

bootstrap_user("admin", "password123", "admin")
bootstrap_user("user", "userpass", "user")
bootstrap_user("viewer", "viewerpass", "viewer")

# Commit and close
db.commit()
db.close()

