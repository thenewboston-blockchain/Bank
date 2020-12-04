from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from thenewboston.models.network_validator import NetworkValidator


class Validator(NetworkValidator):
    trust = models.DecimalField(
        decimal_places=2,
        default=0,
        max_digits=5,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    class Meta(NetworkValidator.Meta):
        default_related_name = 'validators'

    def __str__(self):
        return (
            f'ID: {self.id} | '
            f'IP address: {self.ip_address} | '
            f'Port: {self.port} | '
            f'Trust: {self.trust}'
        )
