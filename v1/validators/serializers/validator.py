from rest_framework import serializers

from ..models.validator import Validator


class ValidatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Validator
        fields = '__all__'
