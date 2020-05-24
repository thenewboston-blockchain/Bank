from django.urls import path

from .views.bank_registration import BankRegistrationDetail, BankRegistrationView
from .views.member_registration import MemberRegistrationView

urlpatterns = [

    # Bank registrations
    path('bank_registrations', BankRegistrationView.as_view()),
    path('bank_registrations/<int:bank_registration_id>', BankRegistrationDetail.as_view()),

    # Member registrations
    path('member_registrations', MemberRegistrationView.as_view()),

]
