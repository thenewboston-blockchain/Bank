from django.urls import include, path

from rest_framework.routers import DefaultRouter

from v1.bank_transactions.views.bank_transaction import BankTransactionView


app_name = 'bank_transactions'

router = DefaultRouter()
router.register('bank_transactions', BankTransactionView)

urlpatterns = [
    path('', include(router.urls)),
]
