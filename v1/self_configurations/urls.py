from rest_framework.routers import SimpleRouter

from .views.self_configuration import SelfConfigurationViewSet

router = SimpleRouter(trailing_slash=False)
router.register('config', SelfConfigurationViewSet, basename='config')
