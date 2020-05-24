from rest_framework import serializers
from thenewboston.utils.fields import all_field_names

from ..models.bank import Bank


class BankSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Bank
        read_only_fields = all_field_names(Bank)
