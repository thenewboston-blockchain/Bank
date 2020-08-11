from rest_framework.routers import SimpleRouter

from .views.confirmation_block import ConfirmationBlockViewSet

router = SimpleRouter(trailing_slash=False)
router.register('confirmation_blocks', ConfirmationBlockViewSet)
