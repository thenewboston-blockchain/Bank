from django.urls import path

from .views.validator_confirmation_service import ValidatorConfirmationServiceView

urlpatterns = [

    # Validator confirmation services
    path('validator_confirmation_services', ValidatorConfirmationServiceView.as_view()),

]
