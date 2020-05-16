from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.bank_registration import BankRegistration
from ..serializers.bank_registration import BankRegistrationSerializer


# bank_registrations
class BankRegistrationView(APIView):

    @staticmethod
    def get(request):
        """
        description: List bank registrations
        """

        bank_registrations = BankRegistration.objects.all()
        return Response(BankRegistrationSerializer(bank_registrations, many=True).data)
