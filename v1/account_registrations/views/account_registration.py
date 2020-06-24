from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from v1.account_registrations.models.account_registration import AccountRegistration
from v1.account_registrations.serializers.account_registration import (
    AccountRegistrationSerializer,
    AccountRegistrationSerializerCreate
)


# account_registrations
class AccountRegistrationView(APIView):

    @staticmethod
    def get(request):
        """
        description: List account registrations
        """

        account_registrations = AccountRegistration.objects.all()
        return Response(AccountRegistrationSerializer(account_registrations, many=True).data)

    @staticmethod
    def post(request):
        """
        description: Register as a bank account
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

        serializer = AccountRegistrationSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            account_registration = serializer.save()
            return Response(
                AccountRegistrationSerializer(account_registration).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
