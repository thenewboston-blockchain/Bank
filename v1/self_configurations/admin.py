from django.contrib import admin

from .models.self_configuration import SelfConfiguration
from .models.self_transaction_fee_tier import SelfTransactionFeeTier

admin.site.register(SelfConfiguration)
admin.site.register(SelfTransactionFeeTier)
