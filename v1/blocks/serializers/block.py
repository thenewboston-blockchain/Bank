from django.db import transaction
from rest_framework import serializers
from thenewboston.blocks.signatures import verify_signature
from thenewboston.serializers.network_block import NetworkBlockSerializer
from thenewboston.transactions.validation import validate_transaction_exists
from thenewboston.utils.fields import all_field_names
from thenewboston.utils.tools import sort_and_encode

from v1.members.models.member import Member
from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.tasks.blocks import sign_and_send_block
from v1.utils.blocks import create_block_and_bank_transactions
from v1.validators.helpers.validator_configuration import get_primary_validator
from ..models.block import Block


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
                sign_and_send_block.delay(
                    block=validated_block,
                    ip_address=primary_validator.ip_address,
                    port=primary_validator.port,
                    protocol=primary_validator.protocol,
                    url_path='/bank_blocks'
                )
        except Exception as e:
            print(e)

        return block

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    def validate(self, data):
        """
        Validate signature

        Note: when building the block, txs are pulled from 'initial_data' since 'data' has already been processed by
        the NetworkTransactionSerializer converting all amounts to DecimalField (which are not JSON serializable)
        """

        account_number = data['account_number']
        signature = data['signature']
        txs = self.initial_data['txs']

        verify_signature(
            message=sort_and_encode(txs),
            signature=signature,
            verify_key=account_number
        )

        block = {
            'account_number': data['account_number'],
            'signature': data['signature'],
            'txs': self.initial_data['txs']
        }

        return block

    @staticmethod
    def validated_account_number(account_number):
        """
        Check account number belongs to a registered member
        """

        if not Member.objects.filter(account_number=account_number).exists():
            raise serializers.ValidationError('Member with that account number does not exist')

        return account_number

    @staticmethod
    def validate_txs(txs):
        """
        Check that Txs exist
        Verify that correct payment exist for both Bank and Validator
        """

        self_configuration = get_self_configuration(exception_class=RuntimeError)
        primary_validator = get_primary_validator()

        bank_registration_fee = self_configuration.registration_fee
        validator_transaction_fee = primary_validator.default_transaction_fee

        if not txs:
            raise serializers.ValidationError('Invalid Txs')

        validate_transaction_exists(
            amount=bank_registration_fee,
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
