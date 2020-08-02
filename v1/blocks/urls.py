from rest_framework.routers import DefaultRouter

from .views.block import BlockViewSet

app_name = 'blocks'

router = DefaultRouter(trailing_slash=False)
router.register('blocks', BlockViewSet)

urlpatterns = router.urls
