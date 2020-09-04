from django.core.cache import cache
from django.utils.decorators import classonlymethod
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet

from v1.cache_tools.cache_keys import CRAWL_LAST_COMPLETED, CRAWL_STATUS
from v1.decorators.nodes import is_self_signed_message
from ..serializers.crawl import CrawlSerializer


class CrawlViewSet(ViewSet):
    serializer_class = CrawlSerializer

    @classonlymethod
    def as_view(cls, actions=None, **kwargs):
        return super().as_view(
            actions={
                'get': 'crawl_status',
                'post': 'create'
            },
            **kwargs
        )

    @staticmethod
    def crawl_status(request):
        return Response(
            {
                'crawl_last_completed': cache.get(CRAWL_LAST_COMPLETED),
                'crawl_status': cache.get(CRAWL_STATUS)
            },
            status=HTTP_200_OK
        )

    @is_self_signed_message
    def create(self, request):
        serializer = self.serializer_class(
            data={
                **request.data['message']
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        crawl_status = serializer.save()

        return Response(
            {'crawl_status': crawl_status},
            status=HTTP_200_OK
        )
