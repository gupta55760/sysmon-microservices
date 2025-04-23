# main.py in feedback_service 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from feedback_service.routes import router
from feedback_service.database import Base, engine
from feedback_service import models

app = FastAPI(
    title="Feedback"
)

# Middlewares
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

# Proxy routes
app.include_router(router)

