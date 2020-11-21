import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.tornado import TornadoIntegration

from .base import *

sentry_sdk.init(
    'https://5a8286bb454c425baa7e995ebc3be100@o455400.ingest.sentry.io/5446923',
    traces_sample_rate=1.0,
    integrations=[CeleryIntegration(), DjangoIntegration(), RedisIntegration(), TornadoIntegration()],
)

DEBUG = False

INTERNAL_IPS = [
    '127.0.0.1',
]
