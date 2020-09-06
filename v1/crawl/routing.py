from django.urls import re_path

from .consumers.crawl_status import CrawlStatusConsumer

websocket_urlpatterns = [
    re_path(r'ws/crawl_status$', CrawlStatusConsumer),
]
