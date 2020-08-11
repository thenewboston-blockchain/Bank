from rest_framework.routers import SimpleRouter

from .views.bank import BankViewSet

router = SimpleRouter(trailing_slash=False)
router.register('banks', BankViewSet)
