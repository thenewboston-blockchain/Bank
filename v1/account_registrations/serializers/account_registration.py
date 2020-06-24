import logging

from django.db import transaction
from rest_framework import serializers
from thenewboston.blocks.signatures import verify_signature
from thenewboston.constants.network import PENDING, SIGNATURE_LENGTH, VERIFY_KEY_LENGTH
from thenewboston.serializers.message import MessageSerializer
from thenewboston.transactions.validation import validate_transaction_exists
from thenewboston.utils.fields import all_field_names
from thenewboston.utils.tools import sort_and_encode

from v1.accounts.models.account import Account
from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.tasks.blocks import send_signed_block
from v1.utils.blocks import create_block_and_bank_transactions
from v1.validators.helpers.validator_configuration import get_primary_validator
from ..models.account_registration import AccountRegistration

logger = logging.getLogger('thenewboston')


class AccountRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountRegistration
        fields = '__all__'
        read_only_fields = all_field_names(AccountRegistration)


class AccountRegistrationSerializerCreate(serializers.Serializer):
    account_number = serializers.CharField(max_length=VERIFY_KEY_LENGTH)
    message = MessageSerializer()
    signature = serializers.CharField(max_length=SIGNATURE_LENGTH)

    def create(self, validated_data):
        """
        Create pending account registration
        Forward block to validator
        """

        validated_block = validated_data
        self_configuration = get_self_configuration(exception_class=RuntimeError)
        bank_registration_fee = self_configuration.registration_fee
        primary_validator = self_configuration.primary_validator

        try:
            with transaction.atomic():
                create_block_and_bank_transactions(validated_block)
                account_registration = AccountRegistration.objects.create(
                    account_number=validated_block['account_number'],
                    fee=bank_registration_fee,
                    status=PENDING
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

        return account_registration

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    def validate(self, data):
        """
        Validate block signature

        Note: when building the block, message is pulled from 'initial_data' since 'data' has already been processed by
        the MessageSerializer converting all amounts to DecimalField (which are not JSON serializable)
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
    def validate_account_number(account_number):
        """
        Check if account already exists
        Check for existing pending registration
        """

        if Account.objects.filter(account_number=account_number).exists():
            raise serializers.ValidationError('Account already exists')

        if AccountRegistration.objects.filter(account_number=account_number, status=PENDING).exists():
            raise serializers.ValidationError('Pending registration already exists')

        return account_number

    @staticmethod
    def validate_message(message):
        """
        Check that the correct number of Txs exist
        Verify that correct payment exist for both Bank and Validator
        """

        txs = message['txs']
        self_configuration = get_self_configuration(exception_class=RuntimeError)
        primary_validator = get_primary_validator()
        bank_registration_fee = self_configuration.registration_fee
        validator_transaction_fee = primary_validator.default_transaction_fee

        if len(txs) != 2:
            raise serializers.ValidationError(f'Expecting 2 transactions, found {len(txs)}')

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

        return message
