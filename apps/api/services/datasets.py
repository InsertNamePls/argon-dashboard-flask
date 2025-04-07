# apps/api/services/datasets.py
import requests
from typing import Dict, Any, List, Optional
import os

class DatasetService:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"X-API-Key": api_key} if api_key else {}
        
        # Handle development mode: if base URL is localhost or 127.0.0.1,
        # we're probably running in development and can use relative URLs
        self.is_local = 'localhost' in base_url or '127.0.0.1' in base_url
        
    def get_datasets(self) -> List[Dict[str, Any]]:
        """Get all available datasets"""
        if self.is_local:
            # For development, we can use a relative URL
            url = "/api/v1/datasets"
            # In development, we don't need to make a real HTTP request
            # as the API is part of the same app
            from flask import current_app
            with current_app.test_client() as client:
                response = client.get(url, headers=self.headers)
                return response.get_json()
        else:
            # For production/Docker, use the full URL
            response = requests.get(f"{self.base_url}/api/v1/datasets", headers=self.headers)
            response.raise_for_status()
            return response.json()

    def get_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """Get a specific dataset by ID"""
        if self.is_local:
            url = f"/api/v1/datasets/{dataset_id}"
            from flask import current_app
            with current_app.test_client() as client:
                response = client.get(url, headers=self.headers)
                return response.get_json()
        else:
            response = requests.get(f"{self.base_url}/api/v1/datasets/{dataset_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()

    def create_dataset(self, dataset_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new dataset"""
        if self.is_local:
            url = "/api/v1/datasets"
            from flask import current_app, json
            with current_app.test_client() as client:
                response = client.post(
                    url,
                    headers=self.headers,
                    json=dataset_data
                )
                return response.get_json()
        else:
            response = requests.post(
                f"{self.base_url}/api/v1/datasets",
                json=dataset_data,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()