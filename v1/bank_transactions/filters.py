from django_filters import rest_framework as filters

from .models.bank_transaction import BankTransaction


class BankTransactionFilter(filters.FilterSet):
    class Meta:
        model = BankTransaction
        fields = (
            'block__sender',
            'recipient',
        )
