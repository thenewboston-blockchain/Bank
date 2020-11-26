from rest_framework import serializers
from thenewboston.constants.network import CONFIRMATION_VALIDATOR
from thenewboston.serializers.configuration import ConfigurationSerializer

from .primary_validator_configuration import PrimaryValidatorConfigurationSerializer

"""
The ValidatorConfigurationSerializer is used to ensure that the requesting validator is properly configured
- used during the connection process
"""


class ValidatorConfigurationSerializer(ConfigurationSerializer):
    primary_validator = PrimaryValidatorConfigurationSerializer()

    @staticmethod
    def validate_node_type(node_type):
        """Validate node type"""
        if node_type != CONFIRMATION_VALIDATOR:
            raise serializers.ValidationError('Incorrect node_type')

        return node_type
