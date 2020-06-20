from rest_framework import serializers
from thenewboston.blocks.signatures import verify_signature
from thenewboston.constants.network import PENDING, VERIFY_KEY_LENGTH
from thenewboston.serializers.network_block import NetworkBlockSerializer
from thenewboston.transactions.validation import validate_transaction_exists
from thenewboston.utils.fields import all_field_names
from thenewboston.utils.tools import sort_and_encode

from v1.validators.models.validator import Validator
from ..models.bank_registration import BankRegistration


class BankRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankRegistration
        fields = '__all__'
        read_only_fields = all_field_names(BankRegistration)


class BankRegistrationSerializerCreate(serializers.Serializer):
    block = NetworkBlockSerializer()
    validator_network_identifier = serializers.CharField(max_length=VERIFY_KEY_LENGTH)

    def create(self, validated_data):
        """
        Create bank registration
        Forward block to validator
        """

        block = validated_data['block']
        validator = validated_data['validator']
        print(block)

        bank_registration = BankRegistration.objects.create(
            fee=validator.registration_fee,
            status=PENDING,
            validator=validator
        )

        return bank_registration

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    def validate(self, data):
        """
        Validate block signature
        Verify that correct payment exist for Validator registration fee

        Note: when building the block, message is pulled from 'initial_data' since 'data' has already been processed by
        the NetworkBlockSerializer converting all amounts to DecimalField (which are not JSON serializable)
        """

        block = self.initial_data['block']
        validator = data['validator_network_identifier']

        verify_signature(
            message=sort_and_encode(block['message']),
            signature=block['signature'],
            verify_key=block['account_number']
        )

        validate_transaction_exists(
            amount=validator.registration_fee,
            error=serializers.ValidationError,
            recipient=validator.account_number,
            txs=block['message']['txs']
        )

        return {
            'block': block,
            'validator': validator
        }

    @staticmethod
    def validate_validator_network_identifier(validator_network_identifier):
        """
        Ensure validator_network_identifier matches known validator NID
        Check for existing pending registration
        """

        validator = Validator.objects.filter(network_identifier=validator_network_identifier).first()

        if not validator:
            raise serializers.ValidationError(
                f'Could not find validator with validator_network_identifier {validator_network_identifier}'
            )

        if BankRegistration.objects.filter(status=PENDING, validator=validator).exists():
            raise serializers.ValidationError('Pending registration already exists')

        return validator


class BankRegistrationSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = BankRegistration
        fields = ('status',)
