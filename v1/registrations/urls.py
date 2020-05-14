from django.urls import path

from .views.member_registration import MemberRegistrationView
from .views.validator_registration import ValidatorRegistrationView

urlpatterns = [

    # Member registrations
    path('member_registrations', MemberRegistrationView.as_view()),

    # Validator registrations
    path('validator_registrations', ValidatorRegistrationView.as_view()),

]
