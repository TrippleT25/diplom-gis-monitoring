from fastapi import FastAPI

app = FastAPI(
    title="GIS Monitoring API",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}