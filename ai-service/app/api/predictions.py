from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
import numpy as np

router = APIRouter()


# Schemas
class PredictionRequest(BaseModel):
    factoryId: str
    historicalData: List[float]
    type: str = "electricity"
    hours: int = 24


class PredictionResponse(BaseModel):
    prediction: float
    confidence: float
    trend: str
    recommendation: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class LeakRequest(BaseModel):
    sensorId: str
    readings: List[Dict[str, Any]]
    threshold: float = 3.0


class LeakResponse(BaseModel):
    hasLeak: bool
    confidence: float
    location: str
    estimatedLoss: float
    cost: float
    carbonImpact: float
    recommendation: str


class AnomalyRequest(BaseModel):
    sensorId: str
    readings: List[Dict[str, Any]]
    threshold: float = 3.0


class AnomalyItem(BaseModel):
    timestamp: str
    value: float
    expectedValue: float
    deviation: float
    score: float


class AnomalyResponse(BaseModel):
    anomalies: List[AnomalyItem]
    threshold: float


class MaintenanceRequest(BaseModel):
    machineId: str
    readings: List[Dict[str, Any]]
    historicalFailures: List[Dict[str, Any]] = []


class MaintenanceResponse(BaseModel):
    machineId: str
    predictedFailure: bool
    confidence: float
    daysUntilFailure: int
    recommendedAction: str
    partsToCheck: List[str]


class HeatRecoveryRequest(BaseModel):
    heatSource: Dict[str, Any]
    wasteHeat: float
    recoverableHeat: float
    factoryId: str


class HeatRecoverySolution(BaseModel):
    type: str
    name: str
    potentialRecovery: float
    efficiency: float
    cost: float
    savings: float
    carbonReduction: float
    roi: float
    paybackPeriod: float


class HeatRecoveryResponse(BaseModel):
    totalWasteHeat: float
    recoverableHeat: float
    solutions: List[HeatRecoverySolution]
    potentialSavings: float
    carbonReduction: float
    roi: float
    paybackPeriod: float


class RecommendationRequest(BaseModel):
    type: str
    currentConsumption: float
    targetReduction: float
    factoryId: str


class RecommendationItem(BaseModel):
    title: str
    description: str
    potentialSavings: float
    carbonReduction: float
    priority: str
    estimatedCost: float
    paybackPeriod: float


class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class CarbonRequest(BaseModel):
    factoryId: str
    currentEmissions: float
    historicalData: List[Dict[str, Any]]
    type: str = "direct_emissions"


class CarbonResponse(BaseModel):
    predictedEmissions: float
    confidence: float
    trend: str
    reductionPotential: float
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class IndustrialMatchRequest(BaseModel):
    companyId: str
    resourceType: str
    quantity: float
    unit: str
    location: Dict[str, str]


class MatchItem(BaseModel):
    companyId: str
    companyName: str
    factoryId: str
    distance: float
    score: float
    potentialSavings: float
    carbonReduction: float


class IndustrialMatchResponse(BaseModel):
    matches: List[MatchItem]
    recommendedPartner: Dict[str, Any]
    recommendations: List[str]


class FinancialRequest(BaseModel):
    estimatedSavings: float
    estimatedCost: float
    timeframe: int
    type: str


class FinancialResponse(BaseModel):
    savings: float
    carbonReduction: float
    paybackPeriod: float
    roi: float
    netPresentValue: float
    internalRateReturn: float
    recommendation: str


class WhatIfRequest(BaseModel):
    factoryId: str
    scenario: Dict[str, Any]


class WhatIfResponse(BaseModel):
    scenario: Dict[str, Any]
    results: Dict[str, Any]
    recommendation: str


class BaselineModels:
    @staticmethod
    def predict_consumption(historical_data: List[float], hours: int = 24) -> dict:
        if not historical_data:
            return {"prediction": 100.0, "confidence": 0.5, "trend": "stable", "recommendation": "Insufficient data"}
        
        recent = historical_data[-min(7, len(historical_data)):]
        avg = sum(recent) / len(recent)
        trend = "increasing" if len(recent) > 1 and recent[-1] > recent[0] else "decreasing" if len(recent) > 1 and recent[-1] < recent[0] else "stable"
        seasonal_factor = 1.0 + 0.1 * np.sin(len(historical_data) * 0.5)
        prediction = avg * seasonal_factor
        confidence = min(0.95, 0.7 + len(historical_data) * 0.02)
        
        rec_map = {
            "increasing": "Check for abnormal consumption during peak hours",
            "decreasing": "Good trend, maintain current efficiency measures",
            "stable": "Monitor for anomalies during operational changes"
        }
        
        return {
            "prediction": round(prediction, 1),
            "confidence": round(confidence, 2),
            "trend": trend,
            "recommendation": rec_map[trend]
        }

    @staticmethod
    def detect_leak(readings: List[Dict], threshold: float = 3.0) -> dict:
        values = [r["value"] for r in readings if "value" in r]
        if len(values) < 3:
            return {"hasLeak": False, "confidence": 0.5, "location": "Unknown", "estimatedLoss": 0, "cost": 0, "carbonImpact": 0, "recommendation": "Insufficient data"}
        
        mean_val = np.mean(values[:-1])
        std_val = max(np.std(values[:-1]) if len(values) > 2 else 1.0, 0.1)
        last_val = values[-1]
        z_score = abs(last_val - mean_val) / std_val
        
        if z_score > threshold:
            loss = max(0, last_val - mean_val - threshold * std_val) * 5
            return {
                "hasLeak": True,
                "confidence": round(min(0.99, 0.5 + z_score * 0.1), 2),
                "location": "Pipe section 3A",
                "estimatedLoss": round(loss, 1),
                "cost": round(loss * 0.8, 1),
                "carbonImpact": round(loss * 0.3, 1),
                "recommendation": "Check joint between sections 3A and 3B"
            }
        
        return {
            "hasLeak": False,
            "confidence": round(min(0.99, 0.5 + z_score * 0.1), 2),
            "location": "N/A",
            "estimatedLoss": 0,
            "cost": 0,
            "carbonImpact": 0,
            "recommendation": "No leak detected"
        }

    @staticmethod
    def detect_anomalies(readings: List[Dict], threshold: float = 3.0) -> dict:
        anomalies = []
        values = [r["value"] for r in readings if "value" in r]
        timestamps = [r["timestamp"] for r in readings if "value" in r]
        
        if len(values) < 3:
            return {"anomalies": [], "threshold": threshold}
        
        mean_val = np.mean(values)
        std_val = max(np.std(values) if len(values) > 2 else 1.0, 0.1)
        
        for ts, val in zip(timestamps, values):
            z_score = abs(val - mean_val) / std_val
            if z_score > threshold:
                anomalies.append({
                    "timestamp": ts,
                    "value": val,
                    "expectedValue": round(mean_val, 1),
                    "deviation": round(val - mean_val, 1),
                    "score": round(z_score, 1)
                })
        
        return {"anomalies": anomalies, "threshold": threshold}

    @staticmethod
    def predict_maintenance(machine_id: str, readings: List[Dict], historical_failures: List[Dict]) -> dict:
        if not readings:
            return {"machineId": machine_id, "predictedFailure": False, "confidence": 0.5, "daysUntilFailure": 999, "recommendedAction": "No data available", "partsToCheck": []}
        
        latest = readings[-1]
        vibration = latest.get("vibration", 2.0)
        temperature = latest.get("temperature", 60)
        rpm = latest.get("rpm", 1500)
        
        failure_score = (vibration > 3.0) * 0.4 + (temperature > 80) * 0.3 + (rpm < 1000 or rpm > 2000) * 0.2 + min(len(historical_failures), 3) * 0.1
        predicted = failure_score > 0.5
        confidence = min(0.95, 0.5 + failure_score)
        days_until = max(1, int(30 * (1 - failure_score)))
        
        parts = []
        if vibration > 3.0: parts.append("bearing")
        if temperature > 80: parts.append("cooling_system")
        if rpm < 1000 or rpm > 2000: parts.append("motor")
        parts.append("lubrication_system")
        
        return {
            "machineId": machine_id,
            "predictedFailure": predicted,
            "confidence": round(confidence, 2),
            "daysUntilFailure": days_until,
            "recommendedAction": "Replace bearing and check lubrication" if predicted else "Continue preventive maintenance schedule",
            "partsToCheck": parts
        }

    @staticmethod
    def analyze_heat_recovery(waste_heat: float, recoverable_heat: float, heat_source: Dict) -> dict:
        temp = heat_source.get("temperature", 150)
        efficiency = min(0.9, 0.5 + temp / 500)
        potential_recovery = recoverable_heat * efficiency
        
        cost_per_kwh = 15
        savings_per_kwh = 12
        cost = max(potential_recovery * cost_per_kwh / 100, 1)
        savings = potential_recovery * savings_per_kwh / 100
        carbon_reduction = potential_recovery * 0.1
        roi = (savings / cost * 100)
        payback = cost / savings * 12 if savings > 0 else 0
        
        return {
            "totalWasteHeat": waste_heat,
            "recoverableHeat": recoverable_heat,
            "solutions": [{
                "type": "heat_exchanger",
                "name": "Shell and Tube Heat Exchanger",
                "potentialRecovery": round(potential_recovery, 1),
                "efficiency": round(efficiency * 100, 1),
                "cost": round(cost, 1),
                "savings": round(savings, 1),
                "carbonReduction": round(carbon_reduction, 1),
                "roi": round(roi, 1),
                "paybackPeriod": round(payback, 1)
            }],
            "potentialSavings": round(savings, 1),
            "carbonReduction": round(carbon_reduction, 1),
            "roi": round(roi, 1),
            "paybackPeriod": round(payback, 1)
        }

    @staticmethod
    def generate_recommendations(req_type: str, current: float, target: float) -> dict:
        reduction_target = current * target / 100
        recommends = []
        
        if req_type in ("energy", "electricity"):
            recommends = [
                {"title": "تحسين كفاءة الطاقة", "description": "استبدال الإضاءة بـ LED وتركيب محركات عالية الكفاءة", "potentialSavings": round(reduction_target * 0.4, 1), "carbonReduction": round(reduction_target * 0.5, 1), "priority": "high", "estimatedCost": round(reduction_target * 10, 1), "paybackPeriod": 0.7},
                {"title": "تحسين أنظمة التبريد", "description": "تركيب وحدات VFD على المضخات والمراوح", "potentialSavings": round(reduction_target * 0.3, 1), "carbonReduction": round(reduction_target * 0.3, 1), "priority": "medium", "estimatedCost": round(reduction_target * 15, 1), "paybackPeriod": 1.2},
                {"title": "نظام إدارة الطاقة (EMS)", "description": "تركيب نظام مراقبة وتحكم آلي في الاستهلاك", "potentialSavings": round(reduction_target * 0.2, 1), "carbonReduction": round(reduction_target * 0.2, 1), "priority": "medium", "estimatedCost": round(reduction_target * 8, 1), "paybackPeriod": 1.0}
            ]
        elif req_type == "water":
            recommends = [{"title": "إعادة تدوير المياه", "description": "تركيب نظام معالجة وإعادة استخدام المياه الرمادية", "potentialSavings": round(reduction_target * 0.5, 1), "carbonReduction": round(reduction_target * 0.1, 1), "priority": "high", "estimatedCost": round(reduction_target * 20, 1), "paybackPeriod": 1.5}]
        elif req_type == "fuel":
            recommends = [{"title": "تحسين كفاءة الوقود", "description": "تحويل المعدات إلى مصادر طاقة أنظف", "potentialSavings": round(reduction_target * 0.35, 1), "carbonReduction": round(reduction_target * 0.7, 1), "priority": "high", "estimatedCost": round(reduction_target * 25, 1), "paybackPeriod": 2.0}]
        
        return {"recommendations": recommends, "timestamp": datetime.utcnow().isoformat() + "Z"}

    @staticmethod
    def predict_carbon(current: float, historical: List[Dict], emission_type: str) -> dict:
        if len(historical) < 2:
            return {"predictedEmissions": round(current * 1.02, 1), "confidence": 0.6, "trend": "stable", "reductionPotential": round(current * 0.15, 1), "timestamp": datetime.utcnow().isoformat() + "Z"}
        
        values = [h["emissions"] for h in historical if "emissions" in h]
        if len(values) < 2:
            values = [current * 0.98, current]
        
        trend_slope = (values[-1] - values[0]) / len(values)
        predicted = values[-1] + trend_slope
        trend = "increasing" if trend_slope > 0 else "decreasing" if trend_slope < 0 else "stable"
        
        return {
            "predictedEmissions": round(predicted, 1),
            "confidence": round(min(0.95, 0.7 + len(values) * 0.03), 2),
            "trend": trend,
            "reductionPotential": round(current * 0.15, 1),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    @staticmethod
    def industrial_matching(resource_type: str, quantity: float, location: Dict, company_id: str) -> dict:
        matches = [
            {"companyId": "company_002", "companyName": "Steel Factory", "factoryId": "factory_002", "distance": 15.0, "score": 92, "potentialSavings": 4500, "carbonReduction": 225},
            {"companyId": "company_003", "companyName": "Cement Plant", "factoryId": "factory_003", "distance": 28.0, "score": 78, "potentialSavings": 3200, "carbonReduction": 180}
        ]
        
        return {
            "matches": matches,
            "recommendedPartner": matches[0],
            "recommendations": [f"Contact {matches[0]['companyName']} for {resource_type} exchange agreement"]
        }

    @staticmethod
    def financial_analysis(savings: float, cost: float, timeframe: int, analysis_type: str) -> dict:
        annual_savings = savings
        total_savings = annual_savings * timeframe
        payback = cost / max(annual_savings, 1)
        roi = (total_savings - cost) / max(cost, 1) * 100
        
        discount_rate = 0.08
        npv = sum(annual_savings / (1 + discount_rate) ** t for t in range(1, timeframe + 1)) - cost
        irr = 0.15 if roi > 0 else 0.05
        
        return {
            "savings": total_savings,
            "carbonReduction": round(total_savings * 0.023, 1),
            "paybackPeriod": round(payback, 1),
            "roi": round(roi, 1),
            "netPresentValue": round(npv, 1),
            "internalRateReturn": round(irr * 100, 1),
            "recommendation": f"يوصى بتنفيذ المشروع، عائد الاستثمار {roi:.0f}%" if roi > 15 else "يحتاج دراسة جدوى تفصيلية"
        }

    @staticmethod
    def whatif_analysis(scenario: Dict, factory_id: str) -> dict:
        investment = scenario.get("investment", 50000)
        expected_savings_pct = scenario.get("expectedSavings", 20)
        current_consumption = scenario.get("currentConsumption", 150000)
        
        energy_saved = current_consumption * expected_savings_pct / 100
        cost_saved = energy_saved * 0.15
        carbon_reduced = energy_saved * 0.5
        roi = (cost_saved * 5 - investment) / investment * 100
        payback = investment / max(cost_saved, 1)
        
        return {
            "scenario": {"type": scenario.get("type", "solar_panels"), "investment": investment, "expectedSavings": expected_savings_pct},
            "results": {"energySaved": round(energy_saved, 1), "costSaved": round(cost_saved, 1), "carbonReduced": round(carbon_reduced, 1), "roi": round(roi, 1), "paybackPeriod": round(payback, 1)},
            "recommendation": "يوصى بتنفيذ المشروع" if roi > 20 else "يحتاج دراسة جدوى تفصيلية"
        }


models = BaselineModels()


@router.post("/predict/consumption", response_model=PredictionResponse)
async def predict_consumption(request: PredictionRequest):
    return PredictionResponse(**models.predict_consumption(request.historicalData, request.hours))


@router.post("/detect/leak", response_model=LeakResponse)
async def detect_leak(request: LeakRequest):
    return LeakResponse(**models.detect_leak(request.readings, request.threshold))


@router.post("/detect/anomalies", response_model=AnomalyResponse)
async def detect_anomalies(request: AnomalyRequest):
    return AnomalyResponse(**models.detect_anomalies(request.readings, request.threshold))


@router.post("/predict/maintenance", response_model=MaintenanceResponse)
async def predict_maintenance(request: MaintenanceRequest):
    return MaintenanceResponse(**models.predict_maintenance(request.machineId, request.readings, request.historicalFailures))


@router.post("/analyze/heat-recovery", response_model=HeatRecoveryResponse)
async def analyze_heat_recovery(request: HeatRecoveryRequest):
    return HeatRecoveryResponse(**models.analyze_heat_recovery(request.wasteHeat, request.recoverableHeat, request.heatSource))


@router.post("/generate/recommendations", response_model=RecommendationResponse)
async def generate_recommendations(request: RecommendationRequest):
    return RecommendationResponse(**models.generate_recommendations(request.type, request.currentConsumption, request.targetReduction))


@router.post("/predict/carbon", response_model=CarbonResponse)
async def predict_carbon(request: CarbonRequest):
    return CarbonResponse(**models.predict_carbon(request.currentEmissions, request.historicalData, request.type))


@router.post("/match/industrial", response_model=IndustrialMatchResponse)
async def match_industrial(request: IndustrialMatchRequest):
    return IndustrialMatchResponse(**models.industrial_matching(request.resourceType, request.quantity, request.location, request.companyId))


@router.post("/analyze/financial", response_model=FinancialResponse)
async def analyze_financial(request: FinancialRequest):
    return FinancialResponse(**models.financial_analysis(request.estimatedSavings, request.estimatedCost, request.timeframe, request.type))


@router.post("/analyze/whatif", response_model=WhatIfResponse)
async def analyze_whatif(request: WhatIfRequest):
    return WhatIfResponse(**models.whatif_analysis(request.scenario, request.factoryId))
