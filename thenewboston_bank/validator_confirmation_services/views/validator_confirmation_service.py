from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from thenewboston_bank.decorators.nodes import is_signed_message
from ..models.validator_confirmation_service import ValidatorConfirmationService
from ..serializers.validator_confirmation_service import (
    ValidatorConfirmationServiceSerializer,
    ValidatorConfirmationServiceSerializerCreate
)
from ...notifications.validation_confirmation import send_validator_confirmation_service_notification


class ValidatorConfirmationServiceViewSet(
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """
    Validator confirmation services

    ---
    list:
      description: List validator confirmation services
    create:
      description: Create validator confirmation service
    """

    filterset_fields = ('validator__node_identifier',)
    ordering_fields = '__all__'
    queryset = ValidatorConfirmationService.objects.all()
    serializer_class = ValidatorConfirmationServiceSerializer
    serializer_create_class = ValidatorConfirmationServiceSerializerCreate

    @is_signed_message
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_create_class(
            data={
                **request.data['message'],
                'node_identifier': request.data['node_identifier']
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        validator_confirmation_service = serializer.save()

        serialized_data = self.get_serializer(validator_confirmation_service).data
        serialized_data_fixed = serialized_data.copy()

        # DRF doesn't serialize UUIDs, JSONRenderer in Response does that
        serialized_data_fixed['validator'] = str(serialized_data_fixed['validator'])

        send_validator_confirmation_service_notification(payload={
            'bank_node_identifier': request.data['node_identifier'],
            'validator_confirmation_service': serialized_data_fixed
        })

        return Response(
            serialized_data,
            status=HTTP_201_CREATED
        )
