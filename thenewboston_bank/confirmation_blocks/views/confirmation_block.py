from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from thenewboston_bank.decorators.nodes import is_signed_message
from ..models.confirmation_block import ConfirmationBlock
from ..serializers.confirmation_block import ConfirmationBlockSerializer, ConfirmationBlockSerializerCreate


class ConfirmationBlockViewSet(
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """
    Confirmation blocks

    ---
    list: description: List confirmation blocks
    create: description: Create confirmation block
    """

    ordering_fields = '__all__'
    queryset = ConfirmationBlock.objects.all()
    serializer_class = ConfirmationBlockSerializer
    serializer_create_class = ConfirmationBlockSerializerCreate

    @is_signed_message
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_create_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        confirmation_block = serializer.save()

        return Response(
            self.get_serializer(confirmation_block).data,
            status=HTTP_201_CREATED
        )
