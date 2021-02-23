from rest_framework.routers import SimpleRouter

from .views.invalid_block import InvalidBlockViewSet

router = SimpleRouter(trailing_slash=False)
router.register('invalid_blocks', InvalidBlockViewSet)
