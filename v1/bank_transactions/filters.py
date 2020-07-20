from django_filters import rest_framework as filters
from django.db.models import Q

from .models.bank_transaction import BankTransaction


class AccountNumberFilter(filters.CharFilter):

    def filter(self, qs, value):
        queryset = None
        if value in EMPTY_VALUES:
            return qs

        kwargs = {
        }
        queryset = qs.filter(**kwargs)

        return queryset


class BankTransactionFilter(filters.FilterSet):

    account_number = filters.CharFilter(
        method='filter_account_number'
    )

    class Meta:
        model = BankTransaction
        fields = (
            'block__sender',
            'recipient',
            'account_number',
        )

    def filter_account_number(self, queryset, name, value):
        return queryset.filter(
            Q(block__sender=value) | Q(recipient=value)
        )
