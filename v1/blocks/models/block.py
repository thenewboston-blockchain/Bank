from uuid import uuid4

from django.db import models
from thenewboston.constants.network import BALANCE_LOCK_LENGTH, SIGNATURE_LENGTH, VERIFY_KEY_LENGTH
from thenewboston.models.created_modified import CreatedModified

"""
created_date - Not stored on the network, stored by bank for reference only
modified_date - Not stored on the network, stored by bank for reference only
"""


class Block(CreatedModified):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)  # noqa: A003
    balance_key = models.CharField(max_length=BALANCE_LOCK_LENGTH, unique=True)
    sender = models.CharField(max_length=VERIFY_KEY_LENGTH)
    signature = models.CharField(max_length=SIGNATURE_LENGTH, unique=True)

    class Meta:
        default_related_name = 'blocks'

    def __str__(self):
        return (
            f'ID: {self.id} | '
            f'Sender: {self.sender} | '
            f'Signature: {self.signature}'
        )
