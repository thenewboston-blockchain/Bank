from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from v1.constants.models import BANK, NODE_TYPE_CHOICES
from v1.utils.validators import validate_is_real_number


class NodeConfiguration(models.Model):
    identifier = models.CharField(max_length=256)
    node_type = models.CharField(choices=NODE_TYPE_CHOICES, default=BANK, max_length=4)
    version = models.CharField(max_length=32)

    # Fees
    default_tx_fee = models.DecimalField(
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
        default_related_name = 'node_configurations'

    def __str__(self):
        return f'{self.id}'

    def clean(self):
        """
        Ensure only one NodeConfiguration exists
        """

        if not self.id and NodeConfiguration.objects.exists():
            raise ValidationError('Only one NodeConfiguration allowed')

    def save(self, *args, **kwargs):
        """
        Ensure only one NodeConfiguration exists
        """

        if not self.id and NodeConfiguration.objects.exists():
            raise RuntimeError('Only one NodeConfiguration allowed')

        super().save(*args, **kwargs)
