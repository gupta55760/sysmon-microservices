from user_service.database import Base, engine
from user_service.models import User

# Drop all tables
Base.metadata.drop_all(bind=engine)
print("✅ All tables dropped.")

# Recreate tables
Base.metadata.create_all(bind=engine)
print("✅ All tables recreated.")

