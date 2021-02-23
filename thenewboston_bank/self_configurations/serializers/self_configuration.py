from rest_framework import serializers
from thenewboston.utils.fields import all_field_names

from thenewboston_bank.validators.serializers.validator import ValidatorSerializer
from ..models.self_configuration import SelfConfiguration


class SelfConfigurationSerializer(serializers.ModelSerializer):
    primary_validator = ValidatorSerializer(read_only=True)

    class Meta:
        exclude = ('id',)
        model = SelfConfiguration
        read_only_fields = all_field_names(SelfConfiguration)
