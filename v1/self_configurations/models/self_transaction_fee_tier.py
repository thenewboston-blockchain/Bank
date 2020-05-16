from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from v1.network.models.network_transaction_fee_tier import NetworkTransactionFeeTier
from v1.self_configurations.helpers.self_configuration import get_self_configuration


class SelfTransactionFeeTier(NetworkTransactionFeeTier):
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
        return (
            f'Trust: {self.trust} | '
            f'Fee: {self.fee}'
        )

    def _validate(self, exception_class):
        """
        Ensure fee is higher than than default transaction fee
        """

        self_configuration = get_self_configuration(exception_class=exception_class)
        default_transaction_fee = self_configuration.default_transaction_fee

        if self.fee <= default_transaction_fee:
            raise exception_class(f'Fee must be higher than default transaction fee of {default_transaction_fee}')

    def clean(self):
        self._validate(ValidationError)

    def save(self, *args, **kwargs):
        self._validate(RuntimeError)
        super().save(*args, **kwargs)
