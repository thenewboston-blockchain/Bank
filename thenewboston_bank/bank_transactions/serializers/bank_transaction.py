from rest_framework import serializers
from thenewboston.utils.fields import all_field_names

from thenewboston_bank.blocks.serializers.block import BlockSerializer
from ..models.bank_transaction import BankTransaction


class BankTransactionSerializer(serializers.ModelSerializer):
    block = BlockSerializer(read_only=True)

    class Meta:
        model = BankTransaction
        fields = '__all__'
        read_only_fields = all_field_names(BankTransaction)
