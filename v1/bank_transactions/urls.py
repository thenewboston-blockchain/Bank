from django.urls import path

from v1.bank_transactions.views.bank_transaction import BankTransactionView

urlpatterns = [

    # Bank transactions
    path('bank_transactions', BankTransactionView.as_view()),

]
