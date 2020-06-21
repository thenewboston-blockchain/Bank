from .base import *

DEBUG = True

INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

CELERY_BROKER_URL = 'redis://localhost'
CELERY_RESULT_BACKEND = 'redis://localhost'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

LOGGING = {
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'error.handler': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'error.log'),
            'formatter': 'verbose',
            'level': 'ERROR',
        },
        'warning.handler': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'warning.log'),
            'formatter': 'verbose',
            'level': 'WARNING',
        },
    },
    'loggers': {
        'thenewboston': {
            'handlers': ['error.handler', 'warning.handler'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
    'version': 1,
}
