from django.contrib import admin
from reversion.admin import VersionAdmin

from accounting import models


@admin.register(models.Ledger)
class LedgerAdmin(VersionAdmin):
    pass


@admin.register(models.Account)
class AccountAdmin(VersionAdmin):
    pass


@admin.register(models.Transaction)
class TransactionAdmin(VersionAdmin):
    pass


@admin.register(models.Payment)
class PaymentAdmin(VersionAdmin):
    pass
