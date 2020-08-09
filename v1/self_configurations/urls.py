from rest_framework.routers import DefaultRouter

from .views.self_configuration import SelfConfigurationViewSet

app_name = 'self_configurations'

router = DefaultRouter(trailing_slash=False)
router.register('config', SelfConfigurationViewSet, basename='config')

urlpatterns = router.urls
