from rest_framework import serializers
from thenewboston.constants.network import VERIFY_KEY_LENGTH

from thenewboston_bank.notifications.status_updates import send_primary_validator_updated_notification
from thenewboston_bank.self_configurations.helpers.self_configuration import get_self_configuration
from thenewboston_bank.tasks.sync import send_primary_validator_updated_notices
from thenewboston_bank.validators.models.validator import Validator


class UpgradeNoticeSerializer(serializers.Serializer):
    bank_node_identifier = serializers.CharField(max_length=VERIFY_KEY_LENGTH)
    node_identifier = serializers.CharField(max_length=VERIFY_KEY_LENGTH)

    def create(self, validated_data):
        """
        If validator is more trusted than the current primary validator:

        - switch to the new primary validator

        If validator is less trusted than the current primary validator:

        - delete the requesting validator (which is now on different network)
        """
        validator = validated_data['node_identifier']
        self_configuration = get_self_configuration(exception_class=RuntimeError)
        current_primary_validator = self_configuration.primary_validator

        if current_primary_validator == validator:
            return True

        if current_primary_validator.trust < validator.trust:
            self_configuration.primary_validator = validator
            self_configuration.save()
            send_primary_validator_updated_notices.delay()
            send_primary_validator_updated_notification()
            return True

        validator.delete()
        raise serializers.ValidationError('Networks out of sync')

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        """
        Check that self node_identifier matches bank_node_identifier

        - this ensures that the request was intended for self
        """
        self_configuration = get_self_configuration(exception_class=RuntimeError)
        self_node_identifier = self_configuration.node_identifier
        bank_node_identifier = data['bank_node_identifier']

        if self_node_identifier != bank_node_identifier:
            raise serializers.ValidationError(
                f'self_node_identifier of {self_node_identifier} does not match '
                f'bank_node_identifier of {bank_node_identifier}'
            )

        return data

    @staticmethod
    def validate_node_identifier(node_identifier):
        """Validate node_identifier is from validator"""
        validator = Validator.objects.filter(node_identifier=node_identifier).first()

        if not validator:
            raise serializers.ValidationError('Validator with that node identifier does not exists')

        return validator
