from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet

from thenewboston_bank.decorators.nodes import is_signed_message
from ..serializers.upgrade_notice import UpgradeNoticeSerializer


class UpgradeNoticeViewSet(ViewSet):
    """
    Upgrade notice

    ---
    create:
      description: Notice from a previous confirmation validator that they are now a primary validator
    """

    serializer_class = UpgradeNoticeSerializer

    @is_signed_message
    def create(self, request):
        serializer = self.serializer_class(
            data={
                **request.data['message'],
                'node_identifier': request.data['node_identifier']
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({}, status=HTTP_200_OK)
