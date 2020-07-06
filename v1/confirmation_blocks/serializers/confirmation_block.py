import logging

from django.db import transaction
from rest_framework import serializers
from thenewboston.constants.network import SIGNATURE_LENGTH, VERIFY_KEY_LENGTH
from thenewboston.serializers.confirmation_block_message import ConfirmationBlockMessageSerializer
from thenewboston.utils.fields import all_field_names

from v1.blocks.models.block import Block
from v1.validators.models.validator import Validator
from ..models.confirmation_block import ConfirmationBlock

logger = logging.getLogger('thenewboston')


class ConfirmationBlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfirmationBlock
        fields = '__all__'
        read_only_fields = all_field_names(ConfirmationBlock)


class ConfirmationBlockSerializerCreate(serializers.Serializer):
    message = ConfirmationBlockMessageSerializer()
    node_identifier = serializers.CharField(max_length=VERIFY_KEY_LENGTH)
    signature = serializers.CharField(max_length=SIGNATURE_LENGTH)

    def create(self, validated_data):
        """
        Create confirmation block
        """

        message = validated_data['message']
        block_identifier = message['block_identifier']
        validator = validated_data['node_identifier']

        inner_block = message['block']
        inner_block_signature = inner_block['signature']

        block = Block.objects.get(signature=inner_block_signature)

        try:
            with transaction.atomic():
                confirmation_block = ConfirmationBlock.objects.create(
                    block=block,
                    block_identifier=block_identifier,
                    validator=validator
                )
        except Exception as e:
            logger.exception(e)
            raise serializers.ValidationError(e)

        return confirmation_block

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    @staticmethod
    def validate_node_identifier(node_identifier):
        """
        Validate that node_identifier belongs to validator
        """

        validator = Validator.objects.filter(node_identifier=node_identifier).first()

        if not validator:
            raise serializers.ValidationError('Validator with that node_identifier does not exist')

        return validator
