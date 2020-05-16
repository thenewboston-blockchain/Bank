from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.self_transaction_fee_tier import SelfTransactionFeeTier
from ..serializers.self_transaction_fee_tier import SelfTransactionFeeTierSerializer


# self_transaction_fee_tiers
class SelfTransactionFeeTierView(APIView):

    @staticmethod
    def get(request):
        """
        description: List self transaction fee tiers
        """

        self_transaction_fee_tiers = SelfTransactionFeeTier.objects.all()
        return Response(SelfTransactionFeeTierSerializer(self_transaction_fee_tiers, many=True).data)
