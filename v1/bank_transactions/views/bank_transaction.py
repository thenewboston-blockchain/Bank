from rest_framework.response import Response
from rest_framework import (
    mixins,
    viewsets,
)

from django_filters.rest_framework import DjangoFilterBackend

from ..filters import BankTransactionFilter
from ..helpers.optimizations import optimize_bank_transaction_list
from ..models.bank_transaction import BankTransaction
from ..serializers.bank_transaction import BankTransactionSerializer


# bank_transactions
class BankTransactionView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = BankTransaction.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = BankTransactionFilter
    serializer_class = BankTransactionSerializer

    def get_queryset(self):
        """
        description: Queryset to list bank transactions
        """
        bank_transactions = optimize_bank_transaction_list(self.queryset)
        return bank_transactions
