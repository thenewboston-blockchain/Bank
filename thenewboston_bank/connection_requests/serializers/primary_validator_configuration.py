from rest_framework import serializers
from thenewboston.constants.network import PRIMARY_VALIDATOR
from thenewboston.serializers.primary_validator import PrimaryValidatorSerializer

from thenewboston_bank.self_configurations.helpers.self_configuration import get_self_configuration
from thenewboston_bank.self_configurations.serializers.self_configuration import SelfConfigurationSerializer
from thenewboston_bank.validators.serializers.validator import ValidatorSerializer

"""
The PrimaryValidatorConfigurationSerializer is used to ensure that the requesting nodes primary validator is:
- properly configured
- matches self primary validator
"""


class PrimaryValidatorConfigurationSerializer(PrimaryValidatorSerializer):

    def validate(self, requesting_node_primary_validator_configuration):
        """Validate that requesting nodes primary validator matches self primary validator"""
        self_configuration = get_self_configuration(exception_class=RuntimeError)

        if self_configuration.node_type == PRIMARY_VALIDATOR:
            self_primary_validator_configuration = SelfConfigurationSerializer(self_configuration).data
        else:
            primary_validator = self_configuration.primary_validator
            self_primary_validator_configuration = ValidatorSerializer(primary_validator).data

        for key in ['account_number', 'ip_address', 'node_identifier', 'protocol']:
            requesting_node_value = requesting_node_primary_validator_configuration.get(key)
            self_primary_validator_value = self_primary_validator_configuration.get(key)

            if requesting_node_value is None:
                raise serializers.ValidationError(f'{key} not found on requesting nodes primary validator')

            if str(requesting_node_value) != str(self_primary_validator_value):
                raise serializers.ValidationError(
                    f'Inconsistent primary validator settings for {key}. '
                    f'Requesting nodes value of {requesting_node_value} '
                    f'does not match expected value of {self_primary_validator_value}.'
                )

        return requesting_node_primary_validator_configuration
