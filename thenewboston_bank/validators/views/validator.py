from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from thenewboston_bank.decorators.nodes import is_self_signed_message
from ..models.validator import Validator
from ..serializers.validator import ValidatorSerializer, ValidatorSerializerCreate, ValidatorSerializerUpdate


class ValidatorViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    """
    Validators

    ---
    list:
      description: List validators
    update:
      description: Update validator
      parameters:
        - name: trust
          type: number
    """

    lookup_field = 'node_identifier'
    ordering_fields = '__all__'
    queryset = Validator.objects.all()
    serializer_class = ValidatorSerializer
    serializer_create_class = ValidatorSerializerCreate
    serializer_update_class = ValidatorSerializerUpdate

    @is_self_signed_message
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_create_class(
            data=request.data['message'],
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        validator = serializer.save()

        return Response(
            self.get_serializer(validator).data
        )

    @is_self_signed_message
    def update(self, request, *args, **kwargs):
        serializer = self.serializer_update_class(
            self.get_object(),
            data=request.data['message'],
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        validator = serializer.save()

        return Response(
            self.get_serializer(validator).data
        )
