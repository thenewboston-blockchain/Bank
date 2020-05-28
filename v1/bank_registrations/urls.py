from django.urls import path

from .views.bank_registration import BankRegistrationDetail, BankRegistrationView

urlpatterns = [

    # Bank registrations
    path('bank_registrations', BankRegistrationView.as_view()),
    path('bank_registrations/<int:bank_registration_id>', BankRegistrationDetail.as_view()),

]
