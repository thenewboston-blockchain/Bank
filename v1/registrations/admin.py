from django.contrib import admin

from .models.member_registration import MemberRegistration
from .models.validator_registration import ValidatorRegistration

admin.site.register(MemberRegistration)
admin.site.register(ValidatorRegistration)
