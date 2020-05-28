from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from v1.member_registrations.models.member_registration import MemberRegistration
from v1.member_registrations.serializers.member_registration import MemberRegistrationSerializer, MemberRegistrationSerializerCreate


# member_registrations
class MemberRegistrationView(APIView):

    @staticmethod
    def get(request):
        """
        description: List member registrations
        """

        member_registrations = MemberRegistration.objects.all()
        return Response(MemberRegistrationSerializer(member_registrations, many=True).data)

    @staticmethod
    def post(request):
        """
        description: Register as a bank member
        parameters:
          - name: account_number
            required: true
            type: string
          - name: balance_lock
            required: true
            type: string
          - name: signature
            required: true
            type: string
          - name: txs
            required: true
            type: array
            items:
              type: object
              properties:
                amount:
                  required: true
                  type: integer
                balance_key:
                  required: true
                  type: string
                recipient:
                  required: true
                  type: string
        """

        serializer = MemberRegistrationSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            member_registration = serializer.save()
            return Response(
                MemberRegistrationSerializer(member_registration).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
