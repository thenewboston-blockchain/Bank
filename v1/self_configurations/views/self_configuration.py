from rest_framework.response import Response
from rest_framework.views import APIView

from ..helpers.self_configuration import get_self_configuration
from ..serializers.self_configuration import SelfConfigurationSerializer


# self_configuration
class SelfConfigurationDetail(APIView):

    @staticmethod
    def get(request):
        """
        description: Get self configuration details
        """

        self_configuration = get_self_configuration()
        return Response(SelfConfigurationSerializer(self_configuration).data)
