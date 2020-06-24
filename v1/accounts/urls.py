from django.urls import path

from .views.account import AccountView

urlpatterns = [

    # Accounts
    path('accounts', AccountView.as_view()),

]
