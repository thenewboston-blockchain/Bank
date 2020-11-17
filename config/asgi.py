"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""
import os

import django
from channels.routing import get_default_application

from config.helpers.environment import SETTINGS_MODULE

os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_MODULE)
django.setup()

application = get_default_application()

if os.getenv('SENTRY_DSN'):
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
    application = SentryAsgiMiddleware(application)
