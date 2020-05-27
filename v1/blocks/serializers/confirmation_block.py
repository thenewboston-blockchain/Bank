from rest_framework import serializers
from thenewboston.constants.network import BLOCK_IDENTIFIER_LENGTH, SIGNATURE_LENGTH, VERIFY_KEY_LENGTH
from thenewboston.serializers.block import BlockSerializer
from thenewboston.utils.fields import all_field_names

from v1.validators.models.validator import Validator
from ..models.block import Block
from ..models.confirmation_block import ConfirmationBlock


class ConfirmationBlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfirmationBlock
        fields = '__all__'
        read_only_fields = all_field_names(ConfirmationBlock)


class ConfirmationBlockSerializerCreate(serializers.Serializer):
    block = BlockSerializer()
    block_identifier = serializers.CharField(max_length=BLOCK_IDENTIFIER_LENGTH)
    network_identifier = serializers.CharField(max_length=VERIFY_KEY_LENGTH)
    signature = serializers.CharField(max_length=SIGNATURE_LENGTH)

    def create(self, validated_data):
        """
        Create
        """

        block_identifier = validated_data['block_identifier']
        inner_block = validated_data['block']
        inner_block_signature = inner_block['signature']
        network_identifier = validated_data['network_identifier']

        block = Block.objects.get(signature=inner_block_signature)
        validator = Validator.objects.get(network_identifier=network_identifier)
        confirmation_block = ConfirmationBlock.objects.create(
            block=block,
            block_identifier=block_identifier,
            validator=validator
        )

        return confirmation_block

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    def validate(self, data):
        """
        Validate
        """

        # TODO: Check NID is from PV or BUV
        # TODO: Validate signature from validator (PV or BUV)

        return data
