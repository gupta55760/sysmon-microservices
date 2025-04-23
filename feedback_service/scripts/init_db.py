# ingest_service/scripts/init_db.py
from ingest_service.database import engine, Base
from ingest_service import models

Base.metadata.create_all(bind=engine)

