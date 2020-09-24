from django.urls import re_path

from .consumers.validator_confirmation_service import ValidatorConfirmationServiceConsumer

websocket_urlpatterns = [
    re_path(r'ws/validator_confirmation_services$', ValidatorConfirmationServiceConsumer),
]
