from rest_framework.routers import DefaultRouter

from .views.account import AccountViewSet

app_name = 'accounts'

router = DefaultRouter(trailing_slash=False)
router.register('accounts', AccountViewSet)

urlpatterns = router.urls
