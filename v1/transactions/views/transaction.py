from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.transaction import Transaction
from ..serializers.transaction import TransactionSerializer


# transactions
class TransactionView(APIView):

    @staticmethod
    def get(request):
        """
        description: List transactions
        """

        transactions = Transaction.objects.all()
        return Response(TransactionSerializer(transactions, many=True).data)
