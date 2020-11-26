from rest_framework import serializers
from thenewboston.constants.network import BANK
from thenewboston.serializers.configuration import ConfigurationSerializer

from .primary_validator_configuration import PrimaryValidatorConfigurationSerializer

"""
The BankConfigurationSerializer is used to ensure that the requesting bank is properly configured
- used during the connection process
"""


class BankConfigurationSerializer(ConfigurationSerializer):
    primary_validator = PrimaryValidatorConfigurationSerializer()

    @staticmethod
    def validate_node_type(node_type):
        """Validate node type"""
        if node_type != BANK:
            raise serializers.ValidationError('Incorrect node_type')

        return node_type
