from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.validator import Validator
from ..serializers.validator import ValidatorSerializer


# validators
class ValidatorView(APIView):

    @staticmethod
    def get(request):
        """
        description: List validators
        """

        validators = Validator.objects.all()
        return Response(ValidatorSerializer(validators, many=True).data)
