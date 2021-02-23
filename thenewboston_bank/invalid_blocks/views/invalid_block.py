from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from thenewboston_bank.decorators.nodes import is_signed_message
from ..models.invalid_block import InvalidBlock
from ..serializers.invalid_block import InvalidBlockSerializer, InvalidBlockSerializerCreate


class InvalidBlockViewSet(
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """
    Invalid blocks

    ---
    list:
      description: List invalid blocks
    create:
      description: Create invalid block
    """

    ordering_fields = '__all__'
    queryset = InvalidBlock.objects.all()
    serializer_class = InvalidBlockSerializer
    serializer_create_class = InvalidBlockSerializerCreate

    @is_signed_message
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_create_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        invalid_block = serializer.save()

        return Response(
            self.get_serializer(invalid_block).data,
            status=HTTP_201_CREATED
        )
