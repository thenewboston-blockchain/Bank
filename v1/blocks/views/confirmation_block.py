from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.confirmation_block import ConfirmationBlock
from ..serializers.confirmation_block import ConfirmationBlockSerializer


# confirmation_blocks
class ConfirmationBlockView(APIView):

    @staticmethod
    def get(request):
        """
        description: List confirmation blocks
        """

        confirmation_blocks = ConfirmationBlock.objects.all()
        return Response(ConfirmationBlockSerializer(confirmation_blocks, many=True).data)
