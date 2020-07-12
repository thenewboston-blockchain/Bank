from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.account import Account
from ..serializers.account import AccountSerializer


# accounts
class AccountView(APIView):

    @staticmethod
    def get(request):
        """
        description: List accounts
        """

        accounts = Account.objects.all()
        return Response(AccountSerializer(accounts, many=True).data)
