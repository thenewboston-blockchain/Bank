from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from v1.decorators.nodes import is_self_signed_message
from ..models.validator import Validator
from ..serializers.validator import ValidatorSerializer, ValidatorSerializerUpdate


# validators
class ValidatorView(APIView):

    @staticmethod
    def get(request):
        """
        description: List validators
        """

        validators = Validator.objects.all()
        return Response(ValidatorSerializer(validators, many=True).data)


# validators/{node_identifier}
class ValidatorDetail(APIView):

    @staticmethod
    @is_self_signed_message
    def patch(request, node_identifier):
        """
        description: Update validator
        parameters:
          - name: trust
            type: number
        """

        validator = get_object_or_404(Validator, node_identifier=node_identifier)
        serializer = ValidatorSerializerUpdate(
            validator,
            data=request.data['message'],
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(ValidatorSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
