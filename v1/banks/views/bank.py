from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from v1.decorators.nodes import is_self_signed_message
from ..models.bank import Bank
from ..serializers.bank import BankSerializer, BankSerializerUpdate


# banks
class BankView(APIView):

    @staticmethod
    def get(request):
        """
        description: List banks
        """

        banks = Bank.objects.all()
        return Response(BankSerializer(banks, many=True).data)


# banks/{node_identifier}
class BankDetail(APIView):

    @staticmethod
    @is_self_signed_message
    def patch(request, node_identifier):
        """
        description: Update bank
        parameters:
          - name: trust
            type: number
        """

        bank = get_object_or_404(Bank, node_identifier=node_identifier)
        serializer = BankSerializerUpdate(
            bank,
            data=request.data['message'],
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(BankSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
