from django.urls import path

from .views.account_registration import AccountRegistrationView

urlpatterns = [

    # Account registrations
    path('account_registrations', AccountRegistrationView.as_view()),

]
