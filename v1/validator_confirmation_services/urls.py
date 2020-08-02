from rest_framework.routers import DefaultRouter

from .views.validator_confirmation_service import ValidatorConfirmationServiceViewSet

app_name = 'validator_confirmation_services'

router = DefaultRouter(trailing_slash=False)
router.register('validator_confirmation_services', ValidatorConfirmationServiceViewSet)

urlpatterns = router.urls
