from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from thenewboston.constants.errors import ERROR

from v1.decorators.nodes import is_signed_message
from ..serializers.connection_request import ConnectionRequestSerializerCreate


# connection_requests
class ConnectionRequestView(APIView):

    @staticmethod
    @is_signed_message
    def post(request):
        """
        description: Create connection request
        """

        message = request.data['message']

        if request.data['node_identifier'] != message.get('node_identifier'):
            return Response(
                {ERROR: 'Signing node_identifier must match message node_identifier'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ConnectionRequestSerializerCreate(
            data=message,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
