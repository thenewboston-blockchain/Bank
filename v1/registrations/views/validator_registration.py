from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.validator_registration import ValidatorRegistration
from ..serializers.validator_registration import ValidatorRegistrationSerializer


# validator_registrations
class ValidatorRegistrationView(APIView):

    @staticmethod
    def get(request):
        """
        description: List validator registrations
        """

        validator_registrations = ValidatorRegistration.objects.all()
        return Response(ValidatorRegistrationSerializer(validator_registrations, many=True).data)
