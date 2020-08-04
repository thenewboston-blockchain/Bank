from rest_framework.routers import DefaultRouter

from .views.confirmation_block import ConfirmationBlockViewSet

app_name = 'confirmation_blocks'

router = DefaultRouter(trailing_slash=False)
router.register('confirmation_blocks', ConfirmationBlockViewSet)

urlpatterns = router.urls
