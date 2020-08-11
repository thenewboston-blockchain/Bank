from rest_framework.routers import SimpleRouter

from .views.block import BlockViewSet

router = SimpleRouter(trailing_slash=False)
router.register('blocks', BlockViewSet)
