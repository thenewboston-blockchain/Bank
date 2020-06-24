from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from thenewboston.constants.network import BALANCE_LOCK_LENGTH, VERIFY_KEY_LENGTH
from thenewboston.models.created_modified import CreatedModified
from thenewboston.utils.validators import validate_is_real_number


class Account(CreatedModified):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    account_number = models.CharField(max_length=VERIFY_KEY_LENGTH, unique=True)
    balance = models.DecimalField(
        decimal_places=16,
        default=0,
        max_digits=32,
        validators=[
            MinValueValidator(0),
            validate_is_real_number
        ]
    )
    balance_lock = models.CharField(max_length=BALANCE_LOCK_LENGTH, unique=True)
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
        default_related_name = 'accounts'

    def __str__(self):
        return (
            f'Account Number: {self.account_number} | '
            f'Balance: {self.balance} | '
            f'Balance Lock: {self.balance_lock} | '
            f'Trust: {self.trust}'
        )
