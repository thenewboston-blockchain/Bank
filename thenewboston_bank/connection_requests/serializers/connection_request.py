import logging

from rest_framework import serializers
from thenewboston.constants.network import (
    BANK,
    CONFIRMATION_VALIDATOR,
    PRIMARY_VALIDATOR,
    PROTOCOL_CHOICES,
    VERIFY_KEY_LENGTH
)
from thenewboston.utils.format import format_address
from thenewboston.utils.network import fetch

from thenewboston_bank.banks.models.bank import Bank
from thenewboston_bank.self_configurations.models.self_configuration import SelfConfiguration
from thenewboston_bank.validators.helpers.validator_configuration import (
    create_bank_from_config_data,
    create_validator_from_config_data
)
from thenewboston_bank.validators.models.validator import Validator
from .bank_configuration import BankConfigurationSerializer
from .validator_configuration import ValidatorConfigurationSerializer

logger = logging.getLogger('thenewboston')


class ConnectionRequestSerializerCreate(serializers.Serializer):
    ip_address = serializers.IPAddressField(protocol='both')
    node_identifier = serializers.CharField(max_length=VERIFY_KEY_LENGTH)
    port = serializers.IntegerField(allow_null=True, max_value=65535, min_value=0, required=False)
    protocol = serializers.ChoiceField(choices=PROTOCOL_CHOICES)

    def create(self, validated_data):
        """Process validated connection request"""
        if validated_data['node_type'] == BANK:
            create_bank_from_config_data(config_data=validated_data)

        if validated_data['node_type'] == CONFIRMATION_VALIDATOR:
            create_validator_from_config_data(config_data=validated_data)

        return True

    @staticmethod
    def get_node_config(data):
        """
        Attempt to connect to node

        Return nodes config data after validation
        """
        ip_address = data['ip_address']
        protocol = data['protocol']

        try:
            address = format_address(
                ip_address=ip_address,
                port=data.get('port'),
                protocol=protocol
            )
            config_address = f'{address}/config'
            config_data = fetch(url=config_address, headers={})

            if config_data['node_type'] == BANK:
                config_serializer = BankConfigurationSerializer(data=config_data)
            elif config_data['node_type'] == CONFIRMATION_VALIDATOR:
                config_serializer = ValidatorConfigurationSerializer(data=config_data)
            elif config_data['node_type'] == PRIMARY_VALIDATOR:
                raise serializers.ValidationError('Unable to accept connection requests from primary validators')
            else:
                raise serializers.ValidationError('Invalid node_type')
        except Exception as e:
            logger.exception(e)
            raise e

        if config_serializer.is_valid():
            return config_data
        else:
            logger.exception(config_serializer.errors)
            raise serializers.ValidationError(config_serializer.errors)

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    def validate(self, data):
        """Attempt to connect to node"""
        ip_address = data['ip_address']
        protocol = data['protocol']
        port = data.get('port', '')

        if Bank.objects.filter(ip_address=ip_address, protocol=protocol, port=port).exists():
            raise serializers.ValidationError('Already connected to bank')

        if SelfConfiguration.objects.filter(ip_address=ip_address, protocol=protocol, port=port).exists():
            raise serializers.ValidationError('Unable to connect to self')

        if Validator.objects.filter(ip_address=ip_address, protocol=protocol, port=port).exists():
            raise serializers.ValidationError('Already connected to validator')

        return self.get_node_config(data)

    @staticmethod
    def validate_node_identifier(node_identifier):
        """Validate node_identifier length"""
        if len(node_identifier) != VERIFY_KEY_LENGTH:
            raise serializers.ValidationError(f'node_identifier must be {VERIFY_KEY_LENGTH} characters long')

        if Bank.objects.filter(node_identifier=node_identifier).exists():
            raise serializers.ValidationError('Bank with that node identifier already exists')

        if Validator.objects.filter(node_identifier=node_identifier).exists():
            raise serializers.ValidationError('Validator with that node identifier already exists')

        return node_identifier
