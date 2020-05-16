from django.contrib import admin

from .models.transaction import Transaction

admin.site.register(Transaction)
