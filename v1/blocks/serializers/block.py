import logging

from django.db import transaction
from rest_framework import serializers
from thenewboston.blocks.signatures import verify_signature
from thenewboston.serializers.network_block import NetworkBlockSerializer
from thenewboston.transactions.validation import validate_transaction_exists
from thenewboston.utils.fields import all_field_names
from thenewboston.utils.tools import sort_and_encode

from v1.accounts.models.account import Account
from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.tasks.blocks import send_signed_block
from v1.utils.blocks import create_block_and_bank_transactions
from v1.validators.helpers.validator_configuration import get_primary_validator
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
                block = create_block_and_bank_transactions(validated_block)
                Account.objects.get_or_create(
                    account_number=validated_block['account_number'],
                    defaults={'trust': 0},
                )
                send_signed_block.delay(
                    block=validated_block,
                    ip_address=primary_validator.ip_address,
                    port=primary_validator.port,
                    protocol=primary_validator.protocol,
                    url_path='/bank_blocks'
                )
        except Exception as e:
            logger.exception(e)
            raise serializers.ValidationError(e)

        return block

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    def validate(self, data):
        """
        Validate block signature

        Note: when building the block, message is pulled from 'initial_data' since 'data' has already been processed by
        the MessageSerializer converting all amounts to IntegerField
        """

        block = {
            'account_number': data['account_number'],
            'message': self.initial_data['message'],
            'signature': data['signature']
        }
        verify_signature(
            message=sort_and_encode(block['message']),
            signature=block['signature'],
            verify_key=block['account_number']
        )
        return block

    @staticmethod
    def validate_message(message):
        """
        Check that Txs exist
        Verify that correct payment exist for both Bank and Validator
        """

        self_configuration = get_self_configuration(exception_class=RuntimeError)
        primary_validator = get_primary_validator()

        bank_default_transaction_fee = self_configuration.default_transaction_fee
        validator_transaction_fee = primary_validator.default_transaction_fee

        txs = message['txs']

        if not txs:
            raise serializers.ValidationError('Invalid Txs')

        validate_transaction_exists(
            amount=bank_default_transaction_fee,
            error=serializers.ValidationError,
            recipient=self_configuration.account_number,
            txs=txs
        )
        validate_transaction_exists(
            amount=validator_transaction_fee,
            error=serializers.ValidationError,
            recipient=primary_validator.account_number,
            txs=txs
        )

        return txs
