from rest_framework import serializers
from thenewboston.constants.network import VERIFY_KEY_LENGTH
from thenewboston.utils.fields import all_field_names

from thenewboston_bank.validators.models.validator import Validator
from ..models.validator_confirmation_service import ValidatorConfirmationService


class ValidatorConfirmationServiceSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = ValidatorConfirmationService
        read_only_fields = all_field_names(ValidatorConfirmationService)


class ValidatorConfirmationServiceSerializerCreate(serializers.Serializer):
    end = serializers.DateTimeField()
    node_identifier = serializers.CharField(max_length=VERIFY_KEY_LENGTH)
    start = serializers.DateTimeField()

    def create(self, validated_data):
        """Create validator confirmation service"""
        validator_confirmation_service = ValidatorConfirmationService.objects.create(
            end=validated_data['end'],
            start=validated_data['start'],
            validator=validated_data['node_identifier'],
        )

        return validator_confirmation_service

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    @staticmethod
    def validate_node_identifier(node_identifier):
        """Validate that node_identifier belongs to validator"""
        validator = Validator.objects.filter(node_identifier=node_identifier).first()

        if not validator:
            raise serializers.ValidationError('Validator with that node_identifier does not exist')

        return validator
