from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from v1.general.models.transaction_fee_tier import TransactionFeeTier
from .self_configuration import SelfConfiguration


class SelfTransactionFeeTier(TransactionFeeTier):
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
        default_related_name = 'self_transaction_fee_tiers'

    def __str__(self):
        return f'{self.trust} | {self.fee}'

    def _validate(self, error):
        """
        Ensure fee is higher than than default transaction fee
        """

        self_configuration = SelfConfiguration.objects.first()
        default_transaction_fee = self_configuration.default_transaction_fee

        if not self_configuration:
            raise error('SelfConfiguration required')

        if self.fee <= default_transaction_fee:
            raise error(f'Fee must be higher than default transaction fee of {default_transaction_fee}')

    def clean(self):
        self._validate(ValidationError)

    def save(self, *args, **kwargs):
        self._validate(RuntimeError)
        super().save(*args, **kwargs)
