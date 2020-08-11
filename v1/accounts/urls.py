from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views.account import AccountViewSet

router = SimpleRouter(trailing_slash=False)
router.register('accounts', AccountViewSet)
