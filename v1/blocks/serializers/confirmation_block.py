from django.db import transaction
from rest_framework import serializers
from thenewboston.blocks.signatures import verify_signature
from thenewboston.constants.network import (
    ACCEPTED,
    BLOCK_IDENTIFIER_LENGTH,
    PENDING,
    SIGNATURE_LENGTH,
    VERIFY_KEY_LENGTH
)
from thenewboston.serializers.block import BlockSerializer
from thenewboston.utils.fields import all_field_names
from thenewboston.utils.tools import sort_and_encode

from v1.members.models.member import Member
from v1.registrations.models.member_registration import MemberRegistration
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
        Create confirmation block
        If the inner blocks account number relates to a pending MemberRegistration:
        - create Member
        - update MemberRegistration to accepted
        """

        block_identifier = validated_data['block_identifier']
        network_identifier = validated_data['network_identifier']

        inner_block = validated_data['block']
        inner_block_account_number = inner_block['account_number']
        inner_block_signature = inner_block['signature']

        block = Block.objects.get(signature=inner_block_signature)
        validator = Validator.objects.get(network_identifier=network_identifier)

        try:
            with transaction.atomic():
                confirmation_block = ConfirmationBlock.objects.create(
                    block=block,
                    block_identifier=block_identifier,
                    validator=validator
                )
                member_registration = MemberRegistration.objects.filter(
                    account_number=inner_block_account_number,
                    status=PENDING
                )

                if member_registration:
                    member = Member.objects.create(
                        account_number=inner_block_account_number,
                        trust=50
                    )
                    member_registration.update(member=member, status=ACCEPTED)
        except Exception as e:
            print(e)

        return confirmation_block

    def update(self, instance, validated_data):
        raise RuntimeError('Method unavailable')

    def validate(self, data):
        """
        Validate signature
        """

        block = data['block']
        network_identifier = data['network_identifier']
        signature = data['signature']

        verify_signature(
            message=sort_and_encode(block),
            signature=signature,
            verify_key=network_identifier
        )

        return data

    @staticmethod
    def validate_network_identifier(network_identifier):
        """
        Validate that network_identifier belongs to validator
        """

        if not Validator.objects.filter(network_identifier=network_identifier).exists():
            raise serializers.ValidationError('Validator with that network_identifier does not exist')

        return network_identifier
