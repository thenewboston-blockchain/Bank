from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.member import Member
from ..serializers.member import MemberSerializer


# members
class MemberView(APIView):

    @staticmethod
    def get(request):
        """
        description: List members
        """

        members = Member.objects.all()
        return Response(MemberSerializer(members, many=True).data)
