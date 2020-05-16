from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.bank_transaction import BankTransaction
from ..serializers.bank_transaction import BankTransactionSerializer


# bank_transactions
class BankTransactionView(APIView):

    @staticmethod
    def get(request):
        """
        description: List bank transactions
        """

        bank_transactions = BankTransaction.objects.all()
        return Response(BankTransactionSerializer(bank_transactions, many=True).data)
