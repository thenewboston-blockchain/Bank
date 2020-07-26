from rest_framework.routers import DefaultRouter

from .views.bank_transaction import BankTransactionViewSet

app_name = 'bank_transactions'

router = DefaultRouter(trailing_slash=False)
router.register('bank_transactions', BankTransactionViewSet)

urlpatterns = router.urls
