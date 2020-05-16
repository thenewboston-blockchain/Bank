from rest_framework import serializers

from v1.utils.serializers import all_field_names
from ..models.transaction import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = all_field_names(Transaction)
