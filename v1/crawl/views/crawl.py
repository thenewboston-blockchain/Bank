from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet

from v1.decorators.nodes import is_self_signed_message
from ..serializers.crawl import CrawlSerializer


class CrawlViewSet(ViewSet):
    serializer_class = CrawlSerializer

    @is_self_signed_message
    def create(self, request):
        serializer = self.serializer_class(
            data={
                **request.data['message']
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        crawl = serializer.save()

        return Response(crawl, status=HTTP_200_OK)
