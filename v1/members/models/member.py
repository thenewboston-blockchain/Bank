from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from v1.network.models.created_modified import CreatedModified


class Member(CreatedModified):
    identifier = models.CharField(max_length=256, unique=True)
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
        default_related_name = 'members'

    def __str__(self):
        return (
            f'ID: {self.id} | '
            f'Identifier: {self.identifier} | '
            f'Trust: {self.trust}'
        )
