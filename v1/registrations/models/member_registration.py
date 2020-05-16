from django.db import models

from v1.members.models.member import Member
from v1.network.models.network_registration import NetworkRegistration


class MemberRegistration(NetworkRegistration):
    identifier = models.CharField(max_length=256)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        default_related_name = 'member_registrations'

    def __str__(self):
        return (
            f'ID: {self.id} | '
            f'Identifier: {self.identifier} | '
            f'Status: {self.status}'
        )
