from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.validator_transaction_fee_tier import ValidatorTransactionFeeTier
from ..serializers.validator_transaction_fee_tier import ValidatorTransactionFeeTierSerializer


# validator_transaction_fee_tiers
class ValidatorTransactionFeeTierView(APIView):

    @staticmethod
    def get(request):
        """
        description: List validator transaction fee tiers
        """

        validator_transaction_fee_tiers = ValidatorTransactionFeeTier.objects.all()
        return Response(ValidatorTransactionFeeTierSerializer(validator_transaction_fee_tiers, many=True).data)
