from django.core.validators import MinValueValidator
from django.db import models

from v1.general.models.created_modified import CreatedModified
from v1.utils.validators import validate_is_real_number

"""
created_date - Not stored on the network transaction log, stored by bank for member reference only
modified_date - Not stored on the network transaction log, stored by bank for member reference only
validated - Boolean indicating if the Tx had been validated by the primary validator

Note: If the Tx does not pass validation from the bank itself, the object is never stored in the database
"""


class Transaction(CreatedModified):
    amount = models.DecimalField(
        decimal_places=16,
        default=0,
        max_digits=32,
        validators=[
            MinValueValidator(0),
            validate_is_real_number
        ]
    )
    balance_key = models.CharField(max_length=256)
    recipient = models.CharField(max_length=256)
    sender = models.CharField(max_length=256)
    signature = models.CharField(max_length=256)
    validated = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'transactions'

    def __str__(self):
        return f'{self.id}'
