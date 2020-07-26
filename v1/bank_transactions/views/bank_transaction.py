from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from v1.thirdparty.rest_framework.pagination import LimitOffsetPagination
from ..filters.bank_transaction import BankTransactionFilter
from ..helpers.optimizations import optimize_bank_transaction_list
from ..models.bank_transaction import BankTransaction
from ..serializers.bank_transaction import BankTransactionSerializer


class BankTransactionViewSet(
    ListModelMixin,
    GenericViewSet,
):
    """
    List bank transactions
    """
    serializer_class = BankTransactionSerializer
    filterset_class = BankTransactionFilter

    queryset = optimize_bank_transaction_list(
        BankTransaction.objects.all(),
    )
    pagination_class = LimitOffsetPagination
