from django.contrib import admin

from .views.bank_transaction import BankTransaction

admin.site.register(BankTransaction)
