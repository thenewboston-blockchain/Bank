from rest_framework.routers import DefaultRouter

from .views.invalid_block import InvalidBlockViewSet

app_name = 'invalid_blocks'

router = DefaultRouter(trailing_slash=False)
router.register('invalid_blocks', InvalidBlockViewSet)

urlpatterns = router.urls
