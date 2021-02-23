from django.urls import re_path

from .consumers.clean_status import CleanStatusConsumer

websocket_urlpatterns = [
    re_path(r'ws/clean_status$', CleanStatusConsumer),
]
