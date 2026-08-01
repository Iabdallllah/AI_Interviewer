from typing import Dict, Any, List, Optional
from datetime import datetime
import numpy as np
from app.models.baseline import (
    CarbonFootprintModel,
    EnergyConsumptionModel,
    AnomalyDetectionModel,
    EnergyOptimizationModel
)
from app.models.registry import model_registry
from app.schemas.predictions import (
    PredictionRequest, PredictionResponse, PredictionType,
    AnomalyRequest, AnomalyResponse,
    OptimizationRequest, OptimizationResponse,
    BatchPredictionRequest, BatchPredictionResponse
)


class PredictionService:
    def __init__(self):
        self._models = {}
        self._initialize_models()

    def _initialize_models(self):
        self._models = {
            "carbon_footprint": CarbonFootprintModel(),
            "energy_consumption": EnergyConsumptionModel(),
            "anomaly_detection": AnomalyDetectionModel(),
            "energy_optimization": EnergyOptimizationModel()
        }
        for name, model in self._models.items():
            model_registry.register(name, model, {
                "name": name,
                "version": model.version,
                "type": type(model).__name__,
                "metrics": {"status": "loaded"}
            })

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        model = self._get_model(request.prediction_type)
        if not model:
            raise ValueError(f"Model for {request.prediction_type} not found")

        if request.prediction_type == PredictionType.CARBON_FOOTPRINT:
            result = model.predict(request.features)
            predictions = [{
                "horizon_hours": 0,
                **result
            }]
        elif request.prediction_type == PredictionType.ENERGY_CONSUMPTION:
            result = model.predict(request.features, request.horizon_hours)
            predictions = result["predictions"]
        elif request.prediction_type == PredictionType.EMISSIONS:
            result = model.predict(request.features)
            predictions = [{
                "horizon_hours": 0,
                "emissions_kg_co2e": result["carbon_footprint_kg_co2e"],
                "confidence": result["confidence"]
            }]
        else:
            result = model.predict(request.features)
            predictions = [{"result": result}]

        return PredictionResponse(
            facility_id=request.facility_id,
            prediction_type=request.prediction_type,
            timestamp=request.timestamp,
            predictions=predictions,
            confidence=result.get("confidence", 0.85),
            model_version=model.version,
            metadata={"horizon_hours": request.horizon_hours}
        )

    def predict_batch(self, request: BatchPredictionRequest) -> BatchPredictionResponse:
        predictions = []
        for req in request.requests:
            try:
                pred = self.predict(req)
                predictions.append(pred)
            except Exception as e:
                predictions.append(PredictionResponse(
                    facility_id=req.facility_id,
                    prediction_type=req.prediction_type,
                    timestamp=req.timestamp,
                    predictions=[],
                    confidence=0.0,
                    model_version="error",
                    metadata={"error": str(e)}
                ))

        summary = {
            "total_requests": len(request.requests),
            "successful": sum(1 for p in predictions if p.confidence > 0),
            "failed": sum(1 for p in predictions if p.confidence == 0),
            "avg_confidence": np.mean([p.confidence for p in predictions if p.confidence > 0]) if any(p.confidence > 0 for p in predictions) else 0
        }

        return BatchPredictionResponse(predictions=predictions, summary=summary)

    def detect_anomaly(self, request: AnomalyRequest) -> AnomalyResponse:
        model = self._models.get("anomaly_detection")
        if not model:
            raise ValueError("Anomaly detection model not found")

        result = model.predict(request.sensor_data, request.threshold)

        return AnomalyResponse(
            facility_id=request.facility_id,
            timestamp=request.timestamp,
            is_anomaly=result["is_anomaly"],
            anomaly_score=result["anomaly_score"],
            affected_sensors=result["affected_sensors"],
            severity=result["severity"]
        )

    def optimize_energy(self, request: OptimizationRequest) -> OptimizationResponse:
        model = self._models.get("energy_optimization")
        if not model:
            raise ValueError("Energy optimization model not found")

        result = model.optimize(request.current_consumption, request.constraints, request.objectives)

        return OptimizationResponse(
            facility_id=request.facility_id,
            optimized_schedule=result["optimized_schedule"],
            estimated_savings=result["estimated_savings"],
            recommendations=result["recommendations"]
        )

    def _get_model(self, prediction_type: PredictionType):
        type_map = {
            PredictionType.CARBON_FOOTPRINT: "carbon_footprint",
            PredictionType.ENERGY_CONSUMPTION: "energy_consumption",
            PredictionType.EMISSIONS: "carbon_footprint",
            PredictionType.ENERGY_OPTIMIZATION: "energy_optimization",
            PredictionType.ANOMALY_DETECTION: "anomaly_detection"
        }
        model_name = type_map.get(prediction_type)
        return self._models.get(model_name) if model_name else None

    def get_model_info(self) -> Dict[str, Any]:
        return model_registry.list_models()


prediction_service = PredictionService()
