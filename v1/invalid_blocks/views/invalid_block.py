from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from v1.decorators.nodes import is_signed_message
from ..models.invalid_block import InvalidBlock
from ..serializers.invalid_block import InvalidBlockSerializer, InvalidBlockSerializerCreate


# invalid_blocks
class InvalidBlockView(APIView):

    @staticmethod
    def get(request):
        """
        description: List invalid blocks
        """

        invalid_blocks = InvalidBlock.objects.all()
        return Response(InvalidBlockSerializer(invalid_blocks, many=True).data)

    @staticmethod
    @is_signed_message
    def post(request):
        """
        description: Create invalid block
        """

        serializer = InvalidBlockSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            invalid_block = serializer.save()
            return Response(
                InvalidBlockSerializer(invalid_block).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
