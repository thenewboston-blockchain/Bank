from django.contrib import admin

from .models.validator import Validator
from .models.validator_transaction_fee_tier import ValidatorTransactionFeeTier

admin.site.register(Validator)
admin.site.register(ValidatorTransactionFeeTier)
