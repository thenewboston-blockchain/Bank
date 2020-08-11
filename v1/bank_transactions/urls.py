from rest_framework.routers import SimpleRouter

from .views.bank_transaction import BankTransactionViewSet

router = SimpleRouter(trailing_slash=False)
router.register('bank_transactions', BankTransactionViewSet)
