from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from v1.blocks.models.block import Block
from v1.blocks.serializers.block import BlockSerializer, BlockSerializerCreate


# blocks
class BlockView(APIView):

    @staticmethod
    def get(request):
        """
        description: List blocks
        """

        blocks = Block.objects.all()
        return Response(BlockSerializer(blocks, many=True).data)

    @staticmethod
    def post(request):
        """
        description: Create block
        parameters:
          - name: account_number
            required: true
            type: string
          - name: signature
            required: true
            type: string
          - name: txs
            required: true
            type: array
            items:
              type: object
              properties:
                amount:
                  required: true
                  type: number
                balance_key:
                  required: true
                  type: string
                recipient:
                  required: true
                  type: string
        """

        serializer = BlockSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            block = serializer.save()
            return Response(
                BlockSerializer(block).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
