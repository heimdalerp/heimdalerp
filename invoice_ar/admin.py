from django.contrib import admin

from reversion.admin import VersionAdmin

from invoice import models


class ClientARAdmin(VersionAdmin):
    pass


class CompanyInvoiceARAdmin(VersionAdmin):
    pass


admin.site.register(models.ClientAR, ClientARAdmin)
admin.site.register(models.CompanyInvoiceAR, CompanyInvoiceAR)

