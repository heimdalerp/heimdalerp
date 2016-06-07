from django.contrib import admin
from reversion.admin import VersionAdmin

from invoice import models


class FiscalPositionAdmin(VersionAdmin):
    pass


class CompanyInvoiceAdmin(VersionAdmin):
    pass


class ContactInvoiceAdmin(VersionAdmin):
    pass


class VATAdmin(VersionAdmin):
    pass


class ProductAdmin(VersionAdmin):
    pass


class InvoiceLineAdmin(VersionAdmin):
    pass


class InvoiceTypeAdmin(VersionAdmin):
    pass


class InvoiceAdmin(VersionAdmin):
    pass


admin.site.register(models.FiscalPosition, FiscalPositionAdmin)
admin.site.register(models.CompanyInvoice, CompanyInvoiceAdmin)
admin.site.register(models.ContactInvoice, ContactInvoiceAdmin)
admin.site.register(models.VAT, VATAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.InvoiceLine, InvoiceLineAdmin)
admin.site.register(models.InvoiceType, InvoiceTypeAdmin)
admin.site.register(models.Invoice, InvoiceAdmin)
