from django.core.validators import MinValueValidator
from django.db import models

from v1.utils.validators import validate_is_real_number


class Node(models.Model):
    identifier = models.CharField(max_length=256)
    version = models.CharField(max_length=32)

    # Fees
    default_transaction_fee = models.DecimalField(
        decimal_places=16,
        default=0,
        max_digits=32,
        validators=[
            MinValueValidator(0),
            validate_is_real_number
        ]
    )
    registration_fee = models.DecimalField(
        decimal_places=16,
        default=0,
        max_digits=32,
        validators=[
            MinValueValidator(0),
            validate_is_real_number
        ]
    )

    class Meta:
        abstract = True
