from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from v1.third_party.rest_framework.pagination import LimitOffsetPagination
from ..filters.bank_transaction import BankTransactionFilter
from ..helpers.optimizations import optimize_bank_transaction_list
from ..models.bank_transaction import BankTransaction
from ..serializers.bank_transaction import BankTransactionSerializer


# bank_transactions
class BankTransactionViewSet(
    ListModelMixin,
    GenericViewSet,
):
    """
    Bank transactions
    ---
    list:
      description: List bank transactions
    """

    filterset_class = BankTransactionFilter
    pagination_class = LimitOffsetPagination
    queryset = optimize_bank_transaction_list(
        BankTransaction.objects.all(),
    )
    serializer_class = BankTransactionSerializer
