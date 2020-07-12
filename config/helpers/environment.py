import os

ENVIRONMENT = os.environ['DJANGO_APPLICATION_ENVIRONMENT']

if ENVIRONMENT == 'development':
    SETTINGS_MODULE = 'config.settings.development'

if ENVIRONMENT == 'local':
    SETTINGS_MODULE = 'config.settings.local'

if ENVIRONMENT == 'postgres_local':
    SETTINGS_MODULE = 'config.settings.local'

if ENVIRONMENT == 'production':
    SETTINGS_MODULE = 'config.settings.production'

if ENVIRONMENT == 'staging':
    SETTINGS_MODULE = 'config.settings.staging'
