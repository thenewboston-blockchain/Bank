from django.utils.decorators import classonlymethod
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet

from thenewboston_bank.decorators.nodes import is_self_signed_message
from ..helpers import get_crawl_info
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
            get_crawl_info(),
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
        serializer.save()

        return Response(
            get_crawl_info(),
            status=HTTP_200_OK
        )
