import logging

from django.db import transaction
from rest_framework import serializers
from thenewboston.constants.network import SIGNATURE_LENGTH, VERIFY_KEY_LENGTH
from thenewboston.serializers.confirmation_block_message import ConfirmationBlockMessageSerializer
from thenewboston.utils.fields import all_field_names

from thenewboston_bank.blocks.models.block import Block
from thenewboston_bank.notifications.confirmation_blocks import send_confirmation_block_notifications
from thenewboston_bank.utils.blocks import create_block_and_related_objects
from thenewboston_bank.validators.models.validator import Validator
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
        """Create confirmation block"""
        message = validated_data['message']
        block_identifier = message['block_identifier']
        validator = validated_data['node_identifier']

        inner_block = message['block']
        inner_block_account_number = inner_block['account_number']
        inner_block_recipients = {tx['recipient'] for tx in inner_block['message']['txs']}

        confirmation_block = self.create_confirmation_block(
            block_identifier=block_identifier,
            inner_block=inner_block,
            validator=validator
        )

        send_confirmation_block_notifications(
            payload=self.initial_data,
            sender_account_number=inner_block_account_number,
            recipient_account_numbers=inner_block_recipients
        )

        return confirmation_block

    @staticmethod
    def create_confirmation_block(*, block_identifier, inner_block, validator):
        """
        Create block, confirmation block, bank transactions, and account if necessary

        - when a block is sent through a bank it will create and store the related block, bank transactions, and account
        - when a block is sent through another bank, the bank that receives the confirmation block may not have that
        information
        - this related information is helpful when users set this bank as their new active bank (since it will already
        have their entire transaction history)
        """
        inner_block_signature = inner_block['signature']
        block = Block.objects.filter(signature=inner_block_signature).first()
        confirmation_block = ConfirmationBlock(
            block=block,
            block_identifier=block_identifier,
            validator=validator
        )

        if not block:
            create_block_and_related_objects(inner_block)
            return confirmation_block

        try:
            with transaction.atomic():
                confirmation_block.save()
                return confirmation_block
        except Exception as e:
            logger.exception(e)
            raise serializers.ValidationError(e)

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    @staticmethod
    def validate_node_identifier(node_identifier):
        """Validate that node_identifier belongs to validator"""
        validator = Validator.objects.filter(node_identifier=node_identifier).first()

        if not validator:
            raise serializers.ValidationError('Validator with that node_identifier does not exist')

        return validator
