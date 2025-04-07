# apps/api/services/models.py
import requests
from typing import Dict, Any, List, Optional

class ModelService:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"X-API-Key": api_key} if api_key else {}
        
        # Handle development mode
        self.is_local = 'localhost' in base_url or '127.0.0.1' in base_url
        
    def get_models(self) -> List[Dict[str, Any]]:
        """Get all available models"""
        if self.is_local:
            url = "/api/v1/models"
            from flask import current_app
            with current_app.test_client() as client:
                response = client.get(url, headers=self.headers)
                return response.get_json()
        else:
            response = requests.get(f"{self.base_url}/api/v1/models", headers=self.headers)
            response.raise_for_status()
            return response.json()

    def get_model(self, model_id: str) -> Dict[str, Any]:
        """Get a specific model by ID"""
        if self.is_local:
            url = f"/api/v1/models/{model_id}"
            from flask import current_app
            with current_app.test_client() as client:
                response = client.get(url, headers=self.headers)
                return response.get_json()
        else:
            response = requests.get(f"{self.base_url}/api/v1/models/{model_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()

    def train_model(self, training_data: Dict[str, Any]) -> Dict[str, Any]:
        """Train a new model"""
        if self.is_local:
            url = "/api/v1/models/train"
            from flask import current_app
            with current_app.test_client() as client:
                response = client.post(
                    url,
                    headers=self.headers,
                    json=training_data
                )
                return response.get_json()
        else:
            response = requests.post(
                f"{self.base_url}/api/v1/models/train",
                json=training_data,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()