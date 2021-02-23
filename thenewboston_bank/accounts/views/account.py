from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from thenewboston_bank.decorators.nodes import is_self_signed_message
from ..models.account import Account
from ..serializers.account import AccountSerializer, AccountSerializerUpdate


class AccountViewSet(
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    """
    Accounts

    ---
    list:
      description: List accounts
    update:
      description: Update account
      parameters:
        - name: trust
          type: number
    """

    lookup_field = 'account_number'
    ordering_fields = '__all__'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    serializer_update_class = AccountSerializerUpdate

    @is_self_signed_message
    def update(self, request, *args, **kwargs):

        serializer = self.serializer_update_class(
            self.get_object(),
            data=request.data['message'],
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            self.get_serializer(serializer.save()).data
        )
