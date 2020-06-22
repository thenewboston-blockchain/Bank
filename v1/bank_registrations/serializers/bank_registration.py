import logging

from django.db import transaction
from rest_framework import serializers
from thenewboston.blocks.signatures import verify_signature
from thenewboston.constants.network import PENDING, VERIFY_KEY_LENGTH
from thenewboston.serializers.network_block import NetworkBlockSerializer
from thenewboston.transactions.validation import validate_transaction_exists
from thenewboston.utils.fields import all_field_names
from thenewboston.utils.tools import sort_and_encode

from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.tasks.signed_requests import send_signed_post_request
from v1.validators.models.validator import Validator
from ..models.bank_registration import BankRegistration

logger = logging.getLogger('thenewboston')


class BankRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankRegistration
        fields = '__all__'
        read_only_fields = all_field_names(BankRegistration)


class BankRegistrationSerializerCreate(serializers.Serializer):
    block = NetworkBlockSerializer()
    validator_node_identifier = serializers.CharField(max_length=VERIFY_KEY_LENGTH)

    def create(self, validated_data):
        """
        Create bank registration
        Forward block to validator
        """

        block = validated_data['block']
        validator = validated_data['validator']

        try:
            with transaction.atomic():
                bank_registration = BankRegistration.objects.create(
                    fee=validator.registration_fee,
                    status=PENDING,
                    validator=validator
                )
                self_configuration = get_self_configuration(exception_class=RuntimeError)
                send_signed_post_request.delay(
                    data={
                        'block': block,
                        'ip_address': self_configuration.ip_address,
                        'port': self_configuration.port,
                        'protocol': self_configuration.protocol,
                        'source_bank_registration_pk': str(bank_registration.pk),
                        'validator_node_identifier': validator.node_identifier,
                        'version': self_configuration.version
                    },
                    ip_address=validator.ip_address,
                    port=validator.port,
                    protocol=validator.protocol,
                    url_path='/bank_registrations'
                )
        except Exception as e:
            logger.exception(e)

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
        validator = data['validator_node_identifier']

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
    def validate_validator_node_identifier(validator_node_identifier):
        """
        Ensure validator_node_identifier matches known validator NID
        Check for existing pending registration
        """

        validator = Validator.objects.filter(node_identifier=validator_node_identifier).first()

        if not validator:
            raise serializers.ValidationError(
                f'Could not find validator with validator_node_identifier {validator_node_identifier}'
            )

        if BankRegistration.objects.filter(status=PENDING, validator=validator).exists():
            raise serializers.ValidationError('Pending registration already exists')

        return validator


class BankRegistrationSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = BankRegistration
        fields = ('status',)
