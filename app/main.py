from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.monitoring_objects import (
    router as monitoring_objects_router,
)
from app.routers.measurements import router as measurements_router


app = FastAPI(
    title="GIS Monitoring API",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(monitoring_objects_router)