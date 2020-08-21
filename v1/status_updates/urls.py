from rest_framework.routers import SimpleRouter

from .views.upgrade_notice import UpgradeNoticeViewSet

router = SimpleRouter(trailing_slash=False)
router.register('upgrade_notice', UpgradeNoticeViewSet, basename='upgrade_notice')
