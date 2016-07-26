from django.contrib import admin
from invoice_ar import models
from reversion.admin import VersionAdmin


@admin.register(models.ContactInvoiceAR)
class ContactInvoiceARAdmin(VersionAdmin):
    pass


@admin.register(models.CompanyInvoiceAR)
class CompanyInvoiceARAdmin(VersionAdmin):
    pass


@admin.register(models.PointOfSale)
class PointOfSaleAdmin(VersionAdmin):
    pass


@admin.register(models.ConceptType)
class ConceptTypeAdmin(VersionAdmin):
    pass


@admin.register(models.InvoiceAR)
class InvoiceARAdmin(VersionAdmin):
    pass


@admin.register(models.InvoiceARHasVATSubtotal)
class InvoiceARHasVATSubtotalAdmin(VersionAdmin):
    pass
