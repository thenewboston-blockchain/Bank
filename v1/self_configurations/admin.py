from django.contrib import admin

from .models.self_configuration import SelfConfiguration
from .models.transaction_fee_tier import TransactionFeeTier

admin.site.register(SelfConfiguration)
admin.site.register(TransactionFeeTier)
