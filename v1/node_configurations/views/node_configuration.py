from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.node_configuration import NodeConfiguration
from ..serializers.node_configuration import NodeConfigurationSerializer


# node_configuration
class NodeConfigurationDetail(APIView):

    @staticmethod
    def get(request):
        """
        description: Get node configuration details
        """

        node_configuration = NodeConfiguration.objects.first()
        return Response(NodeConfigurationSerializer(node_configuration).data)
