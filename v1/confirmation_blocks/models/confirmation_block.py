from django.db import models
from thenewboston.constants.network import BLOCK_IDENTIFIER_LENGTH
from thenewboston.models.created_modified import CreatedModified

from v1.blocks.models.block import Block
from v1.validators.models.validator import Validator


class ConfirmationBlock(CreatedModified):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    validator = models.ForeignKey(Validator, on_delete=models.CASCADE)
    block_identifier = models.CharField(max_length=BLOCK_IDENTIFIER_LENGTH)

    class Meta:
        default_related_name = 'confirmation_blocks'
        constraints = [
            models.UniqueConstraint(
                fields=['block', 'validator'],
                name='unique_block_validator'
            )
        ]

    def __str__(self):
        return (
            f'ID: {self.id} | '
            f'Block: {self.block_id} | '
            f'Validator: {self.validator_id}'
        )
