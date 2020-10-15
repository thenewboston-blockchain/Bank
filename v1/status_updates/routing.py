from django.urls import re_path

from .consumers.primary_validator_updated import PrimaryValidatorUpdatedConsumer

websocket_urlpatterns = [
    re_path(r'ws/primary_validator_updated$', PrimaryValidatorUpdatedConsumer),
]
