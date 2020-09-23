from django.urls import re_path

from v1.validator_confirmation_services.consumers.validation_confirmation_created import ValidationConfirmationConsumer

websocket_urlpatterns = [
    re_path(r'ws/validator_confirmation_services$', ValidationConfirmationConsumer),
]
