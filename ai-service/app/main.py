from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import predictions
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="AI Service for EcoGuardian - Environmental Monitoring & Optimization",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predictions.router, prefix="/api/v1", tags=["Predictions"])


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models": ["consumption", "leak", "anomaly", "maintenance", "heat_recovery", "recommendation", "carbon", "industrial_matching", "financial", "whatif"],
        "timestamp": "2026-07-24T12:00:00Z"
    }


@app.get("/")
async def root():
    return {"message": "AI ECO Service - EcoGuardian", "version": "1.0.0", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
