from accounting import models
from django.contrib import admin
from reversion.admin import VersionAdmin


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


@admin.register(models.CompanyAccounting)
class CompanyAccountingAdmin(VersionAdmin):
    pass
