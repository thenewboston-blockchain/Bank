from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from v1.decorators.nodes import is_self_signed_message
from ..models.account import Account
from ..serializers.account import AccountSerializer, AccountSerializerUpdate


# accounts
class AccountView(APIView):

    @staticmethod
    def get(request):
        """
        description: List accounts
        """

        accounts = Account.objects.all()
        return Response(AccountSerializer(accounts, many=True).data)


# accounts/{account_number}
class AccountDetail(APIView):

    @staticmethod
    @is_self_signed_message
    def patch(request, account_number):
        """
        description: Update account
        parameters:
          - name: trust
            type: number
        """

        account = get_object_or_404(Account, account_number=account_number)
        serializer = AccountSerializerUpdate(
            account,
            data=request.data['message'],
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(AccountSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
