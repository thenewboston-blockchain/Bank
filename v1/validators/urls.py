from rest_framework.routers import DefaultRouter

from .views.validator import ValidatorViewSet

app_name = 'validators'

router = DefaultRouter(trailing_slash=False)
router.register('validators', ValidatorViewSet)

urlpatterns = router.urls
