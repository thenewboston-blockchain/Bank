from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from v1.utils.validators import validate_is_real_number
from .node_configuration import NodeConfiguration


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
    trust = models.DecimalField(
        decimal_places=2,
        default=0,
        max_digits=5,
        unique=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    class Meta:
        default_related_name = 'node_configurations'

    def __str__(self):
        return f'{self.trust} | {self.fee}'

    def _validate(self, error):
        """
        Ensure fee is higher than than default transaction fee
        """

        node_configuration = NodeConfiguration.objects.first()
        default_transaction_fee = node_configuration.default_transaction_fee

        if not node_configuration:
            raise error('NodeConfiguration required')

        if self.fee <= default_transaction_fee:
            raise error(f'Fee must be higher than default transaction fee of {default_transaction_fee}')

    def clean(self):
        self._validate(ValidationError)

    def save(self, *args, **kwargs):
        self._validate(RuntimeError)
        super().save(*args, **kwargs)
