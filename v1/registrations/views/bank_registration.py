from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from v1.decorators.nodes import signed_by_primary_validator
from ..models.bank_registration import BankRegistration
from ..serializers.bank_registration import BankRegistrationSerializer, BankRegistrationSerializerUpdate


# bank_registrations
class BankRegistrationView(APIView):

    @staticmethod
    def get(request):
        """
        description: List bank registrations
        """

        bank_registrations = BankRegistration.objects.all()
        return Response(BankRegistrationSerializer(bank_registrations, many=True).data)


# bank_registrations/{bank_registration_id}
class BankRegistrationDetail(APIView):

    @staticmethod
    @signed_by_primary_validator
    def patch(request, bank_registration_id):
        """
        description: Update bank registration
        parameters:
          - name: status
            type: string
        """

        signed_data = request.data.get('signed_data')
        bank_registration = get_object_or_404(BankRegistration, pk=bank_registration_id)

        serializer = BankRegistrationSerializerUpdate(
            bank_registration,
            data=signed_data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(BankRegistrationSerializer(serializer.instance).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
