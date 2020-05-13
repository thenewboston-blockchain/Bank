from django.db import models


class Validator(models.Model):
    ip_address = models.CharField(max_length=256)

    class Meta:
        default_related_name = 'validators'

    def __str__(self):
        return f'{self.id} | {self.ip_address}'
