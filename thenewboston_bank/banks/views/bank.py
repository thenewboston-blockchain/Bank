from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from thenewboston_bank.decorators.nodes import is_self_signed_message
from ..models.bank import Bank
from ..serializers.bank import BankSerializer, BankSerializerCreate, BankSerializerUpdate


class BankViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    """
    Banks

    ---
    list:
      description: List banks
    update:
      description: Update bank
      parameters:
        - name: trust
          type: number
    create:
      description: Create bank
    """

    lookup_field = 'node_identifier'
    ordering_fields = '__all__'
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    serializer_create_class = BankSerializerCreate
    serializer_update_class = BankSerializerUpdate

    @is_self_signed_message
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_create_class(
            data=request.data['message'],
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        bank = serializer.save()

        return Response(
            self.get_serializer(bank).data,
            status=status.HTTP_201_CREATED
        )

    @is_self_signed_message
    def update(self, request, *args, **kwargs):
        serializer = self.serializer_update_class(
            self.get_object(),
            data=request.data['message'],
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        bank = serializer.save()

        return Response(
            self.get_serializer(bank).data
        )
