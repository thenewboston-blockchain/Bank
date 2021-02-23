from uuid import uuid4

from django.db import models
from thenewboston.constants.network import BLOCK_IDENTIFIER_LENGTH
from thenewboston.models.created_modified import CreatedModified

from thenewboston_bank.blocks.models.block import Block
from thenewboston_bank.validators.models.validator import Validator

"""
The block FK will be set if the bank has a record of the block (meaning it was originated at this bank)
"""


class InvalidBlock(CreatedModified):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)  # noqa: A003
    block = models.ForeignKey(Block, on_delete=models.CASCADE, blank=True, null=True)
    confirmation_validator = models.ForeignKey(
        Validator,
        on_delete=models.CASCADE,
        related_name='confirmation_validator_invalid_blocks'
    )
    primary_validator = models.ForeignKey(
        Validator,
        on_delete=models.CASCADE,
        related_name='primary_validator_invalid_blocks'
    )
    block_identifier = models.CharField(max_length=BLOCK_IDENTIFIER_LENGTH)

    class Meta:
        default_related_name = 'invalid_blocks'
        constraints = [
            models.UniqueConstraint(
                fields=['confirmation_validator', 'primary_validator'],
                name='unique_confirmation_validator_primary_validator'
            )
        ]

    def __str__(self):
        return (
            f'ID: {self.id} | '
            f'block_identifier: {self.block_identifier}'
        )
