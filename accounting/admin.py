from django.contrib import admin
from reversion.admin import VersionAdmin

from accounting import models


class LedgerAdmin(VersionAdmin):
    pass


class AccountAdmin(VersionAdmin):
    pass


class AccountSubtypeAdmin(VersionAdmin):
    pass


class TransactionAdmin(VersionAdmin):
    pass


class PaymentAdmin(VersionAdmin):
    pass

admin.site.register(models.Ledger, LedgerAdmin)
admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.AccountSubtype, AccountSubtypeAdmin)
admin.site.register(models.Transaction, TransactionAdmin)
admin.site.register(models.Payment, PaymentAdmin)
