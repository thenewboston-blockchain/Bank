from rest_framework import serializers

from ..models.validator_registration import ValidatorRegistration


class ValidatorRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ValidatorRegistration
        fields = '__all__'
