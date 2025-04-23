from fastapi import FastAPI
from user_service.routes import router as user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="User Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include user-related routes
app.include_router(user_router)

