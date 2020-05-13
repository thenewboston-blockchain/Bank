from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Validator(models.Model):
    ip_address = models.GenericIPAddressField()
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
        return f'{self.id} | {self.ip_address} | {self.trust}'
