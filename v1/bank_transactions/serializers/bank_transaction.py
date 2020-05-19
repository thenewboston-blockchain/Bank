from rest_framework import serializers

from thenewboston.utils.serializers import all_field_names
from ..models.bank_transaction import BankTransaction


class BankTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankTransaction
        fields = '__all__'
        read_only_fields = all_field_names(BankTransaction)
