from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views.block import BlockViewSet

router = SimpleRouter(trailing_slash=False)
router.register('blocks', BlockViewSet)
