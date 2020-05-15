from rest_framework import serializers

from ..models.transaction_fee_tier import TransactionFeeTier


class TransactionFeeTierSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionFeeTier
        fields = '__all__'
