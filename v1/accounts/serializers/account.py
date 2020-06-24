from rest_framework import serializers
from thenewboston.utils.fields import all_field_names

from ..models.account import Account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = all_field_names(Account)
