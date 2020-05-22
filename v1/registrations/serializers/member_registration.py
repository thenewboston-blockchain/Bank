from rest_framework import serializers
from thenewboston.blocks.validation import validate_block
from thenewboston.constants.network import PENDING
from thenewboston.serializers.network_transaction import NetworkTransactionSerializer
from thenewboston.utils.serializers import all_field_names

from v1.members.models.member import Member
from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.validators.helpers.validator_configuration import get_primary_validator
from ..models.member_registration import MemberRegistration


class MemberRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = MemberRegistration
        fields = '__all__'
        read_only_fields = all_field_names(MemberRegistration)


class MemberRegistrationSerializerCreate(serializers.Serializer):
    account_number = serializers.CharField(max_length=256)
    balance_lock = serializers.CharField(max_length=64)
    signature = serializers.CharField(max_length=256)
    txs = NetworkTransactionSerializer(many=True)

    def create(self, validated_data):
        """
        Create pending member registration
        Forward block to validator
        """

        bank_registration_fee = validated_data['bank_registration_fee']
        block = validated_data['block']

        member_registration = MemberRegistration.objects.create(
            account_number=block['account_number'],
            fee=bank_registration_fee,
            status=PENDING
        )

        # TODO: Send to validator
        # TODO: If it comes back OK, the member is accepted into the bank
        print(block)

        return member_registration

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    @staticmethod
    def _validate_tx_exists(*, amount, recipient, txs):
        """
        Check for the existence of a Tx
        """

        tx = next((tx for tx in txs if tx.get('amount') == amount and tx.get('recipient') == recipient), None)
        if not tx:
            raise serializers.ValidationError({
                'error_message': 'Tx not found',
                'expected_amount': amount,
                'expected_recipient': recipient
            })

    @staticmethod
    def _validate_txs_length(*, bank_registration_fee, txs, validator_transaction_fee):
        """
        Verify that there are not an excessive amount of Txs
        """

        fees = [fee for fee in [bank_registration_fee, validator_transaction_fee] if fee != 0]
        if len(txs) > len(fees):
            raise serializers.ValidationError({
                'error_message': 'Invalid Txs',
                'bank_registration_fee': bank_registration_fee,
                'validator_transaction_fee': validator_transaction_fee
            })

    def validate(self, data):
        """
        Validate block:
        - Tx formatting
        - Tx chaining
        - signature
        """

        tx_details = data['txs']
        bank_registration_fee = tx_details['bank_registration_fee']

        block = {
            'account_number': data['account_number'],
            'signature': data['signature'],
            'txs': self.initial_data['txs']
        }

        validate_block(
            allow_empty_txs=True,
            balance_lock=data['balance_lock'],
            block=block
        )

        return {
            'bank_registration_fee': bank_registration_fee,
            'block': block
        }

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

    def validate_txs(self, txs):
        """
        Check that Txs exist
        - if both Bank and Validator charge 0 fees, return empty list
        Verify that correct payment exist for both Bank and Validator
        Verify that there are no extra payments
        """

        self_configuration = get_self_configuration(exception_class=RuntimeError)
        primary_validator = get_primary_validator()

        bank_registration_fee = self_configuration.registration_fee
        validator_transaction_fee = primary_validator.default_transaction_fee

        if bank_registration_fee == 0 and validator_transaction_fee == 0:
            self._validate_txs_length(
                bank_registration_fee=bank_registration_fee,
                txs=txs,
                validator_transaction_fee=validator_transaction_fee
            )
            return {
                'bank_registration_fee': 0,
                'txs': txs
            }

        if not txs:
            raise serializers.ValidationError('Invalid Txs')

        if len(txs) > 2:
            raise serializers.ValidationError('Length of Txs should never be greater than 2')

        if bank_registration_fee:
            self._validate_tx_exists(
                amount=bank_registration_fee,
                recipient=self_configuration.account_number,
                txs=txs
            )

        if validator_transaction_fee:
            self._validate_tx_exists(
                amount=validator_transaction_fee,
                recipient=primary_validator.account_number,
                txs=txs
            )

        self._validate_txs_length(
            bank_registration_fee=bank_registration_fee,
            txs=txs,
            validator_transaction_fee=validator_transaction_fee
        )

        return {
            'bank_registration_fee': bank_registration_fee,
            'txs': txs
        }
