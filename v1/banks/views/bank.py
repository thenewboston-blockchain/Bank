from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.bank import Bank
from ..serializers.bank import BankSerializer


# banks
class BankView(APIView):

    @staticmethod
    def get(request):
        """
        description: List banks
        """

        banks = Bank.objects.all()
        return Response(BankSerializer(banks, many=True).data)
