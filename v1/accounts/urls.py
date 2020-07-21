from django.urls import path

from .views.account import AccountDetail, AccountView

urlpatterns = [

    # Accounts
    path('accounts', AccountView.as_view()),
    path('accounts/<str:account_number>', AccountDetail.as_view()),

]
