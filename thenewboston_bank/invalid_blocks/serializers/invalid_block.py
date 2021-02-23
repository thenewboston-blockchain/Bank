import logging

from rest_framework import serializers
from thenewboston.constants.network import BLOCK_IDENTIFIER_LENGTH, SIGNATURE_LENGTH, VERIFY_KEY_LENGTH
from thenewboston.serializers.network_block import NetworkBlockSerializer
from thenewboston.utils.fields import all_field_names

from thenewboston_bank.blocks.models.block import Block
from thenewboston_bank.tasks.sync import set_primary_validator
from thenewboston_bank.utils.trust import calculate_weighted_trust, decrease_trust
from thenewboston_bank.validators.helpers.validator_configuration import get_primary_validator
from thenewboston_bank.validators.models.validator import Validator
from ..models.invalid_block import InvalidBlock

logger = logging.getLogger('thenewboston')


class InvalidBlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvalidBlock
        fields = '__all__'
        read_only_fields = all_field_names(InvalidBlock)


class InvalidBlockMessageSerializer(serializers.Serializer):
    block = NetworkBlockSerializer()
    block_identifier = serializers.CharField(max_length=BLOCK_IDENTIFIER_LENGTH)
    primary_validator_node_identifier = serializers.CharField(max_length=VERIFY_KEY_LENGTH)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @staticmethod
    def validate_primary_validator_node_identifier(primary_validator_node_identifier):
        """Validate that primary_validator_node_identifier belongs to primary validator"""
        primary_validator = get_primary_validator()

        if primary_validator_node_identifier != primary_validator.node_identifier:
            raise serializers.ValidationError(
                'The primary_validator_node_identifier does not belong to the primary validator'
            )

        return primary_validator


class InvalidBlockSerializerCreate(serializers.Serializer):
    message = InvalidBlockMessageSerializer()
    node_identifier = serializers.CharField(max_length=VERIFY_KEY_LENGTH)
    signature = serializers.CharField(max_length=SIGNATURE_LENGTH)

    def create(self, validated_data):
        """Create invalid block"""
        message = validated_data['message']
        confirmation_validator = validated_data['node_identifier']

        primary_validator = message['primary_validator_node_identifier']
        block_identifier = message['block_identifier']
        inner_block = message['block']
        inner_block_signature = inner_block['signature']

        try:
            invalid_block = InvalidBlock(
                block_identifier=block_identifier,
                confirmation_validator=confirmation_validator,
                primary_validator=primary_validator
            )

            block = Block.objects.filter(signature=inner_block_signature).first()

            if block:
                invalid_block.block = block

            invalid_block.save()

            weighted_trust = calculate_weighted_trust(
                node=confirmation_validator,
                node_list=Validator.objects.all().exclude(pk=primary_validator.id)
            )
            decrease_trust(
                amount=weighted_trust,
                node=primary_validator
            )
            set_primary_validator.delay()
        except Exception as e:
            logger.exception(e)
            raise serializers.ValidationError(e)

        return invalid_block

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    @staticmethod
    def validate_node_identifier(node_identifier):
        """Validate that node_identifier belongs to a connected validator"""
        validator = Validator.objects.filter(node_identifier=node_identifier).first()

        if not validator:
            raise serializers.ValidationError('Validator with that node_identifier does not exist')

        return validator
