from django.urls import re_path

from .consumers.confirmation_block import ConfirmationBlockConsumer

websocket_urlpatterns = [
    re_path(r'ws/confirmation_blocks/(?P<account_number>[a-f0-9]{64})$', ConfirmationBlockConsumer),
]
