from rest_framework import serializers

from v1.network.utils.serializers import all_field_names
from ..models.bank import Bank


class BankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = '__all__'
        read_only_fields = all_field_names(Bank)
