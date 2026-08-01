from typing import Dict, Any, Optional, Protocol
from abc import ABC, abstractmethod
import numpy as np
import joblib
import os


class BaseModel(Protocol):
    def predict(self, X: np.ndarray) -> np.ndarray: ...
    def predict_proba(self, X: np.ndarray) -> np.ndarray: ...


class ModelRegistry:
    def __init__(self):
        self._models: Dict[str, BaseModel] = {}
        self._model_metadata: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, model: BaseModel, metadata: Dict[str, Any]) -> None:
        self._models[name] = model
        self._model_metadata[name] = metadata

    def get(self, name: str) -> Optional[BaseModel]:
        return self._models.get(name)

    def get_metadata(self, name: str) -> Optional[Dict[str, Any]]:
        return self._model_metadata.get(name)

    def list_models(self) -> Dict[str, Dict[str, Any]]:
        return {
            name: {
                **metadata,
                "loaded": name in self._models
            }
            for name, metadata in self._model_metadata.items()
        }

    def unload(self, name: str) -> bool:
        if name in self._models:
            del self._models[name]
            return True
        return False


model_registry = ModelRegistry()
