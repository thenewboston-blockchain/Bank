from django.core.validators import MinValueValidator
from django.db import models

from v1.utils.validators import validate_is_real_number


class TransactionFeeTier(models.Model):
    fee = models.DecimalField(
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
