import logging

from django.db import transaction
from rest_framework import serializers
from thenewboston.constants.network import BANK, PRIMARY_VALIDATOR
from thenewboston.serializers.network_block import NetworkBlockSerializer
from thenewboston.transactions.validation import validate_transaction_exists
from thenewboston.utils.fields import all_field_names

from thenewboston_bank.self_configurations.helpers.self_configuration import get_self_configuration
from thenewboston_bank.tasks.blocks import send_signed_block
from thenewboston_bank.utils.blocks import create_block_and_related_objects
from thenewboston_bank.validators.helpers.validator_configuration import get_primary_validator
from ..models.block import Block

logger = logging.getLogger('thenewboston')


class BlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Block
        fields = '__all__'
        read_only_fields = all_field_names(Block)


class BlockSerializerCreate(NetworkBlockSerializer):

    def create(self, validated_data):
        """
        Create block and bank transactions

        Forward block to validator
        """
        validated_block = validated_data
        self_configuration = get_self_configuration(exception_class=RuntimeError)
        primary_validator = self_configuration.primary_validator

        try:
            with transaction.atomic():
                block, created = create_block_and_related_objects(validated_block)
                send_signed_block.delay(
                    block=validated_block,
                    ip_address=primary_validator.ip_address,
                    port=primary_validator.port,
                    protocol=primary_validator.protocol,
                    url_path='/bank_blocks'
                )
        except serializers.ValidationError as e:
            logger.exception(e)
            raise e
        except Exception as e:
            logger.exception(e)
            raise serializers.ValidationError(e)

        return block

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    def validate(self, data):
        """Verify that correct payment exist for both Bank and Validator"""
        data = super(BlockSerializerCreate, self).validate(data)

        account_number = data['account_number']
        message = data['message']
        txs = message['txs']

        self_configuration = get_self_configuration(exception_class=RuntimeError)
        primary_validator = get_primary_validator()

        if account_number != self_configuration.account_number:
            validate_transaction_exists(
                amount=self_configuration.default_transaction_fee,
                fee=BANK,
                error=serializers.ValidationError,
                recipient=self_configuration.account_number,
                txs=txs
            )

        if account_number != primary_validator.account_number:
            validate_transaction_exists(
                amount=primary_validator.default_transaction_fee,
                fee=PRIMARY_VALIDATOR,
                error=serializers.ValidationError,
                recipient=primary_validator.account_number,
                txs=txs
            )

        return data
