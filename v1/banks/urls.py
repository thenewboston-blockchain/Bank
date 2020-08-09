from rest_framework.routers import DefaultRouter

from .views.bank import BankViewSet

app_name = 'banks'

router = DefaultRouter(trailing_slash=False)
router.register('banks', BankViewSet)

urlpatterns = router.urls
