from rest_framework import serializers

from v1.network.utils.serializers import all_field_names
from ..models.validator import Validator


class ValidatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Validator
        fields = '__all__'
        read_only_fields = all_field_names(Validator)
