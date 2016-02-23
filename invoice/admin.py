from django.contrib import admin

from reversion.admin import VersionAdmin

from invoice import models


class FiscalPositionAdmin(VersionAdmin):
    pass


class CompanyAdmin(VersionAdmin):
    pass


class ClientAdmin(VersionAdmin):
    pass


class VATAdmin(VersionAdmin):
    pass


class InvoiceProductAdmin(VersionAdmin):
    pass


class InvoiceLineAdmin(VersionAdmin):
    pass


class InvoiceAdmin(VersionAdmin):
    pass


admin.site.register(models.FiscalPosition, FiscalPositionAdmin)
admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.VAT, VATAdmin)
admin.site.register(models.InvoiceProduct, InvoiceProductAdmin)
admin.site.register(models.InvoiceLine, InvoiceLineAdmin)
admin.site.register(models.Invoice, InvoiceAdmin)

