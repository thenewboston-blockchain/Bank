from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ViewSet

from thenewboston_bank.decorators.nodes import is_signed_message
from ..serializers.connection_request import ConnectionRequestSerializerCreate


class ConnectionRequestViewSet(ViewSet):
    """
    Connection requests

    ---
    create:
      description: Create connection request
    """

    serializer_class = ConnectionRequestSerializerCreate

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

        return Response({}, status=HTTP_201_CREATED)
