from rest_framework.routers import SimpleRouter

from .views.connection_request import ConnectionRequestViewSet

router = SimpleRouter(trailing_slash=False)
router.register('connection_requests', ConnectionRequestViewSet, basename='connection_requests')
