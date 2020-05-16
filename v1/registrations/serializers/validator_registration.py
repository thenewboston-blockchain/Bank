from rest_framework import serializers

from v1.utils.serializers import all_field_names
from ..models.validator_registration import ValidatorRegistration


class ValidatorRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ValidatorRegistration
        fields = all_field_names(ValidatorRegistration)
