from django.db import models
from thenewboston.constants.network import SIGNATURE_LENGTH, VERIFY_KEY_LENGTH
from thenewboston.models.created_modified import CreatedModified

"""
created_date - Not stored on the network, stored by bank for member reference only
modified_date - Not stored on the network, stored by bank for member reference only
"""


class Block(CreatedModified):
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
