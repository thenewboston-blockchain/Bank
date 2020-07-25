from django_filters.rest_framework import FilterSet, CharFilter
from django.db.models import Q

from ..models.bank_transaction import BankTransaction


class BankTransactionFilter(FilterSet):

    account_number = CharFilter(
        method='filter_account_number'
    )

    class Meta:
        model = BankTransaction
        fields = [
            'recipient',
            'block__sender',
            'account_number',
        ]

    def filter_account_number(self, queryset, name, value):

        return queryset.filter(
            Q(block__sender=value) | Q(recipient=value)
        )
