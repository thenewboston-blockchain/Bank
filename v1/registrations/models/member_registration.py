from django.db import models

from v1.members.models.member import Member
from .registration import Registration


class MemberRegistration(Registration):
    identifier = models.CharField(max_length=256, unique=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        default_related_name = 'member_registrations'

    def __str__(self):
        return f'{self.id} | {self.identifier} | {self.status}'
