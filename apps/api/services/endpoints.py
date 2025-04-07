# apps/api/services/endpoints.py
import requests
from typing import Dict, Any, List, Optional

class EndpointService:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"X-API-Key": api_key} if api_key else {}
        
        # Handle development mode
        self.is_local = 'localhost' in base_url or '127.0.0.1' in base_url
        
    def get_endpoints(self) -> List[Dict[str, Any]]:
        """Get all available endpoints"""
        if self.is_local:
            url = "/api/v1/endpoints"
            from flask import current_app
            with current_app.test_client() as client:
                response = client.get(url, headers=self.headers)
                return response.get_json()
        else:
            response = requests.get(f"{self.base_url}/api/v1/endpoints", headers=self.headers)
            response.raise_for_status()
            return response.json()

    def get_endpoint(self, endpoint_id: str) -> Dict[str, Any]:
        """Get a specific endpoint by ID"""
        if self.is_local:
            url = f"/api/v1/endpoints/{endpoint_id}"
            from flask import current_app
            with current_app.test_client() as client:
                response = client.get(url, headers=self.headers)
                return response.get_json()
        else:
            response = requests.get(f"{self.base_url}/api/v1/endpoints/{endpoint_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()

    def deploy_endpoint(self, deployment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy a new endpoint"""
        if self.is_local:
            url = "/api/v1/endpoints/deploy"
            from flask import current_app
            with current_app.test_client() as client:
                response = client.post(
                    url,
                    headers=self.headers,
                    json=deployment_data
                )
                return response.get_json()
        else:
            response = requests.post(
                f"{self.base_url}/api/v1/endpoints/deploy",
                json=deployment_data,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    def invoke_endpoint(self, endpoint_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send inference request to an endpoint"""
        if self.is_local:
            url = f"/api/v1/predict/{endpoint_id}"
            from flask import current_app
            with current_app.test_client() as client:
                response = client.post(
                    url,
                    headers=self.headers,
                    json=input_data
                )
                return response.get_json()
        else:
            response = requests.post(
                f"{self.base_url}/api/v1/predict/{endpoint_id}",
                json=input_data,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()