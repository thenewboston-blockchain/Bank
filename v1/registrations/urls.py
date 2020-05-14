from django.urls import path

from .views.validator_registration import ValidatorRegistrationView

urlpatterns = [

    # Validator registrations
    path('validator_registrations', ValidatorRegistrationView.as_view()),

]
