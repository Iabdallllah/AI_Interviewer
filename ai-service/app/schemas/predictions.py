from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class PredictionType(str, Enum):
    CARBON_FOOTPRINT = "carbon_footprint"
    ENERGY_CONSUMPTION = "energy_consumption"
    EMISSIONS = "emissions"
    ENERGY_OPTIMIZATION = "energy_optimization"
    ANOMALY_DETECTION = "anomaly_detection"


class PredictionRequest(BaseModel):
    facility_id: str = Field(..., description="Unique facility identifier")
    prediction_type: PredictionType
    timestamp: str = Field(..., description="ISO format timestamp")
    features: Dict[str, Any] = Field(..., description="Input features for prediction")
    horizon_hours: Optional[int] = Field(default=24, description="Prediction horizon in hours")


class PredictionResponse(BaseModel):
    facility_id: str
    prediction_type: PredictionType
    timestamp: str
    predictions: List[Dict[str, Any]]
    confidence: float
    model_version: str
    metadata: Dict[str, Any] = {}


class BatchPredictionRequest(BaseModel):
    requests: List[PredictionRequest]


class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]
    summary: Dict[str, Any]


class AnomalyRequest(BaseModel):
    facility_id: str
    timestamp: str
    sensor_data: Dict[str, float]
    threshold: Optional[float] = 0.95


class AnomalyResponse(BaseModel):
    facility_id: str
    timestamp: str
    is_anomaly: bool
    anomaly_score: float
    affected_sensors: List[str]
    severity: str


class OptimizationRequest(BaseModel):
    facility_id: str
    current_consumption: Dict[str, float]
    constraints: Dict[str, Any] = {}
    objectives: List[str] = ["minimize_cost", "minimize_emissions"]


class OptimizationResponse(BaseModel):
    facility_id: str
    optimized_schedule: Dict[str, Any]
    estimated_savings: Dict[str, float]
    recommendations: List[str]
