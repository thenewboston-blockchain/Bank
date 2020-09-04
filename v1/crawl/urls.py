from rest_framework.routers import SimpleRouter

from .views.crawl import CrawlViewSet

router = SimpleRouter(trailing_slash=False)
router.register('crawl', CrawlViewSet, basename='crawl')
