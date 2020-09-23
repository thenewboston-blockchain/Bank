import iptools

from .base import *

DEBUG = True

INTERNAL_IPS = iptools.IpRangeList(
    '10/8',
    '127/8',
    '172.16/12',
    '192.168/16'
)

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

CELERY_BROKER_URL = f'redis://{os.getenv("REDIS_HOST", "localhost")}'
CELERY_RESULT_BACKEND = f'redis://{os.getenv("REDIS_HOST", "localhost")}'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{os.getenv("REDIS_HOST", "localhost")}:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}


# class DisableMigrations(object):
#     def __contains__(self, item):
#         """DisableMigrations.__contains__ magic method"""
#         return True
#
#     def __getitem__(self, item):
#         """DisableMigrations.__getitem__ magic method"""
#         return None
#
#
# MIGRATION_MODULES = DisableMigrations()
# # TODO: Commit it uncommented permanently only when a separate migration test implemented
