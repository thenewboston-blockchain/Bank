from django.db.models import Q
from django_filters.rest_framework import CharFilter, FilterSet

from ..models.bank_transaction import BankTransaction


class BankTransactionFilter(FilterSet):
    account_number = CharFilter(method='filter_account_number')
    fee = CharFilter(method='filter_fee')

    class Meta:
        model = BankTransaction
        fields = [
            'account_number',
            'block__sender',
            'fee',
            'recipient',
        ]

    @staticmethod
    def filter_account_number(queryset, _, value):
        """Filter queryset by account number"""
        return queryset.filter(
            Q(block__sender=value)
            | Q(recipient=value)
        )

    @staticmethod
    def filter_fee(queryset, _, value):
        """Filter queryset by fee"""
        if value == 'NONE':
            return queryset.filter(
                fee__exact='',
            )

        return queryset.filter(
            fee__exact=value,
        )
