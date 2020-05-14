from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.member_registration import MemberRegistration
from ..serializers.member_registration import MemberRegistrationSerializer


# member_registrations
class MemberRegistrationView(APIView):

    @staticmethod
    def get(request):
        """
        description: List member registrations
        """

        member_registrations = MemberRegistration.objects.all()
        return Response(MemberRegistrationSerializer(member_registrations, many=True).data)
