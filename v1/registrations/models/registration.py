from django.db import models

from v1.constants.models import DECLINED, REGISTRATION_STATUS_CHOICES
from v1.general.models.created_modified import CreatedModified
from v1.utils.validators import validate_is_real_number


class Registration(CreatedModified):
    fee = models.FloatField(blank=True, null=True, validators=[validate_is_real_number])
    status = models.CharField(choices=REGISTRATION_STATUS_CHOICES, default=DECLINED, max_length=8)

    class Meta:
        abstract = True
