from django.urls import path

from .views.transaction import TransactionView

urlpatterns = [

    # Transactions
    path('transactions', TransactionView.as_view()),

]
