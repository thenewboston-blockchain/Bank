from rest_framework import serializers
from thenewboston.utils.fields import all_field_names

from v1.tasks.sync import set_primary_validator
from ..models.validator import Validator


class ValidatorSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Validator
        read_only_fields = all_field_names(Validator)


class ValidatorSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Validator
        fields = ('trust',)

    def update(self, instance, validated_data):
        """
        Check to see if new primary validator needs set due to updated trust levels
        """

        instance = super().update(instance, validated_data)
        set_primary_validator.delay()
        return instance
