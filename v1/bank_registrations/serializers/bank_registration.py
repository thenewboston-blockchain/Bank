from rest_framework import serializers
from thenewboston.utils.fields import all_field_names

from ..models.bank_registration import BankRegistration


class BankRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankRegistration
        fields = '__all__'
        read_only_fields = all_field_names(BankRegistration)


class BankRegistrationSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = BankRegistration
        fields = ('status',)
