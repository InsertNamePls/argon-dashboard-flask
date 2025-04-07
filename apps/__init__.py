# apps/__init__.py

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    # Import and register blueprints
    for module_name in ('authentication', 'home', 'api'):
        module = import_module(f'apps.{module_name}.routes')
        
        # Try to get the blueprint variable (might have different names)
        if hasattr(module, 'blueprint'):
            app.register_blueprint(module.blueprint)
        elif hasattr(module, f'{module_name}_blueprint'):
            app.register_blueprint(getattr(module, f'{module_name}_blueprint'))
        elif hasattr(module, 'api_blueprint'):
            app.register_blueprint(module.api_blueprint)
    
    # Register the API v1 blueprint
    try:
        from apps.api.api_v1 import api_v1_blueprint
        app.register_blueprint(api_v1_blueprint)
    except ImportError:
        pass  # API v1 blueprint is optional

def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Add API configuration if not present
    if 'API_BASE_URL' not in app.config:
        app.config['API_BASE_URL'] = 'http://localhost:5000'
    
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    
    return app