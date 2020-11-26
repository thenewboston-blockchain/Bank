from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from ..models.block import Block
from ..serializers.block import BlockSerializer, BlockSerializerCreate


class BlockViewSet(
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """
    Blocks

    ---
    list:
      description: List blocks
    create:
      description: Create block
      parameters:
        - name: account_number
          required: true
          type: string
        - name: message
          required: true
          type: object
          properties:
            balance_key:
              required: true
              type: string
            txs:
              required: true
              type: array
              items:
                type: object
                properties:
                  amount:
                    required: true
                    type: number
                  recipient:
                    required: true
                    type: string
        - name: signature
          required: true
          type: string
    """

    filterset_fields = ('sender',)
    ordering_fields = '__all__'
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    serializer_create_class = BlockSerializerCreate

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_create_class(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        block = serializer.save()

        return Response(
            self.get_serializer(block).data,
            status=HTTP_201_CREATED,
        )
