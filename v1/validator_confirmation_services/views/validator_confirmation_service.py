from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from v1.decorators.nodes import is_signed_message
from ..models.validator_confirmation_service import ValidatorConfirmationService
from ..serializers.validator_confirmation_service import (
    ValidatorConfirmationServiceSerializer,
    ValidatorConfirmationServiceSerializerCreate
)


# validator_confirmation_services
class ValidatorConfirmationServiceView(APIView):

    @staticmethod
    def get(request):
        """
        description: List validator confirmation services
        """

        validator_confirmation_services = ValidatorConfirmationService.objects.all()
        return Response(ValidatorConfirmationServiceSerializer(validator_confirmation_services, many=True).data)

    @staticmethod
    @is_signed_message
    def post(request):
        """
        description: Create validator confirmation service
        """

        serializer = ValidatorConfirmationServiceSerializerCreate(
            data={
                **request.data['message'],
                'node_identifier': request.data['node_identifier']
            },
            context={'request': request}
        )
        if serializer.is_valid():
            validator_confirmation_service = serializer.save()
            return Response(
                ValidatorConfirmationServiceSerializer(validator_confirmation_service).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
