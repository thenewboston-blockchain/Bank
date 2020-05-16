from decimal import Decimal

from rest_framework import serializers

from v1.constants.models import PENDING
from v1.members.models.member import Member
from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.utils.serializers import all_field_names
from v1.validators.helpers.validator_configuration import get_primary_validator_configuration
from ..models.member_registration import MemberRegistration


class MemberRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = MemberRegistration
        fields = all_field_names(MemberRegistration)


class TransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=32, decimal_places=16)
    balance_key = serializers.CharField(max_length=256)
    recipient = serializers.CharField(max_length=256)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @staticmethod
    def validate_amount(amount):
        """
        Check that amount is not 0
        """

        if amount == 0:
            raise serializers.ValidationError('Tx amount can not be 0 (Tx should be excluded)')

        return amount


class MemberRegistrationSerializerCreate(serializers.Serializer):
    signature = serializers.CharField(max_length=256)
    txs = TransactionSerializer(many=True, required=True)
    verifying_key_hex = serializers.CharField(max_length=256)

    def create(self, validated_data):
        """
        Create member registration
        Forward block to validator
        """

        tx_details = validated_data['txs']
        txs = tx_details['txs']

        member_registration = MemberRegistration.objects.create(
            identifier=validated_data['verifying_key_hex'],
            fee=tx_details['bank_registration_fee']
        )

        # TODO: Send to validator
        print({
            'signature': validated_data['signature'],
            'txs': txs,
            'verifying_key_hex': validated_data['verifying_key_hex']
        })

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
                'amount': amount,
                'recipient': recipient
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

    @staticmethod
    def validate_verifying_key_hex(verifying_key_hex):
        """
        Check if member already exists
        Check for existing pending registration
        """

        if Member.objects.filter(identifier=verifying_key_hex).exists():
            raise serializers.ValidationError('Member already exists')

        if MemberRegistration.objects.filter(identifier=verifying_key_hex, status=PENDING).exists():
            raise serializers.ValidationError('Pending registration already exists')

        return verifying_key_hex

    def validate_txs(self, txs):
        """
        Check that Txs exist
        Verify that correct payment exist for both Bank and Validator
        Verify that there are no extra payments
        """

        # TODO: Handle logic for when both bank and validators charge 0 fees
        # TODO: Further split up validation functions

        if not txs:
            raise serializers.ValidationError('Invalid Txs')

        if len(txs) > 2:
            raise serializers.ValidationError('Length of Txs should never be greater than 2')

        bank_configuration = get_self_configuration()
        bank_registration_fee = bank_configuration.registration_fee

        if bank_registration_fee:
            self._validate_tx_exists(
                amount=bank_registration_fee,
                recipient=bank_configuration.identifier,
                txs=txs
            )

        # TODO: Consider storing all validator configurations the same as node configuration, in database
        # TODO: This will allow treating all values the same (rather than strings vs decimals)

        validator_configuration = get_primary_validator_configuration()
        validator_transaction_fee = validator_configuration['transaction_fee']
        validator_transaction_fee = Decimal(validator_transaction_fee)

        if validator_transaction_fee:
            self._validate_tx_exists(
                amount=validator_transaction_fee,
                recipient=validator_configuration['identifier'],
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
