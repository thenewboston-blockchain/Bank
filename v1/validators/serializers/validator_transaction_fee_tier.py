from rest_framework import serializers
from thenewboston.utils.fields import all_field_names

from ..models.validator_transaction_fee_tier import ValidatorTransactionFeeTier


class ValidatorTransactionFeeTierSerializer(serializers.ModelSerializer):

    class Meta:
        model = ValidatorTransactionFeeTier
        fields = '__all__'
        read_only_fields = all_field_names(ValidatorTransactionFeeTier)
