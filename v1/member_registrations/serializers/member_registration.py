from django.db import transaction
from rest_framework import serializers
from thenewboston.blocks.validation import validate_block
from thenewboston.constants.network import BALANCE_LOCK_LENGTH, PENDING, SIGNATURE_LENGTH, VERIFY_KEY_LENGTH
from thenewboston.serializers.network_transaction import NetworkTransactionSerializer
from thenewboston.transactions.validation import validate_transaction_exists
from thenewboston.utils.fields import all_field_names

from v1.members.models.member import Member
from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.tasks.blocks import sign_and_send_block
from v1.utils.blocks import create_block_and_bank_transactions
from v1.validators.helpers.validator_configuration import get_primary_validator
from ..models.member_registration import MemberRegistration


class MemberRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = MemberRegistration
        fields = '__all__'
        read_only_fields = all_field_names(MemberRegistration)


class MemberRegistrationSerializerCreate(serializers.Serializer):
    account_number = serializers.CharField(max_length=VERIFY_KEY_LENGTH)
    balance_lock = serializers.CharField(max_length=BALANCE_LOCK_LENGTH)
    signature = serializers.CharField(max_length=SIGNATURE_LENGTH)
    txs = NetworkTransactionSerializer(many=True)

    def create(self, validated_data):
        """
        Create pending member registration
        Forward block to validator
        """

        validated_block = validated_data
        self_configuration = get_self_configuration(exception_class=RuntimeError)
        bank_registration_fee = self_configuration.registration_fee
        primary_validator = self_configuration.primary_validator

        try:
            with transaction.atomic():
                create_block_and_bank_transactions(validated_block)
                member_registration = MemberRegistration.objects.create(
                    account_number=validated_block['account_number'],
                    fee=bank_registration_fee,
                    status=PENDING
                )
                sign_and_send_block.delay(
                    block=validated_block,
                    ip_address=primary_validator.ip_address,
                    port=primary_validator.port,
                    protocol=primary_validator.protocol,
                    url_path='/bank_blocks'
                )
        except Exception as e:
            print(e)

        return member_registration

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    def validate(self, data):
        """
        Validate block:
        - Tx formatting
        - Tx chaining
        - signature

        Note: when building the block, txs are pulled from 'initial_data' since 'data' has already been processed by
        the NetworkTransactionSerializer converting all amounts to DecimalField (which are not JSON serializable)
        """

        block = {
            'account_number': data['account_number'],
            'signature': data['signature'],
            'txs': self.initial_data['txs']
        }
        validate_block(balance_lock=data['balance_lock'], block=block)
        return block

    @staticmethod
    def validate_account_number(account_number):
        """
        Check if member already exists
        Check for existing pending registration
        """

        if Member.objects.filter(account_number=account_number).exists():
            raise serializers.ValidationError('Member already exists')

        if MemberRegistration.objects.filter(account_number=account_number, status=PENDING).exists():
            raise serializers.ValidationError('Pending registration already exists')

        return account_number

    @staticmethod
    def validate_txs(txs):
        """
        Check that the correct number of Txs exist
        Verify that correct payment exist for both Bank and Validator
        """

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

        return txs
