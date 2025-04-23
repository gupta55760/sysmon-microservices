from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from metrics_service.routes import router as metrics_router
from metrics_service.metrics_collector import collect_metrics_forever
import threading
import psutil, time

app = FastAPI(
    title="SysMon Metrics Service",
    description="Provides system status and metrics",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def start_background_metrics():
    app.state.latest_metrics = {}
    t = threading.Thread(target=collect_metrics_forever, args=(app,), daemon=True)
    t.start()


app.include_router(metrics_router)
