from rest_framework import serializers
from thenewboston.utils.fields import all_field_names

from ..models.self_transaction_fee_tier import SelfTransactionFeeTier


class SelfTransactionFeeTierSerializer(serializers.ModelSerializer):

    class Meta:
        model = SelfTransactionFeeTier
        fields = '__all__'
        read_only_fields = all_field_names(SelfTransactionFeeTier)
