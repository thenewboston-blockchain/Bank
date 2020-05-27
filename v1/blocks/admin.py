from django.contrib import admin

from .models.block import Block
from .models.confirmation_block import ConfirmationBlock

admin.site.register(Block)
admin.site.register(ConfirmationBlock)
