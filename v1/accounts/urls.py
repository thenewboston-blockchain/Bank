from rest_framework.routers import SimpleRouter

from .views.account import AccountViewSet

router = SimpleRouter(trailing_slash=False)
router.register('accounts', AccountViewSet)
