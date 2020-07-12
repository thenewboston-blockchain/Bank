from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from v1.decorators.nodes import is_signed_message
from ..models.confirmation_block import ConfirmationBlock
from ..serializers.confirmation_block import ConfirmationBlockSerializer, ConfirmationBlockSerializerCreate


# confirmation_blocks
class ConfirmationBlockView(APIView):

    @staticmethod
    def get(request):
        """
        description: List confirmation blocks
        """

        confirmation_blocks = ConfirmationBlock.objects.all()
        return Response(ConfirmationBlockSerializer(confirmation_blocks, many=True).data)

    @staticmethod
    @is_signed_message
    def post(request):
        """
        description: Create confirmation block
        """

        serializer = ConfirmationBlockSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            confirmation_block = serializer.save()
            return Response(
                ConfirmationBlockSerializer(confirmation_block).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
