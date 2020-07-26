from rest_framework.routers import DefaultRouter

from v1.bank_transactions.views.bank_transaction import BankTransactionViewSet

app_name = 'bank_transactions'

router = DefaultRouter()
router.register('bank_transactions', BankTransactionViewSet)

urlpatterns = router.urls
