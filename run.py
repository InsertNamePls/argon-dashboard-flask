# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit

from apps.config import config_dict
from apps import create_app, db

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

    # Determine if we're running in API-only mode
    # This is set by Dockerfile.api
    API_MODE = (os.getenv('API_MODE', 'False') == 'True')
    
    # Manually override app_config settings if necessary
    if API_MODE:
        if get_config_mode.capitalize() == 'Debug':
            app_config = type('ApiDebugConfig', (app_config,), {'API_ONLY': True})
        else:
            app_config = type('ApiProductionConfig', (app_config,), {'API_ONLY': True})

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

if not DEBUG and not app_config.API_ONLY:
    Minify(app=app, html=True, js=False, cssless=False)
    
if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG))
    app.logger.info('Environment      = ' + get_config_mode)
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    if hasattr(app_config, 'API_ONLY'):
        app.logger.info('API_ONLY         = ' + str(app_config.API_ONLY))
    
if __name__ == "__main__":
    app.run()