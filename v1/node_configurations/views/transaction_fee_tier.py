from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.transaction_fee_tier import TransactionFeeTier
from ..serializers.transaction_fee_tier import TransactionFeeTierSerializer


# transaction_fee_tiers
class TransactionFeeTierView(APIView):

    @staticmethod
    def get(request):
        """
        description: List transaction fee tiers
        """

        transaction_fee_tiers = TransactionFeeTier.objects.all()
        return Response(TransactionFeeTierSerializer(transaction_fee_tiers, many=True).data)
