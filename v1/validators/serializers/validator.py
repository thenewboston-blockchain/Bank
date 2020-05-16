from rest_framework import serializers

from v1.utils.serializers import all_field_names
from ..models.validator import Validator


class ValidatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Validator
        fields = all_field_names(Validator)
