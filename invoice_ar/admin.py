from django.contrib import admin
from reversion.admin import VersionAdmin

from invoice_ar import models


class ContactInvoiceARAdmin(VersionAdmin):
    pass


class CompanyInvoiceARAdmin(VersionAdmin):
    pass


class PointOfSaleAdmin(VersionAdmin):
    pass


class InvoiceTypeAdmin(VersionAdmin):
    pass


class InvoiceARAdmin(VersionAdmin):
    pass


class InvoiceARHasVATSubtypeAdmin(VersionAdmin):
    pass


admin.site.register(models.ContactInvoiceAR, ContactInvoiceARAdmin)
admin.site.register(models.CompanyInvoiceAR, CompanyInvoiceARAdmin)
admin.site.register(models.PointOfSale, PointOfSaleAdmin)
admin.site.register(models.InvoiceType, InvoiceTypeAdmin)
admin.site.register(models.InvoiceAR, InvoiceARAdmin)
admin.site.register(InvoiceARHasVATSubtype, InvoiceARHasVATSubtype)
