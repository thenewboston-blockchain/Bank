from rest_framework import serializers

from v1.utils.serializers import all_field_names
from ..models.transaction_fee_tier import TransactionFeeTier


class TransactionFeeTierSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionFeeTier
        fields = all_field_names(TransactionFeeTier)
