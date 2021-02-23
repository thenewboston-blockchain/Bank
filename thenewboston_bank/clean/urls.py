from rest_framework.routers import SimpleRouter

from .views.clean import CleanViewSet

router = SimpleRouter(trailing_slash=False)
router.register('clean', CleanViewSet, basename='clean')
