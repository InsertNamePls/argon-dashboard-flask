# -*- encoding: utf-8 -*-
"""
Thalos application configuration
"""

import os
from decouple import config

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # SQLite database path (using mounted volume)
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI', default='sqlite:////data/thalos.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Configuration
    API_BASE_URL = config('API_BASE_URL', default='http://localhost:5000')
    API_KEY = config('API_KEY', default=None)
    
    # Whether this instance only serves API requests
    API_ONLY = False


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database (if needed in the future)
    # SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
    #     config('DB_ENGINE', default='postgresql'),
    #     config('DB_USERNAME', default='appseed'),
    #     config('DB_PASS', default='pass'),
    #     config('DB_HOST', default='localhost'),
    #     config('DB_PORT', default=5432),
    #     config('DB_NAME', default='appseed-flask')
    # )


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}