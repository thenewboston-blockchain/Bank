from django.contrib import admin

from .models.bank_registration import BankRegistration
from .models.member_registration import MemberRegistration

admin.site.register(BankRegistration)
admin.site.register(MemberRegistration)
