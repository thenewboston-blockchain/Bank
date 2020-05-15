from django.contrib import admin

from .models.node_configuration import NodeConfiguration
from .models.transaction_fee_tier import TransactionFeeTier

admin.site.register(NodeConfiguration)
admin.site.register(TransactionFeeTier)
