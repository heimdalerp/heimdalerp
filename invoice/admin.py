from django.contrib import admin
from reversion.admin import VersionAdmin

from invoice import models


@admin.register(models.FiscalPosition)
class FiscalPositionAdmin(VersionAdmin):
    pass


@admin.register(models.CompanyInvoice)
class CompanyInvoiceAdmin(VersionAdmin):
    pass


@admin.register(models.ContactInvoice)
class ContactInvoiceAdmin(VersionAdmin):
    pass


@admin.register(models.VAT)
class VATAdmin(VersionAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(VersionAdmin):
    pass


@admin.register(models.InvoiceLine)
class InvoiceLineAdmin(VersionAdmin):
    pass


@admin.register(models.InvoiceType)
class InvoiceTypeAdmin(VersionAdmin):
    pass


@admin.register(models.Invoice)
class InvoiceAdmin(VersionAdmin):
    pass
