import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from ..helpers.self_configuration import get_self_configuration
from ..serializers.self_configuration import SelfConfigurationSerializer

logger = logging.getLogger('thenewboston')


# config
class SelfConfigurationDetail(APIView):

    @staticmethod
    def get(request):
        """
        description: Get self configuration details
        """

        try:
            x = 1 / 0
            print(x)
        except Exception as e:
            logger.exception(e)

        self_configuration = get_self_configuration(exception_class=RuntimeError)
        return Response(SelfConfigurationSerializer(self_configuration).data)
