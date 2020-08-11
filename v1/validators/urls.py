from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views.validator import ValidatorViewSet

router = SimpleRouter(trailing_slash=False)
router.register('validators', ValidatorViewSet)
