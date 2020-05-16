from rest_framework.response import Response
from rest_framework.views import APIView

from ..helpers.node_configuration import get_node_configuration
from ..serializers.node_configuration import NodeConfigurationSerializer


# node_configuration
class NodeConfigurationDetail(APIView):

    @staticmethod
    def get(request):
        """
        description: Get node configuration details
        """

        node_configuration = get_node_configuration()
        return Response(NodeConfigurationSerializer(node_configuration).data)
