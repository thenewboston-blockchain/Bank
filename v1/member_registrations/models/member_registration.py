from django.db import models
from thenewboston.constants.network import VERIFY_KEY_LENGTH
from thenewboston.models.network_registration import NetworkRegistration

from v1.members.models.member import Member


class MemberRegistration(NetworkRegistration):
    account_number = models.CharField(max_length=VERIFY_KEY_LENGTH)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        default_related_name = 'member_registrations'

    def __str__(self):
        return (
            f'ID: {self.id} | '
            f'Account number: {self.account_number} | '
            f'Status: {self.status}'
        )