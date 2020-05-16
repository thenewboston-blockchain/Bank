from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from v1.general.models.node import Node


class Validator(Node):
    ip_address = models.GenericIPAddressField(unique=True)
    primary = models.BooleanField(default=False)
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
        default_related_name = 'validators'

    def __str__(self):
        return (
            f'ID: {self.id} | '
            f'IP Address: {self.ip_address} | '
            f'Trust: {self.trust} | '
            f'Primary: {self.primary}'
        )
