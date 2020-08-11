from rest_framework.routers import SimpleRouter

from .views.validator_confirmation_service import ValidatorConfirmationServiceViewSet

router = SimpleRouter(trailing_slash=False)
router.register('validator_confirmation_services', ValidatorConfirmationServiceViewSet)
