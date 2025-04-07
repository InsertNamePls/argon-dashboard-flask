# apps/api/services/client.py
from typing import Optional
from flask_login import current_user
from apps.api.services.datasets import DatasetService
from apps.api.services.models import ModelService
from apps.api.services.endpoints import EndpointService
import os

class ApiClient:
    """Main API client that combines all service modules"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        
        # Initialize service modules
        self.datasets = DatasetService(base_url, api_key)
        self.models = ModelService(base_url, api_key)
        self.endpoints = EndpointService(base_url, api_key)
    
    @classmethod
    def from_flask_config(cls, app):
        """Create API client from Flask app config"""
        api_url = app.config.get('API_BASE_URL', 'http://localhost:5000')
        api_key = app.config.get('API_KEY')
        return cls(api_url, api_key)
    
    @classmethod
    def for_current_user(cls, app):
        """Create API client for the current logged-in user"""
        api_url = app.config.get('API_BASE_URL', 'http://localhost:5000')
        
        # If user is authenticated, try to get their API key
        # This assumes your Users model has an api_key field
        if current_user.is_authenticated:
            try:
                api_key = current_user.api_key
            except AttributeError:
                # Fallback to global API key if user doesn't have one
                api_key = app.config.get('API_KEY')
        else:
            # Use global API key for anonymous users
            api_key = app.config.get('API_KEY')
            
        return cls(api_url, api_key)