from django.contrib import admin
from reversion.admin import VersionAdmin

from invoice_ar import models


class ContactInvoiceARAdmin(VersionAdmin):
    pass


class CompanyInvoiceARAdmin(VersionAdmin):
    pass


admin.site.register(models.ContactInvoiceAR, ContactInvoiceARAdmin)
admin.site.register(models.CompanyInvoiceAR, CompanyInvoiceARAdmin)
