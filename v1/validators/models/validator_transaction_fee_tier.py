from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from thenewboston.models.network_transaction_fee_tier import NetworkTransactionFeeTier
from .validator import Validator


class ValidatorTransactionFeeTier(NetworkTransactionFeeTier):
    validator = models.ForeignKey(Validator, on_delete=models.CASCADE)
    trust = models.DecimalField(
        decimal_places=2,
        default=0,
        max_digits=5,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    class Meta:
        default_related_name = 'validator_transaction_fee_tiers'
        unique_together = ('validator', 'trust')

    def __str__(self):
        return (
            f'ID: {self.id} | '
            f'Trust: {self.trust} | '
            f'Fee: {self.fee}'
        )
