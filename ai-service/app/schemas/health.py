from pydantic import BaseModel
from typing import Dict, Any, Optional
from enum import Enum


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthResponse(BaseModel):
    status: HealthStatus
    version: str
    uptime_seconds: float
    services: Dict[str, HealthStatus]
    details: Optional[Dict[str, Any]] = {}


class ModelInfo(BaseModel):
    name: str
    version: str
    type: str
    metrics: Dict[str, float]
    last_trained: str
    status: str


class ModelsResponse(BaseModel):
    models: list[ModelInfo]
